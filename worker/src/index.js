// TropeLang corpus CDN — Cloudflare Worker fronting the R2 bucket (spec 19 §6.2).
//
// The R2 object layout mirrors the URL paths, so most routes are a direct key lookup; the Worker's job
// is cache headers, CORS, integrity (ETag = manifest sha256), and the channel `resolve` convenience.
// Read-only: only GET/HEAD/OPTIONS. The publish pipeline (CI) is the sole writer.
//
// Routes:
//   GET /:id/:version/corpus.json     immutable bundle      Cache-Control: public, max-age=1y, immutable
//   GET /:id/:version/corpus.trlb     immutable fast-load   (same) — post-parse binary, pinned by trlbSha256
//   GET /:id/:version/manifest.json   immutable manifest    (same)
//   GET /channels/:id.:channel.json   mutable pointer       public, max-age=30, must-revalidate
//   GET /:id/versions.json            version catalog       public, max-age=30, must-revalidate
//   GET /:id/resolve?channel=stable   → that channel's manifest JSON   public, max-age=30
//   GET /registry.json                discovery index       public, max-age=60

const IMMUTABLE = "public, max-age=31536000, immutable";
const SHORT = "public, max-age=30, must-revalidate";
const REGISTRY = "public, max-age=60";

const CORS = {
  "Access-Control-Allow-Origin": "*", // read-only public data; no credentials
  "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
  "Access-Control-Allow-Headers": "*",
  "Access-Control-Max-Age": "86400",
};

const json = (body, status, headers) =>
  new Response(typeof body === "string" ? body : JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...CORS, ...headers },
  });

const notFound = (msg) => json({ error: msg || "not found" }, 404, { "Cache-Control": "public, max-age=10" });

// Serve an R2 object by key with the given Cache-Control. ETag comes from R2 (or the manifest sha256).
async function serve(env, key, cacheControl, request) {
  const obj = await env.CORPUS.get(key);
  if (!obj) return notFound(`no object: ${key}`);
  const headers = new Headers(CORS);
  headers.set("Cache-Control", cacheControl);
  headers.set("Content-Type", obj.httpMetadata?.contentType || "application/json; charset=utf-8");
  if (obj.httpEtag) headers.set("ETag", obj.httpEtag);
  // Conditional GET: honor If-None-Match for cheap revalidation of the short-TTL pointers.
  const inm = request.headers.get("If-None-Match");
  if (inm && obj.httpEtag && inm === obj.httpEtag) {
    return new Response(null, { status: 304, headers });
  }
  if (request.method === "HEAD") return new Response(null, { status: 200, headers });
  return new Response(obj.body, { status: 200, headers });
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
    if (request.method !== "GET" && request.method !== "HEAD") {
      return json({ error: "method not allowed" }, 405, { Allow: "GET, HEAD, OPTIONS" });
    }

    const url = new URL(request.url);
    const path = url.pathname.replace(/^\/+/, ""); // strip leading slash
    const parts = path.split("/").filter(Boolean);

    // GET /registry.json
    if (path === "registry.json") return serve(env, "registry.json", REGISTRY, request);

    // GET /channels/:id.:channel.json
    if (parts[0] === "channels" && parts.length === 2 && parts[1].endsWith(".json")) {
      return serve(env, `channels/${parts[1]}`, SHORT, request);
    }

    // GET /:id/versions.json   → engine-aware version catalog (mutable: grows on deploy, yanks on demand)
    if (parts.length === 2 && parts[1] === "versions.json") {
      return serve(env, `${parts[0]}/versions.json`, SHORT, request);
    }

    // GET /:id/resolve?channel=stable  → return the channel's pinned manifest JSON
    if (parts.length === 2 && parts[1] === "resolve") {
      const id = parts[0];
      const channel = url.searchParams.get("channel") || "stable";
      const ptrObj = await env.CORPUS.get(`channels/${id}.${channel}.json`);
      if (!ptrObj) return notFound(`no channel: ${id}.${channel}`);
      let ptr;
      try {
        ptr = JSON.parse(await ptrObj.text());
      } catch {
        return json({ error: "corrupt channel pointer" }, 502, { "Cache-Control": "no-store" });
      }
      // ptr.manifest is an absolute path like "/standard/1.7.0/manifest.json"
      const manifestKey = String(ptr.manifest || "").replace(/^\/+/, "");
      if (!manifestKey) return json({ error: "channel missing manifest pointer" }, 502, { "Cache-Control": "no-store" });
      return serve(env, manifestKey, SHORT, request);
    }

    // GET /:id/:version/corpus.json | corpus.trlb | manifest.json  (immutable)
    // corpus.trlb is the post-parse binary fast-load form the manifest pins via trlbSha256; it is served
    // with the same immutable cache policy as corpus.json (its Content-Type comes from R2 —
    // application/octet-stream, set at upload).
    if (parts.length === 3 && (parts[2] === "corpus.json" || parts[2] === "corpus.trlb" || parts[2] === "manifest.json")) {
      return serve(env, parts.join("/"), IMMUTABLE, request);
    }

    return notFound("unrecognized route");
  },
};

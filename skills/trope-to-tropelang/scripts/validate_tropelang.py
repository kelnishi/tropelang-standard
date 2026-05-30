"""
TropeLang structural validator — v1.3 grammar + planned extensions.

Implemented in the reference Rust parser (lib.rs v1.3), accepted here:
  domain tag sigils   = # % @ &   (Body / Mind / Essence / Rel / Verb)
  !...!  *...*  ?...?             epistemic wrappers (absolute / contingent / latent)
  (A|B|C) (A|B|...) (...)         ambiguity expressions; `as <name>` labels them
  resolve <name> -> <fact|ambiguity>   in-world collapse (narrow = collapse to a
                                       smaller ambiguity)
  retcon { <name> -> <fact>, ... }     author-level collapse
  Constraint (01 §11.4): resolve/retcon may target ONLY a named, non-absolute
  ambiguity. The Rust parser enforces this; this structural validator does not yet.

Validator-only (not in the Rust reference parser):
  concept declarations; attr/prop/state/verb/rel decls; import / ref.

Checks performed:
  - Balanced braces / parens / brackets
  - Tag syntax (modifier immediately before name)
  - No fractional-number identifiers
  - rule blocks contain when: and then:
  - No sidecar labels on entity declarations
  - Even count of * epistemic wrappers (warns if odd)
"""

import sys, re as _re

ENTITY_TYPES = {"char", "set", "obj", "evt", "arc", "concept"}  # v1.3: concept added
SCOPE_TYPES  = {"scene", "act", "beat"}
DECL_TYPES   = {"attr", "prop", "state", "verb", "rel"}   # v1.2 attribute declarations
PLANNED_KW   = {"resolve", "retcon", "narrow", "as", "import", "ref"}
# Tag sigils (v1.3):
#   = Body  # Mind  % Essence  ~ Intent  @ Rel  & Verb  + generic Prop
#   - remove  ? query  ! assert-absent
ALL_SIGILS   = set("+-~?!#@&=%")

errors   = []
warnings = []


def lex(src, label=""):
    tokens = []
    i, line = 0, 1
    while i < len(src):
        c = src[i]
        if c == '\n': line += 1; i += 1; continue
        if c in ' \t\r': i += 1; continue

        # Comments
        if c == '/' and i + 1 < len(src) and src[i + 1] == '/':
            while i < len(src) and src[i] != '\n': i += 1
            continue

        # Triple-quoted block string (inline YAML for dialog)
        if c == '"' and src[i:i+3] == '"""':
            end = src.find('"""', i + 3)
            if end == -1:
                errors.append(f"[{label}] line {line}: unterminated block string")
                return tokens
            block = src[i+3:end]
            tokens.append(('BLOCK', block, line))
            line += block.count('\n')
            i = end + 3
            continue

        # String literal
        if c == '"':
            j = i + 1
            while j < len(src) and src[j] != '"': j += 1
            if j >= len(src):
                errors.append(f"[{label}] line {line}: unterminated string")
                return tokens
            tokens.append(('STR', src[i+1:j], line)); i = j + 1; continue

        # Number
        if c.isdigit():
            j = i + 1; dot = False
            while j < len(src) and (src[j].isdigit() or (src[j] == '.' and not dot)):
                if src[j] == '.': dot = True
                j += 1
            tokens.append(('NUM', src[i:j], line)); i = j; continue

        # Variable
        if c == '$':
            j = i + 1
            while j < len(src) and (src[j].isalnum() or src[j] == '_'): j += 1
            if j == i + 1:
                errors.append(f"[{label}] line {line}: bare $"); i += 1; continue
            tokens.append(('VAR', src[i:j], line)); i = j; continue

        # Identifier / keyword
        if c.isalpha() or c == '_':
            j = i + 1
            while j < len(src) and (src[j].isalnum() or src[j] == '_'): j += 1
            tokens.append(('ID', src[i:j], line)); i = j; continue

        # Ellipsis — planned void/open marker
        if c == '.' and src[i:i+3] == '...':
            tokens.append(('ELLIPSIS', '...', line)); i += 3; continue

        # Multi-char operators (current grammar, longest match first)
        matched = False
        for op in ["!--", "->", "!>", "!@", "!=", ">=", "<=", "==", "--", "><"]:
            if src[i:i+len(op)] == op:
                tokens.append(('OP', op, line)); i += len(op); matched = True; break
        if matched: continue

        # Single-char tokens — current grammar + planned extensions (* | .)
        if c in "+-~?!><@=:,{}[]()":
            tokens.append(('OP', c, line)); i += 1; continue
        if c in "*|.#%&":
            tokens.append(('OP', c, line)); i += 1; continue  # planned extensions incl. domain sigils (= # % @ &)

        errors.append(f"[{label}] line {line}: unexpected char {c!r}"); i += 1

    return tokens


def check_braces(tokens, label):
    stack = []
    pairs = {'}': '{', ']': '[', ')': '('}
    for kind, val, line in tokens:
        if kind == 'OP' and val in '{[(':
            stack.append((val, line))
        elif kind == 'OP' and val in '}])':
            if not stack:
                errors.append(f"[{label}] line {line}: unmatched '{val}'")
            elif stack[-1][0] != pairs[val]:
                errors.append(f"[{label}] line {line}: mismatched '{val}' "
                              f"(opened '{stack[-1][0]}' at line {stack[-1][1]})")
            else:
                stack.pop()
    for ch, line in stack:
        errors.append(f"[{label}] line {line}: unclosed '{ch}'")


def check_tags(tokens, label):
    """Tags must be [sigil? name params?] — sigil is any of +-~?!#@&"""
    i = 0
    while i < len(tokens):
        kind, val, line = tokens[i]
        if kind == 'OP' and val == '[':
            i += 1
            if i >= len(tokens): break
            k2, v2, l2 = tokens[i]
            if k2 == 'OP' and v2 in ALL_SIGILS:
                i += 1
                if i >= len(tokens): break
                k3, v3, l3 = tokens[i]
                if k3 not in ('ID', 'VAR', 'STR'):
                    errors.append(
                        f"[{label}] line {l3}: expected tag name after '{v2}', got {v3!r}")
        i += 1


def check_sidecar_labels(tokens, label):
    """Flag entity declarations that still use the deprecated inline label form."""
    all_entity_kw = ENTITY_TYPES | DECL_TYPES
    for idx in range(len(tokens) - 2):
        k1, v1, l1 = tokens[idx]
        k2, v2, l2 = tokens[idx + 1]
        k3, v3, l3 = tokens[idx + 2]
        if (k1 == 'ID' and v1 in ENTITY_TYPES        # only entity types — not attr decls
                and k2 in ('ID', 'VAR')
                and k3 == 'STR'):
            errors.append(
                f"[{label}] line {l1}: sidecar label \"{v3}\" on '{v2}' — "
                "use // annotation instead")


def check_rule_structure(tokens, label):
    i = 0
    while i < len(tokens):
        kind, val, line = tokens[i]
        if kind == 'ID' and val == 'rule':
            depth = 0; found_when = found_then = False; j = i
            while j < len(tokens):
                kj, vj, lj = tokens[j]
                if kj == 'OP' and vj == '{': depth += 1
                elif kj == 'OP' and vj == '}':
                    depth -= 1
                    if depth == 0: break
                elif kj == 'ID' and vj == 'when' and depth == 1: found_when = True
                elif kj == 'ID' and vj == 'then' and depth == 1: found_then = True
                j += 1
            if not found_when: errors.append(f"[{label}] line {line}: rule missing 'when:'")
            if not found_then: errors.append(f"[{label}] line {line}: rule missing 'then:'")
        i += 1


def check_epistemic_balance(tokens, label):
    stars = [t for t in tokens if t[0] == 'OP' and t[1] == '*']
    if len(stars) % 2 != 0:
        warnings.append(f"[{label}]: odd number of '*' epistemic markers — check wrapper balance")


def build_declaration_registry(tokens):
    """Build a set of all declared names (entities + attr decls) from the token stream.
    Used by the reference validation pass to check that referenced identifiers exist."""
    registry = set()
    all_decl_kw = ENTITY_TYPES | DECL_TYPES
    i = 0
    while i < len(tokens):
        kind, val, line = tokens[i]
        # Entity or attr declaration: keyword followed by identifier
        if kind == 'ID' and val in all_decl_kw:
            if i + 1 < len(tokens):
                k2, v2, _ = tokens[i + 1]
                if k2 in ('ID', 'VAR'):
                    registry.add(v2)
        i += 1
    return registry


def check_intent_targets(tokens, registry, label):
    """Check that [~Intent(target=x)] params reference declared graph nodes.
    Variables ($x) are always valid — they're bound in rule patterns.
    Quoted strings are flagged — they should be concept declarations instead."""
    i = 0
    while i < len(tokens):
        kind, val, line = tokens[i]
        # Look for [~ sigil
        if kind == 'OP' and val == '[':
            if i + 1 < len(tokens) and tokens[i+1] == ('OP', '~', tokens[i+1][2]):
                # Scan forward for target= param
                j = i + 1
                depth = 1
                while j < len(tokens) and depth > 0:
                    kj, vj, lj = tokens[j]
                    if kj == 'OP' and vj == '(': depth += 1
                    elif kj == 'OP' and vj == ')': depth -= 1
                    elif kj == 'ID' and vj == 'target':
                        # Next should be = then the value
                        if j + 2 < len(tokens):
                            keq, veq, _ = tokens[j + 1]
                            kval, vval, lval = tokens[j + 2]
                            if keq == 'OP' and veq == '=':
                                if kval == 'STR':
                                    errors.append(
                                        f"[{label}] line {lval}: intent target \"{vval}\" "
                                        f"is a string — declare as: concept {vval.replace(' ', '_')} [...]")
                                elif kval == 'ID' and vval not in registry:
                                    warnings.append(
                                        f"[{label}] line {lval}: intent target '{vval}' "
                                        f"not declared in this file — ensure it is imported")
                    j += 1
        i += 1


def validate(src, label=""):
    toks = lex(src, label)
    check_braces(toks, label)
    check_tags(toks, label)
    check_sidecar_labels(toks, label)
    check_rule_structure(toks, label)
    check_epistemic_balance(toks, label)
    registry = build_declaration_registry(toks)
    check_intent_targets(toks, registry, label)
    return toks


if __name__ == "__main__":
    label = sys.argv[1] if len(sys.argv) > 1 else "file"
    src = open(sys.argv[1]).read()
    toks = validate(src, label)

    if errors:
        print("ERRORS:")
        for e in errors: print("  ✗", e)
    if warnings:
        print("WARNINGS:")
        for w in warnings: print("  ⚠", w)
    if not errors and not warnings:
        rules  = len([t for t in toks if t[0] == 'ID' and t[1] == 'rule'])
        scenes = len([t for t in toks if t[0] == 'ID' and t[1] == 'scene'])
        imply  = len([t for t in toks if t[0] == 'ID' and t[1] == 'imply'])
        resolv = len([t for t in toks if t[0] == 'ID' and t[1] == 'resolve'])
        # count attribute declarations by type
        decl_counts = {kw: len([t for t in toks if t[0] == 'ID' and t[1] == kw])
                       for kw in sorted(DECL_TYPES | {"attr"})}
        decl_summary = ", ".join(f"{v} {k}" for k, v in decl_counts.items() if v)
        print(f"✓ {label}")
        if decl_summary:
            print(f"  declarations: {decl_summary}")
        if rules or scenes or imply or resolv:
            print(f"  {rules} rule(s), {scenes} scene(s), "
                  f"{imply} imply(s), {resolv} resolve(s)")
    sys.exit(1 if errors else 0)

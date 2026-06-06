"""
TropeLang shared lexer (Python) — DEPRECATED, lexer-only.

The structural validator and the tag-origin / corpus-reuse reports have moved to the Rust reference
implementation (the LSP backend):
  - validator   →  `tropelang validate <file.trl>`   (src/validate.rs)
  - tag origins →  `tropelang report <file.trl>`   (src/report.rs)
  - DRY assist  →  `tropelang report <file.trl> --reuse`

This file now retains ONLY the `lex` tokenizer, because `dialog_context.py` still imports it. When
`dialog_context.py` is ported to Rust, delete this file too. Do not re-add validation logic here —
Rust is the reference (see ICEBOX.md, "Port the remaining core Python tooling to Rust").
"""

ALL_SIGILS = set("+-~?!#@&=%")
errors = []  # lex appends lexer-level errors here


def lex(src, label=""):
    """Permissive tokenizer matching the Rust validator's lexer (src/validate.rs)."""
    tokens = []
    i, line = 0, 1
    while i < len(src):
        c = src[i]
        if c == '\n':
            line += 1
            i += 1
            continue
        if c in ' \t\r':
            i += 1
            continue

        # line comment
        if c == '/' and i + 1 < len(src) and src[i + 1] == '/':
            while i < len(src) and src[i] != '\n':
                i += 1
            continue

        # triple-quoted block string (inline YAML for dialog)
        if c == '"' and src[i:i + 3] == '"""':
            end = src.find('"""', i + 3)
            if end == -1:
                errors.append(f"[{label}] line {line}: unterminated block string")
                return tokens
            block = src[i + 3:end]
            tokens.append(('BLOCK', block, line))
            line += block.count('\n')
            i = end + 3
            continue

        # string literal
        if c == '"':
            j = i + 1
            while j < len(src) and src[j] != '"':
                j += 1
            if j >= len(src):
                errors.append(f"[{label}] line {line}: unterminated string")
                return tokens
            tokens.append(('STR', src[i + 1:j], line))
            i = j + 1
            continue

        # number
        if c.isdigit():
            j = i + 1
            dot = False
            while j < len(src) and (src[j].isdigit() or (src[j] == '.' and not dot)):
                if src[j] == '.':
                    dot = True
                j += 1
            tokens.append(('NUM', src[i:j], line))
            i = j
            continue

        # variable
        if c == '$':
            j = i + 1
            while j < len(src) and (src[j].isalnum() or src[j] == '_'):
                j += 1
            if j == i + 1:
                errors.append(f"[{label}] line {line}: bare $")
                i += 1
                continue
            tokens.append(('VAR', src[i:j], line))
            i = j
            continue

        # identifier / keyword
        if c.isalpha() or c == '_':
            j = i + 1
            while j < len(src) and (src[j].isalnum() or src[j] == '_'):
                j += 1
            tokens.append(('ID', src[i:j], line))
            i = j
            continue

        # ellipsis
        if c == '.' and src[i:i + 3] == '...':
            tokens.append(('ELLIPSIS', '...', line))
            i += 3
            continue

        # multi-char operators (longest match first)
        matched = False
        for op in ["!--", "->", "!>", "!@", "!=", ">=", "<=", "==", "--", "><", "<<", ">>"]:
            if src[i:i + len(op)] == op:
                tokens.append(('OP', op, line))
                i += len(op)
                matched = True
                break
        if matched:
            continue

        # single-char tokens
        if c in "+-~?!><@=:,{}[]()":
            tokens.append(('OP', c, line))
            i += 1
            continue
        if c in "*|.#%&":
            tokens.append(('OP', c, line))
            i += 1
            continue

        errors.append(f"[{label}] line {line}: unexpected char {c!r}")
        i += 1

    return tokens


if __name__ == "__main__":
    print(__doc__.strip())
    raise SystemExit("validate_tropelang.py is lexer-only now; use `tropelang validate <file>`")

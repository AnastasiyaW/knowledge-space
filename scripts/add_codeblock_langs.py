"""
Auto-tag untagged ``` code blocks with a language.

Heuristic classifier on the first non-empty line of each block:
- Dockerfile/apt/docker/kubectl/curl/pip/docker run/$ ... -> bash
- def / import / from / print(/class         -> python
- {"..": / [{ / plain JSON                   -> json
- key: value YAML-ish                        -> yaml
- <tag>/HTML                                 -> html
- SELECT/INSERT/UPDATE/WITH                  -> sql
- else                                       -> text

Only touches fences that have NO tag. Never overrides existing tags.
"""
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

FENCE_OPEN = re.compile(r"^( {0,3})```(\s*)$")  # ``` with no language on fence line
FENCE_CLOSE = re.compile(r"^( {0,3})```(\s*)$")


def classify(first_line: str) -> str:
    s = first_line.strip()
    if not s:
        return "text"

    # Shell / command-line
    if re.match(r"^\$\s+\S", s):
        return "bash"
    if re.match(r"^(apt-get|apt|yum|brew|docker|kubectl|helm|curl|wget|pip|npm|yarn|pnpm|ssh|scp|rsync|git|sudo|systemctl|service|echo|cat|cd|ls|mkdir|rm|mv|cp|chmod|chown|export|source|bash|sh) ", s):
        return "bash"
    if s.startswith("#!/"):
        return "bash"
    if re.match(r"^(FROM|RUN|COPY|ADD|CMD|ENTRYPOINT|WORKDIR|ENV|ARG|EXPOSE|VOLUME|USER|LABEL|HEALTHCHECK)\s", s):
        return "dockerfile"

    # Python
    if re.match(r"^(def |class |import |from |async def |@[a-zA-Z_]|print\()", s):
        return "python"
    if re.match(r"^\s*(self\.|await |raise |yield |return |if __name__)", s):
        return "python"

    # JSON
    if s.startswith("{") and '"' in s and ':' in s:
        return "json"
    if s.startswith('[{') and '"' in s:
        return "json"

    # YAML
    if re.match(r"^[a-zA-Z_][\w\-]*:\s*(\S|$)", s) and not s.endswith('{'):
        # Avoid matching C++/JS object lines
        if ';' not in s and '(' not in s:
            return "yaml"

    # SQL
    if re.match(r"^(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|ALTER|DROP|BEGIN|COMMIT)\b", s, re.IGNORECASE):
        return "sql"

    # HTML / XML
    if s.startswith("<") and ">" in s and not s.startswith("<-"):
        return "html"

    # JavaScript-ish
    if re.match(r"^(const |let |var |function |export |require\()", s):
        return "javascript"

    return "text"


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=False)
    out = []
    i = 0
    changed = 0
    in_block = False
    while i < len(lines):
        line = lines[i]
        if not in_block:
            m = FENCE_OPEN.match(line)
            if m:
                # Look ahead for first non-empty body line
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                body_line = lines[j] if j < len(lines) else ""
                lang = classify(body_line)
                out.append(f"{m.group(1)}```{lang}")
                in_block = True
                changed += 1
                i += 1
                continue
            # Fence with a language tag already? keep as is and track state
            if re.match(r"^ {0,3}```\S", line):
                in_block = True
                out.append(line)
                i += 1
                continue
            out.append(line)
            i += 1
        else:
            out.append(line)
            if FENCE_CLOSE.match(line):
                in_block = False
            i += 1

    if changed:
        path.write_text("\n".join(out) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    return changed


def main(roots: list[str]):
    total_files = 0
    total_blocks = 0
    for root in roots:
        rp = Path(root)
        if not rp.is_absolute():
            rp = DOCS / rp
        if rp.is_file():
            files = [rp]
        else:
            files = list(rp.rglob("*.md"))
        for f in files:
            # Skip blog, contributing index, auto-generated
            parts = f.relative_to(DOCS).parts
            if parts and parts[0] in {"blog", "contributing", "javascripts", "stylesheets", "assets"}:
                continue
            if f.name == "index.md":
                continue
            c = process_file(f)
            if c:
                total_files += 1
                total_blocks += c
                print(f"  + {f.relative_to(DOCS)}: {c} blocks tagged")
    print(f"\nTotal: {total_blocks} blocks tagged across {total_files} files.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main([str(DOCS)])

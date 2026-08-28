"""Sync navigation indexes with the articles that actually exist.

Two outputs, both idempotent:

1. docs/{domain}/index.md  - the per-domain MOC. Articles present on disk but linked
   from nowhere in the MOC are appended under "## Additional References".
2. docs/knowledge-base/index.md - the browse page. Per-domain counts are recomputed,
   plain-text entries are converted to wiki-links when they resolve to a real article,
   and missing articles are appended to their domain block.

Run from the repository root:  python scripts/sync_indexes.py [--check]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path("docs")
SKIP_DIRS = {"assets", "javascripts", "stylesheets", "blog", "contributing", "knowledge-base"}
EXTRA_HEADING = "## Additional References"
MAX_DESC = 100


def domains() -> list[str]:
    return sorted(d.name for d in DOCS.iterdir() if d.is_dir() and d.name not in SKIP_DIRS)


def articles(domain: str) -> list[Path]:
    return sorted(
        (p for p in (DOCS / domain).rglob("*.md") if p.name != "index.md"),
        key=lambda p: p.stem.lower(),
    )


def short_description(path: Path) -> str:
    """One-line summary: front-matter description, else the first body sentence."""
    text = path.read_text(encoding="utf-8")
    desc = ""
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if fm:
        m = re.search(r'^description:\s*"?(.+?)"?\s*$', fm.group(1), re.M)
        if m:
            desc = m.group(1)
        text = text[fm.end():]
    if not desc:
        body = re.sub(r"^#\s+.*$", "", text, count=1, flags=re.M)
        for para in body.split("\n\n"):
            para = para.strip()
            if para and not para.startswith(("#", "```", "|", "-", "*", "<")):
                desc = para
                break
    desc = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", desc)
    desc = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", desc)
    desc = re.sub(r"[`*_]", "", desc).replace("\n", " ")
    desc = re.sub(r"\s+", " ", desc).strip()
    desc = desc.split(". ")[0].split("; ")[0]
    if len(desc) > MAX_DESC:
        cut = desc[:MAX_DESC].rsplit(" ", 1)[0]
        desc = cut.rstrip(",;:-") + "..."
    return desc.rstrip(".").strip()


def normalize(text: str) -> str:
    """Fold a display name to the slug shape used by file names."""
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9+]+", "-", text.lower())).strip("-")


# --------------------------------------------------------------------------- MOC


def sync_moc(domain: str) -> int:
    idx = DOCS / domain / "index.md"
    if not idx.exists():
        return 0
    text = idx.read_text(encoding="utf-8")
    linked = {m.split("/")[-1].strip() for m in re.findall(r"\[\[([^\]|]+)", text)}
    missing = [p for p in articles(domain) if p.stem not in linked]
    if not missing:
        return 0

    lines = [f"- [[{p.stem}]] - {short_description(p)}" for p in missing]
    block = "\n".join(lines)

    if EXTRA_HEADING in text:
        text = text.rstrip("\n") + "\n" + block + "\n"
    else:
        text = text.rstrip("\n") + f"\n\n{EXTRA_HEADING}\n\n" + block + "\n"
    idx.write_text(text, encoding="utf-8")
    return len(missing)


# ------------------------------------------------------------------- browse page

BLOCK_RE = re.compile(r'^\?\?\? note "(.*?)"\s*$')

# Display name + planet gradient for domains that have no block on the browse page yet.
# Names match hooks/stats.py DOMAIN_META so the page and the graph agree.
NEW_BLOCK_STYLE = {
    "audio-voice": ("Voice & Audio", "#e0a878,#805828", "rgba(224,168,120,0.5)"),
    "go": ("Go", "#5ec0d8,#1a6880", "rgba(94,192,216,0.5)"),
    "llm-memory": ("LLM Memory", "#b898e0,#584878", "rgba(184,152,224,0.5)"),
    "writing": ("Natural Language & Writing", "#d8b0c8,#785068", "rgba(216,176,200,0.5)"),
}


def sync_browse_page() -> tuple[int, int]:
    path = DOCS / "knowledge-base" / "index.md"
    lines = path.read_text(encoding="utf-8").split("\n")

    slug_by_domain = {d: {p.stem: p for p in articles(d)} for d in domains()}
    domain_of_anchor: dict[int, str] = {}
    current_domain: str | None = None
    for i, line in enumerate(lines):
        m = re.match(r'^<div id="([a-z0-9-]+)"></div>\s*$', line)
        if m and m.group(1) in slug_by_domain:
            domain_of_anchor[i] = m.group(1)

    out: list[str] = []
    added = relinked = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if i in domain_of_anchor:
            current_domain = domain_of_anchor[i]
            i += 1
            continue
        if current_domain and BLOCK_RE.match(line):
            domain = current_domain
            by_slug = slug_by_domain[domain]
            norm_map = {normalize(s): s for s in by_slug}

            # collect the indented body of this admonition
            body_start = i + 1
            j = body_start
            while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith("    ")):
                j += 1
            body = lines[body_start:j]

            seen: set[str] = set()
            new_body: list[str] = []
            for b in body:
                for target in re.findall(r"\[\[([^\]|]+)", b):
                    slug = target.split("/")[-1].strip()
                    if slug in by_slug:
                        seen.add(slug)
                # plain-text entry: "    - Display Name - description"
                m = re.match(r"^(\s*)- (.+)$", b)
                if m and "[[" not in b:
                    indent, rest = m.group(1), m.group(2)
                    parts = rest.split(" - ")
                    # the name may itself contain hyphens, so try the longest prefix first
                    for k in range(len(parts) - 1, 0, -1):
                        name = " - ".join(parts[:k]).strip()
                        slug = norm_map.get(normalize(name))
                        if slug:
                            desc = " - ".join(parts[k:]).strip()
                            b = f"{indent}- [[{slug}]] - {desc}"
                            seen.add(slug)
                            relinked += 1
                            break
                new_body.append(b)

            missing = [s for s in by_slug if s not in seen]
            missing.sort(key=str.lower)
            while new_body and new_body[-1].strip() == "":
                new_body.pop()
            if missing:
                new_body.append("")
                new_body.append("    **More**")
                new_body.append("")
                for slug in missing:
                    new_body.append(f"    - [[{slug}]] - {short_description(by_slug[slug])}")
                added += len(missing)
            new_body.append("")

            # rewrite the heading count
            head = BLOCK_RE.match(line).group(1)
            total = len(by_slug)
            new_head = re.sub(r"\d+ articles", f"{total} articles", head)
            out[-1] = f'??? note "{new_head}"'

            out.extend(new_body)
            i = j
            continue
        i += 1

    # Domains that never got a block on this page (added after it was last curated).
    present = set(domain_of_anchor.values())
    for domain in domains():
        if domain in present:
            continue
        by_slug = slug_by_domain[domain]
        if not by_slug:
            continue
        name, grad, glow = NEW_BLOCK_STYLE[domain]
        out.append("")
        out.append("---")
        out.append("")
        out.append(f'<div id="{domain}"></div>')
        out.append("")
        out.append(
            '??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,'
            "rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,"
            f'{grad});box-shadow:0 0 8px {glow},inset 0 -2px 4px rgba(0,0,0,0.3)"></span>'
            f'{name} · {len(by_slug)} articles"'
        )
        out.append("")
        for slug in sorted(by_slug, key=str.lower):
            out.append(f"    - [[{slug}]] - {short_description(by_slug[slug])}")
            added += 1
        out.append("")

    text = "\n".join(out)
    total_articles = sum(len(v) for v in slug_by_domain.values())
    text = re.sub(r"\b\d{3}\+ (curated )?articles", lambda m: f"{total_articles}+ {m.group(1) or ''}articles", text)
    text = re.sub(r"Browse \d{3}\+ technical articles", f"Browse {total_articles}+ technical articles", text)
    path.write_text(text, encoding="utf-8")
    return added, relinked


def main() -> int:
    moc_added = {d: sync_moc(d) for d in domains()}
    total_moc = sum(moc_added.values())
    for d, n in sorted(moc_added.items(), key=lambda x: -x[1]):
        if n:
            print(f"  MOC {d}: +{n}")
    added, relinked = sync_browse_page()
    print(f"MOC entries added: {total_moc}")
    print(f"Browse page: +{added} entries, {relinked} plain-text entries converted to links")
    return 0


if __name__ == "__main__":
    sys.exit(main())

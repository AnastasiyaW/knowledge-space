"""Propagate the real article/domain/cross-reference counts into every hardcoded place.

Single source of truth for the counts is hooks/stats.py (the same counter the site build
uses for stats.js). Cross-references are counted as wiki-links inside articles only -
index.md, the browse page and the blog are navigation, not cross-references.

Run from the repository root:  python scripts/sync_stats.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, "hooks")
import stats  # noqa: E402

DOCS = Path("docs")
SKIP_DIRS = {"assets", "javascripts", "stylesheets", "blog", "contributing", "knowledge-base"}


def count_cross_references() -> int:
    total = 0
    for d in sorted(x.name for x in DOCS.iterdir() if x.is_dir() and x.name not in SKIP_DIRS):
        for p in (DOCS / d).rglob("*.md"):
            if p.name == "index.md":
                continue
            total += len(re.findall(r"\[\[[^\]]+\]\]", p.read_text(encoding="utf-8")))
    return total


def sub(path: str, pairs: list[tuple[str, str]]) -> None:
    q = Path(path)
    text = before = q.read_text(encoding="utf-8")
    for pattern, repl in pairs:
        text = re.sub(pattern, repl, text)
    q.write_text(text, encoding="utf-8")
    print(f"  {path}: {'updated' if text != before else 'already current'}")


NEW_DOMAIN_COVERAGE = {
    "projects": "One page per tool, model or product the news conveyor follows: dated development line, current use, obsolete guidance, sources",
    "organizations": "One page per company or lab: leadership and structure changes, product lines, what each change made obsolete",
}


def update_readme(total: int, domains: int, xref: int, counts: dict[str, int]) -> None:
    p = Path("README.md")
    text = p.read_text(encoding="utf-8")
    text = re.sub(
        r"\*\*\d+\+ articles \| \d+ domains \| \d+\+ cross-references\*\*",
        f"**{total}+ articles | {domains} domains | {xref}+ cross-references**",
        text,
    )
    text = re.sub(r"\bacross \d+ domains\b", f"across {domains} domains", text)
    row_re = re.compile(r"^\| `([a-z0-9-]+)/` \| +(\d+) +\| (.*?) \|$", re.M)
    rows = row_re.findall(text)
    if not rows:
        raise SystemExit("README domain table not found")
    coverage = {d: c for d, _, c in rows}
    # A domain's first article arrives before its README row exists; add the row
    # instead of refusing, with the coverage sentence declared here.
    for d in counts:
        if d not in coverage:
            coverage[d] = NEW_DOMAIN_COVERAGE.get(d, stats.DOMAIN_META.get(d, {}).get("name", d))
            print(f"  README.md: row added for {d}/")

    new_rows = "\n".join(
        f"| `{d}/` | {counts[d]} | {coverage[d]} |"
        for d in sorted(counts, key=lambda x: (-counts[x], x))
    )
    first = text.index(f"| `{rows[0][0]}/` |")
    last = text.rindex(f"| `{rows[-1][0]}/` |")
    end = text.index("\n", last)
    p.write_text(text[:first] + new_rows + text[end:], encoding="utf-8")
    print("  README.md: updated")


def main() -> int:
    s = stats.count_articles(DOCS)
    total, domains = s["total_articles"], s["total_domains"]
    counts = {k: v["articles"] for k, v in s["domains"].items()}
    xref = count_cross_references()
    print(f"articles={total} domains={domains} cross_references={xref}")

    update_readme(total, domains, xref, counts)
    sub("docs/index.md", [
        (r'(id="ks-graph-nodes">)\d+(</span>)', rf"\g<1>{total}\g<2>"),
        (r'(id="ks-total-domains">)\d+(</span>)', rf"\g<1>{domains}\g<2>"),
        (r"\b\d{3,}\+ articles across \d+ domains", f"{total}+ articles across {domains} domains"),
        (r"\bacross \d+ domains\b", f"across {domains} domains"),
    ])
    sub("mkdocs.yml", [
        (r"\b\d{3,}\+ curated articles", f"{total}+ curated articles"),
        (r"\(\d+ articles across \d+ domains\)", f"({total} articles across {domains} domains)"),
        (r"\bacross \d+ domains\b", f"across {domains} domains"),
    ])
    sub("AGENTS.md", [(r"\(\d{3,}\+ articles, \d+ domains\)", f"({total}+ articles, {domains} domains)")])
    sub("docs/blog/posts/welcome.md", [
        (r"\*\*\d{3,}\+ dense reference articles\*\*", f"**{total}+ dense reference articles**"),
        (r"across \d+ technical domains", f"across {domains} technical domains"),
    ])
    sub(".claude/rules/article-rules.md",
        [(r"\b\d{3,}\+ articles across \d+ domains", f"{total}+ articles across {domains} domains")])
    print()
    print("GitHub description (run manually):")
    print(f'  gh repo edit --description "... {total}+ ... {domains} domains ..."')
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
Freshness check: validates stats consistency, wiki-links, and llms.txt sync.
Can be run standalone or called from CI.

Usage:
    python hooks/freshness_check.py          # full check
    python hooks/freshness_check.py --ci     # CI mode (exit code 1 on errors)
    python hooks/freshness_check.py --fix    # auto-fix stale counts
"""

import os
import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"
ROOT = Path(__file__).parent.parent

# Files with hardcoded article/domain counts
STATS_FILES = {
    "README.md": [
        (r"(\d{3,})\+?\s*articles", "articles"),
        (r"(\d+)\s*domains", "domains"),
    ],
    "AGENTS.md": [
        (r"(\d{3,})\+?\s*articles", "articles"),
        (r"(\d+)\s*domains", "domains"),
    ],
    "docs/index.md": [
        (r"(\d{3,})\+?\s*articles", "articles"),
        (r"across\s+(\d+)\s+domains", "domains"),
    ],
    "docs/blog/posts/welcome.md": [
        (r"(\d{3,})\+?\s*dense reference articles", "articles"),
    ],
    "mkdocs.yml": [
        (r"(\d{3,})\+?\s*curated articles", "articles"),
    ],
    ".claude/rules/article-rules.md": [
        (r"(\d{3,})\+?\s*articles across\s+(\d+)\s+domains", "both"),
    ],
}

# Exclude these from article count
EXCLUDE_FILES = {"index.md", "for-llm-agents.md", "privacy.md"}
EXCLUDE_DIRS = {"blog", "contributing", "javascripts", "stylesheets", "assets", "knowledge-base"}


def count_actual_articles() -> tuple[int, int]:
    """Return (article_count, domain_count)."""
    domains = set()
    articles = 0
    for d in DOCS_DIR.iterdir():
        if not d.is_dir() or d.name in EXCLUDE_DIRS:
            continue
        domain_articles = 0
        for f in d.rglob("*.md"):
            if f.name in EXCLUDE_FILES:
                continue
            domain_articles += 1
        if domain_articles > 0:
            domains.add(d.name)
            articles += domain_articles
    return articles, len(domains)


def check_wiki_links() -> list[str]:
    """Find broken [[wiki-links]] pointing to non-existent articles."""
    errors = []
    # Build slug map
    slug_map = {}
    for md_file in DOCS_DIR.rglob("*.md"):
        slug_map[md_file.stem] = str(md_file.relative_to(DOCS_DIR))

    wiki_re = re.compile(r"\[\[([^\]]+)\]\]")
    code_fence_re = re.compile(r"^```")

    for md_file in DOCS_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8", errors="replace")
        in_code_block = False
        for i, line in enumerate(content.split("\n"), 1):
            if code_fence_re.match(line.strip()):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            # Skip inline code
            clean_line = re.sub(r"`[^`]+`", "", line)
            for match in wiki_re.finditer(clean_line):
                slug = match.group(1).strip()
                # Handle display text: [[slug|Display Text]]
                if "|" in slug:
                    parts = slug.split("|")
                    # Try both orders: [[slug|text]] and [[text|slug]]
                    slug = parts[0].strip()
                    alt_slug = parts[1].strip() if len(parts) > 1 else ""
                # Handle anchor: [[slug#anchor]]
                if "#" in slug:
                    slug = slug.split("#")[0].strip()
                # Handle domain/slug format
                if "/" in slug:
                    parts = slug.split("/")
                    slug = parts[-1]
                # Skip code-like patterns
                if any(c in slug for c in "=<>&(){}[],'\""):
                    continue
                if slug not in slug_map:
                    # Try alt_slug for [[text|slug]] format
                    alt = locals().get("alt_slug", "")
                    if alt and alt in slug_map:
                        continue
                    rel = md_file.relative_to(DOCS_DIR)
                    errors.append(f"  BROKEN: {rel}:{i} -> [[{match.group(1)}]]")
    return errors


def check_llms_txt() -> list[str]:
    """Check if llms.txt article count matches actual count."""
    errors = []
    llms_path = DOCS_DIR / "llms.txt"
    if not llms_path.exists():
        errors.append("  MISSING: docs/llms.txt not found")
        return errors

    content = llms_path.read_text(encoding="utf-8")
    url_count = len(re.findall(r"https://happyin\.space/", content))
    actual, _ = count_actual_articles()

    diff = abs(url_count - actual)
    if diff > 5:
        errors.append(f"  STALE: llms.txt has {url_count} URLs, actual articles: {actual} (diff: {diff})")
    return errors


def check_stats_consistency() -> list[str]:
    """Check hardcoded counts in key files against actual counts."""
    errors = []
    actual_articles, actual_domains = count_actual_articles()

    for filepath, patterns in STATS_FILES.items():
        fpath = ROOT / filepath
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8", errors="replace")

        for pattern, kind in patterns:
            for match in re.finditer(pattern, content):
                if kind == "articles":
                    found = int(match.group(1))
                    if abs(found - actual_articles) > 10:
                        errors.append(
                            f"  STALE: {filepath} says {found} articles, actual: {actual_articles}"
                        )
                elif kind == "domains":
                    found = int(match.group(1))
                    if found != actual_domains:
                        errors.append(
                            f"  STALE: {filepath} says {found} domains, actual: {actual_domains}"
                        )
                elif kind == "both":
                    a = int(match.group(1))
                    d = int(match.group(2))
                    if abs(a - actual_articles) > 10:
                        errors.append(
                            f"  STALE: {filepath} says {a} articles, actual: {actual_articles}"
                        )
                    if d != actual_domains:
                        errors.append(
                            f"  STALE: {filepath} says {d} domains, actual: {actual_domains}"
                        )
    return errors


def main():
    ci_mode = "--ci" in sys.argv
    actual_articles, actual_domains = count_actual_articles()

    print(f"=== Freshness Check ===")
    print(f"Actual: {actual_articles} articles, {actual_domains} domains\n")

    all_errors = []

    # 1. Stats consistency
    print("[1/3] Checking stats consistency...")
    stats_errors = check_stats_consistency()
    all_errors.extend(stats_errors)
    if stats_errors:
        for e in stats_errors:
            print(e)
    else:
        print("  OK: all hardcoded counts match")

    # 2. Wiki-links
    print("\n[2/3] Checking wiki-links...")
    wiki_errors = check_wiki_links()
    all_errors.extend(wiki_errors)
    if wiki_errors:
        print(f"  Found {len(wiki_errors)} broken wiki-links:")
        for e in wiki_errors[:20]:  # Show first 20
            print(e)
        if len(wiki_errors) > 20:
            print(f"  ... and {len(wiki_errors) - 20} more")
    else:
        print("  OK: all wiki-links resolve")

    # 3. llms.txt sync
    print("\n[3/3] Checking llms.txt sync...")
    llms_errors = check_llms_txt()
    all_errors.extend(llms_errors)
    if llms_errors:
        for e in llms_errors:
            print(e)
    else:
        print("  OK: llms.txt in sync")

    # Summary
    print(f"\n=== Result: {len(all_errors)} issues found ===")

    if ci_mode and all_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Standalone link checker for Happyin Knowledge Space.
Run locally or in CI without needing mkdocs build.

Usage:
    python lint.link-check.py
    python lint.link-check.py --strict  # exit 1 on any broken link

Checks:
  1. Every domain folder has index.md
  2. All [[wiki-links]] resolve to existing articles
  3. All internal markdown links point to existing files
"""

import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "docs"

VALID_DOMAINS = {
    "algorithms", "architecture", "bi-analytics", "cpp", "data-engineering",
    "data-science", "devops", "image-generation", "ios-mobile",
    "java-spring", "kafka", "linux-cli", "llm-agents",
    "nodejs", "php", "python", "rust", "security", "seo-marketing",
    "sql-databases", "testing-qa", "web-frontend", "writing", "llm-memory",
    "audio-voice", "go",
}

SKIP_DIRS = {"assets", "javascripts", "stylesheets", "blog", "contributing", "knowledge-base"}


def collect_slugs() -> dict[str, str]:
    slugs = {}
    for md in DOCS_DIR.rglob("*.md"):
        rel = md.relative_to(DOCS_DIR).as_posix()
        slug = md.stem
        if slug not in slugs or md.name != "index.md":
            slugs[slug] = rel
    return slugs


def extract_wikilinks(content: str) -> list[tuple[int, str]]:
    links = []
    in_code = False
    for i, line in enumerate(content.split("\n"), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        cleaned = re.sub(r'`[^`]+`', '', line)
        for m in re.finditer(r'\[\[([^\]]+)\]\]', cleaned):
            slug = m.group(1).strip()
            if any(c in slug for c in ("'", '"', ",", "=", "&", "|", "(", ")", "+")):
                continue
            if "/" in slug:
                slug = slug.rsplit("/", 1)[-1]
            if ":" in slug:
                slug = slug.rsplit(":", 1)[-1]
            links.append((i, slug))
    return links


def extract_md_links(content: str) -> list[tuple[int, str]]:
    links = []
    in_code = False
    for i, line in enumerate(content.split("\n"), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        cleaned = re.sub(r'`[^`]+`', '', line)
        for m in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', cleaned):
            target = m.group(2).strip()
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = target.split("#")[0]
            if target and target.endswith(".md"):
                links.append((i, target))
    return links


def main():
    strict = "--strict" in sys.argv
    slug_map = collect_slugs()
    issues = []

    # 1. Check domain index.md
    for domain in sorted(VALID_DOMAINS):
        d = DOCS_DIR / domain
        if d.is_dir():
            if not (d / "index.md").exists():
                issues.append(f"MISSING INDEX: {domain}/index.md")
        else:
            issues.append(f"MISSING DOMAIN: {domain}/ folder not found")

    # 2. Check links in all articles
    broken_wiki = 0
    broken_md = 0
    checked = 0

    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        rel = md_file.relative_to(DOCS_DIR)
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue

        checked += 1
        content = md_file.read_text(encoding="utf-8", errors="replace")
        rel_str = rel.as_posix()

        for line_num, slug in extract_wikilinks(content):
            if slug not in slug_map:
                issues.append(f"BROKEN WIKI: {rel_str}:{line_num} [[{slug}]]")
                broken_wiki += 1

        for line_num, target in extract_md_links(content):
            target_path = (md_file.parent / target).resolve()
            if not target_path.exists():
                alt = (DOCS_DIR / target).resolve()
                if not alt.exists():
                    issues.append(f"BROKEN LINK: {rel_str}:{line_num} -> {target}")
                    broken_md += 1

    # Report
    print(f"\nLink Check Report")
    print(f"{'=' * 50}")
    print(f"Files checked: {checked}")
    print(f"Slugs indexed: {len(slug_map)}")
    print()

    if issues:
        for issue in issues:
            print(f"  {issue}")
        print()
        print(f"Total: {len(issues)} issues ({broken_wiki} wiki, {broken_md} md-links)")
        if strict:
            sys.exit(1)
    else:
        print("All links OK!")

    return len(issues)


if __name__ == "__main__":
    main()

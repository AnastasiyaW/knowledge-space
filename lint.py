"""
Knowledge Vault Health Check / Lint
Inspired by Karpathy's LLM Wiki lint pattern.

Checks:
1. Orphan pages (no incoming links - counts both [md](paths) AND [[wiki-links]])
2. Broken internal links
3. Missing frontmatter (title, description)
4. Stale articles (no update in 60+ days)
5. Empty or too-short articles (<100 words)
"""

import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "docs"
MIN_WORDS = 100
STALE_DAYS = 60


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()
    return fm


def extract_links(content):
    """Extract internal markdown links: [text](path.md)."""
    return re.findall(r'\[[^\]]*\]\(([^)]+\.md(?:#[^)]*)?)\)', content)


def extract_wikilinks(content):
    """Extract [[wiki-link]] slugs from outside code blocks/inline code.

    Wiki-links are converted to markdown links by hooks/wikilinks.py at build time,
    so they ARE real incoming references — lint must count them or we get false orphans.
    """
    slugs = []
    in_code_block = False
    for line in content.split("\n"):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # Strip inline code before scanning
        cleaned = re.sub(r'`[^`]+`', '', line)
        for m in re.finditer(r'\[\[([^\]]+)\]\]', cleaned):
            slug = m.group(1).strip()
            # Skip code-like patterns (mirrors hooks/wikilinks.py filter)
            if any(c in slug for c in ("'", '"', ",", "=", "&", "|", "(", ")", ":", "+")):
                continue
            slugs.append(slug)
    return slugs


def build_slug_map(all_files):
    """Map slug -> relative path (mirrors hooks/wikilinks.py)."""
    slug_map = {}
    for rel_str in all_files:
        slug = Path(rel_str).stem
        # Prefer non-index articles when slug collides
        if slug not in slug_map or not rel_str.endswith("index.md"):
            slug_map[slug] = rel_str
    return slug_map


def run_lint():
    all_files = {}
    incoming_links = {}
    issues = {"orphans": [], "broken_links": [], "missing_meta": [],
              "stale": [], "too_short": [], "empty": []}
    docs_resolved = DOCS_DIR.resolve()

    # Collect all .md files
    for md_file in DOCS_DIR.rglob("*.md"):
        rel = md_file.relative_to(DOCS_DIR)
        rel_str = str(rel).replace("\\", "/")
        all_files[rel_str] = md_file
        incoming_links[rel_str] = 0

    # Build slug map for [[wiki-link]] resolution
    slug_map = build_slug_map(all_files)

    # Analyze each file
    for rel_str, md_file in all_files.items():
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        fm = extract_frontmatter(content)

        # Check frontmatter
        if not fm.get("title") and not fm.get("description"):
            issues["missing_meta"].append(rel_str)

        # Check word count
        text_only = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)
        text_only = re.sub(r'[#*`\[\]\(\)\-|>]', ' ', text_only)
        words = len(text_only.split())
        if words == 0:
            issues["empty"].append(rel_str)
        elif words < MIN_WORDS:
            issues["too_short"].append((rel_str, words))

        # Check staleness
        mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
        if datetime.now() - mtime > timedelta(days=STALE_DAYS):
            issues["stale"].append((rel_str, mtime.strftime("%Y-%m-%d")))

        # Track markdown links
        links = extract_links(content)
        for link in links:
            link_path = link.split("#")[0]
            # Skip external/absolute
            if link_path.startswith(("http://", "https://", "/")):
                continue
            try:
                resolved = (md_file.parent / link_path).resolve()
                resolved_rel = str(resolved.relative_to(docs_resolved)).replace("\\", "/")
            except (ValueError, OSError):
                issues["broken_links"].append((rel_str, link_path))
                continue

            if resolved_rel in incoming_links:
                if resolved_rel != rel_str:
                    incoming_links[resolved_rel] += 1
            else:
                issues["broken_links"].append((rel_str, link_path))

        # Track [[wiki-links]] - these become real markdown links via hooks/wikilinks.py
        for slug in extract_wikilinks(content):
            # Support [[domain/slug]] syntax - extract slug part
            if "/" in slug:
                slug = slug.rsplit("/", 1)[-1]
            if slug in slug_map:
                target = slug_map[slug]
                if target != rel_str:  # don't count self-references
                    incoming_links[target] = incoming_links.get(target, 0) + 1
            else:
                issues["broken_links"].append((rel_str, f"[[{slug}]]"))

    # Find orphans (excluding index files and special pages)
    skip_orphan_check = {"index.md", "for-llm-agents.md", "privacy.md"}
    for rel_str, count in incoming_links.items():
        if count == 0 and not rel_str.endswith("index.md") and rel_str not in skip_orphan_check:
            # Skip blog posts - they're standalone content
            if rel_str.startswith("blog/") or rel_str.startswith("knowledge-base/"):
                continue
            issues["orphans"].append(rel_str)

    # Report
    total = len(all_files)
    print(f"# Knowledge Vault Health Report")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Total articles: {total}\n")

    # Score
    problem_count = (len(issues["broken_links"]) + len(issues["empty"])
                     + len(issues["missing_meta"]))
    health = max(0, 100 - (problem_count * 2) - (len(issues["orphans"]) * 0.5))
    print(f"Health score: {health:.0f}/100\n")

    for category, items in issues.items():
        if not items:
            print(f"## {category}: OK (0 issues)")
            continue
        print(f"## {category}: {len(items)} issues")
        for item in items[:20]:
            if isinstance(item, tuple):
                print(f"  - {item[0]} ({item[1]})")
            else:
                print(f"  - {item}")
        if len(items) > 20:
            print(f"  ... and {len(items) - 20} more")
        print()


if __name__ == "__main__":
    run_lint()

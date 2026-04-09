"""
Knowledge Vault Health Check / Lint
Inspired by Karpathy's LLM Wiki lint pattern.

Checks:
1. Orphan pages (no incoming links)
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
    """Extract internal markdown links."""
    # [text](path.md) or [text](../path.md)
    return re.findall(r'\[[^\]]*\]\(([^)]+\.md(?:#[^)]*)?)\)', content)


def run_lint():
    all_files = {}
    incoming_links = {}
    issues = {"orphans": [], "broken_links": [], "missing_meta": [],
              "stale": [], "too_short": [], "empty": []}

    # Collect all .md files
    for md_file in DOCS_DIR.rglob("*.md"):
        rel = md_file.relative_to(DOCS_DIR)
        rel_str = str(rel).replace("\\", "/")
        all_files[rel_str] = md_file
        incoming_links[rel_str] = 0

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

        # Track links
        links = extract_links(content)
        for link in links:
            link_path = link.split("#")[0]
            # Resolve relative path
            if link_path.startswith("../") or link_path.startswith("./"):
                resolved = (md_file.parent / link_path).resolve()
                try:
                    resolved_rel = str(resolved.relative_to(DOCS_DIR)).replace("\\", "/")
                except ValueError:
                    continue
            else:
                resolved_rel = str((md_file.parent / link_path).relative_to(DOCS_DIR)).replace("\\", "/")

            if resolved_rel in incoming_links:
                incoming_links[resolved_rel] += 1
            else:
                issues["broken_links"].append((rel_str, link_path))

    # Find orphans (excluding index files)
    for rel_str, count in incoming_links.items():
        if count == 0 and not rel_str.endswith("index.md") and rel_str != "index.md":
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
        for item in items[:20]:  # limit output
            if isinstance(item, tuple):
                print(f"  - {item[0]} ({item[1]})")
            else:
                print(f"  - {item}")
        if len(items) > 20:
            print(f"  ... and {len(items) - 20} more")
        print()


if __name__ == "__main__":
    run_lint()

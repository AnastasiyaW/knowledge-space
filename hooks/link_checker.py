"""
MkDocs hook: check all internal links and wiki-links for broken references.
Runs on every build. Reports broken wiki-links, missing index.md, and dead
cross-references. Also verifies that each domain in VALID_DOMAINS has index.md.

Exit behavior: prints warnings, does NOT fail the build (non-blocking).
"""

import re
from pathlib import Path

# Valid domain folders (must match validate.py)
VALID_DOMAINS = {
    "algorithms", "architecture", "bi-analytics", "cpp", "data-engineering",
    "data-science", "devops", "image-generation", "ios-mobile",
    "java-spring", "kafka", "linux-cli", "llm-agents", "misc",
    "nodejs", "php", "python", "rust", "security", "seo-marketing",
    "sql-databases", "testing-qa", "web-frontend", "writing", "llm-memory",
    "audio-voice", "go",
}

# Skip these directories (not article domains)
SKIP_DIRS = {"assets", "javascripts", "stylesheets", "blog", "contributing", "knowledge-base"}


def _collect_slugs(docs_dir: Path) -> dict[str, str]:
    """Build slug -> relative path mapping for all markdown files."""
    slugs = {}
    for md in docs_dir.rglob("*.md"):
        rel = md.relative_to(docs_dir).as_posix()
        slug = md.stem
        if slug not in slugs or md.name != "index.md":
            slugs[slug] = rel
    return slugs


def _extract_wikilinks(content: str) -> list[tuple[int, str]]:
    """Extract [[wiki-links]] from content, skipping code blocks and inline code."""
    links = []
    in_code_block = False

    for i, line in enumerate(content.split("\n"), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Remove inline code spans before matching
        cleaned = re.sub(r'`[^`]+`', '', line)
        for m in re.finditer(r'\[\[([^\]]+)\]\]', cleaned):
            slug = m.group(1).strip()
            # Skip code-like patterns
            if any(c in slug for c in ("'", '"', ",", "=", "&", "|", "(", ")", "+")):
                continue
            # Handle [[domain/slug]] and [[domain:slug]] syntax
            if "/" in slug:
                slug = slug.rsplit("/", 1)[-1]
            if ":" in slug:
                slug = slug.rsplit(":", 1)[-1]
            links.append((i, slug))

    return links


def _extract_md_links(content: str) -> list[tuple[int, str]]:
    """Extract standard markdown links to internal .md files."""
    links = []
    in_code_block = False

    for i, line in enumerate(content.split("\n"), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        cleaned = re.sub(r'`[^`]+`', '', line)
        for m in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', cleaned):
            target = m.group(2).strip()
            # Only check internal .md links (not http, not anchors)
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Strip anchors
            target = target.split("#")[0]
            if target and target.endswith(".md"):
                links.append((i, target))

    return links


def on_pre_build(config, **kwargs):
    """Run link check before MkDocs build."""
    docs_dir = Path(config["docs_dir"])
    slug_map = _collect_slugs(docs_dir)
    issues = []

    # 1. Check every domain has index.md
    for domain in sorted(VALID_DOMAINS):
        domain_dir = docs_dir / domain
        if domain_dir.is_dir():
            index = domain_dir / "index.md"
            if not index.exists():
                issues.append(f"  MISSING INDEX: {domain}/index.md - domain page will 404")
        else:
            issues.append(f"  MISSING DOMAIN: {domain}/ - folder does not exist")

    # 2. Check all wiki-links and md-links in articles
    broken_wiki = 0
    broken_md = 0
    checked_files = 0

    for md_file in sorted(docs_dir.rglob("*.md")):
        rel = md_file.relative_to(docs_dir)
        # Skip non-article dirs
        parts = rel.parts
        if parts and parts[0] in SKIP_DIRS:
            continue

        checked_files += 1
        content = md_file.read_text(encoding="utf-8", errors="replace")
        rel_str = rel.as_posix()

        # Check wiki-links
        for line_num, slug in _extract_wikilinks(content):
            if slug not in slug_map:
                issues.append(f"  BROKEN WIKI: {rel_str}:{line_num} - [[{slug}]] not found")
                broken_wiki += 1

        # Check markdown links to .md files
        for line_num, target in _extract_md_links(content):
            # Resolve relative to current file's directory
            current_dir = md_file.parent
            target_path = (current_dir / target).resolve()
            if not target_path.exists():
                # Also try relative to docs_dir
                alt_path = (docs_dir / target).resolve()
                if not alt_path.exists():
                    issues.append(f"  BROKEN LINK: {rel_str}:{line_num} - {target} not found")
                    broken_md += 1

    # Report
    if issues:
        print(f"[link-checker] {checked_files} files checked, {len(issues)} issues:")
        for issue in issues[:50]:
            print(issue)
        if len(issues) > 50:
            print(f"  ... and {len(issues) - 50} more")
        print(f"  Summary: {broken_wiki} broken wiki-links, {broken_md} broken md-links")
    else:
        print(f"[link-checker] {checked_files} files checked, all links OK")

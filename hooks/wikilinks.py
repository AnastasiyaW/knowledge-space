"""
MkDocs hook: convert [[wiki-links]] to proper markdown links.
Only converts links OUTSIDE code blocks and inline code.
Resolves [[slug]] to the actual .md file path within docs/.
"""

import re
from pathlib import Path

# Cache: slug -> relative path from docs root
_slug_map: dict[str, str] = {}
_built = False


def _build_slug_map(docs_dir: Path):
    """Build a mapping from article slug to its path relative to docs/."""
    global _slug_map, _built
    if _built:
        return

    for md_file in docs_dir.rglob("*.md"):
        rel = md_file.relative_to(docs_dir)
        slug = md_file.stem  # e.g., "broker-architecture"
        # Store the relative path without .md extension for MkDocs linking
        path_str = str(rel).replace("\\", "/")
        # Prefer domain articles over index files
        if slug not in _slug_map or md_file.name != "index.md":
            _slug_map[slug] = path_str

    _built = True


def _replace_wikilink(match: re.Match) -> str:
    """Replace a [[slug]] with [display name](path)."""
    slug = match.group(1).strip()

    # Skip if slug contains characters that suggest it's code, not a link
    # e.g., ['value'], [1, 2], [cond1 && cond2]
    if any(c in slug for c in ("'", '"', ",", "=", "&", "|", "(", ")", ":", "+")):
        return match.group(0)  # Return unchanged

    # Look up in slug map
    if slug in _slug_map:
        path = _slug_map[slug]
        # Display name: slug with hyphens replaced
        display = slug.replace("-", " ").replace("_", " ")
        return f"[{display}]({path})"

    # Not found - leave as-is (will show as text)
    return match.group(0)


def _process_markdown(content: str) -> str:
    """Convert [[wiki-links]] outside code blocks."""
    lines = content.split("\n")
    result = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        # Track code fences
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # Outside code block: replace [[wiki-links]]
        # But skip inline code: don't replace inside `...`
        # Strategy: split by inline code spans, only replace in non-code parts
        parts = re.split(r'(`[^`]+`)', line)
        processed_parts = []
        for part in parts:
            if part.startswith("`") and part.endswith("`"):
                processed_parts.append(part)
            else:
                processed_parts.append(
                    re.sub(r'\[\[([^\]]+)\]\]', _replace_wikilink, part)
                )
        result.append("".join(processed_parts))

    return "\n".join(result)


def on_pre_build(config, **kwargs):
    """Build slug map before MkDocs starts."""
    docs_dir = Path(config["docs_dir"])
    _build_slug_map(docs_dir)
    print(f"[wikilinks] {len(_slug_map)} article slugs indexed")


def on_page_markdown(markdown, page, config, **kwargs):
    """Process wiki-links in each page's markdown."""
    return _process_markdown(markdown)

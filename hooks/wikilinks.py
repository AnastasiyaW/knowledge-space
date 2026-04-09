"""
MkDocs hook: convert [[wiki-links]] to proper markdown links.
Only converts links OUTSIDE code blocks and inline code.
Resolves [[slug]] to a relative path from the current page.
"""

import os
import re
from pathlib import Path

# Cache: slug -> relative path from docs root (with .md)
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
        path_str = str(rel).replace("\\", "/")
        # Prefer domain articles over index files
        if slug not in _slug_map or md_file.name != "index.md":
            _slug_map[slug] = path_str

    _built = True


def _make_replacer(current_page_path: str):
    """Create a replacer function that resolves paths relative to current page."""
    current_dir = os.path.dirname(current_page_path)

    def _replace_wikilink(match: re.Match) -> str:
        slug = match.group(1).strip()

        # Skip code-like patterns: ['value'], [1, 2], [cond1 && cond2]
        if any(c in slug for c in ("'", '"', ",", "=", "&", "|", "(", ")", ":", "+")):
            return match.group(0)

        # Support [[domain/slug]] syntax - extract the slug part
        # e.g. [[data-engineering/apache-kafka]] -> apache-kafka
        if "/" in slug:
            slug = slug.rsplit("/", 1)[-1]

        if slug in _slug_map:
            target_path = _slug_map[slug]
            # Compute relative path from current page directory
            if current_dir:
                rel_path = os.path.relpath(target_path, current_dir).replace("\\", "/")
            else:
                rel_path = target_path
            display = slug.replace("-", " ").replace("_", " ")
            return f"[{display}]({rel_path})"

        return match.group(0)

    return _replace_wikilink


def _process_markdown(content: str, page_path: str) -> str:
    """Convert [[wiki-links]] outside code blocks."""
    replacer = _make_replacer(page_path)
    lines = content.split("\n")
    result = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # Outside code block: replace [[wiki-links]] but skip inline code
        parts = re.split(r'(`[^`]+`)', line)
        processed_parts = []
        for part in parts:
            if part.startswith("`") and part.endswith("`"):
                processed_parts.append(part)
            else:
                processed_parts.append(
                    re.sub(r'\[\[([^\]]+)\]\]', replacer, part)
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
    # page.file.src_path = e.g. "web-frontend/react-state-and-hooks.md"
    return _process_markdown(markdown, page.file.src_path)

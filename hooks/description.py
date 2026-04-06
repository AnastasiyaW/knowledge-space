"""
MkDocs hook: auto-generate meta description from article content.
Extracts the first meaningful paragraph after H1 and sets page.meta["description"].
This feeds into JSON-LD TechArticle schema and og:description in main.html.

MUST be registered BEFORE hooks/levels.py — levels injects HTML badges after H1
which would corrupt paragraph extraction.
"""

import re

# Max description length (Google truncates at ~155-160)
MAX_LEN = 155

# Markdown formatting patterns to strip
_STRIP_PATTERNS = [
    (re.compile(r'\[([^\]]+)\]\([^)]+\)'), r'\1'),       # [text](url) -> text
    (re.compile(r'\[\[([^\]]+)\]\]'), r'\1'),              # [[wiki-link]] -> wiki-link
    (re.compile(r'`([^`]+)`'), r'\1'),                     # `code` -> code
    (re.compile(r'\*\*([^*]+)\*\*'), r'\1'),               # **bold** -> bold
    (re.compile(r'\*([^*]+)\*'), r'\1'),                    # *italic* -> italic
    (re.compile(r'__([^_]+)__'), r'\1'),                    # __bold__ -> bold
    (re.compile(r'_([^_]+)_'), r'\1'),                      # _italic_ -> italic
    (re.compile(r'~~([^~]+)~~'), r'\1'),                    # ~~strike~~ -> strike
]

_SKIP_PATHS = frozenset({
    "index.md",
    "contributing/index.md",
    "privacy/index.md",
    "privacy.md",
    "for-llm-agents.md",
})


def _clean_markdown(text: str) -> str:
    """Strip markdown formatting from text."""
    for pattern, repl in _STRIP_PATTERNS:
        text = pattern.sub(repl, text)
    return text.strip()


def _truncate(text: str, max_len: int = MAX_LEN) -> str:
    """Truncate text at word boundary."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    # Find last space to avoid cutting mid-word
    last_space = truncated.rfind(' ')
    if last_space > max_len // 2:
        truncated = truncated[:last_space]
    return truncated.rstrip('.,;:') + '...'


def _extract_first_paragraph(markdown: str) -> str | None:
    """Extract first meaningful paragraph after H1 heading."""
    lines = markdown.split('\n')
    found_h1 = False
    paragraph_lines = []

    for line in lines:
        stripped = line.strip()

        # Find H1
        if not found_h1:
            if stripped.startswith('# ') and not stripped.startswith('## '):
                found_h1 = True
            continue

        # Skip empty lines between H1 and first paragraph
        if not paragraph_lines and not stripped:
            continue

        # Stop at: empty line after paragraph, heading, code block, list, hr, HTML
        if paragraph_lines and (
            not stripped
            or stripped.startswith('#')
            or stripped.startswith('```')
            or stripped.startswith('- ')
            or stripped.startswith('* ')
            or stripped.startswith('> ')
            or stripped.startswith('|')
            or stripped == '---'
            or stripped.startswith('<')
            or re.match(r'^\d+\.\s', stripped)
        ):
            break

        # Skip admonition markers, badges, and metadata-like lines
        if stripped.startswith('!!!') or stripped.startswith('???'):
            break

        paragraph_lines.append(stripped)

    if not paragraph_lines:
        return None

    text = ' '.join(paragraph_lines)
    text = _clean_markdown(text)

    # Skip if too short to be meaningful
    if len(text) < 30:
        return None

    return _truncate(text)


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    """Set page.meta['description'] from first paragraph if not already set."""
    src = page.file.src_path

    # Skip non-article pages
    if src in _SKIP_PATHS:
        return markdown
    if src.startswith("blog/"):
        return markdown
    if src.startswith("contributing/"):
        return markdown
    if src.endswith("/index.md"):
        return markdown

    # Skip if description already set in frontmatter
    if page.meta and page.meta.get("description"):
        return markdown

    # Extract and set description
    desc = _extract_first_paragraph(markdown)
    if desc:
        if not page.meta:
            page.meta = {}
        page.meta["description"] = desc

    return markdown

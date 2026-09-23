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


# The news pipeline opens every projects/ and organizations/ page with a metadata block
# ("**Development line:** `project:x` · thread ...", "**Events:** 9 dated ...", "**Last
# researched:** ...", "**Freshness check:** ..."), and some reference pages open with
# "**Scope checked: 2026-09-04.** <prose>". The first is not a description at all; the
# second is a label in front of one (434 pages, 2026-09-23 audit).
_METADATA_LINE = re.compile(
    r'^\*\*(Development line|Last event|Events|Researched|Last researched|Freshness check):\*\*')
_SCOPE_PREFIX = re.compile(r'^\*\*Scope checked:[^*]*\*\*\s*')


def _is_structure(stripped: str) -> bool:
    """A line that is not paragraph prose: heading, list, quote, table, rule, HTML,
    admonition, or a pipeline metadata line."""
    return (
        stripped.startswith(('#', '- ', '* ', '> ', '|', '<', '!!!', '???'))
        or stripped == '---'
        or bool(re.match(r'^\d+\.\s', stripped))
        or bool(_METADATA_LINE.match(stripped))
    )


def _attribute_safe(text: str) -> str:
    """The description goes into content="..." attributes unescaped (MkDocs renders
    without autoescape), so a double quote ended the attribute early: 15 pages shipped a
    truncated description plus stray attributes (measured 2026-09-23)."""
    return text.replace('"', "'")


def _extract_first_paragraph(markdown: str) -> str | None:
    """Extract the first prose paragraph after the H1.

    Structure before the first paragraph (a heading, list, table, admonition, code
    block) is skipped rather than collected: a hub page that opened with "## Topics"
    used to get "## Topics ..." as its description.
    """
    lines = markdown.split('\n')
    found_h1 = False
    in_code = False
    paragraph_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        if not found_h1:
            if stripped.startswith('# ') and not stripped.startswith('## '):
                found_h1 = True
            continue

        if stripped.startswith('```') or stripped.startswith('~~~'):
            if paragraph_lines:
                break
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped:
            if paragraph_lines:
                break
            continue
        if _is_structure(stripped):
            if paragraph_lines:
                break
            continue

        paragraph_lines.append(stripped)

    if not paragraph_lines:
        return None

    text = _clean_markdown(_SCOPE_PREFIX.sub('', ' '.join(paragraph_lines)))

    # Skip if too short to be meaningful
    if len(text) < 30:
        return None

    return _attribute_safe(_truncate(text))


# Hub sections that say nothing about the topic.
_GENERIC_SECTIONS = frozenset({"additional references", "see also", "related", "other"})


def _hub_description(markdown: str) -> str | None:
    """Describe a hub page by its article count and section names.

    13 of 29 domain hubs are only headings and link lists (no prose paragraph), so they
    kept the one site-wide default description (measured 2026-09-23). Their sections are
    an accurate, self-updating summary: "Kafka & Message Queues: 43 articles on Core
    Concepts, Stream Processing, ...".
    """
    h1 = re.search(r'^# +(.+)$', markdown, re.M)
    articles = set(re.findall(r'^\s*[-*] +\[\[?([^\]|#)]+)', markdown, re.M))
    sections = [_clean_markdown(s) for s in re.findall(r'^## +(.+)$', markdown, re.M)]
    sections = [s for s in sections if s.lower() not in _GENERIC_SECTIONS]
    if not h1 or not articles or not sections:
        return None

    head = f"{_clean_markdown(h1.group(1))}: {len(articles)} articles on "
    picked: list[str] = []
    for section in sections:
        if len(head + ", ".join(picked + [section]) + ", and more.") > MAX_LEN:
            break
        picked.append(section)
    if not picked:
        return None
    tail = "." if len(picked) == len(sections) else ", and more."
    return _attribute_safe(head + ", ".join(picked) + tail)


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    """Set page.meta['description'] from first paragraph if not already set."""
    src = page.file.src_uri   # always "/"-separated; src_path uses "\" on Windows

    # A description written in frontmatter is kept, made safe for the attribute.
    if page.meta and page.meta.get("description"):
        page.meta["description"] = _attribute_safe(str(page.meta["description"]))
        return markdown

    # Skip non-article pages. Domain hub pages (<domain>/index.md) are articles for this
    # purpose: skipping them gave 13 hubs the one site-wide default description.
    if src in _SKIP_PATHS:
        return markdown
    if src.startswith("blog/"):
        return markdown
    if src.startswith("contributing/"):
        return markdown

    # Extract and set description
    desc = _extract_first_paragraph(markdown)
    if not desc and src.endswith("index.md"):
        desc = _hub_description(markdown)
    if desc:
        if not page.meta:
            page.meta = {}
        page.meta["description"] = desc

    return markdown

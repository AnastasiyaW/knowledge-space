"""
MkDocs hook: inject article level badges with stars.
Reads `level: 1-5` from page frontmatter and inserts a visual badge
(filled/empty stars) after the first H1 heading.
If no level in frontmatter, auto-assigns based on content analysis.
"""

import re


LEVEL_NAMES = {
    1: "Intro",
    2: "Basic",
    3: "Intermediate",
    4: "Advanced",
    5: "Expert",
}

# Keywords that indicate advanced content
ADVANCED_KEYWORDS = [
    r'\b(concurrency|parallelism|distributed|consensus|raft|paxos)\b',
    r'\b(lock-free|wait-free|memory.model|cache.coherence)\b',
    r'\b(kernel|syscall|eBPF|io_uring|mmap)\b',
    r'\b(proof|theorem|NP-hard|NP-complete|undecidable)\b',
    r'\b(unsafe|lifetime|borrow.checker|zero-cost.abstraction)\b',
    r'\b(sharding|partitioning|replication.factor|quorum)\b',
    r'\b(gradient.descent|backpropagation|transformer|attention.mechanism)\b',
    r'\b(eigenvalue|eigenvector|singular.value|matrix.decomposition)\b',
    r'\b(penetration.testing|exploit|buffer.overflow|privilege.escalation)\b',
    r'\b(compiler|AST|parser|lexer|bytecode|JIT)\b',
]

BASIC_KEYWORDS = [
    r'\b(introduction|getting.started|basics|fundamentals|overview)\b',
    r'\b(what.is|beginner|first.steps|hello.world|setup)\b',
    r'\b(tutorial|walkthrough|step.by.step)\b',
    r'\b(CRUD|REST.API.basics|HTTP.methods)\b',
]

ADVANCED_RE = [re.compile(p, re.IGNORECASE) for p in ADVANCED_KEYWORDS]
BASIC_RE = [re.compile(p, re.IGNORECASE) for p in BASIC_KEYWORDS]


def _analyze_level(markdown: str, title: str) -> int:
    """Auto-determine article level from content analysis."""
    text = (title + " " + markdown).lower()
    lines = markdown.strip().split("\n")
    line_count = len(lines)

    # Count code blocks
    code_blocks = len(re.findall(r'```', markdown)) // 2

    # Count advanced keyword hits
    adv_hits = sum(1 for r in ADVANCED_RE if r.search(text))
    basic_hits = sum(1 for r in BASIC_RE if r.search(text))

    # Count headings depth (h3, h4 = more structured = more complex)
    deep_headings = len(re.findall(r'^#{3,4}\s', markdown, re.MULTILINE))

    # Scoring
    score = 3  # default intermediate

    # Title-based hints
    title_lower = title.lower()
    if any(w in title_lower for w in ["fundamentals", "basics", "introduction", "overview", "getting started"]):
        score -= 1
    if any(w in title_lower for w in ["advanced", "internals", "deep dive", "optimization", "performance"]):
        score += 1

    # Content complexity
    if basic_hits >= 3:
        score -= 1
    if adv_hits >= 2:
        score += 1
    if adv_hits >= 4:
        score += 1

    # Length and structure
    if line_count > 400 and deep_headings > 5:
        score += 1
    elif line_count < 80 and code_blocks < 2:
        score -= 1

    # Code density (lots of code = practical, moderate level)
    if code_blocks > 8 and adv_hits < 2:
        score = max(score, 3)  # at least intermediate

    return max(1, min(5, score))


def _make_badge(level: int) -> str:
    """Generate HTML for level stars badge."""
    level = max(1, min(5, level))
    stars = []
    for i in range(1, 6):
        if i <= level:
            stars.append('<span class="ks-level__star--filled">&#9733;</span>')
        else:
            stars.append('<span class="ks-level__star--empty">&#9733;</span>')
    stars_html = "".join(stars)
    name = LEVEL_NAMES.get(level, "")
    return (
        f'\n<div class="ks-level-badge" markdown="0">'
        f'<span class="ks-level">{stars_html}</span>'
        f' {name}'
        f'</div>\n'
    )


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    """Inject level badge after first H1 heading."""
    src = page.file.src_path
    # Skip non-article pages
    if src in ("index.md", "contributing/index.md", "privacy/index.md", "privacy.md"):
        return markdown
    if src.startswith("blog/"):
        return markdown
    if src.startswith("contributing/"):
        return markdown
    # Skip any index.md files (section pages, not articles)
    if src.endswith("/index.md"):
        return markdown

    # Get level from frontmatter or auto-analyze
    level = None
    if page.meta and "level" in page.meta:
        try:
            level = int(page.meta["level"])
        except (ValueError, TypeError):
            level = None

    if level is None:
        title = page.meta.get("title", "") if page.meta else ""
        level = _analyze_level(markdown, title)

    badge = _make_badge(level)

    # Insert after first H1 line
    match = re.search(r"^(# .+)$", markdown, re.MULTILINE)
    if match:
        pos = match.end()
        markdown = markdown[:pos] + badge + markdown[pos:]

    return markdown

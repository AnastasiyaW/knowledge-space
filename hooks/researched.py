"""Render and validate the date on which an article was actually researched.

``last_researched`` is deliberately separate from a Git commit date: editing links,
formatting, or generated navigation does not make factual claims current.  Articles
without this field are legacy/unknown rather than implicitly fresh.
"""

from __future__ import annotations

from datetime import date, datetime
import re


FIELD = "last_researched"
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SKIP_PATHS = frozenset({"index.md", "contributing/index.md", "privacy/index.md", "privacy.md"})


def parse_last_researched(value, *, today: date | None = None) -> date:
    """Return a strict, non-future ISO date or raise ValueError.

    MkDocs/YAML may give us either an ISO string or a ``date`` instance.  Datetimes,
    prose and future dates are all ambiguous for a research record and therefore fail
    the build instead of being silently ignored.
    """
    today = today or date.today()
    if isinstance(value, datetime):
        raise ValueError(f"{FIELD} must be a date, not a timestamp")
    if isinstance(value, date):
        parsed = value
    elif isinstance(value, str) and _ISO_DATE.fullmatch(value):
        try:
            parsed = date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError(f"{FIELD} must be a valid YYYY-MM-DD date") from exc
    else:
        raise ValueError(f"{FIELD} must be a valid YYYY-MM-DD date")
    if parsed > today:
        raise ValueError(f"{FIELD} cannot be in the future ({parsed.isoformat()})")
    return parsed


def _is_article(src: str) -> bool:
    return not (
        src in _SKIP_PATHS
        or src.startswith("blog/")
        or src.startswith("contributing/")
        or src.endswith("/index.md")
    )


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    """Place a verified research date below the article title when supplied."""
    src = page.file.src_uri
    if not page.meta or FIELD not in page.meta:
        # MkDocs catches YAML errors and leaves the rejected front matter in
        # the body. An impossible YAML date must not masquerade as legacy data.
        front = re.match(r"\A\ufeff?---\s*\n(.*?)\n---\s*(?:\n|$)", markdown, re.DOTALL)
        if front and re.search(r"^['\"]?last_researched['\"]?\s*:", front[1], re.MULTILINE):
            raise ValueError(f"{src}: last_researched front matter could not be parsed")
        return markdown
    researched = parse_last_researched(page.meta[FIELD])
    if not _is_article(src):
        return markdown
    marker = f"\n*Last researched: <time datetime=\"{researched.isoformat()}\">{researched.isoformat()}</time>*\n"
    match = re.search(r"^(# .+)$", markdown, re.MULTILINE)
    if not match:
        return markdown
    return markdown[:match.end()] + marker + markdown[match.end():]

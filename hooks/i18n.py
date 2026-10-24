"""MkDocs hook: connect the language branches page by page.

Every language is its own MkDocs build (mkdocs.yml for English, mkdocs.<lang>.yml for the
rest) over its own docs tree, listed in `extra.locales`. For each page this hook
- points the language selector and the hreflang links at the same page in the other
  languages, and only at languages that have it (Material renders both from
  `extra.alternate`, so pointing every page at the locale home pages told search engines
  that all 1,400 articles were translations of the home page);
- adds x-default (English) through the `i18n_x_default` template variable;
- puts a short note on machine-translated pages that links to the English original.
"""
from __future__ import annotations

import posixpath
import re
from pathlib import Path, PurePosixPath

_pages: dict[str, set[str]] = {}


def _url(src_uri: str) -> str:
    """The directory URL MkDocs gives a source file (use_directory_urls is on)."""
    if src_uri == "index.md":
        return ""
    if src_uri.endswith("/index.md"):
        return src_uri[: -len("index.md")]
    return src_uri[: -len(".md")] + "/"


def on_config(config, **kwargs):
    root = Path(config.config_file_path).parent
    _pages.clear()
    for loc in config["extra"].get("locales", []):
        docs = root / loc["docs"]
        _pages[loc["lang"]] = {p.relative_to(docs).as_posix() for p in docs.rglob("*.md")}
    config["extra"]["alternate"] = []
    return config


def _translations(src_uri: str, config) -> list[dict]:
    return [loc for loc in config["extra"].get("locales", []) if src_uri in _pages.get(loc["lang"], ())]


_MD_LINK = re.compile(r"\]\((?!https?:|mailto:|#)([^)\s#]+\.md)(#[^)\s]*)?\)")


def _fallback_links(markdown: str, src_uri: str, config) -> str:
    """A link to a page this language does not have yet goes to the English original
    instead of breaking the strict build or the reader's click."""
    lang = config["extra"].get("content_language")
    english = next((loc for loc in config["extra"].get("locales", []) if loc["lang"] == "en"), None)
    if not english or lang == "en" or lang not in _pages:
        return markdown
    here = PurePosixPath(src_uri).parent

    def swap(m):
        target = posixpath.normpath((here / m.group(1)).as_posix())
        if target in _pages[lang] or target not in _pages.get("en", ()):
            return m.group(0)
        return f"]({english['base']}{_url(target)}{m.group(2) or ''})"

    return _MD_LINK.sub(swap, markdown)


def on_page_markdown(markdown, page, config, **kwargs):
    markdown = _fallback_links(markdown, page.file.src_uri, config)
    if not (page.meta and page.meta.get("translation") == "machine"):
        return markdown
    english = next((loc for loc in config["extra"]["locales"] if loc["lang"] == "en"), None)
    note = config["extra"].get("ui", {}).get("machine_translation_note")
    if not english or not note:
        return markdown
    url = english["base"] + _url(page.file.src_uri)
    return f'!!! info ""\n    {note.format(url=url)}\n\n' + markdown


def on_page_context(context, page, config, **kwargs):
    found = _translations(page.file.src_uri, config)
    if len(found) > 1:
        path = _url(page.file.src_uri)
        config["extra"]["alternate"] = [
            {"name": loc["name"], "link": loc["base"] + path, "lang": loc["hreflang"]} for loc in found
        ]
        english = next((loc for loc in found if loc["lang"] == "en"), None)
        context["i18n_x_default"] = english["base"] + path if english else None
    else:
        config["extra"]["alternate"] = []
        context["i18n_x_default"] = None
    return context


def on_post_page(output, page, config, **kwargs):
    # The 404 page is rendered without page context: it gets no language links rather than
    # the static root list (relative hrefs, wrong codes; review 2026-10-24).
    config["extra"]["alternate"] = []
    return output

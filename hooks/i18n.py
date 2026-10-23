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

from pathlib import Path

_pages: dict[str, set[str]] = {}
_root_alternate: list[dict] = []


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
    _root_alternate[:] = list(config["extra"].get("alternate") or [])
    return config


def _translations(src_uri: str, config) -> list[dict]:
    return [loc for loc in config["extra"].get("locales", []) if src_uri in _pages.get(loc["lang"], ())]


def on_page_markdown(markdown, page, config, **kwargs):
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
    # 404 and other pages rendered outside on_page_context keep the plain locale list.
    config["extra"]["alternate"] = list(_root_alternate)
    return output

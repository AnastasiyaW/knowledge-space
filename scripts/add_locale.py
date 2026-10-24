"""Create a new language branch: mkdocs.<lang>.yml and the hand-written root pages.

The Russian branch is the template: its config carries every interface string and its
root pages (home, start here, privacy, about, contact, agent guide, llms.txt) are the
reviewed set. They are translated once, synchronously, and checked like articles
(scripts/translate_locales.py); the articles themselves go through translate_locales.py.

  py -3 scripts/add_locale.py fr        # writes mkdocs.fr.yml and locales/fr/docs/*.md
Requires ANTHROPIC_API_KEY. Exit 0 written, 1 a check failed (nothing written), 2 not checked.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import translate_locales as tl  # noqa: E402

ROOT = tl.ROOT
TEMPLATE = "ru"
ROOT_PAGES = ("index.md", "start-here.md", "privacy.md", "about.md", "contact.md", "for-llm-agents.md", "llms.txt")
SEARCH_LANG = {"zh-CN": "zh"}
SOURCE_NOTE = ("The source text is Russian (not English). Translate it into {language}. "
               "Where it says that articles are translated into Russian, say {language} instead.\n\n")


def complete(system: str, text: str) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY is not set: not checked"); sys.exit(2)
    body = {"model": tl.MODEL, "max_tokens": tl.MAX_TOKENS, "system": system,
            "messages": [{"role": "user", "content": text}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(), headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        msg = json.load(r)
    if msg.get("stop_reason") != "end_turn":
        raise ValueError(f"stop_reason {msg.get('stop_reason')}")
    return "".join(c.get("text", "") for c in msg["content"]).strip("\n") + "\n"


def yaml_keys(text: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"(?m)^(\s*-?\s*[A-Za-z_][\w.-]*):", text)]


def translate_config(lang: str, language: str) -> str:
    src = (ROOT / f"mkdocs.{TEMPLATE}.yml").read_text(encoding="utf-8")
    system = (f"You translate the human-readable string values of a YAML file from Russian into {language}. "
              "Keep every key, indentation, URL, `{url}` placeholder, markdown link target, YAML tag and "
              "non-text value exactly as they are. Return only the YAML.")
    out = complete(system, src)
    out = re.sub(r"^```\w*\n|\n```\s*$", "", out)
    if yaml_keys(out) != yaml_keys(src):
        raise ValueError("config keys changed")
    if out.count("{url}") != src.count("{url}") or tl.MDLINK_URL_RE.findall(out) != tl.MDLINK_URL_RE.findall(src):
        raise ValueError("config links or placeholders changed")
    swaps = {
        f"site_url: https://happyin.space/{TEMPLATE}/": f"site_url: https://happyin.space/{lang}/",
        f"docs_dir: locales/{TEMPLATE}/docs": f"docs_dir: locales/{lang}/docs",
        f"site_dir: site/{TEMPLATE}": f"site_dir: site/{lang}",
        f"  language: {TEMPLATE}\n": f"  language: {SEARCH_LANG.get(lang, lang).lower()}\n",
        f"content_language: {TEMPLATE}": f"content_language: {lang}",
        f"      lang: {TEMPLATE}\n  - meta": f"      lang: {SEARCH_LANG.get(lang, lang)}\n  - meta",
    }
    for old, new in swaps.items():
        if out.count(old) != 1:
            raise ValueError(f"config line not found once: {old!r}")
        out = out.replace(old, new)
    return out


def translate_page(name: str, lang: str, language: str) -> str:
    source = (ROOT / "locales" / TEMPLATE / "docs" / name).read_text(encoding="utf-8").replace("\r\n", "\n")
    fm, body = tl.split_front_matter(source)
    protected, blocks, slugs = tl.protect(body)
    out = complete(SOURCE_NOTE.format(language=language) + tl.SYSTEM.format(language=language), fm + protected)
    tr_fm, tr_body = tl.split_front_matter(out)
    if fm and not tr_fm:
        tr_fm = tl.front_matter_from_heading(fm, tr_body)
    tl.check_structure(protected, tr_body)
    restored = tl.restore(tr_body, blocks, slugs, body) if name.endswith(".md") else tr_body
    return (tr_fm + restored.lstrip("\n")).replace(f"https://happyin.space/{TEMPLATE}/", f"https://happyin.space/{lang}/")


def main() -> int:
    lang = sys.argv[1]
    language = tl.LANGS[lang]
    files: dict[Path, str] = {}
    try:
        files[ROOT / f"mkdocs.{lang}.yml"] = translate_config(lang, language)
        for name in ROOT_PAGES:
            files[ROOT / "locales" / lang / "docs" / name] = translate_page(name, lang, language)
    except ValueError as e:
        print(f"FAIL {lang}: {e} (nothing written)")
        return 1
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        print("wrote", path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

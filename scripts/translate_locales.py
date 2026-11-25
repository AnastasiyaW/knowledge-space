"""Translate knowledge-base articles into the localized branches under locales/<lang>/docs/.

English in docs/ is the source of truth. Each translation records the SHA-256 of the English
file it was made from, so `plan` can tell missing, stale and fresh pages apart and only the
changed articles are sent again.

What the model never sees or may not change:
- fenced code blocks are swapped for placeholders and restored byte for byte;
- headings get the English anchor back as an attr_list id, so `page.md#anchor` links and
  shared URLs keep working in every language;
- wiki-link targets, link URLs, front-matter keys other than title/description.
A result that fails any of these checks is not written; `collect` reports it for resubmission.

  py -3 scripts/translate_locales.py plan    --lang ru
  py -3 scripts/translate_locales.py submit  --lang ru [--limit N] [--only domain/slug.md ...]
  py -3 scripts/translate_locales.py status  <batch_id>
  py -3 scripts/translate_locales.py collect <batch_id>

Requires ANTHROPIC_API_KEY. Uses the Message Batches API (asynchronous, half price).
Exit codes: 0 ok, 1 some pages failed or nothing to do where work was expected, 2 not checked.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify as toc_slugify, unique

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "hooks"))
from levels import _analyze_level  # noqa: E402  same level as the English page, not re-guessed from translated words

DOCS = ROOT / "docs"
STATE = ROOT / "var" / "translate"
API = "https://api.anthropic.com/v1/messages/batches"
# Owner routing rule 2026-10-13: execution work runs on Claude Haiku 5.5.
MODEL = "claude-haiku-5-5"
MAX_TOKENS = 32000  # longest article is ~500 lines; Russian/German expand ~1.4x in tokens
# A request carries at most this many characters; longer pages go in parts split at "## ".
# Measured: the 107 KB knowledge-base map ran out of output tokens in one request.
PART_CHARS = 30000

LANGS = {
    "ru": "Russian",
    "zh-CN": "Simplified Chinese",
    "es": "Spanish",
    "de": "German",
    "fr": "French",
    "ko": "Korean",
}
# Top-level docs/ entries that are not translated article content.
SKIP_TOP = {"blog", "contributing", "assets", "javascripts", "stylesheets", "skills"}

FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")
PLACEHOLDER = "@@CODE_{}@@"
PLACEHOLDER_RE = re.compile(r"@@CODE_(\d+)@@")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK_URL_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
ATTR_ID_RE = re.compile(r"\s*\{[^}]*#[^}]*\}\s*$")

SYSTEM = """You translate one technical knowledge-base article from English into {language}.
Readers are engineers. Produce a faithful, natural, precise translation in the register of good
technical documentation written natively in {language}; no simplification, no added content,
no commentary, no notes about the translation.

Keep exactly as they are:
- every line of the form @@CODE_<n>@@ (code placeholders), on its own line, same order, same indentation;
- everything between backticks, byte for byte, even when it looks like English words, a formula
  or a <placeholder> (`Toil / All tasks`, `<secret-name>` stay exactly so); URLs, file paths, commands, flags, config keys, API/function/class names,
  product, library and company names, version numbers, units;
- wiki links: [[target]] stays byte-identical; in [[target|label]] translate only the label;
- markdown link targets (the part in parentheses); translate only the link text;
- markdown structure: heading levels and count, list nesting, table columns, admonition syntax
  (!!! note "Title" - translate only the quoted title), blank lines, HTML tags and attributes.
Established English technical terms that {language}-speaking engineers normally keep in English
may stay in English.
When the input starts with a YAML block between --- lines, your answer starts with that block too:
translate only the values of `title` and `description`; copy every other line unchanged.
Return only the translated document, nothing before or after it."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_files() -> list[Path]:
    out = []
    for p in sorted(DOCS.rglob("*.md")):
        rel = p.relative_to(DOCS)
        if len(rel.parts) == 1 or rel.parts[0] in SKIP_TOP:
            continue
        if p.name.startswith("."):
            continue
        out.append(p)
    return out


def split_front_matter(text: str) -> tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 5], text[end + 5 :]
    return "", text


def target_path(lang: str, rel: Path) -> Path:
    return ROOT / "locales" / lang / "docs" / rel


def translated_source_sha(path: Path) -> str | None:
    if not path.is_file():
        return None
    fm, _ = split_front_matter(path.read_text(encoding="utf-8"))
    if not fm:
        return None
    return fm_value(fm, "source_sha256") or None


def plan(lang: str) -> dict[str, list[str]]:
    result = {"missing": [], "stale": [], "fresh": []}
    for p in source_files():
        rel = p.relative_to(DOCS)
        have = translated_source_sha(target_path(lang, rel))
        if have is None:
            result["missing"].append(rel.as_posix())
        elif have != sha256(p.read_bytes()):
            result["stale"].append(rel.as_posix())
        else:
            result["fresh"].append(rel.as_posix())
    return result


def protect(body: str) -> tuple[str, list[str], list[str]]:
    """Swap fenced code for placeholders; return text, code blocks, English heading slugs."""
    lines = body.split("\n")
    out, blocks, slugs = [], [], []
    i = 0
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if m:
            indent, fence = m.group(1), m.group(2)
            j = i + 1
            while j < len(lines):
                c = FENCE_RE.match(lines[j])
                if c and c.group(2)[0] == fence[0] and len(c.group(2)) >= len(fence) and not lines[j].strip()[len(c.group(2)):].strip():
                    break
                j += 1
            blocks.append("\n".join(lines[i : j + 1]))
            out.append(indent + PLACEHOLDER.format(len(blocks) - 1))
            i = j + 1
            continue
        h = HEADING_RE.match(lines[i])
        if h:
            title = ATTR_ID_RE.sub("", h.group(2))
            slugs.append(toc_slugify(title, "-"))
        out.append(lines[i])
        i += 1
    return "\n".join(out), blocks, english_anchors(body, slugs)


def english_anchors(body: str, fallback: list[str]) -> list[str]:
    """The ids the English build gives these headings (Python-Markdown toc, as in mkdocs.yml)."""
    md = markdown.Markdown(extensions=["toc", "attr_list", "tables", "md_in_html", "pymdownx.superfences"])
    md.convert(body)

    def flat(tokens):
        for t in tokens:
            yield t
            yield from flat(t["children"])

    ids = [t["id"] for t in flat(md.toc_tokens)]
    if len(ids) == len(fallback):
        return ids
    seen: set[str] = set()
    return [unique(s, seen) for s in fallback]


def heading_lines(body: str) -> list[int]:
    idx, in_code = [], False
    for n, line in enumerate(body.split("\n")):
        if FENCE_RE.match(line):
            in_code = not in_code
            continue
        if not in_code and HEADING_RE.match(line):
            idx.append(n)
    return idx


def restore(translated: str, blocks: list[str], slugs: list[str], source_body: str) -> str:
    """Put code back, pin English anchors on headings; raise ValueError on any mismatch."""
    found = [int(n) for n in PLACEHOLDER_RE.findall(translated)]
    if found != list(range(len(blocks))):
        raise ValueError(f"code placeholders {found[:12]} != 0..{len(blocks) - 1}")
    lines = translated.split("\n")
    heads = [n for n, line in enumerate(lines) if HEADING_RE.match(line) and not PLACEHOLDER_RE.search(line)]
    if len(heads) != len(slugs):
        raise ValueError(f"headings {len(heads)} != {len(slugs)}")
    src_levels = [HEADING_RE.match(source_body.split("\n")[n]).group(1) for n in heading_lines(source_body)]
    for n, slug, level in zip(heads, slugs, src_levels):
        m = HEADING_RE.match(lines[n])
        if m.group(1) != level:
            raise ValueError(f"heading level changed at line {n + 1}")
        text = ATTR_ID_RE.sub("", m.group(2))
        lines[n] = f"{m.group(1)} {text} {{#{slug}}}" if slug else f"{m.group(1)} {text}"
    text = "\n".join(lines)
    for i, block in enumerate(blocks):
        text = re.sub(rf"^([ \t]*){re.escape(PLACEHOLDER.format(i))}[ \t]*$", lambda _m, b=block: b, text, count=1, flags=re.M)
    if PLACEHOLDER_RE.search(text):
        raise ValueError("a code placeholder shares its line with text")
    return text


# Sentence punctuation and typographic quotes („…“ in German) are not part of a URL.
URL_RE = re.compile(r"https?://[^\s)\]>\"'`“”„«»]*[^\s)\]>\"'`“”„«».,;:!?]")
ADMONITION_RE = re.compile(r"(?m)^[ \t]*(?:!!!|\?\?\?\+?)[ \t]+([\w-]+)")
PLACEHOLDER_LINE_RE = re.compile(r"(?m)^([ \t]*)(@@CODE_\d+@@)[ \t]*$")
INLINE_CODE_RE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")


def check_structure(source: str, translated: str) -> None:
    """Compare the English and translated prose, both with code still as placeholders.

    Measured on the first full French batch: the model unwraps hard-wrapped paragraphs and
    sometimes adds backticks around identifiers, both harmless; what it must not do is drop
    a list item, a table row, a paragraph or a piece of code, or leave markup unbalanced.
    """
    def targets(s: str) -> list[str]:
        return sorted(t.strip() for t in WIKILINK_RE.findall(s))
    if targets(source) != targets(translated):
        raise ValueError("wiki-link targets changed")
    if sorted(MDLINK_URL_RE.findall(source)) != sorted(MDLINK_URL_RE.findall(translated)):
        raise ValueError("markdown link targets changed")
    if sorted(URL_RE.findall(source)) != sorted(URL_RE.findall(translated)):
        raise ValueError("URLs changed (reference links, HTML href, bare links)")
    if ADMONITION_RE.findall(source) != ADMONITION_RE.findall(translated):
        raise ValueError("admonition types changed")
    if PLACEHOLDER_LINE_RE.findall(source) != PLACEHOLDER_LINE_RE.findall(translated):
        raise ValueError("a code placeholder moved (indentation or line)")
    if first_line(source).startswith("#") and not first_line(translated).startswith("#"):
        raise ValueError("text before the first heading")
    missing = Counter(m.group(0) for m in INLINE_CODE_RE.finditer(source))
    missing.subtract(m.group(0) for m in INLINE_CODE_RE.finditer(translated))
    lost = [code for code, n in missing.items() if n > 0]
    if lost:
        raise ValueError(f"inline code lost or changed: {lost[:3]}")
    for mark in ("`", "**"):
        if translated.count(mark) % 2 and not source.count(mark) % 2:
            raise ValueError(f"unbalanced {mark!r}")

    def shape(s: str) -> tuple[int, int, list[int]]:
        lines = s.split("\n")
        blocks = len([b for b in re.split(r"\n[ \t]*\n", s) if b.strip()])
        return (blocks, sum(1 for line in lines if LIST_ITEM_RE.match(line)),
                [table_cells(line) for line in lines if line.lstrip().startswith("|")])
    (b1, i1, r1), (b2, i2, r2) = shape(source), shape(translated)
    # Equal, not "at least": an extra paragraph is how model chatter got published (review 2026-10-24).
    if i1 != i2 or r1 != r2 or b2 != b1:
        raise ValueError(f"structure changed: blocks {b1}->{b2}, list items {i1}->{i2}, "
                         f"table rows/cells {len(r1)}/{sum(r1)}->{len(r2)}/{sum(r2)}")
    if len(prose_of(translated)) > 2.5 * max(len(prose_of(source)), 200):
        raise ValueError("translation is far longer than the source")


def table_cells(line: str) -> int:
    return len(re.sub(r"`[^`]*`|\[\[[^\]]*\]\]", "", line.strip()).strip("|").split("|"))


def first_line(s: str) -> str:
    return next((line.strip() for line in s.split("\n") if line.strip()), "")


def prose_of(s: str) -> str:
    return INLINE_CODE_RE.sub("", PLACEHOLDER_RE.sub("", s))


SCRIPT_CHECK = {
    "ru": re.compile(r"[Ѐ-ӿ]"),
    "zh-CN": re.compile(r"[一-鿿]"),
    "ko": re.compile(r"[가-힯]"),
}


# Words common in English and absent from the target languages ("in", "on", "as" are left
# out: German and French use them too).
ENGLISH_WORDS = {"the", "and", "of", "to", "is", "that", "for", "with", "this", "are", "by", "you",
                 "should", "when", "not", "or", "which", "let", "need", "here", "was", "will"}
COMMENTARY_RE = re.compile(r"\b(?:[Ll]et me\b|I need to\b|I will now\b|I'll\b|[Hh]ere is the (?:corrected|correct|translated|translation)|"
                           r"[Oo]ops\b|[Hh]mm+\b|I hope this helps|[Tt]he translation (?:is|above|below)|[Aa]s requested\b|as instructed\b|"
                           r"[Tt]ranslator'?s note|Anmerkung des Übersetzers|[Nn]ote du traducteur|[Nn]ota del traductor|역자 주|译者注)")
CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")
WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def cyrillic_share(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    return sum(1 for c in letters if CYRILLIC_RE.match(c)) / len(letters) if letters else 0.0


def check_language(lang: str, prose: str, source: str = "") -> None:
    text = re.sub(r"\[\[[^\]]*\]\]|\]\([^)]*\)|https?://\S+", " ", INLINE_CODE_RE.sub(" ", prose))
    words = [w.lower() for w in WORD_RE.findall(text)]
    if len(words) >= 40 and sum(w in ENGLISH_WORDS for w in words) / len(words) > 0.08:
        raise ValueError("prose reads as English")
    for block in re.split(r"\n[ \t]*\n", text):
        # Tables of sources, quotations and quoted phrases keep their English on purpose.
        # Headings and short lines of English technical terms ("Video-to-Audio mit
        # Chain-of-Thought-Reasoning", Rust "if let") are skipped; commentary is caught above.
        if block.lstrip()[:1] in ("|", "#") or re.search(r"(?m)^\s*>", block) or re.search(r"[\"“”«»„]", block):
            continue
        bw = [w.lower() for w in WORD_RE.findall(block)]
        if len(bw) >= 10 and sum(w in ENGLISH_WORDS for w in bw) / len(bw) > 0.2:
            raise ValueError(f"a paragraph reads as English: {block.strip()[:60]!r}")
    # A phrase the English page itself quotes ("let me explain" as an example) is not commentary.
    extra = Counter(m.lower() for m in COMMENTARY_RE.findall(text))
    extra.subtract(m.lower() for m in COMMENTARY_RE.findall(source))
    if any(n > 0 for n in extra.values()):
        raise ValueError(f"model commentary in the output: {[k for k, n in extra.items() if n > 0][:2]}")
    if lang != "ru":
        # A share allowance let single letters through ("rendерst", "де-facto"; review 2026-10-24):
        # every word with a Cyrillic letter must be one the English page has.
        allowed = {w for w in WORD_RE.findall(source) if CYRILLIC_RE.search(w)}
        stray = [w for w in WORD_RE.findall(text) if CYRILLIC_RE.search(w) and w not in allowed]
        if stray:
            raise ValueError(f"Cyrillic not in the English page: {stray[:3]}")
    pattern = SCRIPT_CHECK.get(lang)
    if pattern is None:
        return
    letters = [c for c in prose if c.isalpha()]
    if letters and sum(1 for c in letters if pattern.match(c)) / len(letters) < 0.25:
        raise ValueError(f"too little {lang} script in prose")


def fm_value(fm: str, key: str) -> str:
    """A one-line front-matter value. Read line by line: some English pages carry YAML that
    does not parse (an unquoted colon in a title), and MkDocs builds them anyway."""
    m = re.search(rf"^{key}:[ \t]*(.*)$", fm, re.M)
    if not m:
        return ""
    raw = m.group(1).strip()
    if raw[:1] == "'" and raw[-1:] == "'":
        return raw[1:-1].replace("''", "'")
    if raw[:1] == '"' and raw[-1:] == '"':
        try:
            return json.loads(raw)
        except ValueError:
            return raw[1:-1]
    return raw


def build_front_matter(source_fm: str, translated_fm: str, src_sha: str, level: int) -> str:
    """The English front matter line for line, with the translated title/description and the
    translation record added; nothing else is re-serialised."""
    lines = source_fm.rstrip("\n").split("\n") if source_fm else ["---", "---"]
    for key in ("title", "description"):
        value = fm_value(translated_fm, key)
        idx = next((i for i, line in enumerate(lines) if line.startswith(f"{key}:")), None)
        if idx is not None and value and value[0] not in ">|" and fm_value(source_fm, key)[:1] not in (">", "|"):
            lines[idx] = f"{key}: {json.dumps(value, ensure_ascii=False)}"
    extra = [] if any(line.startswith("level:") for line in lines) else [f"level: {level}"]
    extra += [f"source_sha256: {src_sha}", "translation: machine", f"translated_at: '{dt.date.today().isoformat()}'"]
    return "\n".join(lines[:-1] + extra + ["---"]) + "\n"


def api(method: str, url: str, body: dict | None = None) -> dict | bytes:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY is not set: not checked"); sys.exit(2)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                raw = r.read()
                return json.loads(raw) if r.headers.get_content_type() == "application/json" else raw
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529) and attempt < 4:
                time.sleep(10 * (attempt + 1)); continue
            print(f"API {method} {url} -> {e.code}: {e.read()[:500]!r}"); sys.exit(2)
        except urllib.error.URLError as e:
            if attempt < 4:
                time.sleep(10 * (attempt + 1)); continue
            print(f"API unreachable: {e}"); sys.exit(2)


def split_parts(text: str) -> list[str]:
    """Whole sections per part, so every part is valid Markdown on its own: cut before a
    heading, or between blocks when a section alone is too long (the map page is one list)."""
    if len(text) <= PART_CHARS:
        return [text]
    parts, current, pieces = [], [], []
    for section in re.split(r"(?m)^(?=#{2,3} )", text):
        pieces += re.split(r"(?<=\n\n)(?=\S)", section) if len(section) > PART_CHARS else [section]
    for section in pieces:
        if current and sum(map(len, current)) + len(section) > PART_CHARS:
            parts.append("".join(current))
            current = []
        current.append(section)
    parts.append("".join(current))
    return parts


def front_matter_from_heading(source_fm: str, body: str) -> str:
    """The model sometimes drops the YAML block. The translated H1 is the translated title;
    a page whose description would be lost is refused instead."""
    if fm_value(source_fm, "description"):
        raise ValueError("front matter dropped")
    h1 = next((m.group(2) for line in body.split("\n") if (m := HEADING_RE.match(line)) and m.group(1) == "#"), "")
    if not h1:
        raise ValueError("front matter dropped")
    return f"---\ntitle: {json.dumps(ATTR_ID_RE.sub('', h1).strip(), ensure_ascii=False)}\n---\n"


def cmd_plan(args) -> int:
    for lang in args.lang:
        p = plan(lang)
        print(f"{lang}: missing {len(p['missing'])}, stale {len(p['stale'])}, fresh {len(p['fresh'])}")
    return 0


def cmd_submit(args) -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    requests, manifest = [], {}
    for lang in args.lang:
        p = plan(lang)
        todo = args.only or (p["missing"] + p["stale"])
        if args.limit:
            todo = todo[: args.limit]
        for rel in todo:
            src = (DOCS / rel).read_bytes()
            text = src.decode("utf-8").replace("\r\n", "\n")
            fm, body = split_front_matter(text)
            protected, blocks, _ = protect(body)
            base = f"{lang}-{sha256((lang + rel).encode())[:40]}"
            parts = split_parts(fm + protected)
            for n, part in enumerate(parts):
                cid = base if len(parts) == 1 else f"{base}-p{n}"
                manifest[cid] = {"lang": lang, "rel": rel, "sha": sha256(src), "base": base, "part": n, "parts": len(parts)}
                requests.append({"custom_id": cid, "params": {
                    "model": MODEL, "max_tokens": MAX_TOKENS,
                    "system": SYSTEM.format(language=LANGS[lang]),
                    "messages": [{"role": "user", "content": part}],
                }})
    if not requests:
        print("nothing to translate"); return 0
    batch = api("POST", API, {"requests": requests})
    (STATE / f"{batch['id']}.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"submitted {batch['id']}: {len(requests)} requests")
    return 0


def verify_written(lang: str, paths: set[str] | None = None) -> list[tuple[str, str]]:
    """Written translations that fail the current rules against their English source."""
    bad = []
    for p in source_files():
        rel = p.relative_to(DOCS)
        dest = target_path(lang, rel)
        name = dest.relative_to(ROOT).as_posix()
        if not dest.is_file() or (paths is not None and name not in paths):
            continue
        src_fm, src_body = split_front_matter(p.read_text(encoding="utf-8").replace("\r\n", "\n"))
        tr_fm, tr_body = split_front_matter(dest.read_text(encoding="utf-8"))
        try:
            src_protected = protect(src_body)[0]
            tr_protected = re.sub(r"(?m)^(#{1,6} .*?)[ \t]*\{#[^}]*\}[ \t]*$", r"\1", protect(tr_body)[0])
            heads = "\n".join(fm_value(tr_fm, k) for k in ("title", "description"))
            check_language(lang, PLACEHOLDER_RE.sub("", heads + "\n\n" + tr_protected), src_fm + src_protected)
            check_structure(src_protected, tr_protected)
        except ValueError as e:
            bad.append((name, str(e)))
    return bad


def cmd_verify(args) -> int:
    """Print written translations that fail the current rules (move them out of locales/
    and they are re-sent as missing)."""
    bad = []
    for lang in args.lang:
        for name, reason in verify_written(lang):
            bad.append(name)
            print(f"FAIL {name}: {reason}")
    if args.out:
        Path(args.out).write_text("\n".join(bad) + ("\n" if bad else ""), encoding="utf-8")
    print(f"{len(bad)} failing")
    return 1 if bad else 0


def cmd_status(args) -> int:
    b = api("GET", f"{API}/{args.batch}")
    print(json.dumps({k: b.get(k) for k in ("id", "processing_status", "request_counts", "ended_at")}))
    return 0


def cmd_collect(args) -> int:
    manifest = json.loads((STATE / f"{args.batch}.json").read_text(encoding="utf-8"))
    b = api("GET", f"{API}/{args.batch}")
    if b["processing_status"] != "ended":
        print(f"batch {args.batch} is {b['processing_status']}: not collected"); return 2
    raw = api("GET", b["results_url"])
    texts: dict[str, dict[int, str]] = {}
    errors: dict[str, str] = {}
    pages: dict[str, dict] = {}
    for line in raw.decode("utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        item = manifest.get(r["custom_id"])
        if item is None:
            continue
        base = item.get("base", r["custom_id"])
        pages[base] = item
        res = r["result"]
        if res["type"] != "succeeded":
            errors[base] = f"request {res['type']}"
        elif res["message"].get("stop_reason") != "end_turn":
            errors[base] = f"stop_reason {res['message'].get('stop_reason')}"
        else:
            text = "".join(c.get("text", "") for c in res["message"]["content"]).replace("\r\n", "\n")
            texts.setdefault(base, {})[item.get("part", 0)] = text.strip("\n") + "\n"
    ok, failed = 0, []
    for base, item in pages.items():
        lang, rel = item["lang"], item["rel"]
        got = texts.get(base, {})
        # Parts were cut at block boundaries, so a blank line goes back between them.
        out = "\n\n".join(got[n].strip("\n") for n in sorted(got)) + "\n" if got else None
        try:
            if base in errors:
                raise ValueError(errors[base])
            if len(got) != item.get("parts", 1):
                raise ValueError(f"parts {len(got)}/{item.get('parts', 1)}")
            src_bytes = (DOCS / rel).read_bytes()
            if sha256(src_bytes) != item["sha"]:
                raise ValueError("English source changed since submit")
            src_fm, src_body = split_front_matter(src_bytes.decode("utf-8").replace("\r\n", "\n"))
            src_protected, blocks, slugs = protect(src_body)
            tr_fm, tr_body = split_front_matter(out)
            if src_fm and not tr_fm:
                tr_fm = front_matter_from_heading(src_fm, tr_body)
            check_language(lang, PLACEHOLDER_RE.sub("", tr_fm + tr_body), src_fm + src_protected)
            check_structure(src_protected, tr_body)
            body = restore(tr_body, blocks, slugs, src_body)
            dest = target_path(lang, Path(rel))
            dest.parent.mkdir(parents=True, exist_ok=True)
            title = fm_value(src_fm, "title")
            front = build_front_matter(src_fm, tr_fm, item["sha"], _analyze_level(src_body, title))
            dest.write_text(front + body.lstrip("\n"), encoding="utf-8", newline="\n")
            ok += 1
        except (ValueError, KeyError, AttributeError) as e:
            failed.append({"lang": lang, "rel": rel, "reason": str(e)})
            if out is not None:  # kept for diagnosis; never published
                rejected = STATE / "rejected" / lang / rel
                rejected.parent.mkdir(parents=True, exist_ok=True)
                rejected.write_text(out, encoding="utf-8")
    report = STATE / f"{args.batch}.result.json"
    report.write_text(json.dumps({"written": ok, "failed": failed}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written {ok}, failed {len(failed)} (details: {report})")
    for f in failed[:20]:
        print(f"  FAIL {f['lang']} {f['rel']}: {f['reason']}")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("plan", "submit"):
        s = sub.add_parser(name)
        s.add_argument("--lang", action="append", choices=sorted(LANGS), required=True)
        if name == "submit":
            s.add_argument("--limit", type=int)
            s.add_argument("--only", nargs="*")
    v = sub.add_parser("verify")
    v.add_argument("--lang", action="append", choices=sorted(LANGS), required=True)
    v.add_argument("--out")
    for name in ("status", "collect"):
        s = sub.add_parser(name)
        s.add_argument("batch")
    args = ap.parse_args()
    return {"plan": cmd_plan, "submit": cmd_submit, "verify": cmd_verify, "status": cmd_status,
            "collect": cmd_collect}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())

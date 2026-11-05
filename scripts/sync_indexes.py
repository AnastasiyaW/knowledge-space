"""Sync navigation indexes with the articles a change added.

Which articles are in scope:

- by default, docs/{domain}/*.md added, modified, renamed or untracked since the merge base
  with origin/master (another ref with --base);
- with PATH arguments, exactly those articles;
- with --all, every article on disk. This is a full sweep: on a tree with old orphans it
  touches many indexes, so review its diff on its own.

What is synced, for in-scope articles only:

1. docs/{domain}/index.md - the per-domain MOC. An in-scope article linked from nowhere in
   the MOC is appended under "## Additional References".
2. docs/knowledge-base/index.md - the browse page. An in-scope article missing from its
   domain block is appended (a plain-text entry for it becomes a link), and that block's
   article count and the page total are recomputed. Blocks of other domains are left byte
   for byte.
3. Ambiguous slugs (one file name in two domains, see ambiguous_slugs). Entries the script
   writes for them are relative links, and so are the ambiguous wiki-links inside in-scope
   articles. Wiki-links to them in other files are only counted; --all pins those too.

Every output is computed in memory first. A missing configuration key, a bad path or any
other error stops the run before a single file is written; if a write itself fails, the
files already written are restored.

Run from the repository root:
    python scripts/sync_indexes.py [--check] [--all | --base REF | PATH ...]
Exit codes: 0 in sync or written, 1 --check found an index to update, 2 error (nothing written).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import traceback
from pathlib import Path

DOCS = Path("docs")
SKIP_DIRS = {"assets", "javascripts", "stylesheets", "blog", "contributing", "knowledge-base"}
EXTRA_HEADING = "## Additional References"
MAX_DESC = 100
WIKI_TARGET_RE = re.compile(r"\[\[([^\]|]+)")
MD_TARGET_RE = re.compile(r"\]\(([^)\s#:]+\.md)(?:#[^)]*)?\)")


class SyncError(Exception):
    """A configuration or input problem, raised before anything is written."""


class Pending:
    """Staged writes: every step reads through this, and nothing reaches disk before commit()."""

    def __init__(self) -> None:
        self.raw: dict[Path, bytes] = {}
        self.original: dict[Path, str] = {}
        self.texts: dict[Path, str] = {}

    def read(self, path: Path) -> str:
        if path not in self.texts:
            self.raw[path] = path.read_bytes()
            # the same newline folding as Path.read_text
            text = self.raw[path].decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
            self.original[path] = self.texts[path] = text
        return self.texts[path]

    def write(self, path: Path, text: str) -> None:
        self.read(path)
        self.texts[path] = text

    def changed(self) -> list[Path]:
        return [p for p, t in self.texts.items() if t != self.original[p]]

    def commit(self) -> list[Path]:
        """Write every changed file; if one write fails, put back the ones already written."""
        changed = self.changed()
        touched: list[Path] = []
        try:
            for p in changed:
                touched.append(p)
                p.write_text(self.texts[p], encoding="utf-8")
        except OSError:
            for p in touched:
                p.write_bytes(self.raw[p])
            raise
        return changed


def domains() -> list[str]:
    return sorted(d.name for d in DOCS.iterdir() if d.is_dir() and d.name not in SKIP_DIRS)


def articles(domain: str) -> list[Path]:
    return sorted(
        (p for p in (DOCS / domain).rglob("*.md") if p.name != "index.md"),
        key=lambda p: p.stem.lower(),
    )


def short_description(path: Path) -> str:
    """One-line summary: front-matter description, else the first body sentence."""
    text = path.read_text(encoding="utf-8")
    desc = ""
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if fm:
        m = re.search(r'^description:\s*"?(.+?)"?\s*$', fm.group(1), re.M)
        if m:
            desc = m.group(1)
        text = text[fm.end():]
    if not desc:
        body = re.sub(r"^#\s+.*$", "", text, count=1, flags=re.M)
        for para in body.split("\n\n"):
            para = para.strip()
            if para and not para.startswith(("#", "```", "|", "-", "*", "<")):
                desc = para
                break
    desc = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", desc)
    desc = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", desc)
    desc = re.sub(r"[`*_]", "", desc).replace("\n", " ")
    desc = re.sub(r"\s+", " ", desc).strip()
    desc = desc.split(". ")[0].split("; ")[0]
    if len(desc) > MAX_DESC:
        cut = desc[:MAX_DESC].rsplit(" ", 1)[0]
        desc = cut.rstrip(",;:-") + "..."
    return desc.rstrip(".").strip()


def normalize(text: str) -> str:
    """Fold a display name to the slug shape used by file names."""
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9+]+", "-", text.lower())).strip("-")


def same_file(path: Path | str) -> str:
    return os.path.normcase(os.path.normpath(path))


def linked_from(text: str, page: Path) -> tuple[set[str], set[str]]:
    """Wiki-link slugs in `text`, and the files its relative .md links point at from `page`."""
    slugs = {t.split("/")[-1].strip() for t in WIKI_TARGET_RE.findall(text)}
    files = {same_file(page.parent / t) for t in MD_TARGET_RE.findall(text)}
    return slugs, files


def entry_link(slug: str, target: Path, page: Path, amb: dict[str, list[str]]) -> str:
    """[[slug]], or a relative link from `page` when the slug names articles in two domains."""
    if slug not in amb:
        return f"[[{slug}]]"
    return f"[{article_title(target)}]({Path(os.path.relpath(target, page.parent)).as_posix()})"


# ------------------------------------------------------------------------- scope
# A scope is a set of article paths relative to DOCS, in POSIX form; None means every article.


def in_scope(path: Path, scope: set[str] | None) -> bool:
    return scope is None or path.relative_to(DOCS).as_posix() in scope


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SyncError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def changed_paths(base: str) -> list[Path]:
    """Files under docs/ added, modified or renamed since the merge base with `base`, or untracked."""
    merge_base = git("merge-base", "HEAD", base).strip()
    tracked = git("diff", "-z", "--name-only", "--diff-filter=ACMR", merge_base, "--", str(DOCS))
    untracked = git("ls-files", "-z", "--others", "--exclude-standard", "--", str(DOCS))
    return [Path(n) for n in (tracked + untracked).split("\0") if n]


def resolve_scope(paths: list[Path], base: str) -> set[str]:
    known = set(domains())
    docs_root = DOCS.resolve()

    def article_key(p: Path) -> str | None:
        try:
            rel = p.resolve().relative_to(docs_root)
        except ValueError:
            return None
        if len(rel.parts) > 1 and rel.parts[0] in known and rel.suffix == ".md" \
                and rel.name != "index.md" and p.is_file():
            return rel.as_posix()
        return None

    if paths:
        bad = [str(p) for p in paths if article_key(p) is None]
        if bad:
            raise SyncError("not an article in a domain folder: " + ", ".join(bad))
        return {article_key(p) for p in paths}
    return {key for p in changed_paths(base) if (key := article_key(p))}


# --------------------------------------------------------------------------- MOC


def sync_moc(domain: str, pending: Pending, scope: set[str] | None, amb: dict[str, list[str]]) -> int:
    idx = DOCS / domain / "index.md"
    if not idx.exists():
        return 0
    text = pending.read(idx)
    slugs, files = linked_from(text, idx)
    missing = [p for p in articles(domain)
               if p.stem not in slugs and same_file(p) not in files and in_scope(p, scope)]
    if not missing:
        return 0

    lines = [f"- {entry_link(p.stem, p, idx, amb)} - {short_description(p)}" for p in missing]
    block = "\n".join(lines)

    if EXTRA_HEADING in text:
        text = text.rstrip("\n") + "\n" + block + "\n"
    else:
        text = text.rstrip("\n") + f"\n\n{EXTRA_HEADING}\n\n" + block + "\n"
    pending.write(idx, text)
    return len(missing)


# ------------------------------------------------------------------- browse page

BLOCK_RE = re.compile(r'^\?\?\? note "(.*?)"\s*$')

# Display name + planet gradient for domains that have no block on the browse page yet.
# Names match hooks/stats.py DOMAIN_META so the page and the graph agree. A domain with an
# in-scope article and neither a block nor an entry here stops the run before any write.
NEW_BLOCK_STYLE = {
    "audio-voice": ("Voice & Audio", "#e0a878,#805828", "rgba(224,168,120,0.5)"),
    "go": ("Go", "#5ec0d8,#1a6880", "rgba(94,192,216,0.5)"),
    "llm-memory": ("LLM Memory", "#b898e0,#584878", "rgba(184,152,224,0.5)"),
    "writing": ("Natural Language & Writing", "#d8b0c8,#785068", "rgba(216,176,200,0.5)"),
}


def sync_browse_page(pending: Pending, scope: set[str] | None, amb: dict[str, list[str]]) -> tuple[int, int]:
    path = DOCS / "knowledge-base" / "index.md"
    lines = pending.read(path).split("\n")

    slug_by_domain = {d: {p.stem: p for p in articles(d)} for d in domains()}
    wanted = {d: {s for s, p in by_slug.items() if in_scope(p, scope)}
              for d, by_slug in slug_by_domain.items()}
    domain_of_anchor: dict[int, str] = {}
    current_domain: str | None = None
    for i, line in enumerate(lines):
        m = re.match(r'^<div id="([a-z0-9-]+)"></div>\s*$', line)
        if m and m.group(1) in slug_by_domain:
            domain_of_anchor[i] = m.group(1)

    # A domain with something to add but no block to add it to needs a style for a new block.
    present = set(domain_of_anchor.values())
    unstyled = [d for d in domains() if wanted[d] and d not in present and d not in NEW_BLOCK_STYLE]
    if unstyled:
        raise SyncError(
            f"no block on {path.as_posix()} and no NEW_BLOCK_STYLE entry in scripts/sync_indexes.py "
            f"for domain(s): {', '.join(unstyled)}. Add (name from hooks/stats.py DOMAIN_META, "
            "planet gradient, glow) to NEW_BLOCK_STYLE, or add the block to the browse page by hand."
        )

    out: list[str] = []
    added = relinked = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if i in domain_of_anchor:
            current_domain = domain_of_anchor[i]
            i += 1
            continue
        if current_domain and BLOCK_RE.match(line):
            domain = current_domain
            by_slug = slug_by_domain[domain]
            norm_map = {normalize(s): s for s in wanted[domain]}

            # collect the indented body of this admonition
            body_start = i + 1
            j = body_start
            while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith("    ")):
                j += 1
            body = lines[body_start:j]

            if not wanted[domain]:
                out.extend(body)  # nothing in scope: the block stays byte for byte
                i = j
                continue

            slugs, files = linked_from("\n".join(body), path)
            seen = {s for s, p in by_slug.items() if s in slugs or same_file(p) in files}
            new_body: list[str] = []
            for b in body:
                # plain-text entry: "    - Display Name - description"
                m = re.match(r"^(\s*)- (.+)$", b)
                if m and "[[" not in b and "](" not in b:
                    indent, rest = m.group(1), m.group(2)
                    parts = rest.split(" - ")
                    # the name may itself contain hyphens, so try the longest prefix first
                    for k in range(len(parts) - 1, 0, -1):
                        name = " - ".join(parts[:k]).strip()
                        slug = norm_map.get(normalize(name))
                        if slug:
                            desc = " - ".join(parts[k:]).strip()
                            b = f"{indent}- {entry_link(slug, by_slug[slug], path, amb)} - {desc}"
                            seen.add(slug)
                            relinked += 1
                            break
                new_body.append(b)

            missing = sorted((s for s in wanted[domain] if s not in seen), key=str.lower)
            while new_body and new_body[-1].strip() == "":
                new_body.pop()
            if missing:
                new_body.append("")
                new_body.append("    **More**")
                new_body.append("")
                for slug in missing:
                    link = entry_link(slug, by_slug[slug], path, amb)
                    new_body.append(f"    - {link} - {short_description(by_slug[slug])}")
                added += len(missing)
            new_body.append("")

            # rewrite the heading count
            head = BLOCK_RE.match(line).group(1)
            total = len(by_slug)
            new_head = re.sub(r"\d+ articles", f"{total} articles", head)
            out[-1] = f'??? note "{new_head}"'

            out.extend(new_body)
            i = j
            continue
        i += 1

    # Domains that never got a block on this page (added after it was last curated). The new
    # block lists every article of the domain, because its heading counts all of them.
    for domain in domains():
        if domain in present or not wanted[domain]:
            continue
        by_slug = slug_by_domain[domain]
        name, grad, glow = NEW_BLOCK_STYLE[domain]
        while out and not out[-1].strip():
            out.pop()
        out.append("")
        out.append("---")
        out.append("")
        out.append(f'<div id="{domain}"></div>')
        out.append("")
        out.append(
            '??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,'
            "rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,"
            f'{grad});box-shadow:0 0 8px {glow},inset 0 -2px 4px rgba(0,0,0,0.3)"></span>'
            f'{name} · {len(by_slug)} articles"'
        )
        out.append("")
        for slug in sorted(by_slug, key=str.lower):
            link = entry_link(slug, by_slug[slug], path, amb)
            out.append(f"    - {link} - {short_description(by_slug[slug])}")
            added += 1
        out.append("")

    text = "\n".join(out)
    total_articles = sum(len(v) for v in slug_by_domain.values())
    text = re.sub(r"\b\d{3,}\+ (curated )?articles", lambda m: f"{total_articles}+ {m.group(1) or ''}articles", text)
    text = re.sub(r"Browse \d{3,}\+ technical articles", f"Browse {total_articles}+ technical articles", text)
    pending.write(path, text)
    return added, relinked


# ------------------------------------------------------- ambiguous slug references


def article_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if fm:
        m = re.search(r'^title:\s*"?(.+?)"?\s*$', fm.group(1), re.M)
        if m:
            return m.group(1)
        text = text[fm.end():]
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else path.stem.replace("-", " ")


def ambiguous_slugs() -> dict[str, list[str]]:
    """Slugs that exist in more than one domain.

    hooks/wikilinks.py resolves [[slug]] through a single global map and strips any
    domain prefix, so a wiki-link to one of these cannot say which article it means -
    every reference lands on whichever file won the map. Those references become
    relative Markdown links instead.
    """
    seen: dict[str, list[str]] = {}
    for d in domains():
        for p in articles(d):
            seen.setdefault(p.stem, []).append(d)
    return {slug: ds for slug, ds in seen.items() if len(ds) > 1}


def fix_ambiguous_links(pending: Pending, scope: set[str] | None,
                        amb: dict[str, list[str]]) -> tuple[int, int, int]:
    """Pin ambiguous wiki-links to the referring file's own domain.

    Returns (pinned, left as cross-domain, left in files outside the scope).
    """
    if not amb:
        return 0, 0, 0
    known = domains()
    by_domain = {d: {p.stem: p for p in articles(d)} for d in known}
    scoped_slugs = set(amb) if scope is None else {Path(k).stem for k in scope} & set(amb)
    fixed = left = elsewhere = 0

    def rewrite(text: str, page: Path, own_domain: str | None) -> str:
        def repl(m: re.Match) -> str:
            nonlocal fixed, left
            slug = m.group(1).split("/")[-1].strip()
            if slug not in amb:
                return m.group(0)
            if own_domain not in amb[slug]:
                left += 1
                return m.group(0)
            fixed += 1
            return entry_link(slug, by_domain[own_domain][slug], page, amb)

        return re.sub(r"\[\[([^\]|]+)\]\]", repl, text)

    def count_elsewhere(text: str) -> int:
        return sum(1 for t in re.findall(r"\[\[([^\]|]+)\]\]", text) if t.split("/")[-1].strip() in scoped_slugs)

    # domain MOCs and article bodies: link relative to the file itself
    for domain in known:
        for path in [DOCS / domain / "index.md", *articles(domain)]:
            if not path.exists():
                continue
            text = pending.read(path)
            if scope is None or (path.name != "index.md" and in_scope(path, scope)):
                new = rewrite(text, path, domain)
                if new != text:
                    pending.write(path, new)
            else:
                elsewhere += count_elsewhere(text)

    # browse page: the domain comes from the enclosing block
    page = DOCS / "knowledge-base" / "index.md"
    if scope is not None:
        return fixed, left, elsewhere + count_elsewhere(pending.read(page))
    lines = pending.read(page).split("\n")
    current: str | None = None
    for i, line in enumerate(lines):
        m = re.match(r'^<div id="([a-z0-9-]+)"></div>\s*$', line)
        if m:
            current = m.group(1) if m.group(1) in known else None
            continue
        lines[i] = rewrite(line, page, current)
    pending.write(page, "\n".join(lines))
    return fixed, left, elsewhere


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Sync domain MOCs and the browse page with new articles.")
    ap.add_argument("paths", nargs="*", type=Path,
                    help="article files to sync (default: articles changed since the merge base with --base)")
    ap.add_argument("--all", action="store_true", help="sweep every article on disk")
    ap.add_argument("--base", default="origin/master", help="ref whose merge base defines changed articles")
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 if an index would change")
    args = ap.parse_args(argv)
    if args.all and args.paths:
        ap.error("--all and explicit paths are mutually exclusive")

    pending = Pending()
    try:
        if not (DOCS / "knowledge-base" / "index.md").is_file():
            raise SyncError(f"{(DOCS / 'knowledge-base' / 'index.md').as_posix()} not found; "
                            "run from the repository root")
        scope = None if args.all else resolve_scope(args.paths, args.base)
        if scope is not None and not scope:
            print("No changed articles under docs/ - nothing to sync.")
            return 0
        amb = ambiguous_slugs()
        moc_added = {d: sync_moc(d, pending, scope, amb) for d in domains()}
        added, relinked = sync_browse_page(pending, scope, amb)
        fixed, left, elsewhere = fix_ambiguous_links(pending, scope, amb)
    except SyncError as e:
        print(f"sync_indexes: {e}\nNothing was written.", file=sys.stderr)
        return 2
    except Exception:  # still exit 2: under --check, 1 must only ever mean "out of date"
        traceback.print_exc()
        print("sync_indexes: unexpected error. Nothing was written.", file=sys.stderr)
        return 2

    print(f"Scope: {'every article' if scope is None else f'{len(scope)} changed article(s)'}")
    for d, n in sorted(moc_added.items(), key=lambda x: -x[1]):
        if n:
            print(f"  MOC {d}: +{n}")
    print(f"MOC entries added: {sum(moc_added.values())}")
    print(f"Browse page: +{added} entries, {relinked} plain-text entries converted to links")
    print(f"Ambiguous slugs: {fixed} references pinned to their own domain, "
          f"{left} left as wiki-links (cross-domain, intent unknown)")
    if elsewhere:
        print(f"  {elsewhere} wiki-links outside the changed articles name an ambiguous changed slug; "
              "left as they are (--all pins them)")

    if args.check:
        changed = pending.changed()
        for p in changed:
            print(f"  would update {p.as_posix()}")
        return 1 if changed else 0
    try:
        changed = pending.commit()
    except OSError as e:
        print(f"sync_indexes: write failed ({e}); the files already written were restored.", file=sys.stderr)
        return 2
    for p in changed:
        print(f"  updated {p.as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

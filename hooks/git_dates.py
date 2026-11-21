"""
MkDocs hook: page dates come from git history, not from the build.

Without it every sitemap <lastmod> is the build day (all 1,428 English URLs said 2026-11-21
on 2026-11-21) and TechArticle had no dateModified, so a crawler cannot tell a changed page
from an unchanged one. Front matter `date` / `updated` written by hand still wins.

One `git log` per build reads the whole history once (2,263 commits, 2026-11-21). A shallow
clone would date every page by the last commit only, so it stops the build instead.
"""

import subprocess
from pathlib import Path

# repo-relative POSIX path -> (first commit date, last commit date), YYYY-MM-DD
_DATES: dict[str, tuple[str, str]] = {}
_ROOT: list[Path] = []


def _git(docs: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=docs, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


def read_history(log: str) -> dict[str, tuple[str, str]]:
    """Parse `git log --format=%x00%cs --name-only` (newest first) into (created, modified)."""
    dates: dict[str, tuple[str, str]] = {}
    day = ""
    for line in log.splitlines():
        if line.startswith("\x00"):
            day = line[1:]
        elif line and day:
            modified = dates[line][1] if line in dates else day
            dates[line] = (day, modified)
    return dates


def on_config(config, **kwargs):
    docs = Path(config["docs_dir"]).resolve()
    if _git(docs, "rev-parse", "--is-shallow-repository").strip() == "true":
        raise SystemExit("git_dates: shallow clone, page dates would all be the last commit; "
                         "check out with fetch-depth: 0")
    _ROOT[:] = [Path(_git(docs, "rev-parse", "--show-toplevel").strip())]
    _DATES.clear()
    _DATES.update(read_history(_git(docs, "log", "--format=%x00%cs", "--name-only", "--no-renames", "--", ".")))
    return config


def on_page_markdown(markdown, page, config, files, **kwargs):
    source = (Path(config["docs_dir"]).resolve() / page.file.src_uri).relative_to(_ROOT[0]).as_posix()
    dates = _DATES.get(source)
    if dates:
        created, modified = dates
        page.update_date = modified
        page.meta.setdefault("date", created)
        page.meta.setdefault("updated", modified)
    return markdown

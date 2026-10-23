"""The index syncer must fail before writing and touch only the indexes of changed articles."""
from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import sync_indexes  # noqa: E402

GAMMA_BLOCK = """??? note "Gamma · 7 articles"

    - [[new-one]] - Gamma's own
"""

BROWSE = f"""# Browse

1850+ curated articles across 3 domains.

<div id="alpha"></div>

??? note "Alpha · 1 articles"

    - [[linked]] - Already listed

---

<div id="gamma"></div>

{GAMMA_BLOCK}"""


def article(title: str) -> str:
    return f"# {title}\n\n{title} body sentence.\n"


class ScopedSyncFailsBeforeWriting(unittest.TestCase):
    """Measured 2026-10-01 on master f3ad807 while adding two image-generation articles: the
    script appended 494 lines of old orphans to 12 domain MOCs, then crashed with
    KeyError: 'organizations', a registered domain with no browse-page block and no
    NEW_BLOCK_STYLE entry. Here `beta` plays organizations and `orphan` the old orphans;
    `new-one` also exists in `gamma`, so its entries are relative links, and a second run
    must still find nothing to do (it used to re-add those on every run). Gamma's stale
    count and its notes article show that files outside the scope are left alone. Once
    beta has a style, its new block must converge on the first write too."""

    def test_missing_style_writes_nothing_and_scope_limits_the_edits(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            files = {
                "alpha/index.md": "# Alpha\n\n- [[linked]] - Already listed\n",
                "alpha/linked.md": article("Linked"),
                "alpha/orphan.md": article("Orphan"),
                "alpha/new-one.md": article("New one"),
                "beta/index.md": "# Beta\n",
                "beta/fresh.md": article("Fresh"),
                "gamma/index.md": "# Gamma\n\n- [[new-one]] - Gamma's own\n",
                "gamma/new-one.md": article("Gamma new one"),
                "gamma/notes.md": "# Notes\n\nSee [[new-one]] for the gamma one.\n",
                "knowledge-base/index.md": BROWSE,
            }
            for rel, text in files.items():
                (docs / rel).parent.mkdir(parents=True, exist_ok=True)
                (docs / rel).write_text(text, encoding="utf-8")
            snapshot = lambda: {rel: (docs / rel).read_bytes() for rel in files}  # noqa: E731
            before = snapshot()

            err = io.StringIO()

            def run(*args: str) -> int:
                argv = [str(docs / a) if a.endswith(".md") else a for a in args]
                err.seek(0)
                err.truncate()
                with mock.patch.object(sync_indexes, "DOCS", docs), \
                        redirect_stdout(io.StringIO()), redirect_stderr(err):
                    return sync_indexes.main(argv)

            # beta needs a new browse block and has no style: a named error, not one byte written
            self.assertEqual(run("alpha/new-one.md", "beta/fresh.md"), 2)
            self.assertIn("NEW_BLOCK_STYLE", err.getvalue())
            self.assertIn("beta", err.getvalue())
            self.assertNotIn("Traceback", err.getvalue())
            self.assertEqual(snapshot(), before)
            self.assertEqual(run("--check", "alpha/new-one.md"), 1)
            self.assertEqual(snapshot(), before)

            # alpha alone: only the changed article is added, the old orphan stays out
            self.assertEqual(run("alpha/new-one.md"), 0)
            moc = (docs / "alpha/index.md").read_text(encoding="utf-8")
            browse = (docs / "knowledge-base/index.md").read_text(encoding="utf-8")
            self.assertIn("[New one](new-one.md)", moc)
            self.assertIn("[New one](../alpha/new-one.md)", browse)
            self.assertNotIn("orphan", moc + browse)
            self.assertIn("Alpha · 3 articles", browse)
            self.assertIn("6+ curated articles", browse)
            self.assertIn(GAMMA_BLOCK, browse)
            for rel in ("beta/index.md", "gamma/index.md", "gamma/new-one.md", "gamma/notes.md"):
                self.assertEqual((docs / rel).read_bytes(), before[rel], rel)
            self.assertEqual(run("--check", "alpha/new-one.md"), 0)

            # with a style, beta gets a new block after gamma's (in scope, so normalised), and a
            # second run has nothing left to do
            style = {"beta": ("Beta", "#ffffff,#000000", "rgba(0,0,0,0.5)")}
            with mock.patch.dict(sync_indexes.NEW_BLOCK_STYLE, style):
                self.assertEqual(run("gamma/new-one.md", "beta/fresh.md"), 0)
                self.assertEqual(run("--check", "gamma/new-one.md", "beta/fresh.md"), 0)
            self.assertIn('<div id="beta"></div>', (docs / "knowledge-base/index.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

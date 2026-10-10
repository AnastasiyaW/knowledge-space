"""The last_researched frontmatter contract must be factual, not a commit surrogate."""
from __future__ import annotations

import importlib.util
import unittest
from datetime import date, datetime
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("researched", ROOT / "hooks" / "researched.py")
researched = importlib.util.module_from_spec(spec)
spec.loader.exec_module(researched)


def page(src: str, meta: dict | None = None):
    return SimpleNamespace(file=SimpleNamespace(src_uri=src), meta=meta or {})


class LastResearched(unittest.TestCase):
    ARTICLE = "# Example\n\nA factual opening paragraph.\n"

    def test_renders_a_real_frontmatter_date_below_the_h1(self):
        rendered = researched.on_page_markdown(
            self.ARTICLE, page("llm-agents/example.md", {"last_researched": "2026-09-02"}), {}, None
        )
        self.assertIn('<time datetime="2026-09-02">2026-09-02</time>', rendered)
        self.assertLess(rendered.index("# Example"), rendered.index("Last researched"))

    def test_legacy_article_without_the_field_stays_unknown_and_unmodified(self):
        self.assertEqual(
            researched.on_page_markdown(self.ARTICLE, page("llm-agents/example.md"), {}, None), self.ARTICLE
        )

    def test_rejects_prose_timestamps_and_future_dates(self):
        for value in ("recently", "2026-9-2", datetime(2026, 9, 2), "2099-01-01"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    researched.parse_last_researched(value, today=date(2026, 10, 10))

    def test_accepts_yaml_date_scalars(self):
        self.assertEqual(
            researched.parse_last_researched(date(2026, 9, 2), today=date(2026, 10, 10)), date(2026, 9, 2)
        )

    def test_rejects_frontmatter_that_mkdocs_could_not_parse(self):
        raw = "---\ntitle: Example\nlast_researched: 2026-02-30\n---\n" + self.ARTICLE
        with self.assertRaisesRegex(ValueError, "could not be parsed"):
            researched.on_page_markdown(raw, page("llm-agents/example.md"), {}, None)
        with self.assertRaises(ValueError):
            researched.on_page_markdown(self.ARTICLE, page("blog/index.md", {"last_researched": "2099-01-01"}), {}, None)

"""Causal checks for the human-facing entry route."""
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HumanEntry(unittest.TestCase):
    def test_home_links_to_a_task_first_guide(self) -> None:
        home = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs" / "start-here.md").read_text(encoding="utf-8")

        self.assertIn('href="start-here/"', home)
        self.assertIn("[open the human guide](start-here.md)", home)
        self.assertIn("## 1. Choose the closest task", guide)
        self.assertIn("## 2. Read a page as a decision aid", guide)
        self.assertIn("[For AI Agents](for-llm-agents.md)", guide)

    def test_schema_only_advertises_published_languages(self) -> None:
        template = (ROOT / "overrides" / "main.html").read_text(encoding="utf-8")

        self.assertIn('"name": "English", "alternateName": "en"', template)
        for unpublished_language in ("Chinese", "Korean", "Spanish", "German", "French"):
            self.assertNotIn(f'"name": "{unpublished_language}"', template)


if __name__ == "__main__":
    unittest.main()

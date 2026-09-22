"""The author-name guard must flag bylines and initials, not product titles or "U.S.".

The five false positives are the exact lines the build reported on 2026-09-22.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate", ROOT / "hooks" / "validate.py")
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)


class NameGuard(unittest.TestCase):
    NOT_NAMES = (
        "| https://www.capcut.com/ | CapCut AI Video Editor: Smart Online Video Editing with Advanced AI Tools | 2026-09-04 |",
        "| https://www.capcut.com/tools/online-video-editor | Free Online Video Editor: Create Videos Easily | CapCut | 2026-09-04 |",
        "- Workflow editor: builds and edits node-based pipelines from natural language.",
        "- 2023-07-12 — NotebookLM launched from Project Tailwind as a small U.S. Google Labs rollout.",
        "- В CI явно задавайте версию Editor: без неё неинтерактивный `unity install` завершается ошибкой.",
    )
    NAMES = (
        "Author: John Smith",
        "- Автор: Иван Иванов",
        "Translator: Jane Doe",
        "As shown by M. D. Fairchild in the appearance model.",
        "Written by Alan Kay",
    )

    def test_titles_and_abbreviations_pass(self) -> None:
        for line in self.NOT_NAMES:
            self.assertEqual(validate.check_names("x.md", line), [], line)

    def test_bylines_and_initials_are_still_caught(self) -> None:
        for line in self.NAMES:
            self.assertTrue(validate.check_names("x.md", line), line)


if __name__ == "__main__":
    unittest.main()

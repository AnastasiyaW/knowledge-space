"""Static contracts for real, reviewed language branches."""
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LocalizedBranches(unittest.TestCase):
    def test_root_declares_only_published_language_branches(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("link: /ru/", config)
        self.assertIn("link: /zh-CN/", config)
        self.assertIn('content_language: en', config)
        self.assertIn('ga4_measurement_id: !ENV [HAPPYIN_GA4_MEASUREMENT_ID, ""]', config)

    def test_locales_are_independent_projects_without_english_fallback(self) -> None:
        for locale, language in (("ru", "ru"), ("zh-CN", "zh")):
            config = (ROOT / f"mkdocs.{locale}.yml").read_text(encoding="utf-8")
            self.assertIn(f"docs_dir: locales/{locale}/docs", config)
            self.assertIn(f"site_dir: site/{locale}", config)
            self.assertIn(f"language: {language}", config)
            self.assertNotIn("fallback_to_default", config)

    def test_every_published_branch_has_a_human_entry_and_privacy_page(self) -> None:
        for locale, marker in (("ru", "Начните с задачи"), ("zh-CN", "从任务开始")):
            docs = ROOT / "locales" / locale / "docs"
            self.assertIn(marker, (docs / "start-here.md").read_text(encoding="utf-8"))
            self.assertTrue((docs / "index.md").is_file())
            self.assertTrue((docs / "privacy.md").is_file())
            self.assertTrue((docs / "for-llm-agents.md").is_file())

    def test_template_uses_configured_language_and_shared_assets(self) -> None:
        template = (ROOT / "overrides" / "main.html").read_text(encoding="utf-8")
        self.assertIn("content_language = config.extra.content_language", template)
        self.assertIn("shared_asset_url = config.extra.shared_asset_url", template)
        self.assertIn('"inLanguage": "{{ content_language }}"', template)


if __name__ == "__main__":
    unittest.main()

"""Tests for the consent-gated GA4 integration."""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OptionalAnalytics(unittest.TestCase):
    def test_consent_boundary(self) -> None:
        completed = subprocess.run(
            ["node", str(ROOT / "tests" / "analytics_consent_harness.mjs")],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS analytics consent harness", completed.stdout)

    def test_source_keeps_measurement_id_unconfigured(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        template = (ROOT / "overrides" / "main.html").read_text(encoding="utf-8")
        privacy = (ROOT / "docs" / "privacy.md").read_text(encoding="utf-8")
        self.assertIn('ga4_measurement_id: ""', config)
        self.assertIn('javascripts/analytics.js', config)
        self.assertIn('name="happyin-ga4-id"', template)
        self.assertIn("data-ks-analytics-preferences", privacy)


if __name__ == "__main__":
    unittest.main()

"""The Web Analytics beacon must come only from the edge injection.

Measured 2026-09-22 in one browser session: a 404 page, which carries only the injected
beacon, reported with HTTP 204; an article page, which also carried the snippet from the
template, had every report blocked by CORS. Web Analytics therefore saw 404 pages and
almost no readers of articles from April to September 2026.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SingleBeacon(unittest.TestCase):
    def test_templates_do_not_load_the_beacon_themselves(self) -> None:
        for template in (ROOT / "overrides").rglob("*.html"):
            text = template.read_text(encoding="utf-8")
            self.assertNotIn("static.cloudflareinsights.com", text, template.name)


if __name__ == "__main__":
    unittest.main()

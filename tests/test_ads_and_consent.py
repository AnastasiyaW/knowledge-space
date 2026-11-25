"""Template conditions for the Google tag, Consent Mode defaults and AdSense slots.

Renders the real partials with a plain Jinja environment, so the checks fail if a template
starts emitting Google code without configuration, or stops emitting it with one.
"""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path
from types import SimpleNamespace

import jinja2

ROOT = Path(__file__).resolve().parents[1]
CLIENT = "ca-pub-1234567890123456"
SLOTS = {"slot_article_top": "1111111111", "slot_article_end": "2222222222", "slot_sidebar": "3333333333"}


def env() -> jinja2.Environment:
    return jinja2.Environment(loader=jinja2.FileSystemLoader(str(ROOT / "overrides")))


def page(src="kafka/broker-architecture.md", homepage=False, index=False, meta=None):
    return SimpleNamespace(
        is_homepage=homepage, is_index=index, meta=meta or {},
        file=SimpleNamespace(src_uri=src),
    )


def config(ga="", ads=None):
    return {"extra": {"ga4_measurement_id": ga, "ads": ads if ads is not None else {"client": ""}, "ui": {}}}


def render(source: str, **context) -> str:
    return env().from_string(source).render(**context)


SLOT = '{% import "partials/ads.html" as ads with context %}{{ ads.slot(name) }}'
BOOT = '{% include "partials/consent-bootstrap.html" %}'


class ConsentBootstrap(unittest.TestCase):
    def test_nothing_without_configuration(self) -> None:
        html = render(BOOT, config=config(), page=page())
        self.assertNotIn("googletagmanager", html)
        self.assertNotIn("gtag", html)

    def test_one_loader_after_regional_defaults(self) -> None:
        html = render(BOOT, config=config(ga="G-TFT9G5XZ2Q"), page=page())
        self.assertEqual(html.count("googletagmanager.com/gtag/js"), 1)
        defaults = html.index('"consent", "default", regional')
        self.assertLess(defaults, html.index('"consent", "default", all('))
        self.assertLess(defaults, html.index("googletagmanager.com/gtag/js"))
        self.assertIn("regional.region = CONSENT_REGIONS", html)
        self.assertIn('"G-TFT9G5XZ2Q"', html)
        # search.highlight puts search terms in ?h=; every hit must use a query-free address.
        self.assertLess(html.index("page_location: clean(w.location.href)"), html.index('"config"'))

    def test_ads_alone_set_defaults_but_load_no_analytics(self) -> None:
        html = render(BOOT, config=config(ads={"client": CLIENT}), page=page())
        self.assertIn('"consent", "default"', html)
        self.assertNotIn("googletagmanager", html)

    def test_region_list_matches_the_function(self) -> None:
        template = (ROOT / "overrides" / "partials" / "consent-bootstrap.html").read_text(encoding="utf-8")
        function = (ROOT / "functions" / "_consent_regions.js").read_text(encoding="utf-8")
        in_template = json.loads(re.search(r"CONSENT_REGIONS = (\[[^\]]+\])", template).group(1))
        array = re.search(r"CONSENT_REGIONS = \[([^\]]+)\]", function).group(1)
        in_function = re.findall(r'"([A-Z]{2})"', array)
        self.assertEqual(sorted(in_template), sorted(in_function))
        self.assertEqual(len(in_template), 39)  # 27 EU + IS, LI, NO + GB + CH + 7 EU territories with own codes


class AdSlots(unittest.TestCase):
    def slot(self, name, ads, **page_args) -> str:
        return render(SLOT, name=name, config=config(ads=ads), page=page(**page_args)).strip()

    def test_inert_without_client(self) -> None:
        for name in ("article_top", "article_end", "sidebar"):
            self.assertEqual(self.slot(name, {"client": "", **SLOTS}), "")

    def test_inert_without_slot_id(self) -> None:
        self.assertEqual(self.slot("article_end", {"client": CLIENT}), "")

    def test_reserved_height_on_articles(self) -> None:
        html = self.slot("article_end", {"client": CLIENT, **SLOTS})
        self.assertIn('data-ad-client="ca-pub-1234567890123456"', html)
        self.assertIn('data-ad-slot="2222222222"', html)
        self.assertIn("height:280px", html)
        self.assertIn("height:600px", self.slot("sidebar", {"client": CLIENT, **SLOTS}))

    def test_never_on_home_index_or_legal_pages(self) -> None:
        ads = {"client": CLIENT, **SLOTS}
        self.assertEqual(self.slot("article_end", ads, src="index.md", homepage=True), "")
        self.assertEqual(self.slot("article_end", ads, src="kafka/index.md", index=True), "")
        for src in ("privacy.md", "about.md", "contact.md", "start-here.md", "contributing/index.md"):
            self.assertEqual(self.slot("article_end", ads, src=src), "", src)
        self.assertEqual(self.slot("article_end", ads, meta={"ads": False}), "")

    def test_malformed_client_is_ignored(self) -> None:
        self.assertEqual(self.slot("article_end", {"client": "pub-123", **SLOTS}), "")


class SourceDefaults(unittest.TestCase):
    def test_every_language_ships_ads_off(self) -> None:
        for name in ("mkdocs.yml", "mkdocs.ru.yml", "mkdocs.zh-CN.yml"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn('client: !ENV [HAPPYIN_ADSENSE_CLIENT, ""]', text, name)
            self.assertNotRegex(text, r"ca-pub-\d", name)
            self.assertNotIn("G-TFT9G5XZ2Q", text, name)

    def test_no_ads_txt_file_in_source(self) -> None:
        self.assertFalse((ROOT / "docs" / "ads.txt").exists())

    def test_functions_harness(self) -> None:
        completed = subprocess.run(
            ["node", str(ROOT / "tests" / "consent_functions_harness.mjs")],
            check=False, capture_output=True, text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS consent and ads.txt functions", completed.stdout)


if __name__ == "__main__":
    unittest.main()

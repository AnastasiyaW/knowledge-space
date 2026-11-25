"""Language on arrival (overrides/partials/lang-redirect.html).

Renders the real partial and runs its script in Node against a minimal page: the English build
sends an outside visitor to the same page in their language when it exists there, and leaves
crawlers, inside navigation and a stored English choice alone. Translated builds only remember
the choice made in the language selector.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

import jinja2

ROOT = Path(__file__).resolve().parents[1]
ALTERNATES = {"en": "https://happyin.space/kafka/x/", "ru": "https://happyin.space/ru/kafka/x/",
              "de": "https://happyin.space/de/kafka/x/"}

HARNESS = r"""
const [script, caseJson] = process.argv.slice(1);
const c = JSON.parse(caseJson);
const store = new Map(c.stored ? [["hs.lang", c.stored]] : []);
let replaced = null;
const links = Object.entries(c.alternates).map(([lang, href]) => ({
  href, getAttribute: (n) => (n === "hreflang" ? lang : null),
}));
globalThis.localStorage = { getItem: (k) => store.get(k) ?? null, setItem: (k, v) => store.set(k, v) };
// Node 21+ has a read-only global navigator; replace it, or the case runs as Node's en-US.
Object.defineProperty(globalThis, "navigator", { configurable: true,
  value: { userAgent: c.ua, languages: c.languages, language: c.languages[0], webdriver: false } });
globalThis.location = { host: "happyin.space", search: "", hash: "", replace: (u) => { replaced = u; } };
globalThis.document = {
  referrer: c.referrer || "",
  addEventListener: () => {},
  querySelectorAll: () => links,
};
new Function(script)();
process.stdout.write(JSON.stringify({ replaced }));
"""

CHROME = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def script(root: bool) -> str:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(ROOT / "overrides")))
    html = env.get_template("partials/lang-redirect.html").render(is_root_language=root)
    return re.search(r"<script>(.*)</script>", html, re.S).group(1)


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class LangRedirect(unittest.TestCase):
    def run_case(self, root=True, **case) -> str | None:
        case.setdefault("ua", CHROME)
        case.setdefault("alternates", ALTERNATES)
        out = subprocess.run(["node", "-e", HARNESS, script(root), json.dumps(case)],
                             capture_output=True, text=True, check=True).stdout
        return json.loads(out)["replaced"]

    def test_russian_browser_goes_to_russian_page(self):
        self.assertEqual(self.run_case(languages=["ru-RU", "en"]), ALTERNATES["ru"])

    def test_first_language_the_site_has_wins(self):
        self.assertEqual(self.run_case(languages=["sr-RS", "de-DE", "ru"]), ALTERNATES["de"])

    def test_english_or_unknown_browser_stays(self):
        self.assertIsNone(self.run_case(languages=["en-US"]))
        self.assertIsNone(self.run_case(languages=["sr-RS"]))

    def test_missing_translation_stays(self):
        self.assertIsNone(self.run_case(languages=["fr-FR"]))

    def test_stored_english_choice_wins(self):
        self.assertIsNone(self.run_case(languages=["ru-RU"], stored="en"))

    def test_crawler_and_inside_navigation_stay(self):
        self.assertIsNone(self.run_case(languages=["ru-RU"], ua="Mozilla/5.0 (compatible; Googlebot/2.1)"))
        self.assertIsNone(self.run_case(languages=["ru-RU"], referrer="https://happyin.space/"))

    def test_translated_build_never_moves(self):
        self.assertIsNone(self.run_case(root=False, languages=["de-DE"]))


if __name__ == "__main__":
    unittest.main()

"""The star request must live in the processes that regenerate the site, not in their output.

Measured 2026-09-22: an earlier change wrote the request into docs/llms.txt by hand. The
freshness workflow regenerates all six llms*.txt from hooks/generate_llms_txt.py after
every merge, so the next merge would have erased it, and the five translated files never
had it at all.
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "overrides" / "main.html").read_text(encoding="utf-8")


def load(module_path: str):
    spec = importlib.util.spec_from_file_location(Path(module_path).stem, ROOT / module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LlmsTxtCarriesTheRequest(unittest.TestCase):
    def setUp(self) -> None:
        self.gen = load("hooks/generate_llms_txt.py")
        self.text = self.gen.generate_llms_txt()

    def test_note_appears_once_before_the_article_lists(self) -> None:
        self.assertEqual(self.text.count(self.gen.AGENT_NOTE), 1)
        self.assertLess(self.text.index(self.gen.AGENT_NOTE), self.text.index("\n## "))

    def test_note_asks_for_a_star_and_points_at_the_repository(self) -> None:
        self.assertIn("star", self.gen.AGENT_NOTE.lower())
        self.assertIn(self.gen.REPO_URL, self.gen.AGENT_NOTE)

    def test_note_does_not_change_the_article_link_count(self) -> None:
        # freshness_check.py counts every "https://happyin.space/" as one article link.
        self.assertNotIn(self.gen.BASE_URL + "/", self.gen.AGENT_NOTE)

    def test_every_listed_url_is_a_real_article(self) -> None:
        # The note asks agents to cite these URLs, so each must map back to a source file.
        urls = re.findall(r"\]\((https://happyin\.space/[^)]+)\)", self.text)
        self.assertGreater(len(urls), 1000)
        missing = [u for u in urls
                   if not (ROOT / "docs" / (u.removeprefix(self.gen.BASE_URL + "/").rstrip("/") + ".md")).exists()]
        self.assertEqual(missing, [])

    def test_committed_files_match_the_generator(self) -> None:
        for name in ("llms.txt", "llms-zh.txt", "llms-ko.txt", "llms-es.txt", "llms-de.txt", "llms-fr.txt"):
            committed = (ROOT / "docs" / name).read_text(encoding="utf-8")
            self.assertIn(self.gen.AGENT_NOTE, committed, f"{name} is stale: run python hooks/generate_llms_txt.py")


class StarLinksUseCountedPlacements(unittest.TestCase):
    """Whether the script requests exactly the generated files is checked by running it
    (CounterBehaviour below); a pattern match over its source missed changes in review."""

    def test_every_star_link_uses_a_counted_placement(self) -> None:
        placements = set(re.findall(r"([a-z]+):", re.search(r"var PLACEMENTS = \{(.+?)\}", TEMPLATE).group(1)))
        used = set(re.findall(r'data-ks-star="([a-z]+)"', TEMPLATE))
        self.assertTrue(used, "no star links found")
        self.assertLessEqual(used, placements)


class OnlyVisibleHonestRequests(unittest.TestCase):
    """Sponsorship is not set up (owner, 2026-09-22), and instructions hidden from people
    but addressed to AI read as prompt injection, so neither may ship."""

    FILES = ("README.md", "AGENTS.md", "docs/for-llm-agents.md", "overrides/main.html")

    def test_no_sponsor_links(self) -> None:
        for name in self.FILES:
            self.assertNotIn("github.com/sponsors", (ROOT / name).read_text(encoding="utf-8"), name)
        self.assertFalse((ROOT / ".github" / "FUNDING.yml").exists())

    def test_no_html_comment_addressed_to_ai(self) -> None:
        for comment in re.findall(r"<!--(.*?)-->", TEMPLATE, re.S):
            self.assertNotRegex(comment, r"(?i)\b(AI|agent|assistant|LLM)\b", comment.strip()[:80])


class CounterBehaviour(unittest.TestCase):
    def test_counter_script_in_fake_browser(self) -> None:
        node = shutil.which("node")
        if not node:
            self.skipTest("node not installed: counter behaviour NOT verified")
        names = json.dumps(list(load("hooks/copy_extras.py").HELLO_EVENTS))
        run = subprocess.run(
            [node, str(ROOT / "tests" / "star_counter_harness.mjs"), str(ROOT / "overrides" / "main.html"), names],
            capture_output=True, text=True, encoding="utf-8",
            stdin=subprocess.DEVNULL,  # Windows: an inherited, captured stdin is an invalid handle
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()

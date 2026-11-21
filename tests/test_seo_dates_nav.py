"""SEO audit 2026-11-21: every sitemap lastmod was the build day, 37 of 50 sampled descriptions
ended in "...", and each page carried about 1,450 navigation links."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "hooks" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


git_dates = load("git_dates")
description = load("description")


class GitDates(unittest.TestCase):
    def test_newest_commit_is_modified_oldest_is_created(self) -> None:
        log = ("\x002026-11-20\n\ndocs/kafka/a.md\n\n"
               "\x002026-10-01\n\ndocs/kafka/a.md\ndocs/kafka/b.md\n\n"
               "\x002026-09-15\n\ndocs/kafka/a.md\n")
        dates = git_dates.read_history(log)
        self.assertEqual(dates["docs/kafka/a.md"], ("2026-09-15", "2026-11-20"))
        self.assertEqual(dates["docs/kafka/b.md"], ("2026-10-01", "2026-10-01"))


class Descriptions(unittest.TestCase):
    def test_whole_sentences_instead_of_an_ellipsis(self) -> None:
        text = ("Consumer groups let several consumers share the partitions of a topic. "
                "Kafka assigns each partition to exactly one member of the group and rebalances "
                "when a member joins or leaves.")
        self.assertGreater(len(text), description.MAX_LEN)
        self.assertEqual(description._truncate(text),
                         "Consumer groups let several consumers share the partitions of a topic.")

    def test_a_version_number_is_not_a_sentence_end(self) -> None:
        text = "FLUX.2 klein adds a trainer. " + "x" * 200
        self.assertEqual(description._truncate(text), "FLUX.2 klein adds a trainer.")

    def test_a_long_first_sentence_is_still_cut_at_a_word(self) -> None:
        text = "word " * 60
        out = description._truncate(text.strip())
        self.assertTrue(out.endswith("..."))
        self.assertLessEqual(len(out), description.MAX_LEN + 3)


class Navigation(unittest.TestCase):
    def test_every_language_prunes_the_nav_and_dates_pages_from_git(self) -> None:
        for config in ("mkdocs.yml", "mkdocs.ru.yml", "mkdocs.zh-CN.yml", "mkdocs.fr.yml", "mkdocs.de.yml"):
            text = (ROOT / config).read_text(encoding="utf-8")
            self.assertIn("- navigation.prune", text, config)
            self.assertNotIn("- navigation.expand", text, config)
            self.assertNotIn("- navigation.sections", text, config)
            self.assertIn("- hooks/git_dates.py", text, config)

    def test_the_deploy_checkout_has_full_history(self) -> None:
        workflow = (ROOT / ".github/workflows/deploy-cloudflare.yml").read_text(encoding="utf-8")
        self.assertIn("fetch-depth: 0", workflow)


if __name__ == "__main__":
    unittest.main()

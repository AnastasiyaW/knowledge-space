"""Contracts of the article translator: code, anchors, links and structure survive translation."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "hooks"))

import i18n  # noqa: E402
import translate_locales as tl  # noqa: E402

BODY = """# Consumer Groups

Intro with `group.id` and [[offsets-and-commits]].

## Key Facts

- One **leader** per group
- See [docs](https://kafka.apache.org/)

```java
props.put("group.id", "my-group");
```

## Gotchas

| Setting | Default |
|---|---|
| `session.timeout.ms` | 45000 |
"""

TRANSLATED = """# Groupes de consommateurs

Introduction avec `group.id` et [[offsets-and-commits]].

## Points clés

- Un seul **leader** par groupe
- Voir la [documentation](https://kafka.apache.org/)

@@CODE_0@@

## Pièges

| Paramètre | Défaut |
|---|---|
| `session.timeout.ms` | 45000 |
"""


class Translator(unittest.TestCase):
    def test_code_is_restored_and_english_anchors_pinned(self) -> None:
        protected, blocks, slugs = tl.protect(BODY)
        self.assertNotIn("props.put", protected)
        self.assertEqual(slugs, ["consumer-groups", "key-facts", "gotchas"])
        tl.check_structure(protected, TRANSLATED)
        out = tl.restore(TRANSLATED, blocks, slugs, BODY)
        self.assertIn('props.put("group.id", "my-group");', out)
        self.assertIn("## Points clés {#key-facts}", out)
        self.assertIn("## Pièges {#gotchas}", out)

    def test_every_identity_round_trip_of_the_real_articles_is_exact(self) -> None:
        for path in tl.source_files()[:200]:
            _, body = tl.split_front_matter(path.read_text(encoding="utf-8").replace("\r\n", "\n"))
            protected, blocks, slugs = tl.protect(body)
            tl.check_structure(protected, protected)
            tl.restore(protected, blocks, slugs, body)

    def test_damaged_translations_are_refused(self) -> None:
        protected, blocks, slugs = tl.protect(BODY)
        damaged = {
            "unbalanced bold": TRANSLATED.replace("**leader**", "**leader*"),
            "dropped list item": TRANSLATED.replace("- Un seul **leader** par groupe\n", ""),
            "translated inline code": TRANSLATED.replace("`group.id`", "`id.groupe`"),
            "changed wiki link": TRANSLATED.replace("[[offsets-and-commits]]", "[[offsets]]"),
            "changed link target": TRANSLATED.replace("https://kafka.apache.org/", "https://example.org/"),
            "dropped table row": TRANSLATED.replace("| `session.timeout.ms` | 45000 |\n", ""),
        }
        for name, text in damaged.items():
            with self.subTest(name):
                with self.assertRaises(ValueError):
                    tl.check_structure(protected, text)
        with self.assertRaises(ValueError):
            tl.restore(TRANSLATED.replace("@@CODE_0@@", ""), blocks, slugs, BODY)
        with self.assertRaises(ValueError):
            tl.restore(TRANSLATED.replace("## Pièges", "### Pièges"), blocks, slugs, BODY)

    def test_front_matter_is_kept_line_for_line_even_when_it_is_not_valid_yaml(self) -> None:
        source = "---\ntitle: Skin Retouching: Consent\ntags: [a, b]\n---\n"
        translated = "---\ntitle: Retouche : consentement\ntags: [a, b]\n---\n"
        front = tl.build_front_matter(source, translated, "abc", 3)
        self.assertIn('title: "Retouche : consentement"', front)
        self.assertIn("tags: [a, b]", front)
        self.assertIn("source_sha256: abc", front)
        self.assertEqual(tl.fm_value(front, "source_sha256"), "abc")


class CommittedTranslations(unittest.TestCase):
    def test_every_committed_translation_passes_the_current_checks(self) -> None:
        import subprocess
        tracked = set(subprocess.run(["git", "ls-files", "--", "locales"], cwd=ROOT,
                                     capture_output=True, text=True, check=True).stdout.split())
        for lang in sorted({p.split("/")[1] for p in tracked}):
            if lang not in tl.LANGS:
                continue
            with self.subTest(lang):
                self.assertEqual(tl.verify_written(lang, tracked), [])


class LanguageLinks(unittest.TestCase):
    def test_source_files_map_to_directory_urls(self) -> None:
        self.assertEqual(i18n._url("index.md"), "")
        self.assertEqual(i18n._url("kafka/index.md"), "kafka/")
        self.assertEqual(i18n._url("kafka/consumer-groups.md"), "kafka/consumer-groups/")

    def test_link_to_an_untranslated_page_goes_to_the_english_original(self) -> None:
        i18n._pages.clear()
        i18n._pages.update({"en": {"kafka/a.md", "kafka/b.md"}, "fr": {"kafka/a.md"}})
        config = {"extra": {"content_language": "fr", "locales": [
            {"lang": "en", "base": "https://happyin.space/"}, {"lang": "fr", "base": "https://happyin.space/fr/"}]}}
        out = i18n._fallback_links("[x](b.md#top) [y](a.md) [z](https://e.org/c.md)", "kafka/a.md", config)
        self.assertEqual(out, "[x](https://happyin.space/kafka/b/#top) [y](a.md) [z](https://e.org/c.md)")

    def test_wiki_link_to_an_untranslated_page_goes_to_the_english_original(self) -> None:
        import wikilinks
        saved = (wikilinks._english_base, set(wikilinks._english_paths))
        try:
            wikilinks._english_base = "https://happyin.space/"
            wikilinks._english_paths.clear()
            wikilinks._english_paths.update({"algorithms/backtracking.md", "cpp/concurrency.md", "rust/concurrency.md"})
            out = wikilinks._process_markdown("see [[backtracking]] and [[cpp/concurrency]] or [[concurrency]]",
                                              "algorithms/index.md")
            self.assertIn("(https://happyin.space/algorithms/backtracking/)", out)
            self.assertIn("(https://happyin.space/cpp/concurrency/)", out)
            self.assertIn("[[concurrency]]", out)  # ambiguous name stays as written
        finally:
            wikilinks._english_base = saved[0]
            wikilinks._english_paths.clear()
            wikilinks._english_paths.update(saved[1])

    def test_every_language_config_inherits_markdown_and_links_pages(self) -> None:
        for config in sorted(ROOT.glob("mkdocs.*.yml")):
            text = config.read_text(encoding="utf-8")
            with self.subTest(config.name):
                self.assertTrue(text.startswith("INHERIT: mkdocs.yml"))
                self.assertIn("hooks/i18n.py", text)
                self.assertIn("machine_translation_note:", text)


if __name__ == "__main__":
    unittest.main()

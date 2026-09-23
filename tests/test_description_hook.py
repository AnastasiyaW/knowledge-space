"""Meta descriptions: the 2026-09-23 SEO audit found 15 pages whose description attribute
was cut short by a double quote, and hub pages described by a heading or by the site-wide
default. Cases below are the real openings of those pages."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("description", ROOT / "hooks" / "description.py")
description = importlib.util.module_from_spec(spec)
spec.loader.exec_module(description)


def page(src: str, meta: dict | None = None):
    return SimpleNamespace(file=SimpleNamespace(src_path=src), meta=meta or {})


class Extraction(unittest.TestCase):
    def test_a_double_quote_can_no_longer_end_the_attribute(self) -> None:
        md = ('# Backtracking\n\nSystematic exploration of solution space by building candidates '
              'incrementally and abandoning ("backtracking") branches that violate constraints.\n')
        desc = description._extract_first_paragraph(md)
        self.assertNotIn('"', desc)
        self.assertIn("('backtracking')", desc)

    def test_structure_before_the_first_paragraph_is_skipped(self) -> None:
        md = ("# Kafka\n\n## Topics\n\n- [[consumer-groups]] - groups\n\n"
              "Kafka is a distributed log used for event streaming between services.\n")
        self.assertEqual(description._extract_first_paragraph(md),
                         "Kafka is a distributed log used for event streaming between services.")

    def test_pipeline_metadata_is_not_a_description(self) -> None:
        md = ("# Anthropic — Anthropic Development\n\n"
              "**Development line:** `organization:anthropic` · thread `anthropic-development`  \n"
              "**Events:** 9 dated, 2023-03-17 → 2026-08-21 · **Researched:** 2026-09-03 · confidence: medium\n\n"
              "## What it is\n\nAnthropic is an AI safety company that builds the Claude family of models.\n")
        self.assertEqual(description._extract_first_paragraph(md),
                         "Anthropic is an AI safety company that builds the Claude family of models.")

    def test_scope_label_is_dropped_from_the_front(self) -> None:
        md = ("# ATI\n\n**Scope checked: 2026-09-04.** ATI is ByteDance's published trajectory-control "
              "extension for image-to-video generation.\n")
        self.assertTrue(description._extract_first_paragraph(md).startswith("ATI is ByteDance's"))

    def test_a_code_block_is_not_a_paragraph(self) -> None:
        md = "# X\n\n```python\nprint('not a description at all, really')\n```\n\nThe real opening paragraph of the page.\n"
        self.assertEqual(description._extract_first_paragraph(md), "The real opening paragraph of the page.")


class Hook(unittest.TestCase):
    MD = "# Kafka\n\nKafka is a distributed log used for event streaming between services.\n"

    def test_domain_hub_pages_get_their_own_description(self) -> None:
        p = page("kafka/index.md")
        description.on_page_markdown(self.MD, p, {}, None)
        self.assertTrue(p.meta["description"].startswith("Kafka is a distributed log"))

    # The real shape of 13 hubs (as the hook receives it, front matter removed): no prose,
    # only sections of links.
    HUB = ("# Kafka & Message Queues\n\n"
           "## Core Concepts\n- [[broker-architecture]] - Broker cluster\n- [[consumer-groups]] - Group protocol\n\n"
           "## Stream Processing\n- [[kafka-streams]] - KStream/KTable\n\n"
           "## Additional References\n\n- [[admin-api]] - The Admin API\n")

    def test_a_hub_without_prose_is_described_by_its_sections(self) -> None:
        p = page("kafka/index.md")
        description.on_page_markdown(self.HUB, p, {}, None)
        self.assertEqual(p.meta["description"],
                         "Kafka & Message Queues: 4 articles on Core Concepts, Stream Processing.")

    def test_a_long_hub_description_stops_at_a_whole_section(self) -> None:
        sections = "".join(f"## Section number {i}\n- [[a{i}]] - x\n\n" for i in range(20))
        desc = description._hub_description("# Security & Cybersecurity\n\n" + sections)
        self.assertLessEqual(len(desc), description.MAX_LEN)
        self.assertTrue(desc.endswith(", and more."))
        self.assertTrue(desc.startswith("Security & Cybersecurity: 20 articles on Section number 0,"))

    def test_an_article_without_prose_gets_no_hub_description(self) -> None:
        p = page("kafka/cheatsheet.md")
        description.on_page_markdown(self.HUB, p, {}, None)
        self.assertNotIn("description", p.meta)

    def test_home_page_keeps_the_site_description(self) -> None:
        p = page("index.md")
        description.on_page_markdown(self.MD, p, {}, None)
        self.assertNotIn("description", p.meta)

    def test_frontmatter_descriptions_are_made_attribute_safe(self) -> None:
        p = page("kafka/x.md", {"description": 'Uses "exactly once" semantics'})
        description.on_page_markdown(self.MD, p, {}, None)
        self.assertEqual(p.meta["description"], "Uses 'exactly once' semantics")


class OgImage(unittest.TestCase):
    def test_only_domains_with_an_image_file_use_their_own(self) -> None:
        spec_og = importlib.util.spec_from_file_location("og_image", ROOT / "hooks" / "og_image.py")
        og_image = importlib.util.module_from_spec(spec_og)
        spec_og.loader.exec_module(og_image)
        domains = og_image.og_domains(ROOT / "docs")
        self.assertIn("kafka", domains)
        self.assertIn("image-generation", domains)
        self.assertNotIn("image", domains)  # og-image.png is the default, not a domain
        self.assertNotIn("organizations", domains)  # no og-organizations.png: default image
        for d in domains:
            self.assertTrue((ROOT / "docs" / "assets" / f"og-{d}.png").is_file(), d)


class Template(unittest.TestCase):
    TEXT = (ROOT / "overrides" / "main.html").read_text(encoding="utf-8")

    def test_no_hreflang_pointing_at_text_files(self) -> None:
        self.assertNotIn("hreflang=", self.TEXT)

    def test_titles_in_attributes_and_json_ld_are_escaped(self) -> None:
        self.assertNotIn('content="{{ page.title }}', self.TEXT)
        self.assertNotIn('"name": "{{ page.title }}"', self.TEXT)


if __name__ == "__main__":
    unittest.main()

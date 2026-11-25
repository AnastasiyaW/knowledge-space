"""BreadcrumbList JSON-LD. Google requires "item" on every ListItem except the last; MkDocs
sections have no URL, so until 2026-09 level 2 of every article either pointed at the home
page or had no "item" at all. The partial is rendered here with a stand-in nav tree."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import jinja2

ROOT = Path(__file__).resolve().parents[1]
ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(str(ROOT / "overrides")))
SITE = "https://happyin.space/"
CONFIG = {"site_name": "Happyin Knowledge Space", "site_url": SITE}


class Node:
    """Nav item with identity equality, like MkDocs pages and sections."""

    def __init__(self, parent: Node | None = None, **attrs) -> None:
        self.__dict__.update(attrs, parent=parent, children=[])
        if parent:
            parent.children.append(self)

    @property
    def ancestors(self) -> list[Node]:
        out, node = [], self.parent
        while node:
            out.append(node)
            node = node.parent
        return out


def section(title: str, parent: Node | None = None) -> Node:
    return Node(parent, title=title, is_page=False, is_index=False)


def page(title: str, url: str, parent: Node | None = None, index: bool = False) -> Node:
    return Node(parent, title=title, canonical_url=SITE + url, is_page=True, is_index=index)


def trail(p: Node) -> list[dict]:
    html = ENV.get_template("partials/breadcrumb-jsonld.html").render(page=p, config=CONFIG)
    data = json.loads(re.search(r"<script[^>]*>(.*)</script>", html, re.S).group(1))
    items = data["itemListElement"]
    for pos, item in enumerate(items, 1):
        assert item["position"] == pos and item["name"], item
        assert item.get("item"), f"ListItem {pos} has no item: {item}"
    assert len({i["item"] for i in items}) == len(items), f"a URL repeats: {items}"
    return [(i["name"], i["item"]) for i in items]


class Breadcrumbs(unittest.TestCase):
    def setUp(self) -> None:
        self.kafka = section("Kafka")
        self.hub = page("Kafka & Message Queues", "kafka/", self.kafka, index=True)

    def test_an_article_links_to_its_domain_hub(self) -> None:
        article = page("Consumer Groups", "kafka/consumer-groups/", self.kafka)
        self.assertEqual(trail(article), [
            ("Happyin Knowledge Space", SITE),
            ("Kafka & Message Queues", SITE + "kafka/"),
            ("Consumer Groups", SITE + "kafka/consumer-groups/"),
        ])

    def test_the_hub_itself_is_not_listed_twice(self) -> None:
        self.assertEqual(trail(self.hub), [
            ("Happyin Knowledge Space", SITE),
            ("Kafka & Message Queues", SITE + "kafka/"),
        ])

    def test_a_section_without_an_index_page_is_left_out(self) -> None:
        loose = section("Misc")
        article = page("Note", "misc/note/", loose)
        self.assertEqual([name for name, _ in trail(article)], ["Happyin Knowledge Space", "Note"])

    def test_a_page_above_a_page_links_to_itself(self) -> None:
        # Material's blog: a post's parent is the blog index page (children None), which is
        # itself the index page of the Blog section; it must appear once, not twice.
        blog = page("Blog", "blog/", section("Blog"), index=True)
        post = page("CLAUDE.md architecture", "blog/2026/claude-md/", blog)
        blog.children = None
        self.assertEqual([url for _, url in trail(post)], [
            SITE, SITE + "blog/", SITE + "blog/2026/claude-md/",
        ])

    def test_nested_sections_give_one_level_each(self) -> None:
        sub = section("Streams", self.kafka)
        page("Kafka Streams", "kafka/streams/", sub, index=True)
        article = page("Windowing", "kafka/streams/windowing/", sub)
        self.assertEqual([url for _, url in trail(article)], [
            SITE, SITE + "kafka/", SITE + "kafka/streams/", SITE + "kafka/streams/windowing/",
        ])


if __name__ == "__main__":
    unittest.main()

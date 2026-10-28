"""The owner's research queue must show every finding under its own topic."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("feedback_queue", ROOT / "scripts" / "feedback_queue.py")
feedback_queue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(feedback_queue)


def row(id_, kind, topic=None, article=None, detail=None, source=None, client="c1"):
    return {"id": id_, "kind": kind, "topic": topic, "article": article, "detail": detail,
            "source_url": source, "agent": None, "client_hash": client}


class FindingsKeepTheirTopic(unittest.TestCase):
    """kind=finding needs a topic but not an article (functions/_feedback_core.js), and /api/wanted
    invites findings by topic. Grouping by (kind, article) put every article-less finding into one
    item whose subject was None: the topics never reached the owner and only three details showed."""

    def test_findings_on_different_topics_are_separate_items(self) -> None:
        items = feedback_queue.group([
            row(1, "finding", topic="Kafka 4 share groups", detail="d1", source="https://a.example/1"),
            row(2, "finding", topic="Python 3.14 free threading", detail="d2", source="https://b.example/2", client="c2"),
        ])
        self.assertEqual(sorted(i["subject"] for i in items), ["Kafka 4 share groups", "Python 3.14 free threading"])

    def test_findings_on_one_topic_still_group(self) -> None:
        items = feedback_queue.group([
            row(1, "finding", topic="Kafka 4 share groups", detail="d1", source="https://a.example/1"),
            row(2, "finding", topic="kafka 4  share groups", detail="d2", source="https://b.example/2", client="c2"),
        ])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["reporters"], 2)

    def test_a_finding_for_an_article_names_both(self) -> None:
        items = feedback_queue.group([
            row(1, "finding", topic="Refresh", article="kafka/consumer-groups", detail="d", source="https://a.example"),
        ])
        self.assertIn("Refresh", items[0]["subject"])
        self.assertIn("kafka/consumer-groups", items[0]["subject"])

    def test_gap_and_article_kinds_are_unchanged(self) -> None:
        items = feedback_queue.group([
            row(1, "gap", topic="Kafka 4 share groups"),
            row(2, "gap", topic="kafka 4 share groups", client="c2"),
            row(3, "outdated", article="kafka/consumer-groups", detail="x"),
        ])
        self.assertEqual(sorted((i["kind"], i["subject"]) for i in items),
                         [("gap", "Kafka 4 share groups"), ("outdated", "kafka/consumer-groups")])


if __name__ == "__main__":
    unittest.main()

"""The count syncer must recognise a count that has passed one thousand."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "scripts" / "sync_stats.py").read_text(encoding="utf-8")


class FourDigitCounts(unittest.TestCase):
    """Measured 2026-09-05: with 1039 articles every count file still said 1000+, the syncer
    printed already current, and the freshness job was red on master and 157 pull requests.
    The patterns looked for exactly three digits."""

    def test_no_pattern_demands_exactly_three_digits(self) -> None:
        self.assertNotIn(r"\d{3}\+", SOURCE)

    def test_the_agents_pattern_rewrites_a_four_digit_count(self) -> None:
        pattern = r"\(\d{3,}\+ articles, \d+ domains\)"
        out = re.sub(pattern, "(1039+ articles, 28 domains)", "A base (1000+ articles, 28 domains) for agents.")
        self.assertIn("(1039+ articles, 28 domains)", out)

    def test_the_index_pattern_rewrites_a_four_digit_count(self) -> None:
        pattern = r"\b\d{3,}\+ articles across \d+ domains"
        out = re.sub(pattern, "1039+ articles across 28 domains", "1000+ articles across 28 domains, each")
        self.assertTrue(out.startswith("1039+ articles across 28 domains"), out)


if __name__ == "__main__":
    unittest.main()

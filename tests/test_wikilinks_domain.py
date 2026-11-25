"""[[domain/slug]] must resolve inside that domain, and a shared bare name must not guess."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "hooks"))

import wikilinks  # noqa: E402

LINK = re.compile(r"\[\[([^\]]+)\]\]")


def base(tmp: str) -> Path:
    """Three domains, one shared page name, one unique page."""
    docs = Path(tmp) / "docs"
    for domain in ("cpp", "python", "rust"):
        (docs / domain).mkdir(parents=True)
        (docs / domain / "concurrency.md").write_text("# " + domain, encoding="utf-8")
    (docs / "projects").mkdir(parents=True)
    (docs / "projects" / "vidu.md").write_text("# Vidu", encoding="utf-8")
    return docs


def render(docs: Path, page: str, text: str) -> str:
    wikilinks._built = False
    wikilinks._slug_map.clear()
    wikilinks._path_map.clear()
    wikilinks._seen_domains.clear()
    wikilinks._ambiguous.clear()
    wikilinks._build_slug_map(docs)
    return LINK.sub(wikilinks._make_replacer(page), text)


class QualifiedLinks(unittest.TestCase):
    """Measured by review 2026-09-05: all three concurrency links resolved to the Rust page,
    because the resolver dropped the domain and looked the basename up globally."""

    def test_each_domain_gets_its_own_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = base(tmp)
            self.assertIn("python/concurrency.md", render(docs, "cpp/threads.md", "[[python/concurrency]]"))
            self.assertIn("rust/concurrency.md", render(docs, "cpp/threads.md", "[[rust/concurrency]]"))
            out = render(docs, "cpp/threads.md", "[[cpp/concurrency]]")
            self.assertIn("concurrency.md", out)
            self.assertNotIn("rust/", out)

    def test_a_bare_name_several_domains_answer_to_is_left_alone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = base(tmp)
            self.assertEqual(render(docs, "cpp/threads.md", "[[concurrency]]"), "[[concurrency]]")

    def test_an_unambiguous_bare_name_still_resolves(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = base(tmp)
            self.assertIn("projects/vidu.md", render(docs, "cpp/threads.md", "[[vidu]]"))

    def test_a_domain_no_page_answers_to_is_left_alone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = base(tmp)
            self.assertEqual(render(docs, "cpp/threads.md", "[[nowhere/concurrency]]"),
                             "[[nowhere/concurrency]]")


if __name__ == "__main__":
    unittest.main()

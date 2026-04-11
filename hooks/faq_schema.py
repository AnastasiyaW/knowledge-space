"""
MkDocs hook: inject FAQPage JSON-LD from Gotchas sections.

Parses the Gotchas section of each article and generates a FAQPage
schema.org structured data block. Google can display these as rich
snippets in search results.

Expected format in articles:
## Gotchas
- **Issue:** some problem -> **Fix:** the solution
- **Issue:** another problem -> **Fix:** another solution
"""

import json
import re


def _extract_gotchas(markdown: str) -> list[dict]:
    """Extract Q&A pairs from ## Gotchas section."""
    # Find Gotchas section
    gotchas_match = re.search(
        r'^## Gotchas\s*\n(.*?)(?=^## |\Z)',
        markdown,
        re.MULTILINE | re.DOTALL,
    )
    if not gotchas_match:
        return []

    section = gotchas_match.group(1)
    pairs = []

    # Pattern: **Issue:** X -> **Fix:** Y
    # or: **X** -> Y (simpler format)
    for m in re.finditer(
        r'\*\*(?:Issue:\s*)?(.+?)\*\*\s*(?:->|→|:)\s*(?:\*\*Fix:\s*\*\*)?\s*(.+?)(?=\n-|\n\n|\Z)',
        section,
    ):
        question = m.group(1).strip().rstrip(".")
        answer = m.group(2).strip()
        # Clean up markdown formatting
        question = re.sub(r'[`*]', '', question).strip()
        answer = re.sub(r'[`*]', '', answer).strip()
        if len(question) > 10 and len(answer) > 10:
            pairs.append({"question": question, "answer": answer})

    return pairs[:10]  # max 10 FAQ items per page


def on_page_context(context, page, config, **kwargs):
    """Inject FAQ schema into page context for template use."""
    if not page.markdown:
        return context

    gotchas = _extract_gotchas(page.markdown)
    if gotchas:
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": g["question"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": g["answer"],
                    },
                }
                for g in gotchas
            ],
        }
        # Store as page meta for template to pick up
        if not hasattr(page, "meta") or page.meta is None:
            page.meta = {}
        page.meta["_faq_schema"] = json.dumps(faq_schema, ensure_ascii=False)

    return context

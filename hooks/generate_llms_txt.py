"""
Generate llms.txt and multilingual variants from docs/ articles.
Reads each article's H1 and first paragraph as description.

Usage:
    python hooks/generate_llms_txt.py
    python hooks/generate_llms_txt.py --dry-run  # print without writing
"""

import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

EXCLUDE_FILES = {"index.md", "for-llm-agents.md", "privacy.md", "CNAME"}
EXCLUDE_DIRS = {"blog", "contributing", "javascripts", "stylesheets", "assets", "knowledge-base"}

# Domain display names (must match stats.py)
DOMAIN_NAMES = {
    "algorithms": "Algorithms & Data Structures",
    "architecture": "Architecture & Design",
    "audio-voice": "Voice & Audio",
    "bi-analytics": "BI & Analytics",
    "cpp": "C++",
    "data-engineering": "Data Engineering",
    "data-science": "Data Science",
    "devops": "DevOps",
    "go": "Go",
    "image-generation": "Image Generation",
    "ios-mobile": "iOS & Mobile",
    "java-spring": "Java & Spring",
    "kafka": "Kafka",
    "linux-cli": "Linux CLI",
    "llm-agents": "LLM & Agents",
    "llm-memory": "LLM Memory",
    "misc": "Misc",
    "nodejs": "Node.js",
    "php": "PHP",
    "python": "Python",
    "rust": "Rust",
    "security": "Security",
    "seo-marketing": "SEO & Marketing",
    "sql-databases": "SQL & Databases",
    "testing-qa": "Testing & QA",
    "web-frontend": "Web Frontend",
    "writing": "Natural Language & Writing",
}

BASE_URL = "https://happyin.space"


def extract_article_info(path: Path) -> tuple[str, str]:
    """Extract H1 title and first paragraph from article."""
    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.split("\n")

    # Find H1
    title = path.stem.replace("-", " ").title()
    for line in lines:
        if line.startswith("# ") and not line.startswith("##"):
            title = line[2:].strip()
            break

    # Find first non-empty paragraph after H1
    desc = ""
    found_h1 = False
    for line in lines:
        if line.startswith("# ") and not line.startswith("##"):
            found_h1 = True
            continue
        if found_h1 and line.strip() and not line.startswith("#") and not line.startswith("---"):
            # Skip frontmatter, empty lines, and headers
            if line.strip().startswith("```") or line.strip().startswith("|") or line.strip().startswith("-"):
                continue
            desc = line.strip()
            break

    # Truncate description
    if len(desc) > 200:
        desc = desc[:197] + "..."

    return title, desc


def generate_llms_txt() -> str:
    """Generate llms.txt content."""
    articles_by_domain = {}

    for d in sorted(DOCS_DIR.iterdir()):
        if not d.is_dir() or d.name in EXCLUDE_DIRS:
            continue
        domain_articles = []
        for f in sorted(d.rglob("*.md")):
            if f.name in EXCLUDE_FILES:
                continue
            title, desc = extract_article_info(f)
            slug = f.stem
            domain = d.name
            url = f"{BASE_URL}/{domain}/{slug}/"
            domain_articles.append((title, url, desc))
        if domain_articles:
            articles_by_domain[d.name] = domain_articles

    total = sum(len(v) for v in articles_by_domain.values())
    domains = len(articles_by_domain)

    lines = [
        "# Happyin Knowledge Space",
        "",
        f"> A comprehensive technical knowledge base with {total}+ curated articles across {domains} domains. "
        "Covers software engineering, data science, DevOps, security, and more. "
        "Designed for software engineers and LLM agents seeking reliable, structured technical reference material. "
        "All articles are in English.",
        "",
        "This knowledge base contains deep technical articles organized by domain. "
        "Each article follows a consistent structure: definition, key concepts, code examples, gotchas, and related links.",
        "",
    ]

    for domain in sorted(articles_by_domain.keys()):
        display_name = DOMAIN_NAMES.get(domain, domain.replace("-", " ").title())
        lines.append(f"## {display_name}")
        for title, url, desc in articles_by_domain[domain]:
            if desc:
                lines.append(f"- [{title}]({url}): {desc}")
            else:
                lines.append(f"- [{title}]({url})")
        lines.append("")

    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    content = generate_llms_txt()

    if dry_run:
        print(content)
        return

    # Write EN version
    (DOCS_DIR / "llms.txt").write_text(content, encoding="utf-8")
    print(f"Generated llms.txt")

    # Write multilingual variants (same content, different header language)
    langs = {
        "zh": "综合技术知识库",
        "ko": "종합 기술 지식 베이스",
        "es": "Base de conocimientos técnicos integral",
        "de": "Umfassende technische Wissensbasis",
        "fr": "Base de connaissances techniques complète",
    }

    for lang, header in langs.items():
        lang_content = content.replace("# Happyin Knowledge Space", f"# {header} - Happyin Knowledge Space")
        (DOCS_DIR / f"llms-{lang}.txt").write_text(lang_content, encoding="utf-8")
        print(f"Generated llms-{lang}.txt")

    # Count articles
    url_count = content.count(f"{BASE_URL}/")
    print(f"\nTotal: {url_count} article URLs")


if __name__ == "__main__":
    main()

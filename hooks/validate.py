"""
MkDocs hook: validate articles before build.
Catches common issues: broken code blocks, forbidden content, format problems.
Runs automatically on every build (mkdocs build / mkdocs serve).
"""

import re
import sys
from pathlib import Path

# Forbidden patterns (course names, instructor names, platform names)
FORBIDDEN_PATTERNS = [
    r'\b(Udemy|Coursera|Stepik|OTUS|Geekbrains|Skillbox)\b',
    r'\b(Karpov\.Courses|Karpov courses)\b',
    r'\b(instructor|преподаватель|курс |лекция)\b',
]

# Compile for performance
FORBIDDEN_RE = [re.compile(p, re.IGNORECASE) for p in FORBIDDEN_PATTERNS]

# Valid domain folders
VALID_DOMAINS = {
    "algorithms", "architecture", "bi-analytics", "data-engineering",
    "data-science", "devops", "image-generation", "ios-mobile",
    "java-spring", "kafka", "linux-cli", "llm-agents", "misc",
    "nodejs", "php", "python", "rust", "security", "seo-marketing",
    "sql-databases", "testing-qa", "web-frontend",
}


def validate_article(path: Path, content: str) -> list[str]:
    """Validate a single article. Returns list of warnings."""
    warnings = []
    lines = content.split("\n")
    rel = path.as_posix()

    # Check: has H1 title
    has_h1 = any(line.startswith("# ") and not line.startswith("##") for line in lines)
    if not has_h1:
        warnings.append(f"  WARN: {rel} - missing H1 title")

    # Check: not too long (>500 lines)
    if len(lines) > 500:
        warnings.append(f"  WARN: {rel} - {len(lines)} lines (max 500, consider splitting)")

    # Check: unclosed code blocks
    fence_count = sum(1 for line in lines if line.strip().startswith("```"))
    if fence_count % 2 != 0:
        warnings.append(f"  ERROR: {rel} - unclosed code block ({fence_count} fences)")

    # Check: code blocks without language tags
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "```":
            # Could be a closing fence or an opening fence without language
            # Check if previous non-empty line is also ``` (meaning this closes)
            # Simple heuristic: if this is opening (no content before next ```)
            if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].strip().startswith("```"):
                warnings.append(f"  WARN: {rel}:{i+1} - code block without language tag")

    # Check: forbidden content
    for pattern in FORBIDDEN_RE:
        for i, line in enumerate(lines):
            match = pattern.search(line)
            if match:
                warnings.append(
                    f"  ERROR: {rel}:{i+1} - forbidden content: '{match.group()}'"
                )

    return warnings


def on_pre_build(config, **kwargs):
    """Validate all articles before MkDocs builds the site."""
    docs_dir = Path(config["docs_dir"])
    all_warnings = []
    errors = 0
    checked = 0

    for domain in VALID_DOMAINS:
        domain_path = docs_dir / domain
        if not domain_path.is_dir():
            continue

        for md_file in domain_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue

            checked += 1
            content = md_file.read_text(encoding="utf-8", errors="replace")
            rel_path = md_file.relative_to(docs_dir)
            warnings = validate_article(rel_path, content)

            if warnings:
                all_warnings.extend(warnings)
                errors += sum(1 for w in warnings if "ERROR" in w)

    if all_warnings:
        print(f"[validate] {checked} articles checked, {len(all_warnings)} issues found:")
        for w in all_warnings[:20]:  # Show first 20
            print(w)
        if len(all_warnings) > 20:
            print(f"  ... and {len(all_warnings) - 20} more")
    else:
        print(f"[validate] {checked} articles checked, all clean")

    # Don't fail the build on warnings, only on errors in CI
    if errors > 0 and "CI" in (config.get("extra", {}) or {}):
        sys.exit(1)

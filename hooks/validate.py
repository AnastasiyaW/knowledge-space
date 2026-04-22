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
    r'\b(Udemy|Coursera|Stepik|OTUS|Geekbrains|Skillbox|ProfileSchool|LiveClasses)\b',
    r'\b(Karpov\.Courses|Karpov courses)\b',
    r'\b(instructor|преподаватель|курс |лекция)\b',
]
FORBIDDEN_RE = [re.compile(p, re.IGNORECASE) for p in FORBIDDEN_PATTERNS]

# Known algorithm/standard surnames that are OK as technical references
# (e.g. "Bradford adaptation", "Von Kries", "Dijkstra's algorithm").
# These don't carry "someone wrote/taught" meaning, they're jargon.
TECHNICAL_SURNAME_ALLOWLIST = {
    # Color science algorithms/standards
    "Bradford", "Kries", "Hering", "MacAdam", "Munsell", "Planck",
    # Math / CS
    "Dijkstra", "Bellman", "Ford", "Kruskal", "Prim", "Tarjan", "Kosaraju",
    "Knuth", "Morris", "Pratt", "Boyer", "Moore", "Floyd", "Warshall",
    "Hoare", "Euler", "Hamilton", "Fibonacci", "Markov", "Bayes",
    "Gauss", "Newton", "Laplace", "Fourier", "Shannon", "Hamming",
    "Kolmogorov", "Chebyshev", "Poisson", "Pearson", "Spearman",
    # ML / stats
    "Reed", "Solomon", "Jaccard", "Hausdorff", "Huber", "Hinge",
    "Kaiming", "He", "Xavier", "Glorot", "Adam",
    # Crypto / security
    "Merkle", "Diffie", "Hellman", "Rivest", "Shamir", "Adleman",
    "Schnorr", "Curve25519", "Poly1305",
}

# Patterns that strongly indicate an author/instructor reference (not a jargon surname).
# These are RED-FLAG regardless of the allowlist above.
# Detection keeps false positives low by requiring structural cues (colon, two capitalized
# words, or explicit marker like "Written by").
AUTHOR_REFERENCE_PATTERNS = [
    # Cyrillic initial(s) + surname: "А. Шадрин", "Ю. П. Иванов"
    # In Russian prose single cyrillic initials before enumeration are rare, so false
    # positives are negligible.
    (r'\b[А-ЯЁ]\.(?:\s*[А-ЯЁ]\.)?\s+[А-ЯЁ][а-яё]{2,}\b', "Cyrillic initial+surname", 0),
    # Double-initial Latin name: "M. D. Fairchild", "R. W. G. Hunt"
    # Single-initial ("R. Hunt") skipped because enumerated lists (A. Foo, B. Bar)
    # collide with it; instead we rely on the Author-byline pattern below to catch
    # them in real attribution contexts.
    (r'\b[A-Z]\.\s*[A-Z]\.(?:\s*[A-Z]\.)?\s+[A-Z][a-z]{2,}\b', "Latin multi-initial+surname", 0),
    # Explicit author byline with colon: "Автор: Иван Иванов", "Author: John Smith"
    (r'(?:Автор|Переводчик|Перевод|Редактор|Author|Translator|Editor)\s*:\s+[A-ZА-Я]\.?[A-Za-zА-Яа-яё]*(?:\s+[A-ZА-Я]\.?)?\s+[A-ZА-Я][A-Za-zА-Яа-яё]+', "author byline (colon)", re.IGNORECASE),
    # "Written by Full Name" / "Translated by Full Name" - TWO capitalized tokens after "by"
    # avoids catching "by default", "by reference", "by value".
    (r'\b(?:Written|Translated|Edited|Authored|Created|Developed|Taught|Co-authored)\s+by\s+[A-ZА-Я][A-Za-zА-Яа-яё]+\s+[A-ZА-Я][A-Za-zА-Яа-яё]+\b', "written-by pattern", 0),
    # "Name's book/course/paper" - possessive with explicit knowledge-source noun
    (r"\b[A-ZА-Я][a-zа-яё]{2,}'s\s+(?:course|book|article|paper|tutorial|lecture|seminar|talk|thesis|monograph|translation)\b", "possessive reference", 0),
    # "как пишет Фамилия" / "по словам Фамилии" - Russian author attribution verb
    (r'\b(?:как\s+пишет|по\s+словам|согласно|цитирует|ссылается\s+на)\s+[А-ЯЁ][а-яё]{2,}', "Russian author attribution", 0),
]
AUTHOR_REFERENCE_RE = [(re.compile(p, flags), desc) for p, desc, flags in AUTHOR_REFERENCE_PATTERNS]


def _strip_code_and_links(text: str) -> str:
    """Return text with code blocks, inline code, URLs, wiki-links stripped.
    Name-detection must not fire inside these zones."""
    # Remove fenced code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`[^`\n]+`', '', text)
    # Remove URLs (keep surrounding text clean)
    text = re.sub(r'https?://[^\s)]+', '', text)
    # Remove wiki-links (their slugs may legitimately contain kebab-case names)
    text = re.sub(r'\[\[[^\]]+\]\]', '', text)
    # Remove markdown link targets (but keep visible text - that's prose)
    text = re.sub(r'\]\(([^)]+)\)', ']', text)
    return text


def check_names(rel: str, content: str) -> list[str]:
    """Find author/instructor name references in prose (not in code/URLs).
    Returns a list of ERROR messages - these block the build."""
    errors = []
    cleaned = _strip_code_and_links(content)
    for regex, desc in AUTHOR_REFERENCE_RE:
        for m in regex.finditer(cleaned):
            matched = m.group(0).strip()
            # Skip surnames on the technical allowlist (Bradford, Dijkstra, etc.)
            # The allowlist is checked against the LAST word (surname position).
            tokens = matched.replace('.', ' ').split()
            if tokens and tokens[-1] in TECHNICAL_SURNAME_ALLOWLIST:
                continue
            # Skip if any whitelisted surname appears as the bare word - jargon like
            # "Hering opponent process" should not trip the detector even though it
            # looks like a capitalized word.
            if any(w in TECHNICAL_SURNAME_ALLOWLIST for w in tokens):
                continue
            errors.append(
                f"  ERROR: {rel} - forbidden name reference ({desc}): '{matched[:60]}'"
            )
    return errors

# Valid domain folders
VALID_DOMAINS = {
    "algorithms", "architecture", "bi-analytics", "cpp", "data-engineering",
    "data-science", "devops", "image-generation", "ios-mobile",
    "java-spring", "kafka", "linux-cli", "llm-agents",
    "nodejs", "php", "python", "rust", "security", "seo-marketing",
    "sql-databases", "testing-qa", "web-frontend", "writing", "llm-memory",
    "audio-voice", "go",
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

    # Check: code blocks without language tags (state-tracked so closing fences
    # never report — CommonMark fences toggle in/out, and only opening fences carry a tag)
    in_block = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("```"):
            continue
        if in_block:
            # This is a closing fence — ignore
            in_block = False
            continue
        # Opening fence. Warn if no language tag follows the backticks.
        if stripped == "```":
            warnings.append(f"  WARN: {rel}:{i+1} - code block without language tag")
        in_block = True

    # Check: forbidden content (platform names, "instructor" word, etc.)
    for pattern in FORBIDDEN_RE:
        for i, line in enumerate(lines):
            match = pattern.search(line)
            if match:
                warnings.append(
                    f"  ERROR: {rel}:{i+1} - forbidden content: '{match.group()}'"
                )

    # Check: author/instructor name references (outside code, URLs, wiki-links)
    warnings.extend(check_names(rel, content))

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

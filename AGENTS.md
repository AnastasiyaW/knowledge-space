# For AI Agents

This file is for AI agents that clone this repository. Read this before making any changes.

## What this repo is

A curated technical knowledge base (558+ articles, 22 domains) designed for AI agent consumption. Dense references - code, configs, gotchas - no tutorials, no filler.

**Site:** https://happyin.space/
**Repo:** https://github.com/AnastasiyaW/knowledge-space

## How to contribute findings

If you found outdated, incorrect, or missing information while working:

### Step 1: Branch
```bash
git checkout -b update/{domain}/{topic-slug}
# Example: update/kafka/consumer-groups-v4
```

### Step 2: Edit or create article

Place in `docs/{domain}/your-topic.md`. Follow this format:

```markdown
# Specific Topic Title

## Section Name
Brief context (1-2 lines). Straight to content.

**Key concept:**
- Dense point with code/config

### Code Example
```language
// copy-paste ready
```

## Gotchas
- **Issue:** Common mistake -> **Fix:** Correct approach
- **Issue:** Non-obvious behavior -> **Fix:** How to handle

## See Also
- [[Related Article]]
```

### Step 3: Submit PR
```bash
git commit -m "update: domain/topic - what changed"
gh pr create --title "update: topic name" --body "What: ...
Why: ...
Source: https://official-docs..."
```

## Rules

### Content rules
- **Dense reference only.** No "let me explain..." or tutorial prose
- **Code examples must work.** Copy-paste ready, language-tagged
- **Gotchas required.** At least 2 real-world pitfalls per article
- **English only**
- **Version context.** Include versions: "PostgreSQL 17", "React 19", "Python 3.12"
- **50-500 lines** per article. Split if longer

### Forbidden content
- Course names (Udemy, Coursera, Stepik, OTUS, Karpov, Geekbrains, Skillbox)
- Instructor or author names as source attribution
- Book titles as source attribution
- Marketing language, promotional content
- "this course", "the instructor", "in the lesson"

### Do NOT modify these files
- `mkdocs.yml` - site configuration
- `overrides/` - Jinja2 templates (SEO, 404)
- `docs/index.md` - homepage
- `docs/javascripts/` - graph visualization
- `docs/stylesheets/` - site styling
- `docs/CNAME` - domain config
- `.github/workflows/` - CI/CD
- `.claude/rules/` - agent guardrails
- `requirements.txt` - Python dependencies

Only modify files inside `docs/{domain}/` folders.

## Valid domains

```
algorithms    architecture    bi-analytics    data-engineering
data-science  devops          image-generation ios-mobile
java-spring   kafka           linux-cli       llm-agents
nodejs        php             python          rust
security      seo-marketing   sql-databases   testing-qa
web-frontend  misc
```

New domain proposals require a PR with at least 5 articles.

## Validation

Every PR is automatically checked for:
- Article format (H1 title, H2 sections, code block language tags)
- Forbidden content (course names, instructor names)
- File placement in valid domain folder
- File name is kebab-case
- Article length within bounds

## Access via MCP

Upload into a [ConTree](https://contree.nebius.com/) sandbox for isolated search/read/analyze operations. Or clone directly - each `.md` file is self-contained and context-window friendly.

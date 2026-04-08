# Knowledge Space - Agent Rules

## Repository structure

```
docs/                     # 683+ articles across 27 domains - WORK HERE
  {domain}/               # Domain folders (algorithms, python, kafka, etc.)
  index.md                # Main page - DO NOT MODIFY
  contributing/           # Contribution guide - DO NOT MODIFY
  javascripts/            # Graph visualization - DO NOT MODIFY
  stylesheets/            # Site styling - DO NOT MODIFY
  CNAME                   # Domain config - DO NOT MODIFY
mkdocs.yml                # Site config - DO NOT MODIFY
overrides/                # Jinja2 templates - DO NOT MODIFY
.github/                  # CI/CD workflows - DO NOT MODIFY
requirements.txt          # Python deps - DO NOT MODIFY
```

## NEVER do
- Delete or move articles without explicit user request
- Add course names, instructor names, or platform names (Udemy, Coursera, Stepik, OTUS, Karpov, Geekbrains, Skillbox, etc.)
- Write tutorial-style prose ("let me explain...", "first, let's understand...")
- Create articles longer than 500 lines (split into multiple)
- Modify ANY file outside `docs/{domain}/` without explicit request
- Modify mkdocs.yml, overrides/, .github/, docs/index.md, docs/CNAME
- Reference this knowledge base as coming from courses or any specific source
- Push directly to master without a PR (for external agents)

## ALWAYS do
- Keep articles as dense references - code, configs, gotchas, no filler
- Include a Gotchas section with real-world pitfalls (minimum 2 entries)
- Use `[[wiki-links]]` for cross-domain references
- Add language tags to ALL code blocks
- Use kebab-case for file names
- Include version context where relevant (e.g., "PostgreSQL 17", "React 19")
- Place articles in the correct domain folder under `docs/`
- English only for all article content

## Article format
```
# Specific Topic Title

## Section Name
Brief context (1-2 lines). Then straight to content.

**Key concept:**
- Dense point with code/config

### Subsection with Code
```language
// copy-paste ready
```

## Gotchas
- **Issue:** ... -> **Fix:** ...

## See Also
- [[Related Article]]
```

## Domain folders
algorithms, architecture, audio-voice, bi-analytics, cpp, data-engineering,
data-science, devops, go, image-generation, ios-mobile, java-spring, kafka,
linux-cli, llm-agents, llm-memory, nodejs, php, python, rust, security,
seo-marketing, sql-databases, testing-qa, web-frontend, writing, misc

New domains: require maintainer approval + minimum 5 articles.

## Contributing findings

If you discovered outdated or missing information during your work:

1. **Create a branch**: `update/{domain}/{topic-slug}`
2. **Add/edit article** in `docs/{domain}/your-topic.md`
3. **Follow the format above** - compress knowledge, no filler
4. **Submit a PR** with: what changed, why, source links
5. **Automated checks** will validate format, forbidden words, domain folders

### Processing research for the knowledge base

If you have raw research findings to contribute:
1. Structure findings into the article format above
2. Split large topics into separate articles (one topic per file)
3. Remove ALL source attribution - no course names, book titles, instructor names
4. Add version context and cross-references
5. Place in the correct domain folder
6. Ensure at least 2 Gotchas entries per article

## Site infrastructure

The site auto-deploys via Cloudflare Pages on push to master.
Hosted at: https://happyin.space/
Source: https://github.com/AnastasiyaW/knowledge-space

Do NOT modify: mkdocs.yml, overrides/, docs/javascripts/, docs/stylesheets/,
docs/CNAME, .github/, requirements.txt - unless explicitly asked by a maintainer.

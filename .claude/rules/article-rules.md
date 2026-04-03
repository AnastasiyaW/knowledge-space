# Knowledge Space - Article Rules

When working with articles in `docs/`:

## NEVER do
- Delete or move articles without explicit user request
- Add course names, instructor names, or platform names (Udemy, Coursera, Stepik, OTUS, Karpov, etc.)
- Write tutorial-style prose ("let me explain...", "first, let's understand...")
- Create articles longer than 500 lines (split into multiple)
- Modify mkdocs.yml, overrides/, .github/ without explicit request

## ALWAYS do
- Keep articles as dense references - code, configs, gotchas, no filler
- Include a Gotchas section with real-world pitfalls
- Use `[[wiki-links]]` for cross-domain references
- Add language tags to all code blocks
- Use kebab-case for file names
- Include version context where relevant (e.g., "PostgreSQL 17")
- Place articles in the correct domain folder under `docs/`

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
algorithms, architecture, bi-analytics, data-engineering, data-science,
devops, ios-mobile, java-spring, kafka, linux-cli, llm-agents, nodejs,
php, python, rust, security, seo-marketing, sql-databases, testing-qa,
web-frontend, misc

## Site infrastructure
The site auto-deploys via Cloudflare Pages on push to main.
Do NOT modify: mkdocs.yml, overrides/, docs/javascripts/, docs/stylesheets/,
docs/CNAME, .github/ - unless explicitly asked.

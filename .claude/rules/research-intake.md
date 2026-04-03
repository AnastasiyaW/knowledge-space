# Research Intake - Processing Raw Research into Articles

## When this applies

When you are asked to update the knowledge base, or when raw research files
need to be converted into publishable articles.

## Source locations

Raw research findings arrive in:
`C:\Users\black\Desktop\CODE_Claude\skill-generator\state\incoming-research\`

Compressed topic summaries live in:
`C:\Users\black\Desktop\CODE_Claude\skill-generator\state\compressed\{topic}\`

## Processing workflow

1. **Read** the raw research or compressed file
2. **Identify** which domain folder(s) the content belongs to
3. **Check** if an article already exists on this topic in `docs/{domain}/`
   - If exists: UPDATE the existing article with new information
   - If not: CREATE a new article
4. **Transform** into article format:
   - Strip ALL source attribution (course names, instructors, book titles)
   - Translate RU -> EN if needed (articles are English-only)
   - Compress into dense reference format
   - Add code examples (copy-paste ready, language-tagged)
   - Add Gotchas section (minimum 2 entries)
   - Add `[[wiki-links]]` to related articles
   - Add version context where relevant
5. **Place** in `docs/{domain}/topic-slug.md`
6. **Verify** article passes validation (50-500 lines, has H1, H2, code tags)

## Quality requirements

- One topic per article, max 500 lines
- No tutorial prose - dense reference only
- All code blocks have language tags
- Gotchas are real pitfalls, not generic warnings
- Cross-references use `[[wiki-links]]`
- File name is kebab-case

## After processing

- Mark the intake entry as DONE in `_intake.md`
- Do NOT delete the source files (they serve as dedup reference)

## Domain mapping hints

| Research topic | Target domain |
|---------------|---------------|
| ML, neural nets, statistics | data-science |
| ETL, Spark, Airflow, warehouses | data-engineering |
| Docker, K8s, Terraform | devops |
| SQL, PostgreSQL, MySQL | sql-databases |
| RAG, LLM, agents, embeddings | llm-agents |
| React, TypeScript, CSS | web-frontend |
| Security, pentesting | security |
| Kafka-specific | kafka |
| Diffusion, image gen, LoRA | image-generation |

---
title: News Development Graph
category: architecture
tags: [news, project-history, knowledge-graph, llm-agents, json-schema]
---

# News Development Graph

## Contract Scope

The Happyin news system schema 1.4 connects each reviewed news record to a
project or organization development thread and to an agent-readable Knowledge
Space resource. Schema 1.2 and 1.3 records remain valid and are not assigned
semantic branches retroactively.

Four repositories own separate stages:

| Repository | Owned state |
|---|---|
| `diffusion-love` | Private skeletons, provider runs, evidence, review decisions, export gate |
| `diffusion-love-news` | Public canonical items, JSON Schema, deterministic indexes |
| `diffusion-love-web` | Read-only feed, project, organization and item presentation |
| `knowledge-space` | Dense public implementation references and agent briefs |

The dependency direction is one-way: the private exporter emits a reviewed
public item, the public builder validates and materializes it, and both the
portal and agents consume the resulting public snapshot. The portal never
writes identity or graph state.

## Public Entities

### Project

`project.family_slug` remains the stable project identity. Model versions and
adaptations stay inside the same family. Legacy project pages continue to use
`_projects.json`.

### Organization

`organization.slug` is the stable company or owner identity. A project item
may include both project and organization; their vendor slug and display name
must agree. Company-only news may use an anonymous project object but must keep
the organization identity.

### Development Thread

`development` contains:

```json
{
  "scope": "project",
  "thread_slug": "news-knowledge-graph",
  "thread_display": "News and knowledge graph",
  "predecessor_ids": ["n-0123456789"]
}
```

`scope` selects the project or organization on the same item. Predecessors are
reviewed continuation edges, not similarity results. The public builder checks
that each predecessor exists, is earlier in deterministic chronology, and has
the same subject and thread.

The builder materializes project `development_threads` and a separate
`_organizations.json`. This allows a project page to show parallel lines of
work and an organization page to join direct company milestones with its
explicitly owned projects.

## Knowledge Space Bridge

Every schema 1.4 item contains one reviewed `knowledge` object:

```json
{
  "title": "News Development Graph",
  "article_url": "https://happyin.space/architecture/news-development-graph/",
  "source_url": "https://raw.githubusercontent.com/AnastasiyaW/knowledge-space/FULL_COMMIT_SHA/docs/architecture/news-development-graph.md",
  "agent_context_url": "https://happyin.space/architecture/news-development-graph/#agent-brief"
}
```

The rendered page is stable navigation for people. `source_url` must pin a full
Git commit so an agent reads the same article that was reviewed with the news
record. `agent_context_url` points to the copy-ready instruction below.

This public agent brief is not a provider prompt. Internal enrichment prompts,
raw provider output and review notes remain private and are rejected
recursively by the public feed builder.

## Publication Sequence

1. Write and validate the Knowledge Space article.
2. Merge it and record the exact commit-addressed Markdown URL.
3. Ingest a news skeleton with project/organization, development and knowledge references.
4. Enrich only through an explicitly selected provider or a reviewed manual evidence run.
5. Compose and inspect the complete public candidate.
6. Record an explicit human review decision.
7. Export the canonical item and rebuild all generated public indexes.
8. Verify the exact producer commit, CI validation and authenticated portal routes.

Publishing the article alone does not publish a news item. Exporting a private
candidate alone does not update the public feed. A branch-addressed CDN response
is not proof of one coherent snapshot.

## Agent Brief

Copy this instruction to an agent together with the relevant Happyin news URL:

```text
Read the linked Happyin news item and this Knowledge Space article. Treat the
news item's project, organization, development thread, predecessor IDs and
commit-addressed knowledge source as the authoritative public graph. Explain:
1. what changed;
2. which project or company development line it continues;
3. how the implementation works across the private pipeline, public builder,
   portal and Knowledge Space;
4. which claims are verified, reported or inferred;
5. the exact source revisions that support the answer.

Do not infer missing graph edges from similar titles, tags or embeddings. Do
not treat a mutable branch URL or a current live page as historical proof. If
the immutable source or referenced predecessor cannot be retrieved, state the
missing evidence instead of filling the gap.
```

## Validation Rules

- Identity slugs are lower-case kebab-case and are reviewed before export.
- One development thread belongs to exactly one project or organization.
- Cross-subject, cross-thread, missing and forward predecessor edges fail closed.
- Knowledge Markdown uses an immutable full Git commit URL.
- The public feed contains URLs to agent context, never internal prompt text.
- Derived JSON is rebuilt from item files and is not hand-edited.

## Gotchas

- **Similar news is not a continuation:** search and embeddings can suggest a
  candidate edge. **Fix:** publish only reviewer-approved predecessor IDs.
- **A company name is not identity:** spelling and branding changes create
  duplicate pages. **Fix:** use one canonical organization slug and reject
  conflicting metadata during aggregation.
- **A stable web page is not immutable input:** its contents may change after a
  news review. **Fix:** pair the page with commit-addressed Markdown.
- **Agent context can be confused with enrichment prompts:** relaxing privacy
  scans would expose internal data. **Fix:** keep internal prompt keys forbidden
  and publish only the reviewed article URLs.

## See Also

- [[happyin-knowledge-space]]
- [[architecture-documentation]]
- [[data-serialization-formats]]
- [[agent-architectures]]

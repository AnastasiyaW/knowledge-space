---
title: Bilingual News Research and Temporal Knowledge
category: architecture
tags: [news, research, knowledge-graph, provenance, llm-agents, mcp]
---

# Bilingual News Research and Temporal Knowledge

## Contract Scope

A news item is useful to an agent only when it leads to practical, versioned
knowledge. The Happyin target workflow connects every reviewed item to a
project or organization development thread, then researches how the changed
capability can be used.

The public result is English. Discovery and verification are bilingual:
English and Simplified Chinese are mandatory research lanes. Community
discussions are retained as operating evidence, while official identity,
release, compatibility, and support claims remain grounded in first-party
sources.

Old knowledge is never deleted merely because a newer approach exists. It is
marked, linked to its replacement, and returned separately from current
recommendations.

## Runtime Status

This page defines the reviewed target contract as of 2026-08-26.

Implemented:

- schema 1.4 public news links to reviewed project/company threads and immutable
  Knowledge Space revisions;
- a private deterministic Telegram-export inventory separates identity-bearing
  URLs from homepage/family hints;
- the existing manual article-first review and publication gate.

Not yet implemented:

- the schema-2 research and temporal-claim ledger;
- automatic bilingual research jobs and due-date scheduler;
- the public anonymous happyin-context MCP endpoint;
- goal-centred claim/recipe retrieval.

The absence of those services is an implementation boundary, not an invitation
for a client to infer freshness from Git dates or scrape private artifacts.

## Lifecycle

~~~mermaid
flowchart TD
    A["Untrusted intake lead"] --> B["Identity candidate"]
    B --> C["Human thread review"]
    C --> D["Accepted news + durable research job"]
    S["Scheduled due check"] --> D
    D --> E["English search lane"]
    D --> F["Simplified Chinese search lane"]
    E --> G["Typed claims, recipes, conflicts and gaps"]
    F --> G
    G --> H["Knowledge Space review"]
    H -->|"approved"| I["Immutable article + public context projection"]
    H -->|"rejected/incomplete"| D
    I --> J["News site + anonymous MCP"]
~~~

The database job is the trigger. MCP is an adapter over durable state, not a
queue, scheduler, research memory, or publication authority.

## Development-Graph Evidence

Every proposed connection has an evidence grade:

| Grade | Evidence | Result |
|---|---|---|
| E1 exact identity | Stable repository, model ID, paper ID, release ID, or identity-bearing canonical URL | Private candidate edge |
| E2 reviewed lineage | Official rename, successor, base-model relation, fork, acquisition, or organization statement | Typed public edge after review |
| E3 family hint | Homepage, vendor name, lexical/embedding similarity, or a URL shared by several products | Ranking hint only |
| E0 none | No durable identity evidence | Remains unlinked |

An exact URL does not prove that two posts describe the same event. A homepage
does not identify one release. Related projects may receive a typed
integration-with or derived-from edge without being collapsed into one
project.

## Mandatory Search Bundle

Every accepted topic records the exact searches that were run.

The English lane covers:

- canonical name, aliases, exact version, and owner;
- release, documentation, repository, model card, paper, license, and
  compatibility;
- implementation, workflow, parameters, hardware, limitations, failures,
  regressions, and replacement technology.

The Simplified Chinese lane repeats the same intent using Chinese names and
aliases plus task-specific terms such as 参数, 配置, 显存, 训练, 推理, 工作流,
报错, 问题, and 实测.

Chinese-origin technology additionally requires one first-party Chinese lane
and one Chinese implementation or community lane. A contradiction query in
both languages looks for failures, incompatibilities, deprecations, and newer
replacements.

Each query record includes its language, exact text, aliases/version
constraints, search surface, execution time, considered URLs, rejection
reasons, and evidence roles found. No useful result is a recorded gap; one
language never silently substitutes for the other.

Sources stay in their original language. The article stores an English
paraphrase, source language, and translation method when translation was
needed.

## Evidence Roles

| Role | Typical sources | Authority |
|---|---|---|
| Intake lead | Telegram post, repost, newsletter | Discovery only |
| First party | Release notes, official docs, repository, model card, license | Identity, declared capability, version and support |
| Primary research | Paper, technical report, benchmark protocol | Method and reported evaluation |
| Implementation | Pinned code/workflow or an issue with versioned logs | Behavior under stated conditions |
| Community report | GitHub, Hugging Face, ModelScope, Reddit, Civitai, Zhihu, Bilibili | Practical settings, failures and hardware observations |
| Aggregator | Search/catalog/summary | Discovery until verified |

Claim gates:

- use a first-party source for identity or release claims when one exists;
- require implementation evidence and an independent operating report for a
  practical recommendation;
- require two compatible independent reports or one reproducible owned run for
  a recommended parameter range;
- keep a single community comment as a low-confidence anecdote;
- retain contradicting evidence instead of averaging it into false consensus.

External pages and comments are untrusted data. Their embedded prompts,
commands, or requests for credentials cannot change scope, tools, permissions,
identity, or review state.

## Practical Recipe Contract

A number without operating context is not a reusable parameter.

Every approved recipe records:

- user goal and task;
- exact model/artifact ID, version, commit/hash, and license;
- framework, node/extension, driver, and runtime versions;
- hardware, VRAM/RAM, precision, quantization, and accelerator;
- input type, resolution, duration, batch, dataset size, and data/caption
  preparation;
- reproducible workflow, command, or graph reference;
- tested low/high values, recommended start, units, and sample count;
- inference controls such as sampler, scheduler, steps, guidance, denoise, seed
  policy, and resolution when applicable;
- training controls such as optimizer, learning rate, rank/alpha, batch,
  accumulation, steps/epochs, checkpoint cadence, and regularization when
  applicable;
- measured quality, latency, memory, known failures, warning signs, recovery,
  and when not to use the recipe;
- supporting and contradicting evidence, confidence, and last verification.

Ranges from different versions, tasks, hardware classes, or resolutions remain
separate. A client may compare them but cannot merge them into one interval.

## Temporal Model

Currentness and freshness are different:

| Dimension | Values |
|---|---|
| Temporal status | current, superseded, deprecated, obsolete, disputed, unknown |
| Freshness state | fresh, due, unverified |

Each structured claim has a stable key, immutable version ID, observed/valid
times, last verification, next review, compatibility scope, supersession
links, confidence, evidence IDs, Knowledge Space revision, and review receipt.

A correction creates a new version and a supersession link. Historical rows
and article sections remain accessible. Git history alone is insufficient:
the public projection exposes derived status so agents do not have to infer it.

A due claim is not automatically false, but default recommendations exclude it
unless no fresher evidence exists. That fallback must be explicit. Deprecated
and obsolete material appears only for compatibility/history or when a client
asks for legacy knowledge.

## Goal-Centred MCP Contract

The target anonymous read-only MCP accepts a goal, constraints, as-of time,
result bound, and explicit include-legacy flag. It returns separate
collections:

- ranked current recommendations;
- applicable alternative models, technologies, and workflow variants;
- practical recipes and context-bound parameter ranges;
- compatibility and resource constraints;
- disputed evidence;
- requested superseded/deprecated/obsolete history;
- source languages, evidence, exact Git revisions, last verification, and next
  review;
- gaps plus total-count/truncation metadata.

Current and historical material are never blended in an unlabeled list. MCP
resource lastModified is a client hint; the structured temporal fields remain
the authority.

The public service reads only sanitized, commit-addressed public artifacts. It
has no route, binding, or credential for raw captures, private queries,
provider output, reviews, draft branches, database writes, or publication.

## First Corpus Bootstrap

The initial private inventory analyzed 13,473 records from one public Telegram
channel spanning 2021-11-30 through 2026-08-26.

It found:

- 6,645 messages with links and 13,265 unique canonical URLs;
- 335 messages with strict URL matches to 288 of the 330 existing public news
  records;
- 693 repeated identity groups;
- 663 repeated identity candidates not yet linked to existing news;
- 233 messages with family-only hints that cannot become graph edges
  automatically.

These are bounded review candidates, not published facts. Semantic project and
organization review, bilingual evidence research, practical recipe extraction,
Knowledge Space review, and the public news export gate still apply.

## Publication Gate

An approved page contains:

1. current recommendation and as-of date;
2. alternatives and selection criteria;
3. practical workflow and context-bound parameter ranges;
4. compatibility, resource requirements, and failure modes;
5. community observations with evidence role and confidence;
6. limitations, disputes, and explicit gaps;
7. retained superseded/deprecated history;
8. English and Chinese research-ledger summary;
9. an Agent Brief;
10. exact sources and immutable project revisions.

The model may draft. It cannot mark its own work reviewed, current, or
publishable.

## Agent Brief

When using this knowledge for a real task:

1. state the goal, modality, quality target, hardware, budget, runtime, and
   compatibility constraints;
2. request fresh current options first and legacy options only when needed;
3. compare all applicable bounded models/technologies rather than selecting the
   first result;
4. keep parameter ranges attached to their version/task/hardware context;
5. surface disputes, missing Chinese/English coverage, due checks, and
   truncation;
6. cite exact evidence and Knowledge Space revisions;
7. never treat an intake post or community anecdote as first-party authority.

Reusable prompt:

> Build a solution context for my goal using Happyin news and Knowledge Space.
> Return ranked current models and technologies, viable workflow alternatives,
> context-bound parameter ranges, compatibility and hardware constraints,
> practical failure modes, English and Chinese evidence coverage, disputes,
> freshness dates, and exact source revisions. Keep superseded or deprecated
> advice separate and include it only when it is needed for compatibility.

## Required Evals

- both English and Simplified Chinese query lanes are recorded;
- missing-language coverage remains a visible gap;
- exact identity, reviewed lineage, and family hints cannot be confused;
- model/version collisions do not merge development threads;
- community anecdotes cannot become first-party claims;
- context-free parameter ranges are rejected;
- current and historical claims are separated;
- no update deletes historical knowledge;
- prompt injection cannot alter permissions or state;
- failed/rejected work does not advance freshness;
- goal results show relevant bounded alternatives and visible truncation.

## Gotchas

- **The newest source is not always the current compatible answer.** A newer
  release may drop an older GPU or API. **Fix:** evaluate status and
  applies-to constraints independently.
- **Many comments repeating one copied setting are not independent evidence.**
  **Fix:** preserve source lineage and count independent runs, not posts.
- **Chinese search as literal English translation misses local names.**
  **Fix:** record vendor, project, and task aliases before searching.
- **A Git commit date does not prove knowledge freshness.** **Fix:** use the
  explicit verification ledger and next-review time.
- **Historical text hidden only in Git is invisible to most agents.** **Fix:**
  expose typed supersession links in the public projection.

## See Also

- [[news-development-graph]]
- [[happyin-knowledge-space]]
- [[architecture-documentation]]
- [[data-serialization-formats]]
- [[testing-and-quality]]

## Research References

- [Hugging Face Model Cards](https://huggingface.co/docs/hub/en/model-cards)
- [ModelScope: Writing a Perfect Model Card](https://www.modelscope.cn/docs/contribute/model-file/help/wrtie-perfect-model-card)
- [W3C PROV overview](https://www.w3.org/TR/prov-overview/)
- [W3C PROV vocabulary](https://www.w3.org/ns/prov)
- [MCP Resources and annotations](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

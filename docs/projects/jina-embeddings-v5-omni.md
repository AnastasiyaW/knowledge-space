---
title: jina-embeddings-v5-omni
category: projects
date: 2026-05-13
tags: [jina-embeddings-v5-omni, project]
aliases: ["jina-embeddings-v5-omni"]
---

# jina-embeddings-v5-omni

**Development line:** `project:jina-embeddings-v5-omni` · thread `jina-embeddings-v5-omni`  
**Last event:** 2026-05-13 · 1 dated since 2026-05-13 · **Researched:** 2026-11-21 · confidence: medium

## What it is

jina-embeddings-v5-omni is a family of multimodal embedding models from Jina AI that map text, images, audio, and video into one shared vector space.

- Users: teams building multimodal search and retrieval indexes, including Elasticsearch users through Elastic Inference Service.
- Key capability: text, image, audio, and video inputs share one vector space with the text-only jina-embeddings-v5-text models, so text queries can search other media without reindexing.
- Limits: non-commercial license for the published weights (commercial use requires contacting Jina); long videos are summarized from up to 32 frames; the models are trained mainly for text queries.

Two sizes exist: small (about 2B parameters, 1024-dimension vectors, 32,768-token context) and nano (about 1.0B parameters, 768-dimension vectors, 8,192-token context per Elastic's article).

## Development line

- **2026-05-13 — Jina AI publicized jina-embeddings-v5-omni.** The public surfaces were in place by 2026-05-13: the arXiv paper (v1 2026-05-08), an Elastic Search Labs article (2026-05-11), and the Hugging Face collection. Dates corrected from the stub's single date to the primary sources above.

## What changed

- 2026-05-08 — arXiv 2605.08384 v1 posted (method: frozen text backbone with trained connectors for image and audio encoders; about 0.35% of joint-model weights trained).
- 2026-05-11 — Elastic Search Labs article: text, image, video, and audio embedded into a single Elasticsearch index through EIS inference IDs.
- 2026-05-12 — MLX and GGUF variant builds appear in the Hugging Face collection with this update date.
- 2026-08-17 — arXiv 2605.08384 v4 revision.
- 2026-09-17 — Hugging Face collection last updated (collection page).
- 2026-10-11 — Omni base, retrieval, classification, clustering, and text-matching variants updated (collection page).

## How to use this

1. Check the license before any commercial plan: the small model card lists CC BY-NC 4.0 and says commercial use requires contacting Jina. — <https://huggingface.co/jinaai/jina-embeddings-v5-omni-small>
2. Choose a size and a task adapter. The base repository holds retrieval, classification, clustering, and text-matching adapters. — <https://huggingface.co/jinaai/jina-embeddings-v5-omni-small>
3. For retrieval, set query and document roles explicitly; the card warns that a bare `encode(text)` call does not know which side is intended. — <https://huggingface.co/jinaai/jina-embeddings-v5-omni-small>
4. In Elasticsearch, use the inference IDs `.jina-embeddings-v5-omni-small` or `.jina-embeddings-v5-omni-nano` through Elastic Inference Service; text fields go through `semantic_text`, other media through the inference API. — <https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index>
5. Pass audio as a separate input part; the card states video soundtracks are not read implicitly. — <https://huggingface.co/jinaai/jina-embeddings-v5-omni-small>

## Best practices

- Index short clips rather than full films: the Elastic article says the model "is optimal with short clips" and extracts up to 32 frames per video. — <https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index>
- Test text-query retrieval first; the article says non-text queries "may be less effective." — <https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index>
- For non-retrieval tasks on raw-path text, add the `Document:` prefix the card requires; otherwise the input is off-distribution. — <https://huggingface.co/jinaai/jina-embeddings-v5-omni-small>
- Use transformers 4.57 or newer; the card recommends 5.1 or newer for the small variants. — <https://huggingface.co/jinaai/jina-embeddings-v5-omni-small>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Benchmark numbers: the paper text fetched only says results are "competitive with the state-of-the-art" and names no benchmark.
- The nano model card was not read; its figures come from the Elastic article.
- Commercial license terms beyond "contact us" are not stated.
- Mixed-media inputs (for example an image with accompanying text) are listed by Elastic as still under development.
- Whether the Hugging Face collection's 26 entries match the Elastic and Jina API surfaces was not checked.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/collections/jinaai/jina-embeddings-v5-omni | Hugging Face collection: jina-embeddings-v5-omni | 2026-11-21 |
| https://huggingface.co/jinaai/jina-embeddings-v5-omni-small | Hugging Face model card: jina-embeddings-v5-omni-small | 2026-11-21 |
| https://arxiv.org/abs/2605.08384 | GELATO paper: jina-embeddings-v5-omni (arXiv) | 2026-11-21 |
| https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index | Elastic Search Labs: all media, one index | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:jina-embeddings-v5-omni`, thread `jina-embeddings-v5-omni`, 1 dated event 2026-05-13; release facts 2026-05-08 → 2026-10-11.
- **Practical note:** As of 2026-11, evaluate jina-embeddings-v5-omni for a shared cross-media index after confirming the non-commercial license fits your use. Use the retrieval query/document roles explicitly and index short video clips.
- **Confidence:** medium. Model card, paper, and Elastic article read; benchmark numbers and nano model card not read. Dated supersedes above are the authority for what is obsolete.

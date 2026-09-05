---
title: Reflection 70B
category: projects
date: 2024-09-09
tags: [project, reflection-70b, reflection-70b-development, reflection_llm]
aliases: ["Reflection 70B"]
---

# Reflection 70B

**Development line:** `project:reflection-70b` · thread `reflection-70b-development`  
**Last event:** 2024-09-09 · 2 dated since 2024-09-06 · **Researched:** 2026-09-04 · confidence: high

## What it is

Reflection 70B is a downloadable Llama 3.1 70B Instruct fine-tune, now hosted as Reflection Llama-3.1 70B.
We run it with Transformers, vLLM, SGLang, or Docker.

- Self-correction: sequences `<thinking>`, `<reflection>`, and `<output>` tokens.
- Deployment: runs under Transformers, vLLM, SGLang, or Docker.

The repository is 282 GB. Treat it as a historical experiment, not a benchmark-qualified production model. It works for controlled local evaluation. It is unsuitable when original performance claims are a buying or deployment criterion.

## Development line

- **2024-09-06 — Reflection 70B opened for public access.** Reflection 70B linked to a public Railway playground and a Hugging Face model page on 2024-09-06. These destinations marked public access for the project. Available evidence does not establish its technical claims or release terms.
- **2024-09-09 — Public questions emerged on provenance and service behavior.** Community posts raised questions about Reflection 70B's provenance, published weights, and hosted API behavior on 2024-09-09. This changed how we evaluate claims about the model. The linked material alone does not settle these questions.

## What changed

- **2024-09-05** — Reflection 70B was announced as a Llama 3.1 70B Instruct fine-tune with Reflection-Tuning, downloadable weights, a hosted demo, and benchmark claims.
- **2024-09-06** — The release acknowledged an initial upload problem and asked users to retry the corrected Hugging Face model. The model card specified Llama 3.1 chat formatting and reflection tags.
- **2024-09-09** — Independent testing failed to reproduce published performance. Community investigations alleged that the hosted API did not correspond to released local weights.
- **Today** — The renamed Hugging Face repository remains available with Transformers, vLLM, SGLang, and Docker instructions. Its model-card history explicitly records benchmark non-reproducibility.

## How to use this

As of 2024-09-09, verify model provenance, weight identity, and endpoint behavior before relying on Reflection 70B claims or integrating a related hosted API.

1. Open the maintained Reflection Llama-3.1 70B repository and confirm the Llama 3.1 license, hardware capacity, and current files before downloading.
  — <https://huggingface.co/mattshumer/Reflection-Llama-3.1-70B/tree/main>
2. Load the repository with Transformers using its documented model identifier and the standard Llama chat template.
  — <https://huggingface.co/mattshumer/Reflection-Llama-3.1-70B/blob/main/README.md>
3. For a service endpoint, run the documented vLLM or SGLang command and call its OpenAI-compatible chat-completions endpoint.
  — <https://huggingface.co/mattshumer/Reflection-Llama-3.1-70B/blob/main/README.md>

## Best practices

- Evaluate the exact revision on representative tasks before relying on it; the repository records that the public benchmark results were not reproducible.
  — <https://huggingface.co/mattshumer/Reflection-Llama-3.1-70B/blob/main/README.md>
- Use the stock Llama 3.1 chat format and preserve the documented reflection tags when testing the intended prompting behavior.
  — <https://huggingface.co/mattshumer/Reflection-Llama-3.1-70B/blob/main/README.md>
- Do not equate results from a hosted demo or API with the downloadable weights without an identity and output-equivalence check.
  — <https://www.reddit.com/r/LocalLLaMA/comments/1fc98fu/confirmed_reflection_70bs_official_api_is_sonnet/>

## Superseded by this

- 2024-09-09 — Claims that Reflection 70B’s published benchmark results established it as a leading open model are obsolete: independent evaluations did not reproduce those measures.
- 2024-09-06 — Guidance to retry an initially broken upload is historical only; use the currently maintained Reflection-Llama-3.1-70B repository and independently evaluate its exact revision.

## Still unknown

- The available source set does not establish a maintained official API or playground as of today.
- The community allegation about the hosted API is evidence for caution, but is not an independently adjudicated provenance finding.
- The event-specific additions and the 2024-09-05 release step remain without separate finding fields.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/mattshumer/Reflection-Llama-3.1-70B/tree/main | mattshumer/Reflection-Llama-3.1-70B repository | 2026-09-05 |
| https://huggingface.co/mattshumer/Reflection-Llama-3.1-70B/blob/main/README.md | Reflection Llama-3.1 70B model card | 2026-09-05 |
| https://huggingface.co/mattshumer/Reflection-70B-Draft/blob/main/README.md | Reflection 70B Draft model card | 2026-09-05 |
| https://venturebeat.com/ai/meet-the-new-most-powerful-open-source-ai-model-in-the-world-hyperwrites-reflection-70b | Meet the new, most powerful open source AI model in the world: HyperWrite's Reflection 70B | 2026-09-05 |
| https://www.reddit.com/r/LocalLLaMA/comments/1fc98fu/confirmed_reflection_70bs_official_api_is_sonnet/ | CONFIRMED: REFLECTION 70B'S OFFICIAL API IS SONNET 3.5 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:reflection-70b`, thread `reflection-70b-development`, 2 dated events 2024-09-06 → 2024-09-09.
- **Practical note:** As of 2024-09-09, practitioners should independently verify model provenance, weight identity, and endpoint behavior before relying on Reflection 70B claims or integrating a related hosted API.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.

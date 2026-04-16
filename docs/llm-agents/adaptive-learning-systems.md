---
title: Adaptive Learning Systems with LLMs
category: applications
tags: [education, knowledge-tracing, spaced-repetition, learner-modeling, tutoring, fsrs]
---

# Adaptive Learning Systems with LLMs

Architecture patterns for AI-powered education systems that adapt to individual learners. Covers knowledge tracing, lesson generation, spaced repetition, and context-efficient student modeling.

## Four-Layer Architecture

```typescript
Domain Model     -> Knowledge graph, prerequisites, difficulty
Student Model    -> Proficiency state, learning style, history
Tutoring Model   -> Pedagogical decisions, review scheduling
Interface Layer  -> LLM interaction, exercise generation
```

### Domain Model

Knowledge graph with concepts as nodes, prerequisites as directed edges, difficulty scores per concept. Stored externally (JSON/SQLite), queried per lesson. LLM does NOT manage the graph - deterministic traversal provides the structure.

### Student Model

Structured JSON profile tracking:

| Dimension | Update Frequency | Storage |
|-----------|-----------------|---------|
| Per-concept proficiency | Every interaction | Tier 1 (always in context) |
| Error patterns / misconceptions | Per session | Tier 2 (summarized) |
| Learning pace indicators | Per session | Tier 2 |
| Full interaction history | Continuous | Tier 3 (RAG retrieval) |
| Forgetting curves | Per review | FSRS algorithm (external) |

### Tutoring Model

Pedagogical decisions run outside the LLM as deterministic rules. LLM handles: lesson generation, exercise creation, feedback adaptation, explanation style. This separation ensures reproducible scheduling while keeping LLM creativity for content.

## Knowledge Tracing Models

Evolution from Bayesian to transformer-based:

| Model | Architecture | Key Feature |
|-------|-------------|-------------|
| BKT | Hidden Markov | Per-skill binary mastery. Still used in OATutor |
| DKT (2015) | RNN/LSTM | Sequence-based prediction |
| SAKT (2019) | Self-attention | Selective relevant history |
| AKT (2020) | Contextual attention | Exponential decay for forgetting |
| **simpleKT (2023)** | Simplified transformer | Beats complex models. Essential baseline |
| DKT2 (2025) | xLSTM + IRT | Interpretable output |
| UKT (2025) | Probability distributions | Uncertainty-aware, Wasserstein attention |

**pyKT** (pykt.org) - definitive Python library. 10+ models, 7+ datasets, actively maintained. Three-step model training.

## Spaced Repetition: FSRS

**FSRS (Free Spaced Repetition Scheduler)** - state of the art, integrated into Anki 23.10+.

Key principle: review scheduling based on predicted forgetting probability, not fixed intervals. Implementations in JS, Go, Rust, Python.

FSRS-7 supports fractional interval lengths. The algorithm runs externally (deterministic) and feeds review queue into the LLM tutoring layer.

## Pedagogical Principles for LLM Tutors

### Comprehensible Input (i+1)

Input slightly above current level. AI dynamically assesses proficiency and curates progressively challenging content. 95-98% comprehensibility threshold for acquisition. One-size-fits-all i+1 fails - adaptive systems must fine-tune per learner.

### Task-Based Teaching (TBLT)

Three task types to encode as exercise templates:

| Type | What | Example |
|------|------|---------|
| Information-gap | Transfer info between participants | Describe image for partner to draw |
| Reasoning-gap | Derive new info from given facts | Debug code from error message |
| Opinion-gap | Express preferences/justify | Choose best architecture and explain |

### Affective Filter

AI tutors reduce anxiety through: gamified interfaces, immediate non-judgmental feedback, low-pressure practice environments. The LLM's tone and response to errors directly impacts learning effectiveness.

## Token-Efficient Student Context

### Tiered Context Strategy

For ~4K token student context budget:

```php
Tier 1 - Always in context (~300 tokens):
  Current proficiency vector (concept -> score)
  Last 3-5 interactions summary

Tier 2 - Summarized (~500 tokens):
  Session summaries (last 5 sessions)
  Known misconceptions, error patterns

Tier 3 - Retrieved on demand (RAG):
  Full interaction history
  Detailed error logs
  Historical proficiency curves
```

### Context Budget Allocation

| Section | Tokens | Purpose |
|---------|--------|---------|
| System prompt + pedagogy rules | ~1000 | Teaching methodology |
| Student profile (Tier 1) | ~300 | Current state |
| Session history (Tier 2) | ~500 | Recent context |
| Current lesson content | ~1000 | Active material |
| Exercise + scaffolding | ~500 | Current task |
| Generation buffer | ~700 | Model output |

### Lost-in-the-Middle Mitigation

30%+ accuracy drop for information placed in the middle of long contexts. Student proficiency data goes at START. Recent interactions at END. Summaries and background in the middle (least critical position).

## LLM Lesson Generation Patterns

### Dual-Layer Prompt Strategy (LPITutor)

- **Static layer**: pedagogically aligned templates (exercise types, feedback rules)
- **Dynamic layer**: injected per-request (retrieved content + learner metadata)

### Content Generation Pipeline

LLMs learn from examples created by learning experts. Key insight from production systems: not fully autonomous - constant prompt tuning required. LLMs generate candidate exercises; pedagogical rules validate structure and difficulty.

### Curriculum Adaptation

Adaptive Difficulty Curriculum Learning (ADCL) addresses the Difficulty Shift phenomenon - when difficulty calibration drifts as student progresses. Monitor difficulty delta between consecutive exercises and cap maximum jump.

## Open-Source Platforms

- **OATutor** (CAHLR/OATutor) - React + Firebase, BKT mastery, field-tested in classrooms
- **adaptive-knowledge-graph** (MysterionRise) - KG + Local LLMs + Bayesian tracking, privacy-first
- **LearnHouse** - Notion-like editor, open learning platform
- **FOKE** (Stanford SCALE) - hierarchical knowledge forest, multi-dimensional profiling

## Gotchas

- **FSRS must run outside the LLM** - putting scheduling logic in prompts makes it non-deterministic. Review intervals drift. Run FSRS as code, inject results into context.
- **simpleKT beats most complex models** - resist the urge to implement cutting-edge KT architectures. Start with simpleKT as baseline, only add complexity if measured improvement justifies it.
- **Student proficiency stales fast in context** - if a student answers 10 questions between proficiency updates, the LLM is working with outdated state. Update Tier 1 profile after every interaction, not batched.
- **i+1 is not universal** - the optimal challenge level varies by learner, topic, and time of day. Fixed i+1 underperforms adaptive systems that calibrate per-learner.

## See Also

- [[agent-memory]] - memory patterns applicable to student modeling
- [[context-engineering]] - context management for long sessions
- [[rag-pipeline]] - retrieval for Tier 3 student history
- [[embeddings]] - concept similarity for prerequisite detection

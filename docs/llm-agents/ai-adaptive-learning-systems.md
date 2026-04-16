---
title: "AI-Powered Adaptive Learning Systems"
description: "Knowledge tracing models, learner profiling, lesson generation architectures, spaced repetition integration, and context-efficient student state management."
---

# AI-Powered Adaptive Learning Systems

Architecture and components for building LLM-based adaptive tutoring systems. Covers student modeling, lesson generation, pedagogical knowledge encoding, and efficient context management.

## Knowledge Tracing Models

Predicting student mastery state from interaction history.

### Evolution

| Model | Year | Architecture | Key Contribution |
|-------|------|-------------|-----------------|
| BKT | 1994 | Hidden Markov | Binary mastery, per-skill |
| DKT | 2015 | LSTM/RNN | Deep learning on interaction sequences |
| SAKT | 2019 | Self-attention | Selectively attends to relevant past interactions |
| AKT | 2020 | Contextual attention + exponential decay | Models forgetting curves |
| simpleKT | 2023 | Simplified transformer + Rasch IRT | Beats complex models, hard to beat |

### 2025 Frontier Models

- **DKT2** - xLSTM + IRT for interpretable output
- **HCGKT** - Hierarchical graph filtering + contrastive learning + GNNs
- **LefoKT** - Decouples forgetting from problem relevance via relative forgetting attention
- **UKT** - Uncertainty-aware knowledge state (Wasserstein attention, probability distributions)
- **ReKT** - 3D knowledge state: topic × knowledge point × knowledge domain; lightweight FRU framework
- **DyGKT** - Dynamic graph learning, models prerequisite structure via GNNs

### Reference Implementation

**pyKT** - canonical Python KT library:
```bash
pip install pykt-toolkit
# 10+ models, 7+ standardized datasets, 3-step training pipeline
# GitHub: github.com/pykt-team/pykt-toolkit
```

## Four-Layer Adaptive Learning Architecture

```text
1. Domain Model         knowledge graph, concept map, prerequisite structure
2. Student Model        proficiency per concept, learning style, forgetting curves
3. Tutoring Model       what to teach next, how to present, when to review
4. Interface Layer      exercise delivery, feedback UI, progress visualization
```

## Student Model: Profile Dimensions

A complete learner profile includes:
- **Knowledge state** - per-concept mastery probability (updated after each interaction)
- **Learning pace** - concept acquisition rate relative to baseline
- **Error patterns** - recurring misconceptions, specific knowledge gaps
- **Forgetting curves** - per-concept forgetting rate for spaced repetition scheduling
- **Cognitive load estimate** - time-on-task, retry frequency, hint usage
- **Behavioral signals** - navigation patterns, session length, break frequency

## Spaced Repetition Integration

**FSRS** (Free Spaced Repetition Scheduler) is the state of the art algorithm:

```python
# FSRS-7 (latest), backed by Anki 23.10+
# github.com/open-spaced-repetition/fsrs4anki
# Implementations: JS, Go, Rust, Python
# Key principle: review scheduling based on predicted forgetting probability
# NOT fixed intervals

# Integration point: FSRS runs OUTSIDE the LLM
# LLM role: generate lesson content
# FSRS role: schedule when to show it again
```

FSRS handles scheduling deterministically. Never route scheduling decisions through an LLM - it's a solved optimization problem.

## LLM Lesson Generation

### Duolingo Birdbrain Architecture (Reference)

- Updates daily from ~1.25B exercises
- After every interaction: estimates (1) exercise difficulty across user base, (2) individual proficiency
- Session generator builds custom lessons in real-time
- Maintains learner in "optimal challenge zone"

### i+1 Comprehensible Input Principle

Target material should be slightly above current proficiency:
- 95-98% comprehensibility threshold for effective acquisition
- Below that: too hard, no acquisition
- Above that: no challenge, no growth
- AI implementation: estimate current level → generate material at i+1 complexity

### Pedagogical Knowledge Base Structure

```
pedagogical_kb/
  theories/
    spaced_repetition.json     # FSRS params, scheduling rules
    comprehensible_input.json  # i+1 rules, thresholds
    cognitive_load.json        # CLT principles, load management
  
  exercise_templates/
    fill_in_blank.json         # template + difficulty params + assessment criteria
    code_completion.json       # for programming specifically
    reasoning_gap.json         # problem-solving exercises
    
  progression_rules/
    difficulty_calibration.json  # adjustment based on performance
    concept_prerequisites.json   # dependency graph
```

Each entry encodes: WHY (pedagogical principle) + WHAT (rule) + WHEN (trigger) + HOW (implementation pattern).

## Context-Efficient Student State

### Tiered Context Loading

```
Tier 1 - Always in context (~300-500 tokens):
  current proficiency vector (last 10-20 concepts)
  active lesson context
  last 3-5 interaction summaries

Tier 2 - Summarized (~500-1000 tokens):
  session summaries (last 5 sessions)
  known misconceptions and error patterns
  learning pace indicators

Tier 3 - RAG on demand:
  full interaction history
  completed lesson details
  historical proficiency curves
```

### 4K Token Budget Example

```text
System prompt + pedagogy rules:  ~1000 tokens
Student profile (Tier 1):         ~300 tokens
Session history summary:          ~500 tokens
Current lesson content:          ~1000 tokens
Exercise + scaffolding:           ~500 tokens
Generation buffer:                ~700 tokens
Total:                           ~4000 tokens
```

### Lost-in-the-Middle Problem

LLMs lose 30%+ accuracy for information in the middle of long contexts:

```text
FIRST: student proficiency data (recency + importance)
LAST:  recent interactions (recency bias)
MIDDLE: lesson background, summaries (less critical)
```

## Open-Source Platforms

**adaptive-knowledge-graph** (MysterionRise/adaptive-knowledge-graph):
- KG + local LLMs + Bayesian skill tracking
- Privacy-first RAG with graph-enhanced retrieval
- KG-aware RAG: retrieves conceptually related content via graph traversal

**OATutor** (CAHLR/OATutor):
- React + Firebase, BKT for skill mastery
- CHI 2023 paper, field-tested in classrooms

**LearnHouse** (learnhouse/learnhouse):
- Notion-like editor, open-source learning platform
- Suitable for content delivery layer

## Architecture Diagram

```text
Knowledge Graph ──────────────────────────────────┐
(concepts, prerequisites, difficulty)             │
                                                  v
Student Model (Proficiency + History) ──→ FSRS Scheduler
                    │                     (Review Queue)
                    v
Lesson Generator ──→ Pedagogical KB
(LLM + Prompts)     (Templates, Rules)
                    │
                    v
Context Builder (Tier 1/2/3 compression → token budget)
```

## Gotchas

- **FSRS runs outside the LLM.** The scheduling algorithm is deterministic. Passing scheduling decisions to an LLM introduces hallucination, inconsistency, and extra cost. Compute the schedule, pass it to the LLM as fact.
- **Knowledge tracing on small interaction histories is unreliable.** BKT and DKT both need 10+ interactions per concept for stable estimates. Cold-start problem: use peer profiling or explicit placement tests before adaptive scheduling.
- **simpleKT outperforms complex models on most datasets.** Before building DyGKT-style graph learning, verify that simpleKT doesn't already meet your accuracy target. The simple model is easier to debug and deploy.
- **"Optimal challenge zone" placement is harder than it sounds.** Birdbrain runs on 1.25B exercises daily. For smaller systems, use conservative difficulty targets (60-70% success rate) rather than trying to hit i+1 precisely.

## See Also

- [[adaptive-learning-systems]]
- [[rag-pipeline]]
- [[knowledge-graph-memory]]
- [[token-optimization]]

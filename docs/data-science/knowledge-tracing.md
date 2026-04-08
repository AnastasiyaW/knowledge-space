---
title: Knowledge Tracing
category: techniques
tags: [knowledge-tracing, learner-modeling, adaptive-learning, spaced-repetition, education-ai, knowledge-graph]
---

# Knowledge Tracing

Knowledge tracing (KT) models predict the probability that a learner will answer a question correctly, given their interaction history. Core component of adaptive learning systems that decide what to teach next and when to review.

## Key Facts

- KT models take sequences of (question, correct/incorrect) pairs and predict P(correct) for the next question
- Evolution: BKT (1995) -> DKT (2015) -> SAKT (2019) -> AKT (2020) -> simpleKT (2023) -> frontier models (2025)
- simpleKT (ICLR 2023) is a simplified transformer baseline that beats most complex models - hard to outperform
- pyKT is the standard library: 10+ models, 7+ datasets, actively maintained
- FSRS-7 is the SOTA spaced repetition scheduler - integrated into Anki 23.10+, implementations in JS/Go/Rust/Python
- The 4-layer adaptive learning architecture (domain model, student model, tutoring model, interface) is the standard framework

## Model Evolution

### BKT (Bayesian Knowledge Tracing)

Hidden Markov model with per-skill binary mastery state. Four parameters per skill: P(init), P(learn), P(guess), P(slip).

```text
State: UNLEARNED -> LEARNED (transition with P(learn))

Observation model:
  If LEARNED:   P(correct) = 1 - P(slip)
  If UNLEARNED: P(correct) = P(guess)

After each observation, update P(LEARNED) via Bayes' rule.
Mastery threshold: typically P(LEARNED) > 0.95
```

Limitations: binary mastery (no partial knowledge), independent skills (no transfer), no forgetting.

### DKT (Deep Knowledge Tracing, 2015)

RNN/LSTM over the full interaction sequence. Learns latent knowledge state implicitly.

```python
# DKT input encoding
# Each timestep: one-hot of (question_id, correctness)
# For Q questions: input_dim = 2 * Q
# x_t = one_hot(q_t + Q * a_t) where a_t in {0, 1}

import torch.nn as nn

class DKT(nn.Module):
    def __init__(self, n_questions, hidden_dim=100):
        super().__init__()
        self.input_dim = 2 * n_questions
        self.rnn = nn.LSTM(self.input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, n_questions)

    def forward(self, x):
        # x: (batch, seq_len, 2*n_questions)
        h, _ = self.rnn(x)
        # h: (batch, seq_len, hidden_dim)
        return torch.sigmoid(self.fc(h))
        # output: (batch, seq_len, n_questions) = P(correct) per question
```

Improvement over BKT: captures complex skill dependencies, partial knowledge, and temporal patterns. But acts as a black box - no interpretable knowledge state.

### SAKT (Self-Attentive KT, 2019)

Replaces RNN with self-attention. Selectively attends to relevant past interactions rather than compressing everything into a hidden state.

```text
Key idea:
  Query: current question embedding
  Keys/Values: past interaction embeddings (question + response)
  
  Attention scores = which past interactions are relevant
  to predicting the current question
  
  Advantage: handles long sequences better than LSTM
  (no vanishing gradient over hundreds of interactions)
```

### AKT (Attentive KT, 2020)

Adds contextual attention + exponential decay for forgetting. Considers question similarity explicitly.

```text
Innovations over SAKT:
  1. Monotonic attention - context-aware, distinguishes 
     "mastered then forgot" from "never learned"
  2. Rasch model integration - question difficulty as explicit parameter
  3. Exponential forgetting factor - recent interactions weighted higher
  4. Question similarity - attention weighted by how similar 
     past questions are to the current one
```

### simpleKT (ICLR 2023)

Simplified transformer baseline with Rasch model-inspired question-specific difficulty. Hard to beat despite its simplicity.

```text
Architecture:
  1. Question embedding + difficulty parameter (Rasch-like)
  2. Interaction embedding = question_emb + correctness_emb
  3. Standard transformer encoder over interaction sequence
  4. Linear prediction head -> P(correct)

Why it wins: proper question difficulty modeling + clean architecture
eliminates noise that complex models add. 
Essential baseline for any KT research.
```

### 2025 Frontier Models

| Model | Innovation | Architecture |
|-------|-----------|-------------|
| DKT2 | xLSTM + IRT output | Interpretable deep KT |
| HCGKT | Hierarchical graph + contrastive learning | Graph convolutions |
| LefoKT | Decouples forgetting from relevance | Relative forgetting attention |
| UKT | Knowledge as probability distributions | Wasserstein attention |
| ReKT | 3D knowledge state (topic/point/domain) | FRU: Forget-Response-Update |
| DyGKT | Dynamic prerequisite graphs | GNNs for prerequisite structure |

## Adaptive Learning Architecture

Standard 4-layer architecture for building adaptive education systems:

```text
Layer 1: Domain Model
  Knowledge graph / concept map / prerequisite structure
  Nodes: concepts/skills
  Edges: prerequisites, similarity, co-occurrence
  
Layer 2: Student Model
  Per-learner state: proficiency per concept, learning style,
  cognitive load, forgetting curve, behavioral patterns
  Updated after every interaction via KT model
  
Layer 3: Tutoring Model
  Pedagogical decisions: what next? how to present? when to review?
  Inputs: student model state + domain model structure
  Uses: FSRS for review scheduling, i+1 for difficulty selection
  
Layer 4: Interface Layer
  Interaction design, exercise rendering, feedback presentation
```

## Spaced Repetition with FSRS-7

FSRS (Free Spaced Repetition Scheduler) is the SOTA algorithm for scheduling reviews. Based on predicted forgetting probability rather than fixed intervals.

```text
FSRS-7 key properties:
  - Predicts P(recall) at any point in time
  - Supports fractional interval lengths
  - 4 core parameters per item: difficulty, stability, 
    elapsed days, scheduled days
  - Backed by academic research, integrated into Anki 23.10+
  
Implementations: JS, Go, Rust, Python
Benchmark: github.com/open-spaced-repetition/srs-benchmark
```

## Student Context Compression

Efficient encoding of student state for LLM-based tutoring systems:

```text
Tier 1 - Always in context (~200-500 tokens):
  Proficiency vector (concept -> score, last 10-20 concepts)
  Active lesson context
  Last 3-5 interaction summaries
  Active misconceptions

Tier 2 - Summarized (~500-1000 tokens):
  Session summaries (last 5 sessions)
  Error pattern clusters
  Learning pace indicators

Tier 3 - Retrieved on demand (RAG):
  Full interaction history
  Detailed error logs
  Historical proficiency curves

Placement in LLM context ("Lost in the Middle" mitigation):
  START: student proficiency data (critical)
  MIDDLE: background summaries (least critical)
  END: recent interactions (high attention)
```

## pyKT Library

The standard Python library for knowledge tracing research and deployment.

```python
# pyKT: 3-step model training
# Step 1: Prepare dataset
# Supports: ASSISTments, EdNet, Junyi, Statics, NIPS34, etc.

# Step 2: Train model
# python train.py --dataset_name assist2015 --model_name simpleKT \
#   --emb_size 64 --learning_rate 0.001 --seed 42

# Step 3: Evaluate
# Metrics: AUC, accuracy, RMSE
# Cross-validation with temporal split (no future leakage)
```

Available models: DKT, DKVMN, SAKT, AKT, simpleKT, CL4KT, LPKT, HawkesKT, and more.

## Open-Source Platforms

- **adaptive-knowledge-graph** - Knowledge Graphs + Local LLMs + Bayesian skill tracking, privacy-first RAG with KG-enhanced retrieval, IRT/BKT mastery modeling
- **OATutor** - React + Firebase, BKT for skill mastery, field-tested in classrooms
- **pyKT** - standard KT library, 10+ models, 7+ standardized datasets

## Gotchas

- **simpleKT is deceptively hard to beat** - many papers claim improvements over DKT/SAKT but fail to outperform simpleKT when properly tuned. Always include it as a baseline. The Rasch-inspired question difficulty parameter carries most of the performance
- **Temporal data leakage in evaluation** - standard random train/test splits leak future information (student interactions from later sessions appear in training). Always use temporal splits: train on interactions before time T, test on interactions after T
- **Knowledge graph quality bottlenecks everything** - the domain model (prerequisite structure) is typically hand-authored and expensive. Errors in prerequisites propagate through the tutoring model. Automated KG construction from exercise data is an active research area but not yet reliable
- **Forgetting is asymmetric** - skills learned through effortful recall are forgotten slower than those learned through re-reading or hints. KT models that treat all correct responses equally miss this. AKT and LefoKT partially address this

## See Also

- [[bayesian-methods]] - foundation for BKT and IRT models
- [[rnn-sequences]] - LSTM architecture used in DKT
- [[attention-mechanisms]] - self-attention used in SAKT, AKT, simpleKT
- [[graph-neural-networks]] - GNNs used in DyGKT and HCGKT
- [[recommender-systems]] - similar collaborative filtering ideas apply to exercise recommendation

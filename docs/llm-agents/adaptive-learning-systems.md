---
title: "Adaptive Learning Systems with LLMs"
description: "A bounded architecture for learner state, deterministic scheduling, content generation, evaluation, and privacy"
---

# Adaptive Learning Systems with LLMs (September 2026)

Version context: learner models, curricula, and scheduling algorithms are domain policies. Treat their versions, calibration data, and privacy rules as deployable artifacts; do not embed them only in an LLM prompt.

An LLM can generate explanations and exercises, but it should not be the source of truth for prerequisite graphs, learner records, review scheduling, or high-stakes assessment decisions.

## Four Bounded Layers

```text
Curriculum model  -> concepts, prerequisites, approved objectives
Learner model     -> evidence-backed estimates and review history
Scheduler         -> deterministic next-review and workload policy
Generation layer  -> explanations, examples, feedback, and exercise candidates
```

The boundary makes a system testable: curriculum and scheduling can be replayed without a model call, while generation can be evaluated against a known learner state.

## Learner Event Contract

Store observed interactions, not ungrounded statements such as `the learner understands algebra`.

```json
{
  "event_id": "evt_01J...",
  "learner_id": "pseudonymous-id",
  "concept_id": "fractions.addition",
  "activity_revision": "fractions-v5",
  "submitted_at": "2026-09-03T18:00:00Z",
  "result": "incorrect",
  "attempt_count": 2,
  "evidence_ref": "encrypted://assessment/...",
  "consent_policy": "education-data-v2"
}
```

A learner-state update is a versioned transformation of events. Record its model or rule revision, confidence, timestamp, and source event range.

## Scheduling Outside the LLM

The scheduler owns when an item is due. Anki documents FSRS as a separate scheduling algorithm that estimates recall probability and uses a desired-retention setting; it is a useful example of why scheduling must be deterministic and independently auditable.

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReviewDecision:
    concept_id: str
    due_at: datetime
    scheduler_revision: str
    reason: str


def next_activity(decision: ReviewDecision) -> dict[str, str]:
    return {
        "concept_id": decision.concept_id,
        "scheduler_revision": decision.scheduler_revision,
        "reason": decision.reason,
    }
```

The LLM may receive this selected activity plus the learner's least-privilege context. It must not choose a different due date or silently rewrite mastery state.

## Generation Contract

Use the model to propose content that is then validated against curriculum constraints:

| Input | Validator |
|---|---|
| Concept and prerequisite set | Curriculum service |
| Difficulty band | Calibrated policy |
| Exercise format | Schema validator |
| Factual source material | Retrieval/citation validator |
| Learner-visible feedback | Safety and tone policy |
| Answer key | Deterministic checker or reviewed rubric |

For open-ended feedback, label the output as assistance. Do not represent generated feedback as a verified grade unless an assessment policy explicitly permits it.

## Knowledge Tracing

Knowledge tracing predicts future performance from interaction sequences. It is an estimator, not a fact about a learner.

Start with a transparent baseline and measure calibration on held-out learner histories. Use a research toolkit such as pyKT only after confirming that its data representation, split strategy, and license fit the product. The implementation choice must be justified by a measured improvement over the baseline.

## Context and Privacy

The model context should contain only what is needed for the current activity:

- current authorized learner and curriculum identifiers;
- selected concept, objective, and difficulty policy;
- recent feedback summary that is relevant to the activity;
- approved source material and assessment constraints.

Keep raw histories, personally identifiable data, and unrelated conversations out of the prompt. Define retention, deletion, access review, and export policies before collecting learner events.

## Evaluation Gate

Evaluate the whole system, not only generated prose:

1. Curriculum traversal respects prerequisites.
2. Scheduler produces reproducible results for the same event sequence.
3. Learner-state estimates are calibrated on held-out histories.
4. Generated exercises obey the objective and answer schema.
5. Feedback does not disclose protected data or make unsupported claims.
6. Workload and learning outcomes are monitored with an approved study design.

## Gotchas

- **Generated tutoring text is not a student model.** A confident explanation can be wrong about skill level. **Fix:** derive learner state from versioned event transformations and expose confidence/uncertainty.
- **Scheduling in a prompt is non-reproducible.** The same history can yield different review advice. **Fix:** run scheduling as deterministic code and pass the chosen activity to the model.
- **Future data leaks invalidate evaluation.** Randomly splitting chronological interactions lets later performance reveal the answer. **Fix:** split by learner and time boundary before fitting or tuning.
- **Educational data is sensitive.** Rich conversation logs can contain identity, disability, or assessment information. **Fix:** minimize prompt context and enforce explicit retention and access policies.

## Sources

- [Anki manual: FSRS](https://docs.ankiweb.net/deck-options.html#fsrs)
- [FSRS for Anki project](https://github.com/open-spaced-repetition/fsrs4anki)
- [pyKT knowledge-tracing toolkit](https://github.com/pykt-team/pykt-toolkit)

## See Also

- [[agent-memory]]
- [[rag-pipeline]]
- [[embeddings]]
- [[agent-evaluation]]

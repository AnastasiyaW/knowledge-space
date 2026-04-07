---
title: Temporal Memory
category: patterns
tags: [llm-memory, temporal-validity, staleness, contradiction-resolution, time-decay, knowledge-graph]
---

# Temporal Memory

Managing the time dimension of stored knowledge. Facts change - a user's preferred framework in 2024 may not be their preference in 2026. Without temporal awareness, memory systems confidently serve outdated information.

## Key Facts

- Every fact has an implicit or explicit validity period (valid_from / valid_to)
- Most memory systems ignore temporality - all stored facts are treated as equally current
- Temporal knowledge graphs store entity-relationship triples with validity timestamps in SQLite or similar
- Staleness detection requires either explicit expiry dates or heuristic age-based scoring
- Contradictions between facts from different time periods should be resolved in favor of the newer fact
- Domain-specific decay rates vary: tech stack preferences change yearly, personal traits rarely change

## Temporal Knowledge Model

```python
@dataclass
class TemporalFact:
    subject: str          # "user"
    predicate: str        # "prefers_framework"
    object: str           # "FastAPI"
    valid_from: datetime  # when this became true
    valid_to: datetime | None  # null = still valid
    confidence: float     # 0.0-1.0
    source: str           # which conversation/document

# Storage: SQLite table
"""
CREATE TABLE facts (
    id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object TEXT NOT NULL,
    valid_from TEXT NOT NULL,
    valid_to TEXT,
    confidence REAL DEFAULT 1.0,
    source TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_facts_subject ON facts(subject, predicate);
CREATE INDEX idx_facts_valid ON facts(valid_from, valid_to);
"""
```

## Staleness Detection

### Explicit Expiry

Set `valid_to` when the fact is known to expire:

```python
def store_fact(subject, predicate, obj, valid_from, valid_to=None):
    # If a conflicting fact exists, close it
    existing = db.query(
        "SELECT id FROM facts WHERE subject=? AND predicate=? AND valid_to IS NULL",
        (subject, predicate)
    )
    if existing:
        db.execute(
            "UPDATE facts SET valid_to=? WHERE id=?",
            (valid_from, existing[0]["id"])
        )

    db.execute(
        "INSERT INTO facts (subject, predicate, object, valid_from, valid_to) VALUES (?,?,?,?,?)",
        (subject, predicate, obj, valid_from, valid_to)
    )
```

### Heuristic Age-Based Decay

When explicit expiry isn't available, score by age and domain:

```python
DECAY_RATES = {
    "tech_preference": 365,    # days until 50% confidence
    "project_status": 30,      # projects change monthly
    "personal_trait": 3650,    # personality rarely changes
    "api_version": 180,        # APIs update ~twice/year
    "team_member": 730,        # team composition changes over years
    "server_config": 90,       # infra changes quarterly
}

def confidence_at(fact: TemporalFact, now: datetime) -> float:
    age_days = (now - fact.valid_from).days
    half_life = DECAY_RATES.get(fact.predicate, 365)
    return fact.confidence * (0.5 ** (age_days / half_life))
```

### Staleness Signals

Detect when memory needs refresh:

| Signal | Detection | Action |
|--------|-----------|--------|
| Age exceeds half-life | `confidence_at() < 0.5` | Flag for verification |
| Direct contradiction | New fact conflicts with stored | Close old fact, store new |
| Context mismatch | Fact references deleted file/project | Mark as potentially stale |
| User correction | User explicitly corrects a fact | Immediately update |
| External change | Version release, team change | Scan related facts |

## Contradiction Resolution

When two facts conflict, resolution depends on context:

```python
def resolve_contradiction(fact_a: TemporalFact, fact_b: TemporalFact) -> TemporalFact:
    # Rule 1: Newer wins for same subject+predicate
    if fact_a.subject == fact_b.subject and fact_a.predicate == fact_b.predicate:
        return fact_b if fact_b.valid_from > fact_a.valid_from else fact_a

    # Rule 2: Higher confidence wins for same time period
    if overlaps(fact_a, fact_b):
        return fact_a if fact_a.confidence > fact_b.confidence else fact_b

    # Rule 3: More specific wins (user preference > general default)
    if is_more_specific(fact_a, fact_b):
        return fact_a

    # Rule 4: Flag for human resolution
    return flag_for_review(fact_a, fact_b)
```

**Resolution hierarchy:**
1. User's explicit correction always wins
2. Recent observation > old observation
3. Specific > general ("User said X" > "Most users prefer Y")
4. If still ambiguous, ask the user

## Patterns

### Temporal Query

```python
def query_current(subject: str, predicate: str, now: datetime = None) -> list:
    """Get currently valid facts."""
    now = now or datetime.utcnow()
    return db.query("""
        SELECT * FROM facts
        WHERE subject = ? AND predicate = ?
          AND valid_from <= ?
          AND (valid_to IS NULL OR valid_to > ?)
        ORDER BY valid_from DESC
    """, (subject, predicate, now, now))

def query_history(subject: str, predicate: str) -> list:
    """Get full history of a fact, including expired values."""
    return db.query("""
        SELECT * FROM facts
        WHERE subject = ? AND predicate = ?
        ORDER BY valid_from ASC
    """, (subject, predicate))
```

### Temporal Metadata in Vector Store

If using a [[vector-databases]] approach, encode temporal data as metadata for filtering:

```python
vector_store.add(
    documents=[conversation_text],
    metadatas=[{
        "valid_from": "2026-04-08",
        "valid_to": None,
        "domain": "tech_preference",
        "confidence": 0.95
    }]
)

# Query with temporal filter
results = vector_store.query(
    query_texts=["database preference"],
    where={"valid_to": None},  # only current facts
    n_results=5
)
```

### Periodic Validity Scan

```python
def scan_stale_facts(threshold: float = 0.5):
    """Find facts that may be outdated."""
    now = datetime.utcnow()
    all_facts = db.query("SELECT * FROM facts WHERE valid_to IS NULL")
    stale = []
    for fact in all_facts:
        conf = confidence_at(fact, now)
        if conf < threshold:
            stale.append({"fact": fact, "confidence": conf})
    return sorted(stale, key=lambda x: x["confidence"])
```

## Gotchas

- **Most memory systems treat all facts as timeless.** A preference from 2 years ago has the same weight as one from yesterday. Without temporal decay or validity tracking, the agent will confidently use outdated information. Always store timestamps with facts
- **Closing old facts on contradiction requires careful key matching.** "User prefers Python" and "User likes Python for scripting" are different facts with different predicates. Naive deduplication will either miss contradictions (too strict) or incorrectly close valid facts (too loose). Use subject+predicate as the conflict key, not full-text matching
- **Time zones matter for validity periods.** If valid_from is stored in UTC but compared against local time, facts may appear valid or expired incorrectly. Standardize on UTC throughout

## See Also

- [[memory-architectures]]
- [[forgetting-strategies]]
- [[knowledge-base-as-memory]]
- [[session-persistence]]
- [[verbatim-vs-extraction]]

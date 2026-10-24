---
title: "Mémoire temporelle"
category: patterns
tags: [llm-memory, temporal-validity, staleness, contradiction-resolution, time-decay, knowledge-graph]
level: 3
source_sha256: 0bd32ac2d68c282890ac27c145fc2b490e1b7812158af31d42217d96b6768d39
translation: machine
translated_at: '2026-10-24'
---
# Mémoire temporelle {#temporal-memory}

Gérer la dimension temporelle des connaissances stockées. Les faits évoluent : le framework préféré d'un utilisateur en 2024 ne l'est peut-être plus en 2026. Sans conscience temporelle, les systèmes de mémoire servent avec assurance des informations périmées.

## Points clés {#key-facts}

- Chaque fait possède une période de validité implicite ou explicite (valid_from / valid_to)
- La plupart des systèmes de mémoire ignorent la temporalité : tous les faits stockés sont traités comme également actuels
- Les graphes de connaissances temporels stockent des triplets entité-relation accompagnés d'horodatages de validité dans SQLite ou un outil similaire
- La détection d'obsolescence requiert soit des dates d'expiration explicites, soit un scoring heuristique basé sur l'âge
- Les contradictions entre faits issus de périodes différentes doivent être résolues en faveur du fait le plus récent
- Les taux de décroissance varient selon le domaine : les préférences de stack technique changent chaque année, les traits de personnalité changent rarement

## Modèle de connaissances temporel {#temporal-knowledge-model}

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

## Détection d'obsolescence {#staleness-detection}

### Expiration explicite {#explicit-expiry}

Définir `valid_to` lorsque l'on sait qu'un fait expire :

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

### Décroissance heuristique basée sur l'âge {#heuristic-age-based-decay}

Lorsqu'aucune expiration explicite n'est disponible, évaluer selon l'âge et le domaine :

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

### Signaux d'obsolescence {#staleness-signals}

Détecter quand une mémoire doit être rafraîchie :

| Signal | Détection | Action |
|--------|-----------|--------|
| L'âge dépasse la demi-vie | `confidence_at() < 0.5` | Signaler pour vérification |
| Contradiction directe | Un nouveau fait entre en conflit avec un fait stocké | Clôturer l'ancien fait, stocker le nouveau |
| Décalage de contexte | Le fait fait référence à un fichier ou projet supprimé | Marquer comme potentiellement obsolète |
| Correction utilisateur | L'utilisateur corrige explicitement un fait | Mettre à jour immédiatement |
| Changement externe | Sortie d'une version, changement d'équipe | Analyser les faits liés |

## Résolution des contradictions {#contradiction-resolution}

Lorsque deux faits entrent en conflit, la résolution dépend du contexte :

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

**Hiérarchie de résolution :**
1. La correction explicite de l'utilisateur l'emporte toujours
2. Observation récente > observation ancienne
3. Spécifique > général (« L'utilisateur a dit X » > « La plupart des utilisateurs préfèrent Y »)
4. En cas d'ambiguïté persistante, demander à l'utilisateur

## Patterns {#patterns}

### Requête temporelle {#temporal-query}

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

### Métadonnées temporelles dans le vector store {#temporal-metadata-in-vector-store}

Si l'on utilise une approche basée sur des [[vector-databases]], encoder les données temporelles sous forme de métadonnées pour permettre le filtrage :

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

### Analyse périodique de validité {#periodic-validity-scan}

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

## Pièges {#gotchas}

- **La plupart des systèmes de mémoire traitent tous les faits comme intemporels.** Une préférence datant de deux ans a le même poids qu'une préférence d'hier. Sans décroissance temporelle ni suivi de validité, l'agent utilisera avec assurance des informations périmées. Toujours stocker des horodatages avec les faits
- **Clôturer les anciens faits en cas de contradiction exige une correspondance de clés rigoureuse.** « L'utilisateur préfère Python » et « L'utilisateur aime Python pour les scripts » sont deux faits différents, avec des prédicats différents. Une déduplication naïve manquera les contradictions (trop stricte) ou clôturera à tort des faits valides (trop souple). Utiliser sujet+prédicat comme clé de conflit, et non une comparaison du texte intégral
- **Les fuseaux horaires comptent pour les périodes de validité.** Si valid_from est stocké en UTC mais comparé à l'heure locale, les faits peuvent apparaître à tort comme valides ou expirés. Standardiser sur UTC partout

## Voir aussi {#see-also}

- [[memory-architectures]]
- [[forgetting-strategies]]
- [[knowledge-base-as-memory]]
- [[session-persistence]]
- [[verbatim-vs-extraction]]

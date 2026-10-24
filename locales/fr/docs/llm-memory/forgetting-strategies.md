---
title: "Stratégies d'oubli"
category: patterns
tags: [llm-memory, forgetting, compaction, archival, ttl, memory-management, pruning]
level: 3
source_sha256: a8b654f22aacbabbd6e6e11d8138edf4cd5ebb316c005fa1acdeee6df801a0c3
translation: machine
translated_at: '2026-10-24'
---
# Stratégies d'oubli {#forgetting-strategies}

Quand et comment retirer des informations de la mémoire d'un agent LLM. Une croissance non bornée de la mémoire dégrade la qualité de la recherche : les résultats non pertinents diluent les résultats pertinents. Savoir oublier de façon stratégique est aussi important que savoir mémoriser de façon stratégique.

## Points clés {#key-facts}

- Une mémoire sans élagage dégrade la précision de la recherche au fil du temps : plus il y a d'entrées, plus il y a de faux positifs
- « Oublier » signifie généralement archiver (déplacer vers un stockage froid), et non supprimer
- Le coût en tokens croît avec la taille de la mémoire : même si la recherche est rapide, injecter trop de contexte coûte cher
- Le compactage (résumé) est une forme d'oubli avec perte : les détails sont perdus de façon définitive
- La taille optimale de la mémoire dépend de la méthode de recherche : la navigation par index se dégrade à partir d'environ 500 entrées, tandis que la recherche vectorielle se dégrade plus progressivement
- Ne jamais supprimer des données qui n'ont pas d'abord été archivées

## Mécanismes d'oubli {#forgetting-mechanisms}

| Mécanisme | Ce qu'il fait | Réversible | Idéal pour |
|-----------|---------------|------------|------------|
| **TTL (Time-to-Live)** | Expiration automatique après une période fixe | Non (sauf si archivé) | État temporaire, données de session |
| **Scoring de pertinence** | Noter les entrées et élaguer les plus faibles | Oui (si archivé) | Grande mémoire de qualité hétérogène |
| **Compactage** | Résumer et remplacer les détails | Non | Historique de conversation |
| **Archivage** | Déplacer vers un stockage froid | Oui | Données anciennes mais potentiellement utiles |
| **Déduplication** | Fusionner les entrées redondantes | Partiellement | Informations qui se chevauchent |
| **Suppression explicite** | Retirer sur demande de l'utilisateur | Non | Confidentialité, corrections |

## Expiration basée sur le TTL {#ttl-based-expiry}

Attribuez une durée de vie (time-to-live) selon le type d'information :

```python
TTL_CONFIG = {
    "session_state": timedelta(hours=24),       # task-specific, short-lived
    "project_status": timedelta(days=30),        # changes monthly
    "tool_output": timedelta(days=7),            # raw outputs are transient
    "decision": timedelta(days=365),             # decisions have long relevance
    "preference": timedelta(days=730),           # preferences are stable
    "identity": None,                            # never expires
}

def should_expire(entry: MemoryEntry, now: datetime) -> bool:
    ttl = TTL_CONFIG.get(entry.type)
    if ttl is None:
        return False
    return (now - entry.created_at) > ttl
```

**Ne supprimez pas à l'expiration, archivez.** Déplacez les entrées expirées vers un magasin séparé. Si elles sont nécessaires plus tard, elles pourront être récupérées depuis l'archive.

## Scoring de pertinence {#relevance-scoring}

Attribuez à chaque entrée de mémoire un score d'utilité. Facteurs :

```python
def relevance_score(entry: MemoryEntry, now: datetime) -> float:
    # Recency: newer is more relevant
    age_days = (now - entry.created_at).days
    recency = 1.0 / (1 + age_days / 30)  # 30-day half-life

    # Access frequency: more-retrieved is more relevant
    access_freq = min(entry.access_count / 10, 1.0)

    # Freshness: recently accessed is more relevant
    last_access_days = (now - entry.last_accessed).days
    freshness = 1.0 / (1 + last_access_days / 7)

    # Type weight: some types are inherently more valuable
    type_weights = {
        "decision": 1.0,
        "gotcha": 0.9,
        "preference": 0.8,
        "finding": 0.7,
        "observation": 0.5,
        "tool_output": 0.3,
    }
    type_weight = type_weights.get(entry.type, 0.5)

    return (0.3 * recency + 0.3 * access_freq + 0.2 * freshness + 0.2 * type_weight)
```

Élaguez les entrées dont le score est inférieur à un seuil. Valeur suggérée : archivez les entrées dont le score est < 0,2.

## Compactage {#compaction}

Résumé avec perte d'un historique détaillé sous une forme compressée. Voir [[context-window-management]] pour les particularités du compactage des conversations.

```python
def compact_memory_topic(topic: str, entries: list[MemoryEntry]) -> MemoryEntry:
    """Replace multiple entries with one summary."""
    full_text = "\n".join(e.text for e in entries)

    summary = llm.complete(f"""Summarize these {len(entries)} memory entries about '{topic}'.
Preserve: key decisions, current state, gotchas, preferences.
Discard: intermediate steps, superseded information, raw outputs.

{full_text}""")

    return MemoryEntry(
        text=summary,
        type="compacted_summary",
        created_at=max(e.created_at for e in entries),
        metadata={"compacted_from": len(entries), "topic": topic}
    )
```

**Attention :** le compactage est irréversible. Archivez les entrées d'origine avant de compacter.

## Archivage {#archival}

Déplacez les anciennes entrées de la mémoire active vers un stockage froid :

```python
def archive_old_entries(active_store, archive_store, max_age_days: int = 90):
    now = datetime.utcnow()
    to_archive = []

    for entry in active_store.all():
        if should_archive(entry, now, max_age_days):
            to_archive.append(entry)

    for entry in to_archive:
        archive_store.add(entry)
        active_store.remove(entry.id)

    return len(to_archive)

def should_archive(entry: MemoryEntry, now: datetime, max_age: int) -> bool:
    # Don't archive: identity, active decisions, high-relevance entries
    if entry.type in ("identity", "active_decision"):
        return False
    if relevance_score(entry, now) > 0.5:
        return False
    return (now - entry.last_accessed).days > max_age
```

La mémoire active reste rapide et ciblée. L'archive est interrogeable, mais avec une latence plus élevée.

## Déduplication {#deduplication}

Plusieurs conversations produisent souvent des souvenirs qui se chevauchent :

```python
def deduplicate(entries: list[MemoryEntry], similarity_threshold: float = 0.92):
    """Merge near-duplicate entries, keeping the most recent."""
    unique = []
    for entry in sorted(entries, key=lambda e: e.created_at, reverse=True):
        is_dup = False
        for existing in unique:
            sim = cosine_similarity(
                embed(entry.text), embed(existing.text)
            )
            if sim > similarity_threshold:
                # Keep existing (more recent), update metadata
                existing.metadata["also_from"] = entry.id
                is_dup = True
                break
        if not is_dup:
            unique.append(entry)
    return unique
```

## Cibles de taille de la mémoire {#memory-size-targets}

| Type de mémoire | Taille cible | Déclencheur d'élagage |
|-----------------|--------------|-----------------------|
| Identité (L0) | <50 tokens | Ne jamais élaguer |
| Faits critiques (L1) | <200 tokens | Revue manuelle uniquement |
| Mémoire de projet actif | <5K tokens | À la fin du projet |
| Mémoire historique | <50K tokens | Archivage mensuel |
| Archive | Illimitée | Revue annuelle |

## Patrons {#patterns}

### Rétention graduée {#graduated-retention}

```text
0-7 days:   Keep everything (verbatim)
7-30 days:  Keep decisions, gotchas, preferences. Archive raw outputs
30-90 days: Compact findings into summaries. Archive details
90+ days:   Archive to cold storage. Keep only identity + decisions
```

### Préservation déclenchée par l'accès {#access-triggered-preservation}

```python
def on_memory_access(entry_id: str):
    """Every time an entry is retrieved, extend its life."""
    entry = store.get(entry_id)
    entry.last_accessed = datetime.utcnow()
    entry.access_count += 1
    store.update(entry)
    # Frequently accessed entries never get archived
```

## Pièges à éviter {#gotchas}

- **Oublier sans archiver revient à détruire des données.** Archivez toujours avant d'élaguer. Le coût de stockage des anciennes données en stockage froid est négligeable comparé au coût de la perte d'une information qui s'avère nécessaire plus tard
- **Le compactage accumule la perte d'information.** Si vous compactez un résumé déjà compacté, la qualité se dégrade de façon exponentielle. Suivez la profondeur de compactage et ne compactez jamais plus de deux fois. Si la mémoire est encore trop volumineuse après deux compactages, archivez à la place
- **Le seuil de déduplication est délicat à régler.** Trop agressif (similarité > 0,85 = doublon), il fusionne des entrées réellement différentes. Trop conservateur (< 0,95), il laisse subsister de la redondance. Commencez à 0,92 et ajustez selon le taux de faux positifs. Journalisez toujours ce qui a été fusionné pour permettre une revue

## Voir aussi {#see-also}

- [[context-window-management]]
- [[temporal-memory]]
- [[memory-architectures]]
- [[verbatim-vs-extraction]]
- [[session-persistence]]

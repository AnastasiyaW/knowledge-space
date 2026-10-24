---
title: "Architectures de mémoire pour agents LLM"
category: concepts
tags: [llm-memory, memory-systems, hierarchical-memory, graph-memory, vector-stores]
level: 3
source_sha256: 2b3ee9ed507294c95d3653734a7c147def42563d63906b96899d998926a0f82d
translation: machine
translated_at: '2026-10-24'
---
# Architectures de mémoire pour agents LLM {#memory-architectures-for-llm-agents}

Approches structurelles d'organisation des connaissances persistantes pour les agents LLM. L'architecture détermine la qualité de la recherche, le coût de stockage et la capacité de l'agent à raisonner sur les informations stockées.

## Points clés {#key-facts}

- Les LLM sont sans état : toute la mémoire est une infrastructure externe que l'agent lit et écrit
- L'architecture de mémoire contraint directement ce que l'agent peut rappeler et avec quelle précision
- Les fichiers plats simples surpassent les systèmes complexes jusqu'à ~100 articles / ~400K mots
- Au-delà de ce seuil, une recherche structurée (basée sur un index ou sur des vecteurs) devient nécessaire
- Un stockage brut verbatim avec les embeddings par défaut atteint 96,6 % de R@5 sur les benchmarks de mémoire longue, devant les systèmes à extraction (~85 %)
- L'ajout d'un reranking LLM léger porte la recherche à ~100 % pour un coût négligeable (~0,001 $/requête)

## Comparaison des architectures {#architecture-comparison}

| Architecture | Échelle | Coût | Recherche | Maintenance |
|-------------|-------|------|-----------|-------------|
| **Fichiers plats** (markdown) | <100 articles | Minimal | Le LLM navigue via l'index | Manuelle ou assistée par LLM |
| **Graphe hiérarchique** | 100-10K entrées | Faible à moyen | Parcours guidé par les métadonnées | Organisée automatiquement par taxonomie |
| **Magasin vectoriel** (verbatim) | 1K-1M entrées | Moyen | Similarité d'embeddings | Indexée automatiquement à l'ingestion |
| **Graphe de connaissances** (triplets) | Quelconque | Élevé | Requêtes structurées + parcours | Complexe, nécessite une résolution d'entités |
| **Hybride** | Quelconque | Variable | Plusieurs chemins de recherche | La plus complexe, meilleurs résultats |

## Architecture à fichiers plats {#flat-file-architecture}

Fichiers markdown simples avec références croisées et index maintenu. Le LLM navigue en lisant l'index, puis en approfondissant des fichiers précis.

```bash
knowledge/
  index.md          # catalog with summaries (LLM reads first)
  log.md            # append-only operation log
  raw/              # immutable source materials
  wiki/             # LLM-generated structured articles
    concept-a.md
    entity-b.md
```

**Trois opérations :**
1. **Ingestion** - une nouvelle source arrive, le LLM la lit, crée ou met à jour ~10 à 15 pages wiki, puis met à jour l'index
2. **Requête** - le LLM lit l'index, navigue vers les pages pertinentes et synthétise une réponse avec citations
3. **Lint** - contrôle de santé périodique : détection des contradictions, des affirmations obsolètes, des pages orphelines et des références croisées manquantes

**Quand ça fonctionne :** le LLM est le moteur de recherche. Avec de bons résumés dans l'index, il navigue dans ~100 articles sans recherche vectorielle. Les connaissances s'accumulent : écrites une fois, maintenues progressivement, sans être redérivées à chaque requête.

**Quand ça casse :** au-delà de ~500 articles, l'index devient trop volumineux pour la fenêtre de contexte. Il faut alors le découper en index par domaine ou ajouter une recherche.

## Architecture de graphe hiérarchique {#hierarchical-graph-architecture}

Organise la mémoire en une taxonomie navigable, à l'aide de métaphores spatiales :

```text
Wing (person/project)
  └── Room (topic)
       └── Hall (type: facts/events/discoveries/preferences/advice)
            └── Closet (summary)
                 └── Drawer (verbatim text)
```

- Les **liens transversaux** (« tunnels ») relient des salles situées dans différentes ailes
- Les métadonnées dans [[vector-databases]] encodent la hiérarchie, sans base de graphe séparée
- Les [[embeddings]] du texte verbatim dans les drawers assurent la recherche de similarité
- Un graphe de connaissances temporel dans SQLite stocke des triplets entité-relation avec des périodes de validité

**Avantage principal :** la navigation est structurée. L'agent ne parcourt pas l'ensemble de la mémoire : il restreint d'abord par wing, puis par room, puis par hall. Cela réduit les faux positifs et rend la recherche explicable.

## Architecture de magasin vectoriel {#vector-store-architecture}

Stocke des fragments de texte avec des [[embeddings]] et les récupère par similarité sémantique.

```python
# Simplest viable memory
import chromadb

client = chromadb.Client()
collection = client.create_collection("memory")

# Store verbatim
collection.add(
    documents=["User prefers Postgres because of jsonb support and pgvector"],
    ids=["mem_001"],
    metadatas=[{"wing": "user", "room": "preferences", "valid_from": "2026-01-15"}]
)

# Retrieve
results = collection.query(query_texts=["database preference"], n_results=5)
```

**Constat déterminant :** le texte brut verbatim avec les embeddings par défaut surpasse nettement les résumés extraits par LLM. Les systèmes qui extraient des faits du type « l'utilisateur préfère Postgres » perdent le *pourquoi*, et c'est justement le pourquoi qui rend la recherche utile. Voir [[verbatim-vs-extraction]].

## Architecture de graphe de connaissances {#knowledge-graph-architecture}

Triplets entité-relation avec validité temporelle :

```text
(User, prefers, PostgreSQL, valid_from=2026-01, valid_to=null)
(PostgreSQL, supports, pgvector, valid_from=2024-06, valid_to=null)
(User, evaluated, MySQL, valid_from=2025-11, valid_to=2025-12)
```

- Idéal pour raisonner sur les relations (« quels outils préfère l'utilisateur qui supportent la recherche vectorielle ? »)
- Coûteux à maintenir : résolution d'entités, déduplication, suivi de la validité
- Souvent combiné à un magasin vectoriel pour une recherche hybride

## Architecture hybride {#hybrid-architecture}

Les systèmes en production combinent plusieurs approches :

```text
L0: Identity core (flat file, ~50 tokens, always loaded)
L1: Critical facts (flat file, ~120 tokens, always loaded)
L2: Topic-specific memory (vector store, loaded on demand)
L3: Full history (vector store, loaded on explicit request)
```

Voir [[context-window-management]] pour le modèle de chargement en couches.

## Modèles d'usage {#patterns}

### Navigation par index d'abord {#index-first-navigation}

```markdown
# Memory Index

## User Preferences
- database-choice - PostgreSQL, reasons, migration history
- editor-setup - Neovim config, plugins, keybindings

## Project: API Rewrite
- architecture-decisions - REST vs GraphQL, chosen GraphQL
- deployment - K8s on GCP, Terraform managed
```

L'agent lit d'abord cet index, puis n'ouvre que les fichiers dont il a besoin. C'est un chargement de contexte JIT : un minimum de tokens tant que la connaissance précise n'est pas requise.

### Flux d'ingestion {#ingest-workflow}

```bash
Source material arrives
  → LLM reads source (raw/ - immutable)
  → LLM creates/updates wiki pages
  → LLM updates index.md with new entries
  → LLM appends to log.md
  → LLM revisits related pages for cross-references
```

Une source touche généralement 10 à 15 pages wiki. Le LLM assure la tenue des écritures de façon fiable : il ne s'ennuie pas et n'oublie pas de mettre à jour les références croisées.

## Pièges {#gotchas}

- **Les fichiers plats atteignent un plafond vers 400K mots.** L'index lui-même devient trop volumineux pour la fenêtre de contexte. Solution : découper en index spécifiques à chaque domaine, et ajouter une recherche BM25 ou vectorielle optionnelle avec reranking LLM
- **Les bases de graphes ajoutent de la complexité sans bénéfice proportionnel pour la plupart des cas d'usage.** Les champs de métadonnées d'un magasin vectoriel (wing, room, type, valid_from) offrent 80 % de la navigation par graphe pour 20 % de la complexité. N'utiliser une base de graphes dédiée que si l'on a besoin de requêtes de relations multi-sauts
- **Une mémoire sans maintenance se dégrade.** Les faits deviennent obsolètes, les contradictions s'accumulent, des pages orphelines apparaissent. Planifier des passes périodiques de lint et de contrôle de santé : détecter les contradictions, vérifier la validité temporelle, supprimer les liens morts

## Voir aussi {#see-also}

- [[verbatim-vs-extraction]]
- [[context-window-management]]
- [[knowledge-base-as-memory]]
- [[memory-retrieval-patterns]]
- [[agent-memory]]
- [[vector-databases]]

---
title: "Base de connaissances comme mémoire"
category: patterns
tags: [llm-memory, knowledge-base, wiki, markdown, ingest, lint, persistent-knowledge]
level: 3
source_sha256: bfcc86470238e81454d7793cf51556b323dfdbe10318dffac57bbf6dcb5145e8
translation: machine
translated_at: '2026-10-24'
---
# Base de connaissances comme mémoire {#knowledge-base-as-memory}

Utiliser une base de connaissances markdown structurée comme mémoire à long terme de l'agent. L'agent lit, écrit et maintient un ensemble d'articles qui se cumulent au fil du temps : la connaissance est écrite une fois puis maintenue, au lieu d'être re-dérivée à chaque requête.

## Faits clés {#key-facts}

- Les collections markdown simples avec références croisées fonctionnent jusqu'à ~100 articles / ~400K mots sans recherche vectorielle
- Le LLM navigue via des résumés et des fichiers d'index : il n'a pas besoin d'embeddings pour des connaissances de taille modérée
- Une source ingérée → ~10-15 pages wiki touchées (créées ou mises à jour)
- Les bases de connaissances sont des « artefacts persistants et cumulatifs » : contrairement au RAG, elles ne re-dérivent pas les réponses à partir des sources brutes à chaque fois
- Les LLM gèrent bien la tenue de registres : ils ne s'ennuient pas, n'oublient pas de mettre à jour les références croisées, et peuvent modifier 15 fichiers en un seul passage
- Au-delà de ~500 articles, ajouter une recherche BM25/vectorielle optionnelle avec reranking par LLM

## Architecture : Raw -> Wiki -> Schema {#architecture-raw-wiki-schema}

Trois couches, chacune avec un rôle précis :

### raw/ - Sources immuables {#raw-immutable-sources}

```text
raw/
  paper-attention-is-all-you-need.md
  meeting-notes-2026-03-15.md
  api-docs-stripe-v3.md
```

- PDF convertis en markdown, articles web capturés, jeux de données, notes de réunion
- Le LLM lit ces fichiers mais ne les modifie JAMAIS
- Source de vérité pour la vérification et la déduplication

### wiki/ - Connaissances générées par le LLM {#wiki-llm-generated-knowledge}

```text
wiki/
  index.md              # catalog with summaries - agent reads first
  log.md                # append-only chronological operation log
  transformer-architecture.md
  stripe-integration.md
  attention-mechanisms.md
```

- Articles de type encyclopédique pour les concepts et les entités
- Résumés, comparaisons, références croisées via `[[wiki-links]]`
- `index.md` - le point d'entrée de l'agent, mis à jour à chaque ingestion
- `log.md` - registre en ajout seul de toutes les opérations (crée une piste d'audit)

### schema - Configuration {#schema-configuration}

Les instructions opérationnelles de l'agent : structure de la base de connaissances, conventions de nommage, workflows, standards de qualité. Équivalent d'un CLAUDE.md ou du guide de contribution d'un projet.

## Trois opérations {#three-operations}

### 1. Ingestion {#1-ingest}

Une nouvelle source arrive. L'agent :

```bash
1. Read source from raw/
2. Discuss key takeaways (optionally with user)
3. Create/update wiki pages for new concepts and entities
4. Update index.md with new entries and summaries
5. Revisit related pages - add cross-references
6. Append to log.md: what changed and why
```

**Signal de qualité :** une bonne ingestion touche 10 à 15 pages. Si elle ne crée qu'une seule page, l'agent ne fait pas assez de références croisées.

### 2. Requête {#2-query}

L'utilisateur pose une question. L'agent :

```sql
1. Read index.md to locate relevant articles
2. Read specific wiki pages
3. Synthesize answer with citations to wiki pages
4. If the answer is valuable, create a new wiki page from it
```

Pas besoin de recherche vectorielle à cette échelle. L'index est le mécanisme de recherche.

### 3. Lint / Contrôle de santé {#3-lint-health-check}

Passe de maintenance périodique :

```python
# Automated checks (scriptable, deterministic)
checks = [
    "orphan_pages",        # pages not referenced from index or other pages
    "dead_links",          # [[wiki-links]] pointing to non-existent pages
    "missing_cross_refs",  # related pages that don't reference each other
    "stale_claims",        # facts with valid_to in the past
    "empty_sections",      # placeholder sections never filled
    "duplicate_topics",    # multiple pages covering the same concept
]

# LLM-assisted checks (need judgment)
llm_checks = [
    "contradictions",      # page A says X, page B says not-X
    "outdated_info",       # claims that may have changed
    "missing_context",     # pages that assume knowledge not in the KB
]
```

**Exécuter le lint périodiquement** : chaque semaine pour les bases actives, chaque mois pour les bases stables. Sans maintenance, les bases de connaissances accumulent les contradictions et les informations obsolètes.

## Patterns {#patterns}

### Navigation pilotée par l'index {#index-driven-navigation}

```markdown
# Knowledge Base Index

## Architecture (12 articles)
- microservices-patterns - saga, CQRS, event sourcing
- api-design - REST vs GraphQL, versioning, pagination

## Infrastructure (8 articles)
- kubernetes-ops - deployment strategies, HPA, resource limits
- observability - metrics, tracing, alerting stack

Last updated: 2026-04-08 | Total: 87 articles
```

L'agent le lit en premier. ~500 tokens suffisent pour couvrir 100 articles avec un résumé d'une ligne chacun. C'est le mécanisme de récupération le moins coûteux possible.

### Journal des opérations en ajout seul {#append-only-operation-log}

```markdown
# Operations Log

## 2026-04-08 14:30
- **Ingested:** Stripe API v3 migration guide
- **Created:** wiki/stripe-v3-migration.md
- **Updated:** wiki/stripe-integration.md (added v3 breaking changes)
- **Updated:** wiki/payment-processing.md (cross-ref to v3 migration)
- **Updated:** index.md (new entry under Payments)

## 2026-04-07 09:15
- **Query:** "How does our auth flow handle token refresh?"
- **Created:** wiki/auth-token-refresh.md (valuable answer, persisted)
```

Le journal sert de piste d'audit et permet à l'agent de comprendre l'évolution de la base de connaissances.

### Passer au-delà du markdown {#scaling-beyond-markdown}

Quand la base de connaissances dépasse la simple navigation :

| Échelle | Stratégie |
|---------|-----------|
| <100 articles | Navigation par index uniquement |
| 100-500 | Index par domaine + recherche par mots-clés |
| 500-5000 | Ajouter une recherche BM25 avec reranking par LLM |
| 5000+ | [[rag-pipeline]] complet avec [[vector-databases]] |

## Outillage {#tooling}

- **Obsidian** - vue graphe pour visualiser les connexions, plugin Dataview pour les requêtes sur le frontmatter YAML
- **MkDocs Material** - génération de site statique à partir du markdown, recherche intégrée
- **Obsidian Web Clipper** - capturer directement des sources web dans raw/

## Pièges courants {#gotchas}

- **L'index est le goulot d'étranglement.** Si index.md n'est pas maintenu, l'agent ne retrouve plus rien. Traiter la mise à jour de l'index comme obligatoire à chaque ingestion, pas comme facultative. Automatiser si possible
- **« Une page par sujet » ne tient pas pour les sujets complexes.** Une seule page « Kubernetes » grossira sans limite. Découper tôt : k8s-networking, k8s-storage, k8s-rbac. Mieux vaut 10 pages ciblées qu'une seule page tentaculaire
- **Les LLM créent trop de pages lors de l'ingestion.** Sans contraintes, l'agent crée une nouvelle page pour chaque nom rencontré. Fixer un seuil de qualité : une page doit contenir au moins 3 faits substantiels pour justifier son existence

## Voir aussi {#see-also}

- [[memory-architectures]]
- [[memory-retrieval-patterns]]
- [[session-persistence]]
- [[context-window-management]]
- [[rag-pipeline]]

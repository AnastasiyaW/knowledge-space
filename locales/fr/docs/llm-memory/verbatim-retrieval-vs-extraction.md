---
title: "Stockage verbatim vs extraction dans la mémoire des agents"
description: "Pourquoi le stockage verbatim de texte brut surpasse l'extraction par LLM pour la récupération de mémoire des agents - benchmarks, architecture MemPalace, chargement en couches et graphes de connaissances temporels."
level: 3
source_sha256: 1224bf6c6873f4329e8f598bd1a5303b0574b11adbd28329e0114258f112d6e7
translation: machine
translated_at: '2026-10-24'
---
# Stockage verbatim vs extraction dans la mémoire des agents {#verbatim-storage-vs-extraction-in-agent-memory}

Constat contre-intuitif : stocker le texte brut tel quel donne de meilleurs résultats que les résumés extraits par LLM pour la récupération de mémoire des agents. L'extraction est avec pertes : lorsqu'on extrait « l'utilisateur préfère Postgres », on perd le POURQUOI.

## Constat clé {#key-finding}

**Du texte brut verbatim dans ChromaDB avec les embeddings par défaut = 96,6 % de R@5 sur LongMemEval, sans aucun appel LLM.**

Cela dépasse :
- Mem0 : ~85 %
- Zep : ~85 %
- Mastra : 94,87 %

Ces trois systèmes utilisent tous une extraction ou un résumé par LLM. La pénalité est mesurable et cohérente à travers les benchmarks.

Ajouter un reranking léger par LLM (par exemple Haiku à ~0,001 $ par requête) porte la récupération verbatim à 100 % (500/500 sur LongMemEval).

## Pourquoi l'extraction perd de l'information {#why-extraction-loses}

L'extraction compresse le contexte d'une manière qui élimine :
- **Les chaînes de raisonnement** - « l'utilisateur a choisi Postgres parce qu'il avait des réserves sur la licence de MySQL et connaissait déjà Postgres grâce au poste X »
- **Les signaux d'incertitude** - « l'utilisateur a mentionné qu'il voudrait peut-être passer à TimescaleDB plus tard »
- **Les préférences implicites** - le ton, le style, le niveau de détail technique que l'utilisateur préfère

Le fait extrait est correct, mais le contexte environnant qui le rend utile a disparu.

## Architecture MemPalace {#mempalace-architecture}

Structure hiérarchique reprenant la mnémotechnique du palais de la mémoire :

```text
Wings     (person / project context)
  └── Rooms     (topic areas)
        └── Halls   (types: facts / events / discoveries / preferences / advice)
              └── Closets   (summaries)
                    └── Drawers   (verbatim text)

Tunnels = cross-links between rooms from different wings
```

Graphe construit à partir des métadonnées de ChromaDB, sans base de données de graphes externe.  
Relations temporelles suivies dans SQLite : triplets entité-relation avec `valid_from` / `valid_to`.

## Chargement en quatre couches {#four-layer-loading}

```text
L0 (~50 tokens)    identity, persistent identity facts   → ALWAYS loaded
L1 (~120 tokens)   critical facts, active context        → ALWAYS loaded
L2/L3              domain knowledge, full history         → loaded on demand
```

Contexte total toujours chargé : ~170 tokens.  
Comparaison des coûts : ~10 $/an (en couches) contre ~507 $/an (résumé complet).

## Graphe de connaissances temporel {#temporal-knowledge-graph}

Les triplets SQLite avec fenêtres de validité résolvent le problème de l'obsolescence :

```sql
CREATE TABLE facts (
  entity      TEXT,
  relation    TEXT,
  value       TEXT,
  valid_from  TEXT,  -- ISO-8601
  valid_to    TEXT,  -- NULL = currently valid
  source      TEXT   -- message/session this came from
);
```

Lorsqu'un fait change : clôturer l'ancien enregistrement (`valid_to = now`), insérer le nouveau. Interroger les « faits courants » avec `WHERE valid_to IS NULL`.

## Déclencheurs de sauvegarde automatique {#auto-save-triggers}

Une mémoire fiable exige une sauvegarde à des moments prévisibles :
- Tous les N messages (par exemple tous les 15 échanges)
- Avant la compaction du contexte (critique : une fois compacté, le détail est perdu)
- À la fin de la session
- Sur retour explicite de l'utilisateur (« retiens que... » déclenche une sauvegarde immédiate)

## Résolution hybride des entités {#hybrid-entity-resolution}

Avant chaque lot de traitement, construire un index en mémoire de toutes les entités connues :

```python
knowledge_index = {
  "people":         [{"name": "...", "aliases": [...], "file": "..."}],
  "organizations":  [...],
  "projects":       [...],
  "topics":         [...]
}
```

Injecter l'index sous forme de tableau formaté dans le prompt de l'agent. L'agent résout « John Smith » vers la note existante `[[People/John Smith]]` au lieu de créer un doublon.

C'est plus simple que la déduplication par vecteurs et plus précis pour la résolution d'entités nommées.

## Schéma de pipeline de connaissances Rowboat {#rowboat-knowledge-pipeline-pattern}

Pipeline en trois étapes pour une accumulation continue de connaissances :

**Étape 1 : Étiquetage** - classer le contenu entrant (bruit ou signal, sujet, type de relation). Filtrage bruit d'abord : décider ce qu'il faut IGNORER avant de décider ce qu'il faut conserver.

**Étape 2 : Construction du graphe** - extraire les entités, les résoudre vers des noms canoniques via l'index de connaissances, écrire ou mettre à jour les notes avec des wiki-liens bidirectionnels. Suivre l'état des fichiers par `mtime + hash SHA-256` pour éviter de les retraiter.

**Étape 3 : Balisage** - appliquer des étiquettes structurées pour les facettes de récupération (type de relation, sujet, action requise, etc.)

L'état est suivi par fichier afin que la progression partielle survive aux échecs.

## Pièges à éviter {#gotchas}

- **Les affirmations de compression 30x du dialecte AAAK ne sont pas vérifiées.** Une analyse communautaire a relevé des erreurs de comptage de tokens (utilisation de `len(text)//3` au lieu d'un tokenizer réel) et une régression sur LongMemEval : 96,6 % → 84,2 %. Le verbatim l'emporte : n'appliquez pas de compression avec pertes.
- **L'approche verbatim exige un bon pipeline d'embeddings et de reranking.** Les embeddings par défaut donnent 96,6 %, mais l'écart de 3,4 % compte en production. Ajoutez une étape de reranking légère (Haiku/Flash) pour combler l'écart et approcher les 100 %.
- **Les graphes de connaissances temporels exigent de la rigueur dans la gestion de `valid_to`.** Si l'on oublie de clôturer les anciens faits à l'arrivée des nouveaux, les requêtes renvoient des informations contradictoires. Ajoutez une contrainte : une seule fait valide par couple (entité, relation) peut avoir `valid_to IS NULL`.
- **La sauvegarde automatique avant compaction est critique.** Une fois que Claude compacte le contexte, les détails des messages précédents sont compressés. Si la mémoire de session n'a pas été sauvegardée sur disque avant la compaction, cette connaissance est réduite de façon définitive. Accrochez-vous aux événements `PreCompact` ou `Stop`.

## Voir aussi {#see-also}

- [[memory-architectures]]
- [[session-persistence]]
- [[knowledge-graph-memory]]
- [[temporal-memory]]

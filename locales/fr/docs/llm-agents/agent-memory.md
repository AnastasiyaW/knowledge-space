---
title: "Mémoire et état des agents (septembre 2026)"
category: concepts
tags: [llm-agents, memory, state, context-management, persistence, authorization]
level: 3
source_sha256: 8efb020906623767e800af791b840523b4a2c1e8d4dbe186f8255b21fc6a7ee9
translation: machine
translated_at: '2026-10-24'
---
# Mémoire et état des agents (septembre 2026) {#agent-memory-and-state-september-2026}

Revu le 2026-09-03. « Mémoire » désigne plusieurs mécanismes différents. Il faut distinguer l'état d'exécution, la mémoire propre à un utilisateur, les connaissances de l'organisation et le matériel source faisant autorité : ils ont des propriétaires, des règles de conservation, des périmètres d'accès et des modes de défaillance distincts.

## Quatre choses souvent appelées mémoire {#four-things-often-called-memory}

| Type | Périmètre | Contenu typique | Contrôle nécessaire |
|---|---|---|---|
| État d'exécution | Une exécution de workflow | Étapes, reçus d'outils, approbation en attente | Checkpointing et reprise idempotente |
| Contexte de fil | Une conversation ou une tâche | Messages récents et artefacts sélectionnés | Budget de tokens et politique de compaction |
| Mémoire à long terme | Espace de noms utilisateur, agent ou organisation | Préférences, faits, résultats antérieurs | Politique d'écriture, provenance, isolation, expiration |
| Corpus de connaissances | Nombreux utilisateurs/tâches | Documents sources versionnés | Autorité, citations, recherche, politique de publication |

Un historique de conversation n'est pas une base de données, et un magasin vectoriel n'autorise pas à traiter un texte récupéré comme un fait mémorisé.

## Contrat d'enregistrement de mémoire {#memory-record-contract}

```json
{
  "memory_id": "user-193:preference-7",
  "namespace": ["user", "193"],
  "kind": "preference",
  "value": "Prefers concise weekly summaries",
  "source": "explicit-user-statement",
  "written_by": "memory-policy-v2",
  "created_at": "2026-09-03T12:00:00Z",
  "expires_at": null,
  "confidence": "confirmed",
  "access_policy": "user-193-only"
}
```

L'enregistrement doit indiquer pourquoi il a été écrit et qui peut le lire. Ne laissez pas un modèle transformer un texte non fiable quelconque en règle durable ou en mémoire partagée entre utilisateurs sans règle déterministe et frontière de validation.

## Chemin de lecture et d'écriture {#read-and-write-path}

```text
incoming request
    -> authenticate and establish namespace
    -> retrieve only scoped, unexpired records
    -> select a bounded context slice
    -> run the workflow with checkpointed state
    -> propose memory candidates
    -> validate/provenance-check/approve writes
```

LangGraph distingue l'état à portée de fil, persisté par checkpoints, des magasins inter-fils. Sa documentation traite la mémoire à court terme et la mémoire à long terme comme des concepts séparés ; conservez cette distinction même si un autre framework utilise d'autres noms d'API. [Memory overview](https://docs.langchain.com/oss/python/concepts/memory) [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

## La compaction du contexte est une politique {#context-compaction-is-a-policy}

Lorsqu'une conversation s'allonge, choisissez ce qui peut être résumé, abandonné, récupéré à nouveau ou conservé sous forme de champ d'état structuré. Conservez les approbations ouvertes, les reçus d'outils, les engagements visibles par l'utilisateur et les références aux sources faisant autorité. Un résumé en texte libre ne doit pas devenir la seule trace d'une action importante.

## Évaluation {#evaluation}

Testez le système de mémoire avec des scénarios distincts pour :

1. le rappel correct au sein d'un même espace de noms utilisateur ;
2. l'absence de recherche entre utilisateurs, locataires ou permissions révoquées ;
3. l'expiration, la correction et la suppression d'un enregistrement obsolète ;
4. la résistance à l'injection de prompt visant l'écriture en mémoire ;
5. la reprise après interruption à un checkpoint.

Mesurez à la fois le rappel utile et le rappel nuisible. Un système qui retient davantage n'est pas nécessairement meilleur.

## Pièges courants {#gotchas}

- **Problème : écrire une préférence parce qu'une page web non fiable l'affirme.** Un texte externe peut orienter un comportement durable. **Correctif :** limitez les écritures aux déclarations explicites de l'utilisateur ou aux événements applicatifs validés, avec provenance.
- **Problème : partager par défaut un espace de noms commun à l'agent.** Les données d'un utilisateur peuvent influencer un autre workflow. **Correctif :** rendez le périmètre explicite et choisissez par défaut l'espace de noms le plus restreint.
- **Problème : résumer une approbation en attente ou un reçu.** Le workflow perd sa frontière de reprise. **Correctif :** stockez-les comme champs d'état typés, et non uniquement en prose.
- **Problème : traiter une ancienne mémoire comme une source de vérité.** Préférences et faits peuvent changer. **Correctif :** associez un horodatage, une provenance, un niveau de confiance et une politique d'expiration ou de révision.

## Voir aussi {#see-also}

- [[context-engineering]]
- [[agent-architectures]]
- [[production-patterns]]
- [[tokenization]]

## Sources {#sources}

- [LangChain memory overview](https://docs.langchain.com/oss/python/concepts/memory)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph add memory](https://docs.langchain.com/oss/python/langgraph/add-memory)

---
title: "Conception d'un pipeline RAG (septembre 2026)"
category: techniques
tags: [llm-agents, rag, retrieval, grounding, citations, evaluation]
level: 3
source_sha256: 261b8c6bb7f225b53f0af2bff1031287053e86fa789c3e585f1ee1733eb29234
translation: machine
translated_at: '2026-10-24'
---
# Conception d'un pipeline RAG (septembre 2026) {#rag-pipeline-design-september-2026}

Relu le 2026-09-03. La génération augmentée par récupération (RAG, *retrieval-augmented generation*) fournit à une étape de génération des preuves externes sélectionnées au moment de l'exécution. Elle peut améliorer l'accès à des connaissances changeantes ou privées, mais elle ne rend pas automatiquement une réponse factuelle, à jour, autorisée ou correctement citée.

## Le concevoir comme un produit de données {#build-it-as-a-data-product}

```text
authoritative sources
    -> ingest with provenance and access policy
    -> normalize and split into citation-preserving units
    -> embed/index as an immutable generation
    -> retrieve and filter candidates at query time
    -> generate only from allowed evidence
    -> validate citations, outcome, and feedback
```

Chaque flèche est une frontière de publication. Si un document change, le système doit pouvoir identifier les fragments, les embeddings, la génération d'index et les réponses publiées qui sont concernés.

## Enregistrement de la source avant le découpage {#source-record-before-chunking}

| Champ | Rôle |
|---|---|
| Identifiant stable et localisateur | Permet à une réponse de renvoyer vers une source lisible par un humain |
| Révision/horodatage | Distingue les preuves actuelles des contenus remplacés |
| Propriétaire et autorité | Indique si une source peut étayer une affirmation |
| Périmètre d'accès | Empêche la récupération de devenir un contournement des permissions |
| Version du parseur/découpeur | Explique un résultat de récupération modifié |

N'ingérez pas une URL ou un fichier simplement parce qu'il est accessible. Définissez d'abord explicitement sa politique d'autorité, de licence et de fraîcheur.

## Contrat au moment de la requête {#query-time-contract}

1. Classer la requête et son périmètre d'accès.
2. Récupérer les candidats dans la génération d'index nommée.
3. Appliquer les filtres déterministes de métadonnées et d'autorisation avant que le modèle ne voie le contenu.
4. Transmettre les extraits accompagnés de localisateurs stables et des métadonnées de révision.
5. Exiger que la couche de réponse cite ses preuves ou émette un état d'insuffisance explicite.
6. Stocker le reçu de récupération séparément de la prose générée.

```json
{
  "query_id": "q-482",
  "index_generation": "kb-2026-09-03-02",
  "candidates": [
    {"source_id": "policy-14", "revision": "sha256:...", "locator": "policy.md#citations"}
  ],
  "access_policy": "editorial-internal",
  "outcome": "EVIDENCE_SUFFICIENT"
}
```

## Évaluer la récupération séparément {#evaluate-retrieval-separately}

Une réponse peut paraître utile alors que la récupération a échoué. Maintenez un jeu de tests de requêtes avec les identifiants de sources attendus/interdits, la granularité de citation attendue et les frontières d'autorisation pertinentes. Analysez les échecs par catégorie : absence de preuve, mauvais document, révision périmée, section manquante, mauvaise langue, fuite de permissions ou synthèse non étayée.

Les valeurs par défaut des frameworks publics sont des hypothèses, non une évaluation de votre corpus. La taille de fragment, le chevauchement, le retriever et le reranker pertinents dépendent de la structure des documents et des exigences de preuve de la tâche.

## Mise à jour et retour arrière {#update-and-rollback}

Créez une nouvelle génération d'index lorsque vous modifiez le contenu du corpus, les embeddings, le découpage ou la politique de récupération. Validez-la à côté de la génération active, basculez le lecteur de manière atomique et conservez la génération précédente assez longtemps pour enquêter et revenir en arrière. Une réindexation partielle en place est difficile à évaluer et quasiment impossible à expliquer.

## Pièges courants {#gotchas}

- **Problème : considérer le texte récupéré comme automatiquement fiable.** Une source peut être obsolète, injectée ou hors du périmètre d'accès du demandeur. **Correctif :** conservez les métadonnées d'autorité, de révision et d'accès, et filtrez de manière déterministe avant d'envoyer le prompt.
- **Problème : ne tester que les réponses finales.** Les échecs de récupération sont invisibles dès que la prose est fluide. **Correctif :** stockez un reçu de récupération et évaluez-le indépendamment de la qualité de la réponse.
- **Problème : masquer l'absence de preuve.** Le modèle peut combler le vide par un texte plausible. **Correctif :** exposez un résultat `EVIDENCE_INSUFFICIENT` et orientez-le vers une recherche, une demande de clarification ou un humain.
- **Problème : réindexer en place.** Les utilisateurs peuvent recevoir un mélange de preuves anciennes et nouvelles. **Correctif :** publiez des générations d'index immuables et changez atomiquement l'alias du lecteur.

## Voir aussi {#see-also}

- [[embeddings]]
- [[chunking-strategies]]
- [[vector-databases]]
- [[production-patterns]]

## Sources {#sources}

- [Article original sur RAG](https://arxiv.org/abs/2005.11401)
- [Vue d'ensemble de la récupération dans LangChain](https://docs.langchain.com/oss/python/langchain/retrieval)
- [Guide de récupération d'OpenAI](https://developers.openai.com/api/docs/guides/retrieval)

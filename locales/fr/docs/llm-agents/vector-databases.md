---
title: "Bases de données vectorielles et récupération"
description: "Concevoir la récupération vectorielle autour d'embeddings versionnés, de filtres de métadonnées autorisés, de la provenance, de l'évaluation du rappel et d'une migration sûre, plutôt que de classements de produits statiques."
tags: [llm-agents, vector-db, embeddings, retrieval, rag, similarity-search, hybrid-search]
level: 4
source_sha256: 9b019a6c62e781c05d2a7801d70b8e4bdc83ab1b250c540c718ea78ec6e672cc
translation: machine
translated_at: '2026-10-24'
---
# Bases de données vectorielles et récupération (septembre 2026) {#vector-databases-and-retrieval-september-2026}

Contexte de version : les modèles d'embedding, les métriques de distance, les dimensions vectorielles, les algorithmes d'index, la sémantique de filtrage, les API de requêtes hybrides et les limites des services hébergés évoluent indépendamment les uns des autres. Conservez-les dans une configuration de récupération examinée et validez le magasin choisi sur le corpus réel et la charge de travail réelle.

Un magasin vectoriel récupère des candidats dont les représentations vectorielles sont proches de la représentation de la requête. Il ne prouve pas qu'un candidat est factuel, à jour, autorisé ou suffisant pour une réponse générée. La qualité de la récupération est une propriété du workflow : l'ingestion, le filtrage, le classement, la construction du contexte, les citations et l'évaluation comptent tous.

## Commencer par un enregistrement de récupération {#start-with-a-retrieval-record}

Chaque élément indexé nécessite un identifiant stable, une provenance, une révision d'embedding et des métadonnées de politique.

```json
{
  "record_id": "doc:policy-17:chunk-004",
  "source_ref": "repository:policies@4f31...",
  "content_digest": "sha256:...",
  "embedding_revision": "embedder@2026-09-03",
  "vector_space": "semantic-search-v4",
  "metadata": {
    "tenant_id": "tenant-42",
    "classification": "internal",
    "published_at": "2026-08-21T00:00:00Z",
    "language": "en"
  },
  "index_state": "ready"
}
```

La source d'origine reste la référence canonique. L'enregistrement vectoriel est une entrée d'index qui doit pouvoir être reconstruite à partir d'un manifeste de source contrôlé.

## La récupération est un pipeline {#retrieval-is-a-pipeline}

```text
authorized query
  -> policy filter
  -> dense / lexical candidate retrieval
  -> fusion or reranking
  -> context selection with source references
  -> model answer
  -> citation and task validator
```

Un système peut utiliser une récupération dense, une récupération lexicale, un filtrage de métadonnées, un reclassement, ou une combinaison de ces éléments. « Hybride » est un choix de conception, et non une garantie que deux scores peuvent être additionnés en toute sécurité. La documentation actuelle de Qdrant, par exemple, illustre une récupération de candidats dense et épars séparée, suivie d'une requête de fusion définie. [Requêtes hybrides Qdrant](https://qdrant.tech/documentation/search/hybrid-queries/)

## Appliquer l'autorisation avant la réponse {#apply-authorization-before-the-answer}

Traitez les filtres de métadonnées comme une partie du contrat de contrôle d'accès, et non simplement comme une préférence de pertinence. Une requête doit être contrainte par le locataire, la classification, le cycle de vie, la région et toute autre dimension de politique avant que le texte récupéré n'atteigne un modèle.

Validez les deux étapes :

1. **étape des candidats :** aucun enregistrement interdit n'apparaît dans la sortie du récupérateur ;
2. **étape du contexte :** aucun extrait interdit ni aucune référence de source périmée n'atteint le prompt ;
3. **étape de la réponse :** les citations identifient les enregistrements de source retenus et la réponse n'affirme pas un appui qu'elle ne possède pas.

Un refus après génération ne répare pas une fuite de contexte non autorisée.

## Le choix de l'index est un compromis mesuré {#index-choice-is-a-measured-trade-off}

Les index de plus proches voisins approximatifs peuvent réduire le coût de recherche tout en introduisant des compromis entre rappel et latence. La recherche exacte, la quantification, les index en graphe, les index inversés par fichiers et les extensions natives des bases de données font des compromis différents selon l'espace vectoriel et la charge de travail considérés.

Le projet FAISS illustre le cycle de vie de base d'un index : définir une dimension vectorielle fixe, ajouter des vecteurs, puis rechercher les plus proches voisins. Certains types d'index nécessitent aussi un entraînement avant utilisation. [Premiers pas avec FAISS](https://github.com/facebookresearch/faiss/wiki/Getting-started)

Ne choisissez une implémentation qu'après avoir mesuré :

| Exigence | Preuves à collecter |
|---|---|
| Qualité de la récupération | rappel ou taux de réussite de la tâche sur un jeu de requêtes examiné |
| Latence et capacité | latence de queue, concurrence, mémoire et temps de construction |
| Filtrage | exactitude de l'autorisation dans des cas adverses de locataire/classification |
| Durabilité | sauvegarde, restauration et reçu de reconstruction à partir du manifeste de source |
| Exploitation | mise à niveau, observabilité, reprise après incident et responsabilité |
| Coût | coûts actuels de stockage, de requête, de réplication et d'exploitation |

## Embarquer et reconstruire de façon idempotente {#embed-and-rebuild-idempotently}

Un worker d'ingestion sûr doit :

1. lire une source versionnée ;
2. normaliser et découper selon une politique de découpage consignée ;
3. calculer un condensat du contenu et une révision d'embedding ;
4. écrire à partir d'un identifiant d'enregistrement déterministe ou d'une clé d'idempotence ;
5. confirmer l'état de l'index et le nombre d'enregistrements par rapport au manifeste ;
6. écrire un reçu dans lequel les échecs sont classés pour nouvelle tentative ou examen.

Ne vous fiez pas à une réponse réussie de `upsert` comme preuve que l'ensemble du corpus est interrogeable et autorisé.

## Migrer les embeddings avec précision {#migrate-embeddings-deliberately}

Un nouveau modèle d'embedding, une nouvelle dimension, une nouvelle règle de normalisation ou une nouvelle métrique de distance définit un nouvel espace vectoriel. Une stratégie de découpage modifiée change la représentation du corpus et le schéma de l'index ; elle exige tout de même une réindexation contrôlée et une évaluation, même lorsque l'encodeur et l'espace vectoriel restent compatibles. Privilégiez une collection ou un espace de noms distinct, ainsi qu'une migration contrôlée en lecture ou en écriture double :

```text
baseline index + evaluation -> candidate index + same evaluation
  -> bounded traffic comparison -> promote or roll back
```

Ne mélangez pas silencieusement des espaces vectoriels incompatibles. Conservez une modification de découpage dans une version d'index évaluée séparément, car l'identité des enregistrements, la couverture des sources et le comportement de récupération peuvent changer même lorsque les dimensions vectorielles ne changent pas.

## Pièges courants {#gotchas}

- **Le plus proche n'est pas forcément vrai.** La recherche de similarité produit des candidats, non des preuves pour une réponse. **Correctif :** conservez les sources, reclassez si nécessaire et validez la couverture des citations.
- **Le filtrage de métadonnées est une surface de contrôle d'accès.** Un filtre de locataire manquant peut exposer les données d'un autre client. **Correctif :** rendez les filtres de politique obligatoires et testez-les avant la construction du contexte du modèle.
- **Un changement d'embedding est un changement de schéma.** Des espaces vectoriels différents ne peuvent pas être comparés ou mélangés en toute sécurité par intuition. **Correctif :** versionnez l'embedding et migrez via des index distincts et évalués.
- **Le succès de l'index ne garantit pas la complétude du corpus.** Une ingestion partielle, des fragments périmés et des suppressions échouées peuvent rester invisibles. **Correctif :** réconciliez les nombres et les condensats avec un manifeste de source.
- **Les scores hybrides exigent une méthode définie.** Les signaux denses et lexicaux n'ont pas les mêmes échelles. **Correctif :** choisissez et évaluez une stratégie de fusion ou de reclassement plutôt que d'additionner des scores bruts.
- **Un index vectoriel n'est pas une sauvegarde.** C'est une dérivée reconstructible. **Correctif :** protégez le corpus source et conservez les reçus de reconstruction de l'index.

## Sources {#sources}

- [Requêtes hybrides Qdrant](https://qdrant.tech/documentation/search/hybrid-queries/)
- [Premiers pas avec FAISS](https://github.com/facebookresearch/faiss/wiki/Getting-started)
- [Projet pgvector](https://github.com/pgvector/pgvector)

## Voir aussi {#see-also}

- [[embeddings]]
- [[rag-pipeline]]
- [[chunking-strategies]]
- [[tokenization]]
- [[llmops]]
- [[agent-security]]

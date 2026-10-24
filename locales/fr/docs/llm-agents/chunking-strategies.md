---
title: "Stratégies de découpage pour la recherche (septembre 2026)"
category: techniques
tags: [llm-agents, chunking, retrieval, rag, document-processing]
level: 3
source_sha256: 5f7a98f6bca65a5c1f0da7036ec5cb93987301816aa00d80e4cd91ae2fb9b0d9
translation: machine
translated_at: '2026-10-24'
---
# Stratégies de découpage pour la recherche (septembre 2026) {#chunking-strategies-for-retrieval-september-2026}

Relu le 2026-09-03. Le découpage (chunking) crée les unités de recherche d'un corpus documentaire. Il n'existe pas de taille de chunk universellement optimale : une stratégie utile préserve les preuves et les métadonnées tout en optimisant la recherche et la qualité des réponses sur un jeu d'évaluation réel.

## Partir du contrat de recherche {#start-from-the-retrieval-contract}

| Question | Implication pour la conception |
|---|---|
| Que doit citer la réponse ? | Conserver la source, la version, la page/section et un localisateur stable |
| Que demande l'utilisateur ? | Choisir une unité contenant assez de preuves pour y répondre |
| Quelle structure existe ? | Privilégier les titres, enregistrements, tableaux et frontières sémantiques |
| Quel modèle consomme le résultat ? | Mesurer le budget de tokens avec le tokenizer exact |
| Comment les documents sont-ils mis à jour ? | Garder l'identité/version des chunks suffisamment stable pour supprimer et réindexer |

LangChain décrit la recherche comme un pipeline modulaire de loaders, text splitters, embeddings, vector stores et retrievers. Un splitter n'est qu'un composant, pas l'ensemble du dispositif de qualité. [LangChain retrieval](https://docs.langchain.com/oss/python/langchain/retrieval)

## Stratégies {#strategies}

| Stratégie | À utiliser quand | Risque principal |
|---|---|---|
| Consciente de la structure | Les titres, enregistrements et paragraphes portent du sens | Une structure d'entrée cassée produit de mauvaises frontières |
| Bornée en tokens | La limite de contexte en aval est stricte | Décalage entre tokenizer et version |
| Parent-enfant | Les petites unités recherchent avec précision, les grandes répondent mieux | Complexité du lien parent et du stockage |
| Consciente des tableaux/enregistrements | Les faits se trouvent dans des lignes ou des champs | L'aplatissement fait perdre les relations |
| Frontière sémantique | Les sections cohérentes comptent plus qu'une longueur fixe | Une heuristique de frontière peut être incohérente |

Ne utilisez le chevauchement (overlap) que lorsqu'il résout un problème de perte à la frontière, établi par évaluation. Le chevauchement augmente la taille de l'index, la duplication lors de la recherche et le coût des prompts.

## Splitter conscient de la structure {#structure-aware-splitter}

Cet exemple Python utilise le package autonome actuel text-splitters de LangChain. Il crée des chunks bornés en privilégiant les frontières de paragraphes et de lignes.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=80,
    separators=["\n\n", "\n", ". ", " ", ""],
)

chunks = splitter.split_text(
    "Heading\n\nFirst paragraph with evidence.\n\nSecond paragraph with context."
)
print(chunks)
```

Traitez les valeurs numériques comme une base de référence pour l'évaluation, et non comme une valeur par défaut adaptée à tous les corpus.

## Contrat de métadonnées {#metadata-contract}

```json
{
  "chunk_id": "policy-2026-09:section-4:chunk-02",
  "document_id": "policy-2026-09",
  "document_version": "sha256:...",
  "source_locator": {"section": "4", "page": 12},
  "parent_id": "policy-2026-09:section-4",
  "text": "..."
}
```

Les métadonnées doivent survivre à la recherche et parvenir au générateur de réponses. Si la réponse finale ne peut pas identifier quelle version et quelle section étayent une affirmation, le pipeline de recherche ne peut pas fournir de citation fiable.

## Évaluation {#evaluation}

Évaluez l'ensemble du chemin, et non seulement la similarité des embeddings :

1. Créez des questions représentatives, avec les sources acceptées et les contraintes attendues sur la réponse.
2. Mesurez si l'ensemble récupéré contient des preuves suffisantes.
3. Mesurez la justesse de la réponse et la précision des citations après génération.
4. Analysez les échecs : extraction, segmentation, embedding, classement, assemblage du contexte ou usage du modèle.
5. Réindexez sous une nouvelle identité de document/version après une modification substantielle du splitter.

## Pièges {#gotchas}

- **Problème : aplatir les tableaux en prose sans étiquettes.** Les relations ligne/colonne disparaissent avant la recherche. **Correctif :** conserver les champs structurés ou rendre une représentation stable et étiquetée avec un localisateur de source.
- **Problème : utiliser le nombre de caractères pour un modèle limité en tokens.** Un chunk peut dépasser la limite après mise en forme ou tokenisation multilingue. **Correctif :** mesurer le contexte final assemblé avec le tokenizer du déploiement.
- **Problème : indexer les doublons créés par le chevauchement.** La recherche peut renvoyer des chunks quasi identiques et masquer des preuves variées. **Correctif :** dédupliquer ou diversifier les résultats, et justifier le chevauchement par des données d'évaluation.
- **Problème : réindexer sans version de document.** Les anciens chunks peuvent rester accessibles après une modification de la source. **Correctif :** rattacher chaque chunk à une version de document immuable, et supprimer ou filtrer les versions remplacées.

## Voir aussi {#see-also}

- [[rag-pipeline]]
- [[embeddings]]
- [[tokenization]]
- [[vector-databases]]
- [[production-patterns]]

## Sources {#sources}

- [Vue d'ensemble de la recherche LangChain](https://docs.langchain.com/oss/python/langchain/retrieval)
- [Text splitters LangChain](https://docs.langchain.com/oss/python/integrations/splitters)

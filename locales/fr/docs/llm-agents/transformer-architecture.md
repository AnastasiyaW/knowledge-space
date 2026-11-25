---
title: "Architecture des transformeurs"
description: "Un guide pratique, sensible aux versions, sur la structure des transformeurs fondés sur l'attention, le décodage autorégressif, l'information positionnelle et les limites de configuration en production."
tags: [llm-agents, transformers, attention, deep-learning, architecture, inference]
level: 5
source_sha256: 8fc965ee099315ace179198deee48708dd6d86bd3ca3f7ac1d1e687fc6cb470f
translation: machine
translated_at: '2026-10-24'
---
# Architecture des transformeurs (septembre 2026) {#transformer-architecture-september-2026}

Contexte de version : les familles de transformeurs, les encodages positionnels, les noyaux d'attention, le comportement des tokenizers, les limites de contexte et les implémentations de cache varient selon chaque version de modèle. Cette page explique des idées architecturales stables ; elle n'affirme pas de manière définitive le fonctionnement interne ni le contexte maximal d'un modèle particulier.

L'article fondateur de 2017 sur le Transformer a introduit une architecture de transduction de séquences fondée sur l'attention plutôt que sur la récurrence ou la convolution. La conception d'origine utilise une structure encodeur-décodeur, reliée par un mécanisme d'attention. [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

## Le calcul de base {#the-core-computation}

Un transformeur traite des représentations de tokens. Pour une couche d'attention, des projections apprises dérivent des requêtes (`Q`), des clés (`K`) et des valeurs (`V`) à partir de ces représentations :

```text
Attention(Q, K, V) = softmax((Q × Kᵀ) / sqrt(d_k)) × V
```

Pour chaque position de requête, les poids d'attention sélectionnent et combinent les vecteurs de valeurs issus des positions de clés autorisées. La disposition exacte des projections, le nombre de têtes, l'ordre de normalisation, la fonction d'activation et le noyau numérique sont des choix d'implémentation propres à chaque modèle.

L'attention multi-têtes exécute plusieurs projections d'attention en parallèle, puis combine leurs résultats. Elle donne à une couche plusieurs sous-espaces de représentation ; il ne s'agit pas d'une liste littérale de « sujets » indépendants et lisibles par un humain.

## Trois familles architecturales courantes {#three-common-architectural-families}

| Famille | Schéma d'attention | Rôle typique en sortie | Limite importante |
|---|---|---|---|
| Encodeur seul | les tokens se rapportent à l'ensemble de l'entrée autorisée | représentations contextuelles | ne peut pas être supposé générer une réponse autorégressive |
| Décodeur seul | chaque token est masqué vis-à-vis des tokens futurs | génération du token suivant | l'inférence produit les tokens séquentiellement |
| Encodeur-décodeur | auto-attention du décodeur plus attention croisée vers l'entrée encodée | génération conditionnelle | la représentation source et la séquence générée ont des rôles différents |

Ce sont des schémas, et non un classement de produits. Le bon choix dépend de l'objectif d'entraînement, du contrat du modèle déployé, du comportement des outils et des résultats d'évaluation.

## Ordre, masques et position {#order-masks-and-position}

L'attention seule ne confère pas intrinsèquement un ordre aux positions d'une séquence. Un transformeur ajoute donc ou représente autrement l'information positionnelle. L'article d'origine utilise des encodages positionnels ; les familles de modèles plus récentes emploient d'autres mécanismes de position. Considérez le schéma positionnel comme une partie de la configuration résolue du modèle.

Les masques définissent quelles positions peuvent porter attention à quelles autres :

- **masque causal :** empêche une position du décodeur de lire les tokens futurs déjà générés ;
- **masque de remplissage ou d'attention :** empêche les positions invalides ou absentes de contribuer ;
- **masque d'attention croisée :** restreint les positions source que le décodeur peut consulter.

Un masque erroné peut produire un système qui semble fonctionner dans une démonstration tout en divulguant des étiquettes futures pendant l'évaluation, ou en mélangeant des enregistrements au sein d'un lot.

## L'entraînement et la génération autorégressive diffèrent {#training-and-autoregressive-generation-differ}

Pendant l'entraînement, les implémentations peuvent souvent évaluer de nombreuses positions de séquence en parallèle, sous réserve du masque du modèle. Pendant la génération de type décodeur, le token `t + 1` dépend de l'état obtenu après le token `t` : chaque nouveau token fait donc avancer l'état de la requête.

Les implémentations d'inférence peuvent conserver dans un cache les projections de clés/valeurs antérieures, afin d'éviter de recalculer tout le préfixe. Le cache est une optimisation soumise à une exigence stricte d'isolation : il doit être lié à la requête, à la révision du modèle et de sa configuration, ainsi qu'à la frontière de locataire ou de données applicable. Ne déduisez pas le comportement ou la capacité du cache à partir du nom d'un modèle. [Guide Hugging Face sur le cache KV](https://huggingface.co/docs/transformers/main/en/kv_cache)

## Un contrat de modèle pratique {#a-practical-model-contract}

Une application doit consigner la configuration, visible par le transformeur, qui modifie le comportement :

```json
{
  "model_key": "approved-generation-model",
  "resolved_model_revision": "observed-at-runtime",
  "tokenizer_revision": "recorded-at-deploy",
  "context_policy_revision": "context@8",
  "attention_or_position_config": "provider-or-local-reference",
  "inference_cache_policy": "per-request-v2",
  "output_contract": "answer-with-citations/v3"
}
```

Ceci est plus utile pour la reproductibilité qu'une formule en prose du type « utilise un transformeur ». Un alias de modèle peut masquer un tokenizer modifié, un comportement de contexte différent ou une autre implémentation de noyau.

## Le travail de performance est un problème d'évaluation {#performance-work-is-an-evaluation-problem}

Le coût de l'attention, l'usage mémoire, le regroupement en lots, la quantification et la stratégie de cache peuvent affecter la latence comme la qualité. N'optimisez qu'avec une charge de travail représentative et une suite d'acceptation au niveau de la tâche.

Mesurez :

- la latence de la requête et celle de la génération de tokens, séparément ;
- la mémoire de pointe et la concurrence sous le mélange de contextes visé ;
- la qualité de la tâche, la couverture des citations et la validité des sorties structurées ;
- les taux d'erreur, de dépassement de délai et de nouvelle tentative ;
- les signaux de succès ou de réutilisation du cache, uniquement lorsque l'environnement d'exécution les expose ;
- le comportement d'isolation et d'annulation lors de requêtes concurrentes.

La documentation de `MultiheadAttention` de PyTorch constitue une référence d'implémentation utile, mais une primitive de framework ne définit pas l'architecture de chaque modèle déployé. [PyTorch MultiheadAttention](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

## Pièges {#gotchas}

- **« Transformeur parallèle » ne signifie pas génération de réponse en parallèle.** La génération de type décodeur avance toujours d'un token suivant à la fois. **Correctif :** mesurez la latence de bout en bout sur le flux de travail déployé, et pas seulement un noyau de type entraînement.
- **Un masque est une frontière de correction.** Un masque inversé ou absent peut laisser fuir un contexte futur ou non lié. **Correctif :** testez les masques avec des cas adverses et des cas inter-enregistrements.
- **La position d'un token n'est pas un décalage de caractères.** La tokenisation, la troncature et le traitement positionnel peuvent modifier ce que le modèle reçoit réellement. **Correctif :** consignez les révisions du tokenizer et de la politique de contexte avec la version.
- **Les caches KV ne sont pas une mémoire partagée.** Un cache trop largement indexé peut franchir les frontières entre requêtes ou entre politiques. **Correctif :** limitez la réutilisation à la configuration exacte approuvée et à la frontière d'identité.
- **Les poids d'attention ne constituent pas une preuve d'explication.** Ce sont des calculs du modèle, et non une piste d'audit causale d'une décision métier. **Correctif :** conservez les citations sources, les validateurs et des reçus de décision explicites.

## Sources {#sources}

- [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [PyTorch MultiheadAttention](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
- [Guide Hugging Face sur le cache KV](https://huggingface.co/docs/transformers/main/en/kv_cache)

## Voir aussi {#see-also}

- [[tokenization]]
- [[kv-cache-compression]]
- [[llm-api-integration]]
- [[context-engineering]]
- [[model-optimization]]
- [[scaling-laws-and-benchmarks]]

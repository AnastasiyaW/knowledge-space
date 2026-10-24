---
title: "Systèmes de recommandation"
category: techniques
tags: [data-science, ml, recommendations, collaborative-filtering, ranking]
level: 2
source_sha256: 5789620a610091e73e84a8e05e94b7093ad7aed0bf8d6d408faf4ccb09dbed2c
translation: machine
translated_at: '2026-10-24'
---
# Systèmes de recommandation {#recommender-systems}

Prédire les préférences des utilisateurs et classer les éléments. Des approches simples de filtrage collaboratif jusqu'aux approches par apprentissage profond. Évalués différemment de la classification et de la régression standard.

## Approches {#approaches}

### Filtrage collaboratif {#collaborative-filtering}
Fondé sur les schémas de comportement des utilisateurs. « Les utilisateurs qui ont aimé X ont aussi aimé Y. »

**Basé sur les utilisateurs** : trouver des utilisateurs similaires et recommander ce qu'ils ont aimé.
**Basé sur les éléments** : trouver des éléments similaires à ceux que l'utilisateur a déjà aimés.

**Factorisation matricielle** : décomposer la matrice d'interactions utilisateur-élément en facteurs latents.
```yaml
R ~ U * V^T
R: user-item matrix (sparse)
U: user latent factors (n_users x k)
V: item latent factors (n_items x k)
```

### Basé sur le contenu {#content-based}
Recommander des éléments similaires à ceux avec lesquels l'utilisateur a déjà interagi, en fonction des caractéristiques des éléments (genre, description, étiquettes).

### Hybride {#hybrid}
Combiner le filtrage collaboratif et le filtrage basé sur le contenu. La plupart des systèmes en production utilisent des approches hybrides.

## Évaluation {#evaluation}

### Métriques hors ligne {#offline-metrics}

| Métrique | Description |
|--------|-------------|
| precision@k | Fraction des éléments pertinents parmi les k premières recommandations |
| recall@k | Fraction de l'ensemble des éléments pertinents trouvés dans les k premières recommandations |
| mAP@k | Précision moyenne (mean average precision) calculée sur l'ensemble des utilisateurs |
| nDCG@k | Pertinence pondérée par la position |
| Hit Rate | Fraction des utilisateurs ayant reçu au moins une recommandation pertinente |

**Formule de nDCG :**
DCG@k = sum_i (2^relevance_i - 1) / log2(i + 1)
nDCG = DCG / ideal_DCG

### Métriques en ligne (test A/B) {#online-metrics-ab-test}
- CTR (taux de clics)
- Durée de session
- Éléments consommés
- Rétention (retour le lendemain ?)
- Revenu par utilisateur

### Pipeline d'évaluation {#evaluation-pipeline}
1. **Hors ligne** : découpage apprentissage/test, calcul des métriques de classement
2. **Test A/B** : déploiement sur un sous-ensemble d'utilisateurs, mesure des métriques métier
3. **Analyse** : vérifier la validité du découpage par groupes, calculer le hitrate

**Piège** : les journaux de recommandations et les journaux de clics se trouvent dans des tables séparées. La jointure nécessite un appariement par proximité temporelle (clics à moins d'environ une heure, avec user_id et item_id correspondants).

## Problème du démarrage à froid {#cold-start-problem}

- **Nouvel utilisateur** : aucun historique d'interactions. Utiliser : éléments populaires, approche démographique, approche basée sur le contenu
- **Nouvel élément** : aucune interaction utilisateur. Utiliser : caractéristiques de contenu, similarité des métadonnées

## Retour implicite vs explicite {#implicit-vs-explicit-feedback}

- **Explicite** : notes, mentions « j'aime » (rares, biaisées vers les opinions tranchées)
- **Implicite** : clics, vues, achats, temps passé (abondants, bruités)

La plupart des systèmes réels utilisent un retour implicite. Interpréter « absence d'interaction » avec prudence : ce n'est pas nécessairement un signal négatif.

## Pièges {#gotchas}
- Les métriques hors ligne ne sont pas toujours corrélées aux métriques métier en ligne : toujours passer par un test A/B
- Biais de popularité : il est facile de recommander les éléments populaires, difficile de faire émerger la longue traîne
- Bulles de filtre : sans injection de diversité, les recommandations deviennent de plus en plus étroites
- L'évaluation avec un retour implicite est délicate : une donnée manquante n'équivaut pas à une préférence négative

## Voir aussi {#see-also}
- [[model-evaluation]] - cadre général des métriques
- [[unsupervised-learning]] - factorisation matricielle, SVD
- [[hypothesis-testing]] - tests A/B sur les recommandations
- [[math-linear-algebra]] - SVD pour la factorisation matricielle

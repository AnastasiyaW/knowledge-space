---
title: "Tests d'hypothèses et tests A/B"
category: concepts
tags: [data-science, statistics, ab-testing, experimentation]
level: 3
source_sha256: 1a9579c045ca3d920c02a38003c9387cad49f269ecdbfbc05010f7515334fb96
translation: machine
translated_at: '2026-10-24'
---
# Tests d'hypothèses et tests A/B {#hypothesis-testing-and-ab-testing}

Cadre statistique pour prendre des décisions à partir de données. Les tests A/B appliquent ces principes aux expériences contrôlées. Compétence essentielle pour les data scientists qui doivent distinguer les effets réels du bruit.

## Cadre des tests d'hypothèses {#hypothesis-testing-framework}

1. **Formuler les hypothèses** : H0 (nulle, aucun effet) et H1 (alternative, il existe un effet)
2. **Choisir le niveau de significativité** alpha (généralement 0,05)
3. **Calculer la statistique de test** à partir des données
4. **Calculer la p-value** ou comparer à la valeur critique
5. **Décision** : rejeter H0 si la p-value < alpha

### Types d'erreurs {#error-types}

| | H0 vraie | H0 fausse |
|--|---------|----------|
| **Rejeter H0** | Erreur de type I (alpha) | Correct |
| **Ne pas rejeter** | Correct | Erreur de type II (bêta) |

- **Erreur de type I** (faux positif) : déclarer un effet alors qu'il n'en existe aucun. Contrôlée par alpha
- **Erreur de type II** (faux négatif) : manquer un effet réel. Puissance = 1 - bêta
- **p-value** : probabilité d'observer des données aussi extrêmes que les nôtres, en supposant H0 vraie

### Tests courants {#common-tests}

| Test | Cas d'usage | Hypothèses |
|------|-------------|------------|
| t-test (de Student) | Comparer les moyennes de deux groupes | ~Normalité, variances similaires |
| t-test de Welch | Comparer les moyennes, variances inégales | ~Normalité |
| Mann-Whitney U | Comparer des distributions de manière non paramétrique | Ordinal ou plus |
| z-test pour proportions | Comparer des proportions binaires | Grand n |
| Chi-deux | Tester l'indépendance de variables catégorielles | Effectif attendu >= 5 |
| ANOVA | Comparer les moyennes de 3 groupes ou plus | Normalité, variances égales |

### Intervalles de confiance {#confidence-intervals}

```python
from scipy import stats
import numpy as np

data = np.array([...])
confidence = 0.95
n = len(data)
mean = data.mean()
se = stats.sem(data)  # standard error
ci = stats.t.interval(confidence, df=n-1, loc=mean, scale=se)
```

Pour une moyenne à variance connue : x_bar +/- z_(alpha/2) * sigma / sqrt(n)
Pour une moyenne à variance inconnue : x_bar +/- t_(alpha/2, n-1) * s / sqrt(n)

## Tests A/B {#ab-testing}

Comparer deux versions (A = contrôle, B = test) sur des groupes d'utilisateurs indépendants. Mesurer des métriques métier.

### Pourquoi ne pas se limiter aux métriques hors ligne ? {#why-not-just-offline-metrics}

Les métriques hors ligne des modèles (précision, NDCG) ne mesurent pas directement l'impact métier. Les entreprises s'intéressent à : durée de session, clics, conversions, rétention, chiffre d'affaires. Les tests A/B relient les modifications des modèles au comportement réel des utilisateurs.

### Conception expérimentale {#experimental-design}

1. **Répartir les utilisateurs** entre groupes contrôle et test (par hachage : `hash(user_id + salt) % 100`)
2. **Exécuter sur une période fixe** (ne pas regarder les résultats en cours et arrêter tôt)
3. **Comparer les métriques** entre les groupes
4. **Appliquer des tests statistiques** pour la significativité

### Puissance du test {#test-power}

Puissance = probabilité de détecter un effet réel. Influencée par :
- **Taille de l'échantillon** : plus d'utilisateurs = plus de puissance (levier principal)
- **Taille de l'effet** : les effets plus importants sont plus faciles à détecter
- **Variance** : une variance plus faible = plus de puissance (utiliser CUPED)
- **Niveau de significativité** : un alpha plus élevé = plus de puissance mais plus de faux positifs

### CUPED (Controlled-experiment Using Pre-Experiment Data) {#cuped-controlled-experiment-using-pre-experiment-data}

Réduit la variance de la métrique de 20 à 30 % à l'aide des données collectées avant l'expérience.

```toml
Y_cuped = Y - theta * X
theta* = cov(Y, X) / Var(X)
Var(Y_cuped) = Var(Y) * (1 - rho^2(Y, X))
```

Plus la corrélation entre la métrique avant et pendant l'expérience est élevée, plus la réduction de variance est importante.

### Mesurer le CTR {#measuring-ctr}

CTR = clics / vues. Problème : les clics individuels ne sont pas indépendants (un même utilisateur en génère plusieurs).

**Solutions :**
- **Agrégation par utilisateur** : agréger les clics par utilisateur, puis appliquer un t-test
- **Bootstrap** : rééchantillonner les utilisateurs avec remise, calculer le CTR pour chaque échantillon
- **Bucketing** : répartir les utilisateurs dans environ 100 buckets, calculer le CTR par bucket, appliquer un t-test sur les buckets
- **Linéarisation** : CTR linéarisé = clics - A * vues (A = CTR global du groupe contrôle)

### Menaces pour la validité {#threats-to-validity}

- **Effet de nouveauté** : les nouveaux utilisateurs réagissent excessivement de manière positive. Gonfle les résultats
- **Aversion au changement** : les utilisateurs expérimentés résistent aux changements. Augmente les faux négatifs
- **Détection** : comparer l'effet entre nouveaux et anciens utilisateurs
- **SRM** (Sample Ratio Mismatch, décalage du ratio d'échantillonnage) : les groupes n'ont pas la même taille, ce qui indique une randomisation défaillante

### Cas où les tests A/B sont impossibles {#when-ab-tests-are-impossible}

- **Marchés bifaces** (taxi, livraison) : agir sur un côté affecte l'autre
- **Fonctionnalités visibles** : les utilisateurs de différents groupes voient l'expérience des autres
- **Fonctionnalité déjà en production** : impossible de réaliser un test inverse

**Alternatives :**
- **Tests switchback** : alterner les algorithmes selon des créneaux géographiques et temporels
- **Contrôle synthétique** : déployer partout, comparer à une référence prédite à partir des régions de contrôle
- **Différence de différences** (Difference-in-Differences) : comparer traitement et contrôle avant et après l'intervention
- **Appariement par score de propension** (Propensity Score Matching) : apparier les unités traitées à des unités de contrôle similaires

## Méthodes d'inférence causale {#causal-inference-methods}

| Méthode | Force | Cas d'usage |
|---------|-------|-------------|
| A/B randomisé | Référence | Contrôle total de l'affectation |
| DiD | Modérée | Randomisation impossible, données avant/après disponibles |
| PSM | Modérée | Randomisation impossible, covariables disponibles |
| Contrôle synthétique | Faible | Aucune répartition possible, régions de contrôle disponibles |

## Pièges courants {#gotchas}
- **Problème du regard anticipé** (peeking) : vérifier les résultats chaque jour et arrêter dès qu'ils sont significatifs gonfle le taux de faux positifs. Utiliser un test séquentiel (SPRT) si vous devez consulter les résultats en cours
- **Comparaisons multiples** : tester 20 métriques à alpha=0,05 signifie qu'environ une sera « significative » par hasard. Appliquer la correction de Bonferroni
- **P-hacking** : essayer de nombreuses analyses jusqu'à en obtenir une significative. Pré-enregistrer le plan d'analyse
- **Piège de la précision avec les tests A/B** : une hausse de 1 % du CTR peut valoir des millions : ne pas écarter les effets faibles mais significatifs
- **Ne pas accumuler les résultats** : la saisonnalité signifie que les résultats du trimestre précédent peuvent ne pas se généraliser

## Voir aussi {#see-also}
- [[probability-distributions]] - théorie sous-jacente
- [[descriptive-statistics]] - synthèse des données avant les tests
- [[bi-dashboards]] - présentation des résultats d'expériences
- [[model-evaluation]] - métriques hors ligne complémentaires des tests A/B

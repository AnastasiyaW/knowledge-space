---
title: "Flux de travail en science des données et bonnes pratiques"
category: practices
tags: [data-science, workflow, methodology, best-practices]
level: 3
source_sha256: eda26c01e742aa2cc3921c73c6f97fa30bdc2d405ee01dbdd6df1823015ebb59
translation: machine
translated_at: '2026-10-24'
---
# Flux de travail en science des données et bonnes pratiques {#data-science-workflow-and-best-practices}

Méthodologie de projet de bout en bout. La différence entre un modèle de démonstration et une solution prête pour la production tient à la rigueur du processus.

## Flux de travail du projet {#project-workflow}

### 1. Définition du problème {#1-problem-definition}
- Comprendre l'objectif métier (et pas seulement l'objectif ML)
- Définir la métrique de succès (à la fois la métrique ML ET la métrique métier)
- Déterminer si le ML est réellement nécessaire : parfois des règles simples suffisent

### 2. Collecte des données {#2-data-collection}
- Requêtes SQL sur des bases de données
- Appels d'API, CSV/Excel fournis par les parties prenantes
- Feature stores / entrepôts de données
- Web scraping (avec autorisation)

### 3. EDA (Exploratory Data Analysis) {#3-eda-exploratory-data-analysis}
- Forme, dtypes, `describe()`
- Valeurs manquantes (pourcentage par colonne)
- Distribution de la cible (équilibrée ? asymétrique ?)
- Analyse univariée : histogrammes (numériques), value_counts (catégorielles)
- Analyse bivariée : matrice de corrélation, groupby + moyenne de la cible
- Valeurs aberrantes : boîtes à moustaches, z-scores, méthode IQR

### 4. Prétraitement {#4-preprocessing}
- Traiter les valeurs manquantes (imputation ou suppression)
- Traiter les valeurs aberrantes (plafonnement, suppression ou conservation)
- Encoder les variables catégorielles
- Mettre à l'échelle les variables numériques
- Créer les découpages train/validation/test
- Ingénierie des caractéristiques

### 5. Modélisation {#5-modeling}
- Commencer par une baseline simple (prédiction par la moyenne, régression logistique)
- Essayer plusieurs familles de modèles (linéaires, à base d'arbres, ensembles)
- Utiliser la validation croisée pour des estimations fiables
- Suivre les expériences

### 6. Évaluation {#6-evaluation}
- Comparer à la baseline
- Vérifier le surapprentissage (écart entre entraînement et validation)
- Analyse des erreurs : que le modèle prédit-il mal ?
- Importance des variables
- Évaluation finale sur le jeu de test réservé, UNE SEULE FOIS

### 7. Déploiement {#7-deployment}
- Exporter le modèle (pickle, ONNX, model.save())
- Créer une API de prédiction (Flask, FastAPI)
- Mettre en place la surveillance (dérive des données, dégradation du modèle)
- Test A/B en production

## Pièges courants {#common-pitfalls}

### Fuite de données {#data-leakage}
Des informations provenant du futur ou du jeu de test s'infiltrent dans l'entraînement. **Erreur la plus dangereuse.**

- **Fuite de la cible** : variable dérivée de la cible ou corrélée à celle-ci
- **Fuite entre train et test** : prétraitement ajusté sur l'ensemble des données, test compris
- **Fuite temporelle** : utiliser des données futures pour prédire le passé

**Prévention** : toujours découper AVANT tout prétraitement. Utiliser les Pipelines de sklearn.

### Surapprentissage {#overfitting}
Le modèle mémorise les données d'entraînement et échoue sur les nouvelles données.
- **Symptômes** : grand écart entre les performances d'entraînement et de validation
- **Solutions** : régularisation, modèle plus simple, plus de données, arrêt anticipé, dropout, CV

### Déséquilibre des classes {#class-imbalance}
Une classe domine largement les autres (99 % négatifs, 1 % positifs).
- **Problème** : le modèle prédit la classe majoritaire et obtient une exactitude élevée
- **Solutions** : poids de classes, SMOTE/suréchantillonnage, sous-échantillonnage, métriques F1/PR-AUC

### Biais de sélection {#selection-bias}
- **Biais de survie** : on ne voit que les exemples qui ont réussi
- **Biais d'échantillonnage** : collecte de données non aléatoire

## Reproductibilité {#reproducibility}

```python
import numpy as np
import random
import torch

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

# sklearn
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=SEED)
```

**Liste de contrôle :**
- Épingler les versions des bibliothèques dans requirements.txt
- Documenter les sources de données et les étapes de prétraitement
- Sauvegarder les modèles entraînés et leurs paramètres
- Versionner le code avec git
- Consigner les résultats des expériences

## Communication {#communication}

- **Commencer par l'impact métier**, pas par le modèle
- Présenter des métriques que le métier comprend (chiffre d'affaires, économies de coûts)
- Expliquer les limites et les cas limites
- Utiliser des visualisations (heatmap de matrice de confusion, importance des variables)
- Fournir des intervalles de confiance, et pas seulement des estimations ponctuelles

## Pièges à éviter {#gotchas}
- Passer des semaines sur la modélisation alors que le problème vient de données de mauvaise qualité
- Optimiser la mauvaise métrique (exactitude élevée sur des données déséquilibrées)
- Ne pas comparer d'abord à une baseline simple
- Déployer sans surveillance : les modèles se dégradent silencieusement
- Ignorer les experts du domaine, qui connaissent les données mieux que n'importe quel algorithme

## Voir aussi {#see-also}
- [[model-evaluation]] - métriques et stratégies de validation
- [[feature-engineering]] - l'étape au meilleur retour sur investissement
- [[pandas-eda]] - mise en œuvre pratique de l'EDA
- [[hypothesis-testing]] - test A/B des modèles déployés

---
title: "KNN et algorithmes classiques de ML"
category: models
tags: [data-science, ml, knn, svm, naive-bayes, decision-tree]
level: 4
source_sha256: 1534b8d951c80d7f1bf9e439aaf5c8fa7a2aa43f70feedbf7df191a4b243657c
translation: machine
translated_at: '2026-10-24'
---
# KNN et algorithmes classiques de ML {#knn-and-classical-ml-algorithms}

Les algorithmes classiques de ML au-delà des modèles linéaires et du gradient boosting. Importants pour comprendre le paysage des algorithmes et choisir les outils appropriés.

## K-Nearest Neighbors (KNN) {#k-nearest-neighbors-knn}

Classification par vote majoritaire des k plus proches voisins. Pas de phase d'entraînement : les prédictions sont calculées au moment de la requête.

```python
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
```

**Métriques de distance :**
- Euclidienne : ||x-y||_2 = sqrt(sum((x_i - y_i)^2))
- Manhattan : ||x-y||_1 = sum(|x_i - y_i|)
- Minkowski : ||x-y||_p (généralisation)

**Choisir k :**
- k trop petit : surapprentissage (sensible au bruit)
- k trop grand : sous-apprentissage (frontières trop lisses)
- Utiliser la validation croisée pour le sélectionner

**Malédiction de la dimensionnalité** : en grande dimension, tous les points deviennent à peu près équidistants. Nécessite une réduction de dimensionnalité (PCA) ou une sélection de variables.

**Avantages** : simple, aucune hypothèse sur la distribution des données, fonctionne pour la classification multi-classes.
**Inconvénients** : lent au moment de la prédiction (O(n) par requête), nécessite une mise à l'échelle des variables, échoue en grande dimension.

## Support Vector Machines (SVM) {#support-vector-machines-svm}

Recherche de l'hyperplan qui maximise la marge entre les classes.

```python
from sklearn.svm import SVC, SVR

svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X_train, y_train)
```

**Astuce du noyau (kernel trick)** : projeter les données dans des dimensions supérieures où elles deviennent linéairement séparables.
- Linéaire : aucune transformation
- RBF (gaussien) : crée des frontières de décision lisses
- Polynomial : non-linéarité basée sur le degré

**Paramètre C** : compromis entre la largeur de la marge et les erreurs de classification. C élevé = marge étroite, moins d'erreurs sur les données d'entraînement.

**Avantages** : efficace en grande dimension, fonctionne bien lorsque la marge de séparation est nette.
**Inconvénients** : lent sur les grands jeux de données, ne passe pas bien à l'échelle au-delà d'environ 10K échantillons, pas de sortie probabiliste par défaut.

## Arbres de décision (autonomes) {#decision-trees-standalone}

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=10)
dt.fit(X_train, y_train)

# Visualization
import matplotlib.pyplot as plt
plt.figure(figsize=(20, 10))
plot_tree(dt, feature_names=features, class_names=['No', 'Yes'], filled=True)
plt.show()
```

**Critères de division** : impureté de Gini = sum(p_i * (1 - p_i)), entropie = -sum(p_i * log(p_i))

**Avantages** : interprétables (visualisables), gèrent des types de données mixtes, aucune mise à l'échelle nécessaire.
**Inconvénients** : forte variance (instables), sujets au surapprentissage. Préférer Random Forest ou le gradient boosting.

## Guide de sélection d'algorithme {#algorithm-selection-guide}

| Situation | Recommandé |
|-----------|-------------|
| Données tabulaires, toute taille | Gradient boosting (CatBoost) |
| Petites données, besoin d'interprétabilité | Régression logistique, arbre de décision |
| Classification de texte, petites données | Naive Bayes, TF-IDF + LogReg |
| Données creuses de grande dimension | SVM, Logistic avec L1 |
| Besoin de probabilités | Régression logistique, CatBoost |
| Images/texte/audio | Deep learning |
| Référence (baseline) | Prédiction moyenne/mode, puis LogReg |

## Pièges à éviter {#gotchas}
- Le KNN nécessite des variables standardisées (la distance euclidienne dépend de l'échelle)
- Le SVM est pratiquement déprécié pour les données tabulaires : le gradient boosting domine
- Un arbre de décision unique ne doit jamais être utilisé seul : toujours utiliser un ensemble (RF, GB)
- Toujours comparer à une référence simple avant d'utiliser des modèles complexes
- Théorème « No free lunch » : aucun algorithme n'est le meilleur pour TOUS les problèmes

## Voir aussi {#see-also}
- [[gradient-boosting]] - approche dominante pour les données tabulaires
- [[linear-models]] - la régression logistique comme référence
- [[unsupervised-learning]] - KNN pour la détection d'anomalies
- [[feature-engineering]] - prétraitement pour les modèles basés sur la distance

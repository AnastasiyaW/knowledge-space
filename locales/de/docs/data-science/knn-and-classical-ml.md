---
title: "KNN und klassische ML-Algorithmen"
category: models
tags: [data-science, ml, knn, svm, naive-bayes, decision-tree]
level: 4
source_sha256: 1534b8d951c80d7f1bf9e439aaf5c8fa7a2aa43f70feedbf7df191a4b243657c
translation: machine
translated_at: '2026-10-24'
---
# KNN und klassische ML-Algorithmen {#knn-and-classical-ml-algorithms}

Klassische ML-Algorithmen jenseits linearer Modelle und Gradient Boosting. Wichtig, um die Landschaft der Algorithmen zu verstehen und geeignete Werkzeuge auszuwählen.

## K-Nearest Neighbors (KNN) {#k-nearest-neighbors-knn}

Klassifikation per Mehrheitsentscheid der k nächsten Nachbarn. Es gibt keine Trainingsphase – Vorhersagen werden zur Abfragezeit berechnet.

```python
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
```

**Distanzmetriken:**
- Euklidisch: ||x-y||_2 = sqrt(sum((x_i - y_i)^2))
- Manhattan: ||x-y||_1 = sum(|x_i - y_i|)
- Minkowski: ||x-y||_p (Verallgemeinerung)

**Wahl von k:**
- k zu klein: Overfitting (empfindlich gegenüber Rauschen)
- k zu groß: Underfitting (zu glatt)
- Mit Kreuzvalidierung auswählen

**Fluch der Dimensionalität**: In hohen Dimensionen liegen alle Punkte ungefähr gleich weit voneinander entfernt. Erfordert Dimensionsreduktion (PCA) oder Feature-Selektion.

**Vorteile**: einfach, keine Annahmen über die Datenverteilung, funktioniert für Mehrklassenprobleme.
**Nachteile**: langsam zur Vorhersagezeit (O(n) pro Abfrage), erfordert Feature-Skalierung, versagt in hohen Dimensionen.

## Support Vector Machines (SVM) {#support-vector-machines-svm}

Findet die Hyperebene, die den Abstand (Margin) zwischen den Klassen maximiert.

```python
from sklearn.svm import SVC, SVR

svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X_train, y_train)
```

**Kernel-Trick**: Projiziert die Daten in höhere Dimensionen, in denen sie linear trennbar werden.
- Linear: keine Transformation
- RBF (Gauß): erzeugt glatte Entscheidungsgrenzen
- Polynomiell: Nichtlinearität auf Basis des Grades

**C-Parameter**: Abwägung zwischen Margin-Breite und Klassifikationsfehlern. Hohes C = schmale Margin, weniger Fehler auf den Trainingsdaten.

**Vorteile**: effektiv in hohen Dimensionen, funktioniert gut bei klarer Trennlinie zwischen den Klassen.
**Nachteile**: langsam bei großen Datensätzen, skaliert schlecht jenseits von ca. 10K Samples, standardmäßig keine Wahrscheinlichkeitsausgabe.

## Entscheidungsbäume (eigenständig) {#decision-trees-standalone}

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

**Splitting-Kriterien**: Gini-Impurity = sum(p_i * (1 - p_i)), Entropie = -sum(p_i * log(p_i))

**Vorteile**: interpretierbar (lässt sich visualisieren), verarbeitet gemischte Datentypen, keine Skalierung nötig.
**Nachteile**: hohe Varianz (instabil), neigt zu Overfitting. Stattdessen Random Forest oder Gradient Boosting verwenden.

## Leitfaden zur Algorithmenauswahl {#algorithm-selection-guide}

| Situation | Empfehlung |
|-----------|-------------|
| Tabellarisch, beliebige Größe | Gradient Boosting (CatBoost) |
| Kleine Daten, Interpretierbarkeit nötig | Logistische Regression, Entscheidungsbaum |
| Textklassifikation, kleine Daten | Naive Bayes, TF-IDF + LogReg |
| Hochdimensionale, dünn besetzte Daten | SVM, logistische Regression mit L1 |
| Wahrscheinlichkeiten benötigt | Logistische Regression, CatBoost |
| Bilder/Text/Audio | Deep Learning |
| Baseline | Mittelwert-/Modus-Vorhersage, danach LogReg |

## Stolpersteine {#gotchas}
- KNN benötigt standardisierte Features (die euklidische Distanz ist skalenabhängig)
- SVM ist für tabellarische Daten praktisch veraltet – Gradient Boosting dominiert
- Ein einzelner Entscheidungsbaum sollte nie allein verwendet werden – immer ein Ensemble nutzen (RF, GB)
- Vor dem Einsatz komplexer Modelle immer mit einer einfachen Baseline vergleichen
- „No Free Lunch“-Theorem: Kein Algorithmus ist für ALLE Probleme der beste

## Siehe auch {#see-also}
- [[gradient-boosting]] – dominierender Ansatz für tabellarische Daten
- [[linear-models]] – logistische Regression als Baseline
- [[unsupervised-learning]] – KNN zur Anomalieerkennung
- [[feature-engineering]] – Vorverarbeitung für distanzbasierte Modelle

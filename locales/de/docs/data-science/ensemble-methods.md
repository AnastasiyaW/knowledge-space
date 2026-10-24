---
title: "Ensemble-Methoden"
category: concepts
tags: [data-science, ensemble, bagging, boosting, stacking, voting]
level: 3
source_sha256: 904c045fc2b890bfc9a72bda7b443b90344d9c7e92129e6689086ef0659cb0a6
translation: machine
translated_at: '2026-10-24'
---
# Ensemble-Methoden {#ensemble-methods}

Kombination mehrerer Modelle, um bessere Vorhersagen zu erzielen als mit einem einzelnen Modell. Drei Hauptstrategien: Bagging (parallel, reduziert Varianz), Boosting (sequenziell, reduziert Bias), Stacking (lernt, wie sich die Modelle kombinieren lassen).

## Bagging (Bootstrap Aggregating) {#bagging-bootstrap-aggregating}

Mehrere Modelle werden auf Bootstrap-Stichproben trainiert (Zufallsstichproben mit Zurücklegen), die Vorhersagen werden per Mehrheitsentscheid (Klassifikation) bzw. Mittelwertbildung (Regression) aggregiert.

```python
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

bagging = BaggingClassifier(
    estimator=DecisionTreeClassifier(max_depth=None),
    n_estimators=50,
    max_samples=0.8,    # 80% of data per base model
    max_features=0.8,   # 80% of features per base model
    bootstrap=True,
    oob_score=True,     # out-of-bag estimate (free validation)
    random_state=42
)
bagging.fit(X_train, y_train)
print(f"OOB score: {bagging.oob_score_:.3f}")
```

**Random Forest** ist Bagging plus zufällige Teilmengen von Merkmalen an jedem Split. Die erfolgreichste Bagging-Methode.

**Warum es funktioniert**: Durch Mittelung weitgehend unkorrelierter Vorhersagen wird die Varianz reduziert. Jedes Modell sieht andere Daten und macht daher andere Fehler. Die Fehler heben sich bei der Aggregation gegenseitig auf.

## Boosting {#boosting}

Schwache Lerner werden sequenziell trainiert, wobei sich jeder auf die Fehler der vorherigen konzentriert.

### AdaBoost {#adaboost}

Erhöht das Gewicht fehlklassifizierter Samples:

```python
from sklearn.ensemble import AdaBoostClassifier

ada = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),  # stumps
    n_estimators=200,
    learning_rate=0.1,
    random_state=42
)
ada.fit(X_train, y_train)
```

### Gradient Boosting (XGBoost / LightGBM / CatBoost) {#gradient-boosting-xgboost-lightgbm-catboost}

Ein neuer Baum wird an die Residuen (Gradient der Verlustfunktion) angepasst. Einen detaillierten Vergleich finden Sie unter [[gradient-boosting]].

### Wichtige Boosting-Parameter {#key-boosting-parameters}

| Parameter | Wirkung | Typischer Bereich |
|-----------|---------|-------------------|
| n_estimators | Anzahl der Bäume | 100-10000 |
| learning_rate | Shrinkage pro Baum | 0.01-0.3 |
| max_depth | Komplexität des Baums | 3-10 |
| subsample | Anteil der Zeilen-Stichprobe | 0.5-1.0 |
| colsample_bytree | Merkmals-Stichprobe | 0.5-1.0 |
| reg_alpha (L1) | Sparsität | 0-10 |
| reg_lambda (L2) | Glättung | 0-10 |

**Faustregel**: Niedrigere Lernrate + mehr Bäume = bessere, aber langsamere Ergebnisse. Early Stopping verwenden.

## Stacking {#stacking}

Ein Meta-Lerner wird auf den Vorhersagen der Basismodelle trainiert:

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression

stack = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=100)),
        ('xgb', XGBClassifier(n_estimators=200)),
        ('svm', SVC(probability=True))],
    final_estimator=LogisticRegression(),
    cv=5,  # use cross-val predictions to prevent leakage
    stack_method='predict_proba'  # use probabilities not hard labels
)
stack.fit(X_train, y_train)
```

**Mehrstufiges Stacking**: Basismodelle -> Meta-Lerner der Stufe 1 -> Meta-Lerner der Stufe 2. Ab 2 Stufen nehmen die Zugewinne ab. Auf Kaggle beliebt, lohnt sich im Produktivbetrieb aber selten im Verhältnis zur zusätzlichen Komplexität.

## Voting {#voting}

Einfache Kombination verschiedenartiger Modelle:

```python
from sklearn.ensemble import VotingClassifier

# Hard voting: majority vote
hard_vote = VotingClassifier(
    estimators=[
        ('lr', LogisticRegression()),
        ('rf', RandomForestClassifier()),
        ('svm', SVC())
    ],
    voting='hard'
)

# Soft voting: average probabilities (usually better)
soft_vote = VotingClassifier(
    estimators=[
        ('lr', LogisticRegression()),
        ('rf', RandomForestClassifier()),
        ('svm', SVC(probability=True))
    ],
    voting='soft',
    weights=[1, 2, 1]  # weight better models higher
)
```

## Blending {#blending}

Einfacher als Stacking – statt Cross-Validation wird ein Holdout-Set verwendet:

```python
# Split: train -> base_train + blend_set
X_base, X_blend, y_base, y_blend = train_test_split(
    X_train, y_train, test_size=0.3, random_state=42
)

# Train base models on base_train
models = [rf.fit(X_base, y_base), xgb.fit(X_base, y_base)]

# Generate blend features
blend_features = np.column_stack([
    m.predict_proba(X_blend)[:, 1] for m in models
])

# Train meta-model on blend_set
meta = LogisticRegression()
meta.fit(blend_features, y_blend)
```

## Modellvielfalt {#model-diversity}

Ensembles funktionieren am besten, wenn die Basismodelle **unterschiedliche Fehler** machen:

- **Unterschiedliche Algorithmen**: Baum + lineares Modell + neuronales Netz
- **Unterschiedliche Merkmale**: Teilmengen, unterschiedliche Vorverarbeitung
- **Unterschiedliche Hyperparameter**: flache + tiefe Bäume
- **Unterschiedliche Trainingsdaten**: Bootstrap, unterschiedliche Zeitfenster

Die Korrelation zwischen den Modellfehlern ist der Feind von Ensembles. Zwei Modelle mit jeweils 80 % Genauigkeit und unkorrelierten Fehlern ergeben im Ensemble etwa 96 %. Zwei korrelierte 80-%-Modelle bleiben bei etwa 80 %.

## Stolperfallen {#gotchas}

- **Stacking ohne Cross-Validation führt zu Data Leakage**: Trainiert man die Basismodelle auf allen Trainingsdaten und verwendet dann genau diese Vorhersagen, um den Meta-Lerner zu trainieren, sind die Vorhersagen der Basismodelle auf den Trainingsdaten überangepasst. Für das Trainings-Set des Meta-Lerners immer Out-of-Fold-Vorhersagen verwenden
- **Abnehmender Ertrag**: Der größte Zugewinn entsteht beim Übergang von einem Modell zu 3–5 verschiedenartigen Modellen. Ein 50. Modell hilft kaum noch. Im Produktivbetrieb überwiegt der Aufwand für die Pflege vieler Modelle häufig den marginalen Genauigkeitsgewinn. Mit 3 verschiedenartigen Modellen beginnen
- **Boosting überanpasst bei verrauschten Labels**: Boosting konzentriert sich auf schwierige Beispiele – sind diese falsch gelabelt, memoriert es das Rauschen. Early Stopping verwenden und auf einem sauberen Holdout-Set validieren. Ist das Label-Rauschen bekannt, eher Bagging verwenden oder Label Smoothing einsetzen

## Siehe auch {#see-also}

- [[gradient-boosting]]
- [[model-evaluation]]
- [[hyperparameter-optimization]]

---
title: "Gradient Boosting und baumbasierte Modelle"
category: models
tags: [data-science, ml, catboost, xgboost, lightgbm, random-forest, ensemble]
level: 3
source_sha256: 25e8afc890bca06615fe52b8c41315a4daf40e507fb8a084e3cb1df06665b1d2
translation: machine
translated_at: '2026-10-24'
---
# Gradient Boosting und baumbasierte Modelle {#gradient-boosting-and-tree-based-models}

Gradient Boosting ist der dominierende Algorithmus für tabellarische Daten. CatBoost, LightGBM und XGBoost sind Implementierungen derselben Idee. Baumbasierte Modelle verarbeiten gemischte Datentypen, nichtlineare Zusammenhänge und Wechselwirkungen ohne manuelles Feature Engineering.

## Entscheidungsbäume {#decision-trees}

Grundlegender Baustein. Daten werden rekursiv anhand von Schwellenwerten einzelner Features aufgeteilt, um die Unreinheit (Impurity) zu minimieren.

**Splitting-Kriterien:**
- **Gini-Unreinheit**: sum(p_i * (1 - p_i)). Misst die Wahrscheinlichkeit einer Fehlklassifikation
- **Entropie**: -sum(p_i * log(p_i)). Informationstheoretisches Maß für Unordnung
- **MSE** (Regression): Varianz innerhalb jedes Splits

**Vorteile**: interpretierbar, verarbeitet gemischte Typen, keine Skalierung nötig.
**Nachteile**: hohe Varianz, neigt zu Overfitting, instabil (kleine Datenänderungen -> anderer Baum).

## Random Forest {#random-forest}

Ensemble aus Entscheidungsbäumen. Jeder Baum wird auf einem Bootstrap-Sample mit einer zufälligen Teilmenge der Features trainiert.

```python
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X_train, y_train)
rf.feature_importances_  # built-in importance scores
```

- **Bagging** reduziert die Varianz durch Mittelung unkorrelierter Vorhersagen
- Feature Importance: Abnahme der Unreinheit beim Split auf das Feature
- Peinlich parallelisierbar – jeder Baum wird unabhängig trainiert

## Gradient Boosting {#gradient-boosting}

Bäume werden sequenziell aufgebaut, wobei jeder die Fehler der vorherigen korrigiert.

**Idee**: Einen Baum an die Residuen (Fehler) des aktuellen Modells anpassen und mit einer kleinen Lernrate hinzufügen.

### CatBoost {#catboost}

Beste Leistung ohne Anpassung. Verarbeitet kategoriale Features nativ.

```python
from catboost import CatBoostRegressor, CatBoostClassifier

model = CatBoostRegressor(cat_features=['transmission', 'fuel_type'])
model.fit(
    train[features], train[target],
    eval_set=(val[features], val[target]),
    verbose=100
)

# Predictions
y_pred = model.predict(test[features])

# Classification: get probabilities
model = CatBoostClassifier(cat_features=cat_features)
model.fit(train[features], train[target],
          eval_set=(val[features], val[target]))
scores = model.predict_proba(test[features])[:, 1]

# Feature importance
model.get_feature_importance(prettified=True)
```

**Validierungsset ist zwingend erforderlich**: CatBoost trainiert iterativ. Ohne Validierung memoriert es die Trainingsdaten. Early Stopping bricht beim Minimum des Validierungsfehlers ab.

### CatBoost Cross-Validation {#catboost-cross-validation}

```python
from catboost import cv, Pool

cv_data = cv(
    pool=Pool(X, y, cat_features=cat_features),
    params={'loss_function': 'Logloss', 'eval_metric': 'AUC'},
    fold_count=5, shuffle=True, stratified=True,
    partition_random_seed=42, verbose=False
)
best_iter = cv_data['test-AUC-mean'].idxmax()
```

**Workflow**: CV zur Bestimmung der optimalen Iterationszahl -> finales Modell auf vollständigen Train+Val-Daten mit dieser Anzahl trainieren -> auf Testdaten evaluieren.

### XGBoost {#xgboost}

```python
import xgboost as xgb
model = xgb.XGBClassifier(
    n_estimators=500, max_depth=6, learning_rate=0.1,
    subsample=0.8, colsample_bytree=0.8,
    early_stopping_rounds=50, eval_metric='auc'
)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=50)
```

### LightGBM {#lightgbm}

Am schnellsten bei großen Datensätzen. Leaf-wise-Wachstum (statt level-wise).

```python
import lightgbm as lgb
model = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=31)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)],
          callbacks=[lgb.early_stopping(50)])
```

## Wichtige Hyperparameter {#key-hyperparameters}

| Parameter | Wirkung | Typischer Bereich |
|-----------|---------|-------------------|
| n_estimators / iterations | Anzahl der Bäume | 100-5000 |
| learning_rate | Schrittweite pro Baum | 0.01-0.3 |
| max_depth | Baumtiefe | 3-10 |
| subsample | Anteil der Zeilen pro Baum | 0.5-1.0 |
| colsample_bytree | Anteil der Features pro Baum | 0.5-1.0 |
| min_child_weight | Minimale Anzahl Samples im Blatt | 1-100 |
| reg_lambda (L2) | L2-Regularisierung | 0-10 |
| reg_alpha (L1) | L1-Regularisierung | 0-10 |

**Faustregel**: Niedrigere learning_rate + mehr Estimators = besser, aber langsamer. Mit den Standardwerten starten, zuerst learning_rate und max_depth abstimmen.

## Umgang mit unausgewogenen Klassen {#handling-imbalanced-classes}

```python
# CatBoost
model = CatBoostClassifier(scale_pos_weight=neg_count/pos_count)

# XGBoost
model = xgb.XGBClassifier(scale_pos_weight=neg_count/pos_count)

# Or: tune threshold on validation set
```

## Vergleich {#comparison}

| Aspekt | CatBoost | XGBoost | LightGBM | Random Forest |
|--------|----------|---------|----------|---------------|
| Standardleistung | Am besten | Gut | Gut | Gut |
| Behandlung kategorialer Features | Nativ | Manuelle Kodierung | Nativ | Manuelle Kodierung |
| Geschwindigkeit | Mittel | Mittel | Am schnellsten | Schnell (parallel) |
| Overfitting-Risiko | Gering | Mittel | Mittel | Gering |
| GPU-Unterstützung | Ja | Ja | Ja | Nein |

## Stolperfallen {#gotchas}
- **Accuracy nicht verwenden** bei unausgewogenen Datensätzen – ein Modell, das immer Null vorhersagt, erreicht bei einer 80/20-Aufteilung 80 % Accuracy
- CatBoost ohne eval_set überanpasst unbemerkt – immer eine Validierung angeben
- Feature Importance schwankt zwischen Läufen und Methoden – für verlässliche Ergebnisse Permutation Importance verwenden
- XGBoost erfordert für kategoriale Features manuelles One-Hot-Encoding (sofern `enable_categorical=True` nicht verwendet wird)
- Zuerst mit Standardwerten starten, bevor Hyperparameter abgestimmt werden – Tuning kompensiert keine schlechten Features

## Siehe auch {#see-also}
- [[model-evaluation]] – Metriken für den Modellvergleich
- [[feature-engineering]] – für Bäume weniger kritisch, aber dennoch wertvoll
- [[linear-models]] – einfachere Alternative, nützliche Baseline
- [[neural-networks]] – wenn tabellarische Modelle nicht ausreichen

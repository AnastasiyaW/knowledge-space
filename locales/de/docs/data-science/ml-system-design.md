---
title: "ML-Systemdesign"
category: patterns
tags: [data-science, system-design, architecture, scalability, production-ml]
level: 4
source_sha256: 4f78f3275069647f2db4f49dd0e3bf7c8846d3a2f6c12e590656d7cc4b3e1ee6
translation: machine
translated_at: '2026-10-24'
---
# ML-Systemdesign {#ml-system-design}

Entwurf end-to-end-ML-Systeme, die im Produktivbetrieb funktionieren. Behandelt Problemformulierung, Datenpipeline, Modellauswahl, Serving-Architektur und Monitoring. Das Modell macht typischerweise < 10 % der gesamten Systemkomplexität aus.

## Problemformulierung {#problem-framing}

Bevor die Modellierung beginnt, definiere:

1. **Geschäftsziel**: Welche Kennzahl bewegt tatsächlich etwas (Umsatz, Engagement, Kosten)?
2. **ML-Ziel**: Was sagt das Modell vorher? (Klassifikation, Ranking, Regression)
3. **Datenverfügbarkeit**: Welche gelabelten Daten existieren? Lassen sich Labels generieren?
4. **Randbedingungen**: Latenzbudget, Rechenbudget, Fairness-Anforderungen
5. **Baseline**: Welche Nicht-ML-Lösung existiert? (Regeln, Heuristiken)

**Gängige Formulierungen:**
- Spam-Erkennung -> binäre Klassifikation
- Suchranking -> Learning to Rank (paarweise oder listenweise)
- Empfehlungen -> kollaboratives Filtern + inhaltsbasiert, als Ranking ausgeliefert
- Betrug -> Anomalieerkennung + überwachte Klassifikation
- ETA-Vorhersage -> Regression mit Konfidenzintervallen

## Architektur der Datenpipeline {#data-pipeline-architecture}

```php
Raw Data -> Ingestion -> Validation -> Feature Engineering -> Feature Store
                                                                |
Training Pipeline <-------- Historical Features ----------------+
    |                                                           |
Model Registry                                                  |
    |                                                           |
Serving Pipeline <--------- Online Features --------------------+
    |
Predictions -> Logging -> Monitoring -> Feedback Loop
```

### Datenvalidierung {#data-validation}

```python
import great_expectations as gx

# Define expectations
suite = gx.ExpectationSuite(name="transaction_data")
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="amount")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount", min_value=0, max_value=1000000
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfUniqueValuesToBeBetween(
        column="user_id", min_value=0.01  # not too many duplicates
    )
)
```

## Muster für Feature Engineering {#feature-engineering-patterns}

### Zeitliche Features {#temporal-features}

```python
# Time-based aggregations
def build_temporal_features(df, entity_col, time_col, value_col):
    features = {}
    for window in ['7d', '30d', '90d']:
        rolled = df.set_index(time_col).groupby(entity_col)[value_col].rolling(window)
        features[f'{value_col}_mean_{window}'] = rolled.mean()
        features[f'{value_col}_std_{window}'] = rolled.std()
        features[f'{value_col}_count_{window}'] = rolled.count()
    return pd.DataFrame(features)
```

### Interaktions-Features {#interaction-features}

```python
# Ratios, differences, products between features
df['price_per_sqft'] = df['price'] / df['sqft']
df['income_to_debt'] = df['income'] / (df['debt'] + 1)
df['recency_x_frequency'] = df['days_since_last'] * df['purchase_count']
```

### Target Encoding (für kategoriale Merkmale mit hoher Kardinalität) {#target-encoding-for-high-cardinality-categoricals}

```python
from category_encoders import TargetEncoder

te = TargetEncoder(cols=['zip_code', 'merchant_id'], smoothing=10)
X_encoded = te.fit_transform(X_train, y_train)
# Use same encoder on test: te.transform(X_test)
```

## Entscheidungsbaum zur Modellauswahl {#model-selection-decision-tree}

```php
Tabular data?
  Yes -> Start with CatBoost/XGBoost
    Need uncertainty? -> Bayesian methods or conformal prediction
    Need interpretability? -> SHAP on tree model or linear model
  No -> What modality?
    Text -> Pretrained transformer (fine-tune or embed)
    Image -> Pretrained CNN/ViT (fine-tune)
    Sequence/Time -> LSTM, Transformer, or specialized (Prophet, N-BEATS)
    Graph -> GNN (PyG)

Data size < 1000?
  Yes -> Simple model (logistic regression, small RF) + strong regularization
  Data size > 1M?
  Yes -> Consider online learning, distributed training, or sampling
```

## Serving-Architekturen {#serving-architectures}

### Online-Serving (Echtzeit) {#online-serving-real-time}

- Latenz < 100 ms pro Anfrage
- REST-API (FastAPI, Flask) oder gRPC
- Modell im Speicher geladen, vorberechnete Features aus dem Feature Store
- Horizontale Skalierung hinter einem Load Balancer

### Batch-Serving {#batch-serving}

- Verarbeitung aller Daten periodisch (stündlich/täglich)
- Günstiger, einfacher, höherer Durchsatz
- Einsatz für Empfehlungen, E-Mail-Targeting, Berichtserstellung
- Vorhersagen in Datenbank/Cache für Abfragen speichern

### Streaming (Nahezu Echtzeit) {#streaming-near-real-time}

- Verarbeitung von Ereignissen bei Eintreffen (Kafka/Flink)
- Für Betrugserkennung, Echtzeit-Personalisierung
- Modell als Stream-Processor deployt

## A/B-Tests für ML-Modelle {#ab-testing-ml-models}

```python
# Traffic splitting
import hashlib

def get_variant(user_id, experiment_id, traffic_pct=0.1):
    hash_key = f"{experiment_id}:{user_id}"
    hash_val = int(hashlib.md5(hash_key.encode()).hexdigest(), 16)
    bucket = hash_val % 1000

    if bucket < traffic_pct * 1000:
        return "treatment"  # new model
    return "control"        # existing model
```

**Statistische Power**: Es werden ausreichend Stichproben für verlässliche Ergebnisse benötigt. Bei kleinen Effektstärken (< 1 % Lift) können Millionen Beobachtungen nötig sein. Sequenzielles Testen nutzen, um bei eindeutigen Ergebnissen frühzeitig zu stoppen.

## Feedback-Schleifen {#feedback-loops}

- **Direktes Feedback**: Nutzer klickt / klickt nicht -> Label innerhalb von Minuten
- **Verzögertes Feedback**: Betrug wird Tage/Wochen später bestätigt
- **Implizites Feedback**: Kein negatives Signal (Nutzer hat sich nicht beschwert != Nutzer ist zufrieden)
- **Gefahr der Feedback-Schleife**: Das Modell beeinflusst, welche Daten es sieht. Ein Empfehlungsmodell, das Element X nie zeigt, wird nie lernen, ob X gut ist

## Monitoring-Checkliste {#monitoring-checklist}

| Was | Wie | Alarm bei |
|-----|-----|-----------|
| Qualität der Eingangsdaten | Schema-Validierung, Null-Prüfungen | Schemaverletzung, Null-Rate > Schwellenwert |
| Feature-Drift | KS-Test, PSI auf Feature-Verteilungen | p-Wert < 0,001 oder PSI > 0,2 |
| Vorhersage-Drift | Verteilung der Modellausgaben | Mittelwert-/Varianzverschiebung über 2 Sigma hinaus |
| Modellleistung | Ist vs. Vorhersage (sofern Labels verfügbar) | Metrik fällt > 5 % unter Baseline |
| Latenz | Antwortzeit P50/P95/P99 | P99 > SLA |
| Durchsatz | Anfragen pro Sekunde | Rückgang > 20 % gegenüber dem Normalwert |

## Fallstricke {#gotchas}

- **Training-Serving-Skew ist der häufigste Produktionsfehler im ML**: Ein Feature wird offline (SQL mit vollständiger Historie) anders berechnet als online (Echtzeit mit unvollständigen Daten). Einen Feature Store oder gemeinsam genutzten Feature-Engineering-Code verwenden. Testen, indem Offline-Vorhersagen mit Produktionsvorhersagen für dieselben Eingaben verglichen werden
- **Bias durch Feedback-Schleifen**: Blockiert ein Betrugsmodell Transaktionen, werden die Ergebnisse der blockierten nie beobachtet. Training auf verzerrten Daten verstärkt bestehende Verzerrungen. Einen kleinen Anteil markierter Fälle zufällig durchlassen (Exploration) oder Techniken der kausalen Inferenz einsetzen
- **Vorzeitige Optimierung**: Mit dem einfachsten Modell beginnen, das funktionieren könnte (logistische Regression, ein einzelner Entscheidungsbaum). Baseline-Metriken festlegen. Komplexe Modelle sind nur gerechtfertigt, wenn einfache Modelle deutlich zurückfallen. Viele Produktionssysteme laufen auf logistischer Regression

## Siehe auch {#see-also}

- [[mlops-pipelines]]
- [[ml-production]]
- [[feature-engineering]]
- [[model-evaluation]]

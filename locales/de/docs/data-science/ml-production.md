---
title: "ML in der Produktion"
category: practices
tags: [data-science, mlops, deployment, monitoring, api]
level: 3
source_sha256: 2bfd591ccd3fdc8ff788a13e22de204db37a8945a8fb5e52cd168b33283dcda9
translation: machine
translated_at: '2026-10-24'
---
# ML in der Produktion {#ml-in-production}

Der Weg von einem Notebook zu einem produktiven Modell. Behandelt werden Modellserialisierung, Bereitstellung (Serving), Monitoring sowie die betrieblichen Aspekte, die Prototypen von Produkten unterscheiden.

## Modellserialisierung {#model-serialization}

```python
# Pickle (sklearn, catboost)
import pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Joblib (better for large numpy arrays)
import joblib
joblib.dump(model, 'model.joblib')
model = joblib.load('model.joblib')

# PyTorch
torch.save(model.state_dict(), 'model.pth')
model.load_state_dict(torch.load('model.pth'))

# ONNX (framework-agnostic)
import torch.onnx
torch.onnx.export(model, dummy_input, 'model.onnx')
```

## Modelle bereitstellen {#serving-models}

### Flask/FastAPI {#flaskfastapi}
```python
from fastapi import FastAPI
import pickle

app = FastAPI()
model = pickle.load(open('model.pkl', 'rb'))

@app.post("/predict")
def predict(features: dict):
    X = preprocess(features)
    prediction = model.predict(X)
    return {"prediction": prediction.tolist()}
```

### Batch-Vorhersage {#batch-prediction}
Für Anwendungsfälle ohne Echtzeitanforderung: Vorhersagen nach Zeitplan ausführen und die Ergebnisse in einer Datenbank speichern.

```python
# Batch scoring pipeline
predictions = model.predict(batch_features)
df['prediction'] = predictions
df.to_parquet('predictions.parquet')
```

## Monitoring {#monitoring}

### Data Drift {#data-drift}
Die Merkmale in der Produktion weichen von der Verteilung der Trainingsdaten ab.

- Merkmalsverteilungen zwischen Trainings- und Produktionsdaten vergleichen
- Statistische Tests (KS-Test, PSI) zur Drift-Erkennung überwachen
- Alarm auslösen, wenn der Drift einen Schwellenwert überschreitet

### Modellverschlechterung {#model-degradation}
Die Leistung nimmt mit der Zeit ab, weil sich die Realität verändert.

- Verschiebungen in der Verteilung der Vorhersagen überwachen
- Geschäftskennzahlen verfolgen, die mit der Modellausgabe korrelieren
- Auslöser für das Neutrainieren einrichten (zeitgesteuert oder drift-basiert)

### Logging {#logging}
Jede Vorhersage zusammen mit Merkmalen, Zeitstempel und Modellversion protokollieren, um Fehler zu analysieren und das Neutrainieren vorzubereiten.

## A/B-Tests in der Produktion {#ab-testing-in-production}

1. Einen Anteil des Traffics auf das neue Modell leiten
2. Geschäftskennzahlen zwischen Kontrollgruppe (altes Modell) und Testgruppe (neues Modell) vergleichen
3. Mit statistischen Tests eine Verbesserung bestätigen
4. Den Traffic schrittweise auf den Gewinner erhöhen
5. Nach dem vollständigen Rollout auf Regressionen achten

## Pipeline-Automatisierung {#pipeline-automation}

- **Feature-Pipelines**: automatisierte Berechnung und Speicherung von Merkmalen
- **Trainings-Pipelines**: zeitgesteuertes Neutrainieren mit den aktuellsten Daten
- **Validierungs-Gates**: automatisierte Prüfungen vor dem Deployment
- **Rollback**: die Möglichkeit, schnell auf eine vorherige Modellversion zurückzuwechseln

## Stolpersteine {#gotchas}
- Pickle-Dateien sind nicht sicher – keine nicht vertrauenswürdigen Pickles laden
- Modell und Vorverarbeitung müssen gemeinsam versioniert werden (ein nicht passender Scaler führt zu falschen Vorhersagen)
- Batch-Vorhersagen sind einfacher und für die meisten Anwendungsfälle ausreichend – Echtzeit-Serving nur bauen, wenn es wirklich nötig ist
- Data Drift bedeutet nicht immer eine Modellverschlechterung – vor dem Neutrainieren untersuchen
- Hardwareanforderungen: Für Inferenz genügt meist eine CPU; eine GPU lohnt nur für große neuronale Netze

## Siehe auch {#see-also}
- [[ds-workflow]] - kompletter Projektlebenszyklus
- [[model-evaluation]] - Offline-Evaluation vor dem Deployment
- [[hypothesis-testing]] - A/B-Tests bereitgestellter Modelle
- [[gradient-boosting]] - gängige Produktionsmodelle

---
title: "MLOps und Feature Store"
category: concepts
tags: [data-engineering, mlops, feature-store, mlflow, model-serving]
level: 2
source_sha256: b8b9525cfb2a439216957cebb310c07229a58e5476a050348e8f30dcd8458bf6
translation: machine
translated_at: '2026-10-24'
---
# MLOps und Feature Store {#mlops-and-feature-store}

MLOps verbindet Data Engineering und Machine Learning und umfasst Experiment-Tracking, Modellversionierung, Feature-Management und Model Serving. Data Engineers bauen die Infrastruktur, auf die ML-Teams angewiesen sind.

## CRISP-DM-Methodik {#crisp-dm-methodology}

1. Business Understanding -> 2. Data Understanding -> 3. Data Preparation -> 4. Modeling -> 5. Evaluation -> 6. Deployment

## Feature Store {#feature-store}

Zentrales Repository für Features, Funktionen zur Feature-Erstellung, Modelle und Datensätze.

| Komponente | Beschreibung |
|-----------|-------------|
| **Transformations** | Vorberechnete und on-demand Feature-Transformationen |
| **Storage** | Online (Redis, DynamoDB) für Serving; Offline (S3, HDFS, BigQuery) für Training |
| **Serving** | Feature-Set-Konfiguration für die Vorbereitung zur Inferenzzeit |
| **Registry** | Metadaten zu Modellen, Datensätzen, Experimenten |
| **Monitoring** | Überwachung der Daten- und Modellqualität |

## MLflow-Plattform {#mlflow-platform}

Vier Kernmodule:

| Modul | Zweck |
|--------|---------|
| **Models** | Standardisiertes Packaging-Format (MLmodel, model.pkl, conda.yaml) |
| **Projects** | Reproduzierbare Code-Organisation |
| **Tracking** | Parameter, Metriken und Code-Versionen protokollieren |
| **Model Registry** | Zentraler Modellspeicher mit Versionierung |

### Experiment-Tracking mit PySpark {#experiment-tracking-with-pyspark}

```python
import mlflow
mlflow.set_tracking_uri("https://mlflow.example.com")
mlflow.set_experiment("PySpark-ML")

mlflow.start_run()
mlflow.log_param('MaxDepth', model.stages[-1].getMaxDepth())
mlflow.log_metric('accuracy', accuracy)
mlflow.log_metric('f1', f1_score)
mlflow.spark.log_model(model, "spark-model", registered_model_name="spark-model")
mlflow.end_run()

# Auto-tracking
mlflow.pyspark.ml.autolog()
pipeline.fit(train)  # triggers auto-tracking
```

## Model Serving {#model-serving}

| Ansatz | Anwendungsfall |
|----------|----------|
| **Microservices** | REST-API (Flask/FastAPI), Docker, K8s |
| **Embedded** | Deployment auf Edge-Geräten und Mobilgeräten |
| **Spark Pipeline** | Batch-Scoring auf großen Datensätzen |

## ML-Versionierung {#ml-versioning}

Anders als bei Software ist die neueste Modellversion nicht zwangsläufig die beste. Version = laufende Nummer des Experiments.

**Was versioniert wird:** Datensätze, Feature-Funktionen, trainierte Modelle, Trainingsjobs, Experimente.

**Tools:** ClearML, DVC, MLflow, Kubeflow Pipelines, Prefect, Dagster.

## Gotchas {#gotchas}
- ML-Versionierung unterscheidet sich von Software-Versionierung - neuer heißt nicht besser
- Online- vs. Offline-Storage im Feature Store erfüllt unterschiedliche Latenzanforderungen
- Model Serving über eine Spark Pipeline eignet sich am besten für Batch, nicht für Echtzeit
- Modellartefakte immer zusammen mit Metriken protokollieren, um Reproduzierbarkeit sicherzustellen

## Siehe auch {#see-also}
- [[apache-spark-core]] - Spark-ML-Integration
- [[etl-elt-pipelines]] - Muster für Feature-Pipelines
- [[kubernetes-for-de]] - Serving-Infrastruktur
- [[data-quality]] - Modell-Monitoring

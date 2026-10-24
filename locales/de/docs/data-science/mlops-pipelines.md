---
title: "MLOps und ML-Pipelines"
category: tools
tags: [data-science, mlops, mlflow, model-serving, ci-cd, feature-store]
level: 3
source_sha256: b405e90477625acddcd78b28cc49559d17640e91688d4d953fe511a32527c568
translation: machine
translated_at: '2026-10-24'
---
# MLOps und ML-Pipelines {#mlops-and-ml-pipelines}

MLOps überträgt DevOps-Prinzipien auf maschinelles Lernen: Versionierung von Daten und Modellen, automatisierte Trainingspipelines, Monitoring im Produktivbetrieb und reproduzierbare Experimente. Die Lücke zwischen Notebook-Prototyp und Produktivsystem ist der Punkt, an dem die meisten ML-Projekte scheitern.

## Experiment-Tracking {#experiment-tracking}

### MLflow {#mlflow}

```python
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("fraud-detection-v2")

with mlflow.start_run(run_name="xgboost-baseline"):
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 6)
    mlflow.log_param("learning_rate", 0.1)

    model = XGBClassifier(**params)
    model.fit(X_train, y_train)

    # Log metrics
    y_pred = model.predict(X_test)
    mlflow.log_metric("f1", f1_score(y_test, y_pred))
    mlflow.log_metric("auprc", average_precision_score(y_test, y_pred))

    # Log model artifact
    mlflow.sklearn.log_model(model, "model")

    # Log data artifact
    mlflow.log_artifact("feature_config.yaml")
```

### Weights & Biases (wandb) {#weights-biases-wandb}

```python
import wandb

wandb.init(project="fraud-detection", config={"lr": 0.01, "epochs": 50})

for epoch in range(50):
    train_loss = train_one_epoch(model, train_loader)
    val_loss = evaluate(model, val_loader)
    wandb.log({"train_loss": train_loss, "val_loss": val_loss, "epoch": epoch})

wandb.finish()
```

## Feature Store {#feature-store}

Zentrales Repository für Feature-Definitionen und berechnete Werte. Verhindert Feature-Skew zwischen Training und Serving.

```python
# Feast example
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")

# Define features
entity = Entity(name="customer_id", value_type=ValueType.INT64)

customer_features = FeatureView(
    name="customer_features",
    entities=[entity],
    schema=[
        Field(name="total_transactions_30d", dtype=Float32),
        Field(name="avg_transaction_amount", dtype=Float32),
        Field(name="account_age_days", dtype=Int64)],
    source=BigQuerySource(table="project.dataset.customer_features"),
)

# Retrieve features for training
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=["customer_features:total_transactions_30d",
              "customer_features:avg_transaction_amount"],
).to_df()

# Online serving (low-latency)
feature_vector = store.get_online_features(
    features=["customer_features:total_transactions_30d"],
    entity_rows=[{"customer_id": 12345}],
).to_dict()
```

## Model Registry {#model-registry}

Modelle versionieren, Herkunft nachverfolgen und Freigabestufen verwalten.

```python
# MLflow Model Registry
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
model_uri = f"runs:/{run_id}/model"
mlflow.register_model(model_uri, "fraud-detector")

# Promote to production
client.transition_model_version_stage(
    name="fraud-detector",
    version=3,
    stage="Production"
)

# Load production model
model = mlflow.pyfunc.load_model("models:/fraud-detector/Production")
```

## Model Serving {#model-serving}

### FastAPI-Serving {#fastapi-serving}

```python
from fastapi import FastAPI
import mlflow.pyfunc
import numpy as np

app = FastAPI()
model = mlflow.pyfunc.load_model("models:/fraud-detector/Production")

@app.post("/predict")
async def predict(features: dict):
    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)
    return {"prediction": int(prediction[0]),
            "model_version": "3"}
```

### BentoML (Batching und Serving) {#bentoml-batching-serving}

```python
import bentoml

# Save model
saved_model = bentoml.sklearn.save_model("fraud_model", model)

# Service definition
@bentoml.service
class FraudDetector:
    model_ref = bentoml.models.get("fraud_model:latest")

    @bentoml.api(batchable=True, max_batch_size=100)
    def predict(self, inputs: np.ndarray) -> np.ndarray:
        return self.model_ref.predict(inputs)
```

## Model-Monitoring {#model-monitoring}

### Data-Drift-Erkennung {#data-drift-detection}

```python
from evidently import ColumnDriftMetric
from evidently.report import Report

# Compare training vs production distributions
drift_report = Report(metrics=[
    ColumnDriftMetric(column_name="transaction_amount"),
    ColumnDriftMetric(column_name="merchant_category")])
drift_report.run(reference_data=train_df, current_data=production_df)
drift_report.save_html("drift_report.html")
```

**Wichtige Metriken zur Überwachung:**
- **Data Drift**: Verteilungen der Eingabe-Features verschieben sich (KS-Test, PSI)
- **Concept Drift**: Der Zusammenhang zwischen Features und Zielgröße ändert sich
- **Prediction Drift**: Die Verteilung der Modellausgaben ändert sich
- **Leistungsverschlechterung**: Die tatsächlichen Metriken sinken (erfordert Ground Truth)

## Pipeline-Orchestrierung {#pipeline-orchestration}

### Prefect-/Airflow-Muster {#prefect-airflow-pattern}

```python
# Prefect pipeline example
from prefect import flow, task

@task
def load_data():
    return pd.read_parquet("s3://data/transactions.parquet")

@task
def preprocess(df):
    return feature_pipeline.transform(df)

@task
def train_model(X, y):
    model = XGBClassifier()
    model.fit(X, y)
    return model

@task
def evaluate_and_register(model, X_test, y_test):
    score = model.score(X_test, y_test)
    if score > 0.85:  # quality gate
        mlflow.sklearn.log_model(model, "model")
        return True
    return False

@flow(name="training-pipeline")
def training_pipeline():
    df = load_data()
    X, y = preprocess(df)
    model = train_model(X, y)
    evaluate_and_register(model, X, y)
```

## CI/CD für ML {#cicd-for-ml}

- **Datenvalidierung**: Great Expectations oder Pandera prüfen die Eingangsdaten
- **Modellvalidierung**: Automatisierte Tests auf einem Holdout-Set, A/B-Test-Framework
- **Shadow Deployment**: Neues Modell läuft parallel zur Produktion, Ausgaben werden verglichen
- **Canary Deployment**: Ein kleiner Anteil des Traffics wird an das neue Modell geleitet und dessen Metriken werden überwacht

## Fallstricke {#gotchas}

- **Training-Serving-Skew**: Features werden im Training (Batch-SQL) anders berechnet als im Serving (Echtzeit). Feature Stores lösen dieses Problem, erhöhen aber die Komplexität. Mindestens sollte der Feature-Engineering-Code zwischen Training- und Serving-Codepfaden geteilt werden
- **Modell-Veralterung**: Modelle verschlechtern sich stillschweigend. Richten Sie automatisierte Retraining-Trigger ein, die auf Drift-Metriken oder einem Kalenderplan basieren. Ohne Monitoring kann ein Modell monatelang fehlerhafte Vorhersagen liefern, bevor es jemand bemerkt
- **Reproduzierbarkeit erfordert mehr als Code-Versionierung**: Random Seeds fixieren, Bibliotheksversionen protokollieren, Trainingsdaten versionieren (DVC oder ähnliche Werkzeuge) und Preprocessing-Parameter protokollieren. Ein Modell, das sich nicht reproduzieren lässt, lässt sich auch nicht debuggen

## Siehe auch {#see-also}

- [[ml-production]]
- [[model-evaluation]]
- [[feature-engineering]]

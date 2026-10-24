---
title: "MLOps et pipelines de ML"
category: tools
tags: [data-science, mlops, mlflow, model-serving, ci-cd, feature-store]
level: 3
source_sha256: b405e90477625acddcd78b28cc49559d17640e91688d4d953fe511a32527c568
translation: machine
translated_at: '2026-10-24'
---
# MLOps et pipelines de ML {#mlops-and-ml-pipelines}

Le MLOps applique les principes du DevOps au machine learning : gestion de versions pour les données et les modèles, pipelines d'entraînement automatisés, supervision en production et expériences reproductibles. L'écart entre le prototype en notebook et le système en production est là où échoue la plupart des projets de ML.

## Suivi des expériences {#experiment-tracking}

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

Dépôt centralisé des définitions de features et des valeurs calculées. Empêche le skew de features entre l'entraînement et le serving.

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

## Registre de modèles {#model-registry}

Versionner les modèles, suivre leur lignage et gérer les étapes de promotion.

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

## Mise à disposition des modèles {#model-serving}

### Serving avec FastAPI {#fastapi-serving}

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

### BentoML (batching + serving) {#bentoml-batching-serving}

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

## Supervision des modèles {#model-monitoring}

### Détection de la dérive des données {#data-drift-detection}

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

**Principales métriques à surveiller :**
- **Dérive des données** : évolution des distributions des features en entrée (test de KS, PSI)
- **Dérive conceptuelle** : évolution de la relation entre les features et la cible
- **Dérive des prédictions** : évolution de la distribution des sorties du modèle
- **Dégradation des performances** : baisse des métriques réelles (nécessite la vérité terrain)

## Orchestration des pipelines {#pipeline-orchestration}

### Motif Prefect / Airflow {#prefect-airflow-pattern}

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

## CI/CD pour le ML {#cicd-for-ml}

- **Validation des données** : contrôles Great Expectations ou Pandera sur les données en entrée
- **Validation des modèles** : tests automatisés sur un jeu de validation (holdout), cadre de test A/B
- **Déploiement fantôme (shadow)** : exécuter le nouveau modèle en parallèle de la production et comparer les sorties
- **Déploiement canari** : router un faible pourcentage du trafic vers le nouveau modèle et surveiller les métriques

## Pièges courants {#gotchas}

- **Skew entraînement-serving** : les features sont calculées différemment à l'entraînement (SQL par lots) et au serving (temps réel). Les feature stores résolvent ce problème mais ajoutent de la complexité. À minima, partager le code d'ingénierie des features entre les chemins d'entraînement et de serving
- **Obsolescence du modèle** : les modèles se dégradent silencieusement. Mettre en place des déclencheurs de réentraînement automatiques basés sur les métriques de dérive ou un calendrier. Sans supervision, un modèle peut servir de mauvaises prédictions pendant des mois avant que quiconque ne s'en aperçoive
- **La reproductibilité exige plus que le versionnement du code** : fixer les graines aléatoires, journaliser les versions des bibliothèques, versionner les données d'entraînement (DVC ou équivalent), journaliser les paramètres de prétraitement. Un modèle que l'on ne peut pas reproduire est un modèle que l'on ne peut pas déboguer

## Voir aussi {#see-also}

- [[ml-production]]
- [[model-evaluation]]
- [[feature-engineering]]

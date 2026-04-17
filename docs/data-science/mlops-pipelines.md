---
title: MLOps and ML Pipelines
category: tools
tags: [data-science, mlops, mlflow, model-serving, ci-cd, feature-store]
---

# MLOps and ML Pipelines

MLOps applies DevOps principles to machine learning: version control for data/models, automated training pipelines, monitoring in production, and reproducible experiments. The gap between notebook prototype and production system is where most ML projects fail.

## Experiment Tracking

### MLflow

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

### Weights & Biases (wandb)

```python
import wandb

wandb.init(project="fraud-detection", config={"lr": 0.01, "epochs": 50})

for epoch in range(50):
    train_loss = train_one_epoch(model, train_loader)
    val_loss = evaluate(model, val_loader)
    wandb.log({"train_loss": train_loss, "val_loss": val_loss, "epoch": epoch})

wandb.finish()
```

## Feature Store

Centralized repository for feature definitions and computed values. Prevents feature skew between training and serving.

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

## Model Registry

Version models, track lineage, manage promotion stages.

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

## Model Serving

### FastAPI Serving

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

### BentoML (Batching + Serving)

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

## Model Monitoring

### Data Drift Detection

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

**Key metrics to monitor:**
- **Data drift**: input feature distributions shift (KS-test, PSI)
- **Concept drift**: relationship between features and target changes
- **Prediction drift**: model output distribution changes
- **Performance degradation**: actual metrics drop (requires ground truth)

## Pipeline Orchestration

### Prefect / Airflow Pattern

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

## CI/CD for ML

- **Data validation**: Great Expectations or Pandera checks on input data
- **Model validation**: automated tests on holdout set, A/B test framework
- **Shadow deployment**: run new model alongside production, compare outputs
- **Canary deployment**: route small % of traffic to new model, monitor metrics

## Gotchas

- **Training-serving skew**: features computed differently in training (batch SQL) vs serving (real-time). Feature stores solve this but add complexity. At minimum, share feature engineering code between training and serving codepaths
- **Model staleness**: models degrade silently. Set up automated retraining triggers based on drift metrics or calendar schedule. Without monitoring, a model can serve bad predictions for months before anyone notices
- **Reproducibility requires more than code versioning**: pin random seeds, log library versions, version the training data (DVC or similar), log preprocessing parameters. A model you cannot reproduce is a model you cannot debug

## See Also

- [[ml-production]]
- [[model-evaluation]]
- [[feature-engineering]]

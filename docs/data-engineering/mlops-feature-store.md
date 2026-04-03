---
title: MLOps and Feature Store
category: concepts
tags: [data-engineering, mlops, feature-store, mlflow, model-serving]
---

# MLOps and Feature Store

MLOps bridges data engineering and machine learning, covering experiment tracking, model versioning, feature management, and model serving. Data engineers build the infrastructure that ML teams depend on.

## CRISP-DM Methodology

1. Business Understanding -> 2. Data Understanding -> 3. Data Preparation -> 4. Modeling -> 5. Evaluation -> 6. Deployment

## Feature Store

Central repository for features, feature-building functions, models, and datasets.

| Component | Description |
|-----------|-------------|
| **Transformations** | Precomputed and on-demand feature transforms |
| **Storage** | Online (Redis, DynamoDB) for serving; Offline (S3, HDFS, BigQuery) for training |
| **Serving** | Feature set config for inference-time preparation |
| **Registry** | Metadata about models, datasets, experiments |
| **Monitoring** | Data/model quality monitoring |

## MLflow Platform

Four core modules:

| Module | Purpose |
|--------|---------|
| **Models** | Standard packaging format (MLmodel, model.pkl, conda.yaml) |
| **Projects** | Reproducible code organization |
| **Tracking** | Log parameters, metrics, code versions |
| **Model Registry** | Centralized model store with versioning |

### Experiment Tracking with PySpark

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

## Model Serving

| Approach | Use Case |
|----------|----------|
| **Microservices** | REST API (Flask/FastAPI), Docker, K8s |
| **Embedded** | Edge/mobile deployment |
| **Spark Pipeline** | Batch scoring on large datasets |

## ML Versioning

Unlike software, latest model version is not necessarily best. Version = experiment ordinal number.

**What to version:** datasets, feature functions, trained models, training jobs, experiments.

**Tools:** ClearML, DVC, MLflow, Kubeflow Pipelines, Prefect, Dagster.

## Gotchas
- ML versioning differs from software versioning - newer != better
- Feature Store online vs offline storage serves different latency requirements
- Model serving via Spark pipeline is best for batch, not real-time
- Always log model artifacts alongside metrics for reproducibility

## See Also
- [[apache-spark-core]] - Spark ML integration
- [[etl-elt-pipelines]] - feature pipeline patterns
- [[kubernetes-for-de]] - serving infrastructure
- [[data-quality]] - model monitoring

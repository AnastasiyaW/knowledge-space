---
title: "MLOps et Feature Store"
category: concepts
tags: [data-engineering, mlops, feature-store, mlflow, model-serving]
level: 2
source_sha256: b8b9525cfb2a439216957cebb310c07229a58e5476a050348e8f30dcd8458bf6
translation: machine
translated_at: '2026-10-24'
---
# MLOps et Feature Store {#mlops-and-feature-store}

MLOps fait le lien entre l'ingénierie des données et le machine learning, en couvrant le suivi des expériences, le versionnement des modèles, la gestion des features et le service des modèles. Les data engineers construisent l'infrastructure dont dépendent les équipes ML.

## Méthodologie CRISP-DM {#crisp-dm-methodology}

1. Business Understanding -> 2. Data Understanding -> 3. Data Preparation -> 4. Modeling -> 5. Evaluation -> 6. Deployment

## Feature Store {#feature-store}

Dépôt central pour les features, les fonctions de construction de features, les modèles et les jeux de données.

| Composant | Description |
|-----------|-------------|
| **Transformations** | Transformations de features précalculées et à la demande |
| **Storage** | En ligne (Redis, DynamoDB) pour le service ; hors ligne (S3, HDFS, BigQuery) pour l'entraînement |
| **Serving** | Configuration des ensembles de features pour la préparation au moment de l'inférence |
| **Registry** | Métadonnées sur les modèles, les jeux de données, les expériences |
| **Monitoring** | Surveillance de la qualité des données et des modèles |

## Plateforme MLflow {#mlflow-platform}

Quatre modules principaux :

| Module | Rôle |
|--------|---------|
| **Models** | Format de packaging standard (MLmodel, model.pkl, conda.yaml) |
| **Projects** | Organisation reproductible du code |
| **Tracking** | Journalisation des paramètres, des métriques et des versions de code |
| **Model Registry** | Magasin centralisé de modèles avec versionnement |

### Suivi des expériences avec PySpark {#experiment-tracking-with-pyspark}

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

## Service des modèles {#model-serving}

| Approche | Cas d'usage |
|----------|----------|
| **Microservices** | API REST (Flask/FastAPI), Docker, K8s |
| **Embarqué** | Déploiement en edge ou sur mobile |
| **Spark Pipeline** | Scoring par lots sur de grands jeux de données |

## Versionnement des modèles de ML {#ml-versioning}

Contrairement au logiciel, la dernière version d'un modèle n'est pas forcément la meilleure. La version correspond au numéro ordinal de l'expérience.

**Ce qu'il faut versionner :** les jeux de données, les fonctions de features, les modèles entraînés, les jobs d'entraînement, les expériences.

**Outils :** ClearML, DVC, MLflow, Kubeflow Pipelines, Prefect, Dagster.

## Pièges à éviter {#gotchas}
- Le versionnement ML diffère du versionnement logiciel : plus récent ne signifie pas meilleur
- Le stockage en ligne et hors ligne du Feature Store répond à des exigences de latence différentes
- Le service de modèles via un pipeline Spark convient au traitement par lots, pas au temps réel
- Journalisez toujours les artefacts de modèle avec les métriques pour garantir la reproductibilité

## Voir aussi {#see-also}
- [[apache-spark-core]] - intégration de Spark ML
- [[etl-elt-pipelines]] - patterns de pipelines de features
- [[kubernetes-for-de]] - infrastructure de service
- [[data-quality]] - surveillance des modèles

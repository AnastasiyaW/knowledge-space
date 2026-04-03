---
title: Spark ML
category: concepts
tags: [spark-ml, mllib, pipeline, transformer, estimator, distributed-ml]
---

# Spark ML

Spark ML is the machine learning library in [[apache-spark]] built on top of [[spark-sql-and-dataframes]]. It provides a Pipeline API with Transformers, Estimators, and Evaluators for scalable feature engineering, model training, and prediction.

## Key Facts

- **Spark ML** (DataFrame-based) replaced **Spark MLlib** (RDD-based) starting from Spark 2.0. Always use `pyspark.ml`, not `pyspark.mllib`
- **Transformer**: transforms one DataFrame into another. Has a `.transform(df)` method. Examples: trained model, VectorAssembler, StringIndexer (after fitting)
- **Estimator**: fits on data to produce a Transformer. Has a `.fit(df)` method. Examples: LinearRegression, StringIndexer (before fitting), Pipeline
- **Pipeline**: chain of Transformers and Estimators executed sequentially. `pipeline.fit(train_df)` returns a PipelineModel (a Transformer)
- **VectorAssembler**: combines multiple feature columns into a single `features` vector column required by all Spark ML algorithms
- **Evaluator**: computes quality metrics. RegressionEvaluator (RMSE, MAE, R2), BinaryClassificationEvaluator (AUROC), MulticlassClassificationEvaluator (accuracy, F1)
- **Hyperparameter tuning**: `CrossValidator` (k-fold CV) and `TrainValidationSplit` (single train/validation split). Both accept ParamGrid and Evaluator
- All components are **stateless** - state is captured in the fitted model, not the estimator
- Supported model types: regression, classification, clustering, decision trees, ensembles (GBT, Random Forest), collaborative filtering (ALS)

## Patterns

### Full ML Pipeline

```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator

# Feature engineering stages
indexer = StringIndexer(inputCol="platform", outputCol="platform_idx")
assembler = VectorAssembler(
    inputCols=["platform_idx", "impressions", "clicks"],
    outputCol="features"
)
gbt = GBTRegressor(featuresCol="features", labelCol="ctr", maxIter=50)

# Build and train pipeline
pipeline = Pipeline(stages=[indexer, assembler, gbt])
model = pipeline.fit(train_df)

# Predict and evaluate
predictions = model.transform(test_df)
evaluator = RegressionEvaluator(labelCol="ctr", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(f"RMSE: {rmse}")
```

### Hyperparameter tuning with CrossValidator

```python
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

paramGrid = (ParamGridBuilder()
    .addGrid(gbt.maxDepth, [5, 10, 15])
    .addGrid(gbt.maxIter, [20, 50, 100])
    .build())

cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=paramGrid,
    evaluator=evaluator,
    numFolds=5
)

cv_model = cv.fit(train_df)
best_model = cv_model.bestModel
```

### Save and load model

```python
# Save
model.write().overwrite().save("hdfs:///models/ctr_predictor_v1")

# Load
from pyspark.ml import PipelineModel
loaded_model = PipelineModel.load("hdfs:///models/ctr_predictor_v1")
predictions = loaded_model.transform(new_data)
```

## Gotchas

- VectorAssembler output column must be named `features` (or explicitly set via `featuresCol` parameter on the model). Missing this step is the #1 beginner error
- StringIndexer assigns indices by frequency (most frequent = 0). This introduces unintended ordinal relationships. Use OneHotEncoder after StringIndexer for categorical features in linear models
- Spark ML models are not TensorFlow/PyTorch models. They are optimized for tabular data and linear/tree-based algorithms. For deep learning on Spark, use Horovod or RAPIDS
- `CrossValidator` with large ParamGrid on big data is expensive: `k * len(paramGrid)` full training runs. Start with TrainValidationSplit for quick experiments
- `fetchall()` on JDBC returns all rows to driver - when preprocessing data for ML, always use Spark's distributed reads

## See Also

- [[apache-spark]] - Spark architecture and SparkSession
- [[spark-sql-and-dataframes]] - DataFrame operations for feature engineering
- [[data-formats]] - Parquet for storing train/test splits
- https://spark.apache.org/docs/latest/ml-guide.html - Spark ML documentation

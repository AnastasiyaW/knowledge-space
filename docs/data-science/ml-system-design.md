---
title: ML System Design
category: patterns
tags: [data-science, system-design, architecture, scalability, production-ml]
---

# ML System Design

Designing end-to-end ML systems that work in production. Covers problem framing, data pipeline, model selection, serving architecture, and monitoring. The model is typically < 10% of the total system complexity.

## Problem Framing

Before any modeling, define:

1. **Business objective**: what metric moves the needle (revenue, engagement, cost)?
2. **ML objective**: what does the model predict? (classification, ranking, regression)
3. **Data availability**: what labeled data exists? Can you generate labels?
4. **Constraints**: latency budget, compute budget, fairness requirements
5. **Baseline**: what non-ML solution exists? (rules, heuristics)

**Common framings:**
- Spam detection -> binary classification
- Search ranking -> learning to rank (pairwise or listwise)
- Recommendation -> collaborative filtering + content-based, served as ranking
- Fraud -> anomaly detection + supervised classification
- ETA prediction -> regression with confidence intervals

## Data Pipeline Architecture

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

### Data Validation

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

## Feature Engineering Patterns

### Temporal Features

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

### Interaction Features

```python
# Ratios, differences, products between features
df['price_per_sqft'] = df['price'] / df['sqft']
df['income_to_debt'] = df['income'] / (df['debt'] + 1)
df['recency_x_frequency'] = df['days_since_last'] * df['purchase_count']
```

### Target Encoding (for high-cardinality categoricals)

```python
from category_encoders import TargetEncoder

te = TargetEncoder(cols=['zip_code', 'merchant_id'], smoothing=10)
X_encoded = te.fit_transform(X_train, y_train)
# Use same encoder on test: te.transform(X_test)
```

## Model Selection Decision Tree

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

## Serving Architectures

### Online Serving (Real-Time)

- Latency < 100ms per request
- REST API (FastAPI, Flask) or gRPC
- Model loaded in memory, precomputed features from feature store
- Horizontal scaling behind load balancer

### Batch Serving

- Process all data periodically (hourly/daily)
- Cheaper, simpler, higher throughput
- Use for recommendations, email targeting, report generation
- Store predictions in database/cache for lookup

### Streaming (Near Real-Time)

- Process events as they arrive (Kafka/Flink)
- For fraud detection, real-time personalization
- Model deployed as stream processor

## A/B Testing ML Models

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

**Statistical power**: need enough samples for reliable results. For small effect sizes (< 1% lift), may need millions of observations. Use sequential testing to stop early if results are clear.

## Feedback Loops

- **Direct feedback**: user clicks / doesn't click -> label within minutes
- **Delayed feedback**: fraud confirmed days/weeks later
- **Implicit feedback**: no negative signal (user didn't complain != user is happy)
- **Feedback loop danger**: model influences what data it sees. Recommendation model that never shows item X will never learn if X is good

## Monitoring Checklist

| What | How | Alert When |
|------|-----|------------|
| Input data quality | Schema validation, null checks | Schema violation, null rate > threshold |
| Feature drift | KS-test, PSI on feature distributions | p-value < 0.001 or PSI > 0.2 |
| Prediction drift | Distribution of model outputs | Mean/variance shift beyond 2 sigma |
| Model performance | Actual vs predicted (when labels available) | Metric drops > 5% from baseline |
| Latency | P50/P95/P99 response time | P99 > SLA |
| Throughput | Requests per second | Drop > 20% from normal |

## Gotchas

- **Training-serving skew is the #1 production ML bug**: feature computed differently offline (SQL with full history) vs online (real-time with partial data). Use a feature store or shared feature engineering code. Test by comparing offline predictions with production predictions on same inputs
- **Feedback loop bias**: if a fraud model blocks transactions, you never see outcomes of blocked ones. Train on biased data -> reinforce existing biases. Randomly let through small % of flagged cases (exploration) or use causal inference techniques
- **Premature optimization**: start with simplest model that could work (logistic regression, single tree). Establish baseline metrics. Complex models justified only when simple ones clearly fall short. Many production systems run on logistic regression

## See Also

- [[mlops-pipelines]]
- [[ml-production]]
- [[feature-engineering]]
- [[model-evaluation]]

---
title: ML in Production
category: practices
tags: [data-science, mlops, deployment, monitoring, api]
---

# ML in Production

Taking a model from notebook to production. Covers model serialization, serving, monitoring, and the operational concerns that separate prototypes from products.

## Model Serialization

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

## Serving Models

### Flask/FastAPI
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

### Batch Prediction
For non-real-time use cases: run predictions on schedule, store results in database.

```python
# Batch scoring pipeline
predictions = model.predict(batch_features)
df['prediction'] = predictions
df.to_parquet('predictions.parquet')
```

## Monitoring

### Data Drift
Features in production diverge from training distribution.

- Compare feature distributions between training and production data
- Monitor statistical tests (KS test, PSI) for drift detection
- Alert when drift exceeds threshold

### Model Degradation
Performance declines over time as world changes.

- Monitor prediction distribution shifts
- Track business metrics correlated with model output
- Set up retraining triggers (scheduled or drift-based)

### Logging
Log every prediction with features, timestamp, and model version for debugging and retraining.

## A/B Testing in Production

1. Route fraction of traffic to new model
2. Compare business metrics between control (old) and test (new)
3. Use statistical tests to confirm improvement
4. Gradually increase traffic to winner
5. Monitor for regression after full rollout

## Pipeline Automation

- **Feature pipelines**: automated feature computation and storage
- **Training pipelines**: scheduled retraining with latest data
- **Validation gates**: automated checks before deployment
- **Rollback**: ability to quickly revert to previous model version

## Gotchas
- Pickle files are not secure - don't load untrusted pickles
- Model + preprocessing must be versioned together (scaler mismatch = wrong predictions)
- Batch prediction is simpler and sufficient for most use cases - don't build real-time serving unless needed
- Data drift doesn't always mean model degradation - investigate before retraining
- Hardware requirements: CPU usually sufficient for inference; GPU only for large neural networks

## See Also
- [[ds-workflow]] - full project lifecycle
- [[model-evaluation]] - offline evaluation before deployment
- [[hypothesis-testing]] - A/B testing deployed models
- [[gradient-boosting]] - common production models

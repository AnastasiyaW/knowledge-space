---
title: Bias-Variance Tradeoff
category: concepts
tags: [data-science, ml, overfitting, underfitting, regularization]
---

# Bias-Variance Tradeoff

The fundamental tension in machine learning: models that are too simple miss patterns (bias), models that are too complex memorize noise (variance). Every modeling decision is a point on this spectrum.

## Definitions

**Bias** = systematic error. How far off predictions are on average from true values.
- High bias = underfitting (model too simple, misses patterns)
- Example: fitting linear regression to quadratic data

**Variance** = how much predictions fluctuate across different training sets.
- High variance = overfitting (model captures noise, not signal)
- Example: degree-10 polynomial on 20 data points

**Total error = Bias^2 + Variance + Irreducible noise**

## Diagnosis

| Symptom | Diagnosis | Solution |
|---------|-----------|----------|
| High train error, high val error | Underfitting (high bias) | More complex model, more features |
| Low train error, high val error | Overfitting (high variance) | Regularization, more data, simpler model |
| Low train error, low val error | Good fit | Ship it |
| High train error, low val error | Impossible (data leakage?) | Check for bugs |

**Learning curves**: plot train/val error vs training set size.
- Converge at high error -> bias problem (more data won't help, need better model)
- Large gap -> variance problem (more data will help)

## Model Complexity Spectrum

Low complexity <---------> High complexity
Linear regression --- Polynomial --- Decision tree --- Deep forest --- Neural net

Low bias, high variance <--> High bias, low variance

## Managing the Tradeoff

### Reduce Variance (fight overfitting)
- **Regularization**: L1/L2 penalties on model weights
- **Dropout**: randomly zero out neurons during training
- **Early stopping**: stop training when validation loss increases
- **Cross-validation**: robust performance estimate
- **More training data**: best remedy for overfitting
- **Ensemble methods**: averaging reduces variance (Random Forest, Bagging)
- **Feature selection**: remove noisy/irrelevant features
- **Simpler model**: fewer parameters, shallower trees

### Reduce Bias (fight underfitting)
- **More complex model**: deeper trees, more layers
- **More/better features**: feature engineering
- **Less regularization**: reduce penalty
- **Ensemble methods**: boosting reduces bias (Gradient Boosting, AdaBoost)
- **Train longer**: more epochs/iterations

## Ensemble Methods and the Tradeoff

- **Bagging** (Random Forest): trains multiple models independently, averages them. Reduces VARIANCE
- **Boosting** (Gradient Boosting): trains models sequentially, each correcting prior errors. Reduces BIAS

This is why gradient boosting (reduces bias) + regularization (controls variance) is so powerful.

## Gotchas
- "More data" helps variance but NOT bias - if model is too simple, more data won't fix it
- Regularization is NOT free - too much regularization increases bias
- Validation set overfitting is real - heavy hyperparameter tuning on the same val set
- Neural networks challenge the classical tradeoff - very large models can generalize well (double descent phenomenon)
- Cross-validation gives a better estimate than single split but is slower

## See Also
- [[model-evaluation]] - detecting overfitting
- [[feature-engineering]] - regularization techniques
- [[gradient-boosting]] - practical bias-variance management
- [[neural-networks]] - regularization in deep learning

---
title: Bayesian Methods in ML
category: concepts
tags: [data-science, bayesian, naive-bayes, inference, prior]
---

# Bayesian Methods in ML

Bayesian thinking updates beliefs with evidence. From simple Naive Bayes classification to Bayesian inference, these methods provide principled uncertainty quantification.

## Bayes' Theorem Applied

P(hypothesis | data) = P(data | hypothesis) * P(hypothesis) / P(data)

- **Prior** P(hypothesis): what we believe before seeing data
- **Likelihood** P(data | hypothesis): probability of data given hypothesis
- **Posterior** P(hypothesis | data): updated belief after seeing data
- **Evidence** P(data): normalizing constant

## Naive Bayes Classifier

P(class | features) proportional to P(class) * product(P(feature_i | class))

"Naive" assumption: features are conditionally independent given class. Often violated but works surprisingly well.

```python
from sklearn.naive_bayes import GaussianNB, MultinomialNB

# Gaussian: continuous features (assumes normal distribution)
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# Multinomial: count features (great for text/TF-IDF)
mnb = MultinomialNB()
mnb.fit(X_train_tfidf, y_train)
```

**Best for**: text classification (spam filtering, sentiment), when training data is small, when you need fast training.

### Why It Works Despite Wrong Assumption
- Classification only needs to rank probabilities correctly, not estimate them precisely
- Feature dependencies often cancel out across classes
- With limited data, simpler models generalize better

## Bayesian vs Frequentist

| Aspect | Frequentist | Bayesian |
|--------|-------------|----------|
| Parameters | Fixed, unknown | Random variables with distributions |
| Data | Random (repeated sampling) | Fixed (observed) |
| Inference | Point estimate + CI | Full posterior distribution |
| Prior knowledge | Not incorporated | Explicitly incorporated |
| Uncertainty | Confidence intervals | Credible intervals |

## Bayesian Inference

Instead of point estimates, compute full posterior distribution of parameters.

**Conjugate priors**: prior and posterior have same family.
- Normal likelihood + Normal prior -> Normal posterior
- Binomial likelihood + Beta prior -> Beta posterior

**MCMC (Markov Chain Monte Carlo)**: sample from posterior when analytical solution is intractable.

## Applications in Data Science

- **A/B testing**: Bayesian A/B testing gives probability that B is better than A (more intuitive than p-values)
- **Hyperparameter tuning**: Bayesian optimization (Optuna, Hyperopt)
- **Spam filtering**: Naive Bayes with word frequencies
- **Medical diagnosis**: prior disease prevalence + test sensitivity
- **Recommendation systems**: Bayesian personalization

## Gotchas
- Naive Bayes assumes feature independence - correlation between features hurts performance
- Prior choice matters, especially with small data
- MCMC can be slow to converge for complex models
- Log-space computation essential to avoid numerical underflow (product of many small probabilities)
- Multinomial NB requires non-negative features (counts, TF-IDF)

## See Also
- [[probability-distributions]] - distribution theory underlying Bayes
- [[nlp-text-processing]] - Naive Bayes for text classification
- [[hypothesis-testing]] - Bayesian alternative to frequentist testing
- [[math-probability-statistics]] - formal probability foundations

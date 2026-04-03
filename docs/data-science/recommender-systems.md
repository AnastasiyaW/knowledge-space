---
title: Recommender Systems
category: techniques
tags: [data-science, ml, recommendations, collaborative-filtering, ranking]
---

# Recommender Systems

Predict user preferences and rank items. From simple collaborative filtering to deep learning approaches. Evaluated differently from standard classification/regression.

## Approaches

### Collaborative Filtering
Based on user behavior patterns. "Users who liked X also liked Y."

**User-based**: find similar users, recommend what they liked.
**Item-based**: find similar items to what user already liked.

**Matrix Factorization**: decompose user-item interaction matrix into latent factors.
```
R ~ U * V^T
R: user-item matrix (sparse)
U: user latent factors (n_users x k)
V: item latent factors (n_items x k)
```

### Content-Based
Recommend items similar to what user previously engaged with, based on item features (genre, description, tags).

### Hybrid
Combine collaborative and content-based. Most production systems use hybrid approaches.

## Evaluation

### Offline Metrics

| Metric | Description |
|--------|-------------|
| precision@k | Fraction of relevant items in top-k recommendations |
| recall@k | Fraction of all relevant items found in top-k |
| mAP@k | Mean average precision across users |
| nDCG@k | Position-weighted relevance |
| Hit Rate | Fraction of users who got at least one relevant recommendation |

**nDCG formula:**
DCG@k = sum_i (2^relevance_i - 1) / log2(i + 1)
nDCG = DCG / ideal_DCG

### Online Metrics (A/B Test)
- CTR (click-through rate)
- Session length
- Items consumed
- Retention (returned next day?)
- Revenue per user

### Evaluation Pipeline
1. **Offline**: train/test split, compute ranking metrics
2. **A/B test**: deploy to user subset, measure business metrics
3. **Analysis**: check group split validity, compute hitrate

**Gotcha**: recommendation logs and click logs are in separate tables. Joining requires time-proximity matching (clicks within ~1 hour, matching user_id and item_id).

## Cold Start Problem

- **New user**: no interaction history. Use: popular items, demographic-based, content-based
- **New item**: no user interactions. Use: content features, metadata similarity

## Implicit vs Explicit Feedback

- **Explicit**: ratings, likes (rare, biased toward strong opinions)
- **Implicit**: clicks, views, purchases, time spent (abundant, noisy)

Most real systems use implicit feedback. Interpret "no interaction" carefully - it's not necessarily negative.

## Gotchas
- Offline metrics don't always correlate with online business metrics - always A/B test
- Popularity bias: easy to recommend popular items, hard to surface long-tail
- Filter bubbles: recommendations become increasingly narrow without diversity injection
- Evaluation with implicit feedback is tricky - missing data != negative preference

## See Also
- [[model-evaluation]] - general metrics framework
- [[unsupervised-learning]] - matrix factorization, SVD
- [[hypothesis-testing]] - A/B testing recommendations
- [[math-linear-algebra]] - SVD for matrix factorization

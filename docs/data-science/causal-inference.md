---
title: Causal Inference
category: techniques
tags: [data-science, statistics, causality, quasi-experiments, observational]
---

# Causal Inference

Determining cause-and-effect from data. Correlation does not imply causation - but with the right methods, we can get closer to causal claims even without randomized experiments.

## Methods Hierarchy (by strength)

1. **Randomized A/B tests** - gold standard
2. **Quasi-experiments** - natural group assignment
3. **Counterfactual analysis** - no control group

## DAGs (Directed Acyclic Graphs)

Visualize causal relationships. Identify confounders, mediators, and colliders.

- **Confounder**: affects both treatment and outcome (must control for it)
- **Mediator**: on the causal path between treatment and outcome
- **Collider**: caused by both treatment and outcome (don't control for it)

Example: School GPA -> University admission, but motivation, income, school quality all interconnect.

## Difference-in-Differences (DiD)

Compare treatment and control groups before and after intervention.

**Effect = (treatment_after - treatment_before) - (control_after - control_before)**

**Requires**: parallel trends assumption - groups would have followed the same trend without intervention.

## Propensity Score Matching (PSM)

When groups aren't randomly assigned:
1. Estimate probability of receiving treatment for each unit (propensity score)
2. Match treatment units to control units with similar propensity scores
3. Compare outcomes between matched pairs

**Validation**: check covariate distributions become similar after matching.

## Synthetic Control

When can't split users at all:
1. Deploy feature in treatment region
2. Build model predicting treatment region metric using control regions
3. Compare actual vs predicted baseline
4. Difference = estimated effect

**Limitation**: needs control regions, fragile to extraordinary events.

## Instrumental Variables (IV)

When treatment assignment is confounded:
- Find a variable (instrument) that affects treatment but not outcome directly
- Use instrument to isolate causal variation in treatment
- Classic example: distance to college as instrument for education's effect on earnings

## Regression Discontinuity (RDD)

When treatment is assigned by a threshold (test score, age, income level):
- Compare units just above and just below the threshold
- They are effectively randomly assigned near the cutoff
- Estimate treatment effect at the discontinuity

## Gotchas
- **Omitted variable bias**: missing confounders invalidate causal claims
- DiD parallel trends assumption is untestable (can only check pre-period)
- PSM only controls for observed confounders - hidden confounders remain
- Synthetic control is fragile with few control units
- Don't confuse prediction models with causal models - a feature can predict well without being causal
- "Natural experiments" are only as good as the argument for exogeneity

## See Also
- [[hypothesis-testing]] - A/B testing as randomized experiment
- [[descriptive-statistics]] - understanding data before causal analysis
- [[bi-dashboards]] - presenting causal analysis results

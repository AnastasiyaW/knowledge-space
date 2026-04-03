---
title: Product Analytics Fundamentals
category: concepts
tags: [bi-analytics, product-analytics, metrics, analyst-role]
---

# Product Analytics Fundamentals

Product analytics is the discipline of measuring and understanding user behavior within a product to drive business decisions. It combines analytical thinking with data measurement - knowing SQL or Tableau is necessary but insufficient; the core skill is understanding what to measure and why.

## Key Facts

- Product analytics answers: what problem are we solving, who is the audience, how are we solving it, what do we want to achieve, and how do we make money
- A product analyst defines key metrics, collects data, analyzes it, runs experiments (A/B tests), and implements findings
- The analyst's five-step cycle: Define metrics -> Collect data -> Analyze -> Experiment -> Implement
- Analytics should be involved from early design stages, not bolted on after launch
- Recommendations must be grounded in numbers, not emotions
- "Active user" definition varies by product and must be explicitly defined for each context

## Patterns

### Metrics Pyramid

A tool for visualizing processes and finding KPIs. Structure: Business GOAL at top, primary metrics at Level 1, decomposition/secondary metrics at Level 2.

Common errors when selecting KPIs:
- Choosing a single indicator (creates blind spots)
- Choosing too many indicators (analysis paralysis)

Task formulation must be specific: not "Analyze site traffic" but "Research the impact of monitor resolution on conversion rate and give recommendations."

### Vanity vs Actionable Metrics

**Vanity metrics** look good but don't guide decisions:
- Total registered users (includes inactive)
- Pageviews (without context)
- Downloads (no indication of engagement)

**Actionable metrics** are directly tied to business decisions:
- DAU/MAU with precise "active" definition
- Funnel conversion rates (step-by-step)
- Retention curves (D1/D7/D30)
- Feature adoption rate
- Revenue per cohort

### North Star Metric

A single metric that best captures delivered value. Everything measured against impact on this metric. Example: Spotify = "time spent listening per user."

**Input metrics** (things teams control) drive **Output metrics** (business outcomes):
- Input: feature adoption rate -> Output: retention
- Input: onboarding completion rate -> Output: D7 retention
- Input: search success rate -> Output: conversion to purchase

## Gotchas

- Product company variables that affect analytics setup: company size/stage, B2B vs B2C, team structure, methodology (Scrum/Agile), tooling, and analytical culture maturity
- Marketing analytics and product analytics answer different questions - marketing focuses on channel effectiveness and budget allocation, product focuses on user behavior and feature performance
- The metrics pyramid should be reassessed as the product evolves - metrics appropriate for a startup differ from those for a mature product

## See Also

- [[product-metrics-framework]] - DAU/MAU, stickiness, retention definitions
- [[funnel-analysis]] - conversion funnel concepts and optimization
- [[unit-economics]] - profitability per user calculations
- [[bi-development-process]] - requirements gathering and dashboard workflow

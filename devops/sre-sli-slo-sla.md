---
title: SRE - SLI, SLO, SLA & Error Budgets
category: operations
tags: [sre, sli, slo, sla, error-budget, reliability, toil, dora-metrics]
---
# SRE - SLI, SLO, SLA & Error Budgets

Site Reliability Engineering principles: measuring reliability, managing risk, and reducing toil.

## Key Facts

- **SRE** (Site Reliability Engineering) = applying software engineering to operations problems
- **SLI** (Service Level Indicator) = measurable metric of service behavior (latency, error rate, throughput)
- **SLO** (Service Level Objective) = target value for an SLI (e.g., "99.9% of requests < 200ms")
- **SLA** (Service Level Agreement) = contract with consequences; SLO + penalty for violation
- **Error budget** = 100% - SLO; amount of unreliability permitted (e.g., 99.9% SLO = 0.1% error budget = 43min/month)
- Error budget spent = slow down releases, invest in reliability; error budget remaining = ship faster
- **Toil** = repetitive, automatable work that scales linearly with service size; SRE goal: eliminate toil
- **DORA metrics** (DevOps Research and Assessment): deployment frequency, lead time, change failure rate, MTTR
- 100% availability is wrong target - costs exponentially more, prevents velocity
- SRE is NOT just "ops with a new name" - it requires engineering capacity (coding, automation)
- [[monitoring-observability]] provides the data for SLI measurement
- [[incident-management]] kicks in when error budget is burning too fast
- Google SRE: "SRE is what happens when you ask a software engineer to design an operations team"

## Patterns

```
# Availability table (monthly)
SLO      | Allowed downtime/month | Error budget
---------|------------------------|-------------
99%      | 7h 18m                 | 1%
99.9%    | 43m 50s                | 0.1%
99.95%   | 21m 55s                | 0.05%
99.99%   | 4m 23s                 | 0.01%
99.999%  | 26s                    | 0.001%

# Common SLI types
- Availability:  successful_requests / total_requests
- Latency:       requests_below_threshold / total_requests
- Throughput:    requests_per_second
- Correctness:   correct_responses / total_responses
- Freshness:     data_updated_within_threshold / total_data_points
```

```yaml
# SLO definition example (structured)
service: payment-api
slos:
  - name: availability
    sli: "ratio of HTTP 2xx+3xx responses to all responses"
    target: 99.95%
    window: 30 days (rolling)
    measurement: |
      sum(rate(http_requests_total{status!~"5.."}[30d])) /
      sum(rate(http_requests_total[30d]))

  - name: latency
    sli: "ratio of requests completed under 300ms"
    target: 99%
    window: 30 days (rolling)
    measurement: |
      histogram_quantile(0.99,
        rate(http_request_duration_seconds_bucket[30d])) < 0.3
```

```
# Error Budget Policy (decision framework)
Budget status     | Action
------------------|----------------------------------
> 50% remaining   | Ship features freely
25-50% remaining  | Normal pace, monitor closely
10-25% remaining  | Slow releases, prioritize reliability
< 10% remaining   | Feature freeze, all hands on reliability
Exhausted         | Stop all changes until budget recovers

# DORA Metrics targets (Elite performers)
Metric                  | Elite           | High
------------------------|-----------------|------------------
Deployment frequency    | On demand       | Weekly-monthly
Lead time for changes   | < 1 hour        | 1 day - 1 week
Change failure rate     | 0-15%           | 16-30%
MTTR                    | < 1 hour        | < 1 day
```

## Gotchas

- SLOs are for USERS, not internal metrics; measure what users experience, not server CPU
- Setting SLO too high (99.99%) when you're at 99.5% is counterproductive - set achievable targets first
- Error budget is not "free downtime" - it's a risk management tool for balancing velocity and reliability
- SLI must be measurable AND actionable; "the system feels slow" is not an SLI
- External SLAs should be LESS strict than internal SLOs (buffer zone)
- Toil measurement: if >50% of SRE time is toil, the team cannot improve - invest in automation
- Averaging hides problems: p50 = 100ms, p99 = 5s means 1% of users wait 50x longer; track percentiles
- SRE is not just Google's model - adapt principles to your organization's maturity level

## See Also

- [[monitoring-observability]] - implementing SLI measurement
- [[incident-management]] - responding to SLO breaches
- [[deployment-strategies]] - managing change failure rate
- [[ci-cd-pipelines]] - deployment frequency and lead time
- Google SRE Book: https://sre.google/sre-book/table-of-contents/
- DORA metrics: https://dora.dev/

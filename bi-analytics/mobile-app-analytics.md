---
title: Mobile App Analytics
category: Product Analytics
tags: [mobile, app-analytics, marketing-analytics, ASO, UX-analytics, store-analytics, attribution, CPI]
---

# Mobile App Analytics

Process of analyzing user interaction effectiveness with a mobile app as a product. Covers five analytics directions specific to mobile.

## Key Facts

- Mobile analytics (MA) provides: product assessment, growth zone identification, growth point detection, revenue decline root cause analysis
- Five main directions: marketing analytics, product analytics, store/market analytics, ASO analytics, UX analytics
- Marketing analytics answers: which channels bring users, how effectively are budgets distributed, which campaigns perform best
- Product analytics: user behavior analysis during interaction with the app - applies all [[funnel-analysis]], [[cohort-analysis]], [[retention-ltv-roi]] techniques
- Store analytics: iOS App Store, Google Play, Huawei AppGallery market analysis
- ASO (App Store Optimization): keyword and listing optimization for organic discovery
- Connected to [[unit-economics]] via CPI (Cost Per Install) as the primary acquisition metric

## Analytics Directions

| Direction | Focus | Key Questions |
|-----------|-------|---------------|
| **Marketing** | Channel effectiveness | Where do users come from? ROI per channel? Budget optimization? |
| **Product** | In-app behavior | How do users engage? Where do they drop off? What drives retention? |
| **Store/Market** | Market positioning | How do competitors perform? Market trends? Category rankings? |
| **ASO** | Organic discovery | Which keywords rank? How to improve listing? Screenshot/icon testing? |
| **UX** | Interface usability | Where do users struggle? Tap heatmaps? Session recordings? |

## Patterns

**Mobile-specific metric stack:**

```
Acquisition:
  - CPI (Cost Per Install)
  - Install rate (impressions -> installs)
  - Attribution by channel/campaign

Activation:
  - First session completion rate
  - Onboarding funnel completion
  - Time to first key action

Engagement:
  - DAU / MAU ratio (stickiness)
  - Session frequency
  - Session duration
  - Feature adoption rates

Retention:
  - Day 1 / Day 7 / Day 30 retention
  - Cohort retention curves
  - Churn rate by segment

Revenue:
  - ARPU / ARPPU
  - LTV by acquisition channel
  - In-app purchase conversion
  - Subscription renewal rate
```

**Key analytics tools:**

```
Attribution & Marketing:
  - AppsFlyer, Adjust, Branch, Singular

Product Analytics:
  - Amplitude, Mixpanel, Firebase Analytics, AppMetrica

Store Analytics:
  - App Annie / data.ai, Sensor Tower, AppFollow

UX Analytics:
  - UXCam, Smartlook, FullStory
```

## Gotchas

- **Symptom**: Install count is high but DAU is flat -> **Cause**: Poor activation / onboarding, users install and never return -> **Fix**: Analyze Day 1 retention, optimize onboarding funnel, check push notification permissions
- **Symptom**: Attribution data doesn't match store data -> **Cause**: Different attribution windows, SKAdNetwork limitations on iOS -> **Fix**: Accept gap, use probabilistic modeling, compare trends not absolutes
- **Symptom**: A/B test on mobile shows no difference -> **Cause**: Test running on cached old version; users haven't updated -> **Fix**: Force-update or filter analysis to users on new version only, account for update adoption curve

## See Also

- [[funnel-analysis]] - mobile onboarding and purchase funnels
- [[retention-ltv-roi]] - retention curves specific to mobile
- [[cohort-analysis]] - install-date cohorts for mobile
- [[unit-economics]] - CPI-based unit economics
- Firebase Analytics: https://firebase.google.com/docs/analytics

---
title: Mobile Analytics Platforms
category: tools
tags: [bi-analytics, mobile-analytics, firebase, appmetrica, amplitude, sdk, product-analytics]
---

# Mobile Analytics Platforms

Mobile analytics platforms collect user behavioral data from mobile apps via SDK integration. This entry covers the major platforms (Firebase, AppMetrica, Amplitude, Mixpanel), their SDK integration patterns, and key reporting capabilities.

## Key Facts

- Analytics SDKs must be planned during app design, not bolted on after launch
- Event map (specification of all trackable actions) should be defined before development sprint
- Retro-fitting analytics is expensive - define events early
- All platforms share core concepts: events, user properties, event properties, sessions
- Free platforms: Firebase Analytics, AppMetrica (Yandex), MyTracker (VK)
- Paid/freemium: Amplitude, Mixpanel, AppsFlyer, Adjust

## Patterns

### Platform Comparison

| Tool | Type | Cost | Strengths |
|------|------|------|-----------|
| **Firebase** | Product + Marketing | Free | Native Android/iOS, BigQuery export, A/B testing |
| **AppMetrica** | Product + Marketing | Free | CIS market strength, Yandex integration |
| **MyTracker** | Product + Marketing | Free | VK ecosystem, Russian market |
| **Amplitude** | Product analytics | Freemium | Best funnel/retention UI |
| **Mixpanel** | Product analytics | Freemium | Event-centric, flexible segmentation |
| **AppsFlyer** | Attribution | Paid | Best attribution, 6000+ integrations |
| **Adjust** | Attribution | Paid | Attribution, deep links, fraud prevention |

### Amplitude Key Charts

**Event Segmentation**: track event volume over time with breakdown by properties.

**Funnel Analysis**: visualize conversion through multi-step flow with segmentation and time windows.

**Retention Analysis**: N-day, bracket, and return-on retention curves by cohort.

**Pathfinder**: shows actual user navigation paths - what users do after event X or before drop-off Y.

**Personas / Behavioral Clustering**: group users by usage pattern similarity without predefined criteria.

**A/B Testing (Amplitude Experiment)**: sequential testing methodology to allow early peeking without inflating false positive rate.

### AppMetrica SDK Integration (Android)

```java
// build.gradle
dependencies {
    implementation 'com.yandex.android:mobmetricalib:3.18.0'
}

// Application.onCreate()
YandexMetricaConfig config = YandexMetricaConfig
    .newConfigBuilder(API_key).build();
YandexMetrica.activate(getApplicationContext(), config);
YandexMetrica.enableActivityAutoTracking(this);

// Send events
YandexMetrica.reportEvent("purchase_complete");
YandexMetrica.reportEvent("add_to_cart",
    "{\"item_id\": \"SKU123\", \"price\": 299}");
```

### AppMetrica SDK Integration (iOS)

```swift
// CocoaPods: pod 'YandexMobileMetrica', '3.15.0'
// SPM: https://github.com/yandexmobile/metrica-sdk-ios (3.14.0+)

let config = YMMYandexMetricaConfiguration.init(apiKey: "API_key")
YMMYandexMetrica.activate(with: config!)

// Send events
YMMYandexMetrica.reportEvent("purchase_complete", onFailure: nil)
YMMYandexMetrica.reportEvent("add_to_cart",
    parameters: ["item_id": "SKU123", "price": 299],
    onFailure: nil)
```

### Amplitude SDK Integration (Android)

```java
Amplitude.getInstance().initialize(context, "YOUR_API_KEY")
    .enableForegroundTracking(getApplication());

// Track events
Amplitude.getInstance().logEvent("purchase_complete");

JSONObject props = new JSONObject();
props.put("item_id", "SKU123");
props.put("price", 299);
Amplitude.getInstance().logEvent("add_to_cart", props);

// User properties
Identify identify = new Identify().set("plan", "premium");
Amplitude.getInstance().identify(identify);
```

### AppMetrica Reports

- **Audience**: new/returning users, demographics, device info
- **Engagement**: sessions count, duration distribution, time between sessions
- **Retention**: by date interval with grouping and breakdown
- **Profiles**: user distribution by custom attributes with sparklines
- **Profile Card**: individual user view with event history
- **Logs API**: raw data export for DWH/BigQuery/ClickHouse

### Amplitude Data Export

- **Amplitude Data** (Snowflake): raw events streaming to data warehouse
- **Export API**: download raw event data as CSV/JSON
- **Amplitude -> Segment -> Anywhere**: bidirectional CDP integration

## Gotchas

- AppMetrica has NO native anti-fraud - requires FraudScore third-party integration
- AppMetrica retention calculation excludes current incomplete month - verify your date range includes only completed months
- Amplitude sequential testing allows peeking but don't stop tests early based on p-value alone without sequential methodology
- SDKs for multiple platforms (Windows, Unity, Xamarin, React Native) exist but may have different feature sets
- Always verify SDK integration: launch app, use it, check that new user and events appear in dashboard

## See Also

- [[mobile-attribution-fraud]] - AppsFlyer, attribution models, fraud detection
- [[product-metrics-framework]] - DAU/MAU, stickiness measured by these platforms
- [[funnel-analysis]] - funnel analysis in Amplitude
- [[cohort-retention-analysis]] - retention analysis patterns
- [[app-store-optimization]] - pre-install analytics

---
title: Mobile Attribution & Fraud Detection
category: concepts
tags: [bi-analytics, mobile-analytics, attribution, appsflyer, fraud, protect360, mmp]
---

# Mobile Attribution & Fraud Detection

Mobile attribution determines which ad source (campaign, network, creative) caused each app install and subsequent in-app action. Fraud detection identifies fake clicks, installs, and events that inflate attribution numbers. AppsFlyer is the leading platform, with Adjust and MyTracker as alternatives.

## Key Facts

- MMP (Mobile Measurement Partner) = attribution platform integrating with ad networks
- AppsFlyer supports 6000+ ad network integrations with real-time attribution
- Attribution window default: 7 days click-through, 24 hours view-through (customizable)
- CTIT (Click-To-Install Time): normal = minutes to hours; <10 sec = click injection fraud; >24h = suspicious
- Standard event names (AFInAppEventType) enable automatic ad network optimization
- Postback URLs notify ad networks about attributed events

## Patterns

### How Attribution Works

1. User sees ad -> ad platform records impression
2. User clicks ad -> AppsFlyer records click with timestamp and fingerprint
3. User installs app -> SDK sends install signal
4. AppsFlyer matches install to click (deterministic via GAID/IDFA, or probabilistic via fingerprint)
5. Postback sent to ad network confirming attributed install
6. Report shows which campaign/source drove install

### Attribution Models

| Model | Description | Use Case |
|-------|-------------|----------|
| **Last click** | 100% credit to last click before install | Default, most common |
| **Last touch** | 100% credit to last interaction (view or click) | View-through attribution |
| **Multi-touch** | Distribute credit across all touchpoints | Full funnel analysis |

### AppsFlyer SDK Integration

**Android:**
```groovy
dependencies {
    implementation "com.appsflyer:af-android-sdk:6.+"
    implementation 'com.android.installreferrer:installreferrer:2.2'
}
```

```java
AppsFlyerLib.getInstance().init("YOUR_DEV_KEY",
    conversionDataListener, context);
AppsFlyerLib.getInstance().start(this);
```

**iOS:**
```swift
AppsFlyerLib.shared().appsFlyerDevKey = "YOUR_DEV_KEY"
AppsFlyerLib.shared().appleAppID = "YOUR_APP_ID"
AppsFlyerLib.shared().start()
```

### In-App Event Tracking

```java
Map<String, Object> eventValues = new HashMap<>();
eventValues.put(AFInAppEventParameterName.PRICE, 200);
eventValues.put(AFInAppEventParameterName.CURRENCY, "USD");
eventValues.put(AFInAppEventParameterName.CONTENT_ID, "item_123");
AppsFlyerLib.getInstance().logEvent(context,
    AFInAppEventType.PURCHASE, eventValues);
```

Standard events: `PURCHASE`, `ADD_TO_CART`, `TUTORIAL_COMPLETION`, `LEVEL_ACHIEVED`, `SUBSCRIBE`, `LOGIN`, `SEARCH`.

### Deep Links

- **URI Scheme**: `myapp://product/123` (doesn't work if app not installed)
- **Universal Links** (iOS) / **App Links** (Android): HTTPS links, app if installed or web if not
- **OneLink** (AppsFlyer): single link for all platforms + attribution

### Fraud Detection Metrics

**Pre-install (click metrics):**
- Short clicks (CTIT < 10 sec) - bot-generated
- Short installs - install too fast after click
- Matching clicks - same device from multiple sources
- Matching installs - same device attributed multiple times

**Post-install (behavioral):**
- Anomalous session durations
- Suspicious session frequency
- Hyperactive installs (too many per device/IP)
- Installs without launches

**Hardware:**
- Frequent country/region changes - device spoofing
- Incorrect device identifiers - fake devices

### Anti-Fraud Solutions

**AppsFlyer Protect360** (multi-layer):
- SDK-level identification (post-compilation hashing blocks fraudulent events)
- Cluster-based anomaly detection (bot behavior patterns in real-time)
- Validation rules (custom CTIT thresholds per campaign/network)
- Attribution calibrator (removes fraud, re-attributes to correct channel)
- Post-attribution analysis (continuous monitoring after attribution)
- Access: requires request (not available on all plans)

**MyTracker Fraud Scanner:**
- Group 1 (Strict): short installs, matching clicks, suspicious devices - near-certain fraud
- Group 2 (Confident): abnormally short sessions, installs without launches - requires context
- Group 3 (Soft): long installs, very low CVR - suspicious but may be legitimate

**AppMetrica**: no native anti-fraud. Third-party FraudScore integration available.

### Ad Market Ecosystem

- **Advertiser** - the app publisher
- **Publisher/Affiliate** - site/app displaying ads
- **Ad Network** - connects advertisers and publishers (Google Ads, Facebook, Unity Ads)
- **DSP** (Demand-Side Platform) - programmatic buying for advertisers
- **SSP** (Supply-Side Platform) - programmatic selling for publishers
- **DMP** (Data Management Platform) - audience data platform

### Postback URLs

```text
https://ad-network.com/postback?
    idfa={idfa}&
    event={event_name}&
    value={revenue}&
    currency={currency}&
    campaign={campaign_id}
```

Ad networks use postbacks to confirm installs, optimize bidding, and prevent paying for fraud.

## Gotchas

- Protect360 is not available by default on all AppsFlyer plans - must request access
- Other providers classify fraudulent installs as organic; AppsFlyer's calibrator re-attributes them correctly
- Cheap install volume often correlates with low LTV - always analyze cohort behavior by acquisition source
- CTIT thresholds should be customized per app, region, partner, and campaign - one-size-fits-all doesn't work
- View-through attribution is inherently noisier than click-through - shorter windows reduce false attribution

## See Also

- [[unit-economics]] - ROAS and CPA calculations
- [[mobile-analytics-platforms]] - product analytics after attribution
- [[cohort-retention-analysis]] - cohort quality by acquisition source
- [[web-marketing-analytics]] - web attribution models

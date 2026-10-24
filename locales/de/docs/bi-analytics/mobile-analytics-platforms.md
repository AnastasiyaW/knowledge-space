---
title: "Plattformen für mobile Analytics"
category: tools
tags: [bi-analytics, mobile-analytics, firebase, appmetrica, amplitude, sdk, product-analytics]
level: 3
source_sha256: 50e7523eb1e092c4781329a3cfb910d339c93f814c5c01f987d3e2cc10cd1a60
translation: machine
translated_at: '2026-10-24'
---
# Plattformen für mobile Analytics {#mobile-analytics-platforms}

Plattformen für mobile Analytics erfassen über SDK-Integration das Nutzerverhalten in mobilen Apps. Dieser Eintrag behandelt die wichtigsten Plattformen (Firebase, AppMetrica, Amplitude, Mixpanel), deren SDK-Integrationsmuster und zentrale Reporting-Funktionen.

## Wichtige Fakten {#key-facts}

- Analytics-SDKs müssen bereits beim App-Design eingeplant werden, nicht erst nach dem Launch ergänzt werden
- Die Event Map (Spezifikation aller erfassbaren Aktionen) sollte vor dem Entwicklungs-Sprint definiert werden
- Nachträgliches Einbauen von Analytics ist aufwendig – Events frühzeitig definieren
- Alle Plattformen teilen dieselben Grundkonzepte: Events, User Properties, Event Properties, Sessions
- Kostenlose Plattformen: Firebase Analytics, AppMetrica (Yandex), MyTracker (VK)
- Bezahlt/Freemium: Amplitude, Mixpanel, AppsFlyer, Adjust

## Muster {#patterns}

### Plattformvergleich {#platform-comparison}

| Tool | Typ | Kosten | Stärken |
|------|-----|--------|---------|
| **Firebase** | Product + Marketing | Kostenlos | Native Android/iOS, BigQuery-Export, A/B-Tests |
| **AppMetrica** | Product + Marketing | Kostenlos | Stärke im GUS-Markt, Yandex-Integration |
| **MyTracker** | Product + Marketing | Kostenlos | VK-Ökosystem, russischer Markt |
| **Amplitude** | Product Analytics | Freemium | Beste UI für Funnels/Retention |
| **Mixpanel** | Product Analytics | Freemium | Event-zentriert, flexible Segmentierung |
| **AppsFlyer** | Attribution | Bezahlt | Beste Attribution, über 6000 Integrationen |
| **Adjust** | Attribution | Bezahlt | Attribution, Deep Links, Betrugsprävention |

### Wichtige Amplitude-Charts {#amplitude-key-charts}

**Event Segmentation**: Entwicklung des Event-Volumens über die Zeit mit Aufschlüsselung nach Properties.

**Funnel Analysis**: Visualisiert die Konversion über einen mehrstufigen Ablauf mit Segmentierung und Zeitfenstern.

**Retention Analysis**: N-Tage-, Bracket- und Return-on-Retention-Kurven nach Kohorte.

**Pathfinder**: Zeigt die tatsächlichen Navigationspfade der Nutzer – was Nutzer nach Event X oder vor dem Absprung bei Y tun.

**Personas / Behavioral Clustering**: Gruppiert Nutzer nach Ähnlichkeit im Nutzungsverhalten, ohne vordefinierte Kriterien.

**A/B Testing (Amplitude Experiment)**: Sequenzielle Testmethodik, die frühes Hineinschauen erlaubt, ohne die Rate falsch-positiver Ergebnisse zu erhöhen.

### AppMetrica SDK-Integration (Android) {#appmetrica-sdk-integration-android}

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

### AppMetrica SDK-Integration (iOS) {#appmetrica-sdk-integration-ios}

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

### Amplitude SDK-Integration (Android) {#amplitude-sdk-integration-android}

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

### AppMetrica-Reports {#appmetrica-reports}

- **Audience**: Neue/wiederkehrende Nutzer, Demografie, Geräteinformationen
- **Engagement**: Anzahl Sessions, Verteilung der Sitzungsdauer, Zeit zwischen Sessions
- **Retention**: Nach Datumsintervall mit Gruppierung und Aufschlüsselung
- **Profiles**: Verteilung der Nutzer nach benutzerdefinierten Attributen mit Sparklines
- **Profile Card**: Einzelansicht eines Nutzers mit Event-Historie
- **Logs API**: Export der Rohdaten für DWH/BigQuery/ClickHouse

### Amplitude-Datenexport {#amplitude-data-export}

- **Amplitude Data** (Snowflake): Streaming der Roh-Events in ein Data Warehouse
- **Export API**: Download der Roh-Eventdaten als CSV/JSON
- **Amplitude -> Segment -> Anywhere**: Bidirektionale CDP-Integration

## Stolperfallen {#gotchas}

- AppMetrica hat KEINEN nativen Betrugsschutz – erfordert die Integration eines Drittanbieters für FraudScore
- Die Retention-Berechnung in AppMetrica schließt den aktuellen, unvollständigen Monat aus – prüfen, ob der Datumsbereich nur abgeschlossene Monate umfasst
- Sequenzielle Tests in Amplitude erlauben frühes Hineinschauen, aber Tests nicht allein auf Basis des p-Werts vorzeitig beenden, ohne sequenzielle Methodik
- SDKs für mehrere Plattformen (Windows, Unity, Xamarin, React Native) existieren, können aber unterschiedliche Funktionsumfänge haben
- SDK-Integration immer prüfen: App starten, benutzen und kontrollieren, ob neue Nutzer und Events im Dashboard erscheinen

## Siehe auch {#see-also}

- [[mobile-attribution-fraud]] - AppsFlyer, Attributionsmodelle, Betrugserkennung
- [[product-metrics-framework]] - DAU/MAU, Stickiness, gemessen von diesen Plattformen
- [[funnel-analysis]] - Funnel-Analyse in Amplitude
- [[cohort-retention-analysis]] - Retention-Analyse-Muster
- [[app-store-optimization]] - Analytics vor der Installation

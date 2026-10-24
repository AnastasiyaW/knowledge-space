---
title: "Mobile-Attribution & Betrugserkennung"
category: concepts
tags: [bi-analytics, mobile-analytics, attribution, appsflyer, fraud, protect360, mmp]
level: 3
source_sha256: 8f0e306b1e52824beff07ff0852e7c9190d68cf7b19b84e2a5f4d65c4832f84f
translation: machine
translated_at: '2026-10-24'
---
# Mobile-Attribution & Betrugserkennung {#mobile-attribution-fraud-detection}

Mobile-Attribution bestimmt, welche Werbequelle (Kampagne, Netzwerk, Creative) jede App-Installation und die anschließende In-App-Aktion ausgelöst hat. Betrugserkennung identifiziert gefälschte Klicks, Installationen und Events, die die Attributionszahlen aufblähen. AppsFlyer ist die führende Plattform, Adjust und MyTracker sind Alternativen.

## Kernfakten {#key-facts}

- MMP (Mobile Measurement Partner) = Attributionsplattform, die mit Werbenetzwerken integriert ist
- AppsFlyer unterstützt über 6000 Werbenetzwerk-Integrationen mit Echtzeit-Attribution
- Standard-Attributionsfenster: 7 Tage für Klick-Attribution, 24 Stunden für View-Through-Attribution (anpassbar)
- CTIT (Click-To-Install Time): normal = Minuten bis Stunden; <10 Sek. = Click-Injection-Betrug; >24 h = verdächtig
- Standard-Eventnamen (AFInAppEventType) ermöglichen automatische Optimierung durch Werbenetzwerke
- Postback-URLs informieren Werbenetzwerke über zugeordnete Events

## Muster {#patterns}

### So funktioniert Attribution {#how-attribution-works}

1. Nutzer sieht Anzeige -> Werbeplattform erfasst Impression
2. Nutzer klickt auf Anzeige -> AppsFlyer erfasst Klick mit Zeitstempel und Fingerprint
3. Nutzer installiert App -> SDK sendet Install-Signal
4. AppsFlyer ordnet Installation dem Klick zu (deterministisch über GAID/IDFA oder probabilistisch über Fingerprint)
5. Postback wird an Werbenetzwerk gesendet, das die zugeordnete Installation bestätigt
6. Report zeigt, welche Kampagne/Quelle die Installation ausgelöst hat

### Attributionsmodelle {#attribution-models}

| Modell | Beschreibung | Anwendungsfall |
|-------|-------------|----------|
| **Last Click** | 100 % des Verdienstes an den letzten Klick vor der Installation | Standard, am häufigsten |
| **Last Touch** | 100 % des Verdienstes an die letzte Interaktion (View oder Klick) | View-Through-Attribution |
| **Multi-Touch** | Verdienst auf alle Touchpoints verteilen | Vollständige Funnel-Analyse |

### AppsFlyer-SDK-Integration {#appsflyer-sdk-integration}

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

### In-App-Event-Tracking {#in-app-event-tracking}

```java
Map<String, Object> eventValues = new HashMap<>();
eventValues.put(AFInAppEventParameterName.PRICE, 200);
eventValues.put(AFInAppEventParameterName.CURRENCY, "USD");
eventValues.put(AFInAppEventParameterName.CONTENT_ID, "item_123");
AppsFlyerLib.getInstance().logEvent(context,
    AFInAppEventType.PURCHASE, eventValues);
```

Standard-Events: `PURCHASE`, `ADD_TO_CART`, `TUTORIAL_COMPLETION`, `LEVEL_ACHIEVED`, `SUBSCRIBE`, `LOGIN`, `SEARCH`.

### Deep Links {#deep-links}

- **URI-Schema**: `myapp://product/123` (funktioniert nicht, wenn die App nicht installiert ist)
- **Universal Links** (iOS) / **App Links** (Android): HTTPS-Links, öffnen die App, falls installiert, oder die Website, falls nicht
- **OneLink** (AppsFlyer): ein einziger Link für alle Plattformen + Attribution

### Metriken zur Betrugserkennung {#fraud-detection-metrics}

**Vor der Installation (Klick-Metriken):**
- Kurze Klicks (CTIT < 10 Sek.) - von Bots erzeugt
- Kurze Installationen - Installation zu schnell nach dem Klick
- Übereinstimmende Klicks - dasselbe Gerät aus mehreren Quellen
- Übereinstimmende Installationen - dasselbe Gerät mehrfach zugeordnet

**Nach der Installation (Verhalten):**
- Auffällige Session-Dauern
- Verdächtige Session-Häufigkeit
- Hyperaktive Installationen (zu viele pro Gerät/IP)
- Installationen ohne App-Start

**Hardware:**
- Häufige Wechsel von Land/Region - Geräte-Spoofing
- Inkorrekte Geräte-Identifier - gefälschte Geräte

### Anti-Betrugs-Lösungen {#anti-fraud-solutions}

**AppsFlyer Protect360** (mehrschichtig):
- Identifikation auf SDK-Ebene (Hashing nach der Kompilierung blockiert betrügerische Events)
- Clusterbasierte Anomalieerkennung (Bot-Verhaltensmuster in Echtzeit)
- Validierungsregeln (individuelle CTIT-Schwellenwerte pro Kampagne/Netzwerk)
- Attribution Calibrator (entfernt Betrug und ordnet neu dem korrekten Kanal zu)
- Post-Attribution-Analyse (kontinuierliche Überwachung nach der Attribution)
- Zugang: auf Anfrage (nicht in allen Tarifen verfügbar)

**MyTracker Fraud Scanner:**
- Gruppe 1 (Strikt): kurze Installationen, übereinstimmende Klicks, verdächtige Geräte - nahezu sicherer Betrug
- Gruppe 2 (Wahrscheinlich): auffällig kurze Sessions, Installationen ohne Start - erfordert Kontext
- Gruppe 3 (Weich): lange Installationszeiten, sehr niedrige CVR - verdächtig, kann aber legitim sein

**AppMetrica**: keine native Betrugserkennung. Drittanbieter-Integration mit FraudScore verfügbar.

### Werbemarkt-Ökosystem {#ad-market-ecosystem}

- **Advertiser** - der App-Publisher
- **Publisher/Affiliate** - Website/App, die Anzeigen ausspielt
- **Werbenetzwerk (Ad Network)** - verbindet Advertiser und Publisher (Google Ads, Facebook, Unity Ads)
- **DSP** (Demand-Side Platform) - programmatischer Einkauf für Advertiser
- **SSP** (Supply-Side Platform) - programmatischer Verkauf für Publisher
- **DMP** (Data Management Platform) - Plattform für Zielgruppendaten

### Postback-URLs {#postback-urls}

```text
https://ad-network.com/postback?
    idfa={idfa}&
    event={event_name}&
    value={revenue}&
    currency={currency}&
    campaign={campaign_id}
```

Werbenetzwerke nutzen Postbacks, um Installationen zu bestätigen, Gebote zu optimieren und die Zahlung für Betrug zu vermeiden.

## Stolperfallen {#gotchas}

- Protect360 ist nicht in allen AppsFlyer-Tarifen standardmäßig enthalten - Zugang muss angefragt werden
- Andere Anbieter klassifizieren betrügerische Installationen als organisch; der Calibrator von AppsFlyer ordnet sie korrekt neu zu
- Günstiges Installationsvolumen korreliert häufig mit niedrigem LTV - Kohortenverhalten immer nach Akquisitionsquelle analysieren
- CTIT-Schwellenwerte sollten pro App, Region, Partner und Kampagne angepasst werden - Einheitslösungen funktionieren nicht
- View-Through-Attribution ist grundsätzlich fehleranfälliger als Klick-Attribution - kürzere Fenster reduzieren Fehlzuordnungen

## Siehe auch {#see-also}

- [[unit-economics]] - ROAS- und CPA-Berechnungen
- [[mobile-analytics-platforms]] - Produktanalyse nach der Attribution
- [[cohort-retention-analysis]] - Kohortenqualität nach Akquisitionsquelle
- [[web-marketing-analytics]] - Web-Attributionsmodelle

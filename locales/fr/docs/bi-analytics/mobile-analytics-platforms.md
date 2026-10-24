---
title: "Plateformes d'analytics mobile"
category: tools
tags: [bi-analytics, mobile-analytics, firebase, appmetrica, amplitude, sdk, product-analytics]
level: 3
source_sha256: 50e7523eb1e092c4781329a3cfb910d339c93f814c5c01f987d3e2cc10cd1a60
translation: machine
translated_at: '2026-10-24'
---
# Plateformes d'analytics mobile {#mobile-analytics-platforms}

Les plateformes d'analytics mobile collectent les données comportementales des utilisateurs à partir des applications mobiles via l'intégration de SDK. Cette entrée couvre les principales plateformes (Firebase, AppMetrica, Amplitude, Mixpanel), leurs modèles d'intégration de SDK et les principales capacités de reporting.

## Points clés {#key-facts}

- Les SDK d'analytics doivent être prévus dès la conception de l'application, et non ajoutés après le lancement
- La carte des événements (spécification de toutes les actions traçables) doit être définie avant le sprint de développement
- Ajouter l'analytics a posteriori est coûteux : définissez les événements au plus tôt
- Toutes les plateformes partagent les mêmes concepts de base : événements, propriétés utilisateur, propriétés d'événement, sessions
- Plateformes gratuites : Firebase Analytics, AppMetrica (Yandex), MyTracker (VK)
- Payantes/freemium : Amplitude, Mixpanel, AppsFlyer, Adjust

## Modèles {#patterns}

### Comparaison des plateformes {#platform-comparison}

| Outil | Type | Coût | Points forts |
|------|------|------|-----------|
| **Firebase** | Produit + Marketing | Gratuit | Natif Android/iOS, export BigQuery, tests A/B |
| **AppMetrica** | Produit + Marketing | Gratuit | Forte présence sur le marché de la CEI, intégration Yandex |
| **MyTracker** | Produit + Marketing | Gratuit | Écosystème VK, marché russe |
| **Amplitude** | Analytics produit | Freemium | Meilleure interface pour les entonnoirs et la rétention |
| **Mixpanel** | Analytics produit | Freemium | Centré sur les événements, segmentation flexible |
| **AppsFlyer** | Attribution | Payant | Meilleure attribution, plus de 6000 intégrations |
| **Adjust** | Attribution | Payant | Attribution, liens profonds, prévention de la fraude |

### Principaux graphiques d'Amplitude {#amplitude-key-charts}

**Segmentation d'événements** : suivi du volume d'un événement dans le temps, avec ventilation par propriétés.

**Analyse de tunnel (funnel)** : visualisation de la conversion dans un parcours en plusieurs étapes, avec segmentation et fenêtres temporelles.

**Analyse de rétention** : courbes de rétention à N jours, par tranches et de type « return-on » par cohorte.

**Pathfinder** : affiche les parcours de navigation réels des utilisateurs, c'est-à-dire ce qu'ils font après l'événement X ou avant l'abandon Y.

**Personas / regroupement comportemental** : regroupe les utilisateurs selon la similarité de leurs habitudes d'usage, sans critères prédéfinis.

**Tests A/B (Amplitude Experiment)** : méthodologie de test séquentiel permettant de consulter les résultats en cours de test sans gonfler le taux de faux positifs.

### Intégration du SDK AppMetrica (Android) {#appmetrica-sdk-integration-android}

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

### Intégration du SDK AppMetrica (iOS) {#appmetrica-sdk-integration-ios}

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

### Intégration du SDK Amplitude (Android) {#amplitude-sdk-integration-android}

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

### Rapports AppMetrica {#appmetrica-reports}

- **Audience** : nouveaux/anciens utilisateurs, données démographiques, informations sur l'appareil
- **Engagement** : nombre de sessions, distribution des durées, temps entre les sessions
- **Rétention** : par intervalle de dates, avec regroupement et ventilation
- **Profils** : répartition des utilisateurs selon des attributs personnalisés, avec sparklines
- **Fiche profil** : vue individuelle d'un utilisateur avec historique des événements
- **API Logs** : export des données brutes vers un DWH, BigQuery ou ClickHouse

### Export de données Amplitude {#amplitude-data-export}

- **Amplitude Data** (Snowflake) : diffusion en continu des événements bruts vers l'entrepôt de données
- **API d'export** : téléchargement des données d'événements brutes au format CSV/JSON
- **Amplitude -> Segment -> Anywhere** : intégration CDP bidirectionnelle

## Pièges à éviter {#gotchas}

- AppMetrica ne dispose PAS de détection de fraude native : elle nécessite l'intégration d'un service tiers FraudScore
- Le calcul de rétention d'AppMetrica exclut le mois en cours, incomplet : vérifiez que votre plage de dates ne couvre que des mois complets
- Le test séquentiel d'Amplitude permet de consulter les résultats en cours de test, mais n'arrêtez pas un test prématurément sur la seule base de la p-value sans méthodologie séquentielle
- Des SDK pour plusieurs plateformes (Windows, Unity, Xamarin, React Native) existent, mais leurs fonctionnalités peuvent différer
- Vérifiez toujours l'intégration du SDK : lancez l'application, utilisez-la, puis contrôlez que le nouvel utilisateur et les événements apparaissent dans le tableau de bord

## Voir aussi {#see-also}

- [[mobile-attribution-fraud]] - AppsFlyer, modèles d'attribution, détection de fraude
- [[product-metrics-framework]] - DAU/MAU, stickiness mesurés par ces plateformes
- [[funnel-analysis]] - analyse de tunnel dans Amplitude
- [[cohort-retention-analysis]] - modèles d'analyse de rétention
- [[app-store-optimization]] - analytics avant installation

---
title: "Attribution mobile et détection de fraude"
category: concepts
tags: [bi-analytics, mobile-analytics, attribution, appsflyer, fraud, protect360, mmp]
level: 3
source_sha256: 8f0e306b1e52824beff07ff0852e7c9190d68cf7b19b84e2a5f4d65c4832f84f
translation: machine
translated_at: '2026-10-24'
---
# Attribution mobile et détection de fraude {#mobile-attribution-fraud-detection}

L'attribution mobile détermine quelle source publicitaire (campagne, réseau, créatif) est à l'origine de chaque installation d'application et de chaque action ultérieure dans l'application. La détection de fraude identifie les faux clics, les fausses installations et les faux événements qui gonflent les chiffres d'attribution. AppsFlyer est la plateforme de référence, avec Adjust et MyTracker comme alternatives.

## Faits clés {#key-facts}

- MMP (Mobile Measurement Partner) = plateforme d'attribution intégrée aux réseaux publicitaires
- AppsFlyer prend en charge plus de 6000 intégrations de réseaux publicitaires avec attribution en temps réel
- Fenêtre d'attribution par défaut : 7 jours pour le clic, 24 heures pour la vue (personnalisable)
- CTIT (Click-To-Install Time) : normal = de quelques minutes à quelques heures ; < 10 secondes = fraude par injection de clic ; > 24 h = suspect
- Les noms d'événements standard (AFInAppEventType) permettent une optimisation automatique par les réseaux publicitaires
- Les URL de postback informent les réseaux publicitaires des événements attribués

## Schémas {#patterns}

### Fonctionnement de l'attribution {#how-attribution-works}

1. L'utilisateur voit une publicité -> la plateforme publicitaire enregistre l'impression
2. L'utilisateur clique sur la publicité -> AppsFlyer enregistre le clic avec horodatage et empreinte
3. L'utilisateur installe l'application -> le SDK envoie le signal d'installation
4. AppsFlyer associe l'installation au clic (déterministe via GAID/IDFA, ou probabiliste via l'empreinte)
5. Un postback est envoyé au réseau publicitaire pour confirmer l'installation attribuée
6. Le rapport indique quelle campagne/source a généré l'installation

### Modèles d'attribution {#attribution-models}

| Modèle | Description | Cas d'usage |
|-------|-------------|----------|
| **Dernier clic** | 100 % du crédit au dernier clic avant l'installation | Par défaut, le plus courant |
| **Dernier contact** | 100 % du crédit à la dernière interaction (vue ou clic) | Attribution par vue |
| **Multi-touch** | Répartition du crédit entre tous les points de contact | Analyse de l'ensemble du tunnel |

### Intégration du SDK AppsFlyer {#appsflyer-sdk-integration}

**Android :**
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

**iOS :**
```swift
AppsFlyerLib.shared().appsFlyerDevKey = "YOUR_DEV_KEY"
AppsFlyerLib.shared().appleAppID = "YOUR_APP_ID"
AppsFlyerLib.shared().start()
```

### Suivi des événements in-app {#in-app-event-tracking}

```java
Map<String, Object> eventValues = new HashMap<>();
eventValues.put(AFInAppEventParameterName.PRICE, 200);
eventValues.put(AFInAppEventParameterName.CURRENCY, "USD");
eventValues.put(AFInAppEventParameterName.CONTENT_ID, "item_123");
AppsFlyerLib.getInstance().logEvent(context,
    AFInAppEventType.PURCHASE, eventValues);
```

Événements standard : `PURCHASE`, `ADD_TO_CART`, `TUTORIAL_COMPLETION`, `LEVEL_ACHIEVED`, `SUBSCRIBE`, `LOGIN`, `SEARCH`.

### Liens profonds {#deep-links}

- **URI Scheme** : `myapp://product/123` (ne fonctionne pas si l'application n'est pas installée)
- **Universal Links** (iOS) / **App Links** (Android) : liens HTTPS, ouvrent l'application si elle est installée, sinon le web
- **OneLink** (AppsFlyer) : lien unique pour toutes les plateformes + attribution

### Métriques de détection de fraude {#fraud-detection-metrics}

**Avant installation (métriques de clic) :**
- Clics courts (CTIT < 10 secondes) - générés par des bots
- Installations courtes - installation trop rapide après le clic
- Clics concordants - même appareil issu de plusieurs sources
- Installations concordantes - même appareil attribué plusieurs fois

**Après installation (comportement) :**
- Durées de session anormales
- Fréquence de session suspecte
- Installations hyperactives (trop nombreuses par appareil/IP)
- Installations sans lancement

**Matériel :**
- Changements fréquents de pays/région - usurpation de l'appareil
- Identifiants d'appareil incorrects - faux appareils

### Solutions anti-fraude {#anti-fraud-solutions}

**AppsFlyer Protect360** (multicouche) :
- Identification au niveau du SDK (le hachage post-compilation bloque les événements frauduleux)
- Détection d'anomalies par clusters (schémas de comportement de bots en temps réel)
- Règles de validation (seuils CTIT personnalisés par campagne/réseau)
- Calibrateur d'attribution (supprime la fraude et réattribue au bon canal)
- Analyse post-attribution (surveillance continue après attribution)
- Accès : sur demande (non disponible sur tous les forfaits)

**MyTracker Fraud Scanner :**
- Groupe 1 (strict) : installations courtes, clics concordants, appareils suspects - fraude quasi certaine
- Groupe 2 (fiable) : sessions anormalement courtes, installations sans lancement - nécessite du contexte
- Groupe 3 (souple) : installations longues, taux de conversion très faible - suspect mais potentiellement légitime

**AppMetrica** : pas de solution anti-fraude native. Intégration tierce FraudScore disponible.

### Écosystème du marché publicitaire {#ad-market-ecosystem}

- **Annonceur** - l'éditeur de l'application
- **Éditeur/Affilié** - site/application affichant les publicités
- **Réseau publicitaire** - met en relation annonceurs et éditeurs (Google Ads, Facebook, Unity Ads)
- **DSP** (Demand-Side Platform) - achat programmatique pour les annonceurs
- **SSP** (Supply-Side Platform) - vente programmatique pour les éditeurs
- **DMP** (Data Management Platform) - plateforme de données d'audience

### URL de postback {#postback-urls}

```text
https://ad-network.com/postback?
    idfa={idfa}&
    event={event_name}&
    value={revenue}&
    currency={currency}&
    campaign={campaign_id}
```

Les réseaux publicitaires utilisent les postbacks pour confirmer les installations, optimiser les enchères et éviter de payer pour de la fraude.

## Pièges {#gotchas}

- Protect360 n'est pas disponible par défaut sur tous les forfaits AppsFlyer : l'accès doit être demandé
- D'autres fournisseurs classent les installations frauduleuses comme organiques ; le calibrateur d'AppsFlyer les réattribue correctement
- Un volume d'installations bon marché est souvent corrélé à une faible LTV : analysez toujours le comportement par cohorte selon la source d'acquisition
- Les seuils CTIT doivent être personnalisés par application, région, partenaire et campagne : une approche unique ne fonctionne pas
- L'attribution par vue est intrinsèquement moins fiable que par clic : des fenêtres plus courtes réduisent les fausses attributions

## Voir aussi {#see-also}

- [[unit-economics]] - calculs de ROAS et de CPA
- [[mobile-analytics-platforms]] - analyse produit après attribution
- [[cohort-retention-analysis]] - qualité des cohortes selon la source d'acquisition
- [[web-marketing-analytics]] - modèles d'attribution web

---
title: "Analytics web et marketing"
category: concepts
tags: [bi-analytics, web-analytics, marketing, google-analytics, utm, gtm, attribution, funnel]
level: 4
source_sha256: e43d47749d35cb70c1476d4e621e45508efb34d63fbf7070901e1d7c483530b3
translation: machine
translated_at: '2026-10-24'
---
# Analytics web et marketing {#web-marketing-analytics}

L'analytics web et marketing regroupe les outils et méthodes permettant de mesurer l'efficacité d'un site web, la performance des sources de trafic et l'attribution multicanale. Cette discipline combine des plateformes d'analytics (GA, Yandex Metrica), la gestion de balises (GTM), le suivi par UTM et la modélisation de l'attribution.

## Faits clés {#key-facts}

- L'analytics n'est pas un métier de chiffres : c'est une manière de raisonner sur les chaînes de causalité
- Tâches de l'analyste web : mettre en place la collecte de données, construire des rapports sur les KPI, analyser les sources de trafic, analyser le tunnel de conversion, formuler et tester des hypothèses
- Les tags UTM sont le standard pour suivre les sources de trafic dans les URL
- Google Tag Manager supprime la dépendance aux développeurs pour la mise en place du suivi
- L'analytics multicanal (bout en bout) relie les dépenses publicitaires au chiffre d'affaires réel, tous canaux confondus
- Les modèles d'attribution déterminent comment le crédit est réparti entre les points de contact

## Modèles {#patterns}

### Métriques web clés {#key-web-metrics}

| Métrique | Description |
|--------|-------------|
| **ROI/ROMI** | Retour sur investissement publicitaire |
| **Revenu** | Revenu total |
| **Panier moyen** | Montant moyen d'une transaction |
| **LTV** | Revenu généré sur la durée de vie de l'utilisateur |
| **Taux de rétention** | % d'utilisateurs revenants |
| **Taux de rebond** | % de sessions avec une seule page vue / sans interaction |
| **Pages par session** | Profondeur de consommation du contenu |
| **Taux de conversion (CR)** | % d'utilisateurs réalisant l'action cible |

### Tags UTM {#utm-tags}

Paramètres d'URL pour le suivi des sources de trafic :
```text
site.com/?utm_source=google&utm_medium=cpc&utm_campaign=summer_sale
```

| Paramètre | Rôle | Exemples |
|-----------|---------|----------|
| `utm_source` | Source de trafic | google, yandex, vk |
| `utm_medium` | Type de canal | cpc, email, banner |
| `utm_campaign` | Nom de la campagne | summer_sale |
| `utm_term` | Mot-clé (recherche) | running_shoes |
| `utm_content` | Variante de publicité (A/B) | blue_button |

### Outils d'analytics web {#web-analytics-tools}

**Google Analytics (GA4)** : suivi basé sur les événements, rapports d'audience, d'acquisition, de comportement et de conversion, objectifs et tunnels, segments et dimensions personnalisées. Export BigQuery pour les données brutes.

**Yandex Metrica** : relecture de session (Webvisor), cartes de chaleur des clics, du défilement et des mouvements de souris, analyse des formulaires, tunnels, segments. Intégration poussée avec Yandex Direct.

**Hotjar** : cartes de chaleur, enregistrements de sessions, sondages de retour utilisateur, tunnels de conversion. Orienté recherche UX.

### Google Tag Manager (GTM) {#google-tag-manager-gtm}

Système de gestion de balises : aucun développeur n'est nécessaire pour le code de suivi.
- **Déclencheurs** : vue de page, DOM prêt, clic, défilement, soumission de formulaire, événement personnalisé
- **Variables** : sélecteurs CSS, valeurs de la couche de données, éléments de l'URL
- Mode aperçu et débogage pour tester avant publication

Exemple de push dans le DataLayer :
```javascript
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 25.42,
    'currency': 'USD'
  }
});
```

### Catégories de sources de trafic {#traffic-source-categories}

- Recherche organique (SEO)
- Recherche payante (PPC/publicité contextuelle)
- Réseaux sociaux (organique + payant)
- Marketing par e-mail
- Trafic direct
- Trafic de référence
- Publicité display

### Modèles d'attribution {#attribution-models}

| Modèle | Répartition du crédit | Cas d'usage |
|-------|-------------------|----------|
| **Dernier clic** | 100 % au dernier point de contact | Par défaut, le plus courant |
| **Premier clic** | 100 % au premier point de contact | Analyse des canaux de découverte |
| **Linéaire** | Répartition égale entre tous les points de contact | Vue d'ensemble équitable |
| **Décroissance temporelle** | Davantage de crédit aux points récents | Produits à cycle de décision long |
| **Basé sur la position** | 40/20/40 premier/milieu/dernier | Équilibre entre premier et dernier contact |

### Analytics multicanal {#cross-channel-analytics}

Analytics de bout en bout = connexion de toutes les sources de données :
- CRM (transactions, revenu)
- Plateformes publicitaires (Google Ads, Yandex Direct, Facebook)
- Analytics web (GA, Metrica)
- Suivi d'appels (prospects téléphoniques)
- Plateformes d'e-mailing

## Pièges courants {#gotchas}

- GA4 est basé sur les événements (et non sur les sessions comme Universal Analytics), ce qui modifie en profondeur la structure des données
- Les paramètres UTM sont sensibles à la casse : `utm_source=Google` et `utm_source=google` créent deux entrées distinctes
- La définition du taux de rebond diffère selon les versions de GA et ne doit pas être comparée entre outils
- Les modèles d'attribution peuvent donner des résultats très différents pour les mêmes données : il faut toujours savoir quel modèle est utilisé
- La relecture de session et les enregistrements Webvisor soulèvent des questions de confidentialité : vérifiez la conformité au RGPD ou à la réglementation locale

## Voir aussi {#see-also}

- [[funnel-analysis]] - techniques d'optimisation des tunnels
- [[mobile-attribution-fraud]] - attribution spécifique au mobile
- [[unit-economics]] - calcul du ROI et du ROAS
- [[product-analytics-fundamentals]] - distinction entre analytics produit et analytics marketing

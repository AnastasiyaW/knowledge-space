---
title: "Micro-frontends"
category: patterns
tags: [microfrontends, frontend, webpack-module-federation, single-spa, web-components]
level: 3
source_sha256: 22fd48f1bfd460e22e2f27641fd6515ee46a9b7e567739c21c73849c861237ea
translation: machine
translated_at: '2026-10-24'
---
# Micro-frontends {#microfrontends}

Les micro-frontends étendent les principes des microservices au frontend. Chaque micro-frontend est développé, testé et déployé de manière indépendante, aligné sur un domaine métier.

## Processus de migration en 5 étapes {#5-stage-migration-process}

### 1. Analyse préliminaire {#1-preliminary-analysis}
- Évaluer la complexité et l'échelle de l'application
- Formuler les objectifs de migration
- Évaluer l'expérience de l'équipe
- Appliquer le DDD pour identifier les bounded contexts

### 2. Définir les fonctions métier {#2-define-business-functions}
Chaque micro-frontend correspond à un domaine : catalogue produits, paiement, profil utilisateur, panneau d'administration. L'autonomie des équipes est le moteur principal.

### 3. Choisir la méthode d'intégration {#3-choose-integration-method}

| Méthode | Type | Avantages | Inconvénients |
|--------|------|------|------|
| **Webpack Module Federation** | Build/Runtime | Partage de modules à l'exécution, la plus populaire | Configuration complexe |
| **Single-SPA** | Côté client | Orchestrateur indépendant du framework | Courbe d'apprentissage |
| **Composition côté serveur** | Côté serveur | Bon référencement, chargement initial rapide | Moins interactive |
| **iframes** | Côté client | Isolation complète | Communication limitée |
| **Web Components** | Côté client | Basé sur les standards | Support navigateur variable |
| **Hybride** | Les deux | Le meilleur des deux mondes | Le plus complexe |

### 4. Sélection du framework/outil {#4-frameworktool-selection}

**Webpack Module Federation :**
```javascript
// Host app
new ModuleFederationPlugin({
  remotes: {
    checkout: "checkout@http://checkout.example.com/remoteEntry.js"
  },
  shared: { react: { singleton: true } }
})

// Checkout micro-frontend
new ModuleFederationPlugin({
  name: "checkout",
  exposes: { "./CheckoutForm": "./src/CheckoutForm" },
  shared: { react: { singleton: true } }
})
```

**Single-SPA :** Orchestrateur indépendant du framework. Enregistrer les applications, gérer leur cycle de vie (bootstrap, mount, unmount). Prend en charge React, Vue, Angular, Svelte simultanément. Activation basée sur les routes.

### 5. Communication inter-modules {#5-inter-module-communication}

| Méthode | Couplage | Cas d'usage |
|--------|---------|----------|
| **API/BFF** | Faible | Chaque MFE dispose d'un backend dédié |
| **Événements personnalisés** | Faible | `window.dispatchEvent` / `addEventListener` |
| **URL/routage** | Faible | Transmettre l'état via les paramètres d'URL |
| **État global** | Fort (à éviter) | Redux partagé - casse l'isolation |

## Décisions d'architecture clés {#key-architectural-decisions}

**Dépendances partagées :** Arbitrer entre la taille du bundle (partager React) et l'indépendance (chacun embarque sa propre version). Configuration `shared` de Module Federation avec des plages de versions.

**Isolation des styles :** CSS Modules, Shadow DOM, CSS-in-JS avec des préfixes uniques, BEM avec un préfixe d'équipe.

**Authentification :** Service d'authentification centralisé. Le shell gère la connexion et transmet le jeton aux micro-frontends.

**Frontières d'erreur :** Chaque MFE dispose d'une error boundary. Une défaillance ne doit pas faire planter les autres.

## Quand l'utiliser {#when-to-use}

**Cas adapté :** Grandes équipes (5+ développeurs frontend), plusieurs équipes sur un même produit, déploiement indépendant nécessaire, besoins technologiques différents selon les sections, migration legacy (Strangler Fig).

**Cas peu adapté :** Petite équipe (<5 développeurs), application simple, couplage fort entre les fonctionnalités, SPA critique en performance, équipe sans maturité DevOps.

## Considérations de performance {#performance-considerations}

- Le chargement initial peut être plus lent (plusieurs bundles)
- Chargement différé à l'activation des routes
- Partager les dépendances communes (React, design system)
- Précharger les micro-frontends critiques
- SSR pour le chargement initial de la page
- Surveiller la taille des bundles de manière indépendante

## Pièges à éviter {#gotchas}

- **Conflits CSS** entre MFE - toujours utiliser une stratégie d'isolation (CSS Modules, Shadow DOM)
- **L'état partagé** casse l'indépendance - privilégier les événements ou l'URL plutôt qu'un store global
- **Conflits de versions** - des MFE qui veulent des versions de React différentes. `singleton: true` de Module Federation aide, mais ne supprime pas le problème
- **Tests d'intégration** - les tests unitaires par MFE sont simples, tester la communication entre MFE nécessite une infrastructure de tests d'intégration dédiée
- **Coordination des déploiements** toujours nécessaire pour les contrats partagés, même avec des déploiements indépendants

## Voir aussi {#see-also}

- [[architectural-styles]] - Évolution des microservices, incluant les micro-frontends
- [[microservices-communication]] - Le pattern BFF pour le frontend
- [[enterprise-integration]] - Le pattern API Gateway

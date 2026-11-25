---
title: "Microfrontends"
category: patterns
tags: [microfrontends, frontend, webpack-module-federation, single-spa, web-components]
level: 3
source_sha256: 22fd48f1bfd460e22e2f27641fd6515ee46a9b7e567739c21c73849c861237ea
translation: machine
translated_at: '2026-10-24'
---
# Microfrontends {#microfrontends}

Microfrontends übertragen die Prinzipien von Microservices auf das Frontend. Jedes Micro-Frontend wird unabhängig entwickelt, getestet und deployt und ist an einer Geschäftsdomäne ausgerichtet.

## 5-Stufen-Migrationsprozess {#5-stage-migration-process}

### 1. Vorab-Analyse {#1-preliminary-analysis}
- Komplexität und Umfang der Anwendung bewerten
- Migrationsziele formulieren
- Erfahrung des Teams einschätzen
- DDD anwenden, um Bounded Contexts zu identifizieren

### 2. Geschäftsfunktionen definieren {#2-define-business-functions}
Jedes Microfrontend ist an einer Domäne ausgerichtet: Produktkatalog, Checkout, Benutzerprofil, Admin-Panel. Die Autonomie der Teams ist der wichtigste Treiber.

### 3. Integrationsmethode wählen {#3-choose-integration-method}

| Methode | Typ | Vorteile | Nachteile |
|--------|------|------|------|
| **Webpack Module Federation** | Build/Runtime | Module zur Laufzeit teilen, am populärsten | Komplexe Konfiguration |
| **Single-SPA** | Client-seitig | Framework-agnostischer Orchestrator | Einarbeitungsaufwand |
| **Server-seitige Komposition** | Server-seitig | Gute SEO, schnelles initiales Laden | Weniger interaktiv |
| **iframes** | Client-seitig | Vollständige Isolation | Eingeschränkte Kommunikation |
| **Web Components** | Client-seitig | Standardbasiert | Browser-Unterstützung variiert |
| **Hybrid** | Beides | Das Beste aus beiden Welten | Am komplexesten |

### 4. Auswahl von Framework/Tool {#4-frameworktool-selection}

**Webpack Module Federation:**
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

**Single-SPA:** Framework-agnostischer Orchestrator. Anwendungen registrieren, Lebenszyklus verwalten (bootstrap, mount, unmount). Unterstützt React, Vue, Angular, Svelte gleichzeitig. Routenbasierte Aktivierung.

### 5. Kommunikation zwischen Modulen {#5-inter-module-communication}

| Methode | Kopplung | Anwendungsfall |
|--------|---------|----------|
| **API/BFF** | Lose | Jedes MFE hat ein eigenes Backend |
| **Custom Events** | Lose | `window.dispatchEvent` / `addEventListener` |
| **URL/Routing** | Lose | Zustand über URL-Parameter übergeben |
| **Globaler Zustand** | Eng (vermeiden) | Gemeinsames Redux - hebelt die Isolation aus |

## Zentrale Architekturentscheidungen {#key-architectural-decisions}

**Gemeinsame Abhängigkeiten:** Abwägung zwischen Bundle-Größe (React teilen) und Unabhängigkeit (jedes bündelt eigene Versionen). Module Federation `shared`-Konfiguration mit Versionsbereichen.

**Style-Isolation:** CSS Modules, Shadow DOM, CSS-in-JS mit eindeutigen Präfixen, BEM mit Team-Präfix.

**Authentifizierung:** Zentraler Auth-Service. Die Shell übernimmt den Login und übergibt das Token an die Microfrontends.

**Error Boundaries:** Jedes MFE hat eine Error Boundary. Ein Fehler darf nicht die anderen zum Absturz bringen.

## Wann einsetzen {#when-to-use}

**Gut geeignet:** Große Teams (5+ Frontend-Entwickler), mehrere Teams am selben Produkt, unabhängiges Deployment nötig, unterschiedliche Technologieanforderungen je Bereich, Legacy-Migration (Strangler Fig).

**Schlecht geeignet:** Kleines Team (<5 Entwickler), einfache Anwendung, enge Kopplung zwischen Features, performancekritische SPA, Team ohne ausgereifte DevOps-Praxis.

## Performance-Überlegungen {#performance-considerations}

- Initiales Laden kann langsamer sein (mehrere Bundles)
- Lazy Loading bei Routenaktivierung
- Gemeinsame Abhängigkeiten teilen (React, Design System)
- Kritische Microfrontends vorab laden (Pre-Fetching)
- SSR für das initiale Laden der Seite
- Bundle-Größen unabhängig überwachen

## Stolperfallen {#gotchas}

- **CSS-Konflikte** zwischen MFEs - immer eine Isolationsstrategie verwenden (CSS Modules, Shadow DOM)
- **Geteilter Zustand** hebelt die Unabhängigkeit aus - Events/URL gegenüber einem globalen Store bevorzugen
- **Versionskonflikte** - verschiedene MFEs benötigen unterschiedliche React-Versionen. `singleton: true` in Module Federation hilft, beseitigt das Problem aber nicht vollständig
- **Testen der Integration** - Unit-Tests pro MFE sind einfach, das Testen der Kommunikation zwischen MFEs erfordert eine eigene Integrationstest-Infrastruktur
- **Abstimmung beim Deployment** ist auch bei unabhängigen Deployments für gemeinsame Verträge (Shared Contracts) weiterhin nötig

## Siehe auch {#see-also}

- [[architectural-styles]] - Entwicklung von Microservices, inklusive Micro-Frontends
- [[microservices-communication]] - BFF-Muster für das Frontend
- [[enterprise-integration]] - API-Gateway-Muster

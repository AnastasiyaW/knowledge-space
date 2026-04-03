---
title: Microfrontends
category: patterns
tags: [microfrontends, frontend, webpack-module-federation, single-spa, web-components]
---

# Microfrontends

Microfrontends extend microservices principles to the frontend. Each micro-frontend is independently developed, tested, and deployed, aligned with a business domain.

## 5-Stage Migration Process

### 1. Preliminary Analysis
- Assess application complexity and scale
- Formulate migration goals
- Evaluate team experience
- Apply DDD to identify bounded contexts

### 2. Define Business Functions
Each microfrontend aligns with a domain: product catalog, checkout, user profile, admin panel. Team autonomy is the primary driver.

### 3. Choose Integration Method

| Method | Type | Pros | Cons |
|--------|------|------|------|
| **Webpack Module Federation** | Build/Runtime | Share modules at runtime, most popular | Complex config |
| **Single-SPA** | Client-side | Framework-agnostic orchestrator | Learning curve |
| **Server-side composition** | Server-side | Good SEO, fast initial load | Less interactive |
| **iframes** | Client-side | Full isolation | Limited communication |
| **Web Components** | Client-side | Standards-based | Browser support varies |
| **Hybrid** | Both | Best of both worlds | Most complex |

### 4. Framework/Tool Selection

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

**Single-SPA:** Framework-agnostic orchestrator. Register apps, manage lifecycle (bootstrap, mount, unmount). Supports React, Vue, Angular, Svelte simultaneously. Route-based activation.

### 5. Inter-Module Communication

| Method | Coupling | Use Case |
|--------|---------|----------|
| **API/BFF** | Loose | Each MFE has dedicated backend |
| **Custom Events** | Loose | `window.dispatchEvent` / `addEventListener` |
| **URL/routing** | Loose | Pass state via URL parameters |
| **Global state** | Tight (avoid) | Shared Redux - breaks isolation |

## Key Architectural Decisions

**Shared dependencies:** Balance bundle size (share React) vs independence (each bundles own). Module Federation `shared` config with version ranges.

**Styling isolation:** CSS Modules, Shadow DOM, CSS-in-JS with unique prefixes, BEM with team prefix.

**Authentication:** Centralized auth service. Shell handles login, passes token to microfrontends.

**Error boundaries:** Each MFE has error boundary. One failure must not crash others.

## When to Use

**Good fit:** Large teams (5+ frontend devs), multiple teams on same product, independent deployment needed, different tech requirements per section, legacy migration (Strangler Fig).

**Poor fit:** Small team (<5 devs), simple app, tight coupling between features, performance-critical SPA, team lacks DevOps maturity.

## Performance Considerations

- Initial load may be slower (multiple bundles)
- Lazy loading on route activation
- Share common dependencies (React, design system)
- Pre-fetch critical microfrontends
- SSR for initial page load
- Monitor bundle sizes independently

## Gotchas

- **CSS conflicts** between MFEs - always use isolation strategy (CSS Modules, Shadow DOM)
- **Shared state** breaks independence - prefer events/URL over global store
- **Version conflicts** - different MFEs wanting different React versions. Module Federation `singleton: true` helps but doesn't eliminate
- **Testing integration** - unit tests per MFE are easy, testing communication between MFEs requires dedicated integration test infrastructure
- **Deployment coordination** still needed for shared contracts even with independent deploys

## See Also

- [[architectural-styles]] - Microservices evolution including micro-frontends
- [[microservices-communication]] - BFF pattern for frontend
- [[enterprise-integration]] - API Gateway pattern

---
title: Web & Marketing Analytics
category: concepts
tags: [bi-analytics, web-analytics, marketing, google-analytics, utm, gtm, attribution, funnel]
---

# Web & Marketing Analytics

Web and marketing analytics encompasses the tools and methods for measuring website effectiveness, traffic source performance, and cross-channel attribution. The discipline combines analytics platforms (GA, Yandex Metrica), tag management (GTM), UTM tracking, and attribution modeling.

## Key Facts

- Analytics is not a numbers profession - it's a way of thinking about causal chains
- Web analyst tasks: set up data collection, build reports on KPIs, analyze traffic sources, analyze funnel, form and test hypotheses
- UTM tags are the standard for traffic source tracking in URLs
- Google Tag Manager eliminates developer dependency for tracking setup
- Cross-channel (end-to-end) analytics connects ad spend with actual revenue across all channels
- Attribution models determine how credit is distributed across touchpoints

## Patterns

### Key Web Metrics

| Metric | Description |
|--------|-------------|
| **ROI/ROMI** | Return on advertising investment |
| **Revenue** | Total income |
| **Average Order Value** | Mean transaction size |
| **LTV** | Revenue over user's lifetime |
| **Retention Rate** | % returning users |
| **Bounce Rate** | % sessions with single pageview / no interaction |
| **Pages per Session** | Content consumption depth |
| **Conversion Rate (CR)** | % completing target action |

### UTM Tags

URL parameters for traffic source tracking:
```text
site.com/?utm_source=google&utm_medium=cpc&utm_campaign=summer_sale
```

| Parameter | Purpose | Examples |
|-----------|---------|----------|
| `utm_source` | Traffic source | google, yandex, vk |
| `utm_medium` | Channel type | cpc, email, banner |
| `utm_campaign` | Campaign name | summer_sale |
| `utm_term` | Keyword (search) | running_shoes |
| `utm_content` | Ad variant (A/B) | blue_button |

### Web Analytics Tools

**Google Analytics (GA4)**: event-based tracking, audience/acquisition/behavior/conversion reports, goals and funnels, segments and custom dimensions. BigQuery export for raw data.

**Yandex Metrica**: session replay (Webvisor), click/scroll/movement heatmaps, form analytics, funnels, segments. Deep integration with Yandex Direct.

**Hotjar**: heatmaps, session recordings, feedback polls, conversion funnels. UX research focused.

### Google Tag Manager (GTM)

Tag management system - no developer needed for tracking code:
- **Triggers**: page view, DOM ready, click, scroll, form submit, custom event
- **Variables**: CSS selectors, data layer values, URL parts
- Preview and debug mode for testing before publish

DataLayer push example:
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

### Traffic Source Categories

- Organic search (SEO)
- Paid search (PPC/contextual advertising)
- Social media (organic + paid)
- Email marketing
- Direct traffic
- Referral traffic
- Display advertising

### Attribution Models

| Model | Credit Distribution | Use Case |
|-------|-------------------|----------|
| **Last click** | 100% to last touchpoint | Default, most common |
| **First click** | 100% to first touchpoint | Discovery channel analysis |
| **Linear** | Equal across all touchpoints | Fair overview |
| **Time decay** | More credit to recent | Consideration-heavy products |
| **Position-based** | 40/20/40 first/middle/last | Balanced first+last emphasis |

### Cross-Channel Analytics

End-to-end analytics = connecting all data sources:
- CRM (deals, revenue)
- Ad platforms (Google Ads, Yandex Direct, Facebook)
- Web analytics (GA, Metrica)
- Call tracking (phone leads)
- Email platforms

## Gotchas

- GA4 is event-based (not session-based like Universal Analytics) - this fundamentally changes how data is structured
- UTM parameters are case-sensitive - `utm_source=Google` and `utm_source=google` create separate entries
- Bounce rate definition differs between GA versions and should not be compared across tools
- Attribution models can give dramatically different results for the same data - always understand which model is in use
- Webvisor/session recordings raise privacy concerns - ensure GDPR/privacy compliance in your region

## See Also

- [[funnel-analysis]] - funnel optimization techniques
- [[mobile-attribution-fraud]] - mobile-specific attribution
- [[unit-economics]] - ROI and ROAS calculations
- [[product-analytics-fundamentals]] - product vs marketing analytics distinction

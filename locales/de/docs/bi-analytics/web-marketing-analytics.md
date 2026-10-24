---
title: "Web- & Marketing-Analytik"
category: concepts
tags: [bi-analytics, web-analytics, marketing, google-analytics, utm, gtm, attribution, funnel]
level: 4
source_sha256: e43d47749d35cb70c1476d4e621e45508efb34d63fbf7070901e1d7c483530b3
translation: machine
translated_at: '2026-10-24'
---
# Web- & Marketing-Analytik {#web-marketing-analytics}

Web- und Marketing-Analytik umfasst die Werkzeuge und Methoden zur Messung der Effektivität von Websites, der Leistung von Traffic-Quellen und der kanalübergreifenden Attribution. Die Disziplin kombiniert Analytics-Plattformen (GA, Yandex Metrica), Tag-Management (GTM), UTM-Tracking und Attributionsmodellierung.

## Kernfakten {#key-facts}

- Analytik ist kein Zahlenberuf – sie ist eine Denkweise über kausale Ketten
- Aufgaben von Web-Analysten: Datenerhebung einrichten, Reports zu KPIs erstellen, Traffic-Quellen analysieren, Funnel analysieren, Hypothesen bilden und testen
- UTM-Tags sind der Standard für das Tracking von Traffic-Quellen in URLs
- Google Tag Manager macht Entwickler für das Einrichten des Trackings unabhängig
- Kanalübergreifende (End-to-End-)Analytik verbindet Werbeausgaben mit dem tatsächlichen Umsatz über alle Kanäle hinweg
- Attributionsmodelle bestimmen, wie die Anerkennung auf die Touchpoints verteilt wird

## Muster {#patterns}

### Zentrale Web-Metriken {#key-web-metrics}

| Metrik | Beschreibung |
|--------|-------------|
| **ROI/ROMI** | Rendite der Werbeinvestition |
| **Umsatz** | Gesamteinnahmen |
| **Average Order Value** | Durchschnittliche Transaktionsgröße |
| **LTV** | Umsatz über die Lebensdauer eines Nutzers |
| **Retention Rate** | % wiederkehrender Nutzer |
| **Bounce Rate** | % Sessions mit einer einzelnen Seitenansicht / ohne Interaktion |
| **Pages per Session** | Tiefe des Content-Konsums |
| **Conversion Rate (CR)** | % der Nutzer, die die Zielaktion abschließen |

### UTM-Tags {#utm-tags}

URL-Parameter für das Tracking von Traffic-Quellen:
```text
site.com/?utm_source=google&utm_medium=cpc&utm_campaign=summer_sale
```

| Parameter | Zweck | Beispiele |
|-----------|-------|----------|
| `utm_source` | Traffic-Quelle | google, yandex, vk |
| `utm_medium` | Kanaltyp | cpc, email, banner |
| `utm_campaign` | Kampagnenname | summer_sale |
| `utm_term` | Keyword (Suche) | running_shoes |
| `utm_content` | Anzeigenvariante (A/B) | blue_button |

### Web-Analytics-Werkzeuge {#web-analytics-tools}

**Google Analytics (GA4)**: ereignisbasiertes Tracking, Berichte zu Zielgruppe/Akquisition/Verhalten/Conversions, Ziele und Funnels, Segmente und benutzerdefinierte Dimensionen. BigQuery-Export für Rohdaten.

**Yandex Metrica**: Session-Replay (Webvisor), Klick-, Scroll- und Bewegungs-Heatmaps, Formularanalysen, Funnels, Segmente. Tiefe Integration mit Yandex Direct.

**Hotjar**: Heatmaps, Session-Aufzeichnungen, Feedback-Umfragen, Conversion-Funnels. Fokus auf UX-Forschung.

### Google Tag Manager (GTM) {#google-tag-manager-gtm}

Tag-Management-System – für den Tracking-Code wird kein Entwickler benötigt:
- **Trigger**: Seitenaufruf, DOM ready, Klick, Scroll, Formularabsendung, benutzerdefiniertes Ereignis
- **Variablen**: CSS-Selektoren, Data-Layer-Werte, URL-Bestandteile
- Vorschau- und Debug-Modus zum Testen vor der Veröffentlichung

Beispiel für einen DataLayer-Push:
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

### Kategorien von Traffic-Quellen {#traffic-source-categories}

- Organische Suche (SEO)
- Bezahlte Suche (PPC/Kontextwerbung)
- Social Media (organisch + bezahlt)
- E-Mail-Marketing
- Direct Traffic
- Referral-Traffic
- Display-Werbung

### Attributionsmodelle {#attribution-models}

| Modell | Verteilung der Anerkennung | Anwendungsfall |
|--------|---------------------------|----------------|
| **Last Click** | 100 % an den letzten Touchpoint | Standard, am häufigsten verwendet |
| **First Click** | 100 % an den ersten Touchpoint | Analyse von Entdeckungskanälen |
| **Linear** | Gleichmäßig auf alle Touchpoints | Faire Gesamtübersicht |
| **Time Decay** | Mehr Anerkennung für neuere Touchpoints | Produkte mit langer Entscheidungsphase |
| **Position-based** | 40/20/40 für erster/mittlerer/letzter Touchpoint | Ausgewogene Betonung von erstem und letztem Touchpoint |

### Kanalübergreifende Analytik {#cross-channel-analytics}

End-to-End-Analytik = Verknüpfung aller Datenquellen:
- CRM (Deals, Umsatz)
- Werbeplattformen (Google Ads, Yandex Direct, Facebook)
- Web-Analytics (GA, Metrica)
- Call-Tracking (Telefonanfragen)
- E-Mail-Plattformen

## Stolperfallen {#gotchas}

- GA4 ist ereignisbasiert (nicht sitzungsbasiert wie Universal Analytics) – das verändert grundlegend, wie Daten strukturiert sind
- UTM-Parameter unterscheiden zwischen Groß- und Kleinschreibung – `utm_source=Google` und `utm_source=google` erzeugen getrennte Einträge
- Die Definition der Bounce Rate unterscheidet sich zwischen GA-Versionen und sollte nicht über Tools hinweg verglichen werden
- Attributionsmodelle können für dieselben Daten drastisch unterschiedliche Ergebnisse liefern – immer klären, welches Modell verwendet wird
- Webvisor/Session-Aufzeichnungen werfen Datenschutzfragen auf – in Ihrer Region die Einhaltung von DSGVO bzw. Datenschutzvorgaben sicherstellen

## Siehe auch {#see-also}

- [[funnel-analysis|Funnel-Analyse]] - Techniken zur Funnel-Optimierung
- [[mobile-attribution-fraud|Mobile-Attribution-Betrug]] - mobilespezifische Attribution
- [[unit-economics|Unit Economics]] - ROI- und ROAS-Berechnungen
- [[product-analytics-fundamentals|Grundlagen der Produktanalytik]] - Unterscheidung Produkt- vs. Marketing-Analytik

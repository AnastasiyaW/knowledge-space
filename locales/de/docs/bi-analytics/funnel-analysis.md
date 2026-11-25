---
title: "Funnel-Analyse"
category: concepts
tags: [bi-analytics, product-analytics, funnel, conversion, optimization]
level: 2
source_sha256: 94af672a6b8552d16a083c5ba7782651afa1c8227cd96848a4fa52fcb38e8c87
translation: machine
translated_at: '2026-10-24'
---
# Funnel-Analyse {#funnel-analysis}

Die Funnel-Analyse visualisiert und misst den Fortschritt von Nutzern durch einen mehrstufigen Ablauf hin zu einem Conversion-Ziel. Jeder Schritt steht für eine Nutzeraktion, und die Analyse konzentriert sich auf die Abbruchraten zwischen den Schritten, um Optimierungspotenziale zu identifizieren.

## Key Facts {#key-facts}

- Funnel = Abfolge von Nutzerschritten hin zu einem Conversion-Ziel
- Zentrale Kennzahlen: Schritt-Conversion (N zu N+1), Gesamt-Conversion, Abbruchpunkte, Zeit zwischen den Schritten
- Typischer E-Commerce-Funnel: Besucher -> Produktseite -> In den Warenkorb -> Checkout-Start -> Zahlung -> Bestellung abgeschlossen
- Typischer Funnel einer Mobile-App: app_open -> registration_start -> registration_complete -> onboarding_complete -> first_purchase
- Die Funnel-Optimierung adressiert zuerst den Schritt mit dem größten Abbruch
- Das Zeitfenster ist entscheidend: Ein Funnel gilt nur dann als abgeschlossen, wenn er innerhalb von N Tagen/Stunden durchlaufen wird

## Patterns {#patterns}

### Funnel-Optimierungsprozess {#funnel-optimization-process}

1. Schritt mit dem größten Abbruch identifizieren
2. Ursache formulieren (verwirrende UX, zu viele Schritte, unklarer Nutzen)
3. Verbesserung testen (A/B oder sequenziell)
4. Veränderung der Conversion messen

### Kritischer Nutzerpfad (Event Map) {#critical-user-path-event-map}

Die minimale Abfolge von Events, die die zentrale Nutzerreise definiert:
1. `app_open` - App gestartet
2. `registration_start` - Registrierungsablauf geöffnet
3. `registration_complete` - Konto erstellt
4. `onboarding_complete` - Tutorial abgeschlossen
5. `first_purchase` - erste Zahlung

### Priorisierung von Events {#event-prioritization}

1. Geschäftliche KPI-Events (Kauf, Abonnement, Aktivierung)
2. Funnel-Schritt-Events (zentrale Bildschirme, zentrale Aktionen)
3. Fehler-/Absturz-Events (Probleme identifizieren)
4. Engagement-Events (Tiefe der Funktionsnutzung)

### Funnel-Analyse in Amplitude {#funnel-analysis-in-amplitude}

- Abfolge von Events definieren: `sign_up` -> `onboarding_complete` -> `first_purchase`
- Zeigt den Abbruch an jedem Schritt
- Nach Eigenschaft segmentieren: Conversion für iOS vs. Android vergleichen
- Zeitfenster: Funnel nur zählen, wenn er innerhalb von N Tagen/Stunden abgeschlossen wird

### SQL-Funnel-Muster {#sql-funnel-pattern}

```sql
SELECT
    COUNT(CASE WHEN event = 'page_view' THEN user_id END) as step1_views,
    COUNT(CASE WHEN event = 'add_to_cart' THEN user_id END) as step2_cart,
    COUNT(CASE WHEN event = 'checkout_start' THEN user_id END) as step3_checkout,
    COUNT(CASE WHEN event = 'purchase' THEN user_id END) as step4_purchase
FROM events
WHERE event_date = CURRENT_DATE;
```

### Install-Conversion-Rate (App Stores) {#install-conversion-rate-app-stores}

**Conversion-Rate** = Installationen / Produktseitenaufrufe. Richtwert: 25–35 % für gut optimierte Apps.

Elemente, die die Conversion beeinflussen:
- **Icon** - erster visueller Eindruck, auch in kleiner Darstellung erkennbar
- **Screenshots** - die ersten 2–3 sind ohne Scrollen sichtbar (am wichtigsten)
- **Vorschauvideo** - wird auf iOS automatisch abgespielt; den Kernnutzen in den ersten 3 Sekunden zeigen
- **App-Name + Untertitel** - vermitteln das Nutzenversprechen sofort
- **Bewertungen** - Apps unter 4,0 haben eine deutlich geringere Conversion
- **Rezensionen** - aktuelle positive Rezensionen zählen mehr als alte

## Gotchas {#gotchas}

- Funnel-Analysen ohne Zeitfenster können irreführend sein – ein Nutzer, der heute startet und 90 Tage später kauft, unterscheidet sich von einem, der in 10 Minuten abschließt
- Das Zählen von Events und das Zählen eindeutiger Nutzer ergibt sehr unterschiedliche Funnel-Verläufe
- Nicht-lineare Funnels (Nutzer überspringen Schritte, gehen zurück) erfordern eine sitzungsbasierte Analyse statt einfacher Schrittzählung
- Die Segmentierung von Funnels nach Akquisitionsquelle zeigt oft, dass aggregierte Zahlen stark unterschiedliche Verhaltensmuster verbergen

## See Also {#see-also}

- [[product-analytics-fundamentals]] - metrics pyramid and analyst role
- [[cohort-retention-analysis]] - post-funnel retention tracking
- [[web-marketing-analytics]] - web funnel setup with GA/GTM
- [[mobile-analytics-platforms]] - funnel tools in Firebase, Amplitude
- [[app-store-optimization]] - app store conversion funnels

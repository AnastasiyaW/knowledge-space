---
title: "Unit Economics"
category: concepts
tags: [bi-analytics, unit-economics, ltv, cpa, arpu, business-metrics]
level: 3
source_sha256: 7a1b2fa1a2306b3f97e0069316b5970a7ca0a8a43d7cb7b6286de403aaf4df85
translation: machine
translated_at: '2026-10-24'
---
# Unit Economics {#unit-economics}

Unit Economics ist eine ökonomische Modellierungsmethode zur Bestimmung der Rentabilität eines Geschäfts, indem die Profitabilität pro Produkteinheit oder pro einzelnem Kunden bewertet wird. Sie kommt zum Einsatz beim Start von Startups, bei der Planung der Skalierung, bei Investorenpräsentationen oder wenn Kundengewinnung und Werbung die wichtigsten Kostentreiber sind.

## Key Facts {#key-facts}

- Kernformel: `Profit = Revenue - Variable Costs - Fixed Costs`
- Das Geschäft ist tragfähig, wenn Gross Profit > Fixed Costs
- **Gross Profit is King** - die wichtigste Kennzahl für Unit Economics
- Höhere Cost-per-Lead bedeutet nicht schlechtere Wirtschaftlichkeit - die Lead-Qualität (Conversion zum Abschluss) ist wichtiger als die Menge
- Der Deckungsbeitrag (Umsatz minus variable Kosten pro Einheit) muss positiv sein, bevor skaliert wird

## Core Formulas {#core-formulas}

```yaml
Profit (Margin) = Gross Profit - Fixed Costs
Gross Profit = Revenue - Variable Costs

Main Unit Economics Formula:
User Acquisition x (ARPU - CPA) = Gross Profit

Where:
ARPU = C1 x APC x AvP x Margin

Expanded:
User Acquisition x (C1 x APC x AvP x Margin - CPA) = Gross Profit

Payback Period = CPA / (Monthly ARPU x Margin)
```

## Patterns {#patterns}

### Key Metrics {#key-metrics}

| Metric | Definition |
|--------|-----------|
| **CPA/CAC** | Cost Per Acquisition / Customer Acquisition Cost |
| **ARPU** | Average Revenue Per User |
| **GMV** | Gross Merchandise Value - Gesamtvolumen vor Abzug der Kosten |
| **LTV** | Lifetime Value - Gesamtumsatz eines Kunden über dessen Lebensdauer |
| **ROMI** | Return on Marketing Investment |
| **C1** | Conversion zum ersten Kauf (% der Nutzer) |
| **APC** | Average Payment Count (Wiederholungskäufe) |
| **AvP** | Average Price per transaction |
| **COGS** | Cost of Goods Sold - direkte Kosten pro Transaktion |
| **ROAS** | Return On Ad Spend = Revenue / Ad Spend |
| **ROI** | Return on Investment = (Revenue - Cost) / Cost |

### Marketing Cost Metrics {#marketing-cost-metrics}

| Metric | Formula |
|--------|---------|
| **CPI** | Cost Per Install = Ad Spend / Installs |
| **CPC** | Cost Per Click = Ad Spend / Clicks |
| **CPM** | Cost Per Mille = Cost per 1,000 impressions |
| **CTR** | Click-Through Rate = Clicks / Impressions |
| **CVR** | Conversion Rate = Actions / Clicks |

### Growth Levers (Goldratt Theory of Constraints) {#growth-levers-goldratt-theory-of-constraints}

1. Den Parameter finden, dessen Änderung den größten Beitrag zum Gross Profit liefert
2. Das Produkt diesem Parameter unterordnen (Fokus darauf legen)
3. Ihn ausbauen/skalieren

Mögliche Entscheidungen auf Basis der Kennzahlen:
- Mehr Nutzer gewinnen (User Acquisition erhöhen)
- Akquisitionskosten senken (CPA reduzieren)
- Conversion zum Kauf steigern (C1 erhöhen)
- Durchschnittlichen Bestellwert steigern (AvP erhöhen)
- Anzahl der Wiederholungskäufe erhöhen (APC erhöhen)
- GMV steigern

### RFM Segmentation (DAX Example) {#rfm-segmentation-dax-example}

RFM = Recency, Frequency, Monetary - Modell zur Kundensegmentierung:

```dax
Recency = DATEDIFF(MAX(Orders[OrderDate]), TODAY(), DAY)
Frequency = COUNT(Orders[OrderID])
Monetary = SUM(Orders[Revenue])
```

Kunden in jeder Dimension auf einer Skala von 1-5 einstufen und zu einem RFM-Score für die Zielgruppenauswahl kombinieren.

## Gotchas {#gotchas}

- Ein günstiger Akquisitionskanal mit Nutzern geringer Qualität ist schlechter als ein teurer Kanal mit Nutzern hohen LTV - das Kohortenverhalten immer nach Akquisitionsquelle analysieren
- Der über alle Nutzer gemittelte ARPU kann bimodale Verteilungen verdecken (Wale vs. kostenlose Nutzer)
- Die Payback-Periode ist für Abonnementmodelle entscheidend - ist Payback > durchschnittliche Nutzerlebensdauer, funktioniert das Modell nicht
- Unit Economics, die beim Launch berechnet wurden, halten bei Skalierung möglicherweise nicht, aufgrund von Marktsättigung und steigenden Akquisitionskosten

## See Also {#see-also}

- [[product-metrics-framework]] - DAU/MAU und Engagement-Kennzahlen
- [[cohort-retention-analysis]] - kohortenbasierte LTV-Analyse
- [[mobile-attribution-fraud]] - Attribution und ROAS-Messung
- [[web-marketing-analytics]] - Analyse der Traffic-Quellen und ROI

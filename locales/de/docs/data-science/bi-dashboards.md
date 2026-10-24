---
title: "BI-Systeme und Dashboards"
category: practices
tags: [data-science, bi, dashboards, analytics, tableau, superset]
level: 3
source_sha256: d5bbdd57e9558ca11ecf63eaae8fbd6eb4062382baf3a6dbaa7a9d3d4af482e6
translation: machine
translated_at: '2026-10-24'
---
# BI-Systeme und Dashboards {#bi-systems-and-dashboards}

Business Intelligence verwandelt Daten in umsetzbare Entscheidungen. Ein BI-System ist ein Produkt und kein einmaliges Projekt. Behandelt werden Dashboard-Design, Tool-Auswahl und die Analytics-Infrastruktur-Pipeline.

## Dashboard-Typen {#dashboard-types}

| Typ | Zweck | Designmuster |
|-----|-------|--------------|
| Alerts/Mailings | Frühwarnung | Einfache Gut/Schlecht-Indikatoren |
| Overview/Hub | Aktueller Zustand auf einen Blick | KPI + Sparkline + Top-Listen |
| Entity Page | Detailansicht einer Entität | Abschnitte entsprechend dem Lebenszyklus |
| Analytical | Prüfung komplexer Hypothesen | Großes Hauptdiagramm + ergänzender Kontext |
| Self-Service | Nutzergesteuerte Exploration | Filter links, Ergebnisse rechts |

## Kennzahlen und KPIs {#key-metrics-and-kpis}

### Produktmetriken {#product-metrics}
- **DAU/MAU**: tägliche/monatliche aktive Nutzer
- **Retention-Rate**: Anteil der Nutzer, die nach N Tagen zurückkehren (D1, D7, D30)
- **Churn-Rate**: 1 - Retention
- **ARPU**: Umsatz / aktive Nutzer
- **LTV**: prognostizierter Gesamtumsatz eines Nutzers
- **CAC**: Marketingausgaben / Neukunden
- **LTV/CAC > 3** für ein gesundes Geschäftsmodell

### Conversion-Funnel {#conversion-funnel}
```sql
SELECT
    COUNT(DISTINCT CASE WHEN event = 'page_view' THEN user_id END) as views,
    COUNT(DISTINCT CASE WHEN event = 'add_to_cart' THEN user_id END) as carts,
    COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as purchases
FROM events WHERE date BETWEEN '2024-01-01' AND '2024-01-31';
```

### Kohortenanalyse {#cohort-analysis}
Nutzer nach Registrierungsdatum gruppieren und die Metrik pro Kohorte über die Zeit verfolgen.

```sql
WITH cohorts AS (
    SELECT user_id,
        DATE_TRUNC('month', first_visit) as cohort_month,
        DATE_TRUNC('month', visit_date) as activity_month
    FROM user_visits
)
SELECT cohort_month, activity_month,
    COUNT(DISTINCT user_id) as active_users
FROM cohorts GROUP BY 1, 2;
```

## SQL für Analytics {#sql-for-analytics}

```sql
-- Running total
SELECT date, revenue,
    SUM(revenue) OVER (ORDER BY date) as running_total
FROM daily_revenue;

-- Rolling 7-day average
SELECT date, revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    as rolling_7d_avg
FROM daily_revenue;

-- Month-over-month growth
SELECT month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as prev_month,
    (revenue - LAG(revenue) OVER (ORDER BY month))
    / LAG(revenue) OVER (ORDER BY month) * 100 as growth_pct
FROM monthly_revenue;
```

## Prozess für das Dashboard-Design {#dashboard-design-process}

### Canvas-Framework {#canvas-framework}
1. **Nutzer und Kontext**: wer, wann und wie das Dashboard verwendet wird
2. **Aufgabenverständnis**: welche Entscheidungen getroffen werden
3. **Fragen**: welche konkreten Fragen das Dashboard beantwortet
4. **Visualisierung**: welche Diagrammtypen zu welchen Fragen passen

### Wireframe-Prinzipien {#wireframe-principles}
- Die Blockgröße spiegelt die Bedeutung der Information wider
- Aufmerksamkeit lenken über: Position (oben links), Kontrast (Größe, Farbe), ungewöhnliche Form
- Alerts: gleichmäßig verteilte Elemente mit hervorgehobenen Abweichungen
- Analytische Werkzeuge: großes Analysediagramm + kleine Trenddiagramme

## BI-Tools {#bi-tools}

| Tool | Typ | Stärke |
|------|-----|--------|
| **Tableau** | Kommerziell | Industriestandard, Drag-and-drop |
| **Apache Superset** | Open Source | SQL-basiert, umfangreiche Diagramme |
| **Metabase** | Open Source | Einfaches "Question"-Paradigma |
| **Redash** | Open Source | SQL-first, für Datenteams |
| **DataLens** | Kostenlos (Yandex) | Nativ für ClickHouse |
| **Looker Studio** | Kostenlos (Google) | Integration mit BigQuery/GA |

**Wesentlicher Unterschied** zu matplotlib/seaborn: BI-Tools dienen der Präsentation für nicht-technische Stakeholder. Python-Plotting dient der Analyse.

## Datenpipeline für Dashboards {#data-pipeline-for-dashboards}

Quelle (OLTP) -> ETL/ELT -> Data Warehouse (OLAP) -> Semantische Schicht -> BI-Tool -> Nutzer

### DWH-Architektur {#dwh-architecture}
1. **Staging** (Rohdaten): Laden aus den Quellen in der ursprünglichen Qualität
2. **Core**: Konsolidierung, Normalisierung, Geschäftsregeln
3. **Presentation** (Data Marts): Star Schemas, geschäftsfertige Aggregate

## Stolperfallen {#gotchas}
- Ein Dashboard ohne definierte KPIs hat keinen Zweck. Mit den Geschäftszielen beginnen.
- Chaotische Berichtserstellung führt zu unbeherrschbarem Wildwuchs. Inhalte systematisieren.
- BI ist KEIN einmaliges Projekt. Es als Produkt mit Iterationen behandeln.
- Eine geringe Nutzerzahl in einem Segment macht Statistiken unzuverlässig. Immer das N anzeigen.

## Siehe auch {#see-also}
- [[data-visualization]] - Python-Plotting für Analysen
- [[hypothesis-testing]] - A/B-Tests auf Dashboard-Metriken
- [[ds-workflow]] - Dashboards im Projektlebenszyklus
- [[select-fundamentals]] - SQL für Analytics-Abfragen

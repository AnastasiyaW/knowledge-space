---
title: "Kohorten- & Retentionsanalyse"
category: concepts
tags: [bi-analytics, cohort-analysis, retention, ltv, product-analytics]
level: 3
source_sha256: b807ad7c5753e884efaa57a8809c43610cdc524f4072446b903620429922d98c
translation: machine
translated_at: '2026-10-24'
---
# Kohorten- & Retentionsanalyse {#cohort-retention-analysis}

Die Kohortenanalyse gruppiert Nutzer nach einem gemeinsamen Merkmal zu einem festen Zeitpunkt und verfolgt ihr Verhalten in den folgenden Zeiträumen. Sie ist die primäre Methode zur Messung von Retention, LTV und der Auswirkungen von Produktänderungen auf unterschiedliche Nutzergruppen.

## Wichtige Fakten {#key-facts}

- **Kohorte** = Gruppe von Nutzern, die innerhalb eines definierten Zeitfensters eine Aktion ausgeführt haben
- **Akquisitionskohorte**: gruppiert nach Installations- bzw. Registrierungswoche/-monat
- **Verhaltenskohorte**: Nutzer, die eine bestimmte Aktion abgeschlossen haben
- Die Kohortenanalyse vergleicht Zielmetriken über Kohorten hinweg im Zeitverlauf und berücksichtigt Saisonalität
- Typisches Muster: Gruppierung nach Datum des ersten Events, Verfolgung einer Metrik (Retention, Umsatz) für D1, D7, D14, D30
- Die Kohortenanalyse nach Akquisitionsquelle zeigt, welche Kanäle die Nutzer mit dem höchsten LTV liefern

## Muster {#patterns}

### Arten der Retentionsmessung {#retention-measurement-types}

**N-Tage-Retention**: Anteil der Nutzer aus der Installationskohorte, die genau an Tag N zurückkehren.

**Bracket-Retention**: Anteil der Nutzer, die in einem Tagesbereich zurückkehren (z. B. Tag 7–14).

**Return-on-Retention**: Anteil der Nutzer, die die App seit der Installation mindestens einmal genutzt haben und an Tag N noch aktiv sind.

### SQL-Abfrage für Kohorten-Retention {#sql-cohort-retention-query}

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', first_order_date) as cohort_month
    FROM users
),
activities AS (
    SELECT
        c.user_id,
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) as activity_month,
        DATEDIFF('month', c.cohort_month,
            DATE_TRUNC('month', o.order_date)) as period
    FROM cohorts c
    JOIN orders o ON c.user_id = o.user_id
)
SELECT
    cohort_month,
    period,
    COUNT(DISTINCT user_id) as users
FROM activities
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Kohortenanalyse in Tableau {#cohort-analysis-in-tableau}

Verwenden Sie `DATEDIFF`, um die Tage seit dem ersten Event zu berechnen, und `DATETRUNC`, um auf Wochen- bzw. Monatskohorten zu normalisieren. Anschließend wird mit Tabellenberechnungen das Kohortenraster aufgebaut.

```sql
-- First event date per user (LOD)
{FIXED [User ID] : MIN([Event Date])}

-- Cohort month
DATETRUNC('month', {FIXED [User ID] : MIN([Event Date])})

-- Period number
DATEDIFF('month',
    {FIXED [User ID] : MIN([Event Date])},
    [Event Date])
```

### Kohortenanalyse in AppsFlyer {#cohort-analysis-in-appsflyer}

- Installationen nach Datum gruppieren
- N-Tage-Retention und Umsatz pro Kohorte verfolgen
- Leistung über Kohorten/Quellen hinweg vergleichen
- D1/D7/D30-Retention zeigt die Qualität des Engagements
- D30-ROAS (Umsatz / Werbeausgaben) zeigt den finanziellen Ertrag

### Muster zur Nutzersegmentierung {#user-segmentation-patterns}

Segmente auf Basis von Event-Historie und Eigenschaften erstellen:
- „Nutzer, die das Onboarding abgeschlossen, aber innerhalb von 7 Tagen keinen ersten Kauf getätigt haben“
- „Nutzer, die Funktion X in den letzten 30 Tagen verwendet haben“
- Segmente für Push-Benachrichtigungen oder Anzeigen-Targeting exportieren

### Verhaltensanalyse (Amplitude Pathfinder) {#behavioral-analysis-amplitude-pathfinder}

- Zeigt die tatsächlichen Navigationspfade der Nutzer durch das Produkt
- Was tun Nutzer NACH Event X?
- Was haben Nutzer VOR Event Y getan (Abbruch)?
- Unerwartete Nutzungsmuster entdecken

## Stolperfallen {#gotchas}

- In AppMetrica wird der aktuelle, unvollständige Monat aus der Berechnung der Retention-% ausgeschlossen – filtern Sie nach Datumsbereich und summieren Sie Installationen nur aus abgeschlossenen Monaten
- Optimieren Sie nicht ausschließlich auf Installationen – ein hohes Volumen günstiger Installationen korreliert häufig mit niedrigem LTV
- Kohortengrößen schwanken naturgemäß; kleine Kohorten erzeugen verrauschte Retentionskurven, die nicht überinterpretiert werden sollten
- Beim Vergleich von Kohorten über die Zeit ist die Saisonalität zu berücksichtigen (Feiertagskohorten verhalten sich anders als reguläre)
- Retentionsmetriken sind in manchen Systemen nur auf Tagesebene gültig – prüfen Sie die Datengranularität, bevor Sie berechnen

## Siehe auch {#see-also}

- [[product-metrics-framework]] - DAU/MAU, Stickiness, Churn-Definitionen
- [[unit-economics]] - LTV- und Amortisationszeit-Berechnungen
- [[funnel-analysis]] - Optimierung des Funnels vor der Retention
- [[mobile-attribution-fraud]] - Kohortenqualität nach Akquisitionsquelle
- [[sql-for-analytics]] - Fensterfunktionen für Kohortenabfragen

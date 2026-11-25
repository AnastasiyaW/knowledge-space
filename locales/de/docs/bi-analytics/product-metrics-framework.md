---
title: "Produkt-Metriken-Framework"
category: concepts
tags: [bi-analytics, product-analytics, metrics, dau, mau, retention, stickiness]
level: 3
source_sha256: f657cf95c21da26aef4e751de3d3915555a2f0e257c941cf5adb2fed04ee78c9
translation: machine
translated_at: '2026-10-24'
---
# Produkt-Metriken-Framework {#product-metrics-framework}

Zentrale Produktmetriken, die Nutzerengagement, Retention und die Gesundheit des Produkts messen. Diese Metriken bilden die Grundlage für Produktanalytik bei Mobile-Apps, Web-Produkten und SaaS-Plattformen.

## Key Facts {#key-facts}

- **DAU** (Daily Active Users) - eindeutige Nutzer, die an einem Tag aktiv sind
- **WAU** (Weekly Active Users) - eindeutige Nutzer, die innerhalb von 7 Tagen aktiv sind
- **MAU** (Monthly Active Users) - eindeutige Nutzer, die innerhalb von 30 Tagen aktiv sind
- **Stickiness** = DAU/MAU - misst, wie stark sich das Produkt als Gewohnheit etabliert
- **Retention Rate** - Anteil der Nutzer, die am Tag N nach der ersten Nutzung zurückkehren
- **Churn Rate** = 1 - Retention - Anteil der Nutzer, die das Produkt nicht mehr verwenden
- "Aktiv" muss für jedes Produkt explizit definiert werden (ein Login? eine Transaktion? die Nutzung eines Features?)

## Patterns {#patterns}

### Stickiness-Benchmarks (DAU/MAU) {#stickiness-benchmarks-daumau}

```toml
Stickiness = DAU / MAU
```

| Bereich | Interpretation | Beispiele |
|-------|---------------|----------|
| 50%+ | Tägliche Nutzungsgewohnheit | Social Media, E-Mail |
| 25-50% | Mehrmals pro Woche | Produktivitäts-Apps |
| 10-25% | Wöchentliche Nutzung | Fitness-, Finanz-Apps |
| <10% | Seltene Nutzung | Reisebuchung, Immobilien |

Stickiness ist kontextabhängig - man sollte die Stickiness eines Messengers nicht mit der einer Hotelbuchungs-App vergleichen.

### Retention-Typen {#retention-types}

**N-Tage-Retention**: Anteil der Nutzer aus einer Install-Kohorte, die genau am Tag N zurückkehren.

**Bracket-Retention**: Anteil der Nutzer, die innerhalb eines Tagesbereichs zurückkehren (z. B. Tag 7-14).

**Return-on-Retention**: Anteil der Nutzer, die die App seit der Installation mindestens einmal genutzt haben und am Tag N noch aktiv sind.

So werden Retention-Kurven gelesen:
- Abflachende Kurve = Produkt hat einen Kernnutzen (Nutzer, die bleiben, bleiben langfristig)
- Kurve fällt auf 0 = kein Product-Market-Fit, alle Nutzer springen ab
- Höhere Werte bei D1 vs. D7 vs. D30 = frühes Engagement ist entscheidend

### Lebenszyklusphasen der Nutzer {#user-lifecycle-stages}

1. **Impression** - Nutzer sieht die Anzeige
2. **Click** - Nutzer klickt auf die Anzeige
3. **Install** - App wird heruntergeladen und installiert
4. **First Open** (Registrierung/Onboarding)
5. **Key Event** - Zielaktion (erster Kauf, Aktivierung)
6. **Retention** - wiederkehrende Nutzung
7. **Monetarisierung** - Kauf/Abonnement
8. **Churn** - Nutzer verwendet die App nicht mehr

### SQL-Muster für DAU/MAU-Stickiness {#daumau-stickiness-sql-pattern}

```sql
SELECT
    event_date,
    COUNT(DISTINCT user_id) as dau,
    COUNT(DISTINCT user_id) OVER (
        ORDER BY event_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as mau_rolling,
    ROUND(100.0 * COUNT(DISTINCT user_id) /
        COUNT(DISTINCT user_id) OVER (
            ORDER BY event_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ), 1) as stickiness
FROM events
GROUP BY event_date;
```

### Alarmstrategie {#alert-strategy}

Automatische Alarme einrichten für:
- Starke Einbrüche bei DAU (>15 % gegenüber dem gleitenden Durchschnitt)
- Funnel-Conversion unter dem Schwellenwert
- Umsatz pro Nutzer unter dem Zielwert

## Gotchas {#gotchas}

- DAU/MAU kann irreführend sein, wenn "aktiv" zu locker definiert ist (z. B. wenn passive Seitenaufrufe mitgezählt werden)
- Retention-Benchmarks unterscheiden sich stark nach Produktkategorie - immer innerhalb der eigenen Branche vergleichen
- Stickiness kann künstlich aufgebläht werden durch Push-Benachrichtigungen, die Öffnungen ohne echtes Engagement erzeugen
- Churn Rate = 1 - Retention ist nur gültig, wenn beide dasselbe Zeitfenster und dieselbe Definition von "aktiv" verwenden

## See Also {#see-also}

- [[product-analytics-fundamentals]] - Rolle der Analysten und Metrik-Pyramide
- [[cohort-retention-analysis]] - kohortenbasierte Retention-Analyse
- [[unit-economics]] - LTV und Kundenprofitabilität
- [[mobile-analytics-platforms]] - Tools zur Messung dieser Metriken

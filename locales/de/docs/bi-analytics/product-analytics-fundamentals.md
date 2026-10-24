---
title: "Grundlagen der Produktanalytik"
category: concepts
tags: [bi-analytics, product-analytics, metrics, analyst-role]
level: 1
source_sha256: 2e899eef468aaac0730639c5f683b3fc078a3178f23a2311ab6428547de6916b
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen der Produktanalytik {#product-analytics-fundamentals}

Produktanalytik ist die Disziplin, das Nutzerverhalten innerhalb eines Produkts zu messen und zu verstehen, um geschäftliche Entscheidungen zu unterstützen. Sie verbindet analytisches Denken mit Datenmessung – SQL oder Tableau zu beherrschen ist notwendig, aber nicht ausreichend; die Kernkompetenz besteht darin zu verstehen, was gemessen werden sollte und warum.

## Kernfakten {#key-facts}

- Produktanalytik beantwortet die Fragen: Welches Problem lösen wir, wer ist die Zielgruppe, wie lösen wir das Problem, was wollen wir erreichen und wie verdienen wir Geld
- Ein Produktanalyst definiert Kennzahlen, sammelt Daten, analysiert sie, führt Experimente (A/B-Tests) durch und setzt die Erkenntnisse um
- Der Fünf-Schritte-Zyklus des Analysten: Metriken definieren -> Daten erheben -> Analysieren -> Experimentieren -> Umsetzen
- Analytik sollte bereits in den frühen Designphasen einbezogen werden und nicht erst nach dem Launch hinzukommen
- Empfehlungen müssen auf Zahlen basieren, nicht auf Gefühlen
- Die Definition von „aktivem Nutzer“ variiert je nach Produkt und muss für jeden Kontext explizit festgelegt werden

## Muster {#patterns}

### Metrik-Pyramide {#metrics-pyramid}

Ein Werkzeug zur Visualisierung von Prozessen und zum Auffinden von KPIs. Aufbau: das geschäftliche ZIEL an der Spitze, primäre Metriken auf Ebene 1, Zerlegung bzw. sekundäre Metriken auf Ebene 2.

Häufige Fehler bei der Auswahl von KPIs:
- Wahl eines einzelnen Indikators (erzeugt blinde Flecken)
- Wahl zu vieler Indikatoren (Analyse-Paralyse)

Die Aufgabenformulierung muss spezifisch sein: nicht „Seitenbesuche analysieren“, sondern „Den Einfluss der Monitorauflösung auf die Conversion Rate untersuchen und Empfehlungen ableiten.“

### Vanity- vs. Actionable-Metriken {#vanity-vs-actionable-metrics}

**Vanity-Metriken** sehen gut aus, leiten aber keine Entscheidungen an:
- Gesamtzahl registrierter Nutzer (inklusive inaktiver)
- Seitenaufrufe (ohne Kontext)
- Downloads (ohne Hinweis auf Nutzung)

**Actionable-Metriken** sind direkt mit geschäftlichen Entscheidungen verknüpft:
- DAU/MAU mit präziser Definition von „aktiv“
- Funnel-Conversion-Raten (schrittweise)
- Retention-Kurven (D1/D7/D30)
- Feature-Adoption-Rate
- Umsatz pro Kohorte

### North-Star-Metrik {#north-star-metric}

Eine einzelne Metrik, die den gelieferten Nutzen am besten erfasst. Alles wird an seiner Wirkung auf diese Metrik gemessen. Beispiel: Spotify = „Hörzeit pro Nutzer“.

**Input-Metriken** (Größen, die Teams steuern können) beeinflussen **Output-Metriken** (geschäftliche Ergebnisse):
- Input: Feature-Adoption-Rate → Output: Retention
- Input: Onboarding-Abschlussrate → Output: D7-Retention
- Input: Erfolgsquote der Suche → Output: Conversion zum Kauf

## Stolperfallen {#gotchas}

- Produktunternehmen-Variablen, die das Analytics-Setup beeinflussen: Unternehmensgröße und Phase, B2B vs. B2C, Teamstruktur, Methodik (Scrum/Agile), Tooling und Reifegrad der analytischen Kultur
- Marketing-Analytik und Produktanalytik beantworten unterschiedliche Fragen – Marketing konzentriert sich auf Kanaleffektivität und Budgetallokation, Produktanalytik auf Nutzerverhalten und Feature-Performance
- Die Metrik-Pyramide sollte mit der Weiterentwicklung des Produkts neu bewertet werden – Metriken, die für ein Startup passen, unterscheiden sich von denen für ein ausgereiftes Produkt

## Siehe auch {#see-also}

- [[product-metrics-framework]] - DAU/MAU, Stickiness, Retention-Definitionen
- [[funnel-analysis]] - Conversion-Funnel-Konzepte und Optimierung
- [[unit-economics]] - Berechnungen der Profitabilität pro Nutzer
- [[bi-development-process]] - Anforderungserhebung und Dashboard-Workflow

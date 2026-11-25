---
title: "Data Vault 2.0"
category: concepts
tags: [data-engineering, data-vault, data-modeling, dwh, scd2]
level: 3
source_sha256: e29b457acb016e4270303529de477eb3cf5d96a9447ee8ef06dbf3d7b78ef0d8
translation: machine
translated_at: '2026-10-24'
---
# Data Vault 2.0 {#data-vault-20}

Data Vault ist eine Datenmodellierungsmethodik für agile DWH-Umgebungen mit vielen Quellen, häufigen Schemaänderungen und Auditanforderungen. Sie löst die Starrheit der 3NF sowie die Redundanzprobleme der dimensionalen Modellierung.

## Kerntabellentypen {#core-table-types}

| Tabelle | Zweck | Schlüsselfelder |
|---------|-------|-----------------|
| **Hub** | Geschäftsentitäten (Kunde, Produkt) | Hash-Schlüssel, Geschäftsschlüssel, Ladezeitstempel, Quellcode |
| **Link** | Beziehungen/Transaktionen zwischen 2+ Hubs | Hash-Schlüssel, Hub-Fremdschlüssel, Ladezeitstempel, Quelle |
| **Satellite** | Beschreibende Attribute mit SCD2-Historie | Hub-/Link-Hash-Schlüssel, Attribute, valid_from, valid_to, Quelle |

## Grundprinzipien {#key-principles}
- Daten werden unverändert aus den Quellen übernommen (keine fachliche Transformation im Core)
- Geschäftsregeln werden nur in der Mart-Schicht angewendet
- Alle Tabellen sind **append-only** – die Historie wird über SCD2 in den Satellites erfasst
- **Hash-Schlüssel** für Joins (deterministisch, keine Sequenzen)
- Trennung von Struktur (Hubs/Links) und Inhalt (Satellites)

## Vorteile {#advantages}
- Einfaches Hinzufügen neuer Quellen (es genügen neue Satellites)
- Vollständige Auditierbarkeit (jede Änderung wird mit Zeitstempeln und Quellcodes nachverfolgt)
- Parallelisierbares Laden (Hubs, Links und Satellites werden unabhängig geladen)
- Unterstützt viele Quellen mit unterschiedlichen Schemata
- Robust gegenüber Änderungen in den Quellen

## Nachteile {#disadvantages}
- Aufwendig für direkte Abfragen (Joins über Hub, Satellite und Link nötig)
- Speist typischerweise dimensionale Marts für die BI-Nutzung
- SCD2-Joins über Satellites mit unterschiedlichen Änderungsfrequenzen = erhöhte Komplexität

## SCD2 (Slowly Changing Dimension Typ 2) {#scd2-slowly-changing-dimension-type-2}

Historische Änderungen werden erfasst, indem neue Zeilen mit Gültigkeitsdaten angelegt werden:

```sql
customer_id | name    | valid_from | valid_to   | is_current
1           | Alice   | 2023-01-01 | 2023-06-15 | false
1           | Alice B | 2023-06-15 | 9999-12-31 | true
```

Beim Join von Satellites aus unterschiedlichen Hubs/Links müssen sich die Datumsbereiche überlappen – andernfalls kann eine kartesische Explosion entstehen.

## Anchor Modeling {#anchor-modeling}

Eine extreme Form von Data Vault, bei der jedes Attribut eine eigene Tabelle erhält (ähnlich 6NF):

| Komponente | Vergleichbar mit | Beschreibung |
|------------|------------------|--------------|
| **Anchor** | Hub | Entität, identifiziert durch eine Surrogat-ID |
| **Attribute** | Satellite | Ein einzelnes Attribut pro Tabelle, mit Zeitstempel |
| **Tie** | Link | Beziehung zwischen Anchors |
| **Knot** | Referenz | Gemeinsam genutzte Referenzdaten (Enums, Lookups) |

### Wesentliche Unterschiede zu Data Vault {#key-differences-from-data-vault}
- Feinere Granularität: ein Attribut = eine Tabelle (statt Satellites, die Attribute gruppieren)
- Einfachere Schemaevolution (Attribut hinzufügen = Tabelle hinzufügen, kein ALTER)
- Führt zu vielen Tabellen und vielen JOINs
- Besser geeignet für Umgebungen mit häufigen Schemaänderungen

## Auswahl einer Methodik {#choosing-a-methodology}

| Methodik | Geeignet für | Kompromiss |
|----------|--------------|------------|
| **3NF (Inmon)** | Kernschicht eines unternehmensweiten DWH | Aufwendig abzufragen, gut für die Integration |
| **Dimensional (Kimball)** | Marts, BI, schnelle Abfragen | Denormalisiert, schwerer zu pflegen |
| **Data Vault** | Agiles DWH, mehrere Quellen, Audit | Aufwendig abzufragen, benötigt Marts darüber |
| **Anchor** | Häufig wechselnde Schemata | Sehr viele Tabellen, viele JOINs |

## Stolperfallen {#gotchas}
- Data Vault erzeugt viele Joins – die Mart-Schicht muss vorab joinen, um akzeptable Performance zu erreichen
- SCD2-Datumsbereichs-Joins über verschiedene Satellites können unerwartete kartesische Produkte erzeugen
- Hash-Schlüssel müssen in allen Ladeprozessen konsistent gehasht werden
- Ohne geeignete Mart-Schicht können Analysten Data Vault nicht direkt abfragen

## Siehe auch {#see-also}
- [[data-modeling]] - Grundlagen der Normalisierung
- [[dimensional-modeling]] - Stern- und Schneeflocken-Schemata für Marts
- [[scd-patterns]] - Techniken für langsam ändernde Dimensionen
- [[dwh-architecture]] - architektonischer Kontext

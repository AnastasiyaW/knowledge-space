---
title: "Dimensionsmodellierung (Kimball)"
category: concepts
tags: [data-engineering, dimensional-modeling, star-schema, snowflake-schema, kimball]
level: 3
source_sha256: 58505c92a668c7c0131abfc51e5170b5de9860cce5fd682e8e630e2fe9277f65
translation: machine
translated_at: '2026-10-24'
---
# Dimensionsmodellierung (Kimball) {#dimensional-modeling-kimball}

Die Dimensionsmodellierung organisiert Daten in Faktentabellen (Kennzahlen/Ereignisse), die von Dimensionstabellen (beschreibender Kontext) umgeben sind. Sie ist der Standardansatz für Data Marts und BI-optimierte analytische Schichten.

## Star Schema {#star-schema}

```text
         dim_date
            |
dim_product--fact_sales--dim_customer
            |
         dim_store
```

- **Faktentabelle:** Fremdschlüssel zu den Dimensionen + Kennzahlen (Betrag, Menge, Dauer)
- **Dimensionstabellen:** Beschreibende Attribute (Name, Kategorie, Adresse) - denormalisiert für Abfrageleistung

## Snowflake Schema {#snowflake-schema}

Dimensionen sind normalisiert (in Unter-Tabellen aufgeteilt). Dies reduziert den Speicherbedarf, erfordert aber mehr JOINs. In der Praxis aufgrund der Abfragekomplexität seltener verwendet.

## Zentrale Konzepte {#key-concepts}

| Konzept | Beschreibung |
|---------|-------------|
| **Surrogatschlüssel** | Systemgenerierte Integer-Primärschlüssel in Dimensionen (keine Geschäftsschlüssel) |
| **Degenerierte Dimension** | Dimensionswert, der direkt in der Faktentabelle gespeichert wird (z. B. Rechnungsnummer) |
| **Junk Dimension** | Gruppiert Flags/Indikatoren mit niedriger Kardinalität in einer einzigen Dimension |
| **Konforme Dimension** | Wird über mehrere Faktentabellen/Data Marts hinweg für Konsistenz geteilt |

## Entwurfsprozess {#design-process}

1. Den zu modellierenden Geschäftsprozess auswählen
2. Die Granularität festlegen (was repräsentiert eine Zeile?)
3. Die Dimensionen identifizieren (wer, was, wann, wo)
4. Die Fakten identifizieren (Kennzahlen - additiv, semi-additiv, nicht-additiv)

## Muster {#patterns}

### Star Schema DDL {#star-schema-ddl}

```sql
CREATE TABLE dim_customer (
    customer_sk SERIAL PRIMARY KEY,  -- surrogate key
    customer_bk VARCHAR(50),          -- business key
    name VARCHAR(200),
    segment VARCHAR(50),
    valid_from DATE,
    valid_to DATE DEFAULT '9999-12-31'
);

CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_sk INT REFERENCES dim_date(date_sk),
    customer_sk INT REFERENCES dim_customer(customer_sk),
    product_sk INT REFERENCES dim_product(product_sk),
    quantity INT,
    amount NUMERIC(12,2)
);
```

## Stolpersteine {#gotchas}
- Die Denormalisierung im Star Schema tauscht Speicherplatz gegen Abfrageleistung - für OLAP akzeptabel
- Ohne konforme Dimensionen kann jeder Data Mart Kennzahlen unterschiedlich definieren
- Surrogatschlüssel entkoppeln das DWH von Änderungen der Schlüssel im Quellsystem
- Die Granularität immer zuerst definieren - eine unklare Granularität führt zu falschen Aggregationen

## Siehe auch {#see-also}
- [[data-modeling]] - Normalisierungstheorie
- [[data-vault]] - Alternative für die zentrale DWH-Schicht
- [[scd-patterns]] - Umgang mit Dimensionsänderungen
- [[dwh-architecture]] - Kimball- vs. Inmon-Ansätze

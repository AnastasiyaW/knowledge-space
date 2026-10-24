---
title: "Slowly Changing Dimensions (SCD)"
category: concepts
tags: [data-engineering, scd, dimensions, data-modeling, history-tracking]
level: 3
source_sha256: 95dface110853d902f79a6e646703e13815d3b1e1477529eb91656b42eff4a15
translation: machine
translated_at: '2026-10-24'
---
# Slowly Changing Dimensions (SCD) {#slowly-changing-dimensions-scd}

SCD-Muster behandeln Änderungen von Dimensionsattributen über die Zeit. SCD2 ist der in Data Warehouses am häufigsten eingesetzte Typ; er erhält die vollständige Historie, indem er neue Zeilen mit Gültigkeitsdaten anlegt.

## SCD-Typen {#scd-types}

| Typ | Verhalten | Historie | Anwendungsfall |
|------|----------|---------|----------|
| **SCD0** | Ändert sich nie | Keine | Statische Referenzdaten |
| **SCD1** | Alter Wert wird überschrieben | Verloren | Korrekturen, nicht-historische Attribute |
| **SCD2** | Neue Zeile mit Datumsangaben anlegen | Vollständig | Die meisten Dimensionsänderungen |
| **SCD3** | Spalte für den vorherigen Wert anlegen | Eingeschränkt (1 Vorgänger) | Selten verwendet |
| **SCD6** | Hybrid (1 + 2 + 3) | Vollständig + Current-Flag | Schneller Zugriff auf den aktuellen Wert |

## SCD2-Muster {#scd2-pattern}

```sql
-- SCD2 table structure
customer_id | name    | city      | valid_from | valid_to   | is_current
1           | Alice   | New York  | 2023-01-01 | 2023-06-15 | false
1           | Alice   | Boston    | 2023-06-15 | 9999-12-31 | true
```

### SCD2-Merge-Logik {#scd2-merge-logic}

```sql
-- Step 1: Close existing records
UPDATE dim_customer
SET valid_to = CURRENT_DATE, is_current = false
WHERE customer_bk = 'C001' AND is_current = true
  AND (name != 'New Name' OR city != 'New City');

-- Step 2: Insert new version
INSERT INTO dim_customer (customer_bk, name, city, valid_from, valid_to, is_current)
SELECT 'C001', 'New Name', 'New City', CURRENT_DATE, '9999-12-31', true
WHERE EXISTS (
    SELECT 1 FROM staging WHERE customer_bk = 'C001'
      AND (name != 'New Name' OR city != 'New City')
);
```

### Point-in-Time-Abfrage {#point-in-time-query}

```sql
-- What was the customer's city on 2023-03-15?
SELECT * FROM dim_customer
WHERE customer_bk = 'C001'
  AND '2023-03-15' BETWEEN valid_from AND valid_to;
```

## Stolpersteine {#gotchas}
- SCD2-Joins über Satelliten mit unterschiedlicher Änderungsfrequenz erzeugen bei überlappenden Datumsbereichen eine kartesische Explosion
- Die Konvention `valid_to = '9999-12-31'` markiert aktuelle Datensätze – für den neuesten Stand immer nach `is_current = true` filtern
- Hash-Schlüssel in SCD2 innerhalb von Data Vault müssen über alle ETL-Prozesse hinweg konsistent berechnet werden
- SCD2-Tabellen wachsen kontinuierlich – Speicherbedarf und Abfrageleistung einplanen

## Siehe auch {#see-also}
- [[data-vault]] - SCD2 in Satellitentabellen
- [[dimensional-modeling]] - Entwurfsmuster für Dimensionen
- [[data-modeling]] - Kontext zur Normalisierung

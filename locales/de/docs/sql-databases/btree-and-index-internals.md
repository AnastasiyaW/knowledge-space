---
title: "B-Tree und Index-Interna"
category: concepts
tags: [sql-databases, btree, b-plus-tree, index, page-split, uuid, clustered-index, bloom-filter]
level: 4
source_sha256: ee9ffe01fa8a2ac979a8d55764686a31b5232f4b8eab8ab3bbdd5558d6759f20
translation: machine
translated_at: '2026-10-24'
---
# B-Tree und Index-Interna {#b-tree-and-index-internals}

B+-Bäume bilden das Rückgrat der Datenbankindizierung in allen gängigen RDBMS. Das Verständnis ihrer Struktur erklärt, warum manche Abfragen schnell sind und andere nicht, und warum die Wahl des Primärschlüssels enorm wichtig ist.

## B-Tree vs. B+Tree {#b-tree-vs-btree}

**B-Tree:** Innere Knoten speichern sowohl Schlüssel ALS AUCH Werte (Datenzeiger). Daten können auf jeder Ebene gefunden werden.

**B+Tree (verwendet von allen gängigen RDBMS):** Nur Blattknoten speichern Werte. Innere Knoten enthalten nur Schlüssel zur Navigation. Blattknoten sind als doppelt verkettete Liste verknüpft.

**Vorteile des B+Trees:**
- Mehr Schlüssel pro innerem Knoten (keine Daten) = flacherer Baum = weniger I/Os
- Bereichsabfragen: Der verketteten Liste der Blattknoten folgen (sequentielle I/O)
- Vorhersagbare I/O-Kosten: Alle Daten liegen auf derselben Tiefe
- Bessere Cache-Auslastung: Kleine innere Knoten werden eher im Cache gehalten

**Quantifiziert:** Eine 8-KB-Seite mit 100-Byte-Schlüsseln ergibt etwa 80 Schlüssel pro innerem Knoten. Ein B+Tree mit 3 Ebenen erreicht 80^3 = 512.000 Blattseiten mit 3 I/Os.

## Clustered vs. Non-Clustered Indexes {#clustered-vs-non-clustered-indexes}

**MySQL InnoDB:** Der Primärschlüssel IST der clustered Index. Die Daten sind physisch nach PK sortiert. Sekundärindizes speichern den PK-Wert als Zeilenzeiger – das erfordert einen doppelten Zugriff (Sekundärindex -> PK finden -> clustered Index -> Zeile).

**PostgreSQL:** Standardmäßig keine clustered Indizes. Alle Indizes zeigen direkt auf `ctid` (Seite, Offset) im Heap. Jede Verschiebung eines Tupels (UPDATE, VACUUM) macht die ctid ungültig und erfordert eine Aktualisierung des Indexes.

**SQL Server:** Ein clustered Index pro Tabelle (standardmäßig der PK). Der Blattknoten eines nicht gruppierten Indexes enthält die RID für Heaps oder den clustered Schlüssel für clustered Tabellen.

## Page Splits {#page-splits}

Wird in eine volle Blattseite eingefügt, findet ein Page Split statt: Die Seite wird geteilt, Einträge werden neu verteilt und die übergeordneten Knoten aktualisiert. Es ist die teuerste Index-Operation.

**Sequentielle Einfügungen** (Auto-Increment, UUID v7/ULID): Landen immer im äußersten rechten Blatt. Minimale Splits, sequentielle I/O, exzellente Cache-Trefferquote.

**Zufällige Einfügungen** (UUID v4): Jede Einfügung zielt auf eine zufällige Blattseite. Häufige Splits, zufällige I/O, Thrashing des Buffer Pools.

## UUID v4 vs. geordnete IDs {#uuid-v4-vs-ordered-ids}

Zufällige UUIDs verursachen:
- Häufige Page Splits (Einträge werden selten am Ende angehängt)
- Zufällige I/O-Muster (Seiten von überall auf der Festplatte)
- Thrashing des Buffer Pools (Seiten werden verdrängt und kurz darauf erneut benötigt)
- Schlechte Cache-Auslastung

**Shopify-Fallstudie:** Umstellung von UUID v4 auf ULID. Kaufbezogene Abfragen sind natürlicherweise zeitlich geordnet, daher verbesserten sich sowohl Lese- als auch Schreibzugriffe.

**MySQL-Vorbehalt:** ALLE Sekundärindizes speichern den PK. Ein zufälliger UUID-PK verteilt die Zufälligkeit auf jeden Sekundärindex.

**Wann Zufälligkeit nicht schadet:** PostgreSQL-Heap-Tabellen ohne clustered Indizes – zufällige Werte werden einfach am Ende des Heaps angehängt. Das Problem liegt in der Index-Pflege.

## Bloom-Filter {#bloom-filters}

Probabilistische Datenstruktur: „möglicherweise vorhanden“ oder „sicher nicht vorhanden“. Keine falsch-negativen Ergebnisse, falsch-positive sind möglich.

```php
Hash(value) % array_size = bit position
Bit = 0 -> definitely absent
Bit = 1 -> might exist (could be collision)
```

Anwendungsfall: Verfügbarkeit eines Benutzernamens prüfen, ohne eine DB-Abfrage auszuführen. Falsch-positive Ergebnisse verursachen unnötige Lookups, aber keine Korrektheitsprobleme. Mehrere Hash-Funktionen senken die Rate falsch-positiver Ergebnisse.

## Wichtige Fakten {#key-facts}

- B+Tree-Fanout: 8-KB-Seite / Schlüsselgröße = Schlüssel pro Knoten. Höherer Fanout = flacherer Baum
- PostgreSQL 13+ hat B-Tree-Deduplizierung eingeführt (mehrere doppelte Schlüssel in einem Blatt)
- Fill Factor < 100 % reserviert Platz für künftige Einfügungen und reduziert Splits
- `REINDEX CONCURRENTLY` baut den Index neu auf, ohne Schreibvorgänge zu blockieren
- Index-Fragmentierung durch Page Splits verschlechtert die Performance – zur Behebung REBUILD oder REORGANIZE ausführen

## Stolperfallen {#gotchas}

- Kleine Tabellen (< 1 Seite): Index-Scan langsamer als sequentieller Scan (Overhead des Optimierers)
- Funktionen auf indizierten Spalten deaktivieren die Indexnutzung: `WHERE YEAR(col) = 2024` kann keinen Index auf `col` verwenden
- UUID v4 als InnoDB-PK: Schlechtester Fall sowohl für den clustered als auch für alle Sekundärindizes
- PostgreSQL Weak-Lock-Fast-Path: 16 Slots pro Backend – stark partitionierte Tabellen können diesen Wert überschreiten

## Siehe auch {#see-also}

- [[index-strategies]] - zusammengesetzte, abdeckende, partielle Indizes
- [[database-storage-internals]] - Seiten, Heaps, I/O
- [[schema-design-normalization]] - Wahl der Primärschlüsselstrategie
- [[query-optimization-explain]] - wie der Optimierer zwischen Indextypen wählt

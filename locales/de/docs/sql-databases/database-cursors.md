---
title: "Datenbank-Cursor"
category: concepts
tags: [sql-databases, cursor, server-side-cursor, client-side-cursor, batch-processing, postgresql, psycopg2]
level: 3
source_sha256: 9e3e69fd89c79c4f0066f19c6ccbaeec6a01ca759ad6f600dfe2274f9776f8c2
translation: machine
translated_at: '2026-10-24'
---
# Datenbank-Cursor {#database-cursors}

Ein Cursor ist ein Zeiger auf eine Ergebnismenge, der eine zeilenweise oder stapelweise Verarbeitung ermöglicht, anstatt alle Ergebnisse auf einmal abzurufen. Die Wahl zwischen clientseitigen und serverseitigen Cursorn hat erhebliche Auswirkungen auf die Performance.

## Clientseitige Cursor (Standard) {#client-side-cursors-default}

Die Datenbank führt die Abfrage aus und überträgt ALLE Ergebnisse an den Client. Der Client hält die Ergebnismenge im Speicher und iteriert lokal darüber.

```python
# Default psycopg2 cursor (client-side)
cur = conn.cursor()
cur.execute("SELECT * FROM large_table")
rows = cur.fetchall()  # ALL rows loaded into Python memory
```

**Vorteile:** Gibt Serverressourcen nach der Übertragung frei, schnelle lokale Iteration.
**Nachteile:** Hohe Netzwerkbandbreite (gesamte Ergebnismenge), Speicherdruck auf dem Client, langsame initiale Ausführung.

## Serverseitige Cursor {#server-side-cursors}

Die Datenbank hält die Ergebnisse auf dem Server. Der Client ruft sie in kleinen Stapeln über FETCH-Anfragen ab.

```python
# psycopg2 named cursor (server-side)
cur = conn.cursor(name='server_cursor')
cur.execute("SELECT * FROM large_table")
batch = cur.fetchmany(1000)  # fetch 1000 rows at a time
```

```sql
-- SQL-level cursor
DECLARE my_cursor CURSOR FOR SELECT * FROM large_table;
FETCH 100 FROM my_cursor;
CLOSE my_cursor;
```

**Vorteile:** ~3 ms initiale Ausführung, minimaler Speicherbedarf auf dem Client, geringe Netzwerklast pro Stapel.
**Nachteile:** Jeder FETCH = Netzwerk-Roundtrip, der Server hält den Zustand im Speicher, Risiko von Cursor-Lecks.

## Wann welcher Cursor? {#when-to-use-which}

| Szenario | Empfehlung |
|----------|---------------|
| Kleine Ergebnismenge, alle Daten benötigt | Clientseitig |
| Große Ergebnismenge, nur Teilmenge benötigt | Serverseitig |
| Streaming-/Pipeline-Verarbeitung | Serverseitig |
| Einfache CRUD-Operationen | Clientseitig (Standard) |

## Wichtige Fakten {#key-facts}

- Serverseitige Cursor halten Serverressourcen belegt, bis sie explizit geschlossen werden
- Cursor immer explizit schließen bzw. deallokieren, um Lecks zu vermeiden
- Cursor vermeiden, wenn mengenbasierte Operationen möglich sind (UPDATE...SET, INSERT...SELECT)
- Im Transaktionsmodus von PgBouncer müssen serverseitige Cursor innerhalb derselben Transaktion geöffnet und geschlossen werden
- Serverseitige Cursor in PostgreSQL erfordern eine aktive Transaktion (BEGIN/COMMIT)

## Stolperfallen {#gotchas}

- Cursor-Lecks bei vielen gleichzeitigen Clients können den Serverspeicher erschöpfen
- Connection Pooling erschwert serverseitige Cursor, da der Cursor-Zustand an die Verbindung gebunden ist
- Mengenbasierte Operationen (JOINs, UPDATEs) sind fast immer schneller als zeilenweise Verarbeitung mit Cursorn
- Benannte Cursor in psycopg2 erzeugen automatisch serverseitige Cursor, wobei `itersize` die Stapelgröße steuert

## Siehe auch {#see-also}

- [[connection-pooling]] - Cursor-Verhalten mit gepoolten Verbindungen
- [[query-optimization-explain]] - mengenbasierte Operationen gegenüber Cursorn bevorzugen
- [[select-fundamentals]] - LIMIT/OFFSET als Alternative zu Cursorn

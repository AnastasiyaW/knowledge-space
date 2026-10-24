---
title: "Kafka-Fehlerbehebung"
category: gotchas
tags: [kafka, troubleshooting, errors, leader-not-available, rebalancing, data-loss, duplicates]
level: 3
source_sha256: 2d6c9aa3f68fdf81ea4bed734da99e1c72d62dc16e6c4304799620bd4b851696
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Fehlerbehebung {#kafka-troubleshooting}

Häufige Kafka-Probleme, zugeordnet zu Symptomen, Ursachen und Lösungen, sowohl für producer- als auch für consumer-seitige Probleme.

## Key Facts {#key-facts}

- Die meisten Kafka-Probleme fallen in folgende Kategorien: Verzögerungen bei der Leader-Wahl, Rebalancing-Stürme, Fehler bei der Offset-Verwaltung, Serialisierungsfehler oder erschöpfter Festplattenspeicher
- „Leader Not Available" ist der häufigste Kafka-Fehler und löst sich meist innerhalb von Sekunden von selbst
- Auto-Commit ist die Nummer-eins-Ursache für Datenverlust bei Einsteigern
- Erschöpfter Festplattenspeicher ist die Nummer-eins-Ursache für Ausfälle im Betrieb
- Serialisierungsfehler kaskadieren, wenn sich Schemata ohne Abstimmung mit den Consumern ändern

## Patterns {#patterns}

### Producer-Probleme {#producer-problems}

**Leader Not Available**
- Symptom: `LEADER_NOT_AVAILABLE`-Fehler beim Produzieren
- Ursachen: Leader ist ausgefallen (Wahl läuft), Cluster unter hoher Last, neues Topic wird angelegt
- Lösung: löst sich meist innerhalb von Sekunden von selbst; hält der Fehler länger als 2 Minuten an, an den Betrieb eskalieren
- Schutz: `retries` mit `retry.backoff.ms` erhöhen; das [[transactional-outbox]]-Muster implementieren

**ACK verloren (Duplikate)**
- Symptom: dieselbe Nachricht erscheint zweimal im Topic
- Ursache: Broker speichert die Nachricht, das ACK-Paket geht im Netzwerk verloren, Producer sendet erneut
- Lösung: [[idempotent-producer]] aktivieren (`enable.idempotence=true`); für sitzungsübergreifende Fälle: [[kafka-transactions]] verwenden

**Batch bei Producer-Absturz verloren**
- Symptom: Nachrichten verschwinden stillschweigend
- Ursache: Batches in Übertragung existieren nur im Speicher des Producers; ein Absturz vor dem Senden führt zu dauerhaftem Verlust
- Lösung: bei kritischen Daten Write-Ahead-Logging implementieren (vor dem Senden an Kafka zuerst in eine lokale Datenbank schreiben)

**Nachricht zu groß**
- Symptom: `MSG_SIZE_TOO_LARGE`-Fehler
- Ursache: Der Standardwert von `message.max.bytes` auf dem Broker beträgt 1 MB
- Lösung: sowohl die Broker-Konfiguration (`message.max.bytes`) als auch die Topic-Konfiguration (`max.message.bytes`) erhöhen

### Consumer-Probleme {#consumer-problems}

**Rebalancing-Sturm**
- Symptom: Consumer hören wiederholt auf zu lesen und starten neu; der Consumer-Lag wächst
- Ursachen: Verarbeitung dauert länger als `session.timeout.ms`, langsamer Anwendungsstart, häufige Deployments, instabiles Netzwerk
- Lösung: `session.timeout.ms` und `max.poll.interval.ms` erhöhen; `max.poll.records` reduzieren; CooperativeStickyAssignor verwenden

**Datenverlust durch Auto-Commit**
- Symptom: Nachrichten gehen ohne Fehlermeldung verloren
- Ursache: Auto-Commit wird ausgelöst, bevor die Verarbeitung abgeschlossen ist; der Consumer stürzt während der Verarbeitung ab
- Lösung: `enable.auto.commit=false` setzen; nach erfolgreicher Verarbeitung manuell committen

**Offset-Ablauf**
- Symptom: Consumer liest nach einer Ausfallzeit alles erneut (oder springt zum neuesten Stand)
- Ursache: Inaktiv länger als `offsets.retention.minutes` (Standard 7 Tage); Kafka löscht die gespeicherten Offsets
- Lösung: `auto.offset.reset` passend setzen; eine externe Speicherung der Offsets in Betracht ziehen

**Serialisierungsfehler**
- Symptom: Consumer stürzt beim Deserialisieren ab; `SerializationException`
- Ursache: Schema wurde geändert (Feld hinzugefügt/entfernt), ohne die Consumer abzustimmen
- Lösung: Dead Letter Queue für nicht lesbare Nachrichten implementieren; [[schema-registry]] mit Kompatibilitätsmodi verwenden

**Lücke durch Datenbank-Wiederherstellung**
- Symptom: Dateninkonsistenz nach der Wiederherstellung der Datenbank aus einem Backup
- Ursache: Der Consumer-Offset in Kafka zeigt auf die aktuelle Position; Daten aus der Lücke wurden bereits über diesen Punkt hinaus committet
- Lösung: Offset der Consumer-Gruppe per CLI zurücksetzen; neuen Namen für die Consumer-Gruppe verwenden; oder Offsets in der Anwendungsdatenbank speichern

### Cluster-Probleme {#cluster-problems}

**Erschöpfter Festplattenspeicher**
- Symptom: Broker kann nicht schreiben und stürzt ab
- Ursache: Retention konfiguriert, aber Segmente bleiben länger offen als erwartet; das Vorstellen der Systemzeit erzeugt Zeitstempel in der Zukunft, die das Löschen verhindern
- Lösung: Festplattennutzung überwachen (Alarm bei 80 %); `log.segment.bytes` und `log.roll.hours` anpassen, damit Segmente schneller geschlossen werden
- **Häufigste Ursache für einen Kafka-Absturz**: Systemzeit während Tests vorstellen; Nachrichten mit Zeitstempeln in der Zukunft verhindern das Löschen jedes Segments

**ISR-Schrumpfung**
- Symptom: `UnderReplicatedPartitions > 0`; `IsrShrinksPerSec` steigt sprunghaft an
- Ursache: langsame Festplatte, Netzwerkprobleme, GC-Pausen, überlasteter Broker
- Lösung: Festplatten-I/O, Netzwerk und JVM-GC-Logs prüfen; als manuelle Abschwächung `acks` vorübergehend von `all` auf `1` umstellen

## Gotchas {#gotchas}

- **„Wir haben Kafka aktualisiert, jetzt wird es schneller sein"** - Änderungen an der Admin-Konfiguration sind der häufigste Auslöser für Leader-Not-Available-Fehler im Produktivbetrieb
- **`flush()` in Python wirft bei Zustellungsfehlern keine Ausnahme** - es gibt die Anzahl der Nachrichten zurück, die sich noch in der Warteschlange befinden; Fehler müssen im Delivery-Callback geprüft werden, nicht im Rückgabewert von `flush()`
- **TCP-Uhrendrift bricht Verbindungen ab** - driften die Uhren von Producer und Broker deutlich auseinander, schlägt die Validierung der Zeitstempel beim TCP-Handshake fehl
- **Immer eine Dead Letter Queue implementieren** - sie kann ein Kafka-Topic, eine Datenbanktabelle oder eine Datei sein; die rohen Nachrichtenbytes protokollieren, nicht die deserialisierte Form
- **Client verbindet sich bei Broker-Ausfall automatisch neu** - `bootstrap.servers` mit mehreren Brokern ermöglicht automatisches Failover; der Metadaten-Refresh erkennt die verfügbaren Broker

## See Also {#see-also}

- [[kafka-monitoring]] - Metriken, Alarmschwellen
- [[delivery-semantics]] - At-most-once-, At-least-once- und Exactly-once-Muster
- [[consumer-groups]] - Mechanik des Rebalancings
- [[broker-architecture]] - Retention, Segmente, ISR-Verwaltung

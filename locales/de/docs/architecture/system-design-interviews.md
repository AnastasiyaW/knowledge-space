---
title: "Systementwurf-Interviews und Praxis"
category: reference
tags: [system-design, interview, estimation, architecture, practice]
level: 3
source_sha256: b3d3998010e117811c907decc11f9a9c60e4ac08d9300c417835e3af506c49d5
translation: machine
translated_at: '2026-10-24'
---
# Systementwurf-Interviews und Praxis {#system-design-interviews-and-practice}

Strukturierter Ansatz für Systementwurfsprobleme, ob im Interview oder bei realer Architekturarbeit. Dieselbe Methodik gilt für beides.

## 7-Schritte-Prozess {#7-step-process}

1. **Anforderungen klären** - Fragen stellen, nichts voraussetzen
2. **Umfang und Grenzen definieren** - was dazugehört, was nicht
3. **Zentrale Entitäten und Beziehungen identifizieren** - Datenmodell
4. **Architektur auf hoher Ebene entwerfen** - Komponenten und Interaktionen
5. **Kritische Komponenten im Detail betrachten** - die schwierigsten Teile
6. **Querschnittsthemen behandeln** - Sicherheit, Monitoring, Fehlertoleranz
7. **Abwägungen und Alternativen diskutieren** - immer erklären, WARUM

## Häufige Fehler {#common-mistakes}

- Sofort zur Lösung springen, bevor die Anforderungen verstanden sind
- Nicht-funktionale Anforderungen ignorieren
- Fehlerszenarien nicht berücksichtigen
- Über-Engineering für unwahrscheinliche Skalierung
- Nur eine Option präsentieren, ohne Alternativen
- Fehlende NFR-Berechnungen (keine Zahlen für Last, Speicher, Latenz)
- Nicht erklären, WARUM eine Technologie gewählt wurde

## NFR-Schätzungstabellen {#nfr-estimation-tables}

Für jedes System Projektionen für Jahr 1-5 erstellen:
- DAU, Spitzenwert gleichzeitiger Nutzer
- Anfragen pro Sekunde (RPS)
- Datenvolumen und Wachstumsrate
- Speicherbedarf
- Farbcodierung: Grün (beherrschbar), Gelb (Aufmerksamkeit), Rot (Herausforderung)

## Referenzwerte zur Performance {#performance-reference-numbers}

| Operation | Latenz |
|-----------|---------|
| Speicherzugriff | ~100 ns |
| SSD-Lesezugriff | ~100 us |
| Netzwerk-Roundtrip (gleiches RZ) | ~500 us |
| Verteilter Cache (Redis) | ~1 ms |
| Einfache DB-Abfrage | ~1-10 ms |
| Netzwerk über Regionen hinweg | ~50-150 ms |

## Drei-Optionen-Regel {#three-option-rule}

Für jede Entscheidung mindestens 3 Ansätze präsentieren:
- Auch wenn zwei offensichtlich falsch sind, erläutern, WARUM sie schlecht sind
- Kommunikation mit nicht-technischen Stakeholdern trainieren
- Ermöglicht informierte Entscheidungsfindung

## Praxisbeispiel: URL-Shortener {#practice-url-shortener}

**Anforderungen:** URLs verkürzen, weiterleiten, Statistiken erfassen. <100ms Latenz, 99,9% Verfügbarkeit, 10K+ RPS.

**Architektur:**
- Redis für häufig genutzte URL-Zuordnungen, PostgreSQL für Metadaten
- ClickHouse für Analysen und Aggregationen
- Horizontale Skalierung des zustandslosen Weiterleitungsdienstes
- Base62-Kodierung für kurze IDs

## Praxisbeispiel: Benachrichtigungsdienst {#practice-notification-service}

**Anforderungen:** mehrere Kanäle (SMS, E-Mail, Push, Messenger), Provider-Integration, Verlauf, Analysen, Vorlagen, A/B-Tests.

**Architektur:**
- Kafka für Zuverlässigkeit und Pufferung
- Kanal-Abstraktionsschicht für Unabhängigkeit von Providern
- Prioritätssystem für verschiedene Benachrichtigungstypen
- Template-Engine mit Variablenersetzung

## Dokumentation für nicht-technische Stakeholder {#documenting-for-non-technical-stakeholders}

1. **Das Offensichtliche erklären** - was Ingenieure wissen, ist für Manager nicht offensichtlich
2. **Gedankenkette zeigen** - wie man zur Schlussfolgerung gelangt ist
3. **Verzweigungspunkte kennzeichnen** - wo die Argumentation abweichen könnte
4. **Abwägungen quantifizieren** - Kosten, Zeit, Risiko für jede Option
5. **Vergleichstabellen verwenden** - nebeneinander mit Kriterien

## Hot/Cold-Storage-Muster {#hotcold-storage-pattern}

- **Hot:** Aktuelle Daten (3-6 Monate) auf schnellem Speicher (SSD, In-Memory)
- **Cold:** Alte Daten auf günstigem Speicher (S3, HDD)
- 999/1000 Anfragen treffen auf Hot-Daten; Cold-Zugriffe sind langsam, aber selten

### Wörterbuch/Normalisierung für Analysen {#dictionarynormalization-for-analytics}
Wiederholte Zeichenketten durch Ganzzahl-IDs ersetzen:
- Zeichenkette der Browserversion (50-100 Bytes) -> 2-Byte-Ganzzahl
- 25-50-fache Speicherreduktion
- Wörterbuch an Abfragegrenzen anwenden (beim Eingang dekodieren, beim Ausgang kodieren)

## Stolperfallen {#gotchas}

- **Anforderungserhebung wird am meisten unterschätzt** - hier scheitern die meisten Kandidaten und Projekte
- **„Die einfachste Lösung, die die Anforderungen erfüllt, gewinnt"** - nicht über-engineeren
- **Immer quantifizieren** - „hohe Last" bedeutet nichts. „10K RPS mit <100ms P99" bedeutet alles
- **Kunden beschreiben IST- und SOLL-Zustand vermischt** - aktuellen Zustand vom gewünschten Zustand trennen
- **Alte API-Versionen länger beibehalten als erwartet** - manche Clients rufen APIs nur einmal im Jahr auf

## Siehe auch {#see-also}

- [[solution-architecture-process]] - Vollständige Anforderungspipeline
- [[architecture-documentation]] - C4, ADR, 4+1-Sichten
- [[database-selection]] - Auswahl von Datenbanken
- [[quality-attributes-reliability]] - SLA, Verfügbarkeitsrechnung

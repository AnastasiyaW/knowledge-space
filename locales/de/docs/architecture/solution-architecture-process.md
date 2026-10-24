---
title: "Prozess der Lösungsarchitektur"
category: concepts
tags: [architecture, requirements, stakeholders, trade-offs, process]
level: 3
source_sha256: 4bcfcb8724331b10443a25cca390c34b2a86454845a6f951b4f202af4d900375
translation: machine
translated_at: '2026-10-24'
---
# Prozess der Lösungsarchitektur {#solution-architecture-process}

Die Lösungsarchitektur verbindet Geschäftsanforderungen mit der technischen Umsetzung. Der Prozess des Architekten reicht von der Erhebung der Anforderungen bis zur Bereitstellung und konzentriert sich darauf, Zielkonflikte (Trade-offs) zu finden und aufzulösen. Mehr als 60 % des Erfolgs hängen von Soft Skills ab – Lösungen werden von Menschen für Menschen geschaffen.

## Architekturebenen und Rollen {#architecture-levels-and-roles}

| Ebene | Umfang | Schwerpunkt |
|-------|-------|-----------------|
| **Unternehmensarchitektur** | Gesamte Organisation | Geschäftsstrategie, globale Prozesse |
| **Lösungsarchitektur** | Konkretes Geschäftsproblem | Schnittstelle Geschäft–Technik, Systemintegration |
| **System-/Technische Architektur** | Einzelnes System | Module, Code, atomare Prozesse |

| Rolle | Umfang | Hauptaktivität |
|------|-------|-----------------|
| Senior Engineer | Eigene Aufgaben/Module | Entwicklung |
| Tech Lead | Teamweit | Entwicklung + etwas Design |
| Solution Architect | Mehrere Teams | Design + Abstimmung mit dem Geschäft |

In kleineren Organisationen übernimmt eine Person mehrere Rollen. Autorität wird durch nachgewiesene Expertise erworben, nicht durch den Titel.

## Anforderungspipeline {#requirements-pipeline}

```php
Business Architecture Study
  -> Stakeholder Identification
    -> Requirements Elicitation (WHY, WHO, HOW)
      -> NFR Definition (quantified with numbers)
        -> ASR Extraction
          -> Trade-off Identification
            -> Trade-off Resolution
              -> Ready for Solution Design
```

### Drei zentrale Fragen {#three-key-questions}

1. **WARUM** wird diese Lösung geschaffen? – Geschäftsanforderungen, Ziele, erwarteter Nutzen
2. **WER** wird sie nutzen? – Alle Nutzergruppen (Kunden, Supportmitarbeiter, Administratoren, Partner, Sicherheit)
3. **WIE** wird sie genutzt? – Nutzungsszenarien als Grundlage des Designs

**Grundsatz:** Antworten dürfen nicht erfunden werden. Interagieren Sie aktiv mit den Stakeholdern. In dieser Phase sind Sie Forscher.

### Identifikation der Stakeholder {#stakeholder-identification}

Übliche Stakeholder: Business-Sponsoren, Endnutzer, Entwickler/Tester, Support/Betrieb, Sicherheitsabteilung, Call-Center-Mitarbeiter. Frühzeitig einbinden, um Vertrauen aufzubauen. Brainstorming, Stakeholder-Mapping sowie Einfluss-/Interessenanalyse einsetzen.

## Nicht-funktionale Anforderungen (NFRs) {#non-functional-requirements-nfrs}

Ohne NFRs baut man ein System, das abstürzt, Daten verliert oder nur einmal pro Stunde antwortet. Immer mit Zahlen quantifizieren.

| Kategorie | Was definiert wird | Beispiel |
|----------|---------------|---------|
| **Performance** | Zielwerte für Antwortzeiten | Chatbot antwortet in < 3 Sekunden |
| **Verfügbarkeit** | Anforderungen an die Betriebszeit | 99,9 % SLA |
| **Skalierbarkeit** | Umgang mit Wachstum | Unterstützung einer Verzehnfachung der Nutzer |
| **Sicherheit** | Datenschutz, Compliance | Einhaltung des Datenschutzrechts |
| **Zuverlässigkeit** | Fehlertoleranz, Dauerhaftigkeit | Daten überstehen Ausfälle |
| **Wartbarkeit** | Einfachheit von Updates und Fehlersuche | Monitoring, strukturiertes Logging |

### Checkliste zur Lastabschätzung {#load-estimation-checklist}

- Erwartete gleichzeitige Nutzer
- Anfragen pro Sekunde (RPS)
- Datenvolumen und Wachstumsrate
- Verhältnis von Spitzen- zu Durchschnittslast
- Antwortzeit bei P95/P99

## Architekturrelevante Anforderungen (ASRs) {#architecturally-significant-requirements-asrs}

Merkmale einer funktionalen ASR:
- Führt eine **neue Integration** in das System ein
- Erfordert ein **neues Nutzerinteraktionsmuster**
- Wirkt **komplex** und hat keine triviale einfache Umsetzung

**ALLE NFRs sind architekturrelevant** – sie beeinflussen die Infrastrukturwahl, Architekturmuster, Technologieauswahl und die Kosten der Lösung.

## Architektonische Zielkonflikte (Trade-offs) {#architectural-trade-offs}

**Kernprinzip: Architektur ist die Kunst und Wissenschaft, Zielkonflikte zu finden und aufzulösen.** Perfekte Lösungen gibt es nicht – nur Zielkonflikte, die in die eine oder andere Richtung aufgelöst werden.

| Zielkonflikt | Beispielhafte Auflösung |
|-----------|-------------------|
| Performance vs. Kosten | Mit günstiger Variante starten, später aufrüsten |
| Sicherheit vs. Benutzerfreundlichkeit | Vollständige Authentifizierung für Chatbot weglassen; nur Name und E-Mail verlangen |
| Skalierbarkeit vs. Komplexität | Mit einem Monolithen starten, auf künftige Microservices auslegen |
| Verfügbarkeit vs. Kosten | 99,9 % statt 99,999 % akzeptieren |
| Funktionsumfang vs. Time-to-Market | MVP mit Kernfunktionen, danach iterieren |

### Auflösungsansätze {#resolution-approaches}

1. **Mit den Stakeholdern priorisieren** – festlegen, welches Merkmal wichtiger ist
2. **Mittelweg finden** – beide Seiten teilweise erfüllen

Immer dokumentieren: welcher Zielkonflikt erkannt wurde, welche Entscheidung getroffen wurde, warum, und was dafür geopfert wurde.

## Referenzpunkte zum Datenvolumen {#data-volume-reference-points}

| Bereich | Einstufung | Auswirkungen |
|-------|---------------|-------------|
| < 100 GB | Klein | Einzelne Maschine, minimale Komplexität |
| < 2 TB | Mittel | Einzelne große Maschine, verwaltete Dienste |
| < 10–50 TB | Erheblich | Mehrere Maschinen, sorgfältige Planung |
| < 1 PB | Groß | Dynamische Skalierung, erheblicher Aufwand |
| > 100 PB | Extrem | Plattentausch wird zur Routine |

## Fallstricke {#gotchas}

- **Überspringen der Anforderungsphase** ist die Hauptursache für Projektscheitern – jede Phase speist die nächste
- **Kunden beschreiben IST und SOLL vermischt** – der Architekt muss beides trennen und fragen: „Warum investiert das Geschäft?“
- **Eine fehlende funktionale ASR erfordert meist keinen vollständigen Neubau** – sie wird typischerweise durch einen zusätzlichen Service gelöst
- **Ticket-Titel ohne Beschreibung** – moderne Teams erwarten, dass Ingenieure Anforderungen selbstständig untersuchen
- **Drei-Optionen-Regel** – für jede Entscheidung mindestens drei Ansätze präsentieren, auch wenn zwei davon offensichtlich falsch sind

## Siehe auch {#see-also}

- [[architecture-documentation]] – C4-Modell, ADRs, 4+1-Sichten
- [[architectural-styles]] – Spektrum von Monolith bis Microservices
- [[quality-attributes-reliability]] – Metriken zu Verfügbarkeit, Fehlertoleranz, Wiederherstellbarkeit
- [[database-selection]] – Auswahl von Datenbanken nach Datentyp und Anforderungen

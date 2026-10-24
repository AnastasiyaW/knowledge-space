---
title: "Architekturdokumentation"
category: concepts
tags: [architecture, documentation, c4-model, adr, uml, diagrams]
level: 3
source_sha256: 8f98448ff3296ec91aa4d0e9b7164eb8ec55f66af0e9e4cad0e0d065423f89c3
translation: machine
translated_at: '2026-10-24'
---
# Architekturdokumentation {#architecture-documentation}

Architekturdokumentation sollte pragmatisch statt erschöpfend sein. Das Agile Manifest besagt, dass funktionierende Software wichtiger ist als umfassende Dokumentation – doch Dokumentation bleibt wertvoll. Der Fokus sollte auf dem liegen, was Teams bei Entscheidungen unterstützt und ihnen hilft, das System zu verstehen.

## Dokumentationsmethoden {#documentation-methods}

- **Diagramme** – frei gestaltet (flexibel, benötigt eine Legende) oder formale Notationen (UML, ArchiMate, C4, BPMN)
- **ADRs** – Architecture Decision Records, RFCs
- **Tabellen** – strukturierter Vergleich von Optionen
- **Code** – ArchUnit für automatisierte Tests der Architekturkonformität
- **Checklisten** – Validierungskriterien

## Minimales praktikables Architekturdokument {#minimum-viable-architecture-document}

Falls kein organisationsweiter Standard existiert, dokumentiere mindestens:

1. **Zentrale Architekturentscheidungen und Prinzipien** – Entscheidungen, die die Gesamtstruktur prägen
2. **Wichtige Komponenten und ihre Interaktionen** – Daten- und Arbeitsfluss durch das System
3. **Technologieentscheidungen mit Begründung** – warum jedes Werkzeug ausgewählt wurde
4. **Datenschemata und Beziehungen** – Datenmodelle, Entitätsbeziehungen

## 4+1-Architektursichtenmodell (Kruchten) {#41-architectural-view-model-kruchten}

| Sicht | Zeigt | Diagramme |
|-------|-------|-----------|
| **Logisch** | Funktionalität für Endbenutzer | Klassen-, Sequenzdiagramme |
| **Prozess** | Nebenläufigkeit, Synchronisation, Performance | Aktivitäts-, Zustandsdiagramme |
| **Komponente** | Softwarestruktur für Entwickler | Komponenten-, Paketdiagramme |
| **Physisch** | Infrastruktur und Hardware | Verteilungsdiagramme |
| **Szenarien (+1)** | Anwendungsfälle, die alle Sichten verbinden | Anwendungsfalldiagramme |

Jedes Szenario wird durch die anderen vier Sichten verfolgt und validiert so die Architektur.

## C4-Modell {#c4-model}

Pragmatische Alternative zu vollständigem UML mit vier Abstraktionsebenen:

### Ebene 1: Systemkontext {#level-1-system-context}
Oberste Ebene. Das System als Kasten, umgeben von Benutzern und externen Systemen. Beantwortet: Was ist das System, wer nutzt es, und mit welchen Systemen ist es integriert?

### Ebene 2: Container {#level-2-container}
Zoomt in das System hinein. Zeigt Anwendungen, Datenbanken, Message-Broker, Dateisysteme. Jeder Container ist eine separat deploybare Einheit.

### Ebene 3: Komponente {#level-3-component}
Zoomt in einen Container hinein. Zeigt interne Komponenten (Controller, Services, Repositories) und deren Interaktionen.

### Ebene 4: Code {#level-4-code}
Diagramme auf Klassenebene. Werden selten von Architekten erstellt – automatisch generiert oder nur für kritische Module.

## Architecture Decision Records (ADR) {#architecture-decision-records-adr}

Leichtgewichtige Dokumentation einzelner Entscheidungen:

```markdown
# ADR-001: Use PostgreSQL for primary data storage

## Status: Accepted
## Date: 2024-01-15

## Context
We need a database for our order processing service.

## Decision
Use PostgreSQL 15.

## Rationale
- Team expertise in PostgreSQL
- ACID compliance required for financial data
- JSON support covers semi-structured data needs
- Cost-effective

## Alternatives Considered
- MongoDB: rejected due to ACID requirements
- MySQL: rejected due to limited JSON support

## Consequences
- Need DBA expertise for optimization
- Must plan for read replicas as load grows
```

## UML-Diagramme für Architekten {#uml-diagrams-for-architects}

### Strukturell (am häufigsten verwendet) {#structural-most-used}
- **Komponentendiagramm** – Systemkomponenten und Schnittstellen
- **Verteilungsdiagramm** – Abbildung der physischen Infrastruktur

### Verhalten (am häufigsten verwendet) {#behavioral-most-used}
- **Sequenzdiagramm** – Interaktion zwischen Komponenten über die Zeit (entscheidend für API-Design)
- **Aktivitätsdiagramm** – Arbeits- bzw. Prozessablauf über Systeme hinweg

## Attribute-Driven Design (ADD) {#attribute-driven-design-add}

Iterativer Entwurfsprozess des CMU SEI:

1. **Sicherstellen, dass Anforderungen erhoben wurden** – Anwendungsfälle, Randbedingungen, Qualitätsattributszenarien
2. **Zu verfeinerndes Element auswählen** – das gesamte System oder ein bestimmtes Modul
3. **Architekturtreiber identifizieren** – Utility Tree nutzen, um zu priorisieren (hohe/mittlere geschäftliche Bedeutung x technische Schwierigkeit)
4. **Entwurfskonzept wählen** – Muster, Taktiken, Referenzarchitekturen, Frameworks, COTS
5. **Elemente instanziieren und Verantwortlichkeiten zuweisen**
6. **Schnittstellen definieren** – Verträge zwischen Elementen
7. **Verifizieren und verfeinern** – prüfen, ob die Zerlegung die Treiber erfüllt

**Abbruchkriterium:** wenn kritische Risiken abgefangen sind, alle Treiber adressiert wurden oder die eingeplante Entwurfszeit abgelaufen ist.

## Reihenfolge der Dokumentationslieferung {#documentation-delivery-sequence}

1. Architekturüberblick – Systemkontext- und Komponentendiagramme
2. API-Spezifikationen – OpenAPI für REST, WSDL für SOAP, AsyncAPI für ereignisgesteuerte Systeme
3. Datenmodelldokumentation – ER-Diagramme, Schemadefinitionen
4. Integrationsspezifikationen – Verbindungen zu externen Diensten
5. Bereitstellungsleitfaden – Infrastrukturanforderungen, Konfiguration
6. Runbook – Betriebsprozeduren, Monitoring, Incident-Response

## Architekturprinzipien, die etabliert werden sollten {#architectural-principles-to-establish}

1. **Separation of Concerns** – jede Komponente hat eine klar begrenzte Verantwortung
2. **DRY** – eine einzige Quelle der Wahrheit für Daten und Logik
3. **KISS** – die einfachste Lösung, die die Anforderungen erfüllt
4. **YAGNI** – baue nicht, was du noch nicht brauchst
5. **Fail Fast** – Fehler sofort erkennen und melden
6. **Design for Failure** – davon ausgehen, dass Komponenten ausfallen werden
7. **Konfiguration statt Code** – umgebungsspezifische Einstellungen auslagern
8. **API First** – Schnittstellen vor der Implementierung entwerfen

## Fallstricke {#gotchas}

- **Wähle Frameworks nicht nach Trends aus** – berücksichtige Teamwissen, Lernkurve, Reife des Produkts und Lizenztypen
- **Entwurf in Isolation** kann zu Lösungen führen, die kritische Qualitätsattribute schlecht unterstützen
- **Feature-Matrix hilft** – Entscheidungen bei der Bewertung von Alternativen Qualitätsattributen zuordnen
- **Qualitätsattribute stehen in Konflikt** – die Verbesserung des einen kann das andere verschlechtern; den Zielkonflikt dokumentieren
- **Vollständige SAD-Dokumente** können buchlang werden – frage zuerst nach bestehenden Dokumentationsstandards

## Siehe auch {#see-also}

- [[solution-architecture-process]] – Anforderungserhebung und Auflösung von Zielkonflikten
- [[api-documentation-specs]] – OpenAPI-, WSDL-, AsyncAPI- und OpenRPC-Spezifikationen
- [[architectural-styles]] – Spektrum vom Monolithen zu Microservices

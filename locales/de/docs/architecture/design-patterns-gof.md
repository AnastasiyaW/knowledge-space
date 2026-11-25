---
title: "Entwurfsmuster (GoF)"
category: concepts
tags: [design-patterns, gof, solid, oop, creational, structural, behavioral]
level: 3
source_sha256: c5f21df0168cad8898eba79991de8205e8af63b286a8e77b371610a877b781f8
translation: machine
translated_at: '2026-10-24'
---
# Entwurfsmuster (GoF) {#design-patterns-gof}

Klassische Entwurfsmuster der Gang of Four. Ein Muster beschreibt ein allgemeines Konzept zur Lösung eines häufig auftretenden Problems. Nur verwenden, wenn es notwendig ist, denn unnötige Muster erhöhen die Komplexität.

## SOLID-Prinzipien {#solid-principles}

| Prinzip | Regel | Anzeichen für eine Verletzung |
|-----------|------|----------------|
| **S**ingle Responsibility | Eine Klasse = ein Grund zur Änderung | Klasse übernimmt Logging UND Geschäftslogik |
| **O**pen/Closed | Offen für Erweiterung, geschlossen für Änderung | Bestehende Klasse wird für neues Verhalten geändert |
| **L**iskov Substitution | Subtypen sind als Basistypen einsetzbar | Überschreibung bricht den Vertrag der Basisklasse |
| **I**nterface Segregation | Viele spezifische Schnittstellen > eine allgemeine | Implementierung ungenutzter Methoden |
| **D**ependency Inversion | Von Abstraktionen abhängen, nicht von Implementierungen | Direkte Instanziierung von Abhängigkeiten |

**Meta-Prinzipien:** Komposition gegenüber Vererbung bevorzugen; gegen Schnittstellen programmieren, nicht gegen Implementierungen.

## Erzeugungsmuster (Creational Patterns) {#creational-patterns}

| Muster | Zweck | Wann verwenden |
|---------|---------|-------------|
| **Factory Method** | Schnittstelle zur Objekterzeugung, Unterklassen entscheiden über den Typ | Typen sind im Voraus unbekannt, Erweiterungspunkt wird benötigt |
| **Abstract Factory** | Familien zusammengehöriger Objekte erzeugen | Mehrere Produktfamilien |
| **Builder** | Komplexe Objekte schrittweise konstruieren | Viele optionale Parameter, unterschiedliche Repräsentationen |
| **Prototype** | Objekte durch Klonen bestehender Objekte erzeugen | Aufwendige Konstruktion, Unterklassenbildung vermeiden |
| **Singleton** | Genau eine Instanz, globaler Zugriff | DB-Pool, Konfiguration. Achtung: verletzt SRP, verbirgt Abhängigkeiten |

## Strukturmuster (Structural Patterns) {#structural-patterns}

| Muster | Zweck | Wann verwenden |
|---------|---------|-------------|
| **Adapter** | Inkompatible Schnittstelle umwandeln | Integration von Legacy-Systemen oder Drittanbieter-Software |
| **Bridge** | Abstraktion von der Implementierung trennen | Mehrere orthogonale Dimensionen, Umschalten zur Laufzeit |
| **Composite** | Baumstrukturen, einheitliche Behandlung | Teil-Ganzes-Hierarchien (Dateisystem, UI, Organigramm) |
| **Decorator** | Verhalten dynamisch durch Umhüllung hinzufügen | Zusatzfunktionen ohne Unterklassenbildung |
| **Facade** | Vereinfachte Schnittstelle zu einem komplexen Subsystem | Kopplung reduzieren, praktische Standardwerte |
| **Flyweight** | Gemeinsamen Zustand zwischen vielen Objekten teilen | Sehr große Anzahl ähnlicher Objekte, die Speicher belegen |
| **Proxy** | Stellvertreter, der den Zugriff steuert | Lazy Loading, Zugriffskontrolle, Caching, Logging |

## Verhaltensmuster (Behavioral Patterns) {#behavioral-patterns}

| Muster | Zweck | Wann verwenden |
|---------|---------|-------------|
| **Chain of Responsibility** | Anfrage entlang einer Kette von Handlern weitergeben | Mehrere Handler, wechselnde Reihenfolge, Kette zur Laufzeit |
| **Command** | Anfrage als Objekt kapseln | Undo, Warteschlangen, Protokollierung von Operationen |
| **Iterator** | Kollektion durchlaufen, ohne interne Details offenzulegen | Komplexe Strukturen (Baum, Graph) mit sequentiellem Zugriff |
| **Mediator** | Kommunikation zentralisieren | Viele Abhängigkeiten zwischen Komponenten |
| **Memento** | Zustand erfassen und wiederherstellen, ohne Kapselung zu verletzen | Undo/Redo, Snapshots (Editor-Verlauf, Spielstände) |
| **Observer** | Abonnementbasierte Ereignisbenachrichtigung | Änderungen in einem Objekt erfordern Aktualisierung anderer Objekte |
| **State** | Verhalten ändert sich abhängig vom internen Zustand | Viele Bedingungen, die vom Zustand abhängen |
| **Strategy** | Austauschbare Algorithmen | Algorithmen zur Laufzeit wechseln, viele Varianten |
| **Template Method** | Algorithmus-Gerüst, Unterklassen überschreiben Schritte | Gemeinsamer Ablauf, unterschiedliche konkrete Schritte |
| **Visitor** | Neue Operationen ohne Änderung der Klassen | Operationen ändern sich häufig, Struktur ist stabil |

## Leitfaden zur Musterauswahl {#pattern-selection-guide}

```yaml
Creating objects:
  One type           -> Factory Method
  Family of types    -> Abstract Factory
  Complex build      -> Builder
  Clone existing     -> Prototype

Structuring:
  Incompatible APIs  -> Adapter
  Dynamic behavior   -> Decorator
  Tree structures    -> Composite
  Simplify complex   -> Facade

Communication:
  Event notification -> Observer
  Centralized comms  -> Mediator
  Sequential handling -> Chain of Responsibility
  Encapsulated ops   -> Command

Algorithm variation:
  Interchangeable    -> Strategy
  Skeleton + hooks   -> Template Method
  State-dependent    -> State
```

## OOP-Beziehungen {#oop-relationships}

| Beziehung | Bedeutung | Stärke |
|-------------|---------|----------|
| **Dependency** | Nutzt vorübergehend | Schwächste |
| **Association** | Nutzt (hat eine Referenz) | Schwach |
| **Aggregation** | Hat, kann eigenständig existieren | Mittel |
| **Composition** | Besitzt, Lebensdauer abhängig | Stark |
| **Inheritance** | Ist-ein | Stärkste |
| **Implementation** | Realisiert eine Schnittstelle | - |

## Fallstricke {#gotchas}

- **Singleton** ist das am häufigsten falsch eingesetzte Muster. Oft reicht einfache Dependency Injection aus.
- **Übermäßiger Einsatz von Mustern** erhöht die Komplexität. Wenn der Code auch ohne Muster sauber funktioniert, sollte keines erzwungen werden.
- **Decorator vs. Vererbung**: Decorator ist flexibler, erzeugt aber viele kleine Objekte. Vererbung ist einfacher, wenn die Hierarchie stabil ist.
- **Speicherlecks durch Observer**: Vergessene Abonnements halten Objekte am Leben. Immer abmelden.
- **Strategy vs. State**: Beim Strategy-Muster wählt der Client den Algorithmus; beim State-Muster finden Übergänge intern statt.

## Siehe auch {#see-also}

- [[architectural-styles]] - Muster auf Architekturebene
- [[microservices-communication]] - Muster für verteilte Systeme
- [[enterprise-integration]] - Enterprise-Integrationsmuster (EIP)

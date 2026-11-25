---
title: "Grenzgetriebenes Refactoring"
description: "Extraktion, Schnittstellen und Migrationsarbeit anhand beobachteter Verantwortlichkeiten und Consumer-Grenzen auswählen und anschließend prüfen, ob das geforderte Verhalten weiterhin funktioniert."
tags: [architecture, refactoring, interfaces, domain-driven-design, testing]
level: 4
source_sha256: 6f245f4bad70012613caddb988c7a2b9d4c4d8470b77bcdabafad40ee7bf4c7e
translation: machine
translated_at: '2026-10-24'
---
# Grenzgetriebenes Refactoring {#boundary-driven-refactoring}

**Stand der Prüfung: 2026-09-06.** Refactoring-Entscheidungen brauchen einen konkreten Grund: eine Verantwortung, die sich unabhängig ändert, eine Abhängigkeit, die kontrolliert werden muss, einen Eigentümerfehler oder einen Consumer-Vertrag, den die aktuelle Struktur verschleiert. Dateilänge und ein Sauberkeitswert können Prüfstellen lokalisieren. Keiner von beiden begründet, dass eine weitere Schicht notwendig ist.

Diese Referenz beschreibt eine technische Entscheidungsrichtlinie. Sie schreibt weder eine universelle Dateigrößenbegrenzung noch eine Anzahl von Klassen, eine Vererbungshierarchie oder eine Anzahl von Reviews vor. Ziel ist eine wartbare Implementierung des akzeptierten Verhaltens einschließlich der Integrationsarbeit, die nötig ist, damit es nutzbar wird.

## Die Grenze identifizieren, bevor die Abstraktion gewählt wird {#identify-the-boundary-before-choosing-the-abstraction}

Beginnen Sie mit der geänderten Operation. Identifizieren Sie ihre Eingaben, ihr Ergebnis, den Zustandseigentümer, die Aufrufer, externe Effekte und das Fehlerverhalten. Fragen Sie dann, welche Verantwortung einen eigenen Vertrag braucht.

| Beobachtetes Signal | Mögliche Änderung | Evidenz, die sie rechtfertigt |
|---|---|---|
| eine wiederholte Berechnung hat eine zusammenhängende Bedeutung | eine benannte Funktion extrahieren | Aufrufer teilen dieselbe Semantik und dasselbe Fehlerverhalten |
| Domänenregeln ändern sich unabhängig von der Ablaufsteuerung | Regeln von der Anwendungslogik trennen | eine reale Regel oder Änderungshistorie identifiziert den Regelverantwortlichen |
| mehrere unterstützte Implementierungen müssen einen Consumer bedienen | eine schmale Schnittstelle oder einen Port definieren | tatsächliche Implementierungen und Anforderungen der Aufrufer stimmen auf den Vertrag überein |
| eine Plugin- oder Binärgrenze braucht eine stabile Oberfläche | den Kompatibilitätsvertrag isolieren | unterstützte Consumer, Eigentümerschaft, Versionierung und Fehlersemantik sind bekannt |
| ein externer Effekt verhindert einen gezielten Test | an diesem Effekt eine schmale Naht (Seam) bereitstellen | der Test isoliert eine reale Abhängigkeit, ohne das getestete Verhalten zu ersetzen |
| eine große Datei enthält unzusammenhängende Lebenszyklen | nach Verantwortung und Eigentümerschaft aufteilen | getrennte Zustands-, Teardown- oder Abhängigkeitsanforderungen lassen sich benennen |
| die Datei ist lediglich lang | vor einer Umstrukturierung ihre Kohäsion prüfen | keine Extraktion ist gerechtfertigt, solange keine echte Grenze oder kein echtes Wartungsproblem gefunden wurde |

Mehrere Implementierungen sind eine Begründung für eine Schnittstelle, aber keine Voraussetzung für jede Schnittstelle. Eine einzelne Implementierung kann trotzdem hinter einem geforderten Plugin-Vertrag oder einer Grenze zu externen Effekten stehen. Umgekehrt bedeuten zwei ähnliche Klassen nicht zwingend, dass sie eine stabile Abstraktion teilen.

Vererbung ist nur angemessen, wenn das abgeleitete Objekt den Basisvertrag erfüllen kann, einschließlich Lebensdauer und Fehlerverhalten. Das Teilen weniger Implementierungszeilen reicht nicht aus. Eine Hilfsfunktion oder ein komponierter Mitarbeiter kann diese Wiederverwendung ausdrücken, ohne Substituierbarkeitspflichten einzuführen.

## Domänenverhalten dort platzieren, wo seine Invarianten durchgesetzt werden können {#put-domain-behavior-where-its-invariants-can-be-enforced}

Halten Sie Verhalten lokal bei dem Zustand, dessen Invarianten es schützt, sofern dies ein kohärentes Domänenmodell ergibt. Ein Domänendienst ist angemessen für eine Domänenoperation, die natürlicherweise weder zu einer Entität noch zu einem Wertobjekt gehört, einschließlich Regeln, die mehrere Entitäten oder Aggregate betreffen. Ein Anwendungsdienst koordiniert einen Anwendungsfall, Transaktionen und externe Interaktionen. Das sind unterschiedliche Verantwortlichkeiten und keine Regel, dass alles Verhalten in Dienstklassen gehört. [Taktisches Domain-Driven Design](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design)

Betrachten Sie als Beispiel eine Bildexport-Funktion. Dies ist ein hypothetisches Designbeispiel, keine gemessene Produktimplementierung:

- eine Export-Spezifikation validiert ihre eigenen Abmessungen und Formatvorgaben;
- eine Farbrichtlinien-Komponente entscheidet über die unterstützte Konvertierungsrichtlinie;
- eine Anwendungsoperation besorgt das Bild, wendet die gewählte Richtlinie an und schreibt das Ergebnis;
- ein Ausgabe-Adapter verantwortet Dateisystem- oder Remote-Storage-Effekte.

Erzeugen Sie nicht jede Komponente allein deshalb, weil die Liste existiert. In einer kleinen Implementierung können eine Funktion und ein Effekt-Adapter die tatsächlichen Grenzen abdecken. Teilen Sie weiter, wenn unterschiedliche Eigentümerschaft, Richtlinien oder Consumer den Vertrag nützlich machen. Halten Sie notwendiges komponentenübergreifendes Verhalten in den Abnahmekriterien fest, statt Erfolg zu erklären, weil die Klassen einzeln kompilieren.

## Build-Abhängigkeiten an den Vertrag angleichen {#make-build-dependencies-match-the-contract}

Eine Trennung auf Quellcode-Ebene ist unvollständig, wenn das Build-System weiterhin Implementierungsabhängigkeiten gegenüber jedem Consumer offenlegt. In CMake gelten `PRIVATE`-Anforderungen für das Bauen des Targets, `INTERFACE`-Anforderungen für Consumer und `PUBLIC`-Anforderungen für beide. Wählen Sie den Gültigkeitsbereich anhand dessen, was Consumer benötigen, insbesondere anhand dessen, was die öffentlichen Header voraussetzen. Usage-Requirements sollten echte Anforderungen abbilden, keine unzusammenhängenden Vorlieben. [CMake: Build-Spezifikation und Usage-Requirements](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html)

Eine Abhängigkeit, die nur von einer Implementierungsdatei verwendet wird, ist ein Kandidat für eine private Verlinkung. Wenn die öffentliche API Abhängigkeitstypen offenlegt oder ihre Header voraussetzt, kann das Verbergen dieser Anforderung Consumer brechen. Der geeignete Nachweis ist ein realer Consumer-Build gegen die deklarierte Target-Schnittstelle, nicht ein erfolgreicher Build, der zufällig globale Include-Pfade erbt.

Diese Unterscheidung verlangt nicht für jede Klasse ein neues CMake-Target. Fügen Sie ein Target hinzu, wenn es eine tatsächliche Build-, Distributions-, Eigentums- oder Abhängigkeitsgrenze darstellt.

## Die Consumer-Migration abschließen {#finish-the-consumer-migration}

Eine Extraktion gilt nicht als geliefert, solange bekannte Aufrufer noch den kaputten Pfad verwenden oder der Ersatz nicht erreichbar ist. Erfassen Sie die Consumer an der geänderten Grenze und erhalten Sie die Kompatibilitätsbedingungen, auf die sie sich stützen.

| Grenze | Relevanter Migrationsnachweis |
|---|---|
| interne Funktion | bekannte Aufrufer kompilieren und die betroffenen Verhaltensprüfungen bestehen |
| API einer gemeinsam genutzten Bibliothek | unterstützte Consumer bauen und beobachten die vereinbarte Eigentümer- und Fehlerregelung |
| Datei- oder Nachrichtenschema | Produzent und Consumer stimmen über Version, Interpretation und Fehlerverhalten überein |
| persistierter Zustand | repräsentative bestehende Daten bleiben lesbar oder es gibt einen verifizierten Migrationspfad |
| bereitgestellter Endpunkt | eine autorisierte Integrationsprüfung erreicht das vorgesehene Release und beobachtet dessen Ergebnis |

Ein Produktions-Canary ist relevant, wenn die akzeptierte Änderung eine bereitgestellte Service-Grenze umfasst. Für eine lokale Funktionsextraktion ist er keine universelle Voraussetzung. Ebenso reicht ein Unit-Test nicht aus, wenn das geforderte Ergebnis von einem unabhängig deployten Consumer abhängt.

Behalten Sie den alten Pfad bei, bis der erforderliche Migrationsnachweis vorliegt. Seine Entfernung ist eine eigene Änderung mit eigenen Kompatibilitäts- und Autorisierungsbedingungen. Wechseln Sie Provider oder Datenstandorte nicht stillschweigend, nur um eine Prüfung grün zu machen.

## Einen ausreichenden Verifikationssatz auswählen {#select-a-sufficient-verification-set}

Verwenden Sie ein fehlschlagendes Beispiel, wenn das Refactoring einen beobachteten Defekt behebt. Bewahren Sie Prüfungen für die Verträge, die die Änderung ungültig machen könnte: Ergebnisstruktur, Eigentümerschaft, Fehlersemantik, Zustandsübergänge und tatsächliches Consumer-Verhalten. Eine reine Quellcode-Bereinigung ohne Verhaltensänderung braucht möglicherweise eine andere Prüfung als eine Reparatur des Lebenszyklus.

Dokumentieren Sie, welcher Nachweis zu welcher Revision und Grenze gehört. Kompilierung belegt eine Build-Eigenschaft, ein Fixture belegt seine Zusicherungen, ein Integrationsbeleg belegt die beobachtete Interaktion in dieser Umgebung. Keiner davon belegt automatisch das gesamte Produktergebnis. Siehe [[agent-evaluation]] und [[testing-and-quality]].

Wiederholen Sie eine bestandene Prüfung nur, wenn eine spätere Änderung oder eine neue Beobachtung ihr früheres Ergebnis unzureichend macht. Setzen Sie andere offene akzeptierte Arbeiten fort, fügen Sie aber nicht allein deshalb Schichten oder Review-Runden hinzu, weil der aktuelle Branch grün ist.

## Fallstricke {#gotchas}

- **Zeilenzahl als Ersatzkriterium:** Das Aufteilen einer zusammenhängenden Datei in viele Dateien kann dieselbe Kopplung erhalten und die Navigation erschweren. Prüfen Sie Verantwortung und Eigentümerschaft, bevor Sie die Aufteilung wählen.
- **Schnittstelle vor Semantik:** Eine Schnittstelle mit ungeklärter Eigentümerschaft, Abbruchverhalten oder Fehlerverhalten verschiebt die Unsicherheit, statt sie aufzulösen.
- **Aufblähung durch Dienstklassen:** Wenn man jede Methode aus einer Entität herauslöst, werden Domänen-Invarianten schwerer durchzusetzen. Unterscheiden Sie Orchestrierung von Domänenverhalten.
- **Vollständig gemockte Integration:** Tests, die beide Seiten einer geänderten Grenze ersetzen, können bestehen, während reale Consumer inkompatibel bleiben.
- **Globales Build-Leck:** Consumer-Builds können gesund erscheinen, weil globale Include-Pfade eine unvollständige Target-Schnittstelle verdecken.
- **Vorzeitige Stilllegung:** Das Löschen eines alten Einstiegspunkts, bevor seine Aufrufer geprüft wurden, verwandelt eine strukturelle Bereinigung in einen Kompatibilitätsfehler.

## Einschränkungen {#limitations}

Diese Richtlinie ersetzt keine Domänenanalyse, keine Kompatibilitätszusagen und keine gemessene Performance-Arbeit. Einige etablierte Grenzen sind durch Plattform- oder organisatorische Randbedingungen begründet, die in einer einzelnen Datei nicht sichtbar sind. Halten Sie diese Randbedingungen fest, bevor Sie solche Grenzen zusammenlegen oder ersetzen. Keine universelle Größen- oder Komplexitätsschwelle kann belegen, dass eine Architektur korrekt ist.

## Verwandte Referenzen {#related-references}

- [[architecture-documentation]] — Grenze, Entscheidung, Alternativen und Consumer-Vertrag dokumentieren.
- [[cmake-build-systems]] — Build-Targets und Abhängigkeitsweitergabe.
- [[object-lifetime]] — Lebensdaueranforderungen, die eine Abstraktion erhalten muss.
- [[agent-evaluation]] — Quellcode-, Fixture-, Installations- und Consumer-Workflow-Nachweise getrennt betrachten.

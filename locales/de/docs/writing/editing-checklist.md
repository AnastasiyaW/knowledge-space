---
title: "Lektoratscheckliste für Textqualität"
description: "Fakten und technische Aussagen bewahren, während Klarheit, Struktur und Veröffentlichungsreife verbessert werden."
category: tools
tags: [writing, editing, checklist, verification, quality]
level: 4
source_sha256: c0adc70de1dd5788d0756d6f288e1f49fb404e4313b68a502c45affb9eb20a45
translation: machine
translated_at: '2026-10-24'
---
# Lektoratscheckliste für Textqualität {#editing-checklist-for-text-quality}

Verwenden Sie diese Checkliste, um ein Dokument zu verbessern, ohne die Aussagen zu verändern, die durch die Belege gestützt werden. Geprüfter Geltungsbereich, Stand 2026-09-06: technische Referenzen, Tutorials, Analysen und Vorfallberichte, einschließlich KI-gestützter Entwürfe.

Ein ungewohntes Wort oder ein gleichmäßiger Satzrhythmus ist kein sachlicher Mangel. Priorisieren Sie Korrektheit und die Aufgabe der Leserin bzw. des Lesers, nicht Detektor-Scores oder Stilvorgaben.

## Die Aussage vor der Änderung ihrer Formulierung sichern {#preserve-the-claim-before-editing-its-wording}

Halten Sie die ursprüngliche Quelle und den Entwurf während der Überarbeitung verfügbar. Ermitteln Sie bei wesentlichen Aussagen den Beleg und die genaue Reichweite der Aussage.

| Geschütztes Element | Unzulässige Änderung | Erforderliche Prüfung |
|---|---|---|
| Anzahl und Grundgesamtheit | 12 von 40 geprüften Datensätzen zu 12 erfolgreichen Datensätzen machen | Erhalten, was gezählt wurde und was ungeprüft bleibt |
| Historisches Datum | Eine datierte Beobachtung durch „derzeit“ ersetzen | Das Datum beibehalten, sofern nicht neue Belege eine Aktualisierung stützen |
| Modalität | Aus „kann sich erholen“ wird „wird sich erholen“ | Unsicherheit und Bedingungen beibehalten |
| Verneinung | „nicht“ beim Kürzen eines Satzes streichen | Die Aussage vergleichen, nicht nur übereinstimmende Schlüsselwörter |
| Einheiten und Versionen | Eine Einheit oder Version als optischen Ballast entfernen | Die Bedingungen beibehalten, die zur Deutung des Ergebnisses nötig sind |
| Zitat oder persönliche Erfahrung | „Wir haben getestet“ erfinden, um den Text authentischer wirken zu lassen | Nur bereitgestellte, klar zugeordnete Aussagen verwenden |
| Technischer Bezeichner | Eine API oder ein Flag für flüssigeren Text umbenennen | Die exakte Schreibweise anhand der maßgeblichen Quelle prüfen |

Unbekannte Größen bleiben unbekannt. Ein als solches gekennzeichnetes hypothetisches Beispiel ist zulässig, wenn es der Leserschaft dient, darf aber nicht als beobachtetes Ergebnis erscheinen.

## Die Struktur auf die Aufgabe der Leserschaft abstimmen {#choose-the-structure-for-the-readers-task}

| Dokument | Was muss leicht auffindbar sein | Was ist nicht zwingend erforderlich |
|---|---|---|
| Referenz | Vertrag, Parameter, Einschränkungen, Version, Fehlerfälle | Anekdoten, dramatische Einleitung, persönliche Meinung |
| Tutorial | Voraussetzungen, lauffähige Abfolge, erwartetes Ergebnis, Wiederherstellung | Ein Benchmark oder eine erfundene Projektgeschichte |
| Analyse | Fragestellung, Belege, Vergleichskriterien, Einschränkungen | Gleich große Abschnitte oder ein vorab festgelegtes Urteil |
| Vorfallbericht | Beobachteter Fehler, Ursache, Eingriff, Verifikation | Eine geschönte Erfolgsgeschichte, wenn die Wiederherstellung unvollständig ist |

Entfernen Sie Wiederholungen, wenn sie diese Elemente verdecken. Strecken Sie einen Absatz nicht und fügen Sie keine rhetorische Frage nur hinzu, damit das Dokument weniger gleichförmig wirkt. Der [Google-Leitfaden zum Tonfall in der Entwicklerdokumentation](https://developers.google.com/style/tone) unterstützt klare, direkte und auf die Leserschaft zugeschnittene Sprache; er schreibt keine derartigen Quoten vor.

## In der Reihenfolge ihrer Tragweite prüfen {#review-in-order-of-consequence}

1. Nicht belegte oder widersprüchliche Aussagen sowie wesentliche Auslassungen prüfen.
2. Prüfen, ob die Leserschaft die beabsichtigte Aufgabe ausführen kann.
3. Beispiele, Bezeichner, Links und relevante Versionsbedingungen prüfen.
4. Mehrdeutige Formulierungen und unnötige Wiederholungen verbessern.
5. Die gewünschte Hausvorlage anwenden, ohne die ersten vier Ergebnisse zu verändern.

Ein brauchbarer redaktioneller Befund nennt die Stelle, erklärt ihre Auswirkung und gibt eine Korrektur, die mit den verfügbaren Belegen übereinstimmt. „Klingt nach KI“ bezeichnet keinen umsetzbaren technischen Mangel.

## Beispiele und Abschlussbehauptungen verifizieren {#verify-examples-and-completion-claims}

Wenn ein Dokument Code enthält, testen Sie die angegebene lauffähige Grenze mit der genannten Laufzeitumgebung und den genannten Abhängigkeiten. Kennzeichnen Sie ein illustratives Fragment als solches. Suggerieren Sie nicht, dass ein ausgelassener Dienst, eine Testvorrichtung, ein Zugangsdatum oder ein Modell erprobt wurde.

Halten Sie diese unterschiedlichen Aussagen getrennt:

- Quellenprüfung: Eine Empfehlung oder ein Codepfad wurde durchgesehen.
- Fixture-Prüfung: Das bereitgestellte Beispiel hat einen begrenzten Test bestanden.
- Installationsprüfung: Die vorgesehenen Dateien oder Konfigurationen sind am Zielort angekommen.
- Verbraucherprüfung: Das vorgesehene Werkzeug oder die vorgesehene Leserschaft hat das gelieferte Ergebnis geladen.
- Produktergebnis: Der angeforderte reale Arbeitsablauf wurde unter seinen tatsächlichen Bedingungen abgeschlossen.

Ein grüner Fixture-Test ersetzt nicht den letzten Punkt. Ebenso belegen eine gültige Artikelquelle oder ein erfolgreicher Git-Push nicht, dass die Leserschaft die neue Seite sehen kann.

## Automatisierung für eng begrenzte Aussagen nutzen {#use-automation-for-narrow-assertions}

Automatisierte Prüfungen können defekte Links, fehlerhaftes Markup, geänderte Zahlen oder fehlende geschützte Bezeichner erkennen. Ihr Ergebnis beschränkt sich auf diese Aussagen.

Ein Zahlenvergleich erkennt nicht jede Bedeutungsänderung: „12 fehlgeschlagen“ und „12 bestanden“ enthalten dieselbe Zahl. Behalten Sie eine inhaltliche Prüfung der Aussage und ihrer Quelle bei. Ein Hinweis eines Prosa-Linters sollte zur Prüfung anregen, nicht zum automatischen Austausch von Wörtern führen.

Verwenden Sie einen Detektor-Score nicht als Bedingung für die redaktionelle Freigabe. Die Hauptstudie zur [Verzerrung von Detektoren bei nicht-muttersprachlichem Englisch](https://arxiv.org/abs/2304.02819) dokumentiert Einschränkungen der untersuchten Detektoren und Stichproben; sie begründet keinen allgemeingültigen Test für die aktuelle Urheberschaft.

## Stoppen, wenn das angeforderte Dokument fertig ist {#stop-when-the-requested-document-is-ready}

Sobald wesentliche Mängel behoben und die angeforderten Prüfungen bestanden sind, beenden Sie die kosmetische Überarbeitung. Dokumentieren Sie gegebenenfalls eine Prüfung ohne Änderungen. Führen Sie verbleibende angeforderte Veröffentlichungs- oder Auslieferungsschritte aus; die bloße Durchsicht des Textes schließt einen Auftrag zur Veröffentlichung nicht ab.

## Stolperfallen {#gotchas}

- **Erfundene Konkretheit:** Eine Quote für Zahlen oder Anekdoten erzeugt Druck, nicht belegte Fakten bereitzustellen. Entfernen Sie die Quote, nicht die Unsicherheit.
- **Historische Aussagen werden aktuell:** Wenn ein Datum durch „jetzt“ ersetzt wird, ändern sich stillschweigend die Wahrheitsbedingungen. Behalten Sie das Quellendatum bei oder beschaffen Sie neue Belege.
- **Endlose Überarbeitungsdurchgänge:** Jeder Durchgang findet eine neue persönliche Vorliebe. Öffnen Sie nur einen wesentlichen Mangel oder eine geänderte Abnahmebedingung erneut.
- **Umschreiben aus dem Gedächtnis:** Quellenbedingungen verschwinden bei einer flüssigen Umformulierung. Vergleichen Sie die bearbeitete Aussage mit der tatsächlichen Quelle, nicht mit der Erinnerung.

## Siehe auch {#see-also}

- [[ai-text-detection]]
- [[technical-article-structure]]
- [[agent-evaluation]]

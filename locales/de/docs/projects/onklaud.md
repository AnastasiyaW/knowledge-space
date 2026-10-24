---
title: "Onklaud 5"
category: projects
date: 2026-07-02
tags: [onklaud, onklaud-5-development, project]
aliases: ["Onklaud 5"]
level: 2
source_sha256: 62808b08818dca5f095e7d5cf36641767dc713d71b367d3f05fb70d0ab5e9f98
translation: machine
translated_at: '2026-10-24'
---
# Onklaud 5 {#onklaud-5}

**Entwicklungslinie:** `project:onklaud` · Thread `onklaud-5-development`  
**Letztes Ereignis:** 2026-07-02 · 1 datiert seit 2026-07-02 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Onklaud 5: ein Python-Orchestrierungswerkzeug für Entwickler, die einen Codeentwurf nicht von einem einzelnen Modell, sondern von mehreren Sprachmodellen bewerten lassen möchten.

- findet bekannte Lösungen aus Bibliotheken oder der Standardbibliothek, bevor Code generiert wird;
- führt Review-Durchläufe mit Kimi und GLM aus, anschließend eine Schiedsschleife und ein lokales Qualitätsgate;
- akzeptiert einen OpenRouter-Schlüssel und kann einen lokalen Endpunkt mit OpenAI-kompatibler API verwenden.

## Entwicklungslinie {#development-line}

- **2026-07-02 — Am 2026-07-02 wurde Onklaud 5 mit einem öffentlichen GitHub-Repository verknüpft.** Am 2026-07-02 enthielt die Entwicklungslinie von Onklaud 5 einen Link zum GitHub-Repository KorroAi/onklaud-5. Der datierte Link belegt einen öffentlichen Repository-Verweis für das Projekt, aber weder ein Release, einen Funktionsumfang noch eine Codeänderung.

## Was sich geändert hat {#what-changed}

2026-06-22 — Laut aktueller Dokumentation hat das Projekt seine interne Benchmark-Suite ausgeführt und dabei 20 von 35 Ponytail-Treffer sowie 29 von 30 Pipeline-Prüfungen gemeldet. 2026-07-02 — Onklaud 5 wurde über das verlinkte Repository verfügbar gemacht; der aktuelle Checkout konfiguriert Kimi K2.7 Code und GLM 5.2, aber kein datierter Tag oder Commit belegt, dass genau dieser Zustand am Ereignisdatum bestand.

## So wird es verwendet {#how-to-use-this}

Ab dem 2026-07-02 sollten Praktiker KorroAi/onklaud-5 als den identifizierten öffentlichen Repository-Verweis für Onklaud 5 behandeln und dessen Inhalte prüfen, bevor sie sich darauf verlassen.

1. Klonen Sie das Repository, kopieren Sie `.env.example` nach `.env` und setzen Sie `OPENROUTER_API_KEY` für die Kimi- und GLM-Aufrufe.
  — <https://github.com/KorroAi/onklaud-5>
2. Führen Sie `python test_pipeline.py` als mitgelieferten lokalen Smoke-Test aus, bevor Sie es mit einem Workflow verbinden.
  — <https://github.com/KorroAi/onklaud-5>
3. Prüfen Sie die Konfiguration mit `python council.py status` und reichen Sie dann einen Entwurf mit `python council.py dual --type code --prompt "..." --draft-file file.py` ein; verwenden Sie `loop` für den längeren Pfad mit Vordesign, Dual-Review, Gate und Schiedsverfahren.
  — <https://github.com/KorroAi/onklaud-5>

## Bewährte Vorgehensweisen {#best-practices}

- Behandeln Sie `test_pipeline.py` als strukturellen Smoke-Test und nicht als End-to-End-Nachweis für gehostete Modelle: Sein Standard-Einstiegspunkt führt lokale Prüfungen aus und ruft nie einen API-Test auf. Ergänzen Sie einen nicht sensiblen API-Canary-Test und Ihre eigene Testsuite, bevor Sie sich auf ein Review-Ergebnis verlassen.
  — <https://github.com/KorroAi/onklaud-5/blob/master/test_pipeline.py>
- Akzeptieren Sie keine degradierte Council-Schleife als normales Review: Ohne `OPENROUTER_API_KEY` warnt der Code ausdrücklich, dass der Loop-Modus degradiert läuft; andere API-Modi geben einen Fehler zurück.
  — <https://github.com/KorroAi/onklaud-5/blob/master/council.py>
- Stellen Sie sicher, dass Ihre Produktivnutzung die Bedingung zu Umsatz oder Mitarbeiterzahl erfüllt, oder erwerben Sie eine kommerzielle Lizenz; die BSL wird erst am 2030-06-22 in MIT umgewandelt.
  — <https://github.com/KorroAi/onklaud-5/blob/master/LICENSE>

## Hierdurch ersetzt {#superseded-by-this}

- Die Empfehlung, das aktuelle Repository als freie Open-Source-Software zu behandeln, ist überholt: Die Lizenz ist BSL 1.1 mit bedingten Produktionsrechten bis zu ihrem MIT-Umstellungsdatum (beobachtet am 2026-09-05).

## Weiterhin unbekannt {#still-unknown}

- Ein datierter Tag, ein Release oder ein archivierter Commit für den 2026-07-02 war nicht verfügbar; daher kann das aktuelle Repository seinen Inhalt zu diesem Datum nicht belegen.
- Die aktuellen Quellen nennen das Repository Onklaud 5, während die Lizenz das lizenzierte Werk als v3.2 bezeichnet; eine dokumentierte Zuordnung zwischen diesen Bezeichnungen wurde nicht gefunden.
- Die Angaben von 57,1 % Aufgabenlösungsrate und zur Qualität sind Selbstauskünfte; eine unabhängige Reproduktion wurde nicht gefunden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/KorroAi/onklaud-5 | KorroAi/onklaud-5 — Onklaud-5-Repository und README | 2026-09-05 |
| https://github.com/KorroAi/onklaud-5/blob/master/council.py | Onklaud 5 council.py | 2026-09-05 |
| https://github.com/KorroAi/onklaud-5/blob/master/test_pipeline.py | Onklaud 5 test_pipeline.py | 2026-09-05 |
| https://github.com/KorroAi/onklaud-5/blob/master/LICENSE | Onklaud 5 Business Source License 1.1 | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:onklaud`, Thread `onklaud-5-development`, 1 datiertes Ereignis vom 2026-07-02 bis 2026-07-02.
- **Praktischer Hinweis:** Ab dem 2026-07-02 sollten Praktiker KorroAi/onklaud-5 als den identifizierten öffentlichen Repository-Verweis für Onklaud 5 behandeln und dessen Inhalte prüfen, bevor sie sich darauf verlassen.
- **Konfidenz:** mittel. Datierte Ersetzungen sind maßgeblich dafür, was veraltet ist.

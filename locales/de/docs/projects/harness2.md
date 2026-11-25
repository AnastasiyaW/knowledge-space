---
title: "Harness^2: harness2-open-source-release — Harness2-Open-Source-Veröffentlichung"
category: "projects"
date: 2026-10-18
tags: ["harness2", "harness2-open-source-release", "project"]
aliases: ["Harness^2: harness2-open-source-release"]
level: 2
source_sha256: c78fda51470e0ac0f7e3829ba44f8dcade711c64c9074437357da30d45aabfaa
translation: machine
translated_at: '2026-10-24'
---
# Harness^2: harness2-open-source-release — Harness2-Open-Source-Veröffentlichung {#harness2-harness2-open-source-release-harness2-open-source-release}

**Entwicklungslinie:** project:harness2 · Thread harness2-open-source-release  
**Letztes Ereignis:** 2026-10-18 · 3 datierte seit 2026-10-18 · **Recherchiert:** 2026-10-19 · Konfidenz: hoch

## Was es ist {#what-it-is}

Harness² ist ein Forschungsframework für Ingenieure, die prüfen, ob sich das System um einen Agenten herum verbessern lässt, ohne die Modellgewichte zu verändern. Es bearbeitet und evaluiert Prompts, Guardrails, Speicher, Anleitungen zur Tool-Nutzung, Subagenten, Skills, Skripte und Plugins. Es unterstützt parallele und sequenzielle Rekursion, die Executors OpenCode und Codex sowie drei Benchmark-Integrationen.

Läufe mit Modellen erfordern lokale Einrichtung und können API-Kosten verursachen. Der Web-Zugriff des Executors ist standardmäßig nicht eingeschränkt. Verwende Harness² für kontrollierte Experimente zur Verbesserung des Harness, nicht als Nachweis dafür, dass ein überarbeitetes Harness für ungeprüften Produktiveinsatz sicher ist.

## Entwicklungslinie {#development-line}

- **2026-10-18 — Harness^2 führt rekursive Optimierung des Agenten-Harness für eingefrorene Sprachmodelle ein.** Autoren von Google stellten Harness^2 vor, ein Framework, das das Harness eines eingefrorenen Sprachmodells (Prompts, Guardrails, Skills, Skripte, Zwischencode) ohne Referenz-Verifikatoren optimiert. Es nutzt Rekursion auf Aufgaben- und Setup-Ebene mit einer wiederverwendbaren Verbesserungsbibliothek. Gemeldete Durchschnittswerte im WorkBuddy-Bench stiegen für GLM-5 bei k=1 von 64,2 auf 75,7 und bei k=5 auf 80,8. JobBench stieg von 31,5/32,9 auf 39,0. Der Beitrag weist darauf hin, dass die Prüfung mehrerer Kandidaten die Inferenz-Token-Kosten erhöht.
- **2026-10-18 — Google macht den Agenten-Harness Harness² als Open Source verfügbar.** Am 2026-10-18 meldete der erfasste Link, dass Google Harness² als Open Source veröffentlicht hat. Beschrieben wird er als sofort einsetzbares Harness für die rekursive Verwaltung von KI-Agenten in offenen Umgebungen. Agenten können aus Erfahrungen bei Aufgaben lernen, die außerhalb des ursprünglichen Zwecks des Harness liegen. Das Harness besteht aus acht Komponenten: System-Prompt, Guardrails, Speicher, Anleitungen zur Tool-Nutzung, Subagenten, Skills, Skripte und Plugins. Das verlinkte GitHub-Repository ist google-research/harness2.
- **2026-10-18 — Google macht den Agenten-Harness Harness² als Open Source verfügbar.** Google hat Harness² als Open Source veröffentlicht. Es wird als sofort einsetzbares Harness für die rekursive Verwaltung von KI-Agenten in einer offenen Umgebung beschrieben. Seine acht Komponenten sind System-Prompt, schützende Randbedingungen, Speicher, Anleitungen zur Tool-Nutzung, Subagenten, Skills, Skripte und Plugins.
- **2026-10-18 — weitere Berichterstattung zu diesem Datum.**
  - Das begleitende Paper beschreibt, dass das Harness für das eingefrorene Modell acht editierbare, dateibasiert eingebundene Komponenten hat. Die Verfeinerung auf Aufgabenebene verwendet Propose–Probe–Compose ohne Ground-Truth-Feedback. Eine separate Schleife auf Harness-Ebene behält durch Belege gestützte Erkenntnisse für spätere Aufgaben. (2026-10-09) — <https://arxiv.org/abs/2610.14224>
  - Die Veröffentlichung ist Quellcode unter Apache-2.0 mit einem Installationsweg für Linux/Python 3.12/uv und einer deterministischen lokalen Demo, die keine Modell-Zugangsdaten benötigt. Läufe des Benchmarks mit Modellen benötigen zusätzlich Node.js, die Google Cloud CLI, benchmarkspezifische Abhängigkeiten und die Modellkonfiguration durch den Nutzer. (undatiert) — <https://github.com/google-research/harness2>
  - Die öffentliche Implementierung unterstützt die Executors OpenCode und Codex, parallele oder sequenzielle Rekursion sowie JobBench, LAB und WorkBuddy-Bench. Die README warnt, dass der Netzwerkzugriff des Executors nicht eingeschränkt ist und dass Codex-Läufe mit deaktivierter Sandbox ausgeführt werden, sofern der Betreiber keine Netzwerkbeschränkungen konfiguriert. (undatiert) — <https://github.com/google-research/harness2>

## Was sich geändert hat {#what-changed}

Öffentliche Veröffentlichung (2026-10-18): Harness² hat seine Methode der rekursiven Harness-Optimierung als Code-Repository unter Apache-2.0 verfügbar gemacht. Das Paper beschreibt die Verfeinerung auf Aufgabenebene mit Propose–Probe–Compose sowie dauerhafte Aktualisierungen der Verbesserungsbibliothek über Aufgaben hinweg.

## So verwendest du es {#how-to-use-this}

1. Unter Linux mit Python 3.12 und uv die dokumentierte virtuelle Umgebung anlegen, das editierbare Paket installieren und die Demo ohne Zugangsdaten ausführen, bevor ein Modell angebunden wird.
  — <https://github.com/google-research/harness2>
2. Für einen Lauf mit einem Modell die aufgeführten Laufzeit- und Benchmark-Abhängigkeiten installieren, Modelleinstellungen und Authentifizierung konfigurieren und dann mit einer Benchmark-Aufgabe und einer kleinen Auswahl beginnen.
  — <https://github.com/google-research/harness2>
3. Prüfung, Verfeinerung, Bewertung und Berichterstattung mit demselben Benchmark, Executor, derselben Teilmenge, demselben Rekursionsbudget, Modus und Seed ausführen. Mit dem Dry-Run lässt sich die Aufgabenauswahl ohne Modellaufrufe prüfen.
  — <https://github.com/google-research/harness2>
4. Parallele Rekursion wählen, um Kandidaten-Harnesses breiter zu erkunden, oder sequenzielle Rekursion, um Verfeinerungen über aufeinanderfolgende Schritte weiterzuführen. Übernommene Harnesses nur zusammen mit den unterstützenden Ausführungsnachweisen behalten.
  — <https://github.com/google-research/harness2>

## Bewährte Vorgehensweisen {#best-practices}

- Netzwerkbeschränkungen vor der Evaluation konfigurieren, damit öffentliche Benchmark-Rubriken, Antworten oder Bewertungskriterien nicht in einen Executor mit uneingeschränktem Web-Zugriff gelangen.
  — <https://github.com/google-research/harness2>
- Die Evaluationskonfiguration bei Bewertung und Berichterstattung identisch zum Verfeinerungslauf halten. Eine Änderung von Benchmark, Executor, Teilmenge, Rekursionsmodus, Budget oder Seed macht ein vergleichbares Ergebnis ungültig.
  — <https://github.com/google-research/harness2>
- Größere Rekursionsbudgets als expliziten Kompromiss zwischen Rechenaufwand und Leistung behandeln. Das Paper zählt sowohl Ausführungs- als auch Verbesserungs-Token, und seine Gewinne wurden nur in den evaluierten Benchmark-Konfigurationen gemessen.
  — <https://arxiv.org/abs/2610.14224>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die Repository-Seite nennt keinen stabilen öffentlichen Veröffentlichungszeitpunkt. Der Ereignisnachweis wird daher als undatiert markiert und nicht einem abgeleiteten Repository-Datum zugeordnet.
- In den qualifizierten Quellen wurde kein unabhängiger Praxisbericht über dauerhafte Nutzung oder die Reproduktion von Benchmarks gefunden.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2610.14224 | Harness²: Recursive Agent Harnessing for an Open World | 2026-10-19 |
| https://github.com/google-research/harness2 | google-research/harness2: Recursive Agent Harnessing for an Open World | 2026-10-19 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** project:harness2, Thread harness2-open-source-release, 3 datierte Ereignisse 2026-10-18 → 2026-10-18.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich für das, was veraltet ist.

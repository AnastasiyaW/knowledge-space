---
title: "Aufbau technischer Artikel"
category: patterns
tags: [writing, technical-writing, article-structure, publishing]
level: 3
source_sha256: 783faee36de60640b14bf597da0d872ec3f25b7437ac5912ebb4a97865dfc68a
translation: machine
translated_at: '2026-10-24'
---
# Aufbau technischer Artikel {#technical-article-structure}

So strukturierst du technische Artikel, die gelesen, geteilt und gespeichert werden. Basis sind Muster aus technischen Inhalten mit hohem Engagement auf verschiedenen Plattformen. Das Kernprinzip: Beginne mit dem Problem, das du tatsächlich hattest, nicht mit einem Themenüberblick.

## Das Hook-Problem-Lösung-Muster {#the-hook-problem-solution-pattern}

Die leistungsstärkste Struktur für technische Artikel:

1. **Hook** (1-3 Sätze) - die konkrete Situation, die dich zum Schreiben bewegt hat
2. **Kontext** - was du erreichen wolltest und warum bestehende Lösungen nicht funktioniert haben
3. **Lösung** - was du gemacht hast, mit Code und Details
4. **Ergebnisse** - was passiert ist, mit Zahlen
5. **Einschränkungen** - was nicht funktioniert, Randfälle, Grenzen
6. **Nächste Schritte** - was du anders machen würdest oder was noch offen ist

Das ist NICHT die übliche akademische Struktur "Einleitung -> Hintergrund -> Methode -> Fazit". Leser technischer Blogs wollen den Nutzen früh und die Details später.

## Einstiege, die funktionieren {#opening-patterns-that-work}

**Mit dem Problem beginnen:**
> Unsere CI-Pipeline brauchte 47 Minuten. Deployments fanden zweimal täglich statt, sodass Ingenieure täglich über 90 Minuten auf Builds warteten.

**Mit einem überraschenden Ergebnis beginnen:**
> Wir haben 60 % unserer Microservices gelöscht, und die Zuverlässigkeit hat sich verbessert. Hier ist der Grund.

**Mit einem Fehlschlag beginnen:**
> Ich habe am Freitag um 16 Uhr 2 Mio. Zeilen in das neue Schema migriert. Das Rollback dauerte bis Sonntag.

**Was nicht funktioniert:**
> In der heutigen schnelllebigen Welt der Softwareentwicklung sind Continuous Integration und Continuous Deployment (CI/CD) zu unverzichtbaren Praktiken für moderne Engineering-Teams geworden. Dieser Artikel untersucht...

## Platzierung von Code-Beispielen {#code-examples-placement}

**Regeln:**
- Das erste Code-Beispiel steht im ersten Drittel des Artikels
- Verwende Code aus deinem echten Projekt, keine generischen Beispiele
- Gib Versionsnummern, Betriebssystem und Laufzeitdetails an
- Zeige den Fehler bzw. die Ausgabe, nicht nur die Eingabe
- Halte einzelne Code-Blöcke unter 30 Zeilen und teile längere Beispiele auf

**Gutes Muster für die Platzierung:**
```ini
[2-3 paragraphs of context]
[code block showing the problem]
[1-2 paragraphs explaining]
[code block showing the solution]
[paragraph on results]
[code block showing results/benchmarks]
```

**Schlechtes Muster für die Platzierung:**
```ini
[10 paragraphs of theory]
[massive code block with everything]
[brief conclusion]
```

## Abschnittsaufbau {#section-breakdown}

### Für Tutorials und How-to-Artikel {#for-tutorialhow-to-articles}

```ini
# [Specific outcome] with [specific tool]

## The Problem
[2-3 sentences - what wasn't working]
[Error message or screenshot]

## What I Tried First
[Brief dead-end descriptions - shows real experience]

## The Solution
[Step-by-step with code blocks]
[Each step: what to do, why, expected output]

## Gotchas
[Things that broke during implementation]
[Edge cases discovered in production]

## Results
[Before/after metrics]
[Timeline: how long the migration/implementation took]
```

### Für Untersuchungs- und Debugging-Artikel {#for-investigationdebug-articles}

```bash
# How We Fixed [specific problem]

## Symptoms
[What was observed - exact error messages, metrics]

## Initial Hypotheses
[What we thought was wrong and why]

## Investigation
[Tools used, commands run, what each revealed]
[Include dead ends - "we checked X but it was fine"]

## Root Cause
[What actually happened]

## Fix
[What we changed, with code diff]

## Prevention
[What we changed to catch this earlier]
```

### Für Vergleichs- und Evaluierungsartikel {#for-comparisonevaluation-articles}

```sql
# [Tool A] vs [Tool B] for [specific use case]

## Our Requirements
[Specific criteria, not generic "performance and scalability"]

## Test Setup
[Exact versions, hardware, dataset size]

## Results
[Table with numbers]
[One section per criterion with details]

## Our Choice
[What we picked and why - take a position]

## What We'd Choose Differently For
[Other use cases where the other tool wins]
```

## Optimale Länge {#optimal-length}

- **Optimum**: 1200-2000 Wörter (7-10 Minuten Lesezeit)
- Kurze Artikel (<5 Min.): hohe Lesequote, aber weniger Engagement
- Mittlere Artikel (5-10 Min.): beste Balance zwischen Lesequote und Tiefe
- Lange Artikel (10+ Min.): geringere Lesequote, mehr Lesezeichen
- "Evergreen"-Tutorials erhalten unabhängig von der Länge langfristig stabilen Traffic

## Formatierungsgrundlagen {#formatting-essentials}

- **Überschriften**: H2 für Hauptabschnitte, H3 für Unterabschnitte. Keine H4+ in Blogbeiträgen
- **Code-Blöcke**: immer mit Sprachangabe, jeweils < 30 Zeilen
- **Bilder/Diagramme**: alle 300-500 Wörter zur Steigerung des Engagements
- **Fett** für Schlüsselbegriffe beim ersten Vorkommen, nicht zur Betonung in jedem Absatz
- **Links**: auf konkrete, relevante Ressourcen, nicht "mehr dazu hier" zu X
- **TL;DR**: bei langen Artikeln oben, nicht unten

## Techniken für Authentizität {#techniques-for-authenticity}

Aus der Analyse der bestbewerteten technischen Artikel:

1. **Sackgassen zeigen** - "Ich habe X versucht, aber es ist fehlgeschlagen, weil..."
2. **Konkrete Fehlermeldungen**, Stack-Traces und Versionsnummern zeigen
3. **Eigene Zahlen verwenden** - "hat auf meinem M1 MacBook 47 Minuten gedauert"
4. **Werkzeuge mit Version nennen** - nicht "ein beliebtes Framework"
5. **Widersprechen** - eine Position zu einem Tool oder Ansatz beziehen
6. **Eingestehen, was du nicht verstehst** - "Ich weiß immer noch nicht, warum das funktioniert"
7. **Code aus deinem echten Projekt verwenden**, keine bereinigten Beispiele
8. **Zeitangaben machen** - "um 2 Uhr nachts habe ich erkannt, dass das Problem..."
9. **Screenshots** deines tatsächlichen Terminals bzw. deiner IDE einfügen
10. **Vorher/Nachher zeigen** - konkreter Beleg, dass die Lösung funktioniert

## Anti-Patterns {#anti-patterns}

- Beginn mit "In der heutigen Welt..." oder "X hat zunehmend an Bedeutung gewonnen"
- Grundlagen erklären, die die Zielgruppe bereits kennt (Kenntnisstand der Leser einschätzen)
- Jedem Abschnitt gleich viel Raum geben, unabhängig vom Wert
- Erst in der zweiten Hälfte des Artikels Code zeigen
- Generisches Fazit, das die Einleitung wiederholt
- "Ich hoffe, das war hilfreich" als Schlusssatz

## Stolpersteine {#gotchas}

- **Problem:** Eine Debugging-Geschichte chronologisch zu erzählen ("zuerst habe ich A geprüft, dann B, dann C") kann ermüdend sein, wenn A und B Sackgassen waren. **Lösung:** Beginne mit Ursache und Fix und erkläre danach die Untersuchung. Leser wollen zuerst die Antwort, dann den Weg.
- **Problem:** Jedes Detail des Setups zu nennen, macht den Artikel für Leser mit anderen Umgebungen unzugänglich. **Lösung:** Nenne deine genaue Umgebung (Betriebssystem, Versionen, Hardware) einmal am Anfang und konzentriere dich dann auf die Konzepte. Verlinke Setup-Anleitungen, statt sie einzubetten.
- **Problem:** Code-Beispiele funktionieren isoliert, aber nicht in echten Projekten, weil Imports, Konfiguration und Fehlerbehandlung fehlen. **Lösung:** Zeige für mindestens ein zentrales Beispiel vollständigen, lauffähigen Code. Kennzeichne vereinfachte Beispiele ausdrücklich: "// vereinfacht - vollständige Version unter [Link]."

## Inhaltliche Rahmenmodelle {#content-frameworks}

### Story Spine (Pixar-adaptiert) {#story-spine-pixar-adapted}

Passt gut zu Debugging-Geschichten und Architekturentscheidungen. Die Erzählform "Mann im Loch" (Problem → schlimmer → gelöst):

```rust
"Once upon a time..." → project context, how things worked
"Every day..."        → the normal state before the problem
"One day..."          → the triggering problem or discovery
"Because of that..."  → failed attempt #1 (include this - it builds trust)
"Because of that..."  → deeper understanding
"Until finally..."    → solution and what changed permanently
```

Der Beat "fehlgeschlagener Versuch" entscheidet bei technischen Artikeln meist über Erfolg oder Misserfolg. Lässt man ihn weg, erhält man eine Pressemitteilung. Enthält er ihn, hat man eine Geschichte, die sich zu lesen lohnt.

### Problem-Entdeckung-Lösung mit Sackgassen {#problem-discovery-solution-with-dead-ends}

Das entscheidende Unterscheidungsmerkmal: Fehlgeschlagene Ansätze schaffen Vertrauen, sparen Lesern Zeit und erzeugen erzählerische Spannung.

```rust
"We tried X and it failed because Y" > clean success story
```

Leser vertrauen keinem Artikel ohne Sackgassen. Echte Ingenieursarbeit hat Sackgassen. Wenn dein Entwurf keine enthält, hast du sie herausredigiert - nimm sie wieder hinein.

### Learning in Public (Swyx-Muster) {#learning-in-public-swyx-pattern}

Schreibe darüber, was du lernst, **während** du es lernst. Nicht im Ton des "Expertentutorials", sondern als ehrliche Prozessdokumentation inklusive Fehler. 80 % der Entwickler veröffentlichen nie etwas. Schon durch das Veröffentlichen bist du voraus.

Format: Beschreibe die Verwirrung und den Moment, in dem sie sich aufgelöst hat, nicht nur die endgültige Antwort.

### Praktiker-Chronik {#practitioner-chronicle}

Geschrieben aus dem, was du **tust**, nicht aus dem, was du **liest**. Vorbilder: Simon Willison (schnelle Experimente, dokumentiert alles), Chip Huyen (verbindet Forschung und Produktion), Lilian Weng (ausführliche Erklärungen).

Der Test: Hätte dieser Artikel ohne die tatsächliche Arbeit entstehen können? Wenn ja, ist es ein Tutorial. Wenn nein, ist es eine Chronik.

### Erkenntnis-Taxonomie als Artikelquellen {#findings-taxonomy-as-article-seeds}

Markiere während der Arbeit deine Rohnotizen mit:

- `[DECISION]` → wird zu einem Artikel "Architekturentscheidungen"
- `[GOTCHA]` → wird zu einem Artikel "Dinge, die ich gern früher gewusst hätte"
- `[REUSE]` → wird zu einem Tutorial oder Leitfaden
- `[STORY]` → wird zu einer Chronik mit erzählerischem Bogen

### Journalistische SEO {#journalistic-seo}

Schreibe Antworten auf konkrete Fragen aus der Praxis, nicht generische Themeneinführungen.

```text
"Why does my RAG pipeline hallucinate on long documents?" ← specific, gets search traffic
"Introduction to RAG"                                     ← no one searches this
```

## Plattformspezifische Hinweise {#platform-specific-notes}

### Habr {#habr}

- Die Zielgruppe erkennt Füllmaterial sofort
- Überschriften: konkrete Zahlen + Fachterminologie → höhere CTR
- Höchstes Engagement: persönliche Erfahrung + technische Tiefe
- **Lesezeichen** sind die eigentliche Kennzahl - praktische Evergreen-Inhalte
- Anti-Patterns: KI-generierter Text, versteckte Werbung (wird von Moderatoren gemeldet)
- Die Dynamik in der ersten Stunde (1000+ Aufrufe) löst den Trending-Algorithmus aus
- Google Discover ist eine wichtige Traffic-Quelle für Habr-Artikel

### Medium / dev.to {#medium-devto}

- Medium: "Sinnstiftung" (erklären, WARUM etwas funktioniert) > Schritt-für-Schritt-Tutorials
- dev.to: anfängerfreundlich, tutoriallastig, anderes Publikum
- Beide: zuerst echten, unaufgeräumten Code zeigen, dann erklären

## Pipeline von der Chronik zum Artikel {#chronicle-article-pipeline}

```text
1. Capture  (during work): tag [DECISION], [GOTCHA], [REUSE], [STORY], screenshot outputs
2. Triage   (weekly): scan for narrative arc (problem → struggle → solution)
3. Outline  (Story Spine): identify the lowest point - that's the article center
4. Draft    write the problem first (hook), then solution (payoff), fill middle
5. Polish   cut ruthlessly, add code blocks/screenshots, write headline LAST
```

## Siehe auch {#see-also}

- [[natural-writing-style]]
- [[publishing-platforms]]
- [[editing-checklist]]
- [[seo-for-articles]]

---
title: "ResearchStudio"
category: projects
date: 2026-07-07
tags: [project, researchstudio]
aliases: ["ResearchStudio"]
level: 3
source_sha256: 5c3dba54d1c92fd0ba761bac2f9d96e9a39d0955b378ed191d9089a48e5a1896
translation: machine
translated_at: '2026-10-24'
---
dass ich die Anweisungen genau befolge. Hier ist die Übersetzung:

---
title: ResearchStudio
category: projects
date: 2026-07-07
tags: [project, researchstudio]
aliases: ["ResearchStudio"]
---

# ResearchStudio {#researchstudio}

**Entwicklungslinie:** `project:researchstudio` · Thread `researchstudio`  
**Letztes Ereignis:** 2026-07-07 · 1 datiertes seit 2026-07-07 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ResearchStudio ist eine unter MIT-Lizenz stehende Skill-Suite für Claude Code und Codex, die zwei Forschungsphasen abdeckt.

- Idea: durchsucht die Literatur, untersucht Richtungen und prüft auf Kollisionen mit dem Stand der Technik, um eine Idea Card zu erstellen.
- Reel: wandelt ein einzelnes Paper-PDF in ein Poster, ein kommentiertes Video, einen zweisprachigen Blog und einen interaktiven Reel um.

## Entwicklungslinie {#development-line}

- **2026-07-07 — Öffentliche Projektreferenzen zu ResearchStudio erfasst.** Am 2026-07-07 tauchten öffentliche Referenzen auf die Projektseite von Microsoft ResearchStudio und das zugehörige GitHub-Repository auf. Sie zeigen, dass das Projekt öffentlich existiert, bestätigen jedoch weder eine Release-Version, einen Funktionsumfang noch einen Launch-Status.

## Was sich geändert hat {#what-changed}

- 2026-07-03 — ResearchStudio-Idea hat den Workflow vor der Paper-Erstellung veröffentlicht: IdeaSpark, Paper-Search und Scoop-Check.
- 2026-07-05 — Begleitende Papers zu Idea und Reel dokumentierten die evidenzbasierten Ideenfindungs- und die Dissemination-Designs mit gemeinsam genutzter Extraktion.
- 2026-07-08 — ResearchStudio-Reel hat die Pipeline aus fünf Skills nach der Paper-Erstellung veröffentlicht, für Poster-, Video-, zweisprachige Blog- und interaktive Reel-Ausgaben.
- 2026-08-13 — IdeaSpark speichert nun die vollständige Anfrage, löst benannte Papers auf und protokolliert, ob die Auswahl einer angegebenen Lösungsrichtung folgte oder von ihr abwich.
- 2026-08-25 — Trending Paper als Einstiegspunkt zum Stöbern in der Forschung auf Basis von Reels veröffentlicht.
- 2026-09-03 — IdeaSpark um einen Validator für die chinesische Wortstellung mit Warnstufe ergänzt.

## Anwendung {#how-to-use-this}

Prüfen Sie vor der Übernahme des Projekts die offizielle ResearchStudio-Website und das Quell-Repository, Stand 2026-07-07. Allein diese Referenz bestätigt keinen bestimmten Workflow, keine bestimmte Funktion und kein bestimmtes Release.

1. Legen Sie mit conda (Python 3.10+) oder uv eine isolierte Python-Umgebung an und installieren Sie dann aus einem Clone heraus mit install.sh oder über den interaktiven npx-Installer.
  — <https://github.com/microsoft/ResearchStudio/blob/main/README.md>
2. Für eine frühe Forschungsrichtung rufen Sie IdeaSpark mit dem Problem sowie gegebenenfalls Randbedingungen, Seed-Papers und Rechenbudget auf; verwenden Sie Paper-Search und Scoop-Check, wenn diese Teile separat benötigt werden.
  — <https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea>
3. Für ein fertiges Paper führen Sie Paper2Assets einmal aus und verwenden dann das gemeinsame Bundle für Paper2Poster, Paper2Video, Paper2Blog und Paper2Reel.
  — <https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md>
4. Betrachten Sie einen interaktiven Reel über den mitgelieferten HTTP-Server statt die HTML-Datei direkt zu öffnen, da das Springen in Videos HTTP-Range-Unterstützung benötigt.
  — <https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md>

## Best Practices {#best-practices}

- Verwenden Sie die empfohlene Untergrenze für leistungsfähige Modelle und eine isolierte Umgebung, bevor Sie die Skills installieren.
  — <https://github.com/microsoft/ResearchStudio/blob/main/README.md>
- Geben Sie IdeaSpark konkrete Randbedingungen, Seed-Papers und Rechenlimits; führen Sie die Prüfung auf Stand der Technik durch, bevor Sie eine Neuheitsbehauptung als umsetzbar behandeln.
  — <https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea>
- Verwenden Sie ein Paper2Assets-Bundle für die Erstellung von Poster, Video, Blog und Reel gemeinsam, damit die Ergebnisse dieselbe extrahierte Evidenz nutzen.
  — <https://microsoft.github.io/ResearchStudio/reel-page/>
- Behalten Sie während Reel-Durchläufen die Zwischen-HTML-Dateien bei und validieren Sie den finalen Viewer über serve_reel.py.
  — <https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md>
- Aktualisieren Sie bei chinesischen Idea-Ausgaben auf die Version mit dem Validator für die Wortstellung und prüfen Sie dessen Warnungen, statt sich auf eine allgemeine Übersetzungsanweisung zu verlassen.
  — <https://github.com/microsoft/ResearchStudio/commit/2540dde4be02dc841444f4ef7d81aa73aa6cf86e>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-07-07 — Die Beschreibung von ResearchStudio als vollständiger Lebenszyklus-Release am selben Tag wird nicht gestützt: Die offizielle Historie datiert Idea auf 2026-07-03 und Reel auf 2026-07-08.
- 2026-08-13 — Die Vorgabe, ein bloßes Thema als gesamtes IdeaSpark-Briefing zu behandeln, ist durch die Beibehaltung der Anfrage, die Auflösung benannter Papers und die ausdrückliche Einordnung der Lösungsrichtung ersetzt.
- 2026-09-03 — „Natürliches Chinesisch, nicht wortwörtlich“ als alleinige Steuerung ist durch einen dokumentierten Validator für die Wortstellung mit Warnstufe ersetzt.

## Weiterhin unbekannt {#still-unknown}

- Kein Release-Eintrag aus erster Hand benennt eine eigenständige Änderung an ResearchStudio am 2026-07-07; ohne den ursprünglichen Quelltext kann dieses Datum nur als Erkennungszeitpunkt zwischen den Releases von Idea und Reel behandelt werden.
- Das Repository stellt keine Kompatibilitätsmatrix für getaggte Versionen bereit, daher bleiben exakte Abhängigkeits- und Laufzeit-Reproduzierbarkeit unverifiziert.
- Die veröffentlichten Benchmark-Behauptungen wurden von uns nicht unabhängig reproduziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://microsoft.github.io/ResearchStudio/ | ResearchStudio — Your AI co-author, from research problem to publication | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio | GitHub — microsoft/ResearchStudio | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/blob/main/README.md | ResearchStudio README | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea | ResearchStudio-Idea | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md | ResearchStudio-Reel README | 2026-09-05 |
| https://microsoft.github.io/ResearchStudio/reel-page/ | ResearchStudio-Reel Gallery | 2026-09-05 |
| https://arxiv.org/abs/2607.04439 | ResearchStudio-Idea: An Evidence-Grounded Research-Ideation Skill Suite from ML Conference Outcomes | 2026-09-05 |
| https://arxiv.org/abs/2607.04438 | ResearchStudio-Reel: Automate the Last Mile of Research from Paper to Poster, Video, and Blog | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/commits/main | ResearchStudio commit history | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/commit/2540dde4be02dc841444f4ef7d81aa73aa6cf86e | feat(idea-spark): Chinese word order is a rule, not a request | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:researchstudio`, Thread `researchstudio`, 1 datiertes Ereignis 2026-07-07 → 2026-07-07.
- **Praxishinweis:** Ab 2026-07-07 können Praktiker vor der Bewertung oder Übernahme des Projekts die offizielle ResearchStudio-Website und das Quell-Repository heranziehen; allein diese Zeile belegt keinen bestimmten Workflow, keine bestimmte Funktion und kein bestimmtes Release.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.

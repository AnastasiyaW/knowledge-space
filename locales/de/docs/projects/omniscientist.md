---
title: "OmniScientist"
category: projects

tags: [omniscientist, project]
aliases: ["OmniScientist"]
level: 3
source_sha256: 94746c7fc9adc8632e2927706d74473661eb05c54bb6b1a68a2d60e06d69dc83
translation: machine
translated_at: '2026-10-24'
---
# OmniScientist {#omniscientist}

**Entwicklungslinie:** `project:omniscientist` · Thread `omniscientist`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

OmniScientist ist ein offener, lokaler Forschungsworkflow für Personen, die aus einem Ordner mit Rohdaten und einer offenen Frage einen nachvollziehbaren Kandidaten für einen Fachartikel erstellen möchten.

- Eingaben: liest Bilder, Wellenformen, Audio, Video, Punktwolken, Trajektorien, Tabellen und Formeln.
- Stufen: führt Ideenfindung, Experiment und Verschriftlichung mit Code- und Artefaktspuren aus.
- Ausgaben: erzeugt TeX/PDF-Ausgaben, deren Zahlen mit aufgezeichneten Ausführungen verknüpft sind.

Die Autoren berichten von 36 Fallstudien mit realen Daten. Die Referenz-Engine erlaubt standardmäßig zwei automatische Rücksprünge zur Ideenfindung. Wir verwenden das System als auditierbares Gerüst für computergestützte Forschung, nicht als Beleg dafür, dass eine generierte wissenschaftliche Aussage korrekt ist.

## Entwicklungslinie {#development-line}

- Die datierte Entwicklungslinie ist noch nicht aufgeschrieben; das Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

- 2026-08-13 — Der technische Bericht wurde erstmals auf arXiv eingereicht.
- 2026-08-16 — v0.1.0 veröffentlichte öffentlich die Desktop-Workbench, den Terminal-Agenten und den Claude-Code-Skill.
- 2026-08-18 — v0.1.1 ergänzte eine release-weite Prüfung per SHA256SUMS.
- 2026-08-21 — Dies ist kein verifiziertes Release- oder Commit-Datum: Die offizielle Historie springt von 2026-08-20 auf 2026-08-22; v0.1.1 war zu diesem Zeitpunkt das jüngste getaggte Release.
- 2026-08-23 — v0.1.2 ergänzte Unterstützung für DeepSeek V4 Flash Vision und behob das Rendering der PDF-Prüfung.
- 2026-08-24 — v0.1.3 ergänzte Unterstützung für mehrsprachige Workspaces und Seiten.
- 2026-08-25 — v0.1.6 wurde mit Desktop-, Terminal- und Skill-Paketen veröffentlicht.
- 2026-08-28 — v0.2.0 lieferte Desktop-Pakete als Windows-Installer, macOS-ZIP und Linux-DEB aus.
- 2026-09-02 — v0.2.1 wurde zum neuesten verifizierten Release; die aktuelle README-Anleitung stellt die eigenständige CLI zugunsten der Desktop-App oder des Skills ein.

## So wird es verwendet {#how-to-use-this}

1. Lade das Desktop-Paket v0.2.1 für die Plattform herunter oder entpacke omnisci-skill.zip nach ~/.claude/skills. Prüfe die Release-Prüfsumme vor der Installation.
  — <https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.1>
2. Gib dem Desktop-Workspace oder dem installierten Skill einen Ordner mit Rohdaten und eine offene Forschungsrichtung. Nutze den lokalen Workspace, um das entstandene Laufprotokoll und die Artefakte zu prüfen.
  — <https://omni-scientist.github.io/>
3. Definiere Daten und offene Richtung in series.json für einen skriptbaren Lauf der Referenz-Engine. Führe agentic.py mit --stage run aus statt einer isolierten Stufe.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md>
4. Konfiguriere das Reasoning-Backbone und ein bildfähiges Wahrnehmungsmodell getrennt, wenn du die Referenz-Engine verwendest.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md>

## Bewährte Vorgehensweisen {#best-practices}

- Verwende --stage run für einen echten Engine-Lauf. Einzelstufen dienen dem Debugging und führen kein automatisches Zurückspringen aus.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md>
- Beginne mit einer offenen, falsifizierbaren Richtung und prüfe die Rohdaten als Evidenz, bevor du eine Analysemethode wählst.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/skill/omnisci/SKILL.md>
- Erfasse jede berichtete Zahl aus der stdout-Ausgabe des Skripts, verwende real abgerufene Referenzen und betrachte ein bestandenes numerisches Gate als Herkunftsnachweis statt als wissenschaftliche Validierung.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/skill/omnisci/SKILL.md>
- Prüfe heruntergeladene Release-Dateien vor der Installation gegen SHA256SUMS.
  — <https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.1>

## Dadurch abgelöst {#superseded-by-this}

- 2026-09-02 — Die Anleitung zur Installation der eigenständigen CLI aus der Linie v0.1.x ist für eine Neuinstallation veraltet: Die aktuelle README besagt, dass die Terminal-Edition in v0.2.1 eingestellt wurde.
- 2026-09-02 — v0.2.0 wurde durch v0.2.1 als neuestes verifiziertes Release abgelöst.

## Weiterhin unbekannt {#still-unknown}

- Der genaue Wortlaut und die beabsichtigte Aussage der Ankündigung vom 2026-08-21 sind nicht verfügbar, daher lässt sie sich nicht genauer einordnen als ein Verweis auf das offizielle Projekt.
- Die offizielle Website nennt Nachrichten nur auf Monatsebene (August), während GitHub die genaue Release-Chronologie enthält; GitHub ist die maßgebliche Quelle für Versionsdaten.
- Die Erstanbieter-Dokumentation weicht ab: Der Release-Text zu v0.2.1 erwähnt weiterhin einen Terminal-Agenten, doch die aktuelle README besagt, dass die eigenständige CLI eingestellt wurde, und die Assets von v0.2.1 enthalten nur Desktop-Pakete und den Skill.
- Es wurde kein Erstanbieter- oder unabhängig reproduzierbarer Betriebsbericht in vereinfachtem Chinesisch gefunden, der eine chinesischsprachige Praxisempfehlung stützen würde.
- Die Evaluationsergebnisse des technischen Berichts sind von den Autoren angegeben; eine unabhängige Replikation wurde hier nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://omni-scientist.github.io/ | OmniScientist: An Omni-Modal Omni-Discipline AI Scientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist | Omni-Scientist/OmniScientist repository and current README | 2026-09-07 |
| https://arxiv.org/abs/2608.13558 | OmniScientist: An Omni-Modal Omni-Discipline AI Scientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.0 | OmniScientist 0.1.0 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.1 | OmniScientist 0.1.1 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/commits/main | OmniScientist main-branch commit history | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.2 | OmniScientist 0.1.2 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.3 | OmniScientist 0.1.3 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.6 | OmniScientist 0.1.6 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.0 | OmniScientist 0.2.0 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.1 | OmniScientist 0.2.1 release | 2026-09-07 |
| https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md | OmniScientist Usage guide | 2026-09-07 |
| https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/skill/omnisci/SKILL.md | OmniScientist agent skill instructions | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:omniscientist`, Thread `omniscientist`, 0 datierte Ereignisse - → -.
- **Practical note:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Confidence:** mittel. Datierte Ablösungen oben sind maßgeblich für das, was veraltet ist.

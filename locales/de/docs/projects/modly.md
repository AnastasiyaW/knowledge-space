---
title: "Modly"
category: projects
date: 2026-03-20
tags: [modly, modly-development, project]
aliases: ["Modly"]
level: 3
source_sha256: 88849578927894f9003807ef17b681fb74abdfdb219680502df9005b96bb2a6c
translation: machine
translated_at: '2026-10-24'
---
# Modly {#modly}

**Entwicklungslinie:** `project:modly` · Thread `modly-development`  
**Letztes Ereignis:** 2026-03-20 · 1 datiertes Ereignis seit 2026-03-20 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Modly ist eine lokale Alternative zu cloudbasierten Image-to-3D-Werkzeugen wie Meshy für Kreative, die Modelle auf eigener Hardware betreiben.

- 3D-Mesh-Generierung aus einem Bild oder einem Text-Prompt.
- Erweiterungen für Modelle und Prozesse, darunter Hunyuan3D 2, TripoSG und Trellis.
- Desktop-App mit Node-Workflows, Mesh-Export und einer lokalen CLI.

## Entwicklungslinie {#development-line}

- **2026-03-20 — Verweis auf das GitHub-Repository von Modly.** Am 2026-03-20 verlinkte die Entwicklungslinie von Modly auf das öffentliche GitHub-Repository github.com/lightningpixel/modly. Der Link belegt einen datierten Repository-Verweis, ohne ein bestimmtes Release, einen Commit, ein Feature oder eine betriebliche Änderung zu benennen.

## Was sich geändert hat {#what-changed}

- 2026-03-20 — Modly wurde mit seinem öffentlichen GitHub-Repository erfasst; für genau den Funktionsumfang dieses Tages wurde kein Artefakt des Herstellers mit Datum abgerufen.
- 2026-03-26 — Modly Beta v0.2.1 überarbeitete das Erweiterungssystem, die Behandlung vertrauenswürdiger Erweiterungen und den Updater.
- 2026-04-03 — Modly Beta v0.3.0 verlagerte das Produkt in Richtung node-basierter Workflows und einer erweiterungszentrierten Models-Seite.
- 2026-04-21 — Modly Beta v0.3.2 ergänzte die headless Ausführung über `/workflow-runs` und eingebettetes Python.
- 2026-04-22 — Modly Beta v0.3.3 ergänzte einen Remesh-Workflow-Node.
- 2026-06-21 — Modly Beta v0.4.0 ergänzte die Agent-CLI, die Installation lokaler Erweiterungen, Arbeiten für Apple Silicon, Transformationssteuerungen und die Anzeige von Gaussian Splats.
- 2026-07-16 — Modly Beta v0.4.1 ergänzte Workflow-Iterations-Nodes, Audio-Prozessausgaben, einen Workflow-Browser und Paketierung für Apple Silicon.
- 2026-08-28 — Modly Beta v0.4.2 wurde zur neuesten getaggten Beta. Behoben wurden die Validierung von Erweiterungen und das Verhalten des Pickers, CLI-JSON-Argumente, UTF-8-Subprozess-I/O unter Windows sowie die Platzierung der Sammlung von Workflow-Läufen.

## Anwendung {#how-to-use-this}

Verwenden Sie ab dem 2026-03-20 das referenzierte GitHub-Repository als Ausgangspunkt für die quellcodebasierte Überprüfung von Modly. Leiten Sie Releases, Fähigkeiten oder Nutzungsanleitungen nicht allein aus diesem Link ab.

1. Prüfen Sie, ob Zielmodell und Plattform zum Rechner passen. Die offizielle Website empfiehlt eine NVIDIA-CUDA-GPU mit mindestens 6 GB VRAM. Laden Sie danach den aktuellen Beta-Installer herunter.
  — <https://modly3d.app/>
2. Installieren Sie eine offizielle Modell-Erweiterung über die Models-Seite mit „Install from GitHub“ und laden Sie anschließend deren Modellvariante herunter.
  — <https://github.com/lightningpixel/modly>
3. Erstellen Sie einen einfachen Graphen: Image → Generate Mesh → Add to Scene. Wählen Sie ihn in Generate aus und starten Sie ihn. Schlägt der Lauf fehl, prüfen Sie Settings, Logs und Errors.
  — <https://github.com/lightningpixel/modly>
4. Zeigen Sie eine Vorschau des Meshes an und exportieren Sie es als GLB, OBJ, STL oder PLY für das Ziel-DCC-Werkzeug, die Engine oder den Slicer.
  — <https://modly3d.app/>
5. Für die Automatisierung starten Sie die Desktop-App, führen `python tools/modly-cli/agent.py health` aus und prüfen die Modelle. Verwenden Sie danach `generate --image ... --output ...` und bewahren Sie die zurückgegebene Run-ID für Statusabfragen oder Abbrüche auf.
  — <https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md>

## Bewährte Vorgehensweisen {#best-practices}

- Beginnen Sie mit dem kleinsten verbundenen Workflow und prüfen Sie jede Kante, bevor Sie generieren. Behalten Sie die Mesh-Ansicht bei und lesen Sie das Fehler- und Log-Panel im Editor, statt nach einem fehlgeschlagenen Lauf den Graphen neu aufzubauen.
  — <https://github.com/lightningpixel/modly>
- Verwenden Sie ein sauberes, isoliertes Eingangsbild oder einen konkreten Prompt. Wählen Sie anschließend die installierte Modellvariante je nach Geschwindigkeit oder Detailtreue aus, statt anzunehmen, dass ein Modell für jede Aufgabe passt.
  — <https://modly3d.app/>
- Für skriptgesteuerte Nutzung verwenden Sie bevorzugt die kanonischen Befehle `health`, `model` und `workflow-run`. Behandeln Sie `/generate/*` und experimentelle ComfyUI-Hilfsfunktionen als Kompatibilitäts- beziehungsweise Experimentalpfade und nicht als stillen Fallback.
  — <https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md>
- Behandeln Sie die Desktop-Installer oder die Standard-Einrichtung von Erweiterungen nicht als Jetson-Unterstützung. Der Jetson-Leitfaden beschreibt einen nicht unterstützten Pfad, der einen Jetson-nativen PyTorch-Build, das Pinning von NumPy und eine Umgehung für die Hintergrundentfernung erfordert.
  — <https://github.com/lightningpixel/modly/blob/main/docs/running-on-jetson.md>

## Hierdurch abgelöst {#superseded-by-this}

- Der Workflow vor v0.3 mit Fokus auf die Modellseite wird ab dem 2026-04-03 durch die node-basierte Workflow- und Erweiterungsarchitektur abgelöst.
- Die alte Automatisierungsschnittstelle `/generate/*` dient nur noch der Kompatibilität. Kanonische Automatisierung ist der Workflow-Run-Vertrag, der mit der v0.4-Linie am 2026-06-21 eingeführt wurde.
- Modly Beta v0.4.1 ist nicht mehr die neueste getaggte Beta. v0.4.2 hat sie am 2026-08-28 abgelöst.

## Weiterhin unbekannt {#still-unknown}

- Kein abgerufener Release-Hinweis, kein Tag und kein archivierter Repository-Snapshot des Herstellers legt den genauen Funktionsumfang von Modly am 2026-03-20 fest. Spätere Releases werden daher als eigenständige Ereignisse geführt.
- Die Hardware-Empfehlungen des Herstellers bilden noch keine einheitliche Unterstützungsmatrix. Die Produktseite empfiehlt NVIDIA CUDA mit 6 GB VRAM, das Repository führt Apple Silicon unter macOS auf, und der Jetson-Leitfaden beschreibt ausdrücklich eine nicht unterstützte Umgehung.
- Eine gezielte Suche nach chinesischsprachigen Quellen fand Sekundärberichterstattung, aber keine offizielle chinesischsprachige Dokumentation oder Release-Aufzeichnung zu Modly.

## Quellen {#sources}

| Quelle | Titel | abgerufen |
|---|---|---|
| https://github.com/lightningpixel/modly | GitHub - lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/releases | Releases · lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/releases/tag/v0.2.1 | Release Modly Beta v0.2.1 · lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/tags | Tags · lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md | Modly CLI SKILL.md | 2026-09-05 |
| https://modly3d.app/ | Modly — Free Local AI 3D Model Generator | 2026-09-05 |
| https://github.com/lightningpixel/modly/blob/main/docs/running-on-jetson.md | Running Modly headless on an NVIDIA Jetson | 2026-09-05 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:modly`, Thread `modly-development`, 1 datiertes Ereignis vom 2026-03-20 bis 2026-03-20.
- **Praktischer Hinweis:** Verwenden Sie ab dem 2026-03-20 das referenzierte GitHub-Repository als Ausgangspunkt für die quellcodebasierte Überprüfung von Modly. Leiten Sie Releases, Fähigkeiten oder Nutzungsanleitungen nicht allein aus diesem Link ab.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Ablösungen oben als maßgeblich.

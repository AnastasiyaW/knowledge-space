---
title: "ComfyUI Setup Manager"
category: projects
date: 2026-07-23
tags: [comfyui-setup-manager, comfyui-setup-manager-development, comfyui_setup_manager, project]
aliases: ["ComfyUI Setup Manager"]
level: 2
source_sha256: 9adf979f8cb1f960ef8ac2b9b6c88314f648ad8c148b03a9c3e15ec6c237509e
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Setup Manager {#comfyui-setup-manager}

**Entwicklungslinie:** `project:comfyui-setup-manager` · Thread `comfyui-setup-manager-development`  
**Letztes Ereignis:** 2026-07-23 · 1 datiertes seit 2026-07-23 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ComfyUI Setup Manager ist eine Terminal-TUI und CLI zur Verwaltung isolierter ComfyUI-Installationen.

- Installationslebenszyklus: installiert, startet, prüft, aktualisiert, repariert, exportiert und rekonstruiert ComfyUI-Checkouts.
- Umgebungsisolation: trennt Checkout, virtuelle Umgebung und Custom Nodes für jede Installation.
- Gemeinsame Asset-Bibliotheken: teilt Modell- und Workflow-Verzeichnisse über Checkouts hinweg, um doppelte Dateien zu vermeiden.
- Setup-Profile: exportiert und baut Installationen anhand portabler `.comfyuisetup`-Rekonstruktionsdateien neu auf.

Aktuelle README-Version: 0.8.8.

Einsetzbar für reproduzierbare Wartung mehrerer ComfyUI-Installationen, nicht als Ersatz für ComfyUI Desktop und nicht als Garantie, dass inkompatible Nodes nebeneinander funktionieren.

## Entwicklungslinie {#development-line}

- **2026-07-23 — Das Repository von ComfyUI Setup Manager wurde öffentlich referenziert.** Am 2026-07-23 verlinkte eine öffentliche Referenz auf das GitHub-Repository von ComfyUI Setup Manager. Dies belegt einen datierten öffentlichen Verweis auf das Projekt, begründet aber allein weder ein Release, eine Funktionsänderung noch Repository-Aktivität.

## Was sich geändert hat {#what-changed}

2026-07-23 — ComfyUI Setup Manager erschien als eigenständiges GitHub-Projekt zur Rekonstruktion und Wartung von ComfyUI-Installationen; das verlinkte Repository steht nun bei Version 0.8.8.

## So wird es verwendet {#how-to-use-this}

Stand 2026-07-23 sollte das Repository beim Testen von ComfyUI-Tooling geprüft werden; seine Funktionen und seine Sicherheit sind nicht verifiziert.

1. Voraussetzungen prüfen: Python 3.10+, Git, Internetzugang und Schreibrechte; unter Windows WinGet prüfen, falls Python oder Git fehlen könnten.
  — <https://github.com/badgids/comfyui-setup-manager/blob/main/docs/getting-started.md>
2. Mit `install.ps1` unter Windows, `install.cmd` in der Eingabeaufforderung oder `./install.sh` unter Linux, WSL2 und macOS installieren.
  — <https://github.com/badgids/comfyui-setup-manager>
3. `./comfyui-setup-manager` ausführen, Setup & Install auswählen, ein Profil wählen und die Installation prüfen; CLI-Entsprechung: `install run --profile vanilla-comfyui --target /path/to/ComfyUI --repository-mode official`.
  — <https://github.com/badgids/comfyui-setup-manager/blob/main/docs/getting-started.md>
4. Vor dem Anlegen mehrerer Installationen ein externes Modellverzeichnis und ein Workflow-Verzeichnis konfigurieren und diese dann auf jeden verwalteten Checkout anwenden.
  — <https://github.com/badgids/comfyui-setup-manager>
5. Vor einem Update `updates check` ausführen; `updates run --strategy safe` erst verwenden, nachdem der Preflight-Bericht geprüft wurde.
  — <https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/automation-and-agents.md>

## Bewährte Vorgehensweisen {#best-practices}

- Einen exakten `.comfyuisetup`-Export als Rekonstruktionsmanifest behandeln, nicht als Backup von Modellen, virtuellen Umgebungen oder dem gesamten Checkout; vor der Wiederverwendung auf einem anderen Rechner Python, Beschleuniger und PyTorch-ABI prüfen.
  — <https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/setup-profiles.md>
- Eine gemeinsame externe Modell- und Workflow-Bibliothek nutzen, um große Checkpoints nicht über stabile, experimentelle und Entwicklungsinstallationen hinweg zu duplizieren.
  — <https://github.com/badgids/comfyui-setup-manager>
- Für unbeaufsichtigten Einsatz JSON- oder YAML-Ausgabe anfordern, vor jeder Änderung einen Plan erstellen, Exit-Codes auswerten und die TUI nicht parsen.
  — <https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/automation-and-agents.md>
- Mit einer unkritischen Installation beginnen: echte Inkompatibilitäten bei Custom-Node-Anforderungen können weiterhin getrennte ComfyUI-Installationen erforderlich machen.
  — <https://www.reddit.com/r/comfyui/comments/1uzgm6o/i_built_a_setup_manager_because_backing_up_entire/>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Keine datierte Erstveröffentlichung oder kein Commit aus dem Projekt selbst belegt, was genau am 2026-07-23 geändert wurde; spätere Funktionen lassen sich ohne Nachweis nicht diesem Datum zuordnen.
- Die Release Notes dokumentieren die Funktionsumfänge von 0.8.0 bis 0.8.7, nennen aber keine Veröffentlichungsdaten.
- Das Projekt-Repository beschreibt Version 0.8.8, die Release-Notes-Seite liefert jedoch keinen datierten Nachweis für ein Release 0.8.8.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/badgids/comfyui-setup-manager | ComfyUI Setup Manager README | 2026-09-05 |
| https://github.com/badgids/comfyui-setup-manager/blob/main/docs/getting-started.md | Getting started | 2026-09-05 |
| https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/automation-and-agents.md | Automation and AI agent use | 2026-09-05 |
| https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/setup-profiles.md | Portable setup profiles | 2026-09-05 |
| https://github.com/badgids/comfyui-setup-manager/blob/main/RELEASE_NOTES.md | Release notes | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1uzgm6o/i_built_a_setup_manager_because_backing_up_entire/ | I built a setup manager because backing up entire ComfyUI installs was getting ridiculous | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-setup-manager`, thread `comfyui-setup-manager-development`, 1 dated events 2026-07-23 → 2026-07-23.
- **Practical note:** As of 2026-07-23, evaluate the repository when testing ComfyUI setup tooling; its capabilities and safety remain unverified.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.

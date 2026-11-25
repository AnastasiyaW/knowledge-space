---
title: "ComfyUI Desktop"
category: projects
date: 2026-01-06
tags: [comfyui-desktop, project]
aliases: ["ComfyUI Desktop"]
level: 3
source_sha256: b8856925ec583ac8cc82309d79f080a16d6e526a8ca05f9375bfaa270b50d1e0
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Desktop {#comfyui-desktop}

**Entwicklungslinie:** `project:comfyui-desktop` · Thread `comfyui-desktop`  
**Letztes Ereignis:** 2026-01-06 · 2 datierte Ereignisse seit 2024-11-27 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

ComfyUI Desktop, inzwischen abgelöst durch Comfy Desktop, ist ein lokaler Launcher für Praktiker, die getrennte ComfyUI-Umgebungen benötigen, statt eine einzige manuelle Python-Installation zu pflegen.

- Instanzen: Erstellt, startet und verwaltet unabhängige ComfyUI-Instanzen.
- Isolation: Hält Version, Custom Nodes, Einstellungen und Python-Umgebung jeder Instanz getrennt.
- Betrieb: Unterstützt Vorlagen, Migration aus Legacy- oder bestehenden Installationen, Update-Kanäle, Snapshots und Rollback.

## Entwicklungslinie {#development-line}

- **2024-11-27 — ComfyUI Desktop wurde als Open-Source-Projekt verfügbar.** Am 2024-11-27 machte ComfyUI seine Desktop-Anwendung als Open-Source-Projekt verfügbar. Dies markiert einen öffentlichen Meilenstein in der Produktlinie. Die Veröffentlichungsunterlagen lassen den genauen anfänglichen Funktionsumfang, die unterstützten Plattformen und die Release-Details aus.
- **2026-01-06 — ComfyUI hat offizielle Unterstützung für AMD ROCm ergänzt.** Am 2026-01-06 kündigte ComfyUI offizielle Unterstützung für AMD ROCm an. Dies ist ein Update zur Plattformkompatibilität für die Desktop-Linie. Die Ankündigung nennt keine genauen Desktop-Versionen, Betriebssysteme, Hardware oder Setup-Anforderungen.

## Was sich geändert hat {#what-changed}

Entwicklungslinie von ComfyUI Desktop:

- 2024-11-27 — v1 Desktop wurde als Open Source veröffentlicht. Den detaillierten Funktionsumfang aus dem ursprünglichen Launch-Artikel konnten wir heute nicht erneut einsehen.
- 2026-01-06 — Windows Desktop v0.7.0 ergänzte offizielle Unterstützung für AMD ROCm; die Installation sollte ROCm automatisch auswählen. Das Release verwendete ROCm 7.1.1 und empfahl dessen Preview-Treiber.
- Heute gefunden (2026-09-04) — Die Dokumentation beschreibt den gepflegten Nachfolger als Comfy Desktop: einen Manager für mehrere Installationen statt der bisherigen Einzelinstallations-App. Er kann Legacy-Workflows, Nodes, Modelle, Eingaben, Ausgaben und Einstellungen in eine neue, eigenständige Umgebung migrieren.
- Heute gefunden (2026-09-04) — Das alte Repository Comfy-Org/desktop ist archiviert und verweist auf Comfy-Org/Comfy-Desktop.

## Verwendung {#how-to-use-this}

Ab 2024-11-27 können Praktiker ComfyUI Desktop anhand des öffentlichen Quell-Repositorys und der Benutzerhandbuch-Materialien evaluieren; ab 2026-01-06 sollten AMD-Nutzer bei der Bewertung eines Desktop-Deployments zusätzlich die offiziellen Hinweise zur ROCm-Unterstützung prüfen.

1. Prüfen Sie vor der Installation die dokumentierte Plattform und Kapazität: Windows 10+ oder macOS 13+ auf Apple Silicon, mit mindestens 4,85 GB pro eigenständiger Instanz und 8 GB RAM.
  — <https://docs.comfy.org/installation/desktop/overview>
2. Führen Sie unter Windows die heruntergeladene .exe aus, starten Sie Comfy Desktop und erstellen Sie die erste Installation über den Begrüßungsbildschirm.
  — <https://docs.comfy.org/installation/desktop/windows>
3. Öffnen Sie unter macOS mit Apple Silicon die .dmg, ziehen Sie Comfy Desktop in den Ordner Programme und starten Sie die App.
  — <https://docs.comfy.org/installation/desktop/macos>
4. Erstellen Sie im Chooser eine benannte Standalone-Instanz auf einer SSD und wählen Sie nach Abschluss der Einrichtung eine Workflow-Vorlage aus.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
5. Wenn eine bestehende Portable-, Git- oder Legacy-Desktop-Installation bereits Arbeitsstände enthält, fügen Sie sie hinzu oder migrieren Sie sie, statt Modelle und Workflows von Hand neu aufzubauen; prüfen Sie anschließend Workflows, Nodes, Modelle und die übernommene URL.
  — <https://docs.comfy.org/installation/desktop/usage/migrate>
6. Verwenden Sie für den normalen Betrieb unter Manage → Update den Kanal Stable; wählen Sie bewusst Latest on GitHub, wenn ein Workflow die neuesten Core-Commits benötigt.
  — <https://docs.comfy.org/installation/desktop/usage/manage>

## Bewährte Praktiken {#best-practices}

- Halten Sie inkompatible Projekte in getrennten Standalone-Instanzen, damit sich ihre Python-Umgebungen, ComfyUI-Revisionen und Custom Nodes nicht gegenseitig beeinträchtigen.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
- Verwenden Sie standardmäßig den Update-Kanal Stable; Latest on GitHub ist für gezieltes Testen neuerer Commits gedacht.
  — <https://docs.comfy.org/installation/desktop/usage/manage>
- Erstellen Sie vor dem Hinzufügen eines Nodes oder dem Aktualisieren eines funktionierenden Stacks einen beschrifteten manuellen Snapshot; Snapshots erfassen den ComfyUI-Commit, die Node-Versionen und pip-Pakete und können den vorherigen Zustand wiederherstellen.
  — <https://docs.comfy.org/installation/desktop/usage/snapshots>
- Belassen Sie ComfyUI-Manager auf der empfohlenen Sicherheitsstufe Standard: Sie erlaubt registrierte Node-Pakete und blockiert beliebige Git-Quellen.
  — <https://docs.comfy.org/installation/desktop/usage/manage>
- Wenn ein Custom Node den Start oder die Oberfläche beeinträchtigt, deaktivieren Sie zuerst alle Custom Nodes und grenzen Sie dann die Menge durch Halbierung ein; sichern Sie custom_nodes, bevor Sie manuell halbieren.
  — <https://docs.comfy.org/troubleshooting/custom-node-issues>

## Hierdurch überholt {#superseded-by-this}

- Legacy-Anleitung zur Einzelinstallation von ComfyUI Desktop vom 2024-11-27: Ersetzen Sie sie durch das aktuelle Modell mit mehreren Instanzen in Comfy Desktop und migrieren Sie, statt die alte Installation zu überschreiben.
- Anleitung für Windows Desktop vor dem 2026-01-06, die von reiner NVIDIA-Hardware ausgeht: v0.7.0 hat die offizielle Unterstützung von AMD ROCm unter Windows für unterstützte Radeon-GPUs und Ryzen-AI-Prozessoren eingeführt.
- Comfy-Org/desktop als aktives Quell-Repository ab 2026-06-26: Es ist archiviert und ausdrücklich durch Comfy-Org/Comfy-Desktop ersetzt.
- Anleitung vom 2026-09-04, dass Desktop stets dem neuesten ComfyUI-Commit entspricht: Stable ist der Standardkanal; Latest muss bewusst ausgewählt werden.

## Weiterhin ungeklärt {#still-unknown}

- Der Launch-Artikel von 2024 wurde beim Abruf nicht angezeigt, daher ist der genaue Funktionsumfang von v1 über das datierte Open-Source-Ereignis hinaus nicht unabhängig verifiziert.
- Die aktuelle englische Dokumentation besagt, dass Linux nur als Quellcode vorliegt und kein offizieller Installer existiert, während das gepflegte Repository Comfy-Desktop die Installation über .deb und AppImage beschreibt. Diesen Widerspruch sollte man anhand des Release-Artefakts klären, bevor man sich für Linux Desktop entscheidet.
- Die englische Dokumentation beschreibt inzwischen den Nachfolger mit mehreren Instanzen, während die chinesische Windows-Seite weiterhin die frühere Einzelinstallations-Beta und den reinen NVIDIA-Pfad beschreibt. Die öffentlichen Quellen nennen kein Datum für den Stichtag der Lokalisierung oder Migration.
- Die AMD-Ankündigung nennt unterstützte Radeon-GPUs und Ryzen-AI-Prozessoren, enthält jedoch keine vollständige aktuelle Hardwarematrix für Desktop; die genaue Kombination aus GPU und Treiber sollte bei der Installation überprüft werden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://blog.comfy.org/open-sourcing-v1-desktop/ | Open Sourcing V1 Desktop | 2026-09-04 |
| https://blog.comfy.org/p/official-amd-rocm-support-arrives | Offizielle AMD-ROCm-Unterstützung für ComfyUI Desktop unter Windows verfügbar | 2026-09-04 |
| https://github.com/Comfy-Org/desktop | Comfy-Org/desktop — archiviert und ersetzt durch Comfy-Org/Comfy-Desktop | 2026-09-04 |
| https://github.com/Comfy-Org/Comfy-Desktop | Comfy-Org/Comfy-Desktop — Die Desktop-App für ComfyUI | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/overview | Comfy Desktop: Überblick | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/windows | Comfy Desktop für Windows | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/macos | Comfy Desktop für macOS | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/instance-management | Instanzverwaltung | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/manage | Installationen verwalten | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/snapshots | Snapshots | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/migrate | Migration von Legacy Desktop | 2026-09-04 |
| https://docs.comfy.org/troubleshooting/custom-node-issues | Fehlersuche und Behebung von ComfyUI-Problemen | 2026-09-04 |
| https://docs.comfy.org/zh/installation/desktop/windows | Windows Desktop — ComfyUI (Chinesisch) | 2026-09-04 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:comfyui-desktop`, Thread `comfyui-desktop`, 2 datierte Ereignisse vom 2024-11-27 bis 2026-01-06.
- **Praktischer Hinweis:** Ab 2024-11-27 können Praktiker ComfyUI Desktop anhand des öffentlichen Quell-Repositorys und der Benutzerhandbuch-Materialien evaluieren; ab 2026-01-06 sollten AMD-Nutzer bei der Bewertung eines Desktop-Deployments zusätzlich die offiziellen Hinweise zur ROCm-Unterstützung prüfen.
- **Konfidenz:** mittel. Die datierten Überholungsangaben oben sind maßgeblich dafür, was veraltet ist.

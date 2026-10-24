---
title: "Comfy Desktop — ComfyUI"
category: projects

tags: [comfy-desktop, comfyui, project]
aliases: ["Comfy Desktop"]
level: 3
source_sha256: f8b811a7e4f69572e233ce22abc00f654a1696a4b762766871dd372b251c7835
translation: machine
translated_at: '2026-10-24'
---
# Comfy Desktop — ComfyUI {#comfy-desktop-comfyui}

**Entwicklungslinie:** `project:comfy-desktop` · Thread `comfyui`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

Comfy Desktop ist ein offizieller Launcher und Manager für mehrere Instanzen für Anwender, die lokales ComfyUI nutzen möchten, ohne jede Python-Umgebung separat pflegen zu müssen.

- Instanzverwaltung: installiert, startet, aktualisiert und verfolgt unabhängige ComfyUI-Instanzen.
- Umgebungsisolation: trennt Versionen, Custom Nodes und Einstellungen, erlaubt aber gemeinsamen Modellspeicher.
- Snapshots: erstellt Snapshots für Rollbacks und reproduzierbare Instanz-Setups.

Die aktuelle Dokumentation unterstützt Windows 10+ sowie macOS 13+ auf Apple Silicon, mit 4,85 GB pro eigenständiger Installation und mindestens 8 GB RAM. Die Linux-Hinweise in der offiziellen Dokumentation und im Repository widersprechen sich. Wir nutzen es, um experimentelle und produktive Node-Stacks zu isolieren. Man sollte nicht davon ausgehen, dass eine verfolgte Legacy-Installation Snapshot-Unterstützung hat.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; das Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

- 2026-06-04 — Comfy Desktop — ein neu aufgebauter Manager für mehrere Instanzen begann einen gestaffelten Rollout und ersetzt das ältere Modell mit gebündeltem Desktop.
- 2026-06-09 — Comfy Desktop — der erfasste Link verweist auf einen Originalbeitrag, der als 8. Juni angezeigt wird; er beschreibt eine neu aufgebaute App, die bestehende Workflows, Custom Nodes, Modelle und Einstellungen beibehält.
- 2026-06-16 — Comfy Desktop — die Dokumentation zu Snapshots wurde korrigiert: Snapshots waren damals nur für Standalone verfügbar, nicht für verfolgte Portable- oder Git-Installationen.
- 2026-06-23 — Comfy Desktop — die Release Notes von ComfyUI v0.26.0 aktualisierten den Link auf das neue Desktop-Repository und die Produktbezeichnungen zu „Comfy Desktop“.
- 2026-06-26 — Comfy Desktop — das Legacy-Repository `desktop` wurde archiviert und ausdrücklich durch `Comfy-Desktop` ersetzt.
- 2026-08-28 — Comfy Desktop — v1.0.46 wurde im Stable-Kanal veröffentlicht; die beobachtete Release-Seite markierte sie als Latest.
- 2026-09-03 — Comfy Desktop — v1.0.47-rc.1 wurde als RC-Vorabversion veröffentlicht, nicht als Standard-Stable-Kanal.

## So nutzt man es {#how-to-use-this}

1. 1. Prüfe die dokumentierten Anforderungen an Plattform und Speicher und lade anschließend den unterstützten Installationspfad für Windows oder macOS herunter.
  — <https://docs.comfy.org/installation/desktop/overview>
2. 2. Erstelle eine Standalone-Instanz für ein neues, isoliertes Setup oder füge eine bestehende Portable-/Git-Installation hinzu, wenn deren aktuelle Umgebung unverändert bleiben muss.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
3. 3. Starte die bereitgestellte Instanz, wähle eine Workflow-Vorlage und verwende Manage, um Pfade, Startargumente und instanzspezifische Konfiguration festzulegen.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
4. 4. Erstelle vor einem Update oder einer Änderung an Custom Nodes einen Snapshot oder prüfe einen vorhandenen; verwende Stable, sofern du nicht bewusst Änderungen am Master-Branch testest.
  — <https://docs.comfy.org/installation/desktop/usage/manage>

## Bewährte Praktiken {#best-practices}

- Verwende für einen experimentellen Node- oder Abhängigkeits-Stack eine separate Standalone-Instanz; Snapshots erfassen den ComfyUI-Commit, die Versionen der Custom Nodes und die Python-Pakete.
  — <https://docs.comfy.org/installation/desktop/usage/snapshots>
- Halte den Update-Kanal der Instanz standardmäßig auf Stable; Latest auf GitHub ist für bewusstes Testen gedacht.
  — <https://docs.comfy.org/installation/desktop/usage/manage>
- Behandle verfolgte Portable- und Git-Installationen als manuell aktualisiert und ohne Snapshot-Unterstützung.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
- Belasse ComfyUI-Manager auf der Standard-Richtlinie; erlaube nicht registrierte Node-Quellen nur in einer bewusst rein lokalen Umgebung.
  — <https://docs.comfy.org/installation/desktop/usage/manage>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-06-04 — Desktop ist nicht mehr eine einzelne gebündelte ComfyUI-Installation; das neu aufgebaute Produkt verwaltet unabhängig konfigurierte Instanzen.
- 2026-06-16 — Verfolgte Portable- oder Git-Instanzen unterstützen keine Snapshots; der dokumentierte Umfang beschränkt sich auf Standalone.
- 2026-06-26 — Behandle `Comfy-Org/desktop` als historischen Beleg, nicht als aktuelles Quell-Repository; dessen eigene README verweist auf `Comfy-Org/Comfy-Desktop`.

## Weiterhin unbekannt {#still-unknown}

- Der direkte Abruf der X-URL lieferte HTTP 403. Wir haben ihren vollständigen Text oder Medieninhalte von X nicht erfasst; die Korrektur vom 8. Juni stützt sich auf eine zugängliche Sekundärdarstellung.
- Das Erfassungsdatum ist 2026-06-09, während die zugängliche Darstellung den Beitrag mit 8. Juni bezeichnet. Die Normalisierung der Zeitzone der Quelle ist nicht verifiziert.
- Erstpartei-Quellen widersprechen sich bei Linux: Die offizielle Dokumentation nennt keinen Installer, während die README des Comfy-Desktop-Repositorys Linux-`.deb`- und AppImage-Pfade bewirbt. Prüfe ein aktuell herunterladbares Artefakt, bevor du Linux als unterstützt oder nicht unterstützt einstufst.
- In diesem Durchgang wurde kein Desktop-Leitfaden in vereinfachtem Chinesisch von Erstpartei-Quellen verifiziert; sekundäre chinesische Spiegel wurden für operative Aussagen nicht verwendet.
- Das Legacy-Repository nennt Comfy-Desktop ausdrücklich als Nachfolger, es handelt sich also nicht um zwei unabhängige Themen. Anleitungen und Binärdateien vor dem Übergang benötigen weiterhin eine separate Zuordnung.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://x.com/ComfyUI/status/2064093003590111314 | ComfyUI status 2064093003590111314 | 2026-09-07 |
| https://easyvibecoding.app/curated/1843-comfy-desktop-launches-multi-instance-management | Comfy Desktop 推出實現多執行個體管理 — EasyVibeCoding | 2026-09-07 |
| https://www.reddit.com/r/comfyui/comments/1tx4qn7/announcing_comfy_desktop_one_app_for_every_comfy/ | Announcing Comfy Desktop: One App for every Comfy | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/overview | Comfy Desktop Overview - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/overview | Using Comfy Desktop - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/instance-management | Instance Management - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/snapshots | Snapshots - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/manage | Managing Installations - ComfyUI | 2026-09-07 |
| https://github.com/Comfy-Org/docs/discussions/1141 | installation/desktop/usage/instance-management #1141 | 2026-09-07 |
| https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.26.0 | Release v0.26.0 · Comfy-Org/ComfyUI | 2026-09-07 |
| https://github.com/Comfy-Org/desktop | Comfy-Org/desktop: archived and superseded by Comfy-Desktop | 2026-09-07 |
| https://github.com/Comfy-Org/Comfy-Desktop | Comfy-Org/Comfy-Desktop | 2026-09-07 |
| https://github.com/Comfy-Org/Comfy-Desktop/releases | Releases · Comfy-Org/Comfy-Desktop | 2026-09-07 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:comfy-desktop`, Thread `comfyui`, 0 datierte Ereignisse - → -.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

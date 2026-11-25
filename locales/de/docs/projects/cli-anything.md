---
title: "CLI-Anything"
category: projects
date: 2026-03-11
tags: [agent_tools, cli-anything, cli-anything-development, project]
aliases: ["CLI-Anything"]
level: 3
source_sha256: b69f20aa5b45a099a4555be0c84671e95c53cafd07e2677916a5b6011060fc3a
translation: machine
translated_at: '2026-10-24'
---
# CLI-Anything {#cli-anything}

**Entwicklungsstrang:** `project:cli-anything` · Thread `cli-anything-development`  
**Letztes Ereignis:** 2026-03-11 · 1 datiertes Ereignis seit 2026-03-11 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

CLI-Anything ist ein HKUDS-Projekt für zwei Aufgaben: die Installation einer bestehenden CLI über CLI-Hub oder die Erzeugung eines Python/Click-Harness für Open-Source-Software.

- JSON-Ausgabe für maschinelle Verarbeitung
- REPL für interaktive Sitzungen
- Undo und Redo für das Zurücksetzen des Zustands
- Tests zur Validierung des Harness
- SKILL.md für die Agenten-Integration

CLI-Hub benötigt Python 3.10+.

Für ein bestehendes Tool CLI-Hub verwenden. Den Generator ausführen, wenn kein Harness vorhanden ist und die Zielanwendung lokal getestet werden kann.

## Entwicklungsstrang {#development-line}

- **2026-03-11 — CLI-Anything-GitHub-Repository im agent_tools-Thread aufgetaucht.** Am 2026-03-11 wurde das GitHub-Repository HKUDS/CLI-Anything im agent_tools-Thread verlinkt. Der Link liefert einen datierten Verweis auf die geprüfte Quelle. Die Belege zeigen kein Release, keine Version, keine Funktionsänderung und keinen Meilenstein.

## Was sich geändert hat {#what-changed}

- **2026-03-11** — Zoom-Harness als elfte unterstützte Anwendung hinzugefügt. Ein separater Beitrag vom selben Tag meldete 4,4k+ GitHub-Sterne, 9 Anwendungen und 1 436 Tests; diese frühen Zählwerte nicht als dauerhaften Katalog oder aktuelle Kennzahl behandeln.
- **2026-03-12** — Codex-Integration hinzugefügt.
- **2026-03-16** — Phase 6.5 hinzugefügt, um für jedes Harness automatisch SKILL.md zu erzeugen.
- **2026-03-17** — CLI-Hub gestartet, um fertige CLIs zu suchen, zu installieren und auszuführen.
- **2026-03-30** — v0.2.0 hat HARNESS.md um progressive Offenlegung herum überarbeitet.
- **2026-04-18** — SKILL.md-Dateien im Root-Verzeichnis skills/ zusammengeführt.
- **2026-04-24** — v0.3.0 hat neue Harness-Tools hinzugefügt, darunter CloudCompare, IntelWatch, VideoCaptioner und Slay the Spire II.
- **2026-06-02** — Paper „CLI-Anything: Towards Agent-Native Computer Use" veröffentlicht, das den Wandel von der GUI-Automatisierung per Bildschirm hin zu strukturierten CLIs beschreibt.
- **2026-06-25** — v0.4.0 hat CLI-Matrix, 30 neue CLIs, 17 Fehlerbehebungen und vier Sicherheitshärtungen hinzugefügt.

## Wie dies zu verwenden ist {#how-to-use-this}

Stand 2026-03-11 sollten Praktiker CLI-Anything als Projekt behandeln, das vor der Einführung einer Bewertung auf Quellcode-Ebene bedarf; der datierte Link allein belegt keine verifizierte Fähigkeit, kein Release und keine Kompatibilitätsaussage.

1. Für ein bestehendes Tool CLI-Hub mit `pip install cli-anything-hub` installieren. Mit `cli-hub search <query>` suchen, mit `cli-hub info <name>` prüfen, mit `cli-hub install <name>` installieren und mit `cli-hub launch <name> --help` ausführen.
  — <https://clianything.cc/docs.html>
2. Für Software, die im Katalog fehlt, Python 3.10+, Quellcode oder ein zugängliches Repository und einen unterstützten Coding-Agenten bereitstellen. In Claude Code den Marketplace verbinden und `/cli-anything <path-or-repo>` ausführen.
  — <https://github.com/HKUDS/CLI-Anything>
3. Nach der Generierung das Harness aus seinem Verzeichnis agent-harness mit `pip install -e .` installieren. Befehle mit `--help` prüfen und für maschinelle Verarbeitung `--json` verwenden.
  — <https://github.com/HKUDS/CLI-Anything>

## Bewährte Praktiken {#best-practices}

- Zuerst in CLI-Hub nach einer bestehenden CLI suchen; den Generator nur verwenden, wenn dem Katalog das benötigte Harness fehlt.
  — <https://github.com/HKUDS/CLI-Anything>
- Eine generierte CLI nach einem einzigen Durchlauf nicht als vollständig betrachten: für erkannte Lücken `refine` ausführen, danach validieren und vor dem produktiven Einsatz testen.
  — <https://github.com/HKUDS/CLI-Anything>
- Die Zielanwendung installieren und testen: Ein Harness kann GIMP, Blender, LibreOffice oder andere Upstream-Software voraussetzen.
  — <https://github.com/HKUDS/CLI-Anything>
- In der Automatisierung `--json` und Exit-Codes verwenden, statt Textausgaben zu parsen.
  — <https://clianything.cc/docs.html>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-03-11: Die frühe Beschreibung des Projekts mit 9 Anwendungen und 1 436 Tests ist überholt. Die offizielle Projekthistorie verzeichnet für dieses Datum Zoom als elftes Harness, und v0.4.0 hat später weitere 30 CLIs hinzugefügt.
- 2026-03-11: Für jede Anfrage eine CLI zu generieren ist überholt. Wir prüfen nun zuerst CLI-Hub, um ein bestehendes Tool aus dem Katalog zu finden und zu installieren.
- 2026-03-11: Das Fehlen eines Codex-Workflows ist seit 2026-03-12 mit der integrierten Unterstützung überholt.

## Weiterhin unbekannt {#still-unknown}

- Das offizielle Projektprotokoll bestätigt das Ereignis vom 2026-03-11, enthält jedoch keinen unveränderlichen Snapshot des Repositorys zum Zeitpunkt der Veröffentlichung. Frühe Zählwerte aus der Sekundärquelle dienen nur als Ereigniskontext.
- Das Ausgabeschema unterstützt die Felder event_findings und new_events nicht; what_changed speichert deren Inhalte.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/HKUDS/CLI-Anything | HKUDS/CLI-Anything-Repository und aktuelle README | 2026-09-05 |
| https://clianything.cc/docs.html | CLI-Anything-Hub-Dokumentation | 2026-09-05 |
| https://github.com/HKUDS/CLI-Anything/releases/tag/v0.4.0 | CLI-Anything v0.4.0 Release | 2026-09-05 |
| https://github.com/HKUDS/CLI-Anything/releases | CLI-Anything-Releases | 2026-09-05 |
| https://arxiv.org/abs/2606.03854 | CLI-Anything: Towards Agent-Native Computer Use | 2026-09-05 |
| https://linux.do/t/topic/1737269?tl=en | CLI-Anything-Diskussion zu GitHub Trending | 2026-09-05 |

## Agenten-Brief {#agent-brief}

- **Gegenstand:** `project:cli-anything`, Thread `cli-anything-development`, 1 datiertes Ereignis vom 2026-03-11 → 2026-03-11.
- **Praxishinweis:** Stand 2026-03-11 sollten Praktiker CLI-Anything als Projekt behandeln, das vor der Einführung einer Bewertung auf Quellcode-Ebene bedarf; der datierte Link allein belegt keine verifizierte Fähigkeit, kein Release und keine Kompatibilitätsaussage.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich für das, was überholt ist.

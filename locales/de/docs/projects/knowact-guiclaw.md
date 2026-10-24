---
title: "KnowAct-GUIClaw"
category: projects
date: 2026-07-18
tags: [knowact-guiclaw, project]
aliases: ["KnowAct-GUIClaw"]
level: 2
source_sha256: 3a656cbdd112b0aacc462b62c7bd4b5e662a3595d1a488601d15cd7a6a998754
translation: machine
translated_at: '2026-10-24'
---
# KnowAct-GUIClaw {#knowact-guiclaw}

**Entwicklungslinie:** `project:knowact-guiclaw` · Thread `knowact-guiclaw`  
**Letztes Ereignis:** 2026-07-18 · 1 datiertes Ereignis seit 2026-07-18 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

KnowAct-GUIClaw ist ein Host und GUI-Executor im Stil von OpenClaw für Entwickler, die langfristige Arbeitsabläufe über Android, iOS, HarmonyOS und Desktop automatisieren.

- Leitet Aufgaben weiter und überträgt typisierte Werte zwischen Apps.
- Ruft Erfahrungsspeicher ab.
- Validiert wiederverwendbare mobile Shortcuts und Skills.

## Entwicklungslinie {#development-line}

- **2026-07-18 — Projektseite von KnowAct-GUIClaw und Quell-Repository verlinkt.** Am 18. Juli 2026 verlinkte eine öffentliche Nachricht die Projektseite von KnowAct-GUIClaw und das GitHub-Repository von KnowAct. Dadurch entsteht eine datierte öffentliche Verbindung zwischen dem GUIClaw-Projekt und der KnowAct-Codebasis, belegt jedoch keinen bestimmten Release, kein bestimmtes Feature und keinen konkreten Implementierungsmeilenstein.

## Was sich geändert hat {#what-changed}

2026-07-18 — An diesem Datum ist kein Release, keine Revision des Papers und keine Änderung am Repository von Erstanbietern dokumentiert; der Code hatte am 2026-07-14 einen öffentlichen Initial-Commit, und MobileWorld hat sein Ergebnis am 2026-07-17 erfasst.

## Anwendung {#how-to-use-this}

Stand 2026-07-18 sollten Praktiker KnowAct-GUIClaw als Projekt mit öffentlicher Projektseite und zugehörigem KnowAct-Quell-Repository behandeln. Fähigkeiten und Setup sollten vor einem Einsatz direkt anhand dieser Ressourcen geprüft werden.

1. Wähle den mitgelieferten nanobot-Pfad für eine WebUI, ein Gateway oder einen Agent-Host, oder verwende das eigenständige guiclaw, wenn ein anderer Host, ein Skript oder ein Terminal die GUI-Schicht aufrufen soll.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
2. Installiere Python 3.11+, uv, einen multimodalen OpenAI-kompatiblen Provider und nur das Backend-Extra, das für Android oder HarmonyOS, Desktop oder iOS benötigt wird; erstelle danach die YAML-Konfiguration des Providers.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
3. Führe zuerst einen Dry-Run aus; er prüft Modell und Agent-Loop, ohne ein reales Gerät zu verändern. Wähle danach das Backend adb, ios, hdc oder local.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
4. Fordere bei Automatisierungs-Hosts JSON-Ausgabe an und werte die Felder success, error und trace aus, statt anzunehmen, dass eine Bildschirmaktion erfolgreich war.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>

## Best Practices {#best-practices}

- Beginne mit einem Dry-Run und einem Testgerät oder -konto: Die Validierung kann Intents auslösen und den Zustand von Anwendungen verändern.
  — <https://github.com/HITsz-TMG/KnowAct>
- Behandle den POLICY-Speicher nur als Empfehlung; setze verbindliche Einschränkungen mit Geräte- oder App-Berechtigungen, Allowlists im Backend, Freigaben durch den Host oder Sandboxing durch.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
- Verwende das Standardprofil für zuverlässiges natives Function Calling; wähle ein anderes Profil nur, wenn das Aktionsformat des Modells dazu passt.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
- Validiere Android-Shortcut-Kandidaten vor der Übernahme auf einem ADB-Gerät; ein deklarierter Intent oder Deep Link beweist nicht, dass sich die erwartete Seite öffnet.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
- Plane nicht mit Skills für macOS, Linux oder Windows: Desktop-Skills rufen nicht ab, führen nicht aus, extrahieren nicht und entwickeln sich nicht weiter; die Extraktion von Speicherinhalten bleibt verfügbar.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>

## Durch dieses ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Es wurde kein primäres Release, kein Commit, keine Revision des Papers und keine Projektankündigung mit Datum 2026-07-18 gefunden; dieses Datum kann daher nicht als eigenständiges Produkt-Release gelten.
- Die aktuelle Dokumentation der Seite und des Repositorys ist veränderlich; der genaue Installationspfad, die Paketversion, die Abhängigkeits-Pins und die Lizenz im Stand vom 18. Juli sind nicht verifiziert.
- Es wurde kein offizieller Modell-Checkpoint und kein Release eines semantischen Pakets identifiziert.
- Ein Demonstrationsdetail widerspricht sich in den aktuellen Quellen von Erstanbietern: Die Seite nennt einen 43-minütigen Durchlauf für den Host-Recovery-Fall, während arXiv v2 für das entsprechende Beispiel 13 Minuten angibt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://shibosusu.github.io/KnowAct-GUIClaw/ | KnowAct-GUIClaw | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct | HITsz-TMG/KnowAct | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/commits/main | Commit-Verlauf · HITsz-TMG/KnowAct | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/releases/tag/Result | Release GUIClaw-Result · HITsz-TMG/KnowAct | 2026-09-06 |
| https://arxiv.org/abs/2607.12625 | KnowAct-GUIClaw: Know Deeply, Act Perfectly, Personal GUI Assistant with Self-Evolving Memory and Skill | 2026-09-06 |
| https://arxiv.org/html/2607.12625v2 | KnowAct-GUIClaw technical report, arXiv v2 | 2026-09-06 |
| https://raw.githubusercontent.com/Tongyi-MAI/MobileWorld/main/site/leaderboard.json | MobileWorld-Leaderboard-Daten | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md | GUIClaw-CLI- und Konfigurationsreferenz | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/blob/main/README_CN.md | KnowAct-README (Chinesisch) | 2026-09-06 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:knowact-guiclaw`, Thread `knowact-guiclaw`, 1 datiertes Ereignis 2026-07-18 → 2026-07-18.
- **Praxishinweis:** Stand 2026-07-18 sollten Praktiker KnowAct-GUIClaw als Projekt mit öffentlicher Projektseite und zugehörigem KnowAct-Quell-Repository behandeln. Fähigkeiten und Setup sollten vor einem Einsatz direkt anhand dieser Ressourcen geprüft werden.
- **Konfidenz:** mittel. Datierte Ersetzungen sind maßgeblich dafür, was veraltet ist.

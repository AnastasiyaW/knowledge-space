---
title: "Unity CLI"
category: projects
date: 2026-07-23
tags: [project, unity-cli, unity-cli-introduction, unity_cli]
aliases: ["Unity CLI"]
level: 2
source_sha256: 62d73d94e26b8296c421444daf77d41f98ab65e1aa105de3b0512f2517612026
translation: machine
translated_at: '2026-10-24'
---
# Unity CLI {#unity-cli}

**Entwicklungslinie:** `project:unity-cli` · Thread `unity-cli-introduction`  
**Letztes Ereignis:** 2026-07-23 · 1 datiertes seit 2026-07-23 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Unity CLI ist ein eigenständiges Binary `unity` für Unity 6.0 LTS+ und CI. Es installiert Editor und Module, öffnet und verwaltet Projekte, Lizenzen und Authentifizierung und steuert mit `com.unity.pipeline` einen lokal laufenden Editor oder Dev Player, führt Befehle aus und startet C#-Eval. Einschränkung: CLI und Pipeline bleiben experimentell; Pipeline ist ein separates Paket und arbeitet standardmäßig lokal. Fazit: Für neue Skripte und CI ist dies ein Ersatz für Hub CLI, die Beta-Version muss jedoch fixiert und anhand der Release Notes geprüft werden.

## Entwicklungslinie {#development-line}

- **2026-07-23 — Unity hat eine Ankündigung zu Unity CLI veröffentlicht.** Am 2026-07-23 veröffentlichte Unity einen datierten offiziellen Blogeintrag zu Unity CLI. Der projektspezifische offizielle Link macht dies zu einem wesentlichen Meilenstein in der Einführung der Unity CLI. Die gesicherten Belege belegen weder ihre Funktionen, ihre Verfügbarkeit noch ihr technisches Verhalten.

## Was sich geändert hat {#what-changed}

2026-04-04 — Die erste öffentliche Beta lieferte ein einheitliches Binary für Windows, macOS und Linux, Editor-Verwaltung, Projekte, Auth und maschinenlesbare Ausgabe. 2026-04-23 — Es kamen Projekterstellung, Anzeige des Changelogs und Aktualisierung auf eine ausgewählte Version hinzu. 2026-05-06 — Unity Hub 3.18 begann, eine eigenständige CLI auszuliefern, die unabhängig vom Desktop-Hub ist. 2026-05-07 — beta.4 ergänzte Diagnose, Completion sowie die grundlegenden Befehle zur Steuerung von Editor und Projekten. 2026-05-21 — Service-Account-Auth und `unity pipeline install` machten unbeaufsichtigtes CI und die Anbindung von Pipeline zu Standardabläufen. 2026-06-04 — `unity eval` und `unity status` ergänzten C#-Eval und die Beobachtung des verbundenen Editors. 2026-06-16 — Lizenzierung sowie das Klonen von Projekten aus GitHub, GitLab und Unity Version Control wurden hinzugefügt. 2026-06-25 — `unity mcp` für agentische Integrationen erschien. 2026-06-30 — Der Zweig wechselte auf 1.0 beta; OAuth- und Session-IDs in Logs sowie die JSON-/NDJSON-Ausgabe wurden korrigiert. 2026-07-16 — Die „warme“ interaktive `unity shell` erschien. 2026-07-23 — 1.0.0-beta.3 ergänzte History, Completion, Session-Kontext und framed NDJSON in der Shell. 2026-08-12 — beta.4 ergänzte winget/Homebrew und hob das Linux-Minimum auf glibc 2.34 an. 2026-08-13 — beta.5 beendete die Übergabe von Name und E-Mail aus `unity bug`. 2026-08-21 — beta.6 änderte die für CI relevanten Exit Codes von `unity bug` und `unity test`. 2026-09-02 — beta.8 ersetzte die zurückgezogene beta.7, ergänzte einen Unity-bewussten VCS-Workflow und behob die Inkompatibilität mit einer noch unveröffentlichten Pipeline-Version.

## So wird es verwendet {#how-to-use-this}

Stand 2026-07-23 sollten Praktiker Unity CLI als offizielle Unity-Entwicklungslinie verfolgen und sie für Kommandozeilen-Automatisierung erst evaluieren, nachdem die dokumentierten Funktionen bestätigt sind.

1. Installieren Sie die CLI gemäß der aktuellen Anleitung von Unity und prüfen Sie die Verfügbarkeit mit `unity --version`.
  — <https://docs.unity.com/en-us/unity-cli/use-unity-cli>
2. Lassen Sie sich die Befehle mit `unity --help` anzeigen, installieren Sie eine bestimmte Editor-Version mit den benötigten Modulen und prüfen Sie die verfügbaren Module-IDs.
  — <https://unity.com/ru/blog/meet-the-unity-cli>
3. Führen Sie `unity auth login` aus, danach `unity auth status`; für unbeaufsichtigtes CI verwenden Sie die unterstützte Service-Account-Authentifizierung.
  — <https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference>
4. Öffnen Sie ein Projekt mit `unity open <path>`; für terminalorientiertes CI geben Sie eine konkrete Editor-Version an statt der interaktiven Auswahl.
  — <https://docs.unity.com/en-us/unity-cli/use-unity-cli>
5. Wenn Sie einen laufenden Editor steuern möchten, installieren Sie `com.unity.pipeline` mit `unity pipeline install` und rufen Sie anschließend `unity command` auf, um den verfügbaren Befehlssatz des Projekts zu erhalten.
  — <https://learn.unity.com/tutorial/6a7e194752fbca26e9ebccbe>
6. Fordern Sie für CI JSON oder NDJSON an, verarbeiten Sie stdout getrennt von stderr und prüfen Sie den Exit Code.
  — <https://unity.com/ru/blog/meet-the-unity-cli>

## Best Practices {#best-practices}

- Betrachten Sie `unity --help` der installierten Version als maßgebliche Quelle für Flags: Die Dokumentation enthält möglicherweise einen kürzlich ergänzten Befehl noch nicht.
  — <https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference>
- Legen Sie in CI die Editor-Version explizit fest: Ohne sie schlägt das nicht-interaktive `unity install` fehl.
  — <https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference>
- Aktualisieren Sie Linux-Runner nicht auf beta.4+ ohne glibc 2.34; für Ubuntu 20.04 und älter, Debian 11, RHEL/CentOS 8 und Amazon Linux 2 bleiben Sie bei beta.3.
  — <https://docs.unity.com/ja-jp/unity-cli/release-notes>
- Belassen Sie Pipeline auf localhost, solange Authentifizierung und Netzwerk für den Fernzugriff nicht entworfen sind.
  — <https://learn.unity.com/tutorial/6a7e194752fbca26e9ebccbe>
- Aktualisieren Sie eine kurzzeitig installierte beta.7 auf beta.8: beta.7 wurde wegen Inkompatibilität mit einem noch nicht veröffentlichten Pipeline-Paket zurückgezogen.
  — <https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542>
- Speichern Sie Änderungen vor `unity close`: Weder der normale Aufruf noch `--force` sichern Ihre Arbeit.
  — <https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542>

## Abgelöst durch dies {#superseded-by-this}

- 2026-05-06 — Für neue Skripte sollte Hub CLI mit `-- --headless` nicht als Hauptweg gewählt werden: Die eigenständige Unity CLI ist für neue Automatisierungs- und CI-Szenarien vorgesehen; Hub CLI ist deprecated und wird nur minimal unterstützt. https://docs.unity.com/hub/cli-overview
- 2026-09-02 — 1.0.0-beta.7 ist keine zulässige Version für ein Update: Das Release wurde zurückgezogen und durch beta.8 ersetzt, wegen Inkompatibilität mit dem erforderlichen Pipeline-Paket. https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542

## Weiterhin unbekannt {#still-unknown}

- Die offizielle Dokumentation kennzeichnet Unity CLI weiterhin als experimentell; ein GA-Datum und eine langfristige Unterstützung sind nicht angekündigt.
- CLI und `com.unity.pipeline` sind verschiedene Komponenten: Ohne Pipeline erhält die CLI keine Steuerungsoberfläche für einen laufenden Editor oder Player.
- Das offizielle Material hinter dem Ereignislink ist auf 2026-07-20 datiert, obwohl das Ereignis auf 2026-07-23 datiert ist; beta.3 erschien laut Release Notes tatsächlich am 2026-07-23.
- Die offizielle chinesische Dokumentation wurde geprüft, ein unabhängiger chinesischsprachiger Erfahrungsbericht zur Nutzung wurde für Empfehlungen jedoch nicht gefunden und nicht verwendet.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://unity.com/ru/blog/meet-the-unity-cli | Meet the Unity CLI: Unity vom Terminal aus steuern | 2026-09-05 |
| https://unity.com/blog/meet-the-unity-cli | Meet the Unity CLI: manage Unity from your terminal | 2026-09-05 |
| https://docs.unity.com/en-us/unity-cli | Unity command-line interface (CLI) | 2026-09-05 |
| https://docs.unity.com/en-us/unity-cli/use-unity-cli | Use the Unity command-line interface (CLI) | 2026-09-05 |
| https://docs.unity.com/zh-cn/unity-cli/use-unity-cli | Use the Unity command-line interface (CLI) | 2026-09-05 |
| https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference | Unity command-line interface (CLI) reference | 2026-09-05 |
| https://docs.unity.com/ja-jp/unity-cli/release-notes | Unity command-line interface (CLI) release notes | 2026-09-05 |
| https://unity.com/unity-hub/release-notes | Unity Hub Release Notes | 2026-09-05 |
| https://docs.unity.com/hub/cli-overview | Command line interface overview | 2026-09-05 |
| https://learn.unity.com/tutorial/6a7e194752fbca26e9ebccbe | Introduction to Unity CLI | 2026-09-05 |
| https://discussions.unity.com/t/unity-cli-1-0-0-beta-6-is-rolling-out/1734486 | Unity CLI 1.0.0-beta.6 is rolling out | 2026-09-05 |
| https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542 | Unity CLI 1.0.0-beta.8 is rolling out | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:unity-cli`, Thread `unity-cli-introduction`, 1 datiertes Ereignis 2026-07-23 → 2026-07-23.
- **Praktische Anmerkung:** Stand 2026-07-23 sollten Praktiker Unity CLI als offizielle Unity-Entwicklungslinie verfolgen und sie für Kommandozeilen-Automatisierung erst evaluieren, nachdem die dokumentierten Funktionen bestätigt sind.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

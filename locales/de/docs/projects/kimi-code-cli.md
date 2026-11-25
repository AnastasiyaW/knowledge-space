---
title: "Kimi Code CLI — Öffentliche Projektreferenz"
category: projects
date: 2026-06-09
tags: [kimi-code-cli, kimi_code, project, public-project-reference]
aliases: ["Kimi Code CLI"]
level: 3
source_sha256: 90ca202bdd556789947dbafc6f2c4abc65ad16d65a12e2503b3dd5c0e0b6d0ba
translation: machine
translated_at: '2026-10-24'
---
# Kimi Code CLI — Öffentliche Projektreferenz {#kimi-code-cli-public-project-reference}

**Entwicklungslinie:** `project:kimi-code-cli` · Thread `public-project-reference`  
**Letztes Ereignis:** 2026-06-09 · 1 datiertes seit 2026-06-09 · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

Kimi Code CLI ist ein terminalbasierter Coding-Agent für Entwickler, kein eigenständiges Modell.

- Liest und bearbeitet Code, führt Shell-Befehle aus, durchsucht Dateien und ruft Webseiten ab.
- Verwendet Kimi Code OAuth, einen API-Schlüssel der Kimi Platform oder konfigurierte kompatible Anbieter; unterstützt die ACP-Editorintegration.
- Aktuell dokumentierte Version: v0.41.0 vom 2026-09-04; die npm-Installation erfordert Node.js 22.19+, unter Windows ist Git for Windows erforderlich.

Berechtigungsmodi und Versionsprüfungen sind Betriebssteuerungen, keine Setup-Details.

## Entwicklungslinie {#development-line}

- **2026-06-09 — Dokumentation und Quellcode-Repository von Kimi Code CLI wurden öffentlich verlinkt.** Am 2026-06-09 verlinkte ein datierter Beitrag zu Kimi Code CLI die englischsprachige Projektdokumentation und das GitHub-Repository. Damit existiert ein öffentlicher Referenzpunkt für Dokumentation und Quellcode der CLI. Die vorliegenden Belege nennen weder eine Version, einen Veröffentlichungsmechanismus noch einen Funktionsumfang.

## Was sich geändert hat {#what-changed}

2026-06-09 — Kimi Code CLI v0.12.0 ergänzte `/swarm` mit Live-Fortschrittsanzeige und rate-limit-bewussten Wiederholungsversuchen. Ziele, Hintergrundfragen und die Erkennung von Sub-Skills wurden aus experimentellen Flags herausgelöst. Hinzu kamen Unterstützung für Proxys und Homebrew sowie die standardmäßige Aktivierung der Mikro-Kompaktierung. Am selben Tag behob v0.12.1 die Kompatibilität mit veralteter experimenteller Konfiguration und die Weitergabe des Aufwandsniveaus xhigh an OpenAI-kompatible Chat-Completions.

## So wird es verwendet {#how-to-use-this}

1. Mit dem offiziellen Skript installieren oder `@moonshot-ai/kimi-code` über npm installieren; unter Windows Git for Windows vor dem ersten Start installieren.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html>
2. In das Repository-Verzeichnis wechseln, `kimi` ausführen und dann `/login` für Kimi Code OAuth oder einen API-Schlüssel der Kimi Platform verwenden.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html>
3. Mit einer rein lesenden Orientierungsanfrage beginnen, etwa indem Kimi die Projektverzeichnisse erklären soll; für eine einmalige Anweisung `kimi -p` verwenden.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html>
4. Freigaben vor Änderungen prüfen und `/plan` vor komplexen oder riskanten Arbeiten verwenden.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html>
5. Für mehrstufige Arbeiten `/goal` mit einer Abschlussbedingung und Nachweisen verwenden, die den Abschluss belegen.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/goals.html>
6. Anbieter außerhalb von Kimi und Modell-Aliasse in `~/.kimi-code/config.toml` konfigurieren; API-Schlüssel-Variablen der Shell-Umgebung werden nicht automatisch als Anbieter-Zugangsdaten verwendet.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html>

## Best Practices {#best-practices}

- Bei komplexen oder riskanten Änderungen Always Ask oder den Plan-Modus beibehalten; Never Ask läuft vollständig unbeaufsichtigt, einschließlich sensibler Zugriffe und Plan-Abschlüssen.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html>
- `/goal`-Ziele mit einer klaren Abschlussgrenze und Verifikationsnachweisen formulieren; offene Ziele wie „jeden Fehler finden“ vermeiden.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/goals.html>
- Dauerhafte Allow-, Deny- und Ask-Regeln mit exakten Mustern für Tool-Befehle verwenden; die Schutzsperre für gefährliche Befehle aktiviert lassen, sofern Befehle nicht durch eine andere Kontrolle gesteuert werden.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html>
- Vor der Automatisierung eines Workflows die installierte Version prüfen: Neuere Versionen haben das Verhalten bei Berechtigungen und Befehlen verändert.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html>

## Hierdurch abgelöst {#superseded-by-this}

- :{
- claim
- Die Anleitung von Kimi Code CLI, die experimentelle Mikro-Kompaktierung über `/experiments` zu deaktivieren, ist veraltet: v0.23.0 hat die Funktion und ihren Schalter entfernt.
- obsolete_since
- 2026-07-06
- source_url
- https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html
- claim
- Der Befehlsbaum `kimi server` ist veraltet; stattdessen `kimi web` im Vordergrund verwenden und mit Strg+C beenden.
- obsolete_since
- 2026-07-20
- source_url
- https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html

## Noch unbekannt {#still-unknown}

- Der Originalwortlaut zum Ereignis vom 2026-06-09 ist nicht verfügbar, daher lässt sich nicht feststellen, ob es sich auf v0.12.0, v0.12.1 oder beide bezog; das offizielle Changelog verzeichnet beide für dieses Datum.
- Der Interaktionsleitfaden verwendet Always Ask, Ask When Needed und Never Ask, während Konfigurationsbeispiele weiterhin `manual`, `yolo` und `auto` nennen; die Kompatibilität der Bezeichnungs-Aliasse haben wir nicht unabhängig geprüft.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://moonshotai.github.io/kimi-code/en/ | Kimi Code CLI Docs | 2026-09-07 |
| https://github.com/MoonshotAI/kimi-code | GitHub - MoonshotAI/kimi-code: Kimi Code CLI — Der Ausgangspunkt für Agenten der nächsten Generation | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html | Changelog | Kimi Code Docs | 2026-09-07 |
| https://www.kimi.com/code/docs/kimi-code-cli/release-notes/changelog.html | 变更记录 | Kimi Code 文档 | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html | Erste Schritte | Kimi Code Docs | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html | Interaktion und Eingabe | Kimi Code Docs | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/guides/goals.html | Ziele | Kimi Code Docs | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html | Konfigurationsdateien | Kimi Code Docs | 2026-09-07 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:kimi-code-cli`, Thread `public-project-reference`, 1 datiertes Ereignis 2026-06-09 → 2026-06-09.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.

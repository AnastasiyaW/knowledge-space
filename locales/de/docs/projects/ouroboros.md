---
title: "Ouroboros — Öffentliche Projekt-Updates"
category: projects
date: 2026-08-02
tags: [ouroboros, project, public-project-updates]
aliases: ["Ouroboros"]
level: 3
source_sha256: 11373893bf57967f6988e649cfe94f817a17b910fb87bcd08cfa26c6cc13587e
translation: machine
translated_at: '2026-10-24'
---
# Ouroboros — Öffentliche Projekt-Updates {#ouroboros-public-project-updates}

**Entwicklungslinie:** `project:ouroboros` · Thread `public-project-updates`  
**Letztes Ereignis:** 2026-08-02 · 1 datiertes seit 2026-08-02 · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

Ouroboros ist eine Laufzeitumgebung für KI-Agenten, die als Desktop-Anwendung und headless betrieben werden kann. Es ist kein Modell.

- Lokaler Speicher: Behält Projektverlauf und dauerhaften Speicher auf dem Datenträger.
- Modell-Runner: Betreibt konfigurierte Remote-Modelle oder ein lokales GGUF-Modell.
- Koordinator: Verwaltet spezialisierte Agenten über Aufgaben hinweg.
- Selbstmodifikation: Verändert die eigene Implementierung über Review-Gates.

Es benötigt einen konfigurierten Modellanbieter oder ein lokales Modell, und die Selbstmodifikation macht es zu einer Umgebung mit hohem Vertrauensbedarf.

Verwenden Sie es für isolierte, überprüfbare Coding- und Rechercheaufgaben. Betreiben Sie es nicht als unbeaufsichtigten Netzwerkdienst.

## Entwicklungslinie {#development-line}

- **2026-08-02 — Öffentliche Quelle und Release-Referenz von Ouroboros.** Am 2026-08-02 verlinkte ein Ouroboros-Eintrag das GitHub-Repository und dessen Seite releases/latest zusammen mit externen technischen und Community-Referenzen. Das Linkbündel markiert einen öffentlichen Referenzpunkt, während das genaue Release, der Änderungsumfang und die Urheberschaft unbestätigt bleiben.

## Was sich geändert hat {#what-changed}

- 2026-07-31 — Ein öffentlicher Architektur- und Benchmark-Bericht erschien; v6.87.5 wurde mit Plattformpaketen ausgeliefert, mit einer historisch begrenzten Artefaktnachweis-Grenze.
- 2026-08-02 — Quelllinks erwähnen Ouroboros, doch der fehlende Nachrichtentext macht keine Aussage zu Release, Modell oder Benchmark.
- 2026-08-07 — v6.90.0 verschärfte Anbieter-Routen, Kontingente, Delegation und Notfall-Stopps.
- 2026-08-08 — Ein technischer Bericht formalisierte die geprüfte Kernentwicklung und trennte eingefrorene Benchmark-Snapshots von der laufenden Hope-Linie.
- 2026-08-21 — v6.109.0 fügte eine Live-Statusanzeige der Aufgabenkosten und Agenten-Konten hinzu, die beim Öffnen bereit sind.
- 2026-09-01 — v6.114.0 wurde das stabile Release und ergänzte Prüfungen zur Erhaltung von Fähigkeiten sowie formbasiertes OpenRouter-Failover.
- 2026-09-05 — v7.0.0-rc.15 wurde als Prerelease ausgeliefert, mit einer Korrektur eines Ledger-Race-Problems beim gleichzeitigen Start, ohne den stabilen Kanal zu ersetzen.

## Verwendung {#how-to-use-this}

1. Laden Sie für die Zielplattform das aktuelle stabile Paket herunter, statt für die normale Nutzung den Quellcode zu klonen.
  — <https://github.com/razzant/ouroboros/releases/latest>
2. Konfigurieren Sie beim ersten Start einen unterstützten Remote-Anbieter oder ein lokales GGUF-Modell und legen Sie danach die Review-Richtlinie und das Budget fest.
  — <https://github.com/razzant/ouroboros>
3. Führen Sie eine begrenzte Aufgabe über die Desktop-App oder mit `ouroboros run --start` aus. Halten Sie externe Arbeiten in einem separaten Git-Worktree und exportieren Sie bei Bedarf einen Patch.
  — <https://github.com/razzant/ouroboros>
4. Verwenden Sie den Quellmodus nur für Entwicklung, Modifikation oder lock-geprüfte Tests: Synchronisieren Sie die gesperrte Umgebung, starten Sie den Server und nutzen Sie danach die lokale UI oder CLI.
  — <https://github.com/razzant/ouroboros>

## Best Practices {#best-practices}

- Bleiben Sie standardmäßig beim neuesten stabilen Release. Behandeln Sie v7-Release-Kandidaten als Testbuilds, bis eines als stabil markiert ist.
  — <https://github.com/razzant/ouroboros/releases>
- Halten Sie den Server auf Loopback. Eine nicht lokale Bindung erfordert `OUROBOROS_NETWORK_PASSWORD` oder bereits authentifizierten privaten Ingress. Stellen Sie die Passwort-Umgehung niemals in einem offenen LAN oder auf einem öffentlichen Port bereit.
  — <https://github.com/razzant/ouroboros/blob/main/docs/DEPLOYMENT.md>
- Nutzen Sie das konfigurierte Budget und die Review-Kontrollen, bevor Sie Kernänderungen zulassen, denn die Laufzeitumgebung kann ihren eigenen Code, ihre Prompts, Tools und Abhängigkeiten verändern.
  — <https://github.com/razzant/ouroboros>
- Für Beiträge zum Kern: Halten Sie eine fokussierte Änderung, testen Sie einen committeten Diff und holen Sie ein Review in einem getrennten Kontext mit dokumentierten Nachweisen ein.
  — <https://github.com/razzant/ouroboros/blob/main/CONTRIBUTING.md>

## Hiermit überholt {#superseded-by-this}

- 2026-08-02 — Den veränderlichen Link `/releases/latest` als Beleg für ein Release im August zu behandeln, ist veraltet. Verwenden Sie für historische Release-Aussagen einen datumsfixierten Tag.
- 2026-08-02 — „Schlägt Codex und Claude Code“ ist als Betriebsempfehlung zu pauschal: Die berichteten Vergleiche hängen von Modell und Harness ab, und der Juli-Bericht beschrieb Parität bei GAIA und SWE-bench Pro.
- 2026-09-01 — Installationshinweise auf Basis von v6.87.5 oder v6.90.0 sind durch das stabile v6.114.0 überholt. v7.0.0-rc.15 bleibt ein Prerelease.

## Weiterhin unbekannt {#still-unknown}

- Der ursprüngliche Nachrichtentext vom 2026-08-02 ist nicht verfügbar. Daher kann diesem Datum über eine quellenverlinkte Projekterwähnung hinaus keine Aussage zu Release, Modell oder Benchmark sicher zugeordnet werden.
- Der verlinkte öffentliche Bericht ist auf 2026-07-31 datiert, und die veränderliche URL des neuesten Releases führt inzwischen zu einem Release vom 2026-09-01. Keines von beiden kann auf das Ereignis zurückdatiert werden.
- Benchmark-Ergebnisse stammen von den Autoren und wurden hier nicht unabhängig reproduziert. Der Juli-Bericht nennt 86,97 % für die benannte Terminal-Bench-Konfiguration, während das August-Paper 86,74 % angibt.
- Es wurde keine verifizierte chinesisch-vereinfachte Anleitung der Urheber für genau dieses Repository gefunden. Der Name Ouroboros wird außerdem von unabhängigen Projekten verwendet. Die künftige Identitätszuordnung sollte daher den Repository-Anker `razzant/ouroboros` beibehalten.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/razzant/ouroboros | GitHub - razzant/ouroboros: Ouroboros — self-creating AI agent. Born Feb 16, 2026. | 2026-09-07 |
| https://habr.com/ru/companies/airi/articles/1065428/ | Мой агент Ouroboros побил Codex с Claude Code на Terminal-Bench, OSWorld и CL-Bench. Он написал себя сам / Хабр | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/latest | Release v6.114.0 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/tag/v6.87.5 | Release v6.87.5 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/ANative-Lab/Awesome-Self-Evolving-Agents/issues/74 | Scope check: Ouroboros, reviewed self-modifying agent runtime · Issue #74 | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/tag/v6.90.0 | Release v6.90.0 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://arxiv.org/abs/2608.08311 | Ouroboros: A Self-Developing Frontier Coding Agent with Reviewed Core Evolution | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases | Releases · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/tag/v6.114.0 | Release v6.114.0 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/blob/main/docs/DEPLOYMENT.md | ouroboros/docs/DEPLOYMENT.md at main · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/blob/main/CONTRIBUTING.md | ouroboros/CONTRIBUTING.md at main · razzant/ouroboros · GitHub | 2026-09-07 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:ouroboros`, Thread `public-project-updates`, 1 datiertes Ereignis 2026-08-02 → 2026-08-02.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Verwendung und Best Practices oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Überholungshinweise sind maßgeblich dafür, was veraltet ist.

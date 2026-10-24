---
title: "DeerFlow 2.0 — Agent-Plattformen"
category: projects
date: 2026-03-12
tags: [agent-platforms, agent_platforms, deerflow, project]
aliases: ["DeerFlow 2.0"]
level: 2
source_sha256: b40bcbf24f406b167f38042128f94b65137551db85639691ed6901e26e2c2dc4
translation: machine
translated_at: '2026-10-24'
---
# DeerFlow 2.0 — Agent-Plattformen {#deerflow-20-agent-platforms}

**Entwicklungslinie:** `project:deerflow` · Thread `agent-platforms`  
**Letztes Ereignis:** 2026-03-12 · 1 datiertes Ereignis seit 2026-03-12 · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

DeerFlow 2.0 ist eine Open-Source-Laufzeitumgebung für Teams, die ein Agent-Harness statt eines reinen Forschungsframeworks benötigen.

- Delegation an Subagenten: plant Arbeit und delegiert sie an Subagenten.
- Ausführungsumgebung: kombiniert Speicher, Skills/Tools und ein sandboxed Dateisystem.
- Modellunterstützung: unterstützt mehrere Modellanbieter und selbst gehostete Bereitstellung.

Das Gateway verwendet standardmäßig einen Worker. Der Betrieb mit mehreren Workern erfordert den dokumentierten gemeinsamen Persistenz- und Event-Stack. Verwenden Sie es für eine vertrauenswürdige, vom Betreiber verwaltete Docker-Bereitstellung und nicht standardmäßig als aus dem Internet erreichbaren Endpunkt.

## Entwicklungslinie {#development-line}

- **2026-03-12 — DeerFlow 2.0 wurde über die offizielle Website, den Workspace und das Repository bekannt gemacht.** Am 2026-03-12 verknüpfte DeerFlow 2.0 seine öffentliche Produkt- und Quellcode-Präsenz mit der offiziellen Website, dem Workspace und dem GitHub-Repository von Bytedance. Die verlinkten Ressourcen belegen eine öffentliche Produkt- und Quellcode-Präsenz, ohne eine bestimmte Version, einen Funktionsumfang oder eine Änderung der Verfügbarkeit zu behaupten.

## Was sich geändert hat {#what-changed}

2026-03-12 — Für dieses Datum ist kein DeerFlow-2.0-Release-Artefakt verifiziert. Community-Berichte beschrieben Tool-Fehler, die Agenten-Abläufe abbrechen konnten. Andere Berichte merkten an, dass ein benutzerdefinierter Postgres-Checkpointer von `make dev/start` ignoriert wird. Keiner der Berichte belegt ausgelieferтes Verhalten oder eine neue Version.

## So verwenden Sie es {#how-to-use-this}

1. Klonen Sie das Repository und führen Sie `make setup` aus, um einen Modellanbieter, optionale Suche sowie Sandbox-/Bash-/Dateischreib-Einstellungen festzulegen; dadurch werden `config.yaml` und `.env` erzeugt.
  — <https://github.com/bytedance/deer-flow>
2. Führen Sie `make doctor` aus und verwenden Sie anschließend `make docker-init` und `make docker-start` für die Docker-Entwicklung; die lokale Anwendung wird unter `localhost:2026` bereitgestellt.
  — <https://github.com/bytedance/deer-flow>
3. Verwenden Sie `make check`, `make install` und `make dev` für die lokale Entwicklung; unter Windows führen Sie die lokalen Skripte über Git Bash aus, nicht über native PowerShell oder cmd.
  — <https://github.com/bytedance/deer-flow>
4. Behandeln Sie den öffentlichen Workspace als Demo: Der beobachtete Demo-Zustand enthält keine To-dos, daher validieren Sie die Terminplanung stattdessen auf einer selbst gehosteten Instanz.
  — <https://deerflow.tech/workspace/>

## Best Practices {#best-practices}

- Verwenden Sie Linux und Docker für einen dauerhaften Dienst; die dokumentierte Mindestgröße des Servers beträgt 8 vCPUs, 16 GB RAM und 40 GB freier SSD-Speicher.
  — <https://github.com/bytedance/deer-flow>
- Belassen Sie `GATEWAY_WORKERS=1`, sofern nicht Postgres, die Redis-Stream-Bridge, Heartbeats für die Run-Zuständigkeit und datenbankgestützte Run-Events konfiguriert sind.
  — <https://github.com/bytedance/deer-flow>
- Lassen Sie das Gateway zunächst nur auf Loopback lauschen. Vor einer externen Freigabe legen Sie ein Admin-Konto an und ergänzen eine IP-Allowlist, eine Vorab-Authentifizierung am Reverse Proxy sowie Netzwerkisolierung.
  — <https://github.com/bytedance/deer-flow>
- Verwenden Sie Docker/AIO, Kubernetes oder E2B, wenn Shell-Zugriff eine erzwingbare Dateisystemgrenze benötigt; Host-Bash mit der lokalen Sandbox ist nur für vollständig vertrauenswürdige Abläufe vorgesehen.
  — <https://github.com/bytedance/deer-flow>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-02-14 — Die Behandlung der aktiven `main`-Linie als ursprüngliches DeerFlow-1.x-Framework wurde für neue Arbeiten durch die Anweisung des Maintainers abgelöst, `main` mit der neuen Version zu verwenden. Die Legacy-Linie wird weiterhin separat gepflegt.
- 2026-06-25 — Das unveränderliche `v2.0.0` (`7e7f041`) ersetzt den Status der RC-Auswahl als formale Basis des 2.0-Releases. Dies bestätigt den Funktionsumfang vom 12. März nicht nachträglich.

## Weiterhin unbekannt {#still-unknown}

- Das Ereignis verweist auf Links, aber es liegt weder öffentlicher Quelltext noch ein eingefrorener Snapshot vom März vor. Daher lassen sich dem 2026-03-12 kein exakter DeerFlow-2.0-Commit, kein Tag und kein vollständiger Funktionsumfang zuordnen.
- Keine datierte Erstquelle aus dem März belegt die genaue unterstützte Modellliste; aktuelle Modellempfehlungen sind aktuelle Leitlinien und keine Belege aus dem März.
- `bytedance/deerflow` ist der übergebene Subjektschlüssel, während der offizielle Repository-Slug `bytedance/deer-flow` lautet.
- Wir haben während dieser Recherche keine selbst gehostete Instanz betrieben; aktuelle Aussagen zum Betrieb sind ausschließlich Dokumentationsbelege.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/bytedance/deer-flow | GitHub - bytedance/deer-flow | 2026-09-07 |
| https://deerflow.tech/ | DeerFlow | 2026-09-07 |
| https://deerflow.tech/workspace/ | DeerFlow-Workspace | 2026-09-07 |
| https://github.com/bytedance/deer-flow/issues/824 | Release-Plan für DeerFlow 2.0 · Issue #824 | 2026-09-07 |
| https://github.com/bytedance/deer-flow/issues/1109 | Tool-Call-Fehler sollte zu einer Error-ToolMessage herabgestuft werden, statt die Konversation abzubrechen · Issue #1109 | 2026-09-07 |
| https://github.com/bytedance/deer-flow/issues/1118 | Checkpointer funktioniert nicht mit dem Befehl „make start“ · Issue #1118 | 2026-09-07 |
| https://deerflow.tech/blog/posts | Alle Beiträge | 2026-09-07 |
| https://github.com/bytedance/deer-flow/releases/tag/v2.0.0 | DeerFlow 2.0.0 veröffentlicht | 2026-09-07 |

## Agent-Kurzfassung {#agent-brief}

- **Subjekt:** `project:deerflow`, Thread `agent-platforms`, 1 datiertes Ereignis 2026-03-12 → 2026-03-12.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel.

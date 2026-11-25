---
title: "Odysseus"
category: projects
date: 2026-06-01
tags: [odysseus, project]
aliases: ["Odysseus"]
level: 3
source_sha256: 36a4e91a28561f3062f0e30738352247b64666c485bce3e51ea51f1f52001784
translation: machine
translated_at: '2026-10-24'
---
# Odysseus {#odysseus}

**Entwicklungsstrang:** `project:odysseus` · Thread `odysseus`  
**Letztes Ereignis:** 2026-06-01 · 1 datiertes seit 2026-06-01 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Odysseus ist ein selbst gehosteter Arbeitsbereich für Anwender, die eine Oberfläche im Stil von ChatGPT oder Claude mit lokalen oder API-basierten Modellen wünschen.

- Chat und Agenten: führt Tools, MCP, Dateien, Shell, Skills und Speicher aus.
- Recherche und Dokumente: unterstützt Deep Research, Modellvergleich, Dokumente, E-Mail, Notizen, Aufgaben, Kalender und ein Cookbook zum Bereitstellen von Modellen.

## Entwicklungsstrang {#development-line}

- **2026-06-01 — Odysseus-GitHub-Repository verknüpft.** Am 2026-06-01 haben wir Verweise auf das GitHub-Repository pewdiepie-archdaemon/odysseus und dessen Git-Endpunkt erfasst. Der Verweis gibt einen Quellort an, wir haben aber weder den Inhalt des Repositorys, den Release-Stand noch die Funktionalität überprüft.

## Was sich geändert hat {#what-changed}

- 2026-06-01 — Das Projekt suchte Mitwirkende für plattformübergreifende Tests, Dokumentation, Sicherheitsprüfung sowie für Cookbook und die Zuverlässigkeit lokaler Modelle. Ein Bericht zu den Zugangsdaten beim ersten Start am selben Tag zeigte Hürden beim Onboarding.
- 2026-07-12 — Ein Commit auf `main` erhöhte die Code-Version auf 1.0.2.
- 2026-08-25 — Ein Commit auf `main` bereitete einen Image-Hotfix 1.0.3 vor.

## So wird es verwendet {#how-to-use-this}

Seit dem 2026-06-01 verwenden wir das erfasste Odysseus-GitHub-Repository als Quellenverweis und prüfen dessen Betriebsstatus separat.

1. Klone `https://github.com/odysseus-dev/odysseus.git`. Verwende für kuratierten Code `main` statt des Standardzweigs `dev`.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/README.md>
2. Für Docker kopiere `.env.example` nach `.env`, führe `docker compose up -d --build` aus und warte, bis die Container healthy sind.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md>
3. Öffne `http://localhost:7000`, rufe das temporäre Admin-Passwort aus `docker compose logs odysseus` ab und ändere es anschließend in den Einstellungen.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md>
4. Für natives Windows statt Docker führe `powershell -ExecutionPolicy Bypass -File .\launch-windows.ps1` aus. Konfiguriere Ollama unter `http://localhost:11434/v1` für ein lokales Windows-Modell.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md>

## Bewährte Verfahren {#best-practices}

- Verwende für kuratierten Code `main`. Wähle `dev` nur, wenn du bewusst die neuesten Änderungen nutzen willst.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/README.md>
- Lass die Authentifizierung aktiviert und die Umgehung für localhost deaktiviert, wenn Bereitstellungen über das Netzwerk erreichbar sind. Verwende HTTPS sowie einen vertrauenswürdigen Proxy, ein VPN oder eine andere private Zugriffsschicht jenseits von localhost.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/SECURITY.md>
- Halte die Ports von Modellen und Unterstützungsdiensten intern. Schütze `.env`, Daten, Logs, Uploads, Sitzungsdateien, Datenbanken, Backups und API-Zugangsdaten.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/SECURITY.md>
- Beschränke den Zugriff auf Shell, Dateisystem, E-Mail, MCP und Modellbereitstellung auf vertrauenswürdige Administratoren. Die Shell- und Dateisystem-Tools der Agenten besitzen weder Sandbox noch Egress-Filter.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/THREAT_MODEL.md>
- Führe vor dem Vertrauen auf den genauen Pfad einen Smoke-Test für Docker, nativen Betrieb, WSL, GPU und Anbieter durch. Die Abdeckung von Neuinstallationen bleibt ein Roadmap-Punkt mit hoher Priorität.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/ROADMAP.md>

## Abgelöst durch {#superseded-by-this}

- 2026-07-12 — Version 1.0.2 löst v1.0 als aktuelle Code-Version auf `main` ab, nach dem Versions-Bump-Commit.
- 2026-08-25 — Ein Commit, der einen Image-Hotfix 1.0.3 vorbereitet, löst 1.0.2 als aktuelles Entwicklungsziel auf `main` ab, ist aber kein formales GitHub-Release.
- 2026-09-05 — `odysseus-dev/odysseus` löst `pewdiepie-archdaemon/odysseus` per Weiterleitung als kanonischen Clone-Namensraum ab; das Datum der Übertragung ist unbekannt.

## Weiterhin unbekannt {#still-unknown}

- Für den Wechsel von `pewdiepie-archdaemon` zu `odysseus-dev` haben wir weder ein erfasstes Datum noch Bedingungen. Die Weiterleitung legt nur die aktuelle kanonische Route fest.
- Wir haben keinen rekonstruierbaren Code-Snapshot für den 2026-06-01, daher können aktuelle Dokumentation und spätere Commits die Fähigkeiten vom Juni nicht verifizieren.
- Wir haben kein formales GitHub-Release und keine vom Projekt veröffentlichte, unveränderliche stabile Version oder Tag gefunden.
- Wir haben keine Dokumentation in vereinfachtem Chinesisch von Projektseite und keine reproduzierbaren Belege für den Betrieb in chinesischer Sprache gefunden.
- Wir haben keine mitgelieferte Foundation-Model-ID gefunden. Odysseus ist eine Anwendungsschicht, die ein konfiguriertes lokales oder API-basiertes Modell benötigt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/pewdiepie-archdaemon/odysseus | GitHub - odysseus-dev/odysseus: Selbst gehosteter KI-Arbeitsbereich. | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/README.md | Odysseus README (Branch dev) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md | Odysseus Setup Guide (Branch dev) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/SECURITY.md | Odysseus Security Policy (Branch dev) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/THREAT_MODEL.md | Odysseus Threat Model (Branch dev) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/ROADMAP.md | Odysseus Roadmap (Branch dev) | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/discussions/551 | Who can help? · Discussion #551 | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/issues/395 | what kind of credentials does it expect on first run · Issue #395 | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/commits/main/ | Commits · odysseus-dev/odysseus · main | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/releases | Releases · odysseus-dev/odysseus | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:odysseus`, Thread `odysseus`, 1 datiertes Ereignis 2026-06-01 → 2026-06-01.
- **Praktischer Hinweis:** Seit dem 2026-06-01 können Praktiker das erfasste Odysseus-GitHub-Repository als Referenz für den Quellort verwenden und dabei dessen Inhalt und Betriebsstatus separat überprüfen.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.

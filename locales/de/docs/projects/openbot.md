---
title: "OpenBot — Projektentwicklung"
category: projects

tags: [openbot, project, project-development]
aliases: ["OpenBot"]
level: 3
source_sha256: e789842d3f733f893cf33d79fba67489c3d23ab8c418e7b70acc89789a185b3e
translation: machine
translated_at: '2026-10-24'
---
# OpenBot — Projektentwicklung {#openbot-project-development}

**Entwicklungsstrang:** `project:openbot` · Thread `project-development`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

OpenBot ist eine Vorlage, die Teams klonen, um eigenständig betriebene, regelgesteuerte AG-UI-Coworker auf der eigenen Infrastruktur laufen zu lassen, statt einen gehosteten Agenten zu verwenden.

- Bot-Isolation: Gibt jedem Bot ein eigenes Browserprofil, ein eigenes Dateisystem und eigene gewährte Tools.
- Policy-Gateway: Leitet Browser-, Datei- und MCP-Aktionen über eine fail-closed CEL-Prüfung und einen Audit-Trail.
- Agenten-Unterstützung: Akzeptiert benutzerdefinierte AG-UI-Agenten sowie die mitgelieferten Proof-of-Concept- und LangGraph-Bots.

Es handelt sich weiterhin um Alpha-Software ohne gehostete Version und ohne installierbares Paket.

Einsetzen lässt es sich, wenn unser Team Docker, PostgreSQL, Modell-Credentials und Zugriffsrichtlinien selbst verantworten kann; es ist nicht als verwawell Dienst zu betrachten.

## Entwicklungsstrang {#development-line}

- Die datierte Entwicklungslinie ist noch nicht aufgearbeitet; das Bekannte steht unten.

## Was sich geändert hat {#what-changed}

- 2026-08-17 — v0.0.1 führte den lokal lauffähigen Alpha-Stand mit isolierten Computern pro Bot, regelgesteuerten Aktionen, AG-UI-Unterstützung und CopilotKit-Intelligence-Threads ein.
- 2026-08-22 — v0.0.2–v0.0.4 machten den Tool-Zugriff bei frisch geklonten Installationen nutzbar und zogen gleichzeitig die Sicherheitsgrenze enger: automatische lokale Erzeugung von AGENT_TOOL_TOKEN, skillbasierte Tool-Auswahl ab 12 Grants, Audit-Sichtbarkeit, korrigiertes Routing für OpenAI-kompatible Endpunkte, mitgelieferte Skills und Ablehnung einer nicht auflösbaren Seitenreferenz.
- 2026-08-28 — v0.0.5 ergänzte die vom Administrator gewährte Übergabe zwischen Bots und die menschliche Eskalation, reparierte hängengebliebene Tool-Ergebnis-Konversationen und ergänzte Streaming-Unterstützung für die Responses API für gpt-5.6-*-Modelle.

## So wird es verwendet {#how-to-use-this}

Zum 2026-08-22 haben wir keine Änderung des praktischen Arbeitsablaufs erfasst. Recherchieren Sie zuerst das verlinkte Repository und rufen Sie die Quellmeldung ab, um festzustellen, was sich geändert hat.

1. OpenBot klonen und Docker, Bun 1.3+, ein CopilotKit-Intelligence-Projekt sowie ein Modell-Credential vorbereiten.
  — <https://github.com/CopilotKit/openbot>
2. .env.example nach .env kopieren, mit der CopilotKit CLI INTELLIGENCE_API_KEY beziehen und das Modell-Credential setzen.
  — <https://github.com/CopilotKit/openbot>
3. bun install ausführen und danach bash scripts/start.sh starten; http://localhost:3010 öffnen, sobald die Health-Checks erfolgreich sind.
  — <https://github.com/CopilotKit/openbot>
4. Das Beispiel-Tenant-Paket durch brand.yaml, agents.yaml, channels.yaml, model.yaml und knowledge.yaml ersetzen; bei Bedarf skills.yaml hinzufügen.
  — <https://github.com/CopilotKit/openbot/blob/main/docs/configuration.md>
5. Coworker unter /agents anlegen oder verbinden, MCP-Server und Grants unter /admin/plugins konfigurieren und Browser-/Datei-/MCP-Regeln unter /admin/boundaries festlegen.
  — <https://github.com/CopilotKit/openbot>
6. Eine kontrollierte Browser-Aktion testen, eine Deny-Regel hinzufügen, die Aktion erneut versuchen und die erlaubte oder abgelehnte Aktion in /admin/audit prüfen.
  — <https://github.com/CopilotKit/openbot>

## Bewährte Praktiken {#best-practices}

- Aktivieren Sie einen Identity Provider, bevor Sie weitere Personen zulassen: Der Standardmodus für einen einzelnen Benutzer behandelt jeden Besucher als Administrator.
  — <https://github.com/CopilotKit/openbot>
- Tools mit minimalen Rechten betreiben. Skills legen fest, welche Tools angeboten werden, gewähren aber keinen Zugriff; die Bot-Grants bleiben die wirksame Grenze.
  — <https://github.com/CopilotKit/openbot/releases>
- Die standardmäßige Computer-Isolation pro Bot beibehalten; gVisor über COMPUTER_RUNTIME=runsc verwenden, sofern der Host es unterstützt.
  — <https://github.com/CopilotKit/openbot>
- Policy und Audit als wiederkehrenden Betriebsablauf behandeln: Eine verweigerte Aktion testen, bevor sie gewährt wird, und danach den resultierenden Audit-Trail prüfen.
  — <https://github.com/CopilotKit/openbot>
- Für ein veröffentlichtes Deployment den Container-Digest aus container-images.json festlegen und die GitHub-Provenance-Attestierung prüfen, statt einen veränderlichen Tag zu deployen.
  — <https://github.com/CopilotKit/openbot/blob/main/docs/releasing.md>

## Hiermit ersetzt {#superseded-by-this}

- 2026-08-22 — Frisch geklonte Laptop-Installationen benötigen beim Start mit scripts/start.sh keine manuelle Bereitstellung von AGENT_TOOL_TOKEN mehr; Deployments außerhalb dieses Skripts scheitern ohne Token weiterhin geschlossen (fail-closed).
- 2026-08-22 — Das Angebot aller gewährten Tools an Bots mit mehr als 12 Tools wird durch skillpassende Angebote plus nicht beanspruchte gewährte Tools ersetzt.
- 2026-08-22 — Eine Browser-Aktion, deren referenziertes Element nicht aufgelöst werden kann, wird nicht mehr zugelassen; der Bot muss einen neuen Snapshot erstellen.
- 2026-08-28 — Läufe von gpt-5.6-*-Framework-Bots, die Content-Blöcke der Responses API stillschweigend verworfen haben, werden durch die Behandlung beider Streaming-Formen ersetzt.

## Weiterhin unbekannt {#still-unknown}

- Der Eintrag vom 2026-08-22 enthält nur die Repository-URL, daher lässt sich die genau beabsichtigte Version nicht ermitteln; GitHub verzeichnet an diesem Datum v0.0.2, v0.0.3 und v0.0.4.
- OpenBot bleibt Alpha, und laut README ist das Repository eine Vorlage und kein gehostetes Produkt; die Produktionsreife für einen konkreten Einsatz erfordert daher eine eigene Sicherheits- und Betriebsprüfung.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/CopilotKit/openbot | OpenBot README | 2026-09-05 |
| https://github.com/CopilotKit/openbot/releases | Releases · CopilotKit/OpenBot | 2026-09-05 |
| https://github.com/CopilotKit/openbot/blob/main/docs/configuration.md | OpenBot configuration | 2026-09-05 |
| https://github.com/CopilotKit/openbot/blob/main/docs/releasing.md | OpenBot releasing guide | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:openbot`, Thread `project-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Zum 2026-08-22 raten wir zu keiner Änderung des praktischen Arbeitsablaufs; recherchieren Sie zuerst das verlinkte Repository und rufen Sie die Quellmeldung ab, um festzustellen, was sich geändert hat.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

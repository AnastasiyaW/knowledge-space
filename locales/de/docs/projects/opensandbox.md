---
title: "OpenSandbox"
category: projects

tags: [opensandbox, opensandbox-development, opensandbox-group/opensandbox, project]
aliases: ["OpenSandbox"]
level: 2
source_sha256: cbb2d4a6dcf06b1628ab9fe3c6123196a3ff03be63e3071d014065e69443612b
translation: machine
translated_at: '2026-10-24'
---
# OpenSandbox {#opensandbox}

**Entwicklungslinie:** `project:opensandbox` · Thread `opensandbox-development`  
**Letztes Ereignis:** - · 0 datierte seitdem - · **Recherchiert:** 2026-09-08 · Konfidenz: mittel

## Was es ist {#what-it-is}

OpenSandbox stellt isolierte Umgebungen für KI-Agenten über Docker und Kubernetes bereit.

- Mehrsprachige SDKs, eine `osb`-CLI und ein MCP-Server
- Lebenszyklus-, Befehls- und Datei-APIs über Docker und Kubernetes
- Egress-Richtlinie pro Sandbox, Credential-Vault-Proxy und optionale Auswahl sicherer Laufzeiten

Die lokale Ausführung erfordert Docker und Python 3.10+; die Lifecycle-API bindet standardmäßig an `0.0.0.0`. Verwenden Sie es als Ausführungsschicht für Agenten-Workloads, sichern Sie jedoch die Control Plane und die ausgehende Netzwerkrichtlinie, bevor Sie es exponieren.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; das Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

OpenSandbox-Entwicklung: 2026-03-03 — das Paket `opensandbox-server` 0.1.5 wurde veröffentlicht, was die Paketverteilung vor der Projektreferenz vom August zeigt. 2026-03-22 — PyPI führt `opensandbox-server` 0.1.8 wegen Inkompatibilität als yanked. 2026-08-15 — die datierte Projektreferenz identifiziert OpenSandbox, belegt aber selbst kein getaggtes Feature und kein Release. 2026-08-19 — Helm-Chart 0.2.2, App-Version 0.2.2, ausgeliefert als All-in-One-Paket aus Controller und Server. 2026-08-26 — `opensandbox-server` 0.2.3 wurde veröffentlicht, und `execd` 1.1.0 ergänzte optionale Init-, Härtungs- und Lifecycle-Hook-Funktionen; die klassische Topologie blieb der Standard.

## Verwendung {#how-to-use-this}

1. Für die lokale Nutzung installieren Sie Docker und Python 3.10+, erzeugen die Beispielkonfiguration für Docker mit `uvx opensandbox-server init-config ~/.sandbox.toml --example docker` und starten anschließend `uvx opensandbox-server`.
  — <https://github.com/opensandbox-group/OpenSandbox>
2. Installieren Sie `opensandbox-cli`, konfigurieren Sie Domain, Protokoll und API-Schlüssel, erstellen Sie eine Sandbox mit explizitem Timeout, führen Sie einen Health-Check durch, starten Sie die Workload und beenden Sie danach die Sandbox.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md>
3. Für einen MCP-fähigen Coding-Client installieren Sie `opensandbox-mcp` und konfigurieren dessen stdio-Prozess mit Domain, Protokoll und API-Schlüssel von OpenSandbox.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/sdks/mcp/sandbox/python/README.md>
4. Für die All-in-One-Topologie unter Kubernetes installieren Sie das offizielle Helm-Release 0.2.2 im Namespace `opensandbox-system`.
  — <https://github.com/opensandbox-group/OpenSandbox/releases/tag/helm%2Fopensandbox%2F0.2.2>

## Best Practices {#best-practices}

- Setzen Sie vor jeder produktiven Exposition einen nicht leeren Server-API-Schlüssel; ein leerer Schlüssel deaktiviert die Prüfungen und erfordert eine explizite Bestätigung für den unsicheren Start.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/server/configuration.md>
- Erstellen Sie Sandboxes mit Credential-Proxy mit einer expliziten Netzwerkrichtlinie und übergeben Sie Credential-Vault-Payloads per Datei oder stdin statt als Klartext in Befehlszeilenflags.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md>
- Verwenden Sie explizite Sandbox-Timeouts und beenden Sie Sandboxes nach der Workload; eine Pause-Anfrage ist asynchron, daher sollten Sie abfragen, bis der Zustand Paused erreicht.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md>
- Lösen Sie Release-Images zu unveränderlichen Digests auf und prüfen Sie deren Cosign-Signatur und Provenance-Attestation, statt sich auf veränderbare Tags zu verlassen.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/docs/community/release-verification.md>

## Hiermit überholt {#superseded-by-this}

- {"claim":"`opensandbox-server` 0.1.8 ist ein brauchbares Server-Release.","obsolete_since":"2026-03-22","source_url":"https://pypi.org/project/opensandbox-server/"}

## Noch unbekannt {#still-unknown}

- Das vorliegende Ereignis enthält nur eine Projekt-URL; das beabsichtigte Feature bzw. die Aussage zum 2026-08-15 lässt sich daher nicht rekonstruieren.
- Es wurde keine Release-Notiz des Herstellers mit dem genauen Datum 2026-08-15 gefunden; das gleichtägige Helm-Detail ist ein Issue-Bericht, keine Release-Ankündigung.
- Der aktuelle Verifizierungsleitfaden verzeichnet für Artefakte vor der Migration eine historische Repository-Identität `alibaba/OpenSandbox`, datiert die Migration der Organisation jedoch nicht.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/opensandbox-group/OpenSandbox | OpenSandbox-Repository-README | 2026-09-08 |
| https://pypi.org/project/opensandbox-server/0.1.5/ | opensandbox-server 0.1.5 auf PyPI | 2026-09-08 |
| https://pypi.org/project/opensandbox-server/ | opensandbox-server auf PyPI | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/issues/1529 | Issue #1529: Lücke beim All-in-One-Helm-Chart-Release | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/releases/tag/helm%2Fopensandbox%2F0.2.2 | Helm Chart opensandbox 0.2.2 (App v0.2.2) | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/releases/tag/docker%2Fexecd%2Fv1.1.0 | components/execd 1.1.0 Release | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md | OpenSandbox-CLI-README | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/server/configuration.md | OpenSandbox-Server-Konfigurationsreferenz | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/sdks/mcp/sandbox/python/README.md | OpenSandbox MCP Sandbox Server | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/docs/community/release-verification.md | OpenSandbox Release-Verifikation | 2026-09-08 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:opensandbox`, Thread `opensandbox-development`, 0 datierte Ereignisse - → -.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Verwendung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Einträge unter „Hiermit überholt“ sind maßgeblich für das, was veraltet ist.

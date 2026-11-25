---
title: "Sicherheit agentischer KI"
description: "Ein Bedrohungsmodell- und Kontrollleitfaden für werkzeugnutzende Agenten, MCP-Integrationen, persistenten Speicher und nicht rückgängig zu machende Wirkungen. Stand der Prüfung: 2026-09-03."
tags: [agent-security, mcp, prompt-injection, authorization, supply-chain, ai-safety]
level: 4
source_sha256: 31ad7c52408b2c52f339d524d26e144022aed1482ff69c185fe1c9fa9f8da13f
translation: machine
translated_at: '2026-10-24'
---
# Sicherheit agentischer KI {#agentic-ai-security}

**Stand der Prüfung: 2026-09-03.** Die Sicherheit von Agenten ist ein Problem der Anwendungssicherheit, in dem ein probabilistischer Planer arbeitet. Verlassen Sie sich nicht auf eine Schlagzeile zur Angriffsrate, auf eine einzelne CVE oder auf einen Prompt-Filter als Sicherheitsgrenze. Beginnen Sie mit einem Bedrohungsmodell, erzwingen Sie Berechtigungen außerhalb des Modells und bewahren Sie für jede externe Wirkung einen Nachweis auf.

Die OWASP Top 10 for Agentic Applications heben unter den kritischen Risikoklassen unter anderem Goal Hijack, Tool Misuse, Identity- und Privilege-Abuse, Supply-Chain-Schwachstellen und unerwartete Codeausführung hervor. [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)

## Zuerst das Bedrohungsmodell {#threat-model-first}

Bilden Sie den tatsächlichen Daten- und Berechtigungsfluss ab:

```text
untrusted input -> retrieval / context -> model planner -> tool request
                       |                    |              |
                    private data          memory         effect executor
                                                               |
                                                         external system
```

Erfassen Sie für jede Grenze den Prinzipal, die Datenklassifizierung, die erlaubte Aktion, das Ablaufdatum, das Audit-Ereignis und den Wiederherstellungspfad. Eine Architektur mit hohem Risiko vereint alle drei der folgenden Eigenschaften in einer unbeschränkten Schleife:

1. liest private Daten;
2. verarbeitet von Angreifern beeinflusste Eingaben;
3. kann eine externe Aktion ausführen.

Die Antwort sind Trennung und erzwungene Vermittlung, nicht lediglich ein stärkerer System-Prompt.

## Zentrale Risikoklassen {#core-risk-classes}

| Risiko | Beispiel | Kontrollgrenze |
|---|---|---|
| Goal Hijack / Prompt Injection | Webseite bittet den Agenten, die Richtlinie zu überschreiben | Inhalte als nicht vertrauenswürdig kennzeichnen; der Tool-Executor behandelt Modelltext nicht als Autorität |
| Tool Misuse | Modell wählt ein gültiges Werkzeug für eine ungültige Geschäftsaktion | Schema, Autorisierung, Freigaben und Idempotenz im Executor |
| Identity- und Privilege-Abuse | geleaktes oder zu weit gefasstes Token erreicht einen Connector | Workload-Identität, eng gefasste Scopes, Audience-Prüfung, Widerruf |
| Supply-Chain-Kompromittierung | Abhängigkeit oder entfernter MCP-Server ändert das Verhalten | Herkunftsnachweis, Pinning, Review, kontrollierter Rollout |
| Unerwartete Codeausführung | Tool-Eingabe erreicht Shell oder Interpreter | Sandbox, Allowlist für Befehle, keine breiten Mounts oder Credentials |
| Memory Poisoning | feindlicher Text wird zu dauerhafter Anweisung | Quellenherkunft, Schreibrichtlinie, prüfbare Änderungshistorie |
| Datenexfiltration | erlaubter Lesezugriff wird in einen erlaubten ausgehenden Aufruf kodiert | End-to-End-Kontrollen für Egress und Aktionsgraph |

## Fähigkeit erzwingen, nicht Absicht {#enforce-capability-not-intent}

Der Agent kann eine Aktion vorschlagen. Ein deterministischer Effect-Service entscheidet, ob sie ausgeführt wird:

```json
{
  "task_id": "research-044",
  "action": "create_draft",
  "resource_scope": "project:happyin-space",
  "arguments_digest": "sha256:...",
  "approval_ref": "approval:appr_01...",
  "idempotency_key": "research-044:v1",
  "expires_at": "2026-09-03T18:00:00Z"
}
```

Prüfen Sie vor einer Wirkung die Identität des Aufrufers, die Zielgruppe des Empfängers, die unveränderliche Anfrage, den Scope, die Freigabe, das Ablaufdatum und die Idempotenz-Reservierung. Geänderte Argumente erfordern eine neue Capability. Ein unbekanntes Ergebnis wird vor einem erneuten Versuch anhand eines Provider-Nachweises abgeglichen.

Einen konkreten Vertrag für Capability und atomare Wiederholung finden Sie unter [[agent-safety-alignment]].

## MCP-Grenzen {#mcp-boundaries}

MCP macht Werkzeuge auffindbar, aber nicht vertrauenswürdig. Das Protokoll empfiehlt Hosts, Nutzerzustimmung und Kontrolle über Datenzugriff und Werkzeugaufrufe zu behalten, und erklärt, dass Werkzeugbeschreibungen als nicht vertrauenswürdig zu behandeln sind, sofern sie nicht von einem vertrauenswürdigen Server stammen. [MCP-Architektur](https://modelcontextprotocol.io/specification/latest/architecture) [MCP-Tools](https://modelcontextprotocol.io/specification/latest/server/tools)

Für entfernte MCP-Server gilt:

1. Prüfen Sie Serveridentität und Transport, bevor Sie den Server registrieren;
2. fordern Sie den minimalen OAuth-Scope an und stellen Sie sicher, dass Tokens für diese Ressource bestimmt sind;
3. halten Sie Upstream-Credentials serverseitig, anstatt sie durchzureichen;
4. stellen Sie nur die für den aktuellen Workflow nötigen Werkzeuge bereit;
5. verlangen Sie für Aufrufe mit hoher Auswirkung eine Freigabe durch Nutzer oder Richtlinie;
6. protokollieren Sie Werkzeugaufruf, Aufrufer, Anfrage-Digest und resultierenden Nachweis.

MCP-Autorisierung erfordert die Bindung an Ressource bzw. Audience und lehnt Token-Passthrough als allgemein sicheres Muster ab. [MCP-Autorisierung](https://modelcontextprotocol.io/specification/latest/basic/authorization)

## Speicher sind Daten, keine Richtlinie {#memory-is-data-not-policy}

Persistenter Speicher kann Aussagen von Nutzern, abgerufenen Seiten, Werkzeugen oder früheren Modellausgaben enthalten. Speichern Sie die Herkunft und behandeln Sie jeden Schreibvorgang als Daten:

| Feld | Zweck |
|---|---|
| Quellenreferenz | identifiziert, woher die Aussage stammt |
| Vertrauenskennzeichnung | unterscheidet Nutzerbehauptung, genehmigte Richtlinie und nicht vertrauenswürdigen Abruf |
| autorisierender Prinzipal | zeigt, wer den Schreibvorgang erlaubt hat |
| Ablaufdatum oder Review-Datum | verhindert, dass veraltete Anweisungen dauerhafte Autorität erlangen |
| Revisionshistorie | ermöglicht Audit der Änderungen und sicheres Zurücksetzen |

Erheben Sie niemals eine abgerufene Anweisung zu einer Berechtigung, einer Routing-Regel oder einem Credential-Verweis allein deshalb, weil sie in einem vertrauenswürdig wirkenden Dokument steht.

## Matrix für Sicherheitstests {#security-test-matrix}

Testen Sie den integrierten Workflow, nicht isolierte Prompts:

- direkte und indirekte Injection in Webseiten, Anhängen, Datensätzen und Werkzeugausgaben;
- mandantenübergreifende Abruf- und Ausgabeversuche;
- manipulierte Werkzeugargumente sowie schemakonforme, aber richtlinienwidrige Aktionen;
- veraltete Freigaben, abgelaufene Capabilities und Abweichungen bei Identität oder Audience;
- doppelte Ausführungen und Pfade mit verlorener Antwort bei Veröffentlichung, Löschung oder Zahlung;
- Simulation kompromittierter Abhängigkeiten oder Server-Versionen;
- Abbruch, Sandbox-Ausbruch, Egress und Prüfung der Log-Schwärzung.

Erfassen Sie die Klasse der Testeingabe, die Richtlinienrevision, die erwartete Entscheidung und den Nachweis. Eine „sichere“ Textvervollständigung ist kein Beleg dafür, dass der Effect-Executor einen unsicheren Aufruf ablehnen würde.

## Incident-fähige Observability {#incident-ready-observability}

Speichern Sie für jede wesentliche Werkzeuganfrage eine geschwärzte Spur mit:

- Task- und Session-Identifikatoren;
- authentifiziertem Aufrufer und Richtlinienrevision;
- normalisierter Aktion und Digest der Argumente;
- Freigabe- oder Ablehnungsentscheidung;
- Werkzeug- bzw. Server-Version;
- externem Nachweis oder Abgleichstatus.

Schützen Sie diese Daten: Andernfalls kann Observability denselben Datenabflusspfad erzeugen, den der Agent eigentlich vermeiden sollte.

## Stolperfallen {#gotchas}

- **Injection-Filterung ist kein Berechtigungssystem.** Neuartige Anweisungen können Textmuster umgehen. **Abhilfe:** Autorisierung und Scope erzwingen, nachdem das Modell einen Aufruf vorgeschlagen hat.
- **Eine Sandbox kann weitreichende Berechtigungen enthalten.** Eingebundene Tokens und großzügiger Egress können die Dateisystemisolation aushebeln. **Abhilfe:** Credentials, Pfade, Prozesse und Ziele gemeinsam minimieren.
- **Ein Werkzeug kann allein sicher, in einer Kette aber unsicher sein.** Lesen, Kodieren und Senden können Daten exfiltrieren, ohne dass ein einzelnes Werkzeug „gefährlich“ wäre. **Abhilfe:** End-to-End-Aktionspfade und Richtlinien für ausgehende Kommunikation modellieren.
- **Speicher erzeugt verzögerte Angriffe.** Eine vergiftete Notiz kann künftige Sitzungen beeinflussen. **Abhilfe:** Herkunft, Ablauf und Review an Speicherschreibvorgänge binden.
- **Ein Wiederholungsversuch kann Schaden verdoppeln.** Timeouts verbergen, ob der externe Dienst gehandelt hat. **Abhilfe:** Idempotenz vor der Wirkung reservieren und vor einer Wiederholung abgleichen.

## Quellen {#sources}

- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [Model Context Protocol tools](https://modelcontextprotocol.io/specification/latest/server/tools)
- [Model Context Protocol authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

## Siehe auch {#see-also}

- [[agent-safety-alignment]]
- [[agent-security]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[social-media-mcp-tools]]

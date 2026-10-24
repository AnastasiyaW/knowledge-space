---
title: "Sicherheit und Schutz von Agenten"
description: "Bedrohungsmodellierung und Kontrollen für LLM-Agenten über Prompts, Tools, Speicher, Identitäten, Lieferkette und Observability"
level: 3
source_sha256: 5ae1808b1dbc505fb594077149225f007b4b2e7da2e0391aecbebdcae8203626
translation: machine
translated_at: '2026-10-24'
---
# Sicherheit und Schutz von Agenten (September 2026) {#agent-security-and-safety-september-2026}

Versionskontext: Verwenden Sie die aktuelle OWASP-Leitlinie für agentische Anwendungen, die aktuelle Sicherheitsdokumentation der Anbieter und die tatsächlich eingesetzten Protokollrevisionen. Bedrohungsmodelle müssen überprüft werden, wann immer sich Tools, Datenquellen, Identitäten oder das Speicherverhalten ändern.

Das Risiko eines Agenten entsteht aus der Kombination von nicht vertrauenswürdigen Inhalten, Modellentscheidungen und Seiteneffekten. Ein Modell kann hilfreich sein und dennoch dazu verleitet werden, eine autorisierte Fähigkeit zu missbrauchen. Sicherheit liegt daher in der Systemgrenze und nicht allein in der Formulierung des Prompts.

## Bedrohungsmodell {#threat-model}

Erfassen Sie jede Vertrauensgrenze:

| Oberfläche | Typische Bedrohung | Erforderliche Kontrolle |
|---|---|---|
| Benutzereingabe | Direkte Prompt-Injection, unsichere Anfrage | Eingaberichtlinie, Prüfung des Geltungsbereichs, Ratenbegrenzung |
| Abgerufene Web-/Dokumentinhalte | Indirekte Anweisungen, vergiftete Fakten | Als Daten behandeln, Herkunftsnachweis, Isolierung von Aktionen |
| Tool-Metadaten / Skills | Irreführende Beschreibung, Kompromittierung der Lieferkette | Identität, Überprüfung, fixierte Revision, Allowlist |
| Langzeitspeicher | Vergiftung von Kontext oder Speicher | Schreibberechtigung, Herkunftsnachweis, Ablauf, Überprüfung |
| Tool-Ausführung | Übermäßiger Geltungsbereich, Parametermissbrauch, Datenabfluss | Serverseitige Autorisierung, Schemas, minimale Berechtigungen |
| Agent-zu-Agent-Austausch | Zu weit gefasster Kontext, verwirrte Berechtigung | Typisierte Übergabe, Identität, Richtlinie pro Aktion |
| Telemetrie | Offenlegung sensibler Ein- und Ausgaben | Schwärzung, Aufbewahrung, Zugriffskontrollen |

Das OWASP Top 10 for Agentic Applications 2026 ist eine nützliche Taxonomie, ersetzt aber keine systemspezifische Überprüfung von Missbrauchsszenarien.

## Nicht verhandelbare Grenze {#non-negotiable-boundary}

```text
untrusted content -> model proposal -> schema validation -> policy authorization
                  -> scoped tool execution -> immutable receipt -> response
```

Nicht vertrauenswürdige Inhalte dürfen die Antwort eines Modells beeinflussen, dürfen aber niemals dessen Berechtigungen, Tool-Allowlist, Identität oder Freigabestatus direkt verändern.

## Tool-Autorisierung {#tool-authorization}

Jeder Tool-Aufruf benötigt eine deklarierte Klasse von Seiteneffekten und einen serverseitig durchgesetzten Geltungsbereich.

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolRequest:
    actor_id: str
    tenant_id: str
    action: str
    resource_id: str
    arguments: dict[str, Any]


def authorize_export(request: ToolRequest) -> None:
    if request.action != "export_report":
        raise PermissionError("action is not available")
    if not request.resource_id.startswith(f"{request.tenant_id}:"):
        raise PermissionError("resource is outside tenant scope")
    if "destination" not in request.arguments:
        raise ValueError("destination is required")
```

Nach der Autorisierung validieren Sie die vollständige typisierte Eingabe und binden die Dienstanmeldedaten an die für diese Aktion minimal notwendigen Berechtigungen. Geben Sie dem Modell kein breit privilegiertes Token und bitten Sie es, vorsichtig zu sein.

## Prompt-Injection und abgerufene Inhalte {#prompt-injection-and-retrieved-content}

Prompt-Injection ist ein Problem der Eingabeintegrität. Defensive Prompts und Klassifikatoren können das Risiko senken, können aber nichtvertrauenswürdigen Text nicht vertrauenswürdig machen.

Kontrollen:

1. Kennzeichnen Sie Daten von Benutzern, Webseiten, E-Mails, Dateien und Tool-Antworten als nicht vertrauenswürdig.
2. Halten Sie nicht vertrauenswürdigen Text außerhalb von Anweisungen und Richtliniendefinitionen.
3. Verlangen Sie einen ausdrücklichen Benutzer- bzw. Autorisierungskontext, bevor externe Seiteneffekte entstehen.
4. Beschränken Sie in jeder Phase, welche Tools verfügbar sind; stellen Sie nicht das gesamte Tool-Universum bereit.
5. Prüfen Sie die Herkunft der Quellen und die Zitate, bevor Sie sich auf abgerufene Aussagen stützen.
6. Testen Sie mehrstufige indirekte Injection-Szenarien in einer kontrollierten Umgebung.

Kopieren Sie niemals Anweisungen aus einem abgerufenen Dokument ohne Prüfung in einen Systemprompt, einen Speichereintrag oder einen Skill.

## Speicher- und Kontextintegrität {#memory-and-context-integrity}

Langzeitspeicher ist eine beschreibbare Angriffsfläche. Jeder Eintrag benötigt eine Schreiberidentität, einen Quellverweis, einen Zeitstempel, ein Schema, einen Mandantenbereich, Konfidenz-/Herkunftsangaben, eine Aufbewahrungsregel und optional einen Freigabestatus.

Verwenden Sie ein explizites Übernahme-Gate:

```json
{
  "memory_id": "mem_01J...",
  "writer": "service:knowledge-curator",
  "source_ref": "artifact://approved/...",
  "tenant_id": "tenant_42",
  "classification": "internal",
  "expires_at": "2026-12-31T00:00:00Z",
  "promotion_state": "approved"
}
```

Ein vom Modell erzeugter Vorschlag ist nicht automatisch für dauerhaften Speicher geeignet. Er muss dieselben Quell- und Autorisierungsregeln erfüllen wie jeder andere Inhalt.

## Identität, Geheimnisse und Lieferkette {#identity-secrets-and-supply-chain}

- Geben Sie jeder Agenten- bzw. Dienstidentität nur die Berechtigungen, die sie benötigt.
- Bewahren Sie Zugangsdaten in einem Geheimnisverwalter oder über delegierte Workload-Identität auf, niemals in Prompts, Tool-Beschreibungen, Logs oder Speicher.
- Fixieren Sie Abhängigkeiten sowie Tool- und Skill-Revisionen; prüfen Sie die Herkunft vor der Installation.
- Trennen Sie schreibgeschützte Recherche-Zugangsdaten von schreibfähigen Betriebs-Zugangsdaten.
- Deaktivieren Sie externe Nachrichtenübermittlung, Zahlungen, destruktive Schreibvorgänge und Rechteänderungen oder verlangen Sie dafür eine Freigabe.
- Rotieren Sie eine Agentenidentität oder widerrufen Sie sie, wenn ein Tool, ein Skill oder eine Speicherquelle im Verdacht steht, kompromittiert zu sein.

Git-Worktrees helfen, Branch-Checkouts zu isolieren, sind aber keine Sandbox für Netzwerk, Zugangsdaten, Prozesse oder eingebundenen Speicher. Ergänzen Sie dort, wo diese Grenzen erforderlich sind, Kontrollen auf Betriebssystem-, Container- oder Cloud-Ebene.

## Observability, Reaktion und Red Teaming {#observability-response-and-red-teaming}

Protokollieren Sie geschwärzte Modell- und Tool-Ereignisse mit Task-ID, Richtlinienrevision, Akteur- bzw. Mandantenbereich, Tool-Entscheidung, Quittung und Endzustand. Alarmieren Sie bei abgelehnten risikoreichen Versuchen, unerwartetem Datenvolumen, wiederholten Versuchen, mandantenübergreifenden Zugriffsversuchen und unerwarteten Zielen.

Ein Reaktionsplan benötigt einen Notausschalter für die Tool-Ausführung, den Widerruf von Identitäten, die Sicherung von Traces, die Quarantäne betroffener Speichereinträge, das Zurücksetzen von Abhängigkeiten sowie eine dokumentierte Neuvalidierung, bevor die Autonomie wieder aktiviert wird.

Führen Sie Red Teaming am realen Ablauf durch: direkte und indirekte Injection, vergifteten Speicher, fehlerhafte Tool-Ausgaben, doppelte Anfragen, kompromittierte Metadaten von Abhängigkeiten, zu weit gefasste Übergaben und Versuche, Verweigerungen zu umgehen.

## Stolperfallen {#gotchas}

- **Systemprompts sind keine Autorisierungsschicht.** Sie können ignoriert oder manipuliert werden. **Abhilfe:** Erzwingen Sie Autorisierung und Kontrollen für Seiteneffekte im Code, bevor ein Tool ausgeführt wird.
- **Abgerufene Dokumente sind keine Anweisungen.** Sie können feindseligen Text oder irreführende Metadaten enthalten. **Abhilfe:** Isolieren Sie sie als nicht vertrauenswürdige Daten und verlangen Sie Prüfungen von Quelle und Herkunft.
- **Speicher macht Kompromittierung dauerhaft.** Ein vergifteter Eintrag kann spätere Läufe beeinflussen. **Abhilfe:** Verwenden Sie Schreibberechtigungen, unveränderliche Herkunftsnachweise, Ablauffristen und einen Quarantäne- und Prüfpfad.
- **Guardrails können Daten über die Telemetrie preisgeben.** Traces können rohe Prompts und Tool-Eingaben erfassen. **Abhilfe:** Testen Sie Schwärzung, Aufbewahrung und Zugriffskontrollen mit repräsentativen sensiblen Inhalten.
- **Worktrees sind keine Sicherheits-Sandbox.** Sie teilen Host-Ressourcen und Zugangsdaten, sofern nicht gesondert eingeschränkt. **Abhilfe:** Isolieren Sie Zugangsdaten, Netzwerk, Prozesse und Speicher auf der Umgebungsebene.

## Quellen {#sources}

- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenAI Agents SDK: guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [Git worktree documentation](https://git-scm.com/docs/git-worktree)

## Siehe auch {#see-also}

- [[agent-fundamentals]]
- [[agent-memory]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[production-patterns]]

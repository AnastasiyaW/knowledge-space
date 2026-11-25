---
title: "Produktions-LLM- und Agenten-Muster (September 2026)"
category: techniques
tags: [llm-agents, production, evaluation, observability, human-in-the-loop]
level: 3
source_sha256: ec7ea06ab1c821d74787a99f1ee16d57c2ed68465790c9a18502731ace1b54f5
translation: machine
translated_at: '2026-10-24'
---
# Produktions-LLM- und Agenten-Muster (September 2026) {#production-llm-and-agent-patterns-september-2026}

Überprüft am 03.09.2026. Ein Produktions-LLM-System ist eine Anwendung mit probabilistischen Komponenten. Datenhoheit, Seiteneffekte, Evaluierung und Wiederherstellung müssen im Anwendungscode explizit gemacht werden; sie sollten nicht allein durch die Formulierung des Prompts kodiert werden.

## Zentrale Steuerungsebene {#core-control-plane}

| Belang | Produktionsvertrag |
|---|---|
| Eingabe | Typisiertes Arbeitselement, Quellenreferenz und Richtlinie zur Datenklassifizierung |
| Modell | Exakte Konfiguration von Modell/Anbieter und Prompt-Version |
| Werkzeuge | Allowlist, Schema, Timeout, Identität und Richtlinie für Seiteneffekte |
| Zustand | Run-ID, Wiederholungszähler, Checkpoint und Idempotenzschlüssel |
| Ausgabe | Schema-Validierung und aufgabenspezifische Akzeptanzkriterien |
| Nachweise | Werkzeugbelege, Quellenreferenzen, Ergebnis des Validators, Entscheidung des Prüfers |
| Betrieb | Trace, Budget, Fehlerkategorie, Verantwortliche Person und Rollback-Pfad |

Das OpenAI Agents SDK unterscheidet zwischen codegesteuerter und modellgesteuerter Orchestrierung. Verwenden Sie Code, wenn die Entscheidung eine Richtlinie, eine Autorisierung, ein Budget oder eine deterministische Routing-Regel ist. [Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)

## Retrieval ist ein Datenprodukt {#retrieval-is-a-data-product}

Retrieval ist angebracht, wenn die Antwort auf sich ändernden oder proprietären Inhalten beruhen muss. Behandeln Sie es als eigenständiges System mit Ingestion, Zugriffskontrolle, Dokumentversionierung, Retrieval-Evaluierung und Prüfung der Zitate.

| Frage | Direkter Kontext ist ausreichend, wenn | Retrieval ist erforderlich, wenn |
|---|---|---|
| Quellenmenge | Sie klein, bekannt und versioniert ist | Sie groß, sich ändernd oder nutzerspezifisch ist |
| Autorität | Ein kontrolliertes Artefakt die Wahrheit ist | Mehrere Quellen Rangbildung und Rückverfolgbarkeit benötigen |
| Fehlermodus | Fehlender Kontext offensichtlich ist | Falsches oder veraltetes Retrieval unbemerkt in die Irre führen kann |

Behaupten Sie niemals, ein Vektorsuchergebnis sei maßgeblich, nur weil es abgerufen wurde. Speichern Sie die Identität und Version der Quelle zusammen mit der Antwort.

## Deterministische Validierung {#deterministic-validation}

Halten Sie Validatoren klein und aufgabenspezifisch. Dieses Python-3.11+-Beispiel validiert einen Kandidaten, der eine bekannte Quelle zitieren und einen erlaubten Status verwenden muss.

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    status: str
    source_id: str
    summary: str


def validate(candidate: Candidate, allowed_sources: set[str]) -> list[str]:
    errors: list[str] = []
    if candidate.status not in {"draft", "approved"}:
        errors.append("invalid_status")
    if candidate.source_id not in allowed_sources:
        errors.append("unknown_source")
    if not candidate.summary.strip():
        errors.append("empty_summary")
    return errors


if __name__ == "__main__":
    item = Candidate("draft", "source-42", "Verified change summary.")
    print(validate(item, {"source-42"}))
```

Verwenden Sie einen separaten menschlichen oder unabhängigen Evaluator für redaktionelle Beurteilung, Sicherheitsprüfung oder semantische Korrektheit, die ein deterministischer Validator nicht messen kann.

## Seiteneffekte benötigen einen Genehmigungszustand {#side-effects-need-an-approval-state}

```text
PENDING -> GENERATED -> VALIDATED -> AWAITING_APPROVAL -> PUBLISHED
                       |                    |
                       v                    v
                     REJECTED             HELD
```

Veröffentlichung, E-Mail, Zahlung, Datenmutation und externe Tickets sollten einen expliziten Genehmigungszustand verwenden. Ein vom Modell erzeugter Satz ist niemals der Nachweis für einen Seiteneffekt.

## Observability {#observability}

Verfolgen Sie Workflows, Modellschritte, Werkzeuge, Validatoren und Genehmigungen unter einer gemeinsamen Run-ID. Das Projekt GenAI Semantic Conventions deckt Spans, Metriken und Events für GenAI-Clients und MCP ab; ergänzen Sie anwendungsspezifische, namensraumbasierte Felder für die Identität von Arbeitselementen und Nachweisen. [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai)

Minimale Fragen für Betreiber:

- Welcher Run und welche Konfiguration haben diese Ausgabe erzeugt?
- Welche Quellen und Werkzeuge haben sie beeinflusst?
- Hat ein Validator oder Genehmiger sie akzeptiert?
- Ist eine externe Aktion abgeschlossen, fehlgeschlagen oder unsicher geblieben?
- Kann dasselbe Arbeitselement wiederholt werden, ohne einen Seiteneffekt zu duplizieren?

## Fallstricke {#gotchas}

- **Problem: Standardmäßige Erfassung roher Prompts und Werkzeugergebnisse.** Traces werden zu einem sekundären Speicher für sensible Daten. **Lösung:** Standardmäßig nur Referenzen und freigegebene Metadaten speichern; für vollständige Payloads eine kontrollierte Erfassung verlangen.
- **Problem: Ein Timeout wie einen sauberen Fehler behandeln.** Die externe Aktion könnte bereits abgeschlossen sein. **Lösung:** Idempotenzschlüssel persistieren und den Beleg des Anbieters abgleichen, bevor erneut versucht wird.
- **Problem: Einem Modell die Wahl einer Governance-Aktion überlassen.** Eine Anweisung ist kein Zugriffskontrollsystem. **Lösung:** Genehmigungs-, Budget- und Veröffentlichungsschranken im deterministischen Code erzwingen.
- **Problem: Eine erfolgreiche Modellantwort als produktionsreif bezeichnen.** Ihr können Quellen, Validierung und Wiederherstellungsverhalten fehlen. **Lösung:** Einen testbaren Akzeptanzvertrag und betriebliche Nachweise verlangen.

## Siehe auch {#see-also}

- [[agent-observability-dashboards]]
- [[agent-evaluation]]
- [[function-calling]]
- [[rag-pipeline]]
- [[tool-use-patterns]]

## Quellen {#sources}

- [OpenAI Agents SDK: Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
- [Claude: How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)

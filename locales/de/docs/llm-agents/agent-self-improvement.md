---
title: "Selbstverbesserung von Agenten"
description: "Eine sichere Experimentschleife zur Verbesserung von Agenten-Prompts, Tools, Code und Richtlinien mit eingefrorenen Evaluierungen und Rollback"
level: 3
source_sha256: 3008cdc49d8be7a88fe016b21d0ee35a8ed0ef617c4e2fe4196150360e7d58ba
translation: machine
translated_at: '2026-10-24'
---
# Selbstverbesserung von Agenten (September 2026) {#agent-self-improvement-september-2026}

Versionskontext: Behandle eine Verbesserungsschleife als experimentelles System. Ihre Metrik, Evaluierungsmenge, Schutzbedingungen, Kandidatenrevision und Rollback-Regel sind versionierte Eingaben; die Änderung einer dieser Größen startet eine neue Experimentreihe.

Ein Agent sollte sich nicht selbst für verbessert erklären. Verbesserung ist ein gemessener Vergleich mit einer Baseline auf einer zurückgehaltenen Evaluierung, ergänzt um Sicherheits- und Betriebsprüfungen.

## Was verbessert werden darf {#what-may-improve}

| Ziel | Sichere Ausgangsmethode | Erforderlicher Nachweis |
|---|---|---|
| Prompt/Anweisungen | Eine eng begrenzte Änderung | Eingefrorene Aufgaben-Evaluierung und Ausgabeprüfung |
| Tool-Beschreibungen/Allowlist | Tool-Menge reduzieren oder präzisieren | Korrektheit der Tool-Nutzung und Tests verweigerter Aktionen |
| Retrieval-Richtlinie | Eine Änderung an Retrieval/Reranking | Quellenbasierte Antworten und Zitat-Evaluierung |
| Workflow-Code | Isolierte Branch-/Worktree-Änderung | Tests, Build, unabhängige Prüfung |
| Modellauswahl/Konfiguration | Kandidaten vergleichen | Gleiche Suite, Protokoll zu Latenz/Kosten/Sicherheit |
| Richtlinie für Langzeitgedächtnis | Kontrollierter Sandbox-Test | Tests auf Poisoning, Ablauf, Herkunft, Datenschutz |

Ändere produktiven Quellcode, globale Tools, Zugangsdaten oder Gedächtnis nicht allein auf Grundlage der Selbstreflexion des Modells. Verwende eine isolierte Umgebung und übernimm nur verifizierte Artefakte.

## Minimaler Experimentvertrag {#minimal-experiment-contract}

```json
{
  "experiment_id": "agent-routing-2026-09-03-001",
  "baseline_revision": "git:abc123",
  "candidate_revision": "git:def456",
  "suite_digest": "sha256:...",
  "primary_metric": "accepted_task_rate",
  "guard_metrics": {
    "policy_violations_max": 0,
    "p95_latency_ms_max": 3000,
    "cost_per_task_max": 0.05
  },
  "decision": "pending"
}
```

Eine Metrik ohne Schutzbedingung ist anfällig für Optimierungen, die Sicherheit, Kosten, Latenz oder Zuverlässigkeit beschädigen. Ein Kandidat ohne feste Baseline und Suite kann keine kausale Wirkung nachweisen.

## Regel für Behalten/Verwerfen {#keepreject-rule}

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluation:
    primary: float
    policy_violations: int
    p95_latency_ms: int
    cost_per_task: float


def accept(
    baseline: Evaluation,
    candidate: Evaluation,
    *,
    latency_limit: int,
    cost_limit: float,
) -> bool:
    return (
        candidate.primary > baseline.primary
        and candidate.policy_violations == 0
        and candidate.p95_latency_ms <= latency_limit
        and candidate.cost_per_task <= cost_limit
    )
```

Eine belastbare Evaluierung benötigt außerdem Konfidenzintervalle oder wiederholte Läufe, wenn die Stichprobenvarianz erheblich ist. Der konservative Standard ist, Gleichstände und Verschlechterungen zu verwerfen.

## Kontrollierte Verbesserungsschleife {#controlled-improvement-loop}

1. Friere die Akzeptanzkriterien, die Testsuite und den Baseline-Beleg ein.
2. Erzeuge oder wähle genau eine Kandidatenänderung.
3. Wende sie nur in einem isolierten Branch/Worktree oder einer Sandbox an.
4. Führe deterministische Tests sowie dieselbe Agenten-Evaluierungssuite aus.
5. Lass einen unabhängigen Evaluator die Nachweise und die ungünstigen Fälle prüfen.
6. Behalte den Kandidaten nur, wenn er die primäre Metrik verbessert und jede Schutzbedingung erfüllt.
7. Bewahre den verworfenen Kandidaten und seinen Beleg auf; überschreibe die Historie nicht stillschweigend.

Die Grundidee agentengetriebener Forschungsprojekte wie autoresearch ist nur dann nützlich, wenn die Evaluierung real und der Änderungsumfang kontrolliert ist. Sie ist keine Lizenz für unbegrenzte Selbstmodifikation.

## Reflexion und Trajektoriedaten {#reflection-and-trajectory-data}

Die Selbstreflexion des Modells kann helfen, Hypothesen zu erzeugen: Eine fehlgeschlagene Aufgabe kann auf fehlenden Tool-Kontext, einen mehrdeutigen Prompt, einen fehlerhaften Parser oder eine unvollständige Stoppbedingung hindeuten. Sie ist jedoch keine Grundwahrheit.

Speichere einen strukturierten Fehlerdatensatz:

```json
{
  "task_id": "eval_431",
  "revision": "git:def456",
  "terminal_state": "failed",
  "evidence": ["tool receipt: timeout", "output schema: invalid"],
  "hypothesis": "retry policy is missing an eligible timeout branch",
  "review_state": "unverified"
}
```

Nutze die Nachweise, um einen testbaren Kandidaten abzuleiten. Trainiere nicht auf modellverfassten Erklärungen und übernimm sie nicht, bevor die zugrunde liegenden Fakten geprüft sind.

## Gestaltung der Evaluierung {#evaluation-design}

Eine nützliche Suite enthält:

- repräsentative normale Aufgaben;
- schwierige Grenzfälle und Wiederherstellungsaufgaben;
- fehlerhafte Eingaben und Fälle mit problematischen Tool-Ergebnissen;
- Richtlinienverweigerungen und Versuche adversarieller Injection;
- in der Produktion entdeckte Regressionsfälle;
- Messungen von Kosten, Latenz und Wiederholungsversuchen.

Halte eine Holdout-Menge vor, die kein Optimierer und keine Prompt-Tuning-Schleife einsehen kann. Nimm nach jedem größeren Release neue verborgene Beispiele in die Holdout-Menge auf.

## Grenze der Übernahme {#promotion-boundary}

Ein Kandidat kann folgende Stufen durchlaufen:

```text
sandbox experiment -> local validation -> independent review
                   -> staged/canary evaluation -> production release
```

Rückmeldungen aus der Produktion sind Evidenz, aber keine Befugnis für ein System, sich selbst umzuschreiben. Jede Übernahme bleibt an Änderungskontrolle und Rollback-Fähigkeit gebunden.

## Stolperfallen {#gotchas}

- **Der Agent kann die Metrik statt des Ergebnisses optimieren.** Ein eng gefasster Scorer lässt sich austricksen. **Abhilfe:** Mehrere Schutzbedingungen, adversarielle Fälle und manuelle Prüfung repräsentativer Ausgaben verwenden.
- **Testdaten-Leakage erzeugt scheinbare Verbesserungen.** Wiederholte Optimierung gegen dieselbe sichtbare Menge führt schließlich zu Überanpassung. **Abhilfe:** Eine verborgene Holdout-Menge bewahren und sie ausschließlich als Freigabe-Evidenz behandeln.
- **Mehrere gleichzeitige Änderungen zerstören die Kausalität.** Ein besserer Score zeigt nicht, welche Änderung geholfen hat. **Abhilfe:** Pro Experiment genau eine eng begrenzte Variable ändern und den vollständigen Beleg aufbewahren.
- **Modellreflexionen können Ursachen erfinden.** Plausible Erklärungen sind keine Diagnosen. **Abhilfe:** Hypothesen vor jeder Änderung mit Logs, Belegen oder reproduzierbaren Tests verknüpfen.
- **Ein Rollback ohne Artefaktintegrität ist kein Rollback.** Veränderbare Branches und überschriebene Dateien verlieren den letzten bekannten guten Zustand. **Abhilfe:** Unveränderliche Commit-IDs und versionierte Evaluierungsprotokolle verwenden.

## Quellen {#sources}

- [OpenAI API: working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
- [Git worktree documentation](https://git-scm.com/docs/git-worktree)

## Siehe auch {#see-also}

- [[agent-evaluation]]
- [[agent-design-patterns]]
- [[autonomous-agent-evolution]]
- [[production-patterns]]
- [[llm-fine-tuning-practical]]

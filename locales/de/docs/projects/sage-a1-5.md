---
title: "Sage-A1.5: sage-a1-5-release — Sage A1 5 Release"
category: "projects"
date: 2026-10-22
tags: ["project", "sage-a1-5", "sage-a1-5-release"]
aliases: ["Sage-A1.5: sage-a1-5-release"]
level: 2
source_sha256: 565f221edffe659f96a7fdb836597b250480c7eac74c779098dee491d48ee3f5
translation: machine
translated_at: '2026-10-24'
---
# Sage-A1.5: sage-a1-5-release — Sage A1 5 Release {#sage-a15-sage-a1-5-release-sage-a1-5-release}

**Entwicklungslinie:** project:sage-a1-5 · Thread sage-a1-5-release  
**Letztes Ereignis:** 2026-10-22 · 2 datierte seit 2026-10-22 · **Recherchiert:** 2026-10-23 · Konfidenz: mittel

## Was es ist {#what-it-is}

Sage-A1.5 ist ein Open-Weight-Foundation-Modell für agentische Aufgaben, basierend auf einer Mixture-of-Experts-Architektur mit 35B Parametern. Es richtet sich an Forschende und Softwareingenieure, die langfristige Aufgaben ausführen, und konkurriert direkt mit proprietären Reasoning-Modellen.

- **Parallele Subagenten:** orchestriert sie, jeweils in einem isolierten Ausführungskontext.
- **Selbstverifikation:** prüft sich innerhalb seiner Gedankenkette selbst, ohne externes Reward-Modell.
- **Wissenschaftliche Entdeckung:** führt Workflows über verschiedene Disziplinen hinweg aus.
- **Serving:** stellt eine OpenAI-kompatible API über vLLM oder SGLang bereit.

Pro Forward-Pass sind 3B von 35B Parametern aktiv. Der Kontext beträgt nativ 256K Token und lässt sich über YaRN auf 512K erweitern. Bei starker paralleler Subagenten-Last bestimmen der Routing-Overhead der MoE-Architektur und die Speicherkapazität die Grenze.

Es handelt sich um eine effiziente, selbst hostbare Open-Basis für komplexe agentische Pipelines, die sich während einer Trajektorie selbst korrigieren müssen.

## Entwicklungslinie {#development-line}

- **2026-10-22 — Shanghai AI Lab veröffentlicht das agentische Modell Sage-A1.5.** Es ist ein agentisches MoE-Modell mit 35B Parametern, aufgebaut auf Qwen3.6-35B-A3B und Agents-A1. Angekündigt wurde es mit einem Kontextfenster von 262K Token und OpenAI-kompatiblem Serving über SGLang oder vLLM. Berichtete Ergebnisse: GAIA 95,1, XBench-DS 92,0, SWE-bench Pro 61,2, MLE-Lite 65,2.
- **2026-10-22 — weitere Berichterstattung zu diesem Datum.**
  - Das Modell wird unter der Apache-2.0-Lizenz von der InternScience-Gruppe des Shanghai AI Lab veröffentlicht. Pro Token sind 3B von insgesamt 35B Parametern aktiv. Es ergänzt die native Delegation von Multi-Agent-Aufgaben durch parallele, isolierte Subagenten. (2026-10-22) — <https://huggingface.co/InternScience/Sage-A1.5>
  - Die Model Card beschreibt eine in die Gedankenkette eingebaute Selbstverifikation. Das Modell korrigiert sich damit während der Ausführung ohne externe Verifikatoren. Der Kontext geht über die native Grenze von 256K hinaus bis zu 512K Token via YaRN. (2026-10-22) — <https://huggingface.co/InternScience/Sage-A1.5>

## Was sich geändert hat {#what-changed}

Die Agents-A1-Reihe setzte auf Dense-Modelle; Sage-A1.5 ist ein sparsames Mixture of Experts auf Basis von Qwen3.6-35B-A3B. Sequenzielle Single-Agent-Pipelines wurden durch die dynamische Delegation an Subagenten mit isolierten Kontexten ersetzt. Die Fehlerkorrektur innerhalb einer Trajektorie stützte sich früher auf externe Critic-Modelle; heute ist sie in die Gedankenkette integriert. Der Kontext wuchs von üblichen Fensterlängen auf nativ 256K, skalierbar auf 512K mit YaRN.

## So wird es verwendet {#how-to-use-this}

1. Lade die Gewichte aus dem Repository InternScience/Sage-A1.5 auf Hugging Face oder ModelScope herunter.
  — <https://huggingface.co/InternScience/Sage-A1.5>
2. Deploye das Modell mit vLLM oder SGLang unter Verwendung der Standardkonfiguration für Qwen-MoE, sodass ein OpenAI-kompatibler API-Endpunkt bereitgestellt wird.
  — <https://huggingface.co/InternScience/Sage-A1.5>
3. Aktiviere das Starten von Subagenten in der Agent-Runtime, sodass das Modell Teilaufgaben parallel auf isolierte Kontexte verteilen kann.
  — <https://huggingface.co/InternScience/Sage-A1.5>
4. Aktiviere die native Verifikation in den Generierungsparametern oder im System-Prompt, damit das Modell sich selbst prüft und bei langen Trajektorien Fehler behebt.
  — <https://huggingface.co/InternScience/Sage-A1.5>

## Bewährte Praktiken {#best-practices}

- Gib parallelen Untersuchungszweigen eigene Subagenten-Kontexte, damit störende Zwischenausgaben von Tools den Root-Agenten nicht ablenken.
  — <https://huggingface.co/InternScience/Sage-A1.5>
- Wende YaRN-Skalierung an, wenn ein Repository oder eine Menge von Papers das native Fenster von 256K Token überschreitet.
  — <https://huggingface.co/InternScience/Sage-A1.5>
- Betreibe FP8/INT4-Quantisierungen mit SGLang oder vLLM, um den Speicherbedarf zu senken und das effiziente MoE-Routing beizubehalten.
  — <https://huggingface.co/InternScience/Sage-A1.5>

## Abgelöst durch dieses Release {#superseded-by-this}

- Dense-Architekturen der Agents-A1-Reihe und sequenzielle Single-Agent-Pipelines werden durch die MoE-Architektur von Sage-A1.5 mit nativer Subagenten-Orchestrierung abgelöst.
  — <https://huggingface.co/InternScience/Sage-A1.5>
- Externe Critic-Modelle zur Trajektorie-Selbstkorrektur werden durch die integrierte Verifikation über die Gedankenkette von Sage-A1.5 abgelöst.
  — <https://huggingface.co/InternScience/Sage-A1.5>

## Noch unbekannt {#still-unknown}

- Die Resonanz der Community und praktische Fehlerberichte aus Praktiker-Foren konnten nicht geprüft werden: Die Suchergebnisse führten nur zu Weiterleitungsseiten.
- Speicherbandbreitenbedarf und Leistung auf verschiedenen heimischen Hardware-Beschleunigern wurden bisher nicht unabhängig gemessen.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/InternScience/Sage-A1.5 | InternScience/Sage-A1.5 · Hugging Face | 2026-10-23 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** project:sage-a1-5, Thread sage-a1-5-release, 2 datierte Ereignisse vom 2026-10-22 bis 2026-10-22.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

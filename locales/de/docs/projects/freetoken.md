---
title: "FreeToken"
category: projects

tags: [freetoken, freetoken-development, project]
aliases: ["FreeToken"]
level: 2
source_sha256: 242ce2cdc9b5d5683400ed42e84d5e77d319a1dc9bf93e7640c3e2c0f597e6e1
translation: machine
translated_at: '2026-10-24'
---
# FreeToken {#freetoken}

**Entwicklungslinie:** `project:freetoken` · Thread `freetoken-development`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

FreeToken ist ein Open-Source-Inferenzserver zum Betrieb großer Mixture-of-Experts-Modelle auf Consumer-PCs als Alternative zu vLLM und SGLang.

- OpenAI-, Anthropic- und Responses-APIs für Client-Kompatibilität.
- CPU-GPU-Offloading, Expert-Cache und das FTW-Gewichtsformat, um Modelle in den Speicher zu bringen.
- CLI-, Desktop-App- und Coding-Agent-Anbindungen für lokale Workflows.

Das offizielle Setup erfordert x86_64, NVIDIA Ampere/RTX 30 oder neuer, Treiber r580+ und ausreichend freien Systemspeicher für die Experten. Das Projekt ändert sich schnell, daher sollten Sie Ihre konkrete GPU und Ihr Modell testen, bevor Sie sich darauf verlassen.

## Entwicklungslinie {#development-line}

- Das datierte Ereignis ist noch nicht ausgearbeitet; das bisher Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

- 2026-08-19: GitHub-Release v0.1.2 wurde unter dem Tag `9db1a39` mit sieben Assets veröffentlicht, und die PyPI-Veröffentlichung wurde korrigiert.
- 2026-08-23: Die Maintainer veröffentlichten ein FAQ und eine Roadmap; der offizielle Support zielt auf NVIDIA/x86_64, während macOS, AMD, aarch64, Tensor-Parallelismus, Vision und erweiterte GGUF-Unterstützung weiterhin geplant sind.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-08-19 lässt sich allein aus den datierten Links kein Workflow-Wechsel für die Praxis belegen; recherchieren Sie die Projektseite und das Repository, bevor Sie sich auf FreeToken verlassen.

1. Prüfen Sie die Anforderungen für Linux x86_64, NVIDIA-GPU, Treiber r580+ und Python 3.10+, erstellen Sie dann eine Umgebung und installieren Sie `freetoken[accel]` mit uv.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md>
2. Führen Sie `ft serve --model <local-path-or-HF-id>` aus; standardmäßig lauscht der Server auf `127.0.0.1:1919`.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>
3. Überprüfen Sie die Installation mit `ft --version` und einer Anfrage an `/v1/chat/completions` und verbinden Sie dann einen OpenAI-kompatiblen Client.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md>

## Best Practices {#best-practices}

- Testen Sie CPU- und PCIe-Bandbreite mit `ft bench bw`, bevor Sie ein Backend wählen, um das MoE-Offloading zu kalibrieren.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>
- Planen Sie den freien RAM anhand der Größe der Expert-Gewichte für MoE-Modelle; für das bf16-Modell Qwen3.6-35B-A3B nennt das FAQ etwa 70 GB.
  — <https://github.com/FlashML-org/FreeToken/issues/84>
- Machen Sie den Server nicht ohne explizite Konfiguration im Netzwerk erreichbar; der Standard-Bind ist `127.0.0.1`. Bestätigen Sie die Antwort zuerst lokal.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>

## Hiermit abgelöst {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die primären Release-Assets bestätigen weder den Funktionsumfang noch die Reife des Windows-Desktop-Builds; die offiziellen pip-Anweisungen decken Linux ab.
- Die Aussagen im Paper zu Leistung und Hardwareunterstützung fehlen unabhängige Benchmarks für bestimmte Modelle, GPUs oder Workloads.
- event_findings_placeholder

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/FlashML-org/FreeToken/releases | FreeToken releases | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken | FlashML-org/FreeToken README | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md | FreeToken installation guide | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md | FreeToken CLI reference | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/issues/84 | FreeToken FAQ | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/issues/79 | FreeToken Roadmap (2026) | 2026-09-05 |
| https://arxiv.org/abs/2608.16157 | FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution | 2026-09-05 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:freetoken`, Thread `freetoken-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-08-19 lässt sich allein aus den datierten Links kein Workflow-Wechsel für die Praxis belegen; recherchieren Sie die Projektseite und das Repository, bevor Sie sich auf FreeToken verlassen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

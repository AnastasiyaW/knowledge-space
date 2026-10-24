---
title: "ComfyUI Sol-Attn — Blackwell- und Triton-Implementierungen"
category: projects
date: 2026-08-07
tags: [blackwell-and-triton-implementations, comfyui-sol-attn, project]
aliases: ["ComfyUI Sol-Attn"]
level: 2
source_sha256: d828905bfe197d0eef8806ead92d5e95ed41d4bf65021e31877193f042a1ad5b
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Sol-Attn — Blackwell- und Triton-Implementierungen {#comfyui-sol-attn-blackwell-and-triton-implementations}

**Entwicklungslinie:** `project:comfyui-sol-attn` · Thread `blackwell-and-triton-implementations`  
**Letztes Ereignis:** 2026-08-07 · 1 datiert seit 2026-08-07 · **Recherchiert:** 2026-09-05 · Konfidenz: medium

## Was es ist {#what-it-is}

ComfyUI Sol-Attn ist ein Sammelbegriff für zwei Community-Erweiterungen für ComfyUI, die die Attention in MiniMax H3 durch eine spärliche Variante von Sol-Attn ersetzen. — Kijai: experimentelle Triton-Variante, nach eigenen Angaben mit MiniMax H3 auf RTX 4090 und RTX 5090 getestet. — KingGore: Variante für RTX 5090 (SM120), die PyTorch flex_attention verwendet. Einschränkung: KingGores Messung ergab 1,46× bei 4K und 9,00× bei 32K Token gegenüber SDPA nach dem Aufwärmen, und zwar nur für seine Konfiguration MiniMax H3/RTX 5090. Fazit: Das ist ein Werkzeug für A/B-Prüfungen langer H3-Renderings, kein allgemeiner Beschleuniger für ComfyUI.

## Entwicklungslinie {#development-line}

- **2026-08-07 — ComfyUI-Sol-Attn-Implementierungen für Blackwell und Triton wurden verlinkt.** Die Triton-Variante von Kijai und die Blackwell-Variante von KingGore.

## Was sich geändert hat {#what-changed}

2026-07-27 — die erste Version der Sol-Attn-Arbeit wurde veröffentlicht: trainingsfreie spärliche Attention mit Korrektur übersprungener Blöcke. 2026-07-28 — NVIDIA veröffentlichte Upstream-Kernel für Sol-Attn für SM89/SM90/SM100/SM120 sowie Integrationen für HunyuanVideo-13B und Wan2.1-T2V-14B. 2026-08-04 — KingGore ergänzte v2 mit exakter Attention für den Conditioning-Präfix und dichten Schlussschritten; Kijai übernahm eine Korrektur des Imports für GPUs vor SM90. 2026-08-06 — der Upstream-Sol-Engine ergänzte MiniMax H3 auf GB10 und RTX 5090; dabei handelt es sich nicht um ein ComfyUI-Node-Release. 2026-08-07 — der ComfyUI-Zweig legte zwei eigenständige Implementierungen fest: die Triton-Variante von Kijai und die Blackwell-Variante von KingGore. 2026-08-17 — der Upstream-Sol-Engine ergänzte einen optimierten SM89-Kernel für RTX 4090; die Kompatibilität des konkreten Kijai-Nodes bleibt eine eigene Frage.

## Anwendung {#how-to-use-this}

Stand 2026-08-07 sollten Praktiker, die ComfyUI Sol-Attn evaluieren, die auf Blackwell ausgerichtete Implementierung von der auf Triton ausgerichteten unterscheiden und die Kompatibilität der Umgebung prüfen, bevor sie eine der beiden übernehmen.

1. Für MiniMax H3 auf RTX 5090 installieren Sie die Blackwell-Variante in ComfyUI/custom_nodes und starten ComfyUI neu; sie benötigt PyTorch 2.6+ und CUDA 12.x oder 13.x.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>
2. Fügen Sie den Sol-Attn MiniMax H3 Patcher zwischen Load Diffusion Model und KSampler ein.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>
3. Beginnen Sie mit tau=1.0; für die Blackwell-Variante ist der Bereich 0.8–1.5 dokumentiert. Bei Artefakten aktivieren Sie dense_steps oder step_off für einen dichten Schluss und exact_kv für den exakten Conditioning-Präfix.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>
4. Für die Triton-Variante von Kijai beschränken Sie den ersten Test von MiniMax H3 auf RTX 4090 oder RTX 5090 und stimmen start_percent, end_percent und tau bei identischem Seed ab.
  — <https://github.com/kijai/ComfyUI-SolAttn_triton/blob/main/readme.md>

## Bewährte Praktiken {#best-practices}

- Messen Sie nicht den ersten Lauf: Die Triton-Kompilierung findet beim ersten Einsatz statt und macht ihn langsamer.
  — <https://github.com/kijai/ComfyUI-SolAttn_triton/blob/main/readme.md>
- Vergleichen Sie Geschwindigkeit und Bild bei gleichem Modell, Seed, Auflösung, Schrittzahl und GPU: Selbst die Upstream-Messungen halten all diese Bedingungen fest.
  — <https://github.com/NVlabs/Sana/tree/sol-engine>
- Halten Sie bei MiniMax H3 die finalen Denoise-Schritte dicht, wenn die spärliche Attention einen spürbaren Fehler hinterlässt; exact_kv liefert exakte Attention für den Conditioning-Präfix bei etwa 3 % zusätzlichen Kosten.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>

## Abgelöst durch dieses {#superseded-by-this}

- 2026-08-04 — Für KingGore ist der ursprüngliche reine Sparse-Modus veraltet: v2 ergänzte dense_steps/step_off und exact_kv/exact_kv_and_rows, um die Qualität bei MiniMax H3 zu erhalten.
- 2026-08-04 — Für Kijai ist es nicht mehr nötig, den ModuleNotFoundError für TensorDescriptor auf Triton-Builds vor SM90 hinzunehmen: die Korrektur wurde übernommen, die Bestätigung beschränkt sich jedoch auf RTX 3060 und ist keine Garantie für RTX 20/10.

## Weiterhin ungeklärt {#still-unknown}

- ComfyUI Sol-Attn ist kein einheitliches Projekt: Kijai und KingGore sind getrennte Repositories mit unterschiedlichen Backends, GPU-Unterstützung und Parametern. Ihre Kompatibilität untereinander ist nicht dokumentiert.
- Im Text des Ereignisses vom 2026-08-07 gibt es keine verfügbaren Inhalte; daher ist event_findings bewusst leer: Keine zusätzliche datierte Aussage lässt sich ehrlich genau diesem Tag zuordnen.
- Kijai bezeichnet das Projekt als work in progress und dokumentiert Tests nur auf RTX 4090 und RTX 5090; ein Merge für RTX 3060 belegt keine Unterstützung aller GPUs vor SM90.
- Keine der verwendeten Upstream-Quellen von NVIDIA kündigt einen offiziellen ComfyUI-Node an; Sol-Engine und Community-Nodes sind als getrennte Integrationswege zu betrachten.
- Die chinesischsprachige Suche ergab keine Primärquelle in chinesischer Sprache, die sich konkret auf diese beiden Repositories bezieht.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/kijai/ComfyUI-SolAttn_triton | kijai/ComfyUI-SolAttn_triton | 2026-09-05 |
| https://github.com/kijai/ComfyUI-SolAttn_triton/blob/main/readme.md | ComfyUI-SolAttn README | 2026-09-05 |
| https://github.com/kijai/ComfyUI-SolAttn_triton/pull/1 | Kijai pull request #1: pre-SM90 TensorDescriptor import fix | 2026-09-05 |
| https://github.com/KingGore/ComfyUI_sol-attn_Blackwell | KingGore/ComfyUI_sol-attn_Blackwell | 2026-09-05 |
| https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md | KingGore Blackwell README | 2026-09-05 |
| https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/commits/main | KingGore Blackwell commit history | 2026-09-05 |
| https://arxiv.org/abs/2607.24027 | Sol-Attn: Accelerating Video Generation Inference via On-the-Fly Attention Sparsification | 2026-09-05 |
| https://nvlabs.github.io/Sana/Sol-Attn/ | NVIDIA Sol-Attn project page | 2026-09-05 |
| https://github.com/NVlabs/Sana/tree/sol-engine | NVlabs/Sana sol-engine branch | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:comfyui-sol-attn`, Thread `blackwell-and-triton-implementations`, 1 datiertes Ereignis 2026-08-07 → 2026-08-07.
- **Praktischer Hinweis:** Stand 2026-08-07 sollten Praktiker, die ComfyUI Sol-Attn evaluieren, die auf Blackwell ausgerichtete Implementierung von der auf Triton ausgerichteten unterscheiden und die Kompatibilität der Umgebung prüfen, bevor sie eine der beiden übernehmen.
- **Konfidenz:** medium. Datierte Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.

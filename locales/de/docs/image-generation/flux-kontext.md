---
title: "FLUX Kontext"
category: models
tags: [image-editing, flux, bfl, dit, flow-matching, sequence-concatenation, character-consistency, multi-turn, non-commercial-dev]
aliases: ["FLUX.1-Kontext-dev", "Kontext"]
level: 2
source_sha256: fea0e789c9b4e32c721e4938e5d018bbc1e0f1c35924e00292b51b852b10fee4
translation: machine
translated_at: '2026-10-24'
---
# FLUX Kontext {#flux-kontext}

Bildbearbeitungsmodell von Black Forest Labs (BFL). Erweitert die FLUX.1-Architektur um **Sequence Concatenation** zur Konditionierung mit Kontextbildern. Best-in-Class für Textbearbeitung, Charakterkonsistenz und Multi-Turn-Bearbeitung.

Paper: arXiv:2506.15742 (Juni 2025).

## Architektur {#architecture}

Gleicher 12B-DiT wie FLUX.1-dev:
- 19 Double-Stream-Blöcke (getrennte Bild-/Text-Gewichte, gemeinsame Aufmerksamkeit)
- 38 Single-Stream-Blöcke (fusioniertes FFN)
- Hidden: 3072, Heads: 24, 16-Kanal-Latent-VAE
- Text: CLIP (768d) + T5 (4096d)

### Zentrale Neuerung: Sequence Concatenation {#key-innovation-sequence-concatenation}

Kontextbilder werden durch das FLUX-VAE kodiert → Latent-Tokens **an die Zielbild-Tokens angehängt** im visuellen Stream:
```text
Target tokens:  position (0, h, w)
Context image:  position (1, h, w)   ← "virtual timestep" via 3D RoPE
Context image 2: position (2, h, w)  ← architecturally supported, not yet released
```

**Channel Concatenation wurde getestet und schnitt schlechter ab.** Sequence Concat erhält die unabhängige Auflösung bzw. das Seitenverhältnis für Ein- und Ausgabe.

Ist der Kontext leer → Rückfall auf reines Text-zu-Bild.

### vs. [[Step1X-Edit]] {#vs-step1x-edit}

| Aspekt | FLUX Kontext | Step1X-Edit / Qwen-Edit |
|--------|-------------|------------------------|
| Basis | FLUX.1 12B DiT | Eigener MMDiT |
| Text-Encoder | CLIP + T5 | Qwen 2.5 VL (Vision-Language) |
| Konditionierung | Sequence Concat (Latent-Tokens) | Gemeinsame Aufmerksamkeit (Bild + Text) |
| Maskenunterstützung | Keine explizite Maske (textgesteuert) | DiffSynth-Pipeline unterstützt Masken |
| Geschwindigkeit | 3-5s bei 1024×1024 | Langsamer (~40 GB VRAM) |

## Varianten {#variants}

| Variante | Zugang | Lizenz |
|---------|--------|---------|
| Kontext [dev] | Open Weights (HF) | **Nicht-kommerziell** (BFL-dev-Lizenz) |
| Kontext [pro] | Nur API | Kommerziell über BFL |
| Kontext [max] | Nur API | Kommerziell über BFL |

**Dev ist nur I2I** (kein T2I). T2I nur in pro/max.

## Training {#training}

- Startet vom FLUX.1-T2I-Checkpoint
- Gemeinsames Fine-Tuning auf I2I + T2I mit Rectified-Flow-Loss
- Daten: Millionen relationaler Paare (nicht offengelegt)
- FSDP2, Flash Attention 3, selektives Activation Checkpointing

## VRAM {#vram}

Mindestens ~24 GB (Transformer in bf16). Gesamte Pipeline ~32-40 GB. FP8-/FP4-Quantisierung für 24-GB-GPUs verfügbar.

## Stolperfallen {#gotchas}

- **Verändert das gesamte Bild**, nicht nur den bearbeiteten Bereich. Für selektives Zusammenführen den flux-kontext-diff-merge-Node nutzen, mit LAB-Farbraumerkennung + Poisson-Blending
- Multi-Turn-Bearbeitung verschlechtert sich nach ~6 Iterationen
- Das Dev-Modell weist Distillations-Artefakte auf
- Nicht-kommerzielle Lizenz für Open Weights — kommerzielle Nutzung erfordert eine Lizenzierung bei BFL
- Die Entwicklung von [ACE++](ACE++.md) auf FLUX-Basis wurde aufgrund von Trainingsinstabilität **eingestellt**

## Wichtige Links {#key-links}

- GitHub: github.com/black-forest-labs/flux
- HF: huggingface.co/black-forest-labs/FLUX.1-Kontext-dev
- Diff-Merge: github.com/safzanpirani/flux-kontext-diff-merge

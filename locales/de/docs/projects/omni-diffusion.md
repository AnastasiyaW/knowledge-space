---
title: "Omni-Diffusion"
category: projects
date: 2026-03-11
tags: [multimodal_models, omni-diffusion, omni-diffusion-development, project]
aliases: ["Omni-Diffusion"]
level: 2
source_sha256: 8ed6b65de65a8ac4873a405610c63cf974cfd09dbacd677b0fef96bb525e1549
translation: machine
translated_at: '2026-10-24'
---
# Omni-Diffusion {#omni-diffusion}

**Entwicklungslinie:** `project:omni-diffusion` · Thread `omni-diffusion-development`  
**Letztes Ereignis:** 2026-03-11 · 1 datiertes Ereignis seit 2026-03-11 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Omni-Diffusion ist ein Any-to-Any-Multimodalmodell, das maskierte diskrete Diffusion verwendet. Es bietet Forschenden und Ingenieuren einen offenen Stack anstelle separater autoregressiver Modelle.

- Text-zu-Bild-, Sprache-zu-Bild-, VQA-, gesprochene VQA-, ASR- und TTS-Aufgaben.
- Gemeinsame Generierung und Verständnis über Text, Bilder und Sprache hinweg.

Der veröffentlichte Checkpoint hat 8B Parameter in BF16. Audioaufgaben benötigen einen separaten GLM-4-Voice-Tokenizer und -Decoder; für Bilder wird MagViT-v2 benötigt. Dabei handelt es sich um einen reproduzierbaren Forschungsstack und nicht um eine gehostete API, da auf der Modellkarte kein verbundener Inference-Provider angegeben ist.

## Entwicklungslinie {#development-line}

- **2026-03-11 — Öffentliche Projektressourcen von Omni-Diffusion verlinkt.** Am 2026-03-11 verlinkte ein datierter Eintrag die Projektwebsite, das Quellcode-Repository und die Hugging-Face-Modellseite von Omni-Diffusion. Zusammen bilden diese Ressourcen einen öffentlichen Bezugspunkt für die Dokumentation, die Implementierung und den Modellzugang des Projekts. Allein die datierten Links belegen weder die Release-Version, die Fähigkeiten noch die Evaluationsergebnisse.

## Was sich geändert hat {#what-changed}

- 2026-03-11 — Code, Projektseite und der offene 8B-BF16-Checkpoint von Omni-Diffusion für Any-to-Any-Aufgaben mit Text, Bild und Sprache veröffentlicht.
- 2026-07-03 — arXiv v2 aktualisierte die ICML-Version des Papers und lieferte einen optimierten Modell-Checkpoint.

## Anwendung {#how-to-use-this}

Stand 2026-03-11 sollte Omni-Diffusion über die verlinkte Projektseite, das Quellcode-Repository und die Hugging-Face-Modellseite evaluiert werden, nicht anhand ungeprüfter Sekundärbeschreibungen.

1. Repository klonen, Submodule initialisieren und Abhängigkeiten sowie das Paket in einer Umgebung auf Basis des offiziellen Docker-Images installieren.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
2. Den Hauptcheckpoint nach ../models/Omni-Diffusion herunterladen; für Audioaufgaben den GLM-4-Voice-Tokenizer und -Decoder hinzufügen, für Bilder MagViT-v2.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
3. tools/inference.py mit den Pfaden zum Hauptgewicht, Bild-Tokenizer, Audio-Tokenizer, Audio-Decoder und Ausgabeverzeichnis ausführen.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>

## Best Practices {#best-practices}

- Für multimodale Aufgaben den offiziellen Inferenzpfad des Repositories verwenden: Das Laden über Transformers ersetzt nicht die erforderlichen Bild- und Audio-Tokenizer.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
- Die Modellrevision festlegen und prüfen, bevor `trust_remote_code` aktiviert wird, da die Modellkarte ausdrücklich eine benutzerdefinierte Architektur voraussetzt.
  — <https://huggingface.co/lijiang/Omni-Diffusion>
- Hauptgewicht und die drei Hilfsartefakte in passenden Pfaden und in derselben Umgebung halten, sonst lässt sich der beworbene vollständige Text-, Bild- und Sprach-Stack nicht aufbauen.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-07-03 — arXiv v2 ersetzt v1 vom 2026-03-06 als aktuelle Version des Papers; v2 ist als ICML-Version mit optimiertem Checkpoint gekennzeichnet.

## Weiterhin unbekannt {#still-unknown}

- Primäre veröffentlichte Angaben zu VRAM-Bedarf, Latenz oder unterstützter CUDA-Version für die Inferenz wurden nicht gefunden.
- Es wurde keine offizielle chinesischsprachige Quelle oder unabhängiger chinesischsprachiger Erfahrungsbericht bestätigt; die chinesischsprachige Suche ergab nur Sekundärzusammenfassungen.
- Das Fehlen eines Inference-Providers auf der Hugging-Face-Modellkarte bestätigt, dass kein gelisteter gehosteter Provider existiert, schließt aber selbst gehostete Deployments durch Dritte nicht aus.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://omni-diffusion.github.io/ | Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion | 2026-09-05 |
| https://github.com/VITA-MLLM/Omni-Diffusion | VITA-MLLM/Omni-Diffusion Repository | 2026-09-05 |
| https://huggingface.co/lijiang/Omni-Diffusion | Modellkarte lijiang/Omni-Diffusion | 2026-09-05 |
| https://arxiv.org/abs/2603.06577 | Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:omni-diffusion`, Thread `omni-diffusion-development`, 1 datiertes Ereignis, 2026-03-11 → 2026-03-11.
- **Praktischer Hinweis:** Stand 2026-03-11 sollten Praktiker Omni-Diffusion über die verlinkte Projektseite, das Quellcode-Repository und die Hugging-Face-Modellseite evaluieren, nicht anhand ungeprüfter Sekundärbeschreibungen.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.

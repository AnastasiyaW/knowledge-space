---
title: "SAMA"
category: projects
date: 2026-03-20
tags: [project, sama]
aliases: ["SAMA"]
level: 2
source_sha256: b205bd9d1d99e77b86e0868f79a336e5f5acc55e29da2c390f3035d61c637e10
translation: machine
translated_at: '2026-10-24'
---
# SAMA {#sama}

**Entwicklungslinie:** `project:sama` · Thread `sama`  
**Letztes Ereignis:** 2026-03-20 · 1 datiertes seit 2026-03-20 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Ein Open-Source-Modell zur anweisungsgesteuerten Videobearbeitung für Wan-Nutzer, die Objekte, Stil oder Text in einem Video ändern und dabei die Bewegung beibehalten.

- Semantische Verankerung plant Bearbeitungen über Keyframes hinweg.
- Bewegungsausrichtung bewahrt die zeitliche Dynamik.
- Der SAMA-14B-Checkpoint und ein offizieller ComfyUI-Workflow sind verfügbar.

Voraussetzungen: Linux, eine NVIDIA-GPU, Python 3.10, eine mit CUDA 12.1 kompatible Umgebung und Wan2.1-T2V-14B. Dies ist ein lokaler Inferenz-Stack auf Basis von Wan, kein gehosteter Dienst.

## Entwicklungslinie {#development-line}

- **2026-03-20 — Öffentliche Projekt-, Quellcode- und Modellressourcen zu SAMA wurden verlinkt.** Am 2026-03-20 verlinkte eine datierte SAMA-Meldung die öffentliche Projektwebsite, das Quellcode-Repository und die Hugging-Face-Seite für SAMA-14B. Diese Links belegen, dass die drei öffentlichen Ressourcen an diesem Datum mit SAMA verknüpft waren, ohne weitergehende Aussagen über das Modell oder das Projekt zu begründen.

## Was sich geändert hat {#what-changed}

- **2026-03-20** — SAMA-Paper veröffentlicht; Preprint am 2026-03-19 eingereicht, mit 24 Seiten und 12 Abbildungen.
- **2026-03-21** — SAMA-14B-Checkpoint veröffentlicht; SAMA-5B weiterhin als „Coming soon“ markiert.
- **2026-03-24** — Offizieller SAMA-ComfyUI-Workflow verfügbar gemacht.
- **2026-06-20** — SAMA für ECCV 2026 angenommen.
- **2026-06-26** — Metadatensatz SAMA-edit-filtered-1M veröffentlicht.

## So wird es verwendet {#how-to-use-this}

Stand 2026-03-20 nutzen wir die verlinkte SAMA-Website, das Quellcode-Repository und die Modellseite SAMA-14B als Ausgangspunkte für die Evaluierung. Fähigkeiten, Lizenzierung und Nutzungsanforderungen sind vor einem Einsatz anhand dieser Ressourcen zu prüfen.

1. Repository klonen, eine Python-3.10-Umgebung anlegen und die Abhängigkeiten installieren.
  — <https://github.com/Cynthiazxy123/SAMA>
2. SAMA-14B herunterladen und das vollständige lokale Verzeichnis Wan2.1-T2V-14B vorbereiten.
  — <https://huggingface.co/syxbb/SAMA-14B>
3. MODEL_ROOT, STATE_DICT, SRC_VIDEO, PROMPT und OUTPUT_DIR in infer_sh/run_sama.sh setzen und das Skript anschließend ausführen.
  — <https://github.com/Cynthiazxy123/SAMA>
4. Für einen knotenbasierten Workflow die offizielle ComfyUI-Integration mit dem Wan-Basismodell und SAMA-14B verwenden.
  — <https://github.com/Cynthiazxy123/SAMA>

## Best Practices {#best-practices}

- Prüfen, ob das Basisverzeichnis Wan2.1-T2V-14B vollständig ist: Das Skript bricht absichtlich ab, wenn Dateien fehlen.
  — <https://github.com/Cynthiazxy123/SAMA>
- Die FPS der Quelle verwenden; --fps explizit setzen, wenn sie fehlt.
  — <https://github.com/Cynthiazxy123/SAMA>
- Die automatische Auffüllung der Eingabeframes auf die Wan-Anforderung 4k+1 einkalkulieren.
  — <https://github.com/Cynthiazxy123/SAMA>

## Abgelöst durch {#superseded-by-this}

- 2026-03-20 — Zustand nur mit Paper: SAMA-14B ist seit 2026-03-21 verfügbar, der offizielle ComfyUI-Workflow seit 2026-03-24.

## Weiterhin unbekannt {#still-unknown}

- Offizielle Materialien nennen weder gemessenen VRAM-Bedarf, Inferenzgeschwindigkeit noch unterstützte Auflösungen. Die Hardwareplanung erfordert separate Tests der Konfiguration und des Workflows.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://cynthiazxy123.github.io/SAMA/ | SAMA: Factorized Semantic Anchoring and Motion Alignment for Instruction-Guided Video Editing | 2026-09-05 |
| https://github.com/Cynthiazxy123/SAMA | Cynthiazxy123/SAMA — offizieller Inferenz-Code | 2026-09-05 |
| https://huggingface.co/syxbb/SAMA-14B | syxbb/SAMA-14B | 2026-09-05 |
| https://arxiv.org/abs/2603.19228 | SAMA: Factorized Semantic Anchoring and Motion Alignment for Instruction-Guided Video Editing | 2026-09-05 |

## Agenten-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:sama`, Thread `sama`, 1 datiertes Ereignis 2026-03-20 → 2026-03-20.
- **Praxishinweis:** Stand 2026-03-20 können Praktiker die verlinkte SAMA-Website, das Quellcode-Repository und die Modellseite SAMA-14B als primäre Ausgangspunkte für die Evaluierung nutzen. Fähigkeiten, Lizenzierung und Nutzungsanforderungen sind vor einem Einsatz anhand dieser Ressourcen zu prüfen.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.

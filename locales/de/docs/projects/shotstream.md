---
title: "ShotStream"
category: projects
date: 2026-03-31
tags: [project, shotstream]
aliases: ["ShotStream"]
level: 2
source_sha256: 863fb2e57be4307e03617dd1702ed6451417364908e1122c454bbb50c2474979
translation: machine
translated_at: '2026-10-24'
---
# ShotStream {#shotstream}

**Entwicklungslinie:** `project:shotstream` · Thread `shotstream`  
**Letztes Ereignis:** 2026-03-31 · 1 datiertes seit 2026-03-31 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

ShotStream ist eine CUDA-Forschungsimplementierung für Kreative und Entwickler von Video-Modellen, die eine mehrteilige Text-zu-Video-Erzählung während der Ausführung steuern müssen.

- Generierung des nächsten Shots aus historischen Shots und Streaming-Prompts.
- Ausführung auf Wan2.1-T2V-1.3B mit lokalen Checkpoints.
- Getrennte globale und lokale Caches für Kontinuität über Shots hinweg und innerhalb eines Shots.

Die Autoren berichten von 15,95 FPS bei 832×480 auf einer NVIDIA H200. Demos zeigen 5–6 Shots und knapp 500 Frames. Dies ist ein lokaler Forschungsreproduktionspfad, kein gehosteter Video-Dienst. Öffentliche Demos garantieren keine Parität mit dem internen Trainingsaufbau.

## Entwicklungslinie {#development-line}

- **2026-03-31 — Öffentliche Projektseite, Code und Modellseite von ShotStream wurden verlinkt.** Am 2026-03-31 verwies ein datierter Beitrag auf die öffentliche Projektseite, das GitHub-Repository und die Hugging-Face-Seite. Die Belege liefern einen öffentlichen Bezugspunkt für die Entwicklungslinie. Sie belegen weder eine Release-Version, Fähigkeiten, Urheberschaft noch den genauen Wortlaut der ursprünglichen Nachricht.

## Was sich geändert hat {#what-changed}

- 2026-03-25 — Die Hugging-Face-Historie von ShotStream verzeichnet eine Konfiguration und drei Checkpoint-Uploads.
- 2026-03-26 — ShotStreams arXiv-v1 wurde eingereicht.
- 2026-03-27 — ShotStream veröffentlichte seine Projektseite, die arXiv-Version, Training-/Inferenz-Code und Checkpoints.
- 2026-03-31 — Die Model Card von ShotStream erhielt ein Text-to-Video-Tag sowie erweiterte Dokumentation, Nutzungshinweise und Zitationsmaterial.
- 2026-06-18 — Das Repository von ShotStream meldete die Annahme bei der ECCV 2026.

## So verwenden Sie es {#how-to-use-this}

1. Klonen Sie das Repository und richten Sie die dokumentierte Umgebung mit Python 3.10, CUDA, PyTorch, Requirements und FlashAttention ein.
  — <https://github.com/KlingAIResearch/ShotStream>
2. Laden Sie sowohl das Wan2.1-T2V-1.3B-Basismodell als auch die ShotStream-Checkpoints mit Git LFS in die dokumentierten Verzeichnisse herunter.
  — <https://github.com/KlingAIResearch/ShotStream>
3. Bereiten Sie eine Prompt-JSON mit einem global_caption sowie den Beschreibungen shot1 bis shotN für die Sequenz vor.
  — <https://github.com/KlingAIResearch/ShotStream/blob/main/demo/testdata/json/01.json>
4. Führen Sie den dokumentierten autoregressiven Vier-Schritt-Launcher für die mehrteilige Inferenz aus.
  — <https://github.com/KlingAIResearch/ShotStream>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- 2026-03-27 — Die veröffentlichten Trainings- und Inferenz-Codes sowie die Checkpoints lösen den Zustand des Papers vor der Veröffentlichung ab.
- 2026-03-31 — Dokumentation der Model Card und Pipeline-Metadaten aktualisiert; dieses Datum brachte keine neuen Gewichte oder keinen neuen Code.
- 2026-06-18 — Die Annahme zur ECCV 2026 löst den Status des Veranstaltungsorts vor der Annahme ab, ohne ein neues Laufzeitartefakt anzukündigen.

## Noch unbekannt {#still-unknown}

- Die Links allein belegen nicht, ob sich das Ereignis vom 2026-03-31 konkret auf die Model-Card-Aktualisierung am selben Tag bezog.
- Primärquellen nennen keinen unterstützten gehosteten Endpunkt, keine Mindestanforderung für Consumer-GPUs, keinen VRAM-Bedarf und keinen unabhängigen Reproduktions-Benchmark. Der angegebene Durchsatz ist eine Messung der Autoren auf einer H200.
- Primärquellen enthalten keine herstellereigene Anleitung auf Vereinfachtem Chinesisch und keine unabhängige Diskussion aus der Praxis. Sekundärzusammenfassungen wurden nicht als Beleg verwendet.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://luo0207.github.io/ShotStream/ | ShotStream project page | 2026-09-07 |
| https://github.com/KlingAIResearch/ShotStream | KlingAIResearch/ShotStream repository and README | 2026-09-07 |
| https://huggingface.co/KlingTeam/ShotStream | KlingTeam/ShotStream model card | 2026-09-07 |
| https://arxiv.org/abs/2603.25746 | ShotStream: Streaming Multi-Shot Video Generation for Interactive Storytelling | 2026-09-07 |
| https://arxiv.org/html/2603.25746 | ShotStream paper HTML | 2026-09-07 |
| https://huggingface.co/KlingTeam/ShotStream/commits/main | KlingTeam/ShotStream commit history | 2026-09-07 |
| https://huggingface.co/KlingTeam/ShotStream/discussions/1 | Improve model card and add pipeline tag | 2026-09-07 |
| https://github.com/KlingAIResearch/ShotStream/blob/main/demo/testdata/json/01.json | ShotStream demo prompt JSON | 2026-09-07 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:shotstream`, Thread `shotstream`, 1 datiertes Ereignis 2026-03-31 → 2026-03-31.
- **Praxishinweis:** Siehe die belegten Nutzungs- und Praxisabschnitte oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Abgelöst-durch-Einträge sind maßgeblich dafür, was veraltet ist.

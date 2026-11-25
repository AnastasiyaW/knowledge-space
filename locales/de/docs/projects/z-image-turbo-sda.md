---
title: "z-image-turbo-sda — Hugging-Face-Modellveröffentlichung"
category: projects
date: 2026-03-26
tags: [hugging-face-model-release, project, z-image-turbo-sda, z_image_turbo_sda]
aliases: ["z-image-turbo-sda"]
level: 2
source_sha256: 7c3f5d73dbe3714f5f4d9ed191408311d588f1bbfd8a153fe1a950467cb62efa
translation: machine
translated_at: '2026-10-24'
---
# z-image-turbo-sda — Hugging-Face-Modellveröffentlichung {#z-image-turbo-sda-hugging-face-model-release}

**Entwicklungslinie:** `project:z-image-turbo-sda` · Thread `hugging-face-model-release`  
**Letztes Ereignis:** 2026-03-26 · 1 datiertes Ereignis seit 2026-03-26 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

Z-Image-Turbo-SDA ist ein Drittanbieter-Adapter vom Typ LoKr/LyCORIS für Nutzer, die Tongyi-MAI/Z-Image-Turbo einsetzen. Es handelt sich nicht um einen eigenständigen Z-Image-Checkpoint.

- Wird in die Turbo-Pipeline geladen, um Pose, Kamerawinkel und Layout zwischen Seeds zu variieren.
- Behält den 8-Schritte-Workflow bei, wobei ein berichteter Zielkonflikt zwischen Diversität und Anatomie besteht.

## Entwicklungslinie {#development-line}

- **2026-03-26 — z-image-turbo-sda wurde mit einem Hugging-Face-Modell-Repository verknüpft.** Z-Image-Turbo-SDA wurde als bereits veröffentlichter Adapter referenziert. An diesem Datum ist kein Repository-Commit verzeichnet.

## Was sich geändert hat {#what-changed}

- 2026-03-11: Das Repository hat `zit_sda_v1.safetensors` hochgeladen und einen LoKr-Adapter für Tongyi-MAI/Z-Image-Turbo dokumentiert.
- 2026-03-26: Z-Image-Turbo-SDA wurde als bereits veröffentlichter Adapter referenziert; an diesem Datum ist kein Repository-Commit verzeichnet.
- 2026-04-09: Zwei Commits mit der Bezeichnung `Update README.md` änderten die Dokumentation, nicht das öffentliche Gewichtsartefakt.
- 2026-05-12: Der Maintainer hat Kompatibilitätsprobleme mit einigen abgeleiteten ZIT-Modellen bestätigt und auf eine separate, nur aus Code bestehende Alternative verwiesen.

## So wird es verwendet {#how-to-use-this}

Ab 2026-03-26 behandeln wir das Hugging-Face-Repository F16/z-image-turbo-sda als Referenz für die Verteilung von z-image-turbo-sda. Prüfen Sie vor der Verwendung Model Card, Dateien, Lizenz und Kompatibilität.

1. Beginnen Sie mit der exakten Basis `Tongyi-MAI/Z-Image-Turbo`. SDA ist ein Adapter und kein Checkpoint, der allein geladen werden kann.
  — <https://huggingface.co/F16/z-image-turbo-sda>
2. Laden Sie in einem CUDA-Diffusers-Setup die Basis in float16 und anschließend `F16/z-image-turbo-sda` mit `pipeline.load_lora_weights(..., adapter_name="sda_diversity")`. Die Card setzt aktuelle `diffusers` samt `peft` voraus.
  — <https://huggingface.co/F16/z-image-turbo-sda>
3. Reproduzieren Sie zunächst den mitgelieferten Referenzlauf: 8 Inferenzschritte, CFG 1.0 und ein festes Raster von Seeds. Bewerten Sie die Variation über das Raster hinweg und nicht anhand einer einzelnen Ausgabe.
  — <https://huggingface.co/F16/z-image-turbo-sda>

## Best Practices {#best-practices}

- Validieren Sie SDA allein, bevor Sie weitere Z-Image-Turbo-LoRAs stapeln. Falls ein Stapeln nötig ist, empfiehlt der Maintainer, das SDA-Gewicht auf 0,5–0,7 zu reduzieren und eine geringere Diversität in Kauf zu nehmen.
  — <https://huggingface.co/F16/z-image-turbo-sda>
- Verwenden Sie einen festen Multi-Seed-A/B-Test mit einfachen und räumlich eingeschränkten Prompts und prüfen Sie anschließend komplexe Posen auf Anatomiefehler. Die Card weist darauf hin, dass eingeschränkte Prompts weniger Spielraum für Kompositionsänderungen lassen.
  — <https://huggingface.co/F16/z-image-turbo-sda>
- Halten Sie das 8-Schritte-Preset mit CFG 1.0 der Adapter-Card getrennt vom offiziellen Basisrezept. Das offizielle Rezept gibt ZImagePipeline, bf16, 9 Scheduler-Schritte für 8 DiT-Forwards und CFG 0.0 vor.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>
- Behandeln Sie die berichtete LPIPS-Verbesserung und die Prozentwerte zur Wiederherstellung der Diversität als Ergebnisse des Maintainers, nicht als unabhängig reproduzierte Benchmarks.
  — <https://huggingface.co/F16/z-image-turbo-sda>

## Hierdurch ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Es wurde kein öffentlicher Trainingscode, keine Herkunftsangabe der Datensätze, kein unveränderlicher Digest des Trainings-Checkpoints, keine minimale Version von `diffusers`/`peft` und kein unterstützter ComfyUI-Workflow gefunden.
- Die LPIPS-Werte der Model Card sowie die behaupteten 70,2 %/58 % Wiederherstellung der Diversität sind vom Maintainer berichtet und wurden nicht unabhängig validiert.
- Öffentliche Repository-Aktivität belegt keine neue SDA-Veröffentlichung genau am 2026-03-26. Das Datum kennzeichnet ein bereits vorhandenes Artefakt, nicht ein nachgewiesenes Gewichts-Update.
- Es wurden keine Belege gefunden, dass Tongyi-MAI diesen Adapter erstellt, unterstützt oder gepflegt hat.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/F16/z-image-turbo-sda | Model Card F16/z-image-turbo-sda | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/commits/main | Commit History · F16/z-image-turbo-sda | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/blob/2557329bb6c6b23fdf846f3f21ab42d4f8df523e/README.md | README.md · F16/z-image-turbo-sda bei Revision 2557329 | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/blob/main/zit_sda_v1.safetensors | zit_sda_v1.safetensors · F16/z-image-turbo-sda | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/discussions/5 | Why does applying this LoRA to certain ZIT models cause the image to break? | 2026-09-06 |
| https://huggingface.co/Tongyi-MAI/Z-Image-Turbo | Model Card Tongyi-MAI/Z-Image-Turbo | 2026-09-06 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:z-image-turbo-sda`, Thread `hugging-face-model-release`, 1 datiertes Ereignis vom 2026-03-26 bis 2026-03-26.
- **Praktischer Hinweis:** Ab 2026-03-26 behandeln wir das Hugging-Face-Repository F16/z-image-turbo-sda als Referenz für die Verteilung von z-image-turbo-sda. Prüfen Sie vor der Verwendung Model Card, Dateien, Lizenz und Kompatibilität.
- **Konfidenz:** mittel. Datierte Ersetzungshinweise sind maßgeblich dafür, was veraltet ist.

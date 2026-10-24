---
title: "Marlin-2B"
category: projects
date: 2026-05-21
tags: [marlin-2b, project]
aliases: ["Marlin-2B"]
level: 3
source_sha256: ff1b59db696832ae4132c7f5382909830a48f7d665a5087697bb72879d6c5ea8
translation: machine
translated_at: '2026-10-24'
---
# Marlin-2B {#marlin-2b}

**Entwicklungslinie:** `project:marlin-2b` · Thread `marlin-2b`  
**Letztes Ereignis:** 2026-05-21 · 1 datiertes seit 2026-05-21 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Marlin-2B ist ein 2B-Video-VLM für Entwickler, die zeitgestempelte visuelle Indizierung benötigen.

- Caption: eine Szenenbeschreibung sowie zeitlich begrenzte Events.
- Find: eine natürlichsprachliche Event-Abfrage liefert einen Start-/Endbereich.

Am 2026-09-05 ist das Basismodell gated, lädt benutzerdefinierten Code und hat kein Hugging-Face-Inference-Provider-Deployment. Beginnen Sie mit begrenzten Captioning- oder Event-Lokalisierungsaufgaben und testen Sie anschließend die Zeitstempelgenauigkeit mit eigenem Videomaterial.

## Entwicklungslinie {#development-line}

- **2026-05-21 — Marlin-2B-Modellseite und begleitende VLM-Website wurden veröffentlicht.** Am 2026-05-21 teilte die Marlin-2B-Entwicklungslinie eine Hugging-Face-Modellseite und eine begleitende VLM-Website. Wir erfassen diesen Schritt, weil er das Projekt mit öffentlichen Modell- und Nutzungsressourcen verbindet. Die datierten Links allein belegen jedoch weder die genaue Release-Version, die Fähigkeiten, die Lizenz noch, ob eine der Ressourcen erstmals an diesem Datum erschien.

## Was sich geändert hat {#what-changed}

- 2026-05-20 — Das Projekt erklärte, seine BSL-1.1-Lizenz durch Apache-2.0 ersetzt zu haben.
- 2026-05-21 — Eine Anfrage an den Provider-Support bestätigte die öffentliche Modellkennung, nicht einen gehosteten Endpunkt.
- 2026-05-26 — Ein technischer Beitrag beschrieb das Modell und seinen Evaluierungsansatz, während Audit-Artefakte unveröffentlicht blieben.
- 2026-05-29 — Eine Antwort des Organisationskontos besagte, dass MLX/MPS noch nicht offiziell unterstützt werde, und nannte entferntes NVIDIA plus Hugging Face Transformers als Referenz-Setup.
- 2026-06-24 — Die Auflistung der Organisation zeigte eine separate 8-Bit-MLX-Distributionslinie.

## Verwendung {#how-to-use-this}

Wir können die Evaluierung ab 2026-05-21 über die verlinkte Hugging-Face-Modellseite und die begleitende VLM-Website beginnen. Vor einer Verwendung sollten Model Card, unterstützte Aufgaben, Lizenz und genaue Version überprüft werden.

1. Zugang zum gated Basis-Repository anfordern und sich authentifizieren; anonyme Besucher können Dateien auflisten, aber nicht deren gated Inhalte herunterladen.
  — <https://huggingface.co/NemoStation/Marlin-2B/tree/main>
2. Den dokumentierten Stack installieren: Transformers 5.7 oder neuer, PyTorch 2.11 oder neuer, TorchCodec, qwen-vl-utils, av und Pillow.
  — <https://huggingface.co/NemoStation/Marlin-2B>
3. AutoProcessor und AutoModelForCausalLM mit aktiviertem trust_remote_code, BF16 und einem CUDA-Device-Mapping laden.
  — <https://huggingface.co/NemoStation/Marlin-2B>
4. caption(video) für eine geparste Szenen- und Event-Zeitleiste oder find(video, event=...) für einen geparsten Zeitbereich aufrufen.
  — <https://huggingface.co/NemoStation/Marlin-2B>
5. Auf Apple Silicon die separate MLX-8bit-Route verwenden; für zeitliche Verankerung einen zeitstempelbewussten Serving-Pfad statt eines Einzelschritt-Caption-Pfads nutzen.
  — <https://huggingface.co/NemoStation/Marlin-2B-MLX-8bit>

## Best Practices {#best-practices}

- Den Helper-Prompt nicht setzen, solange kein gemessener Grund für eine Überschreibung besteht. Die Model Card besagt, dass der kanonische Trainingsprompt fast immer beibehalten werden sollte.
  — <https://huggingface.co/NemoStation/Marlin-2B>
- Zuerst die trainierten Preprocessing-Standardwerte beibehalten: TorchCodec, 2 FPS, 4–240 Frames und etwa 200K Pixel pro Frame. Die Standardobergrenze deckt ungefähr zwei Minuten ab.
  — <https://huggingface.co/NemoStation/Marlin-2B>
- span=null oder format_ok=false aus find() als nicht parsebares Ergebnis behandeln, nicht als Beleg dafür, dass das Event fehlt.
  — <https://huggingface.co/NemoStation/Marlin-2B>
- Entfernten benutzerdefinierten Code prüfen und einen geprüften Commit-Hash festlegen (pinnen), bevor trust_remote_code in einem Produktivworkflow aktiviert wird.
  — <https://huggingface.co/docs/transformers/v4.43.3/custom_models>
- Gemeldete Ergebnisse des Dense-Caption-Benchmarks als Herstellerevaluierung behandeln. Die Autoren erklärten im Beitrag vom 26. Mai, dass ihr Audit-Code, ihre Prompts, Annotationen und der GRACE-Benchmark noch ausstehende Materialien seien.
  — <https://nemostation.com/blog/marlin-2b-the-map-was-wrong>
- Für zeitliche Verankerung in MLX die Zeit pro Frame mit einem zeitstempelbewussten Serving-Pfad erhalten. Die MLX-Model-Card beschränkt die Einzelschritt-Route auf dichtes Captioning.
  — <https://huggingface.co/NemoStation/Marlin-2B-MLX-8bit>

## Hiermit ersetzt {#superseded-by-this}

- 2026-05-20 — Der bisherige BSL-1.1-Lizenzstatus wurde laut Angaben durch Apache-2.0 ersetzt.
- 2026-06-24 — Die Aussage vom 2026-05-29, dass MLX/MPS keine offizielle Unterstützung habe, ist für die separat gelistete MLX-8bit-Distribution veraltet; sie ersetzt nicht die ursprüngliche CUDA/Transformers-Route.

## Weiterhin unbekannt {#still-unknown}

- Für 2026-05-21 wurde kein unveränderlicher Snapshot der Model Card, kein Commit-SHA und kein Release-Eintrag gefunden; daher datieren wir aktuelle Aussagen der Model Card nicht auf dieses Datum zurück.
- Der anfängliche Veröffentlichungszeitpunkt des ursprünglichen Checkpoints bleibt unbekannt. Die primären Belege belegen eine Lizenzantwort vom 20. Mai und eine Provider-Support-Anfrage vom 21. Mai, nicht den ersten Upload.
- Die Verfügbarkeit der gehosteten Demo bleibt ungeprüft. Die Demo-URL wurde aufgelöst, zeigte aber weder einen prüfbaren API-Vertrag noch einen erfolgreichen Inferenznachweis.
- Die MLX-Distribution ist eine Änderung des Deployment-Formats. Die abgerufenen Quellen belegen weder einen neuen Marlin-2B-Kern-Checkpoint noch neue Fähigkeiten.
- Es wurde keine offizielle minimale NVIDIA-VRAM-Anforderung gefunden.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://huggingface.co/NemoStation/Marlin-2B | NemoStation/Marlin-2B · Hugging Face | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B/tree/main | NemoStation/Marlin-2B at main | 2026-09-05 |
| https://huggingface.co/spaces/huggingface/InferenceSupport/discussions/10010 | huggingface/InferenceSupport · NemoStation/Marlin-2B | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B/discussions/1 | NemoStation/Marlin-2B · 👉 Marlin-2B model? "Open Source" -- my ass! | 2026-09-05 |
| https://nemostation.com/blog/marlin-2b-the-map-was-wrong | Part 1: The Map Was Wrong — Nemostation | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B/discussions/9 | NemoStation/Marlin-2B · use marlin on a remote GPU machine ? third party providers ? | 2026-09-05 |
| https://huggingface.co/NemoStation/models | NemoStation (Nemo Station) | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B-MLX-8bit | NemoStation/Marlin-2B-MLX-8bit · Hugging Face | 2026-09-05 |
| https://huggingface.co/docs/transformers/v4.43.3/custom_models | Building custom models · Hugging Face | 2026-09-05 |
| https://vlm.nemostation.com | vlm.nemostation.com | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:marlin-2b`, Thread `marlin-2b`, 1 datiertes Ereignis 2026-05-21 → 2026-05-21.
- **Praktischer Hinweis:** Wir können die Evaluierung ab 2026-05-21 über die verlinkte Hugging-Face-Modellseite und die begleitende VLM-Website beginnen. Vor einer Verwendung sollten Model Card, unterstützte Aufgaben, Lizenz und genaue Version überprüft werden.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.

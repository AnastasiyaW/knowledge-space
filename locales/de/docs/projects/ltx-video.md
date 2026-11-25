---
title: "LTX-2.3"
category: projects
date: 2026-07-30
tags: [ltx-video, project]
aliases: ["LTX Video", "LTX-2.3"]
level: 3
source_sha256: 38d216683489406a70db0179a5706d6f9895ebb94ac526e49131f6a3f05635c6
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.3 {#ltx-23}

**Entwicklungslinie:** `project:ltx-video` · Thread `ltx-video`  
**Letztes Ereignis:** 2026-07-30 · 3 datierte Einträge seit 2026-03-05 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

LTX-2.3 ist ein auf 22B-DiT basierendes Audio-Video-Foundation-Modell für Teams, die synchronisierte Videos und Audio lokal, in ComfyUI oder über die LTX API generieren.

- Generierung: Text-zu-Video und Bild-zu-Video.
- Pro-Funktionen: Audio-zu-Video, Retake, Extend und Reframe.
- Gewichtspfade: dev-, distilled-, fp8- und Latent-Upscaler-Checkpoints.

22B Parameter; das aktuelle Hugging-Face-Repository umfasst 156 GB, der dev-Checkpoint allein 46,1 GB. Wir behalten es für bestehende Integrationen und 2.3-spezifische Adapter; neue Arbeiten zu Multi-Shot, Footage-Bearbeitung oder tiefem Fine-Tuning beginnen auf LTX-2.5.

## Entwicklungslinie {#development-line}

- **2026-03-05 — LTX-2.3 wurde mit Dokumentation und einem Text-zu-Video-Playground vorgestellt.** Fast übernahm Text-zu-Video und Bild-zu-Video, während Pro Audio-zu-Video, Retake und Extend hinzufügte; 22B-dev-/distilled-Gewichte und Latent Upscaler wurden ausgeliefert.
- **2026-03-05 — LTX-2.3-Modelldateien und ein ComfyUI-Text-zu-Video-Workflow wurden verlinkt.** Fast übernahm Text-zu-Video und Bild-zu-Video, während Pro Audio-zu-Video, Retake und Extend hinzufügte; 22B-dev-/distilled-Gewichte und Latent Upscaler wurden ausgeliefert.
- **2026-07-30 — Ein LTX-2.3 22B IC LoRA für Relighting wurde veröffentlicht.** Am 2026-07-30 wurde eine Hugging-Face-Ressource mit dem Namen LTX-2.3-22B-IC-LoRA-Relight verlinkt. Dies ist eine wesentliche Erweiterung der LTX-2.3-Linie, da sie über eine LoRA-Ressource eine spezialisierte Relighting-Fähigkeit ergänzt.

## Was sich geändert hat {#what-changed}

- **2026-03-05** — LTX-2.3 wurde zum API-Standard: Fast übernahm Text-zu-Video und Bild-zu-Video, während Pro Audio-zu-Video, Retake und Extend hinzufügte; 22B-dev-/distilled-Gewichte und Latent Upscaler wurden ausgeliefert.
- **2026-04-23** — Asynchrone HDR-Konvertierung ergänzte die SDR-zu-EXR-Ausgabe.
- **2026-05-03** — Async V2 wurde auf Text-zu-Video, Bild-zu-Video, Audio-zu-Video, Retake und Extend erweitert.
- **2026-07-02** — LTX-2 wurde abgekündigt, mit vorübergehendem automatischem Routing zu LTX-2.3.
- **2026-07-07** — Asynchrones Video-Reframe ergänzte generierte Füllung für ein neues Seitenverhältnis.
- **2026-07-30** — LTX-2.3-22B-IC-LoRA-Relight ergänzte kontrolliertes Relighting von Außenvideos aus einem Quellclip plus einer Lichtrichtungskugel.
- **2026-08-02** — LTX-2.3 Text-zu-Video und Bild-zu-Video erhielten eine 720p-Stufe.
- **2026-08-11** — LTX-2.5 ergänzte Fast bis 4K, Pro bei 720p/1080p, Kamerabewegung, Bild-zu-Video mit letztem Frame und automatische Dauer; es ist nun der empfohlene Ausgangspunkt.
- **2026-08-16** — LTX-2-API-Modell-IDs funktionieren nicht mehr; verbleibende Migrationsziele sind LTX-2.3 und LTX-2.5.

## So wird es verwendet {#how-to-use-this}

Ab 2026-03-05 können Praktiker LTX-2.3 über die dokumentierte Text-zu-Video-Route oder den verlinkten ComfyUI-Workflow nutzen; ab 2026-07-30 sollten sie den dedizierten 22B-IC-Relighting-LoRA evaluieren, wenn Relighting erforderlich ist.

1. Behalten Sie LTX-2.3 für eine laufende Integration oder einen 2.3-spezifischen Adapter bei; wählen Sie LTX-2.5 für ein neues Projekt.
  — <https://ltx.io/model/ltx-2-3>
2. Erstellen Sie in der Developer Console einen API-Schlüssel und senden Sie anschließend eine Text-zu-Video- oder Bild-zu-Video-Anfrage.
  — <https://docs.ltx.video/quickstart>
3. Verwenden Sie `ltx-2-3-fast` für Text-/Bild-Vorschauen; verwenden Sie `ltx-2-3-pro`, wenn der Workflow Audio-zu-Video, Retake, Extend oder Reframe benötigt.
  — <https://docs.ltx.io/models/ltx-2-3>
4. Für den Produktivbetrieb senden Sie einen V2-Async-Job, speichern dessen Job-ID, pollen bis zum Abschluss und laden die Ergebnis-URL herunter.
  — <https://docs.ltx.io/async-jobs>
5. Für einen lokalen Lauf klonen Sie LTX-2, führen `uv sync` aus, laden LTX-2.3 sowie Gemma 3 12B herunter und wählen dann die distilled-Pipeline für Geschwindigkeit oder die zweistufige HQ-Pipeline für Qualität.
  — <https://huggingface.co/Lightricks/LTX-2.3/blob/main/README.md>
6. Aktualisieren Sie in ComfyUI zuerst ComfyUI, laden Sie den mitgelieferten Text-zu-Video-Workflow und legen Sie dessen fp8-Checkpoint, LoRAs und Spatial Upscaler in den benannten Modellordnern ab.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_t2v.json>
7. Für Relighting von Außenvideos verwenden Sie den offiziellen einstufigen Graphen mit dem Relight-IC-LoRA bei Gewicht 1.0 und einem Quellclip, der die Lichtrichtungskugel enthält.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight>

## Best Practices {#best-practices}

- Behandeln Sie Breite und Höhe, die durch 32 teilbar sind, und Frame-Anzahlen, die durch 8+1 teilbar sind, als Eingabevertrag; andernfalls mit -1 auffüllen und nach der Generierung zuschneiden.
  — <https://huggingface.co/Lightricks/LTX-2.3/blob/main/README.md>
- Schreiben Sie einen fokussierten, chronologischen Shot mit expliziter Aktion, Kamera, Licht und Audio; formulieren Sie Prompts aus anderen Videomodellen um, statt deren Tags oder Shot-Listen unverändert zu übernehmen.
  — <https://docs.ltx.io/api-documentation/implementation-guides/prompting-guide>
- Verwenden Sie Fast für iterative Text-/Bild-Generierung und reservieren Sie Pro für das Endpoint-Set, das es benötigt.
  — <https://docs.ltx.io/models/ltx-2-3>
- Verwenden Sie asynchrone Jobs für Produktivlasten, statt eine langlebige synchrone Verbindung offen zu halten.
  — <https://docs.ltx.io/async-jobs>
- Beim Relighting bleiben Sie bei Außenaufnahmen, richten die Kugel-Referenz am Zielclip aus, verwenden den minimalen Richtungsprompt und vermeiden den echten zweistufigen Pfad, da Stufe 2 die Konditionierung verwirft.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight>
- Bei der Migration von LTX-2 trainieren Sie eigene LoRAs für den Latent Space von LTX-2.3 neu, statt von Drop-in-Kompatibilität auszugehen.
  — <https://ltx.io/model/ltx-2-3>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2026-03-05 — „Eigene LTX-2-LoRAs funktionieren unverändert auf LTX-2.3“ ist veraltet; für den Latent Space von 2.3 ist ein Retraining erforderlich.
- 2026-08-11 — „LTX-2.3 ist der empfohlene Start für ein neues Projekt“ wird durch LTX-2.5 ersetzt; LTX-2.3 bleibt für bestehende Integrationen unterstützt.
- 2026-08-16 — „`ltx-2-fast` und `ltx-2-pro` bleiben gültige API-Modell-IDs“ ist veraltet; diese Anfragen liefern Fehler.

## Weiterhin unbekannt {#still-unknown}

- Der Eintrag vom 2026-07-30 ist eine Veröffentlichung eines First-Party-IC-LoRA-Adapters und kein neuer LTX-2.3-Basis-Checkpoint; die verfügbaren Quellen legen nicht fest, ob jede Adapter-Veröffentlichung in die Historie des Kernmodells gehört.
- Die Modellkarte zu Relight zeigt kein eigenständiges Veröffentlichungsdatum; der Zeitpunkt wird deshalb auf 2026-07-30 verankert, während der technische Umfang als First-Party-verifiziert gilt.
- Die ursprüngliche Studio-URL für Text-zu-Video leitet inzwischen auf die Studio-Startseite weiter; ohne datierten Snapshot lassen sich die genaue Oberfläche und Verfügbarkeit vom 2026-03-05 nicht rekonstruieren.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://ltx.io/model/ltx-2-3 | LTX-2.3: Vorherige Generation des KI-Videomodells | LTX | 2026-09-04 |
| https://docs.ltx.video/quickstart | Schnellstart | LTX-Dokumentation | 2026-09-04 |
| https://app.ltx.studio/ltx-2-playground/t2v | KI-Videoproduktion | LTX | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3/tree/main | Lightricks/LTX-2.3 at main | 2026-09-04 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_t2v.json | workflow_templates/templates/video_ltx2_3_t2v.json at main · Comfy-Org/workflow_templates · GitHub | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight | Lightricks/LTX-2.3-22b-IC-LoRA-Relight · Hugging Face | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3/commits/main | Commits · Lightricks/LTX-2.3 | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3/blob/main/README.md | README.md · Lightricks/LTX-2.3 at main | 2026-09-04 |
| https://docs.ltx.io/models/ltx-2-3 | LTX-2.3 | LTX-Dokumentation | 2026-09-04 |
| https://docs.ltx.io/api-documentation/implementation-guides/prompting-guide | Prompting-Leitfaden | LTX-Dokumentation | 2026-09-04 |
| https://docs.ltx.io/async-jobs | Asynchrone Jobs | LTX-Dokumentation | 2026-09-04 |
| https://docs.ltx.io/api-changelog | API-Changelog | LTX-Dokumentation | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:ltx-video`, Thread `ltx-video`, 3 datierte Ereignisse 2026-03-05 → 2026-07-30.
- **Praktischer Hinweis:** Ab 2026-03-05 können Praktiker LTX-2.3 über die dokumentierte Text-zu-Video-Route oder den verlinkten ComfyUI-Workflow nutzen; ab 2026-07-30 sollten sie den dedizierten 22B-IC-Relighting-LoRA evaluieren, wenn Relighting erforderlich ist.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

---
title: "Krea2-realism — Krea2-LoRAs"
category: projects
date: 2026-07-04
tags: [krea2-loras, krea2-realism, project]
aliases: ["Krea2-realism"]
level: 2
source_sha256: f8add336247b196f6cf4261cde724b26766d8cbb3f92378d128c88bd96929348
translation: machine
translated_at: '2026-10-24'
---
# Krea2-realism — Krea2-LoRAs {#krea2-realism-krea2-loras}

**Entwicklungslinie:** `project:krea2-realism` · Thread `krea2-loras`  
**Letztes Ereignis:** 2026-07-04 · 1 datiertes seit 2026-07-04 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Krea2-realism ist eine Community-LoRA-Linie für das lizenzgeschützte Text-zu-Bild-Modell Krea 2 Turbo.

- V1 zielt auf SFW- und NSFW-fotorealistische Motive.
- V2 zielt auf Gesichtsausdruck, Textur, Beleuchtung, Komposition und Kompatibilität mit Character-LoRAs.
- Dient der Generierung und Bild-zu-Bild-Verarbeitung, ist aber kein Bildbearbeitungsmodell.

Die gepflegte Anleitung zu V2 empfiehlt einen Prompt in natürlicher Sprache mit 4–5 Sätzen und eine LoRA-Stärke von 1,5–2,0.

Wir verwenden V2 für neue Krea-2-Arbeiten, besonders wenn ein Character-LoRA sein Gesicht behalten muss. V1 behalten wir nur, um ein bestehendes Setup zu reproduzieren.

## Entwicklungslinie {#development-line}

- **2026-07-04 — Versionsspezifische Modellreferenzen für Krea2 Realism v1 erfasst.** Am 2026-07-04 hat die Entwicklungslinie Krea2-realism zwei versionsspezifische Civitai-Referenzen für Krea2 Realism v1 erfasst. Die Links verweisen auf unterschiedliche Modellversions-Artefakte, 3066973 und 3090634, daher verfolgen wir die verfügbaren Versionen in der Projekthistorie.

## Änderungen {#what-changed}

- 2026-06-24 — Krea2-realism-V1, Modellversion 3066973, erschien als Krea-2-Realismus-LoRA für SFW- und NSFW-Generierung.
- 2026-07-02 — Krea2-realism-V2, Modellversion 3090634, ersetzte V1 als aktive Revision. Sie brachte natürlichere Gesichter, verbesserte Textur, Beleuchtung und Komposition sowie eine bessere Koexistenz mit Character-LoRAs.
- 2026-07-04 — Die Links zu den Modellversionen von V1 und V2 wurden gemeinsam gesammelt. Dies war kein eigenständig datiertes Release.

## Verwendung {#how-to-use-this}

Ab 2026-07-04 fixieren wir Krea2 Realism v1 über die exakte Civitai-modelVersionId und dokumentieren, welche der beiden referenzierten Versionen verwendet wurde, statt die Modellseite als einzelnes unversioniertes Artefakt zu behandeln.

1. Zugriff auf Krea 2 Turbo beantragen und die Community-Lizenz akzeptieren, bevor das Basismodell heruntergeladen oder ausgeführt wird.
  — <https://huggingface.co/krea/Krea-2-Turbo>
2. Krea2-realism-V2 herunterladen, die aktuelle Revision dieser LoRA-Linie.
  — <https://huggingface.co/RudySen/Krea2-realism-V2>
3. In ComfyUI die LoRA-Datei in `ComfyUI/models/loras/` ablegen und sie in einem Krea-2-Workflow über einen Load-LoRA-Node auswählen.
  — <https://note.com/yasashii_maou/n/naf58ef9a48fb?hl=en>
4. Falls verfügbar, vom V1-Workflow ausgehen und nur das LoRA durch V2 ersetzen. Bild-zu-Bild verwenden, statt es als dedizierten Editor zu behandeln.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/>
5. Die Szene in einem kurzen Absatz in natürlicher Sprache beschreiben. Das LoRA-Gewicht gegen das gewählte Motiv und das Character-LoRA abstimmen und rendern.
  — <https://huggingface.co/RudySen/Krea2-realism-V2>

## Best Practices {#best-practices}

- V2 gegenüber V1 bevorzugen, wenn ein Character-LoRA kombiniert wird: V2 verändert keine Gesichter, die von anderen Character-LoRAs vorgegeben werden.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/>
- Eine Szenenbeschreibung mit 4–5 Sätzen statt Tag-Stapeln verwenden. Für einen kontrollierten Vergleich bei etwa Stärke 1,0 beginnen und dann 1,5–2,0 testen, falls das Ergebnis mehr Wirkung braucht.
  — <https://huggingface.co/RudySen/Krea2-realism-V2>
- V2 als Komponente für Bildgenerierung oder Bild-zu-Bild behandeln, nicht als semantischen Bildeditor.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/>

## Dadurch ersetzt {#superseded-by-this}

- 2026-06-24 — Krea2-realism-V1 (Modellversion 3066973) wird für neue Arbeiten durch Krea2-realism-V2 (Modellversion 3090634, veröffentlicht 2026-07-02) ersetzt. Der V1-Workflow bleibt nutzbar, indem das LoRA ausgetauscht wird.

## Weiterhin unbekannt {#still-unknown}

- Die ursprünglichen Civitai-Endpunkte waren nicht erreichbar, daher konnten Modellmetadaten, Download-Verfügbarkeit und Lizenzbedingungen auf diesen Seiten nicht verifiziert werden.
- Die Hugging-Face-Spiegelung von V2 deklariert MIT, während für das Krea-2-Basismodell die Krea 2 Community License gilt. Die anwendbaren Weitergabe- und Nutzungsbedingungen für den kombinierten Workflow müssen anhand der ursprünglichen Modellseite bestätigt werden.
- Keine Quelle dokumentiert ein Release am 2026-07-04 selbst. Dieses Datum erfasst beide Versionslinks und keine neue Modelländerung.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://civitai.red/models/2728365/krea2-realism-v1?modelVersionId=3066973 | Krea2-realism-V1, Modellversion 3066973 | 2026-09-05 |
| https://civitai.red/models/2728365/krea2-realism-v1?modelVersionId=3090634 | Krea2-realism-V2, Modellversion 3090634 | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ueq9au/one_lora_for_krea_2_sfw_and_not_sfw_realism/ | Ein LoRA für Krea 2. SFW- und Not-SFW-Realismus. | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/ | Krea2-realism-V2 ist endlich da! Die Dinge sind etwas wild geworden (im besten Sinne) | 2026-09-05 |
| https://huggingface.co/RudySen/Krea2-realism-V2 | RudySen/Krea2-realism-V2 | 2026-09-05 |
| https://huggingface.co/krea/Krea-2-Turbo | krea/Krea-2-Turbo | 2026-09-05 |
| https://note.com/yasashii_maou/n/naf58ef9a48fb?hl=en | [ComfyUI] Ein Memo zur Verwendung des Realismus-LoRA „realism-V2“ für Krea 2. Mit Bildern | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:krea2-realism`, Thread `krea2-loras`, 1 datiertes Ereignis 2026-07-04 → 2026-07-04.
- **Praktischer Hinweis:** Ab 2026-07-04 fixieren wir Krea2 Realism v1 über die exakte Civitai-modelVersionId und dokumentieren, welche der beiden referenzierten Versionen verwendet wurde, statt die Modellseite als einzelnes unversioniertes Artefakt zu behandeln.
- **Konfidenz:** mittel. Die datierten Ersetzungsvermerke oben sind maßgeblich dafür, was veraltet ist.

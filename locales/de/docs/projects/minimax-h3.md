---
title: "MiniMax H3"
category: projects
date: 2026-07-31
tags: [minimax, minimax-h3, project]
aliases: ["MiniMax H3"]
level: 3
source_sha256: d0bfb5f318edcffa9e5e9d6d56fff7653ccf6defeac5a94ebb68563b8f57cdde
translation: machine
translated_at: '2026-10-24'
---
# MiniMax H3 {#minimax-h3}

**Entwicklungslinie:** `project:minimax-h3` · Thread `minimax-h3`  
**Letztes Ereignis:** 2026-07-31 · 1 datiertes Ereignis seit 2026-07-31 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

MiniMax H3 ist ein audiovisuelles Open-Weight-Video-Basismodell mit 33B Parametern für Kreative und Entwickler, die zwischen lokaler 768p-Generierung und einem API-gestützten 2K-Workflow wählen.

- Eingaben: Text, erstes/letztes Frame oder Referenzen aus Bild, Video und Audio.
- Ausgabe: synchronisiertes Video mit nativem Stereo-Audio; FL2VA deckt Text- und Keyframe-Arbeit ab, Ref2VA deckt multimodale Referenzarbeit ab.
- Grenze: 4–15 Sekunden; Context-IR und H3-Regenerate-2K bleiben im offiziellen vollständigen 2K-Workflow gehostet.

## Entwicklungslinie {#development-line}

- **2026-07-31 — MiniMax veröffentlicht einen offiziellen Blogbeitrag zu MiniMax H3.** MiniMax hat H3 mit multimodalem Kontext und Video mit nativem Stereo bis 2K/15 Sekunden vorgestellt; die Gewichte wurden für eine spätere Veröffentlichung angekündigt.

## Was sich geändert hat {#what-changed}

- 2026-07-31: MiniMax hat H3 mit multimodalem Kontext und Video mit nativem Stereo bis 2K/15 Sekunden vorgestellt; die Gewichte wurden für eine spätere Veröffentlichung angekündigt.
- 2026-08-03: MiniMax hat die Gewichte von H3 Base veröffentlicht, mit FL2VA- und Ref2VA-Checkpoints, während Context-IR und die 2K-Regenerierung in der gehosteten Pipeline blieben.
- 2026-08-10: Ein verlinktes AMA hat Hinweise zu Prompts und Workflow sowie Pläne für künftige lokale Veröffentlichungen präzisiert; es war keine neue versionierte Modellveröffentlichung.
- 2026-08-27: fal hat H3 Max veröffentlicht, eine nachtrainierte Ableitung von MiniMax H3, die über fal angeboten wird.

## Wie man es verwendet {#how-to-use-this}

Ab 2026-07-31 sollte man zur Bewertung des Projekts zunächst die offizielle MiniMax-H3-Seite aufrufen. Funktionsumfang und Einsatzreife sollten nicht allein aus frühen Materialien abgeleitet werden.

1. Für den gehosteten Weg einen API-Schlüssel erstellen und eine application/json-Anfrage mit Bearer-Authentifizierung an den Endpunkt zur Videogenerierung für H3 senden.
  — <https://platform.minimax.io/docs/api-reference/video-generation-v2-create>
2. MiniMax-H3 auswählen, ein nicht leeres Textelement angeben und dann entweder erstes/letztes Frame oder Referenz-Bild-, Video- und Audioeingaben hinzufügen; die beiden Eingabemodi können nicht in einer Anfrage kombiniert werden.
  — <https://platform.minimax.io/docs/api-reference/video-generation-v2-create>
3. Die H3-Auflösung auf 768P oder 2K und die Dauer auf 4 bis 15 Sekunden setzen, anschließend den Task abfragen oder einen Callback für die Zustände queued, running, succeeded, failed oder cancelled registrieren.
  — <https://platform.minimax.io/docs/api-reference/video-generation-v2-create>
4. Für lokales 768p FL2VA für Text- bzw. erstes/letztes-Frame-Arbeit oder Ref2VA für multimodale Referenzarbeit herunterladen und anschließend den passenden H3-Base-Checkpoint mit einem unterstützten Framework bereitstellen.
  — <https://www.minimax.io/news/minimax-h3-open-source>
5. Für eine gehostete nachtrainierte Ableitung statt der offenen Base-Variante H3 Max von fal über dessen Playground oder API verwenden.
  — <https://blog.fal.ai/introducing-h3-max-by-fal/>

## Bewährte Praktiken {#best-practices}

- Context-IR als Planungs- bzw. Vorverarbeitungsschritt verwenden oder dessen Struktur anhand der Prompt-Hinweise des Anbieters nachbilden, bevor Arbeiten an H3 Base gesendet werden.
  — <https://www.minimax.io/news/minimax-h3-open-source>
- Bei Arbeiten mit erstem/letztem Frame die Anweisung zur Frame-Ausrichtung im Base-Leitfaden befolgen und einen kontinuierlichen Verlauf zum letzten Frame beschreiben; die Schnittzeitpunkte späterer Einstellungen müssen streng monoton steigen.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md>
- Bei vollständiger Referenzarbeit jede Bezeichnung Subject, Picture, Video und Audio einmal definieren und ihre Bedeutung beibehalten; angeben, ob Audio kopiert oder nur referenziert wird.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md>
- Die lokale Ausgabe von H3 Base als 768p behandeln; den angegebenen vollständigen 2K-Workflow verwenden, statt anzunehmen, dass Context-IR oder H3-Regenerate-2K mit den Gewichten ausgeliefert werden.
  — <https://www.minimax.io/news/minimax-h3-open-source>
- Die Community License vor kommerziellem oder gehostetem Einsatz prüfen: Sie schließt mehrere Gebiete aus und verlangt eine gesonderte Genehmigung ab einem Jahresumsatz von 20 Mio. US-Dollar.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE>

## Durch dies ersetzt {#superseded-by-this}

- 2026-08-03: der Stand vom 2026-07-31, in dem die Veröffentlichung der MiniMax-H3-Gewichte nur für die kommenden Tage geplant war.

## Weiterhin unbekannt {#still-unknown}

- Ob MiniMax-H3-Max in der MiniMax-API und H3 Max bei fal denselben Checkpoint verwenden.
- Ob MiniMax H3-Context-IR, H3-Regenerate-2K oder deren Sparse-Attention-Implementierung für die lokale Nutzung veröffentlicht hat.
- Mindestanforderungen an GPU bzw. VRAM für die lokale Bereitstellung; der SGLang-Befehl ist ein Beispiel mit vier GPUs und keine Mindestspezifikation.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://www.minimax.io/blog/minimax-h3 | MiniMax H3: An Open Model Breaking the Boundaries Between Tasks and Modalities - MiniMax Research | MiniMax | 2026-09-04 |
| https://www.minimax.io/news/minimax-h3-open-source | Open General Intelligence: MiniMax H3 Is Now Open Source - MiniMax News | MiniMax | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/1vh9rtw/ama_minimax_h3_team_ask_us_anything_about_our/ | AMA: MiniMax H3 Team — Ask us anything about our open video generation model, training, and future plans : r/StableDiffusion | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/video-generation-v2-create | Create Video Generation Task - MiniMax API Docs | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md | docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md · MiniMaxAI/MiniMax-H3 at main | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md | docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md · MiniMaxAI/MiniMax-H3 at main | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE | LICENSE · MiniMaxAI/MiniMax-H3 at main | 2026-09-04 |
| https://blog.fal.ai/introducing-h3-max-by-fal/ | Introducing H3 Max by fal | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:minimax-h3`, Thread `minimax-h3`, 1 datiertes Ereignis vom 2026-07-31 → 2026-07-31.
- **Praktischer Hinweis:** Ab 2026-07-31 sollte man zur Bewertung des Projekts zunächst die offizielle MiniMax-H3-Seite aufrufen. Funktionsumfang und Einsatzreife sollten nicht allein aus frühen Materialien abgeleitet werden.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.

<!-- live-update:d336eed43fa2789e79635be365c8a2a0bb09b0d8651d55809dfa1659a5457423 -->
## 2026-09-05 — MiniMax H3 Semantic Bridge fügt einen Adapter für den FL2VA-Textpfad von H3 hinzu {#2026-09-05-minimax-h3-semantic-bridge-adds-an-adapter-for-h3s-fl2va-text-path}

MiniMax H3 Semantic Bridge ist ein ComfyUI-Conditioning-Adapter für den standardmäßigen, textkonditionierten FL2VA-Workflow von MiniMax H3. Es handelt sich um ein Community-Projekt, nicht um eine offizielle Veröffentlichung von MiniMax oder SenseNova. Eine Ref2VA-Unterstützung wurde nicht veröffentlicht, weil Tests des Autors eine Verschlechterung von Gesang und Lippensynchronisation ergaben.

### Verwendung und Praktiken {#usage-and-practices}

- Das veröffentlichte Archiv des Custom Nodes unter ComfyUI/custom_nodes/ installieren. MiniMaxH3_SemanticBridge_v1.safetensors unter ComfyUI/models/semantic_bridge/ ablegen, ComfyUI neu starten und mit dem mitgelieferten Workflow-Beispiel beginnen. [Quelle](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)
- v1 nur mit dem standardmäßigen, textkonditionierten FL2VA-Pfad von MiniMax H3 verwenden. Es nicht in Ref2VA oder einen anderen referenzkonditionierten Workflow einbinden. [Quelle](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)
- Mit Alpha 0,10 und Magnitude-Matching pro Token beginnen. Native H3-Ausgabe und Ausgabe mit aktivierter Bridge mit identischem Prompt, Seed und identischen Generierungseinstellungen vergleichen. Die veröffentlichten A/B-Vergleiche mit Alpha 0,15 als Beispiele betrachten, nicht als allgemeingültige Voreinstellung. [Quelle](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)
- Die Kosinus-Messungen des Autors im Repräsentationsraum getrennt von Aussagen zur Videoqualität halten. Die Veröffentlichung besagt, dass sie die Übereinstimmung mit einer aus einem Teacher abgeleiteten Repräsentation messen, nicht wahrgenommene Qualität oder eine allgemeine Verbesserung der Prompt-Treue. [Quelle](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)

### Zusätzliche Belege {#additional-evidence}

- 2026-09-05: Das öffentliche Repository ist speach1sdef178/MiniMax-H3-Semantic-Bridge in der Revision 8c2d9b0edb844d6002864a9addd61458dbe81c22. Öffentliche Dateien umfassen den v1-Adapter, das Archiv des Custom Nodes, Workflow-Beispiele, Prüfsummen, README, Forschungsmaterial, NOTICE und Lizenzen. Es handelt sich um ein Community-Projekt, nicht um eine offizielle Veröffentlichung von MiniMax oder SenseNova. [Quelle](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/tree/8c2d9b0edb844d6002864a9addd61458dbe81c22)
- 2026-09-05: Der Autor berichtet, dass v1 ausschließlich auf den standardmäßigen, textkonditionierten FL2VA-Pfad von MiniMax H3 gehört. Ref2VA-/Referenzaudio-Experimente verschlechterten Gesang und Lippensynchronisation, daher wurde kein Ref2VA-Node veröffentlicht. Alpha 0,10 ist der Ausgangspunkt des Autors. Die A/B-Beispiele mit Alpha 0,15 sind qualitative Illustrationen, kein Nachweis allgemeiner Verbesserungen. [Quelle](https://www.reddit.com/r/StableDiffusion/comments/1w7wtco/i_tried_transferring_semantic_representations/)

### Grenzen und offene Fragen {#limits-and-open-questions}

- Für genau diesen Adapter wurde zum Stand 2026-09-05 keine unabhängige Reproduktion, kein standardisierter Benchmark für menschliche Präferenzen und keine separate Leistungsvalidierung durch Dritte gefunden.
- Die Angabe von 5–6 Mio. Parametern, die Repräsentationsmetriken, der Trainingssplit und die Kompatibilitätsaussagen sind vom Autor veröffentlichte Angaben der Veröffentlichung und hier nicht unabhängig geprüft.
- Chinesischsprachige Suchanfragen ergaben keine exakte zh-CN-Ankündigung, kein Tutorial und keine unabhängige Reproduktion für MiniMax H3 Semantic Bridge. Das untersuchte Ergebnis zu MiniMaxH3 CondBridge Qwen3.5-4B betrifft ein anderes Projekt und darf nicht in dieses Ereignis einfließen.
- Das Paket wurde weder heruntergeladen noch ausgeführt. Laufzeitkompatibilität, Integrität der Artefakte über die genannte Revision hinaus, die Lizenzinterpretation und praktische Videogewinne bleiben ungeprüft.

<!-- Retained base: 10a35259638c923851e915e3b979bbd355ddaf2b; article blob: 3d4f380ad8d34d47f874ef8a5bfdcd7a04126e47 -->

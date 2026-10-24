---
title: "LTX2.3 Audio Reactive LoRA — LTX-Videomodelle"
category: projects
date: 2026-06-13
tags: [ltx-video-models, ltx2-3-audio-reactive-lora, ltx_video_models, project]
aliases: ["LTX2.3 Audio Reactive LoRA"]
level: 3
source_sha256: 81910924f12ceb644e27e1f7a4b57c89c53d6c6131d7a755c35cbd46490e00f0
translation: machine
translated_at: '2026-10-24'
---
# LTX2.3 Audio Reactive LoRA — LTX-Videomodelle {#ltx23-audio-reactive-lora-ltx-video-models}

**Entwicklungslinie:** `project:ltx2-3-audio-reactive-lora` · Thread `ltx-video-models`  
**Letztes Ereignis:** 2026-06-13 · 1 datiert seit 2026-06-13 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

LTX2.3 Audio Reactive LoRA ist ein LoRA-Adapter im fal-Repository für Lightricks/LTX-2.3, kein eigenständiges Basismodell, entwickelt für Ersteller von Musikvisualisierungen.

- Klangreaktion: verstärkt klanggesteuerte Pulsation, Partikel, Licht, Verformungen und Kamerabewegung.
- Pipeline-Modi: arbeitet in Audio-zu-Video und Bild+Audio-zu-Video mit einer Audiospur, einem Prompt und optional einem Anfangsbild.

Die Modellkarte empfiehlt eine Skalierung von 1.0–1.5, 24 fps und Clips von 5–15 s; eine exakte Beat-Erkennung ist nicht garantiert. Der Adapter eignet sich für kurze Visualisierungen mit klarer Geometrie, ersetzt aber keine bildgenaue Synchronisation.

## Entwicklungslinie {#development-line}

- **2026-06-13 — LTX2.3 Audio Reactive LoRA erschien auf Hugging Face unter fal.** Am 2026-06-13 wurde die LTX2.3-Audio-Reactive-LoRA-Linie mit einem direkten Hugging-Face-Link unter fal erfasst. Dies bietet einen öffentlichen Bezugspunkt für die Linie, doch die verfügbaren Belege belegen weder Modellfähigkeiten, Versionsdetails, Trainingsdaten noch Nutzungsbedingungen.

## Was sich geändert hat {#what-changed}

2026-06-12 — Die Kartenmetadaten wechselten von `private: true` zu `private: false`; dies kennzeichnet die Sichtbarkeit der Karte und ist keine unabhängige Laufzeitprüfung. 2026-06-13 — Die primäre Historie zeigt für diesen Tag keine separate datierte Revision für V1, V2 oder die API; der Link führte zu dem bereits sichtbaren Adapter. 2026-06-15 — Eine separate V2-Datei wurde hinzugefügt; die Karte des Autors behauptete stärkere Audioreaktivität, ohne einen unabhängigen Benchmark vorzulegen.

## Anwendung {#how-to-use-this}

Ab 2026-06-13 sollte dies als eigenständige, mit fal verknüpfte LTX-Videomodell-Linie behandelt werden; vor einer Übernahme ist die Hugging-Face-Modellkarte zu prüfen. Öffentliche Quellen liefern keine validierte Konfiguration und keine Leistungsangaben.

1. LTX-2.3 verwenden, statt die Basis durch LTX-2.5 zu ersetzen: Laut offizieller Dokumentation sind die Dateien inkompatibel, und das LoRA funktioniert nur mit dem Modell, auf dem es trainiert wurde.
  — <https://github.com/Lightricks/LTX-2>
2. `prompt`, verpflichtendes `audio_url` und `loras` in der aktuellen fal-API übermitteln; `image_url` ist optional, und der Endpunkt erlaubt bis zu drei LoRAs gleichzeitig.
  — <https://fal.ai/models/fal-ai/ltx-2.3-quality/audio-to-video/lora/api>
3. V1- oder V2-safetensors aus der Modellkarte zu `loras` hinzufügen, `transformer: "both"` setzen und im angegebenen Skalierungsbereich von 1.0–1.5 starten.
  — <https://huggingface.co/fal/ltx2.3-audio-reactive-lora>
4. `image_url` als Anfangsbild übergeben, um einen gezielteren Clip zu erhalten; `match_audio_length` aktiviert lassen, wenn die Videodauer der Audiolänge folgen muss.
  — <https://fal.ai/models/fal-ai/ltx-2.3-quality/audio-to-video/lora/api>
5. Das Ergebnis vor der Veröffentlichung auf Textlesbarkeit, Logotreue und Synchronisation prüfen.
  — <https://huggingface.co/fal/ltx2.3-audio-reactive-lora>

## Bewährte Vorgehensweisen {#best-practices}

- Den Adapter nicht mit einer anderen LTX-Release-Linie kombinieren: Laut offizieller Dokumentation funktioniert das LoRA nur mit dem Modell, auf dem es trainiert wurde.
  — <https://github.com/Lightricks/LTX-2>
- Dem Anfangsbild bewegliche Strukturen geben: Geometrie, Ebenen, Partikel, Lichtnähte oder Visualisierungsformen.
  — <https://huggingface.co/fal/ltx2.3-audio-reactive-lora>
- Eine saubere, kontrollierte visuelle Vorgabe als praktischen Schutz gegen chaotische Artefakte behandeln: Dies spiegelt einen einzelnen Nutzerlauf wider, nicht einen allgemeinen Benchmark.
  — <https://www.reddit.com/r/StableDiffusion/comments/1un6vh3/followup_followup_more_experimentation_with_the/>
- Bei einem komplexen Track mehrere Varianten erzeugen und die beste auswählen; ein Nutzertest berichtete bessere Ergebnisse bei spärlicheren Arrangements, wenn man unter etwa drei Renderings wählte.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulq1jk/followup_i_take_it_back_the_ltx_23_audioreactive/>

## Dadurch ersetzt {#superseded-by-this}

- 2026-06-12 — Der frühe Kartenstatus `private: true` ist veraltet: Ein Commit änderte das Sichtbarkeitsflag auf `private: false`; dies ersetzt nur den Kartenstatus.
- 2026-06-15 — Die Angabe, dass nur eine Adapterdatei existiert, ist veraltet: V2 wurde als separate Datei hinzugefügt; ein Ersatz von V1 durch V2 als Standard bleibt unbelegt.

## Weiterhin unbekannt {#still-unknown}

- Keine externe Primärquelle mit Datum 2026-06-13 ergänzt Fakten zu diesem Schritt selbst; `event_findings` bleibt leer.
- Trainingsdaten, Rank/Alpha, Zielmodule und ein reproduzierbares Trainingsrezept für diesen konkreten Adapter sind nicht veröffentlicht.
- Kein unabhängiger Benchmark vergleicht V1 mit V2; die Behauptung stärkerer Audioreaktivität stammt von der Karte des Autors.
- Lokale Ausführung, Gewichtsdownloads und fal-API-Aufrufe wurden in diesem Durchlauf nicht getestet; die aktuelle Dokumentation ersetzt keine Laufzeitprüfung.
- Die genaue Anwendbarkeit der LTX-2 Community License auf konkrete Anwendungsfälle wurde nicht analysiert.
- Chinesischsprachige Suchen ergaben keine unabhängigen Primär- oder Praxisquellen für genau diesen Adapter.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://huggingface.co/fal/ltx2.3-audio-reactive-lora | fal/ltx2.3-audio-reactive-lora · Hugging Face | 2026-09-05 |
| https://huggingface.co/fal/ltx2.3-audio-reactive-lora/commit/bca5b48eb77552e1f92e9916a22f9b3c6c0f3a66 | Set model card visibility metadata to public · fal/ltx2.3-audio-reactive-lora at bca5b48 | 2026-09-05 |
| https://huggingface.co/fal/ltx2.3-audio-reactive-lora/commit/9d432f6bd21fdda9848b7eeb3a3a12faa01c91ef | Add V2 LoRA as separate file · fal/ltx2.3-audio-reactive-lora at 9d432f6 | 2026-09-05 |
| https://huggingface.co/fal/ltx2.3-audio-reactive-lora/commit/23a333233d1df57d1279fd63a745e854375e8859 | Update model card for V2 · fal/ltx2.3-audio-reactive-lora at 23a3332 | 2026-09-05 |
| https://fal.ai/models/fal-ai/ltx-2.3-quality/audio-to-video/lora/api | Ltx 2.3 Quality Audio to Video API Docs | fal | 2026-09-05 |
| https://github.com/Lightricks/LTX-2 | Lightricks/LTX-2 — official Python inference and LoRA trainer package | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1un6vh3/followup_followup_more_experimentation_with_the/ | Follow-up follow-up: More experimentation with the audio-reactive LoRA for LTX-2.3 | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ulq1jk/followup_i_take_it_back_the_ltx_23_audioreactive/ | Follow-up: I take it back, the LTX 2.3 audio-reactive LoRA is actually pretty amazing | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:ltx2-3-audio-reactive-lora`, Thread `ltx-video-models`, 1 datiertes Ereignis 2026-06-13 → 2026-06-13.
- **Praktischer Hinweis:** Ab 2026-06-13 sollte dies als eigenständige, mit fal verknüpfte LTX-Videomodell-Linie behandelt werden; vor einer Übernahme ist die Hugging-Face-Modellkarte zu prüfen. Öffentliche Quellen liefern keine validierte Konfiguration und keine Leistungsangaben.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich für das, was veraltet ist.

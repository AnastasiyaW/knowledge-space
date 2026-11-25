---
title: "Audio Flamingo"
description: "Versionsbezogene Referenz für die Verständnis-Checkpoints Audio Flamingo 3, Music Flamingo und Audio Flamingo Next."
level: 4
source_sha256: faaf08c64e3a7f268c48caeca723319d73b4aee5d546e6b4a35d49bfdf9e5c7a
translation: machine
translated_at: '2026-10-24'
---
# Audio Flamingo {#audio-flamingo}

Audio Flamingo ist eine Forschungsfamilie von NVIDIA für das Verständnis von Audio. Audio Flamingo 3 (AF3), Music Flamingo und Audio Flamingo Next (AF-Next) sind verwandt, aber eigenständige Zweige. Der Status wurde am **27.08.2026** anhand der primären Projekt-, Paper-, Repository- und Model-Card-Quellen überprüft.

## Aktuelle Familienübersicht {#current-family-map}

| Zweig | Zweck | Aktueller Artefakt-Stand |
|---|---|---|
| Audio Flamingo 3 | Allgemeines Audio-Sprach-Verständnis | Früher veröffentlichter Forschungszweig |
| Music Flamingo | Verständnis und Schlussfolgern im Musikbereich | Eigenständiger Musikzweig; nicht als AF3-Point-Release behandeln |
| Audio Flamingo Next | Aktuelle Familie für das Verständnis langer Audioaufnahmen | 8B-BF16-Hugging-Face-Checkpoints: Instruction-, Thinking- und Captioning-Varianten |

Die offizielle Model Card `nvidia/audio-flamingo-next-hf` ist die maßgebliche Artefaktquelle für die AF-Next-Inferenz. Das ältere Repository `NVIDIA/audio-flamingo` ist älter als AF-Next und sollte nicht herangezogen werden, um alle aktuellen Funktionen oder Installationsdetails abzuleiten.

## Eingabevertrag von AF-Next {#af-next-input-contract}

| Eigenschaft | Verifizierter Wert aus der Model Card |
|---|---|
| Checkpoint-Familie | 8B BF16 |
| Varianten | Instruction, Thinking, Captioner |
| Audioformat | 16 kHz, Mono |
| Verarbeitungsfenster | 30 Sekunden |
| Maximal dokumentierte Dauer | 1.800 Sekunden / 30 Minuten |
| Laufzeitumgebung | Beispiel der Model Card mit Transformers |
| Gehosteter Inferenzanbieter | Zum Zeitpunkt der Überprüfung keiner angegeben |
| Lizenz | Nicht kommerziell; vor der Nutzung die genaue Lizenz in der Model Card prüfen |

Die Unterstützung langer Audioaufnahmen wird durch fensterweise Verarbeitung umgesetzt. „Unterstützt 30 Minuten“ bedeutet nicht einen einzelnen, unbegrenzten Kontext-Tensor, Echtzeit-Streaming oder speichersparende Inferenz.

Der veröffentlichte AF-Next-Checkpoint ist ein Modell für das Audioverständnis. Das breitere Forschungsprojekt behandelt Streaming-TTS und Voice-to-Voice-Fähigkeiten, diese sind jedoch **nicht im veröffentlichten Hugging-Face-Checkpoint enthalten**.

## Entwicklungsverlauf {#development-history}

| Datum | Strang | Ereignis | Zeitlicher Status |
|---|---|---|---|
| 27.10.2025 | Allgemeines Audio-Sprach-Verständnis | Audio Flamingo 3 veröffentlicht | Historische Grundlage |
| 15.11.2025 | Musikverständnis | Music Flamingo veröffentlicht | Aktueller, eigenständiger Zweig |
| 15.04.2026 | Allgemeines Audio-Sprach-Verständnis | Audio Flamingo Next veröffentlicht | Aktueller Nachfolgezweig |

AF3 kann im allgemeinen Audio-Sprach-Strang der Vorgänger von AF-Next sein. Music Flamingo bleibt ein eigenständiger Projektzweig, da sich Spezialisierung und Artefakte unterscheiden.

## Praktische Anwendung {#practical-use}

Die AF-Next-Variante wird anhand des Ausgabeverhaltens gewählt:

- **Instruction-Checkpoint:** direkte, anweisungsgeführte Analyse von Audio.
- **Thinking-Checkpoint:** schlussfolgernde Aufgaben, sofern der Vertrag der Model Card diesen Modus ausdrücklich unterstützt.
- **Captioner:** dichte oder strukturierte Audio-Beschreibungen.

Eingaben vor der Auswertung normalisieren:

```yaml
sample_rate_hz: 16000
channels: 1
duration_seconds: <0-to-1800>
checkpoint: nvidia/audio-flamingo-next-hf
checkpoint_revision: <immutable-revision>
variant: instruction-or-thinking-or-captioner
dtype: bfloat16
device: <exact-gpu>
transformers_version: <exact-version>
```

Bei langen Aufnahmen die Zeitversätze jedes 30-Sekunden-Fensters beibehalten, damit Antworten auf das Quellaudio zurückgeführt werden können. Das Verhalten bei Überlappung und Aggregation an der jeweiligen Zielaufgabe testen, statt anzunehmen, dass Fenstergrenzen semantisch neutral sind.

## Anwendungsfälle {#when-to-use}

- Audiobasierte Fragebeantwortung, Captioning und semantische Analyse im Rahmen des Aufgabenvertrags der Model Card.
- Lange Aufnahmen, bei denen der dokumentierte Pfad mit 30-minütiger Fensterverarbeitung nützlich ist.
- Forschungsevaluierung, sofern die nicht kommerzielle Lizenz akzeptabel ist.

Den veröffentlichten AF-Next-Checkpoint nicht als Nachweis für Streaming-Sprachsynthese, Voice Conversion oder kommerzielle Nutzungsrechte verwenden.

## Grenzen der Community-Belege {#community-evidence-boundary}

Im begrenzten Durchlauf wurde keine qualifizierte chinesischsprachige Quelle und kein reproduzierbares Speicherrezept für Consumer-Hardware akzeptiert. Eine konkrete Implementierungslücke wurde dokumentiert:

- [Issue #104](https://github.com/NVIDIA/audio-flamingo/issues/104) zeigt, dass `audio-flamingo-3-hf` in Transformers eine Mehrfach-Turn-Konversation mit zwei Audioeingaben mit einem `ValueError` für das Verhältnis 1:1 von Text und Audio-Anzahl ablehnt. Das Issue ist offen, ohne Antwort des Maintainers. Es betrifft AF3, nicht AF-Next, und macht die allgemeine Aussage zum „Multi-Audio-Dialog“ als generisches Transformers-Rezept unsicher.
- [Issue #106](https://github.com/NVIDIA/audio-flamingo/issues/106) dokumentiert ungelöste Unklarheiten in der Zeitachse des LongAudio-Datensatzes (Stitching-Lücken von 1 Sekunde gegenüber 10 ms sowie Segmente in falscher Reihenfolge). Dies betrifft die Reproduktion temporaler QA-Ergebnisse, nicht die gewöhnliche Checkpoint-Inferenz.

## Stolperfallen {#gotchas}

- **Problem:** Ergebnisse von AF3, Music Flamingo und AF-Next werden zusammengeführt -> **Lösung:** In jeder Aussage den Zweig und die Checkpoint-Variante nennen.
- **Problem:** „Unterstützung von 30 Minuten“ wird als Streaming oder als einmaliger Kontext gelesen -> **Lösung:** Den dokumentierten 30-Sekunden-Fensterungsvertrag beibehalten und die Aggregation testen.
- **Problem:** TTS/Voice-to-Voice wird dem AF-Next-HF-Checkpoint zugeschrieben -> **Lösung:** Aussagen zum Checkpoint auf die veröffentlichten Fähigkeiten zum Audioverständnis beschränken.
- **Problem:** Die nicht kommerzielle Lizenz wird ignoriert -> **Lösung:** Die genaue Checkpoint-Lizenz vor einer Produktnutzung prüfen und dokumentieren.
- **Problem:** Annahme, dass Multi-Audio-Forschungsergebnisse direkt auf das Chat-Template von AF3 in Transformers übertragbar sind -> **Lösung:** Den genauen Processor-Vertrag testen; Issue #104 berichtet von einem aktuellen Fehler wegen des Verhältnisses 1:1.

## Zeitlicher Status {#temporal-status}

- **Aktuell:** AF-Next-8B-BF16-Varianten der Model Card sowie deren Vertrag mit 16 kHz, Mono, 30-Sekunden-Fenstern und maximal 30 Minuten.
- **Historisch:** AF3-Zweig für allgemeines Audio.
- **Parallel:** Music-Flamingo-Zweig für Musikverständnis.
- **Im zitierten Checkpoint nicht veröffentlicht:** Streaming-TTS und Voice-to-Voice-Funktionen.

## Kurzbriefing für Agenten {#agent-brief}

Vor der Antwort `AF3`, `Music Flamingo` oder `AF-Next` eindeutig zuordnen. Bei AF-Next die aktuelle Model Card abrufen und die genaue Variante bestimmen. Audioformat, Dauer bzw. Fensterung, Datentyp, Hardware, Revision und Lizenz erhalten. Breitere Forschungsdemonstrationen nie als Fähigkeiten des veröffentlichten Checkpoints darstellen und Community-Beobachtungen getrennt von Fakten aus primären Artefakten kennzeichnen.

## Quellen {#sources}

- Audio-Flamingo-Repository: https://github.com/NVIDIA/audio-flamingo
- Audio-Flamingo-3-Projekt: https://research.nvidia.com/labs/adlr/AF3/
- Audio-Flamingo-Next-Checkpoint: https://huggingface.co/nvidia/audio-flamingo-next-hf
- Audio-Flamingo-Next-Paper: https://arxiv.org/abs/2604.10905
- Lücke bei Multi-Audio in Transformers für AF3: https://github.com/NVIDIA/audio-flamingo/issues/104
- Lücke bei der Reproduktion der LongAudio-Zeitachse: https://github.com/NVIDIA/audio-flamingo/issues/106

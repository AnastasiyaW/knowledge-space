---
title: "Block Causal Linear Attention"
description: "Block Causal Linear Attention ist der trainierte Mechanismus von SANA-Video für lange Videos mit einem kumulativen Attention-State fester Größe. Er ist kein generisches Plug-in für beliebiges Bild-Tiling oder DiTs."
category: architectures
tags: [sana-video, causal, kv-cache, temporal, linear-attention, long-video, diffusion-transformer]
aliases: ["BCLA", "Causal Linear Attention", "SANA-Video Attention"]
level: 2
source_sha256: 4154c0bd82035ea27bb0c4c5cffe1fe5adbc8954862c42d75bc516a323eba0a4
translation: machine
translated_at: '2026-10-24'
---
# Block Causal Linear Attention {#block-causal-linear-attention}

**Geprüfter Stand: 2026-09-04.** Block Causal Linear Attention ist der Mechanismus für langen Kontext, der für SANA-Video beschrieben wird. Er zerlegt ein Video in kausal geordnete Blöcke und überträgt einen kumulativen Linear-Attention-State fester Größe von früheren auf spätere Blöcke. Es handelt sich um eine trainierte Architekturkomponente und nicht um ein Nachbearbeitungsverfahren für beliebige Bildkacheln.

## Was SANA-Video tatsächlich verwendet {#what-sana-video-actually-uses}

SANA-Video erweitert die lineare DiT-Familie [[SANA]] für Video um eine zeitliche Positionsbehandlung und ein kausales Mix-FFN. Für die Generierung langer Videos formuliert die Arbeit Causal Linear Attention so um, dass ein Block kumulative Attention-States und Key-Zusammenfassungen früherer Blöcke benötigt, anstatt eines wachsenden KV-Caches pro Token.

Der Cache konstanter Größe ist Teil eines größeren, eng gekoppelten Designs:

- ein geordnetes blockweises autoregressives Diffusionsziel;
- ein kausaler Linear-Attention-State, der über vorherige Blöcke akkumuliert wird;
- zeitliche Positionsbehandlung innerhalb des Modells;
- ein kausales Mix-FFN, das zusätzlich das letzte Frame des vorherigen Blocks für die zeitliche Faltung vorhält;
- Trainings- und Post-Training-Verfahren, die dem Modell den Betrieb mit diesem State beibringen.

Die feste Cache-Größe reduziert das Speicherwachstum, das mit einem herkömmlichen langen Token-Cache verbunden ist. Allein daraus folgt jedoch keine zeitliche Qualität, und ein generisches DiT wird dadurch nicht kausal. Auch entfällt die Notwendigkeit einer Auswertung an den Blockgrenzen nicht.

## Keine Verallgemeinerung auf Bild-Tiling ohne Nachweis {#do-not-generalize-it-to-image-tiling-without-evidence}

Das Quellmaterial betrifft die Generierung langer Videos. Es validiert weder einen rasterweise gescannten Bild-Kachel-Workflow noch eine nahtfreie hochauflösende Bildsynthese oder ein generelles Argument zum kausalen State für beliebige Diffusionsmodelle.

Eine Implementierung, die kumulativen State in ein unverändertes Bildmodell einspeist, ist ein neues Forschungsexperiment. Sie benötigt eigene Trainings- und Kompatibilitätsnachweise, ein eigenes Positionsschema, eine eigene Blockreihenfolge und eine visuelle Validierung. Sie darf nicht als Verhalten von SANA-Video dargestellt werden.

## Integrationsvertrag {#integration-contract}

1. Eine offizielle SANA-Version wählen und die passende Dokumentation zu Modell und Konfiguration lesen.
2. Das deklarierte Modell, den VAE, den Attention-Kernel, die Blockreihenfolge und den Checkpoint der Implementierung gemeinsam verwenden.
3. Die Zustandsisolation explizit halten: Ein Generierungsstrom darf keinen Cache eines anderen Prompts, Seeds oder Videos wiederverwenden.
4. Modell- und Konfigurationsrevisionen, Prompt, Seed, Blockplan, Zustandsbehandlungsrichtlinie, Ausgabe und Logs aufbewahren.
5. Kurze Clips testen, bevor die Dauer erhöht wird, und danach Blockgrenzen, Bewegungskontinuität, Identität des Motivs und Prompt-Treue prüfen.

Die SANA-Familie entwickelt sich schnell. Spätere Versionen führen hybride Linear-/Softmax-Attention und Attention-Residual-Designs ein. Deren Leistung oder API darf daher nicht rückwirkend auf den ursprünglichen Block-Causal-Mechanismus übertragen werden.

## Abnahmeprüfungen {#acceptance-checks}

| Frage | Nachweis |
|---|---|
| Ist die vorgesehene Architektur tatsächlich aktiv? | passende offizielle Konfiguration, Checkpoint und Laufzeit-Trace |
| Ist der Cache korrekt isoliert und geordnet? | Zustandsnachweis pro Lauf und deterministische Wiederholung |
| Sind die Übergänge stabil? | sequenzielle Prüfung an jeder generierten Blockgrenze |
| Ist die behauptete Effizienz für diesen Build real? | gemessener Speicher und gemessene Latenz auf der deklarierten Hardware und bei der deklarierten Dauer |
| Ist es besser als eine einfachere Baseline? | Vergleich mit demselben Prompt gegen eine nicht-kausale oder kürzere Kontext-Baseline |

## Referenzen {#references}

- [SANA offizielles Repository](https://github.com/NVlabs/Sana)
- [SANA-Video-Paper](https://arxiv.org/abs/2509.24695)
- [SANA-Video-Dokumentation](https://nvlabs.github.io/Sana/docs/sana_video/)
- [SANA-Video-2.0-Dokumentation](https://nvlabs.github.io/Sana/docs/sana_video2/)

---
title: "Zeta-Chroma"
category: projects
date: 2026-03-18
tags: [project, zeta-chroma, zeta-chroma-base-model]
aliases: ["Zeta-Chroma"]
level: 3
source_sha256: f9b1b4cc021096a768c39cdc94f4b65d40477ee0abb6ae5aa30982f77f4f5c84
translation: machine
translated_at: '2026-10-24'
---
# Zeta-Chroma {#zeta-chroma}

**Entwicklungslinie:** `project:zeta-chroma` · Thread `zeta-chroma-base-model`  
**Letztes Ereignis:** 2026-03-18 · 1 datiertes Ereignis seit 2026-03-18 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Zeta-Chroma ist ein pixelbasierter Diffusion-Transformer für Text-zu-Bild, abgeleitet von Tongyi-MAI/Z-Image.

- Erzeugt Bilder direkt im RGB-Raum und verwendet kein VAE.
- Wird unter Apache-2.0 verbreitet.
- Läuft in ComfyUI; SD.Next hat am 28.04.2026 Unterstützung hinzugefügt.

Größenordnung: Der veröffentlichte BF16-Checkpoint ist etwa 13 GB groß.

Fazit: Das Modell eignet sich für experimentelle Bildgenerierung, bleibt aber WIP mit regelmäßig ersetzten Gewichten und schwankender Qualität.

## Entwicklungslinie {#development-line}

- **2026-03-18 — Zeta-Chroma-Basismodell-Artefakt erfasst.** Am 2026-03-18 hat die Zeta-Chroma-Entwicklungslinie einen Link auf ein Safetensors-Artefakt im Hugging-Face-Repository des Projekts erfasst. Verlinkte Social-Media- und Repository-Diskussions-URLs ordnen das Element derselben Projektlinie zu. Die angegebenen Links belegen weder die Fähigkeiten, das Training, die Lizenzierung noch die Veröffentlichungsbedingungen des Artefakts.

## Was sich geändert hat {#what-changed}

18.03.2026 — Ein früher Checkpoint `zeta-chroma-base-x0-pixel-dino-distance.safetensors` wurde verfügbar; eine spätere Repository-Beschreibung präzisiert, dass Zeta-Chroma ein WIP-Text-zu-Bild-Modell auf Basis von Tongyi-MAI/Z-Image ist.

01.03.2026 — Der Repository-Eigentümer schrieb vor, den frühen Checkpoint vor dem Laden in ComfyUI in das Comfy-Format zu konvertieren.

23.04.2026 — Diese Anforderung ist veraltet: Ein ComfyUI-Nutzer berichtete, dass der aktuelle Build das Modell ohne separate Konvertierung lädt.

28.04.2026 — SD.Next hat die Unterstützung für Zeta-Chroma veröffentlicht und festgehalten, dass das Modell eine große Anzahl von Schritten für ein akzeptables Ergebnis benötigt.

09.–10.06.2026 — Das Repository erhielt aktualisierte BF16-Gewichte `full_1024_20M_dataset_run`; eine Datei wurde von der Variante mit `dino-distance-1024` in `no-dino-1024` umbenannt.

## Verwendung {#how-to-use-this}

Stand 2026-03-18 sollten Praktiker, die Zeta-Chroma evaluieren, das verlinkte Basis-Safetensors-Artefakt als datierten Kandidaten im Auge behalten und dessen Repository-Metadaten sowie die Diskussion prüfen, bevor sie sich darauf verlassen.

1. Laden Sie den aktuellen Checkpoint aus dem Zeta-Chroma-Repository herunter und legen Sie ihn im Verzeichnis `diffusion_models` der gewählten Installation ab.
  — <https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md>
2. Laden Sie das Modell in einem aktuellen ComfyUI direkt; prüfen Sie bei älteren Builds die Kompatibilität, da die frühe Anleitung eine Konvertierung der Gewichte verlangte.
  — <https://huggingface.co/lodestones/Zeta-Chroma/discussions/9>
3. Beginnen Sie mit 1024 px an der langen Seite, Euler, dem Standard-Scheduler, CFG 4–7 und etwa 20 Schritten; bei schwachem Ergebnis erhöhen Sie die Schrittzahl.
  — <https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md>

## Best Practices {#best-practices}

- Behandeln Sie das Modell als experimentell: Fixieren Sie den Hash des Checkpoints und den Workflow, da die Gewichte im Repository während des Trainings aktualisiert werden.
  — <https://huggingface.co/lodestones/Zeta-Chroma/tree/main>
- Hängen Sie kein VAE an und übertragen Sie keine LoRAs von Z-Image: Für Zeta-Chroma ist dieses Schema nicht kompatibel.
  — <https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md>
- Bei den aktuellen Gewichten sind mehr Schritte einem kurzen Standarddurchlauf vorzuziehen: Frühes Training kann schwache oder halluzinierende Ergebnisse liefern.
  — <https://github.com/vladmandic/sdnext/discussions/4808>

## Hierdurch abgelöst {#superseded-by-this}

- 01.03.2026 — Die separate Konvertierung von `zeta-chroma-base-x0-pixel-dino-distance.safetensors` in das Comfy-Format ist keine aktuelle allgemeine Empfehlung mehr: Am 23.04.2026 wurde über direktes Laden im aktuellen ComfyUI berichtet.
- 09.–10.06.2026 — Der Name `zeta-chroma-base-x0-pixel-dino-distance-1024.safetensors` wurde durch `zeta-chroma-base-x0-pixel-no-dino-1024.safetensors` ersetzt; wählen Sie die Datei nicht allein anhand des alten Namens aus.

## Weiterhin unbekannt {#still-unknown}

- Der Beitrag vom 18.03.2026 ist über X nicht lesbar; sein genauer Wortlaut ist daher nicht bestätigt. Das Datum ist durch die Beitrags-ID belegt, die technische Beschreibung durch andere Quellen.
- Das Repository hat keine stabile Version und keinen unveränderlichen Release-Tag; der aktuelle Branch enthält laufende Gewichtsaktualisierungen.
- Die Meldung über direktes Laden ohne Konvertierung ist ein praktischer Nutzerbericht, keine dokumentierte Zusage von ComfyUI für alle Versionen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/lodestones/Zeta-Chroma/blob/main/zeta-chroma-base-x0-pixel-dino-distance.safetensors | zeta-chroma-base-x0-pixel-dino-distance.safetensors — Zeta-Chroma | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/tree/main | Modell-Repository lodestones/Zeta-Chroma | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/raw/main/README.md | Zeta-Chroma README | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/discussions/9 | Gibt es einen funktionierenden Workflow für dieses Modell? | 2026-09-05 |
| https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md | SwarmUI-Unterstützung für obskure Modelle: Zeta Chroma | 2026-09-05 |
| https://github.com/vladmandic/sdnext/discussions/4808 | SD.Next Release 2026-04-28 | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/commit/53a5aa59f875b3b9ee31ef1a6afb9a480f9c62f1 | full_1024_20M_dataset_run (bf16) | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/commit/eb27e547dcf324b4ecf219ea3fdd9e913422d5cb | Umbenennung von zeta-chroma-base-x0-pixel-dino-distance-1024.safetensors in zeta-chroma-base-x0-pixel-no-dino-1024.safetensors | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:zeta-chroma`, Thread `zeta-chroma-base-model`, 1 datiertes Ereignis vom 2026-03-18 → 2026-03-18.
- **Praxishinweis:** Stand 2026-03-18 sollten Praktiker, die Zeta-Chroma evaluieren, das verlinkte Basis-Safetensors-Artefakt als datierten Kandidaten im Auge behalten und dessen Repository-Metadaten sowie die Diskussion prüfen, bevor sie sich darauf verlassen.
- **Konfidenz:** mittel. Die datierten Abschnitte „Hierdurch abgelöst“ sind maßgeblich dafür, was veraltet ist.

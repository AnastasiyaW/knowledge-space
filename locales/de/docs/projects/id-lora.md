---
title: "ID-LoRA"
category: projects
date: 2026-03-15
tags: [id-lora, id-lora-development, id_lora, project]
aliases: ["ID-LoRA"]
level: 2
source_sha256: af00885906550dfa4fb7afeb3569fb8eb9775b8dcb64303b1c29337ac63e12cd
translation: machine
translated_at: '2026-10-24'
---
# ID-LoRA {#id-lora}

**Entwicklungslinie:** `project:id-lora` · Thread `id-lora-development`  
**Letztes Ereignis:** 2026-03-15 · 1 datiertes Ereignis seit 2026-03-15 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

ID-LoRA ist eine Zero-Shot-Methode zur Identitätskonditionierung für LTX-Audio-Video-Diffusion, entwickelt für Kreative, die sprechende Personen in Videos benötigen, ohne für jeden Sprecher zu trainieren.

- Übertragung der Stimmidentität aus einer Referenz-Audiodatei
- Visuelle Identitätskonditionierung über ein Erstbild
- Einheitliche Steuerung von Szene, gesprochenen Worten, Stimmstil und Umgebungsgeräuschen in einem einzigen Prompt

## Entwicklungslinie {#development-line}

- **2026-03-15 — Öffentliche Projektressourcen von ID-LoRA verlinkt.** Am 2026-03-15 veröffentlichte ID-LoRA Links zu seiner Projektseite, dem Quellcode-Repository und den Modellprofilen. Diese Links verweisen auf primäre Ressourcen, legen jedoch keine konkrete Version, Fähigkeit oder Lizenz fest.

## Was sich geändert hat {#what-changed}

2026-03-15 — ID-LoRA erschien als Forschungsprojekt für die einheitliche, identitätskonditionierte Audio-Video-Generierung auf Basis des LTX-2-Backbones; am 2026-03-15 wurden Links zu Projekt-, Code- und Modellzielen veröffentlicht. Das ursprüngliche arXiv-Paper vom 2026-03-10 stellt Identity-Driven In-Context LoRA, negative RoPE-Zeitpositionen für Referenz-Tokens und Identity Guidance vor. Es berichtet von einer Präferenz von 73 % gegenüber Kling 2.6 Pro hinsichtlich der Stimmähnlichkeit, einem Zugewinn von 24 % bei der sprecherbezogenen Ähnlichkeit über verschiedene Umgebungen hinweg sowie etwa 3.000 Trainingspaaren auf einer GPU.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-03-15: Nutzen Sie die verlinkte Website und das Repository, um ID-LoRA kennenzulernen, prüfen Sie jedoch Version, Lizenz und Verfügbarkeit des Modells, bevor Sie es einsetzen.

1. Klonen Sie das offizielle Repository und installieren Sie die gesperrten Abhängigkeiten mit `uv sync --frozen`; verwenden Sie Python 3.11+ und CUDA 12.x.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
2. Laden Sie die benötigten Basismodell-Komponenten und den ID-LoRA-Checkpoint mit dem Download-Skript des Repositorys herunter.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
3. Stellen Sie ein Erstbild, eine etwa fünfsekündige Referenz-Audiodatei und einen Prompt bereit, der in die Abschnitte `[VISUAL]`, `[SPEECH]` und `[SOUNDS]` gegliedert ist.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
4. Für die aktuelle Verwendung mit LTX-2.3 wechseln Sie den uv-Workspace auf `ID-LoRA-2.3/packages/*` und führen anschließend das zweistufige HQ-Skript mit dem LTX-2.3-Checkpoint aus.
  — <https://github.com/ID-LoRA/ID-LoRA/blob/main/ID-LoRA-2.3/README.md>

## Bewährte Vorgehensweisen {#best-practices}

- Verwenden Sie Referenz-Stimmaufnahmen von etwa fünf Sekunden; kürzere oder längere Clips können die Übertragung der Sprecheridentität verschlechtern.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
- Schreiben Sie das exakt gewünschte Transkript in `[SPEECH]`; Sprechstil und Umgebungsgeräusche gehören in `[SOUNDS]`, nicht in die visuelle Beschreibung.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
- Verwenden Sie auf LTX-2.3 den zweistufigen HQ-Modus für höhere Treue; wählen Sie den einstufigen Modus mit Quantisierung, wenn VRAM oder Durchlaufzeit die Einschränkung darstellen.
  — <https://github.com/ID-LoRA/ID-LoRA/blob/main/ID-LoRA-2.3/README.md>
- Verwenden Sie nur Referenzbilder und Stimmmaterial, für die Sie eine Berechtigung besitzen.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>

## Hiermit überholt {#superseded-by-this}

- 2026-03-24 — Die native, upstream bereitgestellte ComfyUI-Unterstützung für die Übertragung der Identität über Referenz-Audio bei LTX2 ersetzt teilweise den separaten ComfyUI-Custom-Node-Weg für ID-LoRA LTX-2.3; die Originalgewichte müssen nicht konvertiert werden.

## Weiterhin unbekannt {#still-unknown}

- Öffentliche Quellen nennen kein erstpubliziertes Veröffentlichungsdatum für den LTX-2.3-Checkpoint; daher ordnen wir ihm kein datiertes Entwicklungsereignis zu.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://id-lora.github.io/ | ID-LoRA: Identity-Driven Audio-Video Personalization | 2026-09-05 |
| https://github.com/ID-LoRA/ID-LoRA/tree/main | GitHub — ID-LoRA/ID-LoRA | 2026-09-05 |
| https://github.com/ID-LoRA/ID-LoRA/blob/main/ID-LoRA-2.3/README.md | GitHub — ID-LoRA 2.3: LTX-2.3 Support | 2026-09-05 |
| https://huggingface.co/AviadDahan/LTX-2.3-ID-LoRA-CelebVHQ-3K | Hugging Face — LTX-2.3-ID-LoRA-CelebVHQ-3K | 2026-09-05 |
| https://arxiv.org/abs/2603.10256 | ID-LoRA: Identity-Driven Audio-Video Personalization with In-Context LoRA | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:id-lora`, Thread `id-lora-development`, 1 datiertes Ereignis 2026-03-15 → 2026-03-15.
- **Praxishinweis:** Stand 2026-03-15 können Praktiker die verlinkte Website und das Quell-Repository als Einstiegspunkte zu ID-LoRA nutzen und dabei die jeweils gültige Version, Lizenz und Modellverfügbarkeit vor dem Einsatz eigenständig prüfen.
- **Konfidenz:** hoch. Die datierten Überholungseinträge sind maßgeblich dafür, was veraltet ist.

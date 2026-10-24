---
title: "MMDiT: Multimodaler Diffusion Transformer"
description: "MMDiT ist das multimodale Transformer-Muster von Stable Diffusion 3: modalitätsspezifische Repräsentationen nehmen an gemeinsamer Aufmerksamkeit (Joint Attention) teil; Implementierungs-APIs und LoRA-Zielnamen variieren je nach Modellrevision."
category: architectures
tags: [mmdit, transformer, diffusion, attention, architecture, dit, joint-attention, stable-diffusion-3]
aliases: ["Multi-Modal Diffusion Transformer", "MM-DiT"]
level: 3
source_sha256: 74f1dbff8b0ce1e6f17ae1552857415b3920f7b6addadb5edf085de97baabce8
translation: machine
translated_at: '2026-10-24'
---
# MMDiT: Multimodaler Diffusion Transformer {#mmdit-multimodal-diffusion-transformer}

**Geprüft am: 2026-09-04.** MMDiT ist die multimodale Diffusion-Transformer-Architektur, die mit Stable Diffusion 3 eingeführt wurde. Sie repräsentiert Bild- und Spracheingaben mit modalitätsspezifischen Parametern, verbindet ihre Token-Sequenzen für die Aufmerksamkeit und setzt danach die modalitätsspezifische Verarbeitung fort. Diese Grenze der gemeinsamen Aufmerksamkeit erlaubt es, dass Bild- und Textrepräsentationen einander beeinflussen, ohne dass jede Implementierung als dasselbe Modell oder dieselbe API behandelt wird.

## Kernentwurf {#core-design}

Das Stable-Diffusion-3-Paper beschreibt MMDiT als zwei Repräsentationsströme mit getrennten Gewichten, deren Token-Sequenzen an der Aufmerksamkeit zusammentreffen. Das unterscheidet sich von einem Textencoder, der als passive Key/Value-Quelle für einen separaten, rein bildbasierten Transformer dient:

| Aspekt | MMDiT-Grenze |
|---|---|
| Repräsentation | Bild und Text behalten modalitätsspezifische Parameter |
| Aufmerksamkeit | die Ströme können über gemeinsame Aufmerksamkeit Informationen austauschen |
| Entrauschung | der multimodale Transformer sagt über kodierten Bild-Latents voraus |
| Implementierung | Konfiguration, Textencoder, Latent-Format und Blocknamen gehören zu einer bestimmten Modellrevision |

Die Architektur ist für Stable Diffusion 3 relevant. Andere Transformer können Ideen wie duale Ströme oder gemeinsame Aufmerksamkeit teilen, aber ein ähnliches Diagramm oder ein Marketing-Label ist kein Beleg für Kompatibilität von Parametern, Checkpoints oder Adaptern.

## Integration ist modellspezifisch {#integration-is-model-specific}

Für die aktuelle Diffusers-SD3-Pipeline wird die MMDiT-Komponente als `SD3Transformer2DModel` bereitgestellt, zusammen mit VAE, Textencodern, Scheduler und Pipeline-Konfiguration. Diese Klassennamen und Ladesemantiken sind Implementierungsdetails und keine portable Spezifikation.

Bevor Sie ein MMDiT-basiertes Modell anpassen oder betreiben:

1. fixieren Sie Modell-, Pipeline- und Bibliotheksrevision;
2. prüfen Sie die veröffentlichte Konfiguration und die State-Dict-/Modulnamen;
3. verwenden Sie den Adapter bzw. LoRA-Loader, der für genau diesen Transformer vorgesehen ist;
4. erfassen Sie Textencoder, latenten VAE, Scheduler, Präzision und Prompt-Einstellungen als Teil der Run-Identität;
5. validieren Sie Ausgabe und Fehlerverhalten an einem kleinen Testfall, bevor Sie einen größeren Render-Batch starten.

Kopieren Sie keine statische Liste von `to_q`- oder `add_q_proj`-Zielmodulen aus einem nicht verwandten, MMDiT-ähnlichen Modell. Modulnamen, Projektionen, Dual-Stream-Schichten und unterstützte Adapterformate ändern sich zwischen Releases.

## Leistungs- und Bearbeitungsaussagen müssen gemessen werden {#performance-and-editing-claims-need-measurement}

Speicherbedarf und Latenz hängen ab von Anzahl der Bild-Token, Textlänge, Transformer-Konfiguration, Aufmerksamkeitsimplementierung, Präzision und Hardware. Profilieren Sie die genaue Pipeline, statt einen Auflösungs-/VRAM-Wert eines anderen Modells zu übernehmen. Ebenso kann gemeinsame Aufmerksamkeit die Konditionierung verbessern, garantiert aber weder exakte Textdarstellung, Erhalt von Regionen, kompositionelle Korrektheit noch sichere Bearbeitung.

Für einen kontrollierbaren Bearbeitungsworkflow führen Sie getrennte Nachweise für:

- Erhalt des Quellbildes;
- die gewünschte lokale Änderung;
- Genauigkeit von Prompt und Typografie;
- Adapter- bzw. Modellrevision;
- Ausgabeprüfung und zulässige Veröffentlichungsnutzung.

## Referenzen {#references}

- [Stable Diffusion 3 research paper](https://arxiv.org/abs/2403.03206)
- [Stability AI MMDiT architecture overview](https://stability.ai/news-updates/stable-diffusion-3-research-paper)
- [Diffusers SD3 transformer documentation](https://huggingface.co/docs/diffusers/main/en/api/models/sd3_transformer2d)
- [Diffusers Stable Diffusion 3 pipeline documentation](https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/stable_diffusion_3)

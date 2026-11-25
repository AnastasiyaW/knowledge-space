---
title: "WAN 2.2 — WAN"
category: projects
date: 2025-07-28
tags: [project, wan, wan-2-2]
aliases: ["WAN 2.2"]
level: 2
source_sha256: 390a85cc8790999d45e8b971692e9f7079d6e301291c826ed04a3f142134aa12
translation: machine
translated_at: '2026-10-24'
---
# WAN 2.2 — WAN {#wan-22-wan}

**Entwicklungslinie:** `project:wan-2-2` · Thread `wan`  
**Letztes Ereignis:** 2025-07-28 · 2 datierte Einträge seit 2025-07-28 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

WAN 2.2 ist eine Reihe offener Video-Diffusionsmodelle für Entwickler und Kreative: Text-zu-Video, Bild-zu-Video, Text-und-Bild-zu-Video, Sprache-zu-Video und Charakteranimation. Einschränkung: TI2V-5B ist für 720p bei 24 fps angegeben; T2V-A14B benötigt im offiziellen Single-GPU-Beispiel mindestens 80 GB VRAM. Fazit: Für 720p auf begrenzter Hardware ist es praktischer, mit TI2V-5B zu beginnen. A14B sollte für T2V/I2V gewählt werden, wenn deutlich mehr VRAM zur Verfügung steht.

## Entwicklungslinie {#development-line}

- **2025-07-28 — Offizieller WAN-Social-Post erfasst.** T2V-A14B, I2V-A14B und TI2V-5B; am selben Tag erschienen Integrationen in ComfyUI, Diffusers und Space für TI2V-5B. Ergänzung zum Ereignis: A14B ist eine MoE-Serie mit zwei Experten, mit 27B Gesamt- und etwa 14B aktiven Parametern pro Schritt; TI2V-5B vereint T2V und I2V über ein VAE mit 16×16×4-Kompression.
- **2025-07-28 — Referenz zur WAN-Modellsammlung erfasst.** T2V-A14B, I2V-A14B und TI2V-5B; am selben Tag erschienen Integrationen in ComfyUI, Diffusers und Space für TI2V-5B. Ergänzung zum Ereignis: A14B ist eine MoE-Serie mit zwei Experten, mit 27B Gesamt- und etwa 14B aktiven Parametern pro Schritt; TI2V-5B vereint T2V und I2V über ein VAE mit 16×16×4-Kompression.

## Was sich geändert hat {#what-changed}

2025-07-28 — Inferenzcode und Gewichte von WAN 2.2 wurden veröffentlicht: T2V-A14B, I2V-A14B und TI2V-5B; am selben Tag erschienen Integrationen in ComfyUI, Diffusers und Space für TI2V-5B. Ergänzung zum Ereignis: A14B ist eine MoE-Serie mit zwei Experten, mit 27B Gesamt- und etwa 14B aktiven Parametern pro Schritt; TI2V-5B vereint T2V und I2V über ein VAE mit 16×16×4-Kompression. 2025-08-26 — Wan2.2-S2V-14B wurde hinzugefügt: Videogenerierung aus Bild und Audio, mit Gewichten, Code und technischem Bericht. 2025-09-05 — Unterstützung für CosyVoice-Sprachsynthese für Sprache-zu-Video wurde hinzugefügt. 2025-09-19 — Wan2.2-Animate-14B wurde hinzugefügt, für Animation und Charakterersetzung anhand von Bewegung und Mimik. 2025-11-13 — Wan2.2-Animate-14B wurde in Diffusers integriert. Die neuen Schritte erweitern die Familie; sie sind keine Präzisierungen des Ereignisses vom 2025-07-28.

## So verwenden Sie das {#how-to-use-this}

Stand 2025-07-28 sollten Anwender die offizielle Hugging-Face-Modellsammlung von Wan-AI und das verlinkte offizielle WAN-Update konsultieren, wenn sie WAN-2.2-Artefakte suchen. Die verfügbaren datierten Links allein belegen jedoch kein bestimmtes Modell, keine bestimmte Fähigkeit und keine bestimmte Workflow-Änderung.

1. Klonen Sie das offizielle Repository, installieren Sie die Abhängigkeiten bei PyTorch 2.4 oder neuer und laden Sie den benötigten Checkpoint über die Hugging-Face-CLI herunter.
  — <https://github.com/Wan-Video/Wan2.2>
2. Für Text-zu-Video wählen Sie Wan2.2-T2V-A14B; für Bild-zu-Video I2V-A14B; für gemischtes T2V/I2V bei 720p TI2V-5B.
  — <https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B>
3. Starten Sie generate.py mit dem passenden --task, --ckpt_dir, der Größe und dem prompt; für Multi-GPU verwenden Sie den dokumentierten Aufruf über torchrun mit FSDP und Ulysses.
  — <https://github.com/Wan-Video/Wan2.2>

## Best Practices {#best-practices}

- Beginnen Sie mit einem Basislauf ohne Erweiterung des Prompts und ergänzen Sie die Erweiterung nur bei Bedarf; das offizielle Projekt unterstützt DashScope und lokales Qwen.
  — <https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B>
- Bei Speichermangel aktivieren Sie --offload_model True, --convert_model_dtype und bei Bedarf --t5_cpu; dies sind offiziell empfohlene Maßnahmen gegen OOM.
  — <https://github.com/Wan-Video/Wan2.2>
- Für Sprache-zu-Video installieren Sie zusätzlich requirements_s2v.txt und nehmen Sie nicht an, dass die Basisdatei requirements.txt CosyVoice enthält.
  — <https://github.com/Wan-Video/Wan2.2>

## Abgelöst durch dies {#superseded-by-this}

- 2025-07-28 — Wan 2.1 als aktuelle offene Basisreihe von Wan zu betrachten, ist für die Aufgaben T2V, I2V und TI2V veraltet: WAN 2.2 hat sie als nächste veröffentlichte Hauptreihe abgelöst.
- 2025-11-13 — Die bisherige Empfehlung, Wan2.2-Animate-14B nur über eigenen Code zu verwenden, ist für Diffusers-Anwender veraltet: Es gibt jetzt eine offiziell dokumentierte Integration.

## Weiterhin unbekannt {#still-unknown}

- Der Text des X-Posts war bei der Prüfung nicht verfügbar; daher lässt sich ihm zuverlässig keine engere Aussage zuschreiben als Datum und URL des ursprünglichen Ereignisses.
- Die Hugging-Face-Seite mit der Modellliste gibt den aktuellen Stand der Organisation wieder, nennt aber nicht das ursprüngliche Veröffentlichungsdatum jedes Checkpoints.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/Wan-Video/Wan2.2 | Wan-Video/Wan2.2 — offizielles Repository und Nutzungsanleitung | 2026-09-05 |
| https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B | Wan-AI/Wan2.2-T2V-A14B — offizielle Modellkarte | 2026-09-05 |
| https://huggingface.co/Wan-AI/models | Wan-AI — Hugging-Face-Modellsammlung | 2026-09-05 |
| https://x.com/Alibaba_Wan/status/1949332715071037862 | Alibaba-Wan-X-Post zum Ereignis vom 2025-07-28 | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:wan-2-2`, Thread `wan`, 2 datierte Ereignisse 2025-07-28 → 2025-07-28.
- **Praktischer Hinweis:** Stand 2025-07-28 sollten Anwender die offizielle Hugging-Face-Modellsammlung von Wan-AI und das verlinkte offizielle WAN-Update konsultieren, wenn sie WAN-2.2-Artefakte suchen. Die verfügbaren datierten Links allein belegen kein bestimmtes Modell, keine bestimmte Fähigkeit und keine bestimmte Workflow-Änderung.
- **Konfidenz:** mittel. Die datierten Abschnitte „Abgelöst durch dies“ sind maßgeblich dafür, was veraltet ist.

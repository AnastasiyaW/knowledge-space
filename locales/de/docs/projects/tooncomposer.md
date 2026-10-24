---
title: "ToonComposer"
category: projects
date: 2025-08-19
tags: [project, tooncomposer, tooncomposer-public-availability]
aliases: ["ToonComposer"]
level: 2
source_sha256: 76c6a34798916fa6367bb5f5f15d9488e47b2b73b4df3c082fc88a74bc4b8fab
translation: machine
translated_at: '2026-10-24'
---
# ToonComposer {#tooncomposer}

**Entwicklungslinie:** `project:tooncomposer` · Thread `tooncomposer-public-availability`  
**Letztes Ereignis:** 2025-08-19 · 2 datierte seit 2025-08-16 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

ToonComposer ist ein Post-Keyframing-Modell von TencentARC, das auf Wan2.1-I2V-14B-480P aufbaut. Es nimmt ein farbiges Referenzbild, einen Textprompt und eine oder mehrere Skizzen an gewählten Frames entgegen. Daraus erzeugt es eine animierte Cartoon-Sequenz, unterstützt regionsbezogene Bewegungsmasken und bietet Checkpoints für 480p oder 608p. Eine Generierung mit 61 Frames in 480p benötigt etwa 57 GB VRAM. Wir setzen es für kontrollierte kurze Cartoon-Shots ein, wenn spärliche, von Künstlern gezeichnete Bewegungsvorgaben vorliegen. Als leichtgewichtigen allgemeinen Videogenerator verwenden wir es nicht.

## Entwicklungslinie {#development-line}

- **2025-08-16 — Die öffentliche Projektseite und die Quellressourcen von ToonComposer wurden erfasst.** Am 2025-08-16 erhielt ToonComposer eine öffentliche Projektseite und das GitHub-Repository von TencentARC. Diese belegen die öffentliche Projektdarstellung und den Quellcode zu diesem Zeitpunkt der Zeitleiste. Sie belegen keine bestimmte Version, Fähigkeit oder ursprüngliche Veröffentlichungsdaten.
- **2025-08-19 — Ein gehosteter Hugging-Face-Space für ToonComposer wurde erfasst.** Am 2025-08-19 erhielt ToonComposer den Hugging-Face-Space TencentARC/ToonComposer. Dieser ergänzt die öffentliche Projektseite und den Quellcode um eine gehostete öffentliche Oberfläche. Diese Links belegen weder die genauen Funktionen des Space noch die Modellrevision oder neue Fähigkeiten.

## Was sich geändert hat {#what-changed}

- 2025-08-14 — Das Paper stellte ToonComposer, die Injektion spärlicher Skizzen, spatial Low-Rank Adaptation und PKBench vor, noch vor den aufgeführten Veröffentlichungsbeiträgen.
- 2025-08-16 — TencentARC veröffentlichte Projekt und Code und etablierte damit einen einheitlichen Post-Keyframing-Workflow anstelle einer getrennten Kette aus Inbetweening und Kolorierung.
- 2025-08-19 — Der offizielle Hugging-Face-Space stellte den Workflow zusammen mit dem veröffentlichten Modell als gehostete Demo bereit.
- 2026-03-24 — Der Projektautor berichtete, dass die offizielle Hugging-Face-Demo nach einem vorübergehenden Ausfall des Space neu gestartet wurde.

## Anwendung {#how-to-use-this}

Stand 2025-08-19 suchen wir ToonComposer über die öffentliche Projektseite, das Quell-Repository und den gehosteten Hugging-Face-Space. Die genaue Fähigkeit und Revision überprüfen wir direkt, da diese Entwicklungslinie bisher nicht recherchiert wurde.

1. Klone das offizielle Repository, lege eine Conda-Umgebung mit Python 3.10 an und installiere die fixierten Abhängigkeiten.
  — <https://github.com/TencentARC/ToonComposer>
2. Führe `python app.py` aus. Zuerst werden zwischengespeicherte Gewichte verwendet; andernfalls werden das Wan2.1-Basismodell und der ToonComposer-Checkpoint nachgeladen.
  — <https://github.com/TencentARC/ToonComposer>
3. Lege in der Gradio-Oberfläche Prompt, Anzahl der Ausgabe-Frames und Auflösung fest; stelle ein farbiges Keyframe und spärliche Skizzen an den Frames bereit, die du steuern möchtest.
  — <https://github.com/TencentARC/ToonComposer>
4. Nutze den offiziellen gehosteten Space, wenn der lokale GPU-Speicher nicht ausreicht.
  — <https://huggingface.co/spaces/TencentARC/ToonComposer>

## Best Practices {#best-practices}

- Beginne mit einem farbigen Referenzbild und einer Skizze und füge weitere Skizzen nur dort hinzu, wo zusätzliche Bewegungssteuerung nötig ist.
  — <https://arxiv.org/abs/2508.10881>
- Verwende die Skizzenmaske für Regionen, in denen kontextgesteuerte Bewegung gewünscht ist, und markiere diese Regionen nicht als unmarkiert.
  — <https://github.com/TencentARC/ToonComposer>
- Bei Variationen der Ausgabe oder Fehlern passe Seed, Sampling-Schritte, CFG-Skala, die Skalierung des positionsbewussten Residuums sowie die Skizzen- oder Masken-Eingaben an.
  — <https://github.com/TencentARC/ToonComposer>
- Betrachte den offiziellen Space als Ausweichlösung für die dokumentierte lokale Arbeitslast mit 57 GB VRAM in 480p mit 61 Frames; setze nicht voraus, dass ein Deployment bei einem Inference-Provider existiert.
  — <https://huggingface.co/TencentARC/ToonComposer>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2026-03-24 — Die Angabe, die offizielle Hugging-Face-Demo sei nicht verfügbar, ist veraltet: Der Projektautor berichtete, dass sie nach einem Neustart wieder funktionierte.

## Weiterhin unbekannt {#still-unknown}

- Die angeforderten Felder event_findings und new_events waren im Schema nicht vorgesehen; ihre Belege sind unter what_changed erhalten.
- Es wurde kein datierter erstrangiger Changelog und keine Release-Historie gefunden, die Modelländerungen nach dem Release im August 2025 dokumentiert; der Neustart der Demo im März 2026 ist eine Änderung der Verfügbarkeit und kein Beleg für eine neue Modellversion.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/TencentARC/ToonComposer | GitHub — TencentARC/ToonComposer | 2026-09-05 |
| https://huggingface.co/spaces/TencentARC/ToonComposer | Hugging-Face-Space — TencentARC/ToonComposer | 2026-09-05 |
| https://huggingface.co/TencentARC/ToonComposer | Hugging-Face-Modellkarte — TencentARC/ToonComposer | 2026-09-05 |
| https://arxiv.org/abs/2508.10881 | ToonComposer: Streamlining Cartoon Production with Generative Post-Keyframing | 2026-09-05 |
| https://huggingface.co/TencentARC/ToonComposer/discussions/2 | ToonComposer-Diskussion: Verfügbarkeit? | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:tooncomposer`, Thread `tooncomposer-public-availability`, 2 datierte Ereignisse vom 2025-08-16 bis 2025-08-19.
- **Praktischer Hinweis:** Stand 2025-08-19 sollten Praktiker ToonComposer über die öffentliche Projektseite, das Quell-Repository und den gehosteten Hugging-Face-Space suchen. Die genaue Fähigkeit und Revision sollten sie direkt überprüfen, da diese Entwicklungslinie bisher nicht recherchiert wurde.
- **Konfidenz:** mittel. Die datierten Ersetzungen sind maßgeblich dafür, was veraltet ist.

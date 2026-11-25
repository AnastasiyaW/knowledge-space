---
title: "OmniAvatar — Öffentliche Veröffentlichung und Verfügbarkeit der Demo"
category: projects
date: 2025-08-05
tags: [omniavatar, project, public-release-and-demo]
aliases: ["OmniAvatar"]
level: 2
source_sha256: d44698bbbdc966603d4d735b2a645655759ff7a53cf07f17151f2f40eb75fc17
translation: machine
translated_at: '2026-10-24'
---
# OmniAvatar — Öffentliche Veröffentlichung und Verfügbarkeit der Demo {#omniavatar-public-release-and-demo-availability}

**Entwicklungslinie:** `project:omniavatar` · Thread `public-release-and-demo`  
**Letztes Ereignis:** 2025-08-05 · 2 datierte seit 2025-07-04 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

OmniAvatar ist ein offenes Forschungssystem zur Erzeugung sprechender Avatar-Videos aus einem Bild, Audio und einem Textprompt.

- Lippensynchronisation zur Sprachaufnahme.
- Gesichtsausdrücke und Körperbewegungen, abgestimmt auf das Audio.
- Textsteuerung von Figurenhandlung, Hintergrund und Emotion.

Die Modelle sind LoRA- und Audio-Condition-Checkpoints auf Basis von Wan2.1 T2V in den Varianten 14B und 1.3B. Die Ausgabeauflösung ist auf 480p begrenzt. Für lokale Experimente handelt es sich um einen funktionierenden Wan2.1-Stack. Der öffentliche Space stammt von Dritten, weshalb wir ihn nicht als einzigen Startweg voraussetzen.

## Entwicklungslinie {#development-line}

- **2025-07-04 — Öffentliches OmniAvatar-Projekt und Quellcode-Repository wurden verlinkt.** Das offizielle Repository datiert die Veröffentlichung dieser Gewichte auf 2025-07-02.
- **2025-08-05 — Der Hugging-Face-Space von OmniAvatar wurde verlinkt.** Am 2025-08-05 erschien ein Hugging-Face-Space namens OmniAvatar, der auf die frühere Ankündigung des Projekts im Juli verwies. Damit entsteht eine gehostete Demo-Oberfläche, doch die Links allein belegen weder deren genaue Funktionalität und Verfügbarkeit noch die Beziehung zu einer bestimmten Repository-Revision.

## Was sich geändert hat {#what-changed}

2025-07-04 — Das öffentliche Projekt umfasste Code, Gewichte und die 1.3B-Variante für Wan2.1. Das offizielle Repository datiert die Veröffentlichung dieser Gewichte auf 2025-07-02. 2025-08-05 — Der Drittanbieter-Hugging-Face-Space alexnasa/OmniAvatar erschien. Am 2025-08-06 bestätigte das Autorenteam von OmniAvatar öffentlich, dass die Demo erfolgreich war, sie wurde jedoch nicht zu einer offiziellen Inferenz-API. 2025-06-23 — Das OmniAvatar-Paper wurde veröffentlicht (arXiv:2506.18866). 2025-06-24 — Die Autoren veröffentlichten den Inferenzcode und die ersten Gewichte.

## Anwendung {#how-to-use-this}

Stand 2025-08-05 konnten Praktiker OmniAvatar über das öffentliche Repository und den verlinkten Hugging-Face-Space finden. Vor dem Einsatz beider sollten sie die aktuelle Repository-Revision, das Verhalten des Space und die Nutzungsanleitung prüfen.

1. Das Repository klonen und die gepinnten Abhängigkeiten installieren: PyTorch 2.4.0 mit CUDA 12.4 sowie requirements.txt.
  — <https://github.com/Omni-Avatar/OmniAvatar>
2. Kompatibles Wan2.1 T2V, den offiziellen OmniAvatar-LoRA/Audio-Condition-Checkpoint und wav2vec2-base-960h in die Struktur pretrained_models herunterladen.
  — <https://huggingface.co/OmniAvatar/OmniAvatar-14B>
3. Den Eingabestring im Format [prompt]@@[img_path]@@[audio_path] vorbereiten und scripts/inference.py mit der Konfiguration 14B oder 1.3B ausführen.
  — <https://github.com/Omni-Avatar/OmniAvatar>
4. Den Space für eine kurze Vorabprüfung öffnen, dabei aber mit zeitweiser Verfügbarkeit rechnen und kritische Ergebnisse lokal reproduzieren.
  — <https://huggingface.co/spaces/alexnasa/OmniAvatar>

## Best Practices {#best-practices}

- Mit 480p beginnen und Prompt- und Audio-CFG im Bereich 4–6 wählen; die Audio-CFG erhöhen, wenn die Lippensynchronisation nicht stabil genug ist.
  — <https://github.com/Omni-Avatar/OmniAvatar>
- Den Prompt aus der Beschreibung des ersten Frames, dem Verhalten der Person und bei Bedarf dem Hintergrund zusammensetzen.
  — <https://github.com/Omni-Avatar/OmniAvatar>
- Den VRAM-Bedarf für 14B frühzeitig planen: Die Autoren geben 36 GB ohne Speicherverwaltung, 21 GB mit 7B persistenten Parametern und 8 GB mit null persistenten Parametern auf einer einzelnen GPU an.
  — <https://github.com/Omni-Avatar/OmniAvatar>
- Den Space nicht als Produktions-Endpunkt verwenden: Nutzerdiskussionen berichten von leeren Bildschirmen und Problemen beim lokalen Klonen. Wenn Reproduzierbarkeit erforderlich ist, offiziellen Code ausführen.
  — <https://huggingface.co/spaces/alexnasa/OmniAvatar/discussions/1>

## Hierdurch ersetzt {#superseded-by-this}

- 2025-06-24 — Der Status „nur Paper oder nur Beispiele“ ist überholt: Die Autoren haben Inferenzcode und Gewichte veröffentlicht.
- 2025-07-02 — Der Status „nur 14B“ ist überholt: Die Autoren haben OmniAvatar-Gewichte für Wan2.1 T2V-1.3B veröffentlicht.

## Weiterhin unbekannt {#still-unknown}

- Das Antwortschema enthält keine Felder event_findings und new_events; ihre bestätigten Fakten stehen im Abschnitt what_changed statt in separaten strukturierten Objekten.
- Service-Level-Agreement des Space und stabile interaktive Verfügbarkeit sind nicht bestätigt: Die Seite zeigt Running on Zero, und spätere Nutzermeldungen berichten von einem leeren Bildschirm.
- Das offizielle Repository legt keine Produktions-API, kommerziellen Support oder eine vollständige Liste verifizierter GPU-Konfigurationen fest.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://omni-avatar.github.io/ | OmniAvatar: Efficient Audio-Driven Avatar Video Generation with Adaptive Body Animation | 2026-09-05 |
| https://github.com/Omni-Avatar/OmniAvatar | Omni-Avatar/OmniAvatar | 2026-09-05 |
| https://huggingface.co/OmniAvatar/OmniAvatar-14B | OmniAvatar/OmniAvatar-14B | 2026-09-05 |
| https://huggingface.co/spaces/alexnasa/OmniAvatar | alexnasa/OmniAvatar | 2026-09-05 |
| https://huggingface.co/spaces/alexnasa/OmniAvatar/discussions/1 | alexnasa/OmniAvatar-Diskussion: Funktioniert es? | 2026-09-05 |
| https://huggingface.co/spaces/alexnasa/OmniAvatar/discussions/2 | alexnasa/OmniAvatar-Diskussion: Es funktioniert. Sehr gute Demo-Space. | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:omniavatar`, Thread `public-release-and-demo`, 2 datierte Ereignisse vom 2025-07-04 bis 2025-08-05.
- **Praktischer Hinweis:** Stand 2025-08-05 konnten Praktiker OmniAvatar über das öffentliche Repository und den verlinkten Hugging-Face-Space finden. Vor dem Einsatz beider sollten sie die aktuelle Repository-Revision, das Verhalten des Space und die Nutzungsanleitung prüfen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was überholt ist.

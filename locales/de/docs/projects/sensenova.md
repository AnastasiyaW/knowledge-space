---
title: "SenseNova — U1 MoT-Modell und Infografik-Artefakte"
category: projects
date: 2026-08-01
tags: [project, sensenova, u1-mot-model-and-infographic]
aliases: ["SenseNova"]
level: 3
source_sha256: 34844dcc2b5bc41e4640f26d59e514aee4f4e3bcb41f3917925c275d8be06844
translation: machine
translated_at: '2026-10-24'
---
# SenseNova — U1 MoT-Modell und Infografik-Artefakte {#sensenova-u1-mot-model-and-infographic-artifacts}

**Entwicklungslinie:** `project:sensenova` · Thread `u1-mot-model-and-infographic`  
**Letztes Ereignis:** 2026-08-01 · 1 datiertes Ereignis seit 2026-08-01 · **Recherchiert:** 2026-09-06 · Konfidenz: hoch

## Was es ist {#what-it-is}

SenseNova U1 ist eine Modellfamilie von OpenSenseNova unter Apache-2.0 für Praktiker, die visuelle Erstellung lokal betreiben.

Fähigkeiten:
- Text-zu-Bild.
- Bildbearbeitung.
- Verschachtelte Bild-Text-Generierung.
- Visuelles Verständnis.

Die aktuelle Modellkarte von U1.5-8B-MoT nennt 18B Parameter in BF16 und keinen Hugging Face Inference Provider. Verwende U1.5 für allgemeine Erstellung und Bearbeitung und Infographic-V3 nur für infografikspezifische Arbeiten.

## Entwicklungslinie {#development-line}

- **2026-08-01 — SenseNova hat Artefakte der U1-MoT-Vorschau und Infografik auf Hugging Face verlinkt.** Am 2026-08-01 ergänzte SenseNova Links zu Hugging-Face-Seiten und Spaces für SenseNova-U1.5-8B-MoT-Preview und SenseNova-U1-8B-MoT-Infographic-V3. Diese Links markieren einen Meilenstein bei Modell und Demo. Sie belegen weder den Veröffentlichungsstatus, technische Änderungen noch Fähigkeiten der Artefakte.

## Was sich geändert hat {#what-changed}

- 2026-07-16 — SenseNova-U1-8B-MoT-Infographic-V3 ergänzte integrierte Infografik-Erstellung und -Bearbeitung: lokale Text-/Inhaltsbearbeitung sowie globale Stil- und Layoutänderungen.
- 2026-08-01 — SenseNova-U1.5-8B-MoT-Preview war eine Vorschau vom 31. Juli für breitere Erstellung und Bearbeitung; sie wurde zusammen mit der früheren V3-Karte verlinkt, nicht gemeinsam mit ihr veröffentlicht.
- 2026-08-04 — Ein von der Community gepflegtes Q8-GGUF mit 19,9 GB machte die Vorschau leichter lauffähig, änderte aber die offiziellen Gewichte nicht.
- 2026-08-20 — SenseNova-U1.5-8B-MoT wurde die aktuelle offizielle Veröffentlichung; das passende 8-Schritt-LoRA ergänzte einen schnelleren Pfad.
- 2026-09-01 — Für den finalen U1.5-Checkpoint erschien ein Community-Q8-GGUF mit 21,2 GB.

## Verwendung {#how-to-use-this}

1. Für eine Auswertung ohne Installation öffne den verlinkten SenseNova-Studio-Playground auf der aktuellen U1.5-Karte; betrachte ihn als Workflow-Test und nicht als Nachweis für Produktionsleistung.
  — <https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT>
2. Für die lokale Nutzung klone OpenSenseNova/SenseNova-U1, führe `uv sync` in dessen Umgebung aus und verwende den Modellpfad U1.5-8B-MoT mit dem Einstiegspunkt für Text-zu-Bild oder Bildbearbeitung.
  — <https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT>
3. Wähle eine trainierte Auflösungsklasse und konfiguriere `device_map` oder den VRAM-Modus des Projekts, bevor du Auflösung oder Batchgröße erhöhst.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/examples/README.md>
4. Für die Erstellung oder Bearbeitung von Infografiken wähle SenseNova-U1-8B-MoT-Infographic-V3, statt anzunehmen, dass der allgemeine U1.5-Checkpoint dieselbe Aufgabenspezialisierung besitzt; der Space sensenova ist eine interaktive V3-Route.
  — <https://huggingface.co/spaces/sensenova/sensenova-u1-infographic-v3>

## Bewährte Vorgehensweisen {#best-practices}

- Verwende einen direkten Prompt für eine klare Aufgabe mit wenigen Vorgaben. Nutze Image PE für komplexe Komposition, Texte, Anzahlen, Layout oder Referenzplanung und variiere Seeds, wenn Vielfalt wichtig ist.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/u1.5_best_practices.md>
- Benenne bei einer komplexen Bearbeitung die gewünschte Änderung und alles, was unverändert bleiben muss. Ordne mehrere Referenzbilder bewusst an und beschreibe die Rolle jedes Bildes.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/u1.5_best_practices.md>
- Bevorzuge die dokumentierten Auflösungsklassen von etwa 2K. Beliebige Kombinationen aus Breite und Höhe können die Qualität verringern.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/examples/README.md>
- Prüfe dichten Text, exakte Anzahl und Layout, Anatomie sowie umfangreiche Bearbeitungen mit mehreren Referenzen manuell. Senke `cfg_scale`, wenn Detail oder Farbe übermäßig betont werden.
  — <https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-08-20 — Die Behandlung von SenseNova-U1.5-8B-MoT-Preview als aktueller allgemeiner U1.5-Checkpoint ist veraltet.

## Weiterhin unbekannt {#still-unknown}

- SenseNova ist eine breitere Marke von SenseTime; das verifizierte Material identifiziert die U1-Familie von OpenSenseNova, belegt jedoch nicht, dass U1.5 dasselbe Produkt wie das kommerzielle SenseNova 6.x oder U1 Pro ist.
- Die Preview-Demo gehört zu hugging-apps und nicht zu sensenova; ihre zugängliche Seite belegt nicht, welchen Checkpoint sie derzeit ausführt, wie hoch ihre Verfügbarkeit ist oder ob ein Produktionsservice zugesichert wird.
- Die Quellen behaupten native 4K-Unterstützung, die geprüften Beispiele dokumentieren jedoch etwa 2K-Auflösungsklassen für das Training und kein unabhängiges Qualitätsergebnis für 3840x2160 in einem festgelegten Produktionsszenario.
- Für den finalen U1.5-Checkpoint wurden keine aktuellen Preise der gehosteten API, kein SLA und kein Hugging Face Inference Provider verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT-Preview | sensenova/SenseNova-U1.5-8B-MoT-Preview | 2026-09-06 |
| https://huggingface.co/spaces/hugging-apps/sensenova-sensenova-u1-5-8b-mot-preview | SenseNova-U1.5-8B-MoT (Preview) - a Hugging Face Space by hugging-apps | 2026-09-06 |
| https://huggingface.co/sensenova/SenseNova-U1-8B-MoT-Infographic-V3 | sensenova/SenseNova-U1-8B-MoT-Infographic-V3 | 2026-09-06 |
| https://huggingface.co/spaces/sensenova/sensenova-u1-infographic-v3 | SenseNova U1 Infographic V3 - a Hugging Face Space by sensenova | 2026-09-06 |
| https://github.com/OpenSenseNova/SenseNova-U1 | OpenSenseNova/SenseNova-U1: SenseNova-U series with NEO-unify | 2026-09-06 |
| https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT | sensenova/SenseNova-U1.5-8B-MoT | 2026-09-06 |
| https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/u1.5_best_practices.md | SenseNova-U1.5 Cookbook | 2026-09-06 |
| https://github.com/OpenSenseNova/SenseNova-U1/blob/main/examples/README.md | SenseNova-U1 reference inference examples | 2026-09-06 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:sensenova`, Thread `u1-mot-model-and-infographic`, 1 datiertes Ereignis 2026-08-01 → 2026-08-01.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Verwendung und Vorgehensweisen oben, einschließlich ihrer Grenzen.
- **Konfidenz:** hoch. Datierte Ersetzungen oben sind maßgeblich für das, was veraltet ist.

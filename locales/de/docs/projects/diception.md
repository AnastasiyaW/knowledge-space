---
title: "DICEPTION"
category: projects
date: 2025-10-02
tags: [diception, diception-development, project]
aliases: ["DICEPTION"]
level: 3
source_sha256: 43b39dda46990491999158dc1ef1b0f854c88a862f1e66186592a09480903152
translation: machine
translated_at: '2026-10-24'
---
# DICEPTION {#diception}

**Entwicklungslinie:** `project:diception` · Thread `diception-development`  
**Letztes Ereignis:** 2025-10-02 · 2 datierte Einträge seit 2025-04-21 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

DICEPTION ist ein auf SD3 basierendes Diffusionsmodell für Praktiker, die ein einziges lokales Modell für Ausgaben der visuellen Wahrnehmung wollen.

- Monokulare Tiefe und Oberflächennormalen.
- Posenschätzung.
- Entitäts-, semantische und punktgesteuerte Segmentierung.

## Entwicklungslinie {#development-line}

- **2025-04-21 — Ressourcen des DICEPTION-Projekts wurden öffentlich verlinkt.** Am 2025-04-21 erschienen Links zur Projektwebsite, zum GitHub-Repository und zu einer Hugging-Face-Spaces-Demo. Sie etablierten einen datierten öffentlichen Einstiegspunkt für das Projekt, seinen Quellcode und eine interaktive Demonstration.
- **2025-10-02 — Hugging-Face-Repository von DICEPTION wurde hinzugefügt.** Am 2025-10-02 wurde neben dem früheren Projektbeitrag das Hugging-Face-Repository von DICEPTION verlinkt. Damit kam ein eigenständiger Zugangspunkt zum Modell-Repository zum datierten öffentlichen Verlauf hinzu, ohne dass erkennbar wäre, welche Dateien sich geändert haben oder ob es sich um eine erste Veröffentlichung handelt.

## Was sich geändert hat {#what-changed}

Entwicklung von DICEPTION:

- 2025-02-24/25 — arXiv v1/v2 begründeten die diffusionsbasierte Methode für generalistische Wahrnehmung.
- 2025-04-21 — öffentliche Einstiegspunkte waren die Projektseite, das Repository und die Web-Demo. Nutzbarer Inferenzcode und Gewichte folgten erst im September, sodass eine lokale Installation noch nicht funktionierte.
- 2025-09-19 — als NeurIPS-2025-Spotlight angenommen.
- 2025-09-21 — Maintainer veröffentlichten Inferenzcode und das Modell v1.
- 2025-10-02 — Dateien ergänzten den Hugging-Face-Modellbaum mit dem Checkpoint DICEPTION_v1.pth.
- 2026-09-04 — die gehostete Demo meldet RUNTIME_ERROR, daher ist lokaler Code plus Gewichte der nutzbare Weg.

## Anwendung {#how-to-use-this}

Ab 2025-10-02 sollten die Projektseite von DICEPTION, das Repository, die Demo und das Hugging-Face-Repository bei der Bewertung des Projekts gemeinsam herangezogen werden.

1. Klonen Sie das Repository, erstellen Sie dessen Python-3.10-Conda-Umgebung und installieren Sie die Requirements.
  — <https://github.com/aim-uofa/Diception>
2. Laden Sie Stable Diffusion 3 Medium im Diffusers-Format und DICEPTION_v1.pth herunter und setzen Sie --pretrained_model_path und --diception_path auf diese lokalen Verzeichnisse.
  — <https://huggingface.co/Canyu/DICEPTION/tree/main>
3. Führen Sie inference.py mit einem Eingabebild und einem exakten Task-Token aus, etwa `[[image2depth]]`, `[[image2normal]]`, `[[image2pose]]`, `[[image2entity]]` oder `[[image2segmentation]]`.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
4. Für semantische Segmentierung hängen Sie die COCO-Kategorie an `[[image2semantic]]` an; für interaktive Segmentierung übergeben Sie normalisierte y,x-Punkte, höchstens fünf Punkte.
  — <https://github.com/aim-uofa/Diception>
5. Für Datensätze verwenden Sie batch_inference.py mit der mitgelieferten JSON-Struktur; verwenden Sie --save_npy, wenn Tiefen- oder Normalenwerte benötigt werden und nicht nur eine Visualisierung.
  — <https://github.com/aim-uofa/Diception>

## Bewährte Vorgehensweisen {#best-practices}

- Stellen Sie vor dem Ausführen des veröffentlichten Skripts eine CUDA-fähige bfloat16-Umgebung bereit: Es verschiebt das Modell explizit nach CUDA/bfloat16 und lädt den Checkpoint auf CUDA.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
- Beginnen Sie für allgemeine Qualität mit den von den Maintainern vorgesehenen 28 Inferenzschritten und einem Guidance Scale von 2.0; verwenden Sie 1 Schritt und Guidance 1.0 nur, wenn Geschwindigkeit wichtig ist, insbesondere für Tiefe oder Normalen.
  — <https://github.com/aim-uofa/Diception>
- Validieren Sie im nativen Auswertungsformat der jeweiligen Aufgabe: Single-Image-Inferenz arbeitet immer mit 768×768 und speichert ein Nebeneinander-Bild aus Eingabe und Ausgabe, nicht eine unveränderte Vorhersage in nativer Auflösung.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
- Laden Sie die v1-.pth-Datei nur aus dem benannten Modell-Repository herunter und behandeln Sie sie als PyTorch-Pickle-Artefakt; der Hub markiert Pickle-Importe, und der Code verwendet torch.load.
  — <https://huggingface.co/Canyu/DICEPTION/tree/main>
- Machen Sie den gehosteten Space nicht zur Abhängigkeit eines Workflows, solange er nicht repariert ist; verwenden Sie stattdessen den veröffentlichten lokalen Code und die Gewichte.
  — <https://huggingface.co/spaces/Canyu/Diception-Demo>
- Für kommerzielle Nutzung folgen Sie der Anweisung des Projekts, den angegebenen Maintainer zu kontaktieren, statt anzunehmen, dass der Hinweis zur akademischen Nutzung den Einsatz abdeckt.
  — <https://github.com/aim-uofa/Diception>

## Abgelöst durch {#superseded-by-this}

- Zugriff für Forschung/Demo allein seit 2025-04-21: abgelöst am 2025-09-21 durch den veröffentlichten lokalen Inferenzcode und die Gewichte von v1.
- Demo-first-Zugriff seit 2025-04-21: seit 2026-09-04 als aktueller Workflow überholt, da der gehostete Hugging-Face-Space RUNTIME_ERROR meldet.

## Weiterhin unbekannt {#still-unknown}

- Für die Einträge vom 2025-04-21 und 2025-10-02 liegt kein Originaltext des Beitrags vor, daher lässt sich ihr Wortlaut nur aus den datierten Links rekonstruieren.
- Wir fanden sekundäre übersetzte Zusammenfassungen, aber keine Dokumentation der Erstanbieter auf Chinesisch und keinen unabhängigen chinesischsprachigen Ausführungsbericht; keines davon wurde als praktischer Beleg verwendet.
- Wir fanden keinen aktuellen lokalen End-to-End-Lauf, keine VRAM-Messung und keine Matrix unterstützter Hardware. CUDA-/bfloat16-Code ist Implementierungsbeleg, kein bestandener Laufzeitnachweis.
- Das aktuelle README führt Training und Few-Shot-Feinabstimmung noch als geplant auf; das im Paper beschriebene Ergebnis mit 50 Bildern und 1 % Parameteranpassung ist daher kein lauffähiger öffentlicher Workflow.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://aim-uofa.github.io/Diception/ | DICEPTION project page | 2026-09-04 |
| https://github.com/aim-uofa/Diception | aim-uofa/Diception README and release notes | 2026-09-04 |
| https://github.com/aim-uofa/Diception/blob/main/inference.py | DICEPTION single-image inference script | 2026-09-04 |
| https://github.com/aim-uofa/Diception/blob/main/models/Renderer.py | DICEPTION renderer and diffusion execution path | 2026-09-04 |
| https://huggingface.co/Canyu/DICEPTION/tree/main | Canyu/DICEPTION model files | 2026-09-04 |
| https://huggingface.co/spaces/Canyu/Diception-Demo | Diception Demo | 2026-09-04 |
| https://arxiv.org/abs/2502.17157 | DICEPTION: A Generalist Diffusion Model for Visual Perceptual Tasks | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:diception`, Thread `diception-development`, 2 datierte Ereignisse vom 2025-04-21 bis 2025-10-02.
- **Praktischer Hinweis:** Ab 2025-10-02 sollten Praktiker bei der Bewertung des Projekts oder beim Auffinden seiner öffentlichen Artefakte die Projektseite von DICEPTION, das Quell-Repository, die Demo und das verlinkte Hugging-Face-Repository gemeinsam heranziehen.
- **Konfidenz:** mittel. Die datierten Abschnitte „Abgelöst durch“ sind maßgeblich dafür, was veraltet ist.

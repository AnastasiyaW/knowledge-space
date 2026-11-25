---
title: "Capybara"
category: projects
date: 2026-02-24
tags: [capybara, capybara-development, project]
aliases: ["CAPYBARA", "Capybara"]
level: 4
source_sha256: 9f63befab217238f6ea0b0323ec6fd4b508c2223b5ec34121c22c9f37b67fd05
translation: machine
translated_at: '2026-10-24'
---
# Capybara {#capybara}

**Entwicklungslinie:** `project:capybara` · Thread `capybara-development`  
**Letztes Ereignis:** 2026-02-24 · 2 datierte seit 2026-02-17 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Capybara ist eine Open-Source-Inferenz-Pipeline für Anwender, die Generierung und anweisungsbasierte Bearbeitung in einer einzigen Oberfläche benötigen.

- Text-zu-Bild (T2I) und Text-zu-Video (T2V) Generierung.
- Anweisungsbasierte Bild-zu-Bild- (TI2I) und Video-zu-Video-Bearbeitung (TV2V).
- Einzelläufe, CSV-Batches, verteilte Inferenz über Accelerate sowie ComfyUI-Nodes.

Die Dokumentation empfiehlt Python 3.11 und CUDA 12.6. FP8 erfordert NVIDIA Ada/Hopper mit einer Compute Capability von mindestens 8.9 sowie torchao. Es handelt sich um eine brauchbare Integration für lokale Inferenz, nicht jedoch um eine dokumentierte Produktions- oder Trainingsplattform.

## Entwicklungslinie {#development-line}

- **2026-02-17 — Quellcode-, Modell- und Demo-Ressourcen zu Capybara wurden verlinkt.** Am 2026-02-17 verknüpfte der datierte Ressourcensatz das Quell-Repository und die Modellseite von Capybara miteinander, zusammen mit einem Qwen3-VL-Modell und einem gehosteten Endpunkt. Dies markiert einen frühen öffentlichen Entwicklungsschritt für Capybara, wobei die Links allein jedoch weder die genaue Leistungsfähigkeit, den Veröffentlichungsstatus noch ihre Beziehung zueinander belegen.
- **2026-02-24 — Die Capybara-Dokumentation machte ComfyUI- und FP8-Workflows sichtbar.** Die Dokumentation beschrieb ComfyUI-Custom-Nodes, FP8 und einen Beispiel-Workflow. Das offizielle README datiert diese Ergänzungen für Code-Änderungen auf 2026-02-20, während 2026-02-24 das erfasste Ereignisdatum ist.

## Was sich geändert hat {#what-changed}

Capybara — am 2026-02-17 erschien das Inferenz-Framework v0.1 mit T2I, T2V, TI2I und TV2V. Am 2026-02-24 erfasste die Dokumentation ComfyUI-Custom-Nodes, FP8 und einen Beispiel-Workflow. Das offizielle README datiert diese Funktionen für Code-Änderungen auf 2026-02-20, weshalb 2026-02-24 das erfasste Ereignisdatum ist. Stand 2026-09-04 enthält das aktuelle erstanbieterseitige README weiterhin nur diese beiden datierten Zeilen, markiert ComfyUI als erledigt und führt die Veröffentlichung des einheitlichen Erstellungsmodells sowie des Trainingscodes weiterhin als TODO.

## Anwendung {#how-to-use-this}

Nach dem 2026-02-24 sollte Capybara anhand seiner ComfyUI-Dokumentation, des Beispiel-Workflows und der FP8-Hinweise bewertet werden, nicht allein anhand des Basis-Repositorys oder der Modellseite.

1. Lege eine isolierte Python-3.11-Umgebung an, installiere PyTorch für CUDA 12.6 und installiere die Projektabhängigkeiten.
  — <https://github.com/xgen-universe/Capybara>
2. Lade alle erforderlichen Checkpoint-Komponenten in `ckpts/` herunter. Qwen3-VL-8B-Instruct wird nur benötigt, wenn die Umschreibung von Anweisungen aktiviert ist.
  — <https://github.com/xgen-universe/Capybara>
3. Für einen ersten Lauf rufe `inference.py` mit `task_type` `t2i` oder `t2v` auf. Für `ti2i` und `tv2v` übergib `media_path` und eine Textanweisung.
  — <https://github.com/xgen-universe/Capybara>
4. Für Batch-Jobs bereite eine CSV mit `img_path` oder `video_path` sowie `instruction` vor und übergib anschließend `csv_path` und `data_root_path`.
  — <https://github.com/xgen-universe/Capybara>
5. Für ComfyUI verlinke wurzel des Capybara-Verzeichnisses in `custom_nodes` und starte ComfyUI in derselben `capybara`-Umgebung.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
6. Lade `sample_workflow.json` in die ComfyUI-Arbeitsfläche und passe anschließend `task_type` sowie den Eingang `reference` für T2I, T2V, TI2I oder TV2V an.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/examples/sample_workflow.json>

## Bewährte Vorgehensweisen {#best-practices}

- Beginne mit dem offiziellen Basismodus: 480p und 50 Schritte für Video, 720p und 50 Schritte für Bilder. Erhöhe die Auflösung erst, nachdem eine funktionierende Basislinie etabliert ist.
  — <https://github.com/xgen-universe/Capybara>
- Stelle in ComfyUI für TI2I und TV2V das Einzelbild bzw. das Video über `reference` bereit. Der Node leitet das Seitenverhältnis aus `reference` ab und setzt `guidance_scale` fest auf 1.0.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Aktiviere FP8 nur auf Ada/Hopper mit `torchao`. Dies halbiert den Speicherbedarf der Transformer-Gewichte annähernd, verspricht aber keinen Geschwindigkeitsgewinn und hält den Transformer im GPU-Speicher fest.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Vermische keine Python-Umgebungen zwischen Capybara und ComfyUI. Die Dokumentation verlangt, ComfyUI aus derselben Umgebung zu starten, damit die Custom-Nodes ihre Abhängigkeiten finden.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Fixiere das aufgelöste Modell-Repository und die Revision vor dem Herunterladen. Der offizielle Link `xgen-universe` leitet derzeit auf `Glanty/Capybara` weiter.
  — <https://huggingface.co/xgen-universe/Capybara>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- 2026-02-20: Das frühere TODO „Add support for ComfyUI“ ist überholt, da Capybara Custom-Nodes und einen Beispiel-Workflow bereitstellt. Die native CLI bleibt unterstützt und wird nicht ersetzt.

## Weiterhin unbekannt {#still-unknown}

- Offizielle Quellen erklären nicht, ob die Hugging-Face-Weiterleitung von `xgen-universe/Capybara` auf `Glanty/Capybara` eine Übertragung der Eigentümerschaft, ein Spiegel oder ein Fehler ist. Überprüfe vor der Verwendung konkrete Dateien und Revision.
- Die Dokumentation des Erstanbieters enthält keine VRAM-Tabellen, unabhängigen Benchmarks oder Nachweise für Produktionsreife. Der Trainingscode ist ebenfalls noch nicht veröffentlicht.
- Die temporäre ngrok-Demo-URL vom Ereignis am 2026-02-17 ließ sich nicht gefahrlos öffnen, daher ist ihre aktuelle Verfügbarkeit nicht bestätigt.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/xgen-universe/Capybara | xgen-universe/Capybara — Repository-README | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/README.md | Capybara — Haupt-README, Rohquelle | 2026-09-04 |
| https://huggingface.co/xgen-universe/Capybara | xgen-universe/Capybara — Hugging-Face-Modellseite, weitergeleitet auf Glanty/Capybara | 2026-09-04 |
| https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct | Qwen3-VL-8B-Instruct — Hugging-Face-Modellkarte | 2026-09-04 |
| https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md | Capybara ComfyUI Custom Nodes | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/comfyui/README.md | Capybara ComfyUI Custom Nodes — Rohquelle | 2026-09-04 |
| https://github.com/xgen-universe/Capybara/blob/main/comfyui/examples/sample_workflow.json | Capybara ComfyUI Beispiel-Workflow | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/comfyui/examples/sample_workflow.json | Capybara ComfyUI Beispiel-Workflow — Rohquelle | 2026-09-04 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:capybara`, Thread `capybara-development`, 2 datierte Ereignisse vom 2026-02-17 bis 2026-02-24.
- **Praxishinweis:** Nach dem 2026-02-24 sollten Praktiker, die Capybara evaluieren, dessen ComfyUI-Dokumentation, Beispiel-Workflow und FP8-Hinweise heranziehen, statt sich nur auf das Basis-Repository oder die Modellseite zu stützen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was überholt ist.

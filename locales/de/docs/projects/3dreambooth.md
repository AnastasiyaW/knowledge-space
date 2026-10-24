---
title: "3DreamBooth"
category: projects
date: 2026-03-21
tags: [3dreambooth, 3dreambooth-development, project]
aliases: ["3DreamBooth"]
level: 3
source_sha256: 7fccec91638e54a5674ee80aa7ab3b37da3ff5443d88dc75d23d7c3ffb0dc52a
translation: machine
translated_at: '2026-10-24'
---
# 3DreamBooth {#3dreambooth}

**Entwicklungslinie:** `project:3dreambooth` · Thread `3dreambooth-development`  
**Letztes Ereignis:** 2026-03-21 · 1 datiertes Ereignis seit 2026-03-21 · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

3DreamBooth ist eine Forschungscodebasis, die HunyuanVideo-1.5 an ein aus mehreren Blickwinkeln erfasstes Subjekt anpasst.

- 3DreamBooth: Ein-Frame-LoRA-Optimierung pro Subjekt für räumliche Identität.
- 3Dapter: Ein Adapter zur Referenzbild-Konditionierung, der gemeinsam mit der Subjekt-LoRA optimiert wird.

Das Paper berichtet von Ausgaben mit 720p, 81 Frames und 50 Schritten; das öffentliche Repository kennzeichnet den Evaluierungscode weiterhin als nicht verfügbar. Verwenden Sie es für kontrollierte Reproduktion oder Inferenz mit bereitgestellten Checkpoints, nicht als fertiges Produktionspaket.

## Entwicklungslinie {#development-line}

- **2026-03-21 — Projektressourcen zu 3DreamBooth wurden öffentlich verlinkt.** Am 2026-03-21 verlinkte ein Eintrag die Projektwebsite von 3DreamBooth und das zugehörige GitHub-Quellcode-Repository. Wir betrachten dies als öffentlichen Referenzpunkt für die Projektgeschichte. Wir leiten keine belegslose Veröffentlichung, Funktion oder sonstige Änderung ab.

## Was sich geändert hat {#what-changed}

- 2026-03-19 — arXiv v1 stellte 3DreamBooth, 3Dapter und 3D-CustomBench vor.
- 2026-03-20 — Das Repository verzeichnet seinen initialen Commit, entfernt das Badge „Code Coming Soon“ und lädt Quelldateien hoch.
- 2026-03-21 — Die Projektseite und das Repository wurden für das datierte Ereignis verlinkt. Eine unabhängige Überprüfung eines offiziellen Starttermins liegt uns nicht vor.
- 2026-07-22 — Hugging Face führte den Datensatz 3D-CustomBench als aktualisiert.
- 2026-07-28 — Hugging Face führte die Checkpoint-Sammlung 3DreamBooth-CustomBench als aktualisiert.

## So verwenden Sie es {#how-to-use-this}

1. Klonen Sie das Repository, erstellen Sie seine Python-3.10-Umgebung und installieren Sie die deklarierten Anforderungen.
  — <https://github.com/Ko-Lani/3DreamBooth>
2. Laden Sie HunyuanVideo-1.5, dessen Text- und Vision-Abhängigkeiten sowie den vortrainierten 3Dapter herunter. Erhalten Sie Zugriff auf das zugangsbeschränkte FLUX.1-Redux-dev, bevor Sie einen Job starten.
  — <https://github.com/Ko-Lani/3DreamBooth>
3. Für einen fertigen Testlauf laden Sie eines der 30 gemeinsamen CustomBench-Checkpoint-Paare herunter und verwenden Sie dessen exakte Kombination aus Identifikator und Klassen-Trigger-Phrase.
  — <https://huggingface.co/lanikoworld/3DreamBooth-CustomBench>
4. Für ein eigenes Subjekt bereiten Sie geordnete Mehransichtsaufnahmen in `images/` vor sowie eine kleinere Menge hintergrundfreigestellter, weiß normalisierter quadratischer Referenzen in `references/`.
  — <https://github.com/Ko-Lani/3DreamBooth>
5. Führen Sie die mitgelieferte YAML-Konfiguration zunächst mit `--dry-run` aus und verwenden Sie dann je nach Bedarf den Modus `3dreambooth` als Baseline oder den gemeinsamen Modus.
  — <https://github.com/Ko-Lani/3DreamBooth/blob/main/docs/training-modes.md>
6. Halten Sie die Länge generierter Videos bei 4n + 1, etwa 49, 81 oder 129 Frames. Betrachten Sie einen visuellen Lauf nicht als offizielle Metrik-Reproduktion, solange der Evaluierungscode fehlt.
  — <https://github.com/Ko-Lani/3DreamBooth>

## Bewährte Vorgehensweisen {#best-practices}

- Beginnen Sie mit einem mitgelieferten CustomBench-Checkpoint, bevor Sie eigenes Training versuchen. Dadurch lassen sich Umgebungs- und Prompt-Fehler von Fehlern im Subjekt-Training trennen.
  — <https://huggingface.co/lanikoworld/3DreamBooth-CustomBench>
- Verwenden Sie vielfältige, geordnete Ansichten und Referenzen, die die volle 360-Grad-Ausdehnung des Objekts abdecken. Entfernen Sie Referenzhintergründe vor der Konditionierung.
  — <https://arxiv.org/html/2603.18524>
- Halten Sie die Phrase aus Identifikator und Klasse in eckigen Klammern während Training und Validierung identisch. Die wörtliche Phrase ist der LoRA-Abschnitt, der die Identität aktiviert.
  — <https://huggingface.co/lanikoworld/3DreamBooth-CustomBench>
- Validieren Sie die YAML-Auflösung mit `--dry-run`, bevor Sie große Checkpoints laden oder verteiltes Training starten.
  — <https://github.com/Ko-Lani/3DreamBooth/blob/main/docs/training-modes.md>
- Prüfen Sie die FLUX-Zugangsrechte und die aus Hunyuan abgeleiteten Lizenzbedingungen, bevor Sie sich auf einen Workflow oder eine kommerzielle Nutzung festlegen.
  — <https://github.com/Ko-Lani/3DreamBooth>

## Durch dieses ersetzt {#superseded-by-this}

- 2026-03-20 — Der anfängliche Zustand „Code Coming Soon“ ist veraltet: Die Repository-Historie verzeichnet dessen Entfernung und das Hochladen der Quelldateien.

## Weiterhin unbekannt {#still-unknown}

- Wir haben für den exakten Codestand vom 2026-03-21 weder einen unveränderlichen Tag noch ein GitHub-Release gefunden, sodass wir diese Revision anhand der geprüften öffentlichen Seiten nicht fixieren können.
- Die Hugging-Face-Kennzeichnungen aus Juli belegen Aktualisierungsdaten, nicht aber die genauen dateibezogenen Änderungen an diesen Tagen.
- Wir haben keine lokale Installation, keine Messung des GPU-Speichers, keinen Durchsatztest und keine unabhängige Metrik-Reproduktion durchgeführt; der offizielle Evaluierungscode bleibt nicht verfügbar.
- Wir haben keine Dokumentation in vereinfachtem Chinesisch von den Entwicklern und keine offizielle chinesischsprachige Community-Anleitung gefunden; die aktuelle praktische Anleitung stützt sich auf englischsprachige Primärquellen.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://ko-lani.github.io/3DreamBooth/ | 3DreamBooth | 2026-09-07 |
| https://github.com/Ko-Lani/3DreamBooth | Ko-Lani/3DreamBooth | 2026-09-07 |
| https://arxiv.org/abs/2603.18524 | 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model | 2026-09-07 |
| https://arxiv.org/html/2603.18524 | 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model — HTML | 2026-09-07 |
| https://github.com/Ko-Lani/3DreamBooth/commits/main | Commits · Ko-Lani/3DreamBooth | 2026-09-07 |
| https://github.com/Ko-Lani/3DreamBooth/blob/main/docs/training-modes.md | Trainings- und Validierungsmodi | 2026-09-07 |
| https://huggingface.co/lanikoworld/3DreamBooth-CustomBench | 3DreamBooth-CustomBench-Checkpoints | 2026-09-07 |
| https://huggingface.co/datasets/lanikoworld/3D-CustomBench | 3D-CustomBench | 2026-09-07 |
| https://huggingface.co/papers/2603.18524 | Paper-Seite — 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model | 2026-09-07 |

## Agent-Kurzbriefing {#agent-brief}

- **Subjekt:** `project:3dreambooth`, Thread `3dreambooth-development`, 1 datiertes Ereignis 2026-03-21 → 2026-03-21.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Nutzung und Vorgehensweisen oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

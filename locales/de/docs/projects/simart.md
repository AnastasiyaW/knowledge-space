---
title: "SIMART"
category: projects
date: 2026-05-19
tags: [project, simart, simart-development]
aliases: ["SIMART", "SimArt"]
level: 2
source_sha256: 0e53f8aea05b9cd1a6531a668154119f223fd71413301215cd140abdc467495f
translation: machine
translated_at: '2026-10-24'
---
# SIMART {#simart}

**Entwicklungslinie:** `project:simart` · Thread `simart-development`  
**Letztes Ereignis:** 2026-05-19 · 2 datierte seit 2026-03-30 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

SIMART ist eine Forschungsimplementierung von ByteDance Seed für 3D- und Robotik-Praktiker, die ein monolithisches Mesh in artikulierte Teile für Simulatoren umwandeln müssen. Es kombiniert ein auf Qwen3-VL basierendes MLLM mit einem Sparse 3D VQ-VAE. Es sagt zerlegte Teile, physikalische Metadaten, Gelenktypen, Achsen und Grenzwerte voraus und gibt anschließend URDF-orientierte Dateien aus. Laut Paper benötigt es 70 % weniger Geometrie-Tokens als dichte Voxel. Das Repository ist für Python 3.10 getestet und stellt lokale Checkpoints bereit, keinen gehosteten Inferenz-Endpunkt. Verwenden Sie es als lokale Forschungspipeline zur Vorbereitung artikulierter Assets, und validieren Sie die erzeugte URDF, bevor Sie sich in einem Simulator darauf verlassen.

## Entwicklungslinie {#development-line}

- **2026-03-30 — Referenz auf die SIMART-Projektwebsite.** Am 2026-03-30 etablierte die Projektwebsite den ersten öffentlichen Einstiegspunkt. Die verfügbaren Belege nennen kein konkretes Release, keine Fähigkeit und keine Version.
- **2026-05-19 — Referenz auf das SIMART-Hugging-Face-Repository.** Am 2026-05-19 erschien das Hugging-Face-Repository ByteDance-Seed/SimArt zusammen mit der Projektseite. Die verfügbaren Belege belegen weder den Inhalt des Repositorys noch die Lizenz oder den genauen Release-Status.

## Was sich geändert hat {#what-changed}

- **2026-03-24** — Das arXiv-Preprint führte die einheitliche Methode von SIMART für die Umwandlung von Mesh zu artikulierten Assets, den Sparse 3D VQ-VAE und SIMART-Bench ein und berichtete eine Token-Reduktion um 70 % gegenüber dichten Voxel-Tokens.
- **2026-03-30** — Die Projektseite machte die Forschungspräsentation und eine interaktive Galerie artikulierter Assets verfügbar und beschrieb strukturierte URDF-Metadaten zusammen mit zerlegten Segmenten.
- **2026-05-19** — Verfolgte Links ergänzten das Hugging-Face-Repository von ByteDance-Seed neben der Projektseite. Die Model Card nennt zwei Checkpoint-Gruppen, `simart_mllm/` und `simart_vqvae/`.
- **2026-05-28** — Auf Hugging Face erschien ein Update zu `ByteDance-Seed/SimArt`. Die Model Card stellt Gewichte ohne gehosteten Inferenzanbieter bereit.
- **2026-09-05** — Das öffentliche GitHub-README dokumentierte lokale Installation, Mesh-Ausrichtung, Vorverarbeitung und Inferenz für GLB-Eingaben.

## Verwendung {#how-to-use-this}

Ab dem 2026-05-19 sollten Praktiker bei der Suche nach Projektmaterialien das verlinkte Hugging-Face-Repository ByteDance-Seed/SimArt zusammen mit der SIMART-Projektseite prüfen; die datierten Belege bestätigen nicht, welche Artefakte nutzbar sind.

1. Klonen Sie die Implementierung, erstellen Sie eine Python-3.10-Umgebung und installieren Sie `requirements.txt`.
  — <https://github.com/ByteDance-Seed/SimArt>
2. Laden Sie beide Checkpoint-Gruppen aus dem offiziellen Hugging-Face-Repository herunter und legen Sie sie unter `./checkpoints` ab oder übergeben Sie eigene Pfade.
  — <https://huggingface.co/ByteDance-Seed/SimArt>
3. Normalisieren Sie ein rohes `.glb`-Mesh mit `scripts/process_raw_objects.py`; rendern Sie während der Vorverarbeitung eine Vorschau.
  — <https://github.com/ByteDance-Seed/SimArt>
4. Führen Sie `inference/infer.py --object_path <processed.glb> --debug` aus, um die artikulierte Struktur, URDF und Debug-Visualisierungen zu erzeugen.
  — <https://github.com/ByteDance-Seed/SimArt>

## Best Practices {#best-practices}

- Verwenden Sie ein rechtshändiges Koordinatensystem mit +Z nach oben und einer konsistenten Vorwärtsrichtung; korrigieren Sie Rotationen bei Meshes, die eine andere Konvention verwenden.
  — <https://github.com/ByteDance-Seed/SimArt>
- Rendern Sie die Normalisierungsvorschau und prüfen Sie vor der Inferenz, ob das Objekt aufrecht und nach vorne ausgerichtet ist, da die Orientierung semantische Teile wie Griffe und Vorderbeine beeinflusst.
  — <https://github.com/ByteDance-Seed/SimArt>
- Verwenden Sie `--debug`, um farbige Teil-Meshes und Gelenkachsen zu prüfen, und validieren Sie die erzeugte URDF im Zielsimulator, bevor Sie sie für Robot-Policy-Arbeiten verwenden.
  — <https://github.com/ByteDance-Seed/SimArt>

## Abgelöst durch diesen Stand {#superseded-by-this}

- 2026-03-24 — Die Behandlung von SIMART als reine Papermethode ist veraltet: Das Repository und die Veröffentlichung der Checkpoints bieten einen lokalen Inferenzpfad.
- 2026-05-28 — Die Annahme, SIMART sei über einen verwalteten Inferenzanbieter auf Hugging Face verfügbar, wird nicht unterstützt; die offizielle Modellseite besagt, dass kein Anbieter es bereitstellt.

## Weiterhin unbekannt {#still-unknown}

- Die offizielle Hugging-Face-Model-Card zeigt keinen eigenen Veröffentlichungszeitstempel an, daher lässt sich über das Vorhandensein des Repository-Links hinaus keine unabhängig datierte Änderung speziell dem Ereignis vom 2026-05-19 zuordnen.
- Der Name ist im weiteren Web mehrdeutig: Eine unverwandte 6G-Plattform für Sensorik und Kommunikation trägt ebenfalls den Namen SimART. Das zitierte ByteDance-Seed-Projekt, Paper, Code und die Gewichte bezeichnen konsistent den Gegenstand der artikulierten 3D-Assets.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://arxiv.org/abs/2603.23386 | SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM | 2026-09-05 |
| https://simart-mllm.github.io/ | SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM | 2026-09-05 |
| https://github.com/ByteDance-Seed/SimArt | ByteDance-Seed/SimArt | 2026-09-05 |
| https://huggingface.co/ByteDance-Seed/SimArt | ByteDance-Seed/SimArt | 2026-09-05 |
| https://huggingface.co/MinghanQin/activity/all | Minghan Qin activity | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:simart`, Thread `simart-development`, 2 datierte Ereignisse 2026-03-30 → 2026-05-19.
- **Praktischer Hinweis:** Ab dem 2026-05-19 sollten Praktiker bei der Suche nach Projektmaterialien das verlinkte Hugging-Face-Repository ByteDance-Seed/SimArt zusammen mit der SIMART-Projektseite prüfen; die datierten Belege bestätigen nicht, welche Artefakte nutzbar sind.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

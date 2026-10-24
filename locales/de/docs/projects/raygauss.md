---
title: "RayGauss"
category: projects
date: 2024-11-17
tags: [project, raygauss]
aliases: ["RayGauss"]
level: 2
source_sha256: 76eb421bfabca4c925746026bfdaa999f9cbef49afababfe923c61eefbd8a96f
translation: machine
translated_at: '2026-10-24'
---
# RayGauss {#raygauss}

**Entwicklungslinie:** `project:raygauss` · Thread `raygauss`  
**Letztes Ereignis:** 2024-11-17 · 2 datierte seit 2024-08-08 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Worum es sich handelt {#what-it-is}

RayGauss ist Code und Methode zur neuartigen Ansichtssynthese (novel view synthesis) für Forschende und wurde als volumetrische Alternative zu Splatting entwickelt.

- Szenentraining aus Multi-View-Bildern.
- Volumetrisches Rendering mit elliptischen Gauß-Basisfunktionen, SH- und SG-Features sowie BVH/OptiX-Ray-Casting.
- PLY-Export für die Szenengeometrie.
- GUI-Viewer zur Inspektion trainierter Szenen.

Das ursprüngliche Paper berichtet 25 FPS auf Blender. Der Code eignet sich zur Reproduktion des Papers und zum Experimentieren auf NVIDIA/OptiX, ist aber keine allgemeine Produktionsbibliothek.

## Entwicklungslinie {#development-line}

- **2024-08-08 — Öffentliche Projektseite zu RayGauss referenziert.** Gauß-parametrisiertes Strahlungsfeld (radiance field) mit differenzierbarem volumetrischem Ray-Casting, in Konkurrenz zu Splatting.
- **2024-11-17 — Quellcode-Repository zu RayGauss referenziert.** Am 2024-11-17 wurde das öffentliche GitHub-Repository verlinkt, ohne verifizierte Aussagen zu Codeversion, Inhalt oder Release-Status.

## Was sich geändert hat {#what-changed}

2024-08-08 — RayGauss wird veröffentlicht: ein Gauß-parametrisiertes Strahlungsfeld mit differenzierbarem volumetrischem Ray-Casting, in Konkurrenz zu Splatting. 2024-11-17 — Das öffentliche Implementierungs-Repository ist verfügbar, mit Setup, Training, Evaluation, PLY-Export und GUI. 2025-09-09 — Die Autorinnen und Autoren veröffentlichen RayGaussX, das das Training und das Rendering von RayGauss auf realen Szenen beschleunigt.

## So wird es verwendet {#how-to-use-this}

Um RayGauss zum Stand 2024-11-17 zu reproduzieren oder zu bewerten, beginnen Sie mit der öffentlichen Projektseite und dem verlinkten GitHub-Repository und überprüfen Sie anschließend Installation, Version und Ergebnisaussagen.

1. NVIDIA-Treiber, CUDA und OptiX 7.6 installieren, das Repository klonen und aus environment.yml eine conda-Umgebung erstellen; die angegebene Trainingsqualität setzt eine GPU mit 24 GB VRAM voraus.
  — <https://github.com/hugobl1/ray_gauss>
2. Die Szene in COLMAP-Struktur vorbereiten: images und sparse/0 mit cameras.bin, images.bin und points3D.bin; unterstützte Kameramodelle sind SIMPLE_PINHOLE und PINHOLE.
  — <https://github.com/hugobl1/ray_gauss>
3. Das Training einer Einzelszene über main_train.py mit einer YAML-Konfiguration ausführen und anschließend über main_test.py evaluieren.
  — <https://github.com/hugobl1/ray_gauss>
4. Die trainierte Szene über convertpth_to_ply.py nach PLY exportieren und das Ergebnis in main_gui.py betrachten.
  — <https://github.com/hugobl1/ray_gauss>

## Best Practices {#best-practices}

- Unter Windows die Versionen cuda-toolkit und pytorch-cuda in environment.yml an die installierte CUDA-Version anpassen; python-optix aus dem Quellcode bauen, statt ein conda-Paket zu erwarten.
  — <https://github.com/hugobl1/ray_gauss>
- Für reproduzierbare Vergleiche den Datensatz in dataset/ ablegen und das mitgelieferte Skript nerf_synth.sh oder mip_nerf360.sh ausführen.
  — <https://github.com/hugobl1/ray_gauss>
- Die angegebenen 25 FPS auf Blender nicht auf reale Szenen übertragen: Die nachfolgende Arbeit der Autorinnen und Autoren stellt fest, dass der Rechenaufwand von RayGauss Echtzeit-Rendering auf realen Szenen verhindert.
  — <https://arxiv.org/abs/2509.07782>

## Hierdurch abgelöst {#superseded-by-this}

- 2025-09-09 — Für Echtzeitaufgaben auf realen Szenen ist die Annahme, dass das Basis-RayGauss schnell genug ist, durch RayGaussX abgelöst; die Basisimplementierung bleibt als eigenständiger Code für die ursprüngliche Methode bestehen.

## Weiterhin unbekannt {#still-unknown}

- Keine unabhängige, datierte Primärquelle zum 2024-11-17 liefert über die Beschreibung des aktuellen Repository-Zustands hinaus datumsspezifische Fakten.
- In den verfügbaren Primärquellen existiert kein stabiles, versioniertes Release und keine unterstützte API; die Kompatibilität mit dem jeweiligen CUDA-, OptiX- und Treiber-Setup ist zu prüfen.
- event_findings: [{"event_date":"2024-08-08","finding":"Das Preprint vom 2024-08-06 präzisiert die Methode: Strahlungsdichte und Dichte werden durch Gauß-Basisfunktionen mit sphärischen Harmonischen und sphärischen Gauß-Funktionen dargestellt, mit Integration Schicht für Schicht über eine GPU-BVH; für den Blender-Datensatz werden 25 FPS angegeben.","source_url":"https://arxiv.org/abs/2408.03356","source_date":"2024-08-06"}]
- new_events: [{"date":"2025-09-09","finding":"Die Autorinnen und Autoren stellen RayGaussX vor: Überspringen des leeren Raums, adaptives Sampling, erhöhte Strahlkohärenz, Skalenregularisierung und ein neues Kriterium für die Verdichtung (densification); das Paper berichtet 5- bis 12-fach schnelleres Training, 50- bis 80-fach schnelleres Rendering und einen Gewinn von bis zu 0,56 dB PSNR auf realen Datensätzen.","source_url":"https://arxiv.org/abs/2509.07782","source_date":"2025-09-09"}]

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://raygauss.github.io/ | RayGauss: Volumetric Gaussian-Based Ray Casting for Photorealistic Novel View Synthesis | 2026-09-05 |
| https://arxiv.org/abs/2408.03356 | RayGauss: Volumetric Gaussian-Based Ray Casting for Photorealistic Novel View Synthesis | 2026-09-05 |
| https://github.com/hugobl1/ray_gauss | hugobl1/ray_gauss | 2026-09-05 |
| https://arxiv.org/abs/2509.07782 | RayGaussX: Accelerating Gaussian-Based Ray Marching for Real-Time and High-Quality Novel View Synthesis | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:raygauss`, Thread `raygauss`, 2 datierte Ereignisse 2024-08-08 → 2024-11-17.
- **Praxishinweis:** Zum Stand 2024-11-17 sollten Praktiker, die RayGauss bewerten oder reproduzieren wollen, mit der öffentlichen Projektseite und dem verlinkten GitHub-Repository beginnen und danach Installation, Version und Ergebnisaussagen eigenständig überprüfen.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich für die Frage, was veraltet ist.

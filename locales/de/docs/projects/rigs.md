---
title: "RiGS — Referenz zum Repository"
category: projects
date: 2026-07-25
tags: [project, repository-reference, rigs]
aliases: ["RiGS"]
level: 2
source_sha256: 0a0e9de8234db679f9d9bd936a2eda29c3a09092887519aed925fce0d5952027
translation: machine
translated_at: '2026-10-24'
---
# RiGS — Referenz zum Repository {#rigs-repository-reference}

**Entwicklungslinie:** `project:rigs` · Thread `repository-reference`  
**Letztes Ereignis:** 2026-07-25 · 1 datiertes seit 2026-07-25 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Worum es geht {#what-it-is}

RiGS stellt die Codebasis für Rigid-aware 4D Gaussian Splatting bereit:
- Primitive: trennt Szenen in statische, starre und transiente Gaussian-Komponenten.
- Datenvorbereitung: erzeugt Eingaben über ViPE und TAPIR/BootsTAPIR.
- Workflow: trainiert, evaluiert, rendert und zeigt Szenen in einem Viewer an.

Erfordert Python 3.10 und einen CUDA-12.x-kompatiblen Stack. Forschungscode ohne Release-Pakete.

## Entwicklungslinie {#development-line}

- **2026-07-25 — Auf das RiGS-Projekt-Repository wurde verwiesen.** Am 2026-07-25 verlinkte die Projektlinie auf das RiGS-GitHub-Repository. Der Verweis dokumentiert die öffentliche Verfügbarkeit, ohne Funktionen, Release-Status oder Repository-Inhalte zu behaupten.

## Was sich geändert hat {#what-changed}

2026-07-25 — Die RiGS-Implementierung im Repository wurde verfügbar. Quellmaterialien geben an, dass die Methode auf einem einzelnen monokularen Video arbeitet und statische, starre und transiente Komponenten über unterschiedliche Bewegungszeitskalen hinweg verwendet.

2026-05-22 — Frühere Angabe: Die Autorinnen und Autoren veröffentlichten das RiGS-Paper auf arXiv (v1), das objektweise dynamische Masken und Scene-Flow-Supervision beschreibt.

## So wird es verwendet {#how-to-use-this}

Ab dem 2026-07-25 das verlinkte RiGS-GitHub-Repository als datierte Quellenreferenz für diese Projektlinie verwenden und dessen aktuellen Inhalt separat prüfen.

1. Repository mit dem ViPE-Submodul klonen, eine Conda-Umgebung mit Python 3.10 anlegen, die Requirements und das lokale ViPE-Paket installieren und anschließend den TAPIR/BootsTAPIR-Checkpoint herunterladen.
  — <https://github.com/ladvu/RiGS>
2. Video und Frames vorbereiten, Tiefe, Posen, Intrinsics, optischen Fluss, Flusskonsistenz und statische Masken über ViPE extrahieren und danach TAPIR-Tracks erzeugen.
  — <https://github.com/ladvu/RiGS>
3. `src/main.py` mit Datenpfaden und einem Experimentnamen ausführen; mit `--eval_step`, `--render_video` oder `run_viewer.py` die Ergebnisse der Checkpoints prüfen.
  — <https://github.com/ladvu/RiGS>

## Best Practices {#best-practices}

- Mit `--recursive` klonen oder die Submodule anschließend manuell initialisieren; ohne sie läuft die monokulare Vorverarbeitung nicht.
  — <https://github.com/ladvu/RiGS>
- PyTorch-, CUDA-Toolkit- und Treiberversionen vor dem Training mit den festgelegten Requirements abgleichen, da das Repository auf CUDA 12.x ausgelegt ist.
  — <https://github.com/ladvu/RiGS>
- Visualisierungen der Vorverarbeitung prüfen und TAPIR-Tracks vor der Rekonstruktion erzeugen: Die Pipeline benötigt sowohl ViPE-Ausgaben als auch 2D-Tracks.
  — <https://github.com/ladvu/RiGS>

## Ersetzt durch dies {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- GitHub veröffentlicht keine Releases, daher bietet das Repository weder eine versionierte Release-Historie noch einen Pfad für eine paketierte Installation.
- Die verfügbaren Seiten des Erstanbieters legen keinen datierten Eintrag zur Erstellung des Repositorys oder zu Commits offen, der die Veröffentlichung des Codes unabhängig konkret auf den 2026-07-25 bezieht; dieses Datum bleibt das datierte Ereignis, das für den Repository-Link angegeben wurde.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/ladvu/RiGS | ladvu/RiGS — offizielle Implementierung und Nutzungsanleitung | 2026-09-05 |
| https://arxiv.org/abs/2605.23672 | RiGS: Rigid-aware 4D Gaussian Splatting from a Single Monocular Video | 2026-09-05 |
| https://ladvu.github.io/RiGS/ | RiGS-Projektseite | 2026-09-05 |
| https://github.com/ladvu/RiGS/releases | RiGS-Releases | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:rigs`, Thread `repository-reference`, 1 datiertes Ereignis 2026-07-25 → 2026-07-25.
- **Praktischer Hinweis:** Ab dem 2026-07-25 sollten Praktiker das verlinkte RiGS-GitHub-Repository als datierte Quellenreferenz für diese Projektlinie verwenden und dessen aktuellen Inhalt separat prüfen.
- **Konfidenz:** hoch. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

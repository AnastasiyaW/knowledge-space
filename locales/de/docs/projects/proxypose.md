---
title: "ProxyPose"
category: projects
date: 2026-07-11
tags: [project, proxypose, proxypose-development]
aliases: ["ProxyPose"]
level: 2
source_sha256: 22cb6a9630aae978ded512d5855c4943d40a035d058a65b45155b19db39146e2
translation: machine
translated_at: '2026-10-24'
---
# ProxyPose {#proxypose}

**Entwicklungslinie:** `project:proxypose` · Thread `proxypose-development`  
**Letztes Ereignis:** 2026-07-11 · 1 datiertes Ereignis seit 2026-07-11 · **Recherchiert:** 2026-09-05 · Konfidenz: high

## Was es ist {#what-it-is}

ProxyPose ist eine Methode und eine offene Implementierung für Forscherinnen und Forscher der Computer Vision, die die 6-DoF-Trajektorie einer lokalen Oberfläche oder eines Objekts aus monokularem Video benötigen. Funktionen: RGB-Video und ein Punkt im ersten Frame; Erzeugung eines Proxy-Videos mit einem farbigen Polyeder; Posenrekonstruktion per geometrischem PnP; Anwendung auf Objekte, Kameras und Gesichter. Einschränkung: Schnelle Bewegungen, spiegelnde und texturarme Oberflächen können Drift verursachen oder die Proxy-Frames verwischen. Fazit: Praktisch für reproduzierbare Forschungsauswertung auf GPU, sofern ein generativer Schritt und die Überprüfung der Ergebnisse akzeptabel sind.

## Entwicklungslinie {#development-line}

- **2026-07-11 — Öffentliche Projektressourcen von ProxyPose verlinkt.** Am 2026-07-11 wurde ProxyPose über verlinkte Projekt-, Quellcode- und Hugging-Face-Ressourcen vorgestellt. Dies ist ein wesentliches öffentliches Entwicklungsereignis, da damit eine auffindbare Projektpräsenz entsteht; die technischen Aussagen und der Veröffentlichungsstatus der verlinkten Ressourcen wurden jedoch nicht unabhängig geprüft.

## Was sich geändert hat {#what-changed}

2026-07-11 — Projektseite, Quellcode und Gewichte von ProxyPose für 6-DoF-Pose-Tracking über Video-to-Video-Translation wurden veröffentlicht.

## Verwendung {#how-to-use-this}

Stand 2026-07-11 sollten Praktikerinnen und Praktiker die verlinkte Projektseite, das Repository und die Hugging-Face-Ressource als Ausgangspunkte für die Bewertung von ProxyPose nutzen. Dieses reine Link-Ereignis gilt hinsichtlich technischer Fähigkeiten und Veröffentlichungsdetails als nicht verifiziert.

1. Repository klonen, eine Python-3.10-Umgebung anlegen, PyTorch mit CUDA 12.1, PyTorch3D und das ProxyPose-Paket installieren.
  — <https://github.com/ruihangzhang97/proxypose>
2. Den lokalen Annotator mit `proxypose-annotate --input-video ...` öffnen, im ersten Frame einen Punkt auswählen und die Koordinaten als JSON speichern.
  — <https://github.com/ruihangzhang97/proxypose>
3. Bei Bedarf die Brennweite mit Depth Anything 3 schätzen; andernfalls wird ein fester horizontaler FOV von 45° verwendet.
  — <https://github.com/ruihangzhang97/proxypose>
4. `proxypose-infer` mit Video, JSON-Punkt und Ausgabepfad starten; für das kleinere Modell die Konfiguration Wan2.1-T2V-1.3B übergeben.
  — <https://github.com/ruihangzhang97/proxypose>

## Bewährte Praktiken {#best-practices}

- Für Qualität mit 14B beginnen; 1.3B eignet sich für schnelle Experimente oder begrenzten VRAM. LoRA und Basismodell müssen zur gewählten Größe passen.
  — <https://github.com/ruihangzhang97/proxypose>
- Die mit Depth Anything 3 geschätzte Brennweite verwenden, wenn die Genauigkeit der Geometrie wichtiger ist als ein schneller Start.
  — <https://github.com/ruihangzhang97/proxypose>
- Trajektorien bei schnellen, spiegelnden und texturarmen Szenen manuell prüfen, da diese Fälle als Ursachen für Drift und eine Verschlechterung der Konturerkennung angegeben sind.
  — <https://ruihangzhang97.github.io/proxypose/>

## Durch dies ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Das Datum, an dem die aktuelle Unterstützung für Wan2.1-T2V-1.3B ins Repository aufgenommen wurde, ist durch die verfügbare Commit-Historie nicht belegt. Deshalb wurde es nicht als eigenes datiertes Ereignis erfasst.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://ruihangzhang97.github.io/proxypose/ | ProxyPose — 6-DoF Pose Tracking via Video-to-Video Translation | 2026-09-05 |
| https://github.com/ruihangzhang97/proxypose | Offizielles ProxyPose-Repository und Installationsanleitung | 2026-09-05 |
| https://arxiv.org/abs/2607.06555 | ProxyPose: 6-DoF Pose Tracking via Video-to-Video Translation | 2026-09-05 |
| https://github.com/ruihangzhang97/proxypose/issues/2 | Issue #2: Request for Wan2.1-T2V-1.3B ProxyPose variant | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:proxypose`, Thread `proxypose-development`, 1 datiertes Ereignis vom 2026-07-11 → 2026-07-11.
- **Praxishinweis:** Stand 2026-07-11 sollten Praktikerinnen und Praktiker die verlinkte Projektseite, das Repository und die Hugging-Face-Ressource als Ausgangspunkte für die Bewertung von ProxyPose nutzen. Dieses reine Link-Ereignis gilt hinsichtlich technischer Fähigkeiten und Veröffentlichungsdetails als nicht verifiziert.
- **Konfidenz:** high. Datierte Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.

---
title: "QuerySplat"
category: projects
date: 2026-08-04
tags: [project, querysplat, querysplat-development]
aliases: ["QuerySplat"]
level: 2
source_sha256: 598e952ebb319537d3e7984a5c17062f64ed7a4e6284946d19de325b8cfbf901
translation: machine
translated_at: '2026-10-24'
---
# QuerySplat {#querysplat}

**Entwicklungslinie:** `project:querysplat` · Thread `querysplat-development`  
**Letztes Ereignis:** 2026-08-04 · 1 datiertes seit 2026-08-04 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

QuerySplat ist ein Feed-Forward-Framework für 3D Gaussian Splatting für Anwender, die aus Multi-View-Bildern ohne vorgegebene Kameraposen eine renderbare Szene und Novel Views benötigen.

- Ein dual-branch Query-Decoder trennt Geometrie und Erscheinungsbild.
- VGGT-Omega liefert die Kamera- und Tiefenvorhersage; Test-Time-Optimierung ist optional.

## Entwicklungslinie {#development-line}

- **2026-08-04 — Am 2026-08-04 wurde QuerySplat über seine Projektseite, das GitHub-Repository und die Hugging-Face-Seite verknüpft..** Am 2026-08-04 verknüpfte der datierte Eintrag QuerySplat mit einer öffentlichen Projektwebsite, einem GitHub-Repository und einer Hugging-Face-Seite. Das ist ein wesentlicher öffentlicher Entwicklungsmeilenstein, weil damit verknüpfte Projektressourcen etabliert werden. Die verfügbaren Belege stützen jedoch keine Aussagen über eine Release-Version, Funktionalität oder Ergebnisse.

## Was sich geändert hat {#what-changed}

2026-08-02 — InSpatio hat QuerySplat als Open Source gekennzeichnet. 2026-08-04 — Ein separat versioniertes QuerySplat-Release ist nicht belegt; das öffentliche Paper und der Open-Source-Status verweisen beide auf das Release vom 2. August.

## Wie man es verwendet {#how-to-use-this}

Stand 2026-08-04 sollten Praktiker die verlinkte Projektseite, das Quellcode-Repository und die Hugging-Face-Seite von QuerySplat als öffentlichen Ressourcensatz heranziehen und Fähigkeiten sowie Release-Status vor einer Adoption direkt anhand dieser Ressourcen prüfen.

1. Den getesteten Stack vorbereiten: Linux, eine CUDA-fähige NVIDIA-GPU, Python 3.12, PyTorch 2.11.0 und CUDA 12.8; danach das offizielle Inferenz-Repository klonen und dessen Anforderungen installieren.
  — <https://github.com/inspatio/querysplat>
2. Den QuerySplat-Checkpoint und die mitgelieferte Konfiguration herunterladen, vggt_omega_1b_512.pt dorthin in checkpoints herunterladen und vor der Inferenz `sha256sum -c SHA256SUMS` ausführen.
  — <https://github.com/inspatio/querysplat>
3. Vor dem Download des VGGT-Omega-Checkpoints anmelden und die Zugangsbedingungen akzeptieren; der Zugang ist separat beschränkt.
  — <https://huggingface.co/facebook/VGGT-Omega>
4. Bilder einer Szene in den Eingabeordner legen und `python -m scripts.infer` mit der mitgelieferten Konfiguration, dem QuerySplat-Checkpoint, dem Eingabeordner und dem Ausgabeverzeichnis ausführen.
  — <https://github.com/inspatio/querysplat>
5. Für Test-Time-Optimierung `--use_tto` hinzufügen; für reine Feed-Forward-Inferenz weglassen.
  — <https://github.com/inspatio/querysplat>

## Best Practices {#best-practices}

- In jedem Eingabeordner nur die Bilder einer Szene belassen. Beliebig viele Bilder stellen die vorgelagerte Eingabeschnittstelle dar, keine veröffentlichte Garantie für Skalierbarkeit.
  — <https://github.com/inspatio/querysplat>
- Die getestete PyTorch-/CUDA-Kombination verwenden und die Erweiterungen gsplat und fused-ssim dazu passend installieren; LPIPS kann beim ersten Gebrauch VGG16-Gewichte herunterladen.
  — <https://github.com/inspatio/querysplat>
- Beide heruntergeladenen Checkpoints vor jedem Lauf mit dem SHA-256-Manifest des Projekts verifizieren.
  — <https://github.com/inspatio/querysplat>
- 30+ Ansichten als ungeprüfte Kapazitätszone behandeln: Ein Nutzer berichtete am 6. August von einem Out-of-Memory-Fehler, ohne Angaben zu Hardware, Auflösung oder Reproduktion und ohne Antwort eines Maintainers. Mit kleineren Mengen beginnen und den VRAM-Verbrauch messen; dies ist anekdotisch und kein offizielles Limit.
  — <https://github.com/inspatio/querysplat/issues/2>
- Lizenzen je Komponente prüfen: Der von QuerySplat selbst geschriebene Code steht unter Apache-2.0, während der mitgelieferte VGGT-Omega-/DINOv3-Quellcode unter der FAIR Noncommercial Research License steht.
  — <https://github.com/inspatio/querysplat>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Ein separat versioniertes QuerySplat-Release vom 2026-08-04 wurde nicht gefunden; das öffentliche Paper und der Open-Source-Status sind unabhängig voneinander auf den 2026-08-02 datiert.
- Das geprüfte offizielle Repository beschreibt nur Inferenz. In diesem Rechercheschritt wurde keine Veröffentlichung von Trainingscode verifiziert; eine Frage dazu vom 7. August ist ohne Antwort eines Maintainers offen.
- In diesem Rechercheschritt wurde keine unabhängige Reproduktion des DL3DV-Ergebnisses gefunden; die berichteten Gewinne von 2,30 dB ohne Posen und 1,04 dB mit Posen sind vom Autorenteam im Paper berichtete Ergebnisse.
- Die benötigte VGGT-Omega-Abhängigkeit hat am 18. August eine Warnung über mögliche Benchmark-Kontamination in einem Vorgänger-Checkpoint veröffentlicht. Sie besagt, dass die nachgelagerte Nutzung fortgesetzt werden kann, belegt aber keinen direkten Fehler im DL3DV-Ergebnis von QuerySplat.
- Eine von der Quelle selbst stammende vereinfachtes-chinesische Beschreibung wurde gefunden, es wurde aber kein unabhängiger Betriebsbericht auf Vereinfacht-Chinesisch verwendet.

## Quellen {#sources}

| Quelle | Titel | gelesen am |
|---|---|---|
| https://inspatio.github.io/querysplat/ | QuerySplat-Projektseite | 2026-09-05 |
| https://github.com/inspatio/querysplat | QuerySplat offizielles Inferenz-Repository | 2026-09-05 |
| https://huggingface.co/inspatio/querysplat | QuerySplat-Modellkarte und Checkpoint | 2026-09-05 |
| https://arxiv.org/abs/2608.01186 | QuerySplat: Decoupling Geometry and Appearance Representations in 3DGS Prediction | 2026-09-05 |
| https://www.inspatio.com/models/querysplat | InSpatio-QuerySplat-Modellseite | 2026-09-05 |
| https://huggingface.co/facebook/VGGT-Omega | VGGT-Omega-Modellkarte und Zugangsbedingungen | 2026-09-05 |
| https://github.com/inspatio/querysplat/issues/2 | large scene reconstruction, QuerySplat Issue 2 | 2026-09-05 |
| https://github.com/inspatio/querysplat/issues/3 | Will the training code be open-sourced?, QuerySplat Issue 3 | 2026-09-05 |
| https://www.inspatio.com/zh/models | InSpatio-Open-Models, vereinfachtes Chinesisch | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:querysplat`, Thread `querysplat-development`, 1 datiertes Ereignis 2026-08-04 → 2026-08-04.
- **Praktischer Hinweis:** Stand 2026-08-04 sollten Praktiker die verlinkte Projektseite, das Quellcode-Repository und die Hugging-Face-Seite von QuerySplat als öffentlichen Ressourcensatz heranziehen und Fähigkeiten sowie Release-Status vor einer Adoption direkt anhand dieser Ressourcen prüfen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

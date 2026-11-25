---
title: "CutLER"
category: projects
date: 2024-03-11
tags: [cutler, cutler-development, project]
aliases: ["CutLER", "VideoCutLER"]
level: 3
source_sha256: e5f70c51bdd22ee22e0391fc4b1ed27f06bdd3d3f8a01a6e5e74f8325232b7d6
translation: machine
translated_at: '2026-10-24'
---
# CutLER {#cutler}

**Entwicklungslinie:** `project:cutler` · Thread `cutler-development`  
**Letztes Ereignis:** 2024-03-11 · 2 datierte seit 2023-03-01 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

CutLER ist eine Pipeline von Pseudomasken zu Detektoren für unüberwachte Objekterkennung und Instanzsegmentierung.

- MaskCut erzeugt Pseudomasken mit mehreren Instanzen.
- CutLER trainiert Bilddetektoren und Segmentierer auf Basis dieser Masken.
- VideoCutLER wandelt Bildpaare in synthetische Videotrajektorien um und trainiert anschließend Video-Instanzsegmentierung ohne menschliche Labels, natürliche Videos oder optischen Fluss.

Das Setup zielt auf Linux/macOS, Python 3.8+, PyTorch 1.8+, Detectron2 und OpenCV 4.6+; das Repository hat keine getaggten Releases.

Wir können es als Forschungscode oder als reproduzierbare Baseline einsetzen. Testen Sie den veralteten Abhängigkeitsstack per Smoke-Test, bevor Sie sich auf das Training festlegen.

## Entwicklungslinie {#development-line}

- **2023-03-01 — CutLER-Projektressourcen wurden verfügbar.** MaskCut erzeugt Pseudomasken, danach lernt CutLER Objekterkennung und Instanzsegmentierung aus ImageNet-1K ohne menschliche Annotationen.
- **2024-03-11 — Die VideoCutLER-Dokumentation erweiterte die CutLER-Entwicklungslinie.** MaskCut → ImageCut2Video → Training des Videomodells, wodurch das Projekt auf das Tracking mehrerer Instanzen über Frames hinweg ausgeweitet wird.

## Was sich geändert hat {#what-changed}

2023-03-01 — CutLER etablierte den Bild-Workflow: MaskCut erzeugt Pseudomasken, danach lernt CutLER Objekterkennung und Instanzsegmentierung aus ImageNet-1K ohne menschliche Annotationen.

2023-08-27–29 — Die offizielle Git-Historie ordnet die Ergänzung des VideoCutLER-Codes vor dem späteren Dokumentationsereignis ein, in Commits mit der Bezeichnung „Add videocutler.“

2024-03-02 — Die offizielle Historie verzeichnet zwei weitere VideoCutLER-Commits, deren knappe Meldungen jedoch keine konkrete funktionale Änderung belegen.

2024-03-11 — VideoCutLER ist als eigenständiger Video-Workflow dokumentiert: MaskCut → ImageCut2Video → Training des Videomodells, wodurch das Projekt auf das Tracking mehrerer Instanzen über Frames hinweg ausgeweitet wird.

2025-06-03–04 — Upstream aktualisierte die Links zu den VideoCutLER-Checkpoints und dessen README. Es ist kein getaggtes Release verfügbar.

## Anwendung {#how-to-use-this}

Ab 2023-03-01 konnten Praktiker das CutLER-Repository, den MaskCut-Space und die Colab-Ressourcen nutzen, um das Projekt zu evaluieren. Ab 2024-03-11 sollten Sie die VideoCutLER-Dokumentation heranziehen, wenn der Anwendungsfall Video betrifft.

1. Installieren Sie den dokumentierten lokalen Stack: Linux oder macOS, kompatibles PyTorch/torchvision und Detectron2. Klonen Sie CutLER rekursiv und installieren Sie dessen Anforderungen.
  — <https://github.com/facebookresearch/CutLER/blob/main/INSTALL.md>
2. Für Einzelbilder beginnen Sie mit dem lokalen MaskCut- oder dem vortrainierten CutLER-Demo. Wählen Sie die passende Konfiguration und den Checkpoint aus dem Model Zoo und speichern Sie die Ausgaben lokal.
  — <https://github.com/facebookresearch/CutLER>
3. Für Videoinferenz laden Sie den offiziellen VideoCutLER-Checkpoint herunter. Führen Sie `videocutler/demo_video/demo.py` auf sequentiellen Einzelbildern aus, mit der mitgelieferten Mask2Former-Konfiguration, einem Ausgabeverzeichnis und den Modellgewichten.
  — <https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md>
4. Für das erneute Training bereiten Sie ImageNet-1K vor und erzeugen oder laden dann MaskCut-Pseudomasken herunter. Legen Sie den CutLER-Pretrain in `videocutler/pretrain` ab und führen Sie danach `train_net_video.py` aus.
  — <https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md>

## Bewährte Vorgehensweisen {#best-practices}

- Halten Sie PyTorch, torchvision und Detectron2 in kompatiblen Versionen. Das Upstream-Beispiel verwendet PyTorch 1.8.1, behandeln Sie daher eine moderne Umgebung als eigenes Validierungsziel.
  — <https://github.com/facebookresearch/CutLER/blob/main/INSTALL.md>
- Verwenden Sie den lokalen Workflow statt der MaskCut-Web-Demo: Der offizielle Hugging-Face-Space meldet derzeit einen Build-Fehler.
  — <https://huggingface.co/spaces/facebook/MaskCut>
- Beginnen Sie bei VideoCutLER mit der dokumentierten Konfidenzschwelle von 0,8. Senken Sie sie nur, wenn eine höhere Trefferquote Priorität hat, und speichern Sie Frames oder Masken zur Prüfung.
  — <https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md>
- Bei großen MaskCut-Annotationsläufen verteilen Sie Ordner mit `--num-folder-per-job` und `--job-index` auf mehrere Jobs. Führen Sie JSON-Dateien nur mit übereinstimmenden Einstellungen für `fixed_size`, `tau` und `N` zusammen.
  — <https://github.com/facebookresearch/CutLER>
- Fixieren Sie den exakten Repository-Commit und den Checkpoint eines Laufs, da Upstream keine getaggten Releases bereitstellt.
  — <https://github.com/facebookresearch/CutLER/tags>

## Abgelöst durch {#superseded-by-this}

- 2023-03-01: Der Weg über die MaskCut-Web-Demo ist für die aktuelle Nutzung veraltet. Ihr offizieller Hugging-Face-Space meldet nun einen Build-Fehler, daher verwenden Sie stattdessen lokalen Code.
- 2023-03-01: Die reine Bild-Anleitung zu CutLER ist für Videoarbeiten mit mehreren Instanzen unvollständig. Nutzen Sie für Video den eigenen Inferenz- und Trainings-Workflow von VideoCutLER und behalten Sie CutLER für Einzelbilder bei.
- 2024-03-11: Veraltete Dokumentation zu VideoCutLER-Checkpoints sollte hinter der am 2025-06-03–04 erfassten Überarbeitung des Upstream-README zurückstehen. Die Verfügbarkeit der Checkpoints wurde nicht unabhängig heruntergeladen.

## Weiterhin unbekannt {#still-unknown}

- Wir haben das Repository nicht installiert und nicht ausgeführt; die Kompatibilität mit aktuellen Versionen von CUDA, PyTorch und Detectron2 bleibt ungeprüft.
- Die ursprüngliche Projektseite der Berkeley-Gruppe und das Colab-Notebook von 2023 konnten in dieser Sitzung nicht unabhängig abgerufen oder ausgeführt werden, daher stützt keines von beiden eine Aussage zur aktuellen Nutzung.
- Die offizielle Historie benennt das Update zu VideoCutLER vom März 2024, nicht aber dessen genaue Verhaltensänderung.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/facebookresearch/CutLER | Cut and Learn für unüberwachte Bild- & Videoobjekterkennung und Instanzsegmentierung — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/blob/main/INSTALL.md | CutLER-Installationsanleitung — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md | VideoCutLER: Unsupervised Video Instance Segmentation — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/commits/main | CutLER-Commit-Historie — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/tags | CutLER-Releases und Tags — GitHub | 2026-09-04 |
| https://huggingface.co/spaces/facebook/MaskCut | MaskCut — Hugging-Face-Space von facebook | 2026-09-04 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:cutler`, Thread `cutler-development`, 2 datierte Ereignisse 2023-03-01 → 2024-03-11.
- **Praktischer Hinweis:** Ab 2023-03-01 konnten Praktiker das CutLER-Repository, den MaskCut-Space und die Colab-Ressourcen nutzen, um das Projekt zu evaluieren; ab 2024-03-11 sollten sie zusätzlich die VideoCutLER-Dokumentation heranziehen, wenn ihr Anwendungsfall Video betrifft.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

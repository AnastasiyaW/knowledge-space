---
title: "Align3R"
category: projects
date: 2024-12-18
tags: [align3r, project]
aliases: ["Align3R"]
level: 3
source_sha256: c7268ca9e1707e7202875a9c89bc1494829f67928d928cca77441aa0693e87e5
translation: machine
translated_at: '2026-10-24'
---
# Align3R {#align3r}

**Entwicklungslinie:** `project:align3r` · Thread `align3r`  
**Letztes Ereignis:** 2024-12-18 · 2 datierte Einträge seit 2024-12-06 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Align3R ist Forschungscode zur Rekonstruktion dynamischer Videos aus einer einzigen Kamera.

- richtet die monokulare Tiefe einzelner Frames an einem feinabgestimmten DUSt3R-Modell aus
- erzeugt zeitlich konsistente Tiefenkarten, dynamische Punktwolken und Kameraposen
- unterstützt Checkpoint-Pfade für Depth Pro und Depth Anything V2

## Entwicklungslinie {#development-line}

- **2024-12-06 — Öffentliche Projektressourcen von Align3R wurden verlinkt.** Am 2024-12-06 veröffentlichte Align3R eine offizielle Projektseite, ein öffentliches Quellcode-Repository und eine ergänzende Projektseite. Diese Links stellen öffentlich zugänglichen Code bereit, ohne die Inhalte des Releases näher zu beschreiben.
- **2024-12-18 — Align3R wurde mit einem gehosteten Hugging-Face-Space verknüpft.** Am 2024-12-18 verlinkte ein Folgeeintrag zu Align3R die frühere Projektseite und einen Align3R-Hugging-Face-Space. Der Link zeigt einen gehosteten Zugangspunkt, die Quelle beschreibt jedoch keine Änderungen an der Demo.

## Was sich geändert hat {#what-changed}

2024-12-06 — Align3R erschien als arXiv-Methode mit Projektseite, Quellcode und rekonstruierten Punktwolken. Sie kombiniert monokulare Tiefen-Priors mit DUSt3R-Ausrichtung und Optimierung für dynamische Videos. 2024-12-18 — ein interaktiver Align3R-Space wurde zusammen mit lokalem Code verfügbar; er läuft heute. Stand heute (2026-09-04) — das Haupt-README nennt Version 1.0.2 und den Status „CVPR 2025 Highlight“. Die PromptDA-Verfeinerung ist abgeschlossen; offen bleiben die Evaluation statischer Szenen, mehr reale Trainingsdaten sowie die Vorhersage von Kameraposen und Punktkorrespondenzen.

## So wird es verwendet {#how-to-use-this}

Stand 2024-12-06 konnten Anwender Align3R-Projektmaterialien und Quellcode finden; Stand 2024-12-18 können sie zusätzlich den Hugging-Face-Space für den gehosteten Zugang prüfen.

1. Das offizielle Repository klonen, die dokumentierte Python-3.11-Conda-Umgebung anlegen, einen passenden PyTorch/CUDA-Build installieren und die Requirements installieren.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
2. Vor der Inferenz die CUDA-Erweiterung für CroCo RoPE in croco/models/curope kompilieren.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
3. Depth Pro oder Depth Anything V2 wählen, den jeweiligen Tiefen-Stack installieren und danach den passenden Align3R-Checkpoint sowie gewichtete DUSt3R-Basisgewichte beschaffen.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
4. Die Platzhalter für Eingabe, Ausgabe und Sequenz in demo.sh setzen und das Skript auf der gewählten GPU ausführen; der mitgelieferte Launcher verwendet ein Intervall von 50.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/demo.sh>
5. Eine MP4-Datei oder ein Verzeichnis mit JPG-/PNG-Frames verwenden; die Demo erzeugt monokulare Tiefe, rekonstruiert die Szene und schreibt Posen, Intrinsics, Tiefenkarten, Masken, Konfidenzkarten und RGB-Ausgaben.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/tool/demo.py>
6. Für eine Verfeinerung in Originalauflösung PromptDA separat installieren und demo_refine.sh ausführen; mit dem mitgelieferten viser-Befehl lassen sich die Punktwolken inspizieren.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>

## Best Practices {#best-practices}

- Einen Repository-Commit fixieren und das genaue Checkpoint-Set für Reproduzierbarkeit dokumentieren: Es wird kein GitHub-Release-Artefakt veröffentlicht.
  — <https://github.com/jiah-cloud/Align3R/releases>
- Die benutzerdefinierte RoPE-CUDA-Erweiterung nach der Installation der Abhängigkeiten bauen; eine reine pip-Umgebung ist nicht die dokumentierte Laufzeitumgebung.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
- Den gewählten Tiefen-Prior, seinen Align3R-Checkpoint und die Evaluationseinstellung depth_prior_name konsistent halten.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
- Vor der Ergänzung der PromptDA-Verfeinerung, die einen eigenen Installationsweg hat, eine Baseline mit demo.sh etablieren.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
- Vor dem Berichten von Sintel-Ergebnissen die Aufteilung clean versus final im Checkout abgleichen; ein offenes Issue meldet diese Abweichung.
  — <https://github.com/jiah-cloud/Align3R/issues/27>
- Die Bedingungen des Repositorys (CC BY-NC-SA 4.0) prüfen, bevor es für kommerzielle Arbeiten ausgewählt wird.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>

## Durch diesen Stand abgelöst {#superseded-by-this}

- 2024-12-06: „Nur arXiv-Preprint“ ist als Statusbeschreibung veraltet; das Repository kennzeichnet Align3R als CVPR-2025-Highlight und stellt lauffähigen Code in Version 1.0.2 bereit.
- 2024-12-18: Für den interaktiven Space gibt es keine verifizierte Ersetzung oder Abkündigung; er bleibt eine sekundäre Demo-Route und ist kein reproduzierbarer lokaler Workflow.

## Weiterhin unbekannt {#still-unknown}

- Es wurde kein aktueller Nachweis zu GPU, Treiber, Modell-Download oder einer vollständigen Rekonstruktion erhoben; die Laufzeitkompatibilität und die Qualität bei einem Zielvideo sind daher unverifiziert.
- Die Versionskennzeichnung 1.0.2 im README identifiziert kein unveränderliches Paket oder Checkpoint-Bundle, da das Repository kein GitHub-Release-Artefakt hat.
- Die Reproduktion des MPI-Sintel-Benchmarks hat eine ungeklärte Mehrdeutigkeit bei der Aufteilung clean versus final, die in einem offenen Issue dokumentiert ist.
- Das offizielle README verlinkt denselben Hugging-Face-Space, daher scheinen die beiden datierten Einträge nicht unterschiedliche Gegenstände zu betreffen; ob der bereitgestellte Space-Code exakt dem Stand von main entspricht, ist nicht angegeben.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://arxiv.org/abs/2412.03079 | Align3R: Aligned Monocular Depth Estimation for Dynamic Videos — arXiv | 2026-09-04 |
| https://igl-hkust.github.io/Align3R.github.io/ | Align3R — offizielle Projektseite | 2026-09-04 |
| https://igl-hkust.github.io/Align3R.github.io/page1.html | Align3R — rekonstruierte Punktwolken | 2026-09-04 |
| https://github.com/jiah-cloud/Align3R | jiah-cloud/Align3R — offizielles Repository | 2026-09-04 |
| https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md | Align3R README — Branch main | 2026-09-04 |
| https://raw.githubusercontent.com/jiah-cloud/Align3R/main/demo.sh | Align3R Demo-Launcher — Branch main | 2026-09-04 |
| https://raw.githubusercontent.com/jiah-cloud/Align3R/main/tool/demo.py | Align3R Demo-Implementierung — Branch main | 2026-09-04 |
| https://huggingface.co/spaces/cyun9286/Align3R | Align3R — Hugging Face Space | 2026-09-04 |
| https://github.com/jiah-cloud/Align3R/releases | Align3R Releases | 2026-09-04 |
| https://github.com/jiah-cloud/Align3R/issues/27 | Align3R Issue #27 — Verwirrung um die Sintel-Aufteilung | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:align3r`, Thread `align3r`, 2 datierte Ereignisse 2024-12-06 → 2024-12-18.
- **Praktischer Hinweis:** Stand 2024-12-06 konnten Anwender Align3R-Projektmaterialien und Quellcode finden; Stand 2024-12-18 sollten sie zusätzlich den verlinkten Hugging-Face-Space auf einen gehosteten Projektzugang prüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Ablösungen oben als maßgeblich.

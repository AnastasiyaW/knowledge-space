---
title: "ARDY — Öffentliche Verfügbarkeit"
category: projects
date: 2026-07-15
tags: [ardy, project, public-availability]
aliases: ["ARDY"]
level: 2
source_sha256: a37db083f4cb6c1709fedc2d10adb712859fbab1fc038492f5d89aa2c11aae56
translation: machine
translated_at: '2026-10-24'
---
# ARDY — Öffentliche Verfügbarkeit {#ardy-public-availability}

**Entwicklungslinie:** `project:ardy` · Strang `public-availability`  
**Letztes Ereignis:** 2026-07-15 · 1 datiertes Ereignis seit 2026-07-15 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

ARDY ist ein autoregressives Diffusionssystem für Echtzeit-Bewegungen humanoider Figuren auf Core- und Unitree-G1-Rigs.

- Streaming-Textprompts: steuern die Figurenbewegung zur Laufzeit.
- Wurzelpfade und Wegpunkte: lenken die Trajektorie im Raum.
- Ganzkörper-Keyframes: legen Posen zu bestimmten Frames fest.
- Sparse Joint Constraints: fixieren einzelne Gliedmaßen während der Bewegung.

Es werden vier Checkpoints mit jeweils 326 Mio. Parametern ausgeliefert, und pro Ausgabe werden bis zu acht Sekunden Bewegung erzeugt. Einsatz für Prototypen und Integrationsarbeiten unter Linux mit NVIDIA-GPUs, nicht als Drop-in-Werkzeug für DCC-Animation.

## Entwicklungslinie {#development-line}

- **2026-07-15 — Öffentliche Projektressourcen zu ARDY wurden verlinkt.** Am 2026-07-15 wurde ARDY über die NVIDIA-Research-Projektseite, das Quell-Repository, die Hugging-Face-Collection und den interaktiven Hugging-Face-Space verlinkt. Die Links verbinden das Projekt mit seinen Einstiegspunkten für Forschung, Code, Modelle und praktische Erprobung. Allein die datierten Links belegen weder den genauen Ankündigungswortlaut noch Version, Funktionsumfang oder Veröffentlichungsstatus.

## Was sich geändert hat {#what-changed}

2026-07-15 — Die Projektseite von ARDY, der offizielle Code, die Checkpoint-Collection und die interaktive Demo wurden verfügbar; das Release umfasst Core- und Unitree-G1-Rigs und nicht ein einziges generisches Figurenmodell.

Am 2026-07-15 legt das verlinkte offizielle Repository vier am 2026-07-10 veröffentlichte Checkpoints fest: 20-FPS-Core-Modelle mit 8- oder 40-Frame-Horizont sowie 25-FPS-Unitree-G1-Modelle mit 8- oder 52-Frame-Horizont. Die NVIDIA-Modellkarte datiert den Core-Checkpoint mit 40-Frame-Horizont auf 2026-07-10, gibt 326 Mio. Parameter an und besagt, dass er auf 630 Stunden Bewegungserfassung aus Bones Rigplay 1 trainiert wurde.

2026-07-09 — Das begleitende ARDY-Paper wurde auf arXiv veröffentlicht; es beschreibt die hybride Root-Motion-/Body-Latent-Repräsentation und den zweistufigen Transformer-Denoiser. 2026-07-10 — NVIDIA veröffentlichte die vier vortrainierten Checkpoints unter der NVIDIA Open Model Agreement.

## So wird es verwendet {#how-to-use-this}

Stand 2026-07-15 ARDY über die Projektseite, das Quell-Repository, die Hugging-Face-Collection und den interaktiven Space evaluieren und dabei die unterstützten Workflows und Versionen direkt überprüfen.

1. Eine Python-3.10+-Umgebung unter Linux anlegen, einen CUDA-passenden PyTorch-Build installieren und danach ARDY installieren; das offizielle Setup wurde hauptsächlich auf Ubuntu 22.04 mit einer RTX 4090, Treiber 575 und Python 3.11 getestet.
  — <https://github.com/nv-tlabs/ardy>
2. Zugriff auf Meta-Llama-3-8B-Instruct beantragen und sich bei Hugging Face authentifizieren, da der Text-Encoder von ARDY von diesem gated Modell abhängt.
  — <https://github.com/nv-tlabs/ardy>
3. `python scripts/run_demo.py` ausführen, `http://localhost:2333` öffnen, einen Checkpoint laden und die Bewegung anschließend mit Text, Wegpunkten, Geschwindigkeitstasten oder kinematischen Constraints steuern.
  — <https://github.com/nv-tlabs/ardy>
4. Einen rig-spezifischen Checkpoint wählen: Core für das Figuren-Rig mit 27 Gelenken oder G1 für Unitree G1; dabei die angegebene FPS-Rate und den Horizont beachten, statt die Varianten als austauschbar zu behandeln.
  — <https://huggingface.co/nvidia/ARDY-Core-RP-20FPS-Horizon40>

## Best Practices {#best-practices}

- PyTorch vor ARDY installieren, damit der CUDA-Build zu GPU und Treiber passt; das TensorRT-Extra nur verwenden, wenn dessen Treiber- und Paketindex-Anforderungen erfüllt sind.
  — <https://github.com/nv-tlabs/ardy>
- Nachbearbeitung zunächst deaktiviert lassen: Sie kann Fußgleiten reduzieren und die Einhaltung von Constraints verbessern, ist aber langsamer und standardmäßig deaktiviert.
  — <https://github.com/nv-tlabs/ardy>
- Die Länge der History aufgabenabhängig festlegen: kürzere History passt sich an geänderte Prompts oder Constraints schneller an; längere History verbessert die semantische Kontinuität und die Übergänge.
  — <https://github.com/nv-tlabs/ardy>
- Eine anwendungsspezifische Integration vor dem Deployment validieren; die Modellkarte nennt Linux sowie NVIDIA Ampere, Hopper und Blackwell als unterstützte Umgebungen.
  — <https://huggingface.co/nvidia/ARDY-Core-RP-20FPS-Horizon40>

## Hierdurch abgelöst {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Der gehostete Hugging-Face-Space konnte während der Recherche nicht abgerufen werden; seine aktuelle Verfügbarkeit und Oberfläche wurden daher nicht überprüft.
- Für die Veröffentlichung vom 2026-07-15 selbst wurde kein datierter Release-Hinweis gefunden; das Ereignis vom 15. Juli wird durch die offiziellen Seiten von Projekt, Repository und Modell belegt, während die Veröffentlichungsdaten der Checkpoints ausdrücklich mit 2026-07-10 angegeben sind.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://research.nvidia.com/labs/sil/projects/ardy/ | ARDY: Interactive Human Motion Generation | 2026-09-05 |
| https://github.com/nv-tlabs/ardy | Offizielle Implementierung von ARDY | 2026-09-05 |
| https://huggingface.co/collections/nvidia/ardy | ARDY — NVIDIA-Collection | 2026-09-05 |
| https://huggingface.co/nvidia/ARDY-Core-RP-20FPS-Horizon40 | Modellkarte ARDY-Core-RP-20FPS-Horizon40 | 2026-09-05 |
| https://arxiv.org/abs/2607.08741 | ARDY: Autoregressive Diffusion with Hybrid Representation for Interactive Human Motion Generation | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:ardy`, Strang `public-availability`, 1 datiertes Ereignis 2026-07-15 → 2026-07-15.
- **Praktischer Hinweis:** Stand 2026-07-15 sollten Praktiker die Projektseite von ARDY, das Quell-Repository, die Hugging-Face-Collection und den interaktiven Space gemeinsam als Ausgangspunkte für Evaluation oder Erprobung des Projekts nutzen und dabei den genauen unterstützten Workflow und die Versionen eigenständig überprüfen.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

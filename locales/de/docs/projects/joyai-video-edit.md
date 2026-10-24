---
title: "JoyAI-Video-Edit"
category: projects
date: 2026-08-06
tags: [joyai-video-edit, joyai-video-edit-public-reference, joyai_video_edit, project]
aliases: ["JoyAI-Video-Edit"]
level: 2
source_sha256: 6181d24f08bad7193eb9b7174ba2d4fcb382ff4e3f9b26f5e301794a410f5269
translation: machine
translated_at: '2026-10-24'
---
# JoyAI-Video-Edit {#joyai-video-edit}

**Entwicklungslinie:** `project:joyai-video-edit` · Thread `joyai-video-edit-public-reference`  
**Letztes Ereignis:** 2026-08-06 · 1 datiertes seit 2026-08-06 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

JoyAI-Video-Edit: ein Apache-2.0-lizenzierter, autoregressiv-diffusiver Video-Editor mit 16B Parametern für kausale, Live-Video-zu-Video-Bearbeitungen.

- Text-, lokale, Hintergrund-, Stil-, Bewegungs- und Referenzbild-Bearbeitungen.
- Live-Kamera- oder hochgeladene Videoeingabe über WebSocket.
- Angegebener Benchmark: 720p mit etwa 30 FPS auf einer Nvidia B200; die Konfiguration für Consumer-GPUs liegt bei 840×480 mit 24 FPS auf einer RTX 5090.

## Entwicklungslinie {#development-line}

- **2026-08-06 — Öffentliche Projektreferenzen zu JoyAI-Video-Edit erfasst.** Am 2026-08-06 erschienen öffentliche Links zu einem GitHub-Repository, einer Hugging-Face-Seite und einer JoyAI-Labs-Website. Die Referenzen zeigen laufende Arbeit, nennen aber keine konkrete Release-Version, keine Funktion und keinen Launch-Status.

## Was sich geändert hat {#what-changed}

- 2026-08-06 — Deployment-Code, Checkpoints und ein technischer Bericht veröffentlicht; der initiale DiT-Checkpoint war `joyai_video_edit_dit_0804.pth`.
- 2026-08-14 — Der DiT-Checkpoint `joyai_video_edit_dit_0811.pth` ersetzte den initialen Checkpoint für das Serving und verbesserte die referenzbildgeführte Bearbeitung.
- 2026-08-15 — Eine Live-Demo auf Hugging Face auf RTX-PRO-6000-Hardware wurde verfügbar.
- 2026-08-24 — Die offizielle Unterstützung für Consumer-GPUs wurde um eine RTX-5090-Konfiguration mit 840×480 und 24 FPS erweitert.

## So wird es verwendet {#how-to-use-this}

Stand 2026-08-06: Bevor JoyAI-Video-Edit eingesetzt wird, sollten die öffentlichen Code-, Modellverteilungs- und offiziellen Web-Referenzen geprüft werden, um den genauen Release-Stand und die Nutzungshinweise zu verifizieren.

1. Repository klonen, eine Python-3.10-Conda-Umgebung anlegen und danach `deploy/requirements.txt` installieren.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit>
2. Die im Repository enthaltene CUDA-Erweiterung `joyomni_ops` bauen; für Blackwell-Hardware wird CUDA nvcc 12.8 oder neuer benötigt.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>
3. `joyai_video_edit_dit_0811.pth`, die VAE-Dateien und den erforderlichen MiMo-VL-Encoder in die dokumentierte Checkpoint-Struktur herunterladen.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>
4. GPU-spezifische Umgebungsvariablen setzen und `bash deploy/run_server.sh` ausführen; Port 8080 öffnen oder per SSH weiterleiten.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>

## Best Practices {#best-practices}

- Den aktuellen DiT-Checkpoint `0811` verwenden; `0804` wird nur zur Reproduzierbarkeit aufbewahrt und ist nicht der Server-Standard.
  — <https://huggingface.co/jdopensource/JoyAI-Video-Edit>
- Wenn ein Checkout gemeinsam genutzt wird, jedem GPU-Modell ein eigenes `JOYOMNI_CACHE_ROOT` zuweisen und die dokumentierten GPU-spezifischen Auflösungs- und FPS-Einstellungen verwenden.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>
- SageAttention nur auf der RTX 5090 verwenden; auf RTX PRO 6000 und B200 deaktiviert lassen. Den Low-VRAM-Modus auf Karten mit 48 GB oder weniger aktivieren.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>

## Dadurch ersetzt {#superseded-by-this}

- 2026-08-14 — `joyai_video_edit_dit_0804.pth` wird für das Serving durch `joyai_video_edit_dit_0811.pth` ersetzt; der erstgenannte wird nur zur Reproduzierbarkeit aufbewahrt.

## Noch unbekannt {#still-unknown}

- Die ursprüngliche Demo-URL von JoyAI Labs konnte in dieser Recherche nicht abgerufen werden, daher ist ihre aktuelle Verfügbarkeit nicht verifiziert.
- Der angegebene Durchsatz stammt aus einem Benchmark des Herstellers und ist kein unabhängig reproduziertes Leistungsergebnis.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/jd-opensource/JoyAI-Video-Edit | JoyAI-Video-Edit official repository | 2026-09-05 |
| https://huggingface.co/jdopensource/JoyAI-Video-Edit | jdopensource/JoyAI-Video-Edit model card | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md | JoyAI-Video-Edit Deployment Guide | 2026-09-05 |
| https://arxiv.org/abs/2608.03974 | JoyAI-Video-Edit: Real-Time Open-Ended Video Editing with Autoregressive Diffusion | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:joyai-video-edit`, Thread `joyai-video-edit-public-reference`, 1 datiertes Ereignis 2026-08-06 → 2026-08-06.
- **Praxishinweis:** Stand 2026-08-06 sollten Praktiker JoyAI-Video-Edit so behandeln, als gäbe es öffentliche Code-, Modellverteilungs- und offizielle Web-Referenzen; den genauen Release-Stand und die Nutzungshinweise sollten sie vor dem Einsatz an diesen Quellen verifizieren.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise sind maßgeblich dafür, was veraltet ist.

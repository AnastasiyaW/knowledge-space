---
title: "DEMON"
category: projects
date: 2026-06-03
tags: [demon, project]
aliases: ["DEMON"]
level: 3
source_sha256: 4e07a151f080c0b7c7fc47ee1ebd16d9f2d2d24dd02cad902b60f4b1099362a6
translation: machine
translated_at: '2026-10-24'
---
# DEMON {#demon}

**Entwicklungsstrang:** `project:demon` · Thread `demon`  
**Letztes Ereignis:** 2026-06-03 · 1 datiertes Ereignis seit 2026-06-03 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

DEMON macht ACE-Step v1.5 zu einem Live-Musikgenerator und -Transformer auf GPU. Es ist das Audio-Pendant zu StreamDiffusion für Performer, Entwickler kreativer Werkzeuge und Forscher.

- Ring-Buffer-Diffusion streamt fertiges Audio, während sich Quellaudio, Prompts, LoRAs und Kurven während der Wiedergabe ändern.
- Die Weboberfläche stellt Prompt-Blending, Klangfarben- und Strukturreferenzen, Automatisierung, MIDI-Zuordnung, Aufnahme und eine Session-API bereit.

## Entwicklungsstrang {#development-line}

- **2026-06-03 — Öffentlicher DEMON-Ressourcensatz dokumentiert.** Das Kernprojekt hatte keinen GitHub-Releases-Eintrag. Der separat versionierte TouchDesigner-Client demonTD veröffentlichte v0.2.11 und v0.2.12 mit Korrekturen für gehostete Sitzungen und das Socket-Protokoll.

## Was sich geändert hat {#what-changed}

- 2026-04-22: DreamVAE wurde als eigenständiges ACE-Step-Decoder-Asset veröffentlicht.
- 2026-05-27: Das DEMON-Paper veröffentlichte den Ring-Buffer und die TensorRT-Laufzeit mit Messungen auf einer RTX 5090.
- 2026-06-02: DreamVAE wurde als Teil der DEMON-Forschung eingeordnet, bleibt aber ein reines Decoder-Asset.
- 2026-06-03: Das Kernprojekt hatte keinen GitHub-Releases-Eintrag; der separat versionierte TouchDesigner-Client demonTD veröffentlichte v0.2.11 und v0.2.12 mit Korrekturen für gehostete Sitzungen und das Socket-Protokoll.
- 2026-06-04: demonTD v0.2.13 ergänzte eine Auswahl des Audio-Ausgabegeräts.
- 2026-06-09: demonTD v0.2.15 ergänzte die automatische Behandlung von LoRA-Triggern und die Verdrahtung von Prompt B. demonTD v0.2.16 verlagerte die Taktsteuerung vom UI-Thread, um ruckelndes Audio zu beheben.
- 2026-06-11: demonTD v0.2.17 fasste Korrekturen für Verbindung und Audio-Übersprechen zusammen und dokumentierte die Installation über ein Bundle.

## Verwendung {#how-to-use-this}

1. Für einen Test ohne Installation die gehostete Instanz unter music.daydream.live öffnen; dies ist der angegebene Weg für Nutzer ohne lokale GPU.
  — <https://huggingface.co/daydreamlive/DEMON>
2. Für einen lokalen Web-Workflow eine NVIDIA-GPU, uv und etwa 40 GB freien Speicherplatz verwenden. daydreamlive/DEMON klonen, `uv sync` ausführen und `uv run demon-setup` starten, um unterstützte ACE-Step-v1.5-Assets zu beziehen und minimale TensorRT-Engines zu bauen.
  — <https://github.com/daydreamlive/DEMON>
3. `uv run python -u -m demos.realtime_motion_graph_web.run` starten und http://localhost:6660 öffnen. Wurden Engines beim Setup übersprungen, `-- --accel compile` statt des standardmäßigen All-TensorRT-Starts verwenden.
  — <https://github.com/daydreamlive/DEMON>
4. Quellaudio, Prompts und optionale Referenzen in der Weboberfläche laden. Prompt-Blending, Stärke, LoRAs, Kurven, MIDI oder Aufnahme je nach Performance-Ziel einsetzen.
  — <https://huggingface.co/daydreamlive/DEMON>
5. Kompatible optionale LoRAs als .safetensors-Dateien unter $ACESTEP_MODELS_DIR/loras/ ablegen (Standard: ~/.daydream-scope/models/demon/loras/) und ihre Stärke in der laufenden Sitzung anpassen.
  — <https://huggingface.co/daydreamlive/DEMON>

## Bewährte Praktiken {#best-practices}

- Die mitgelieferten ACE-Step-v1.5-Checkpoints und das DEMON-Setup zusammenhalten; keine beliebigen Checkpoints oder Pfade für eine TensorRT-Konfiguration ersetzen, die das festgelegte Modelllayout erwartet.
  — <https://github.com/daydreamlive/DEMON>
- Mit dem TensorRT-Windowed-VAE-Decoder plus einem kompilierten Decoder beginnen, um einen vollständigen Engine-Build zu vermeiden; dies ist der dokumentierte kostengünstige Weg zum Streaming-Decoding.
  — <https://huggingface.co/daydreamlive/DEMON>
- TensorRT-Pläne nach einem Wechsel von GPU, CUDA, Treiber oder TensorRT-Version neu erstellen, da Pläne hardware- und versionsspezifisch sind.
  — <https://github.com/daydreamlive/DEMON>
- Änderungen an Prompt, Quelle und skalarem Denoise-Wert als ringgepufferte Steuerungen behandeln: Änderungen bewusst vornehmen und das Audio erst nach der Ausbreitung beurteilen, statt zu erwarten, dass alle Steuerungen im selben Takt hörbar werden.
  — <https://daydreamlive.github.io/DEMON/>
- Bei separater Nutzung von DreamVAE dessen Decoder mit dem Standard-Encoder von ACE-Step kombinieren; nur der Decoder ist destilliert.
  — <https://huggingface.co/daydreamlive/DreamVAE>
- Für die TouchDesigner-Integration die Release-ZIP installieren, wobei demonTD.tox neben seinem Vendor-Verzeichnis liegt; die nackte .tox-Datei ist nur für eine Installation gedacht, die bereits passende Abhängigkeiten hat.
  — <https://github.com/daydreamlive/demonTD>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-06-04: Für demonTD sind Anleitungen obsolet, die Edit -> Preferences -> Audio -> Audio Device -> None verwenden. demonTD v0.2.13 erklärt, dass diese Einstellung nicht existiert, und stellt eine Auswahl des Audio-Ausgabegeräts bereit. Quelle: https://github.com/daydreamlive/demonTD/releases
- 2026-06-09: Für demonTD ist die Annahme obsolet, dass ein ausgewähltes LoRA ohne sein Trigger-Wort automatisch wirksam ist. demonTD v0.2.15 stellt gespeicherte primäre Trigger voran und sendet den Prompt erneut, wenn sich das LoRA ändert. Quelle: https://github.com/daydreamlive/demonTD/releases

## Weiterhin unbekannt {#still-unknown}

- Kein offizieller GitHub-Release des Kern-Engines kennzeichnet den 2026-06-03 als versionierte DEMON-Veröffentlichung. Dieses Datum sollte nicht als Veröffentlichungsdatum eines Kernmodells oder einer Kernlaufzeit behandelt werden.
- Die Civitai-URL https://civitai.com/models/2416425/acestep-loras lieferte während der Recherche keine überprüfbare Modellkarte. Genaue Dateien, Versionen, Daten, Trigger und die Kompatibilität mit DEMON sind unbestätigt; diese LoRAs sollten als optionale externe Assets und nicht als Standardabhängigkeit behandelt werden.
- Die veröffentlichte Lizenz des Kerncodes ist AGPL-3.0-or-later, während die Hugging-Face-Karte von DEMON und die Projektseite MIT angeben. Die Quellen klären diesen Unterschied nicht; vor Änderungen, Netzwerkbereitstellung oder Weitergabe die anwendbare Distributionslizenz bestätigen.
- Die Daydream-Projektseite bezeichnet die XL-Turbo-Basis als 5B, während das ACE-Step-Upstream-Repository dessen XL-DiT als 4B angibt. Die Quellen erklären die Abweichung der Parameterzahl nicht.
- Leistungsangaben sind vom Autor berichtete Messungen auf einer RTX 5090 unter den genannten Einstellungen für 60 Sekunden, TensorRT, Tiefe und Schritte. Es wurde kein unabhängiger Benchmark über verschiedene Hardware und keine allgemeingültige Latenz- oder VRAM-Untergrenze gefunden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://daydreamlive.github.io/DEMON/ | DEMON: Diffusion Engine for Musical Orchestrated Noise | 2026-09-06 |
| https://music.daydream.live/ | Daydream Demo | 2026-09-06 |
| https://github.com/daydreamlive/DEMON | daydreamlive/DEMON | 2026-09-06 |
| https://github.com/daydreamlive/DEMON/releases | Releases · daydreamlive/DEMON | 2026-09-06 |
| https://huggingface.co/daydreamlive/DEMON | daydreamlive/DEMON model card | 2026-09-06 |
| https://arxiv.org/abs/2605.28657 | DEMON: Diffusion Engine for Musical Orchestrated Noise | 2026-09-06 |
| https://huggingface.co/daydreamlive/DreamVAE | daydreamlive/DreamVAE model card | 2026-09-06 |
| https://huggingface.co/daydreamlive/DreamVAE/commit/53e74f7ed07cd053680fc2aa2b072124c63528d0 | DreamVAE initial release | 2026-09-06 |
| https://huggingface.co/daydreamlive/DreamVAE/commit/abb4c6d9913df0aedd685fed2e2f5aef3d742707 | DreamVAE: add links to paper, project page, and code repository | 2026-09-06 |
| https://github.com/daydreamlive/demonTD | daydreamlive/demonTD | 2026-09-06 |
| https://github.com/daydreamlive/demonTD/releases | Releases · daydreamlive/demonTD | 2026-09-06 |
| https://huggingface.co/ACE-Step/Ace-Step1.5 | ACE-Step/Ace-Step1.5 model card | 2026-09-06 |
| https://github.com/ACE-Step/ACE-Step-1.5 | ACE-Step/ACE-Step-1.5 | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:demon`, Thread `demon`, 1 datiertes Ereignis 2026-06-03 → 2026-06-03.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Verwendung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was obsolet ist.

---
title: "ATI: Any Trajectory Instruction"
description: "ATI ergänzt seinen auf Wan2.1 basierenden Image-to-Video-Workflow um trajektoriengesteuerte Steuerung von Objekt-, lokaler und Kamerabewegung; die veröffentlichten Grenzen von Modell, Checkpoint und localhost-Editor sind beizubehalten."
category: models
tags: [video-generation, trajectory-control, camera-motion, object-motion, wan2.1, bytedance]
aliases: ["Any Trajectory Instruction"]
level: 2
source_sha256: 3ea3a8ff458dfca565fec3085f33723645859c13a62c17231e465aad5fecdd09
translation: machine
translated_at: '2026-10-24'
---
# ATI: Any Trajectory Instruction {#ati-any-trajectory-instruction}

**Geprüfter Stand: 2026-09-04.** ATI ist die veröffentlichte Trajektorien-Steuerungserweiterung von ByteDance für die Bild-zu-Video-Generierung. Objekt-, lokale und Kamerabewegungen werden als Trajektorien dargestellt, und das resultierende Bewegungssignal wird in den Wan2.1-Image-to-Video-Workflow eingespeist. Die offizielle Implementierung ist eine spezifische, auf Wan2.1 basierende Integration und kein generisches Steuerungsmodul für beliebige Videomodelle.

## Was gesteuert wird {#what-it-controls}

ATI verwendet Punkttrajektorien, um mehrere Bewegungsabsichten über eine einheitliche Schnittstelle auszudrücken:

- **Objektbewegung** — Trajektorien, die am Motiv oder an einem lokalen Bereich verankert sind;
- **lokale Bewegung** — gerichtete Bewegung für ausgewählte Bildbereiche;
- **Kamerabewegung** — koordinierte Pfade wie Schwenk und Zoom;
- **Bewegungsübertragung** — Extraktion von Tracks aus einem Quellvideo und Anwendung auf ein neues Erstbild.

Das Ergebnis hängt weiterhin vom Basismodell, vom ersten Bild, vom Prompt, von der Platzierung der Trajektorien und von der Bewegungsgeschwindigkeit ab. Ein gezeichneter Pfad ist eine Anweisung, keine Garantie, dass verdeckte oder mehrdeutige Bildbereiche physikalisch konsistent bleiben.

## Veröffentlichte Laufzeitgrenze {#published-runtime-boundary}

Das offizielle Repository basiert auf der Wan2.1-Implementierung. Der Installationsleitfaden setzt das originale `Wan2.1-I2V-14B-480P`-Modell, einen separaten ATI-Checkpoint sowie das Kopieren des originalen VAE, des Text-Encoders und weiterer erforderlicher Komponenten in den ATI-Checkpoint-Pfad voraus. Diese Artefakte und ihre Revisionen sind gemeinsam in einem unveränderlichen Lauf-Protokoll festzuhalten.

Vor der Verwendung ist zu prüfen:

1. die ATI-Repository-Revision und die dazu passende Wan2.1-Umgebung;
2. die Vollständigkeit des Checkpoints und die lokalen Pfade;
3. das YAML-/Eingabeformat, das im aktuellen Beispiel oder API-Wrapper verwendet wird;
4. der verfügbare GPU-Speicher, die Videolänge, die Auflösung und der Ausgabeort;
5. eine kleine, bekannte Trajektorie als Testfall, bevor ein größerer Renderstapel gestartet wird.

Es gibt Community-Unterstützung für ComfyUI über Drittanbieter-Nodes. Diese ist als eigenständige Integration mit eigener Version, eigenen Sicherheits- und Ausgabeprüfungen zu behandeln; sie ist kein austauschbarer Nachweis für das Upstream-Repository.

## Sicherheit des Trajektorien-Editors {#trajectory-editor-safety}

Das Upstream-Projekt weist Betreiber ausdrücklich an, seinen interaktiven Trajektorien-Editor auf localhost auszuführen. Diese Entwicklungsschnittstelle ist nicht direkt in einem nicht vertrauenswürdigen Netzwerk freizugeben. Wird ein entfernter Workflow benötigt, sind Authentifizierung, eine eingeschränkte Upload-Oberfläche, Isolation pro Job, Ressourcenlimits und aufbewahrte Job-Belege vorzuschalten.

## Abnahmeprüfungen {#acceptance-checks}

Für jede Ausgabe ist zu prüfen, ob sich das vorgesehene Motiv bewegt hat, ob statische Bereiche stabil geblieben sind, ob die gewünschte Kamerabewegung stattgefunden hat und ob bei der finalen Wiedergabegröße Artefakte auftreten. Quellbild, Trajektoriendatei, Prompt, Basis- und ATI-Revisionen, Einstellungen, Ausgabe und Prüfergebnis sind aufzubewahren. Nach einem Upgrade von ATI oder Wan ist ein begrenzter Testfall erneut auszuführen.

Das ATI-Repository steht unter der Apache-2.0-Lizenz, das Wan-Basismodell, die Checkpoints und etwaige Community-Wrapper können jedoch eigenen Bedingungen unterliegen. Die aktuelle Lizenz und die Zugangsbedingungen jedes Artefakts sind zu prüfen.

## Referenzen {#references}

- [ATI official repository](https://github.com/bytedance/ATI)
- [ATI paper](https://arxiv.org/abs/2505.22944)
- [ATI checkpoint collection](https://huggingface.co/bytedance-research/ATI)
- [Community ComfyUI Wan Video Wrapper](https://github.com/kijai/ComfyUI-WanVideoWrapper)

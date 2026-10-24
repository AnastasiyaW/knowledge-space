---
title: "ID-V2V — Öffentliche Projektressourcen"
category: projects
date: 2026-07-30
tags: [id-v2v, project, public-project-resources]
aliases: ["ID-V2V"]
level: 2
source_sha256: 741e2bfe3394c68138389baed6891dc5cde4acaed5eed4649a49bea704c54cb0
translation: machine
translated_at: '2026-10-24'
---
# ID-V2V — Öffentliche Projektressourcen {#id-v2v-public-project-resources}

**Entwicklungslinie:** `project:id-v2v` · Thread `public-project-resources`  
**Letztes Ereignis:** 2026-07-30 · 1 datiertes seit 2026-07-30 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

ID-V2V ist eine Open-Source-Forschungspipeline auf Basis von Wan2.1 I2V-14B-720P und VACE für Videoeditoren. Sie wandelt Quellvideo, ein stilisiertes erstes Bild, optionale Keyframes und einen Textprompt in ein neues Video um und bewahrt dabei menschliches Erscheinungsbild, Mimik, Blickrichtung und Bewegung.

- Restyling überträgt ein neues visuelles Erscheinungsbild auf das Material.
- Relighting passt die Szenenbeleuchtung an und erhält dabei die Identität.
- Mehrfigurenverarbeitung bearbeitet mehrere Personen in derselben Szene.
- Zusätzliche Keyframes steuern die Erzeugung von Zwischenfiguren.
- Langvideoverarbeitung teilt längere Sequenzen auf mehrere Clips auf.

Die Generierung läuft in 720p, die Basisgewichte und Abhängigkeiten benötigen etwa 96 GB, und die Testumgebung des Autors ist 8× A100 80GB. Dies ist ein schwergewichtiges Forschungsartefakt für lokale, reproduzierbare Inferenz, kein Produktionsdienst.

## Entwicklungslinie {#development-line}

- **2026-07-30 — Öffentliche Projektressourcen von ID-V2V wurden verlinkt.** Der offizielle Code definiert das Eingabeverzeichnis, den Ablauf von Preprocessing zu Generierung und die 720p-Generierung. Er verarbeitet Clips mit mehr als 81 Frames über überlappende Fenster. Er stellt Rezepte für Restyling, Relighting und Keyframes bereit. Ein Model-Card-Update vom 2026-07-29 nennt die Basisarchitektur als Wan 2.1 Image-to-Video mit VACE-Steuerung. Die Gewichte sind nur für Demonstration und Inspiration gedacht.

## Was sich geändert hat {#what-changed}

2026-07-24 — Das arXiv-Paper „ID-V2V: Identity-Preserving Video Restylization“ wurde veröffentlicht. Es beschreibt die Trennung von keyframegesteuerter Synthese und quellbasierter Identitätserhaltung durch Relighting. 2026-07-29 — Hugging Face veröffentlichte zwei feinabgestimmte, nicht kompatible Checkpoints: den empfohlenen `idv2v.pth` mit einer SAM3-Bedingung Vordergrund-auf-Grau und `idv2v_with_normal_depth.pth` mit zusätzlichen Normal- und Tiefensteuerungen. 2026-07-30 — Das Release wurde praktisch reproduzierbar: Der offizielle Code definiert ein Eingabeverzeichnis, einen Ablauf von Preprocessing zu Generierung, 720p-Generierung, die Verarbeitung von Clips mit mehr als 81 Frames über überlappende Clips sowie Rezepte für Restyling, Relighting und Keyframes. Ein Model-Card-Update vom 2026-07-29 nennt die Basisarchitektur als Wan 2.1 Image-to-Video mit VACE-Steuerung, wobei die Gewichte nur für Demonstration und Inspiration gedacht sind.

## Wie man das nutzt {#how-to-use-this}

Ab dem 2026-07-30 sollten Praktiker die Evaluierung oder Reproduktion von ID-V2V über die verlinkte offizielle Projektseite, das Quell-Repository und die Hugging-Face-Seite beginnen und dort vor der Nutzung exakte Fähigkeiten und Release-Status prüfen.

1. Klonen Sie das Repository, erstellen Sie mit `uv sync` eine einheitliche Umgebung, aktivieren Sie sie und melden Sie sich früh bei Hugging Face an, da SAM3 einen Zugang mit Freigabe erfordert.
  — <https://github.com/Eyeline-Labs/ID-V2V>
2. Laden Sie Standard-Checkpoints und Abhängigkeiten mit `bash scripts/download_checkpoints.sh` herunter; ergänzen Sie `--with-depth` für die Variante mit Normal- und Tiefenkarte.
  — <https://github.com/Eyeline-Labs/ID-V2V>
3. Bereiten Sie ein Verzeichnis mit `source.mp4`, `stylized_first_frame.png` und `prompt.txt` vor; ergänzen Sie bei Bedarf `keyframes/<frame_number>.png`.
  — <https://github.com/Eyeline-Labs/ID-V2V>
4. Für das Standardmodell führen Sie das Preprocessing mit dem SAM3-Textprompt aus und starten danach die Inferenz; Relighting nutzt einen separaten Pfad ohne Preprocessing.
  — <https://github.com/Eyeline-Labs/ID-V2V>
5. Für langes Quellmaterial fügen Sie Keyframes hinzu und verwenden das Rezept für Langvideos: Das System verbindet Clips über überlappende Grenzframes.
  — <https://github.com/Eyeline-Labs/ID-V2V>

## Bewährte Vorgehensweisen {#best-practices}

- Ordnen Sie jeden Checkpoint dem passenden Varianten-Skript zu: Passende Architektur erzeugt bei einem ungültigen Paar keinen Fehler, aber die Ausgabe verschlechtert sich unbemerkt.
  — <https://huggingface.co/Eyeline-Labs/ID-V2V>
- Verwenden Sie bei langen Videos mehr Keyframes, damit die Abweichung zwischen Clips gering bleibt.
  — <https://github.com/Eyeline-Labs/ID-V2V>
- Behandeln Sie Ergebnisse als experimentell und prüfen Sie Identitätserhalt, Gesichtsausdrücke und Lippensynchronität an eigenem Material, bevor Sie in der Produktion einsetzen.
  — <https://huggingface.co/Eyeline-Labs/ID-V2V>

## Hierdurch ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Das bereitgestellte Schema lässt `event_findings` und `new_events` aus; ihre überprüfbaren Details stehen in `what_changed`.
- Offizielle Materialien beschreiben reproduzierbare Inferenz, enthalten aber keine bestätigte Produktionsunterstützung, keine öffentlich gehostete API und keine minimalen GPU-Anforderungen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://eyeline-labs.github.io/ID-V2V/ | ID-V2V: Identity-preserving Video Restylization | 2026-09-05 |
| https://github.com/Eyeline-Labs/ID-V2V | Eyeline-Labs/ID-V2V | 2026-09-05 |
| https://huggingface.co/Eyeline-Labs/ID-V2V | Eyeline-Labs/ID-V2V | 2026-09-05 |
| https://arxiv.org/abs/2607.22830 | ID-V2V: Identity-Preserving Video Restylization | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:id-v2v`, Thread `public-project-resources`, 1 datiertes Ereignis 2026-07-30 → 2026-07-30.
- **Praktischer Hinweis:** Ab dem 2026-07-30 sollten Praktiker die Evaluierung oder Reproduktion von ID-V2V über die verlinkte offizielle Projektseite, das Quell-Repository und die Hugging-Face-Seite beginnen und dort vor der Nutzung exakte Fähigkeiten und Release-Status prüfen.
- **Konfidenz:** hoch. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

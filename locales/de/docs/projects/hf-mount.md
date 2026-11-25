---
title: "hf-mount"
category: projects
date: 2026-03-25
tags: [hf-mount, hf-mount-development, hf_mount, project]
aliases: ["hf-mount"]
level: 3
source_sha256: 26492c9516cf5a813229c05a16c0d0f5b15ed900a61881d3e3a6d6be2efeab95
translation: machine
translated_at: '2026-10-24'
---
# hf-mount {#hf-mount}

**Entwicklungslinie:** `project:hf-mount` · Thread `hf-mount-development`  
**Letztes Ereignis:** 2026-03-25 · 1 datiertes Ereignis seit 2026-03-25 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

hf-mount ist eine Rust-CLI für Entwickler und ML-Infrastruktur, um Hugging-Face-Speicher in lokale Dateisysteme einzuhängen.

- Hugging-Face-Buckets, eingehängt mit Schreibzugriff über NFS oder FUSE.
- Modell- und Datensatz-Repositories, schreibgeschützt eingehängt, wobei Dateien beim ersten Zugriff geladen werden.

Repositories bleiben schreibgeschützt, und Änderungen auf dem Remote-Speicher werden unter FUSE innerhalb von 10 Sekunden und unter NFS innerhalb von 30 Sekunden übernommen. Wir setzen es für leseintensive ML-Aufgaben auf knappen Datenträgern ein, nicht jedoch für Schreibvorgänge mehrerer Benutzer, maschinenübergreifendes Locking oder latenzkritische zufällige I/O.

## Entwicklungslinie {#development-line}

- **2026-03-25 — Das hf-mount-Repository von Hugging Face wurde öffentlich referenziert.** Am 2026-03-25 hat diese Entwicklungslinie einen Link auf das GitHub-Repository hf-mount von Hugging Face erfasst. Aus dem datierten Link allein lässt sich nur ableiten, dass das Projekt an diesem Datum öffentlich referenziert wurde; eine Aussage über Veröffentlichung, Funktion oder Nutzung ist damit nicht belegt.

## Was sich geändert hat {#what-changed}

2026-03-25 — hf-mount wurde verfügbar, um Hub-Modelle, Datensätze und Storage Buckets an einem lokalen Pfad einzuhängen; Buckets unterstützen Schreibzugriff, Repositories bleiben schreibgeschützt.

Eine offizielle Ankündigung vom 2026-03-24 klärt den Umfang für den Start am 2026-03-25: Nutzer können Remote-Speicher anbinden, der laut Angabe bis zu 100-mal so groß wie die lokale Festplatte sein kann; dies ist kein neues Release am 25. März, sondern eine Präzisierung des ursprünglichen Starts.

Neue Ereignisse:
- 2026-06-10 — v0.7.0 ergänzte die JSON-Log-Formatierung und behob Probleme beim Herunterfahren von FUSE/NFS, die Pods zum Hängen brachten.
- 2026-07-08 — v0.9.0 begrenzte die Dauer von Remote-Chunk-Lesevorgängen, senkte das CAS-Lese-Timeout auf 30 Sekunden und machte FUSE-`link()` zu einer serverseitigen Kopie.
- 2026-08-14 — v0.9.2 behob Phantomverzeichnisse bei Baumübereinstimmungen mit Raw-Präfix, URL-Kodierung von Pfaden und die Unterstützung des object_store-Writers.

## So wird es verwendet {#how-to-use-this}

Stand 2026-03-25 können Praktiker das GitHub-Repository hf-mount als Ausgangspunkt für die Evaluierung des Projekts nutzen; Funktionsumfang und Reife sollten dabei anhand der primären Dokumentation überprüft werden.

1. Installation über Homebrew unter macOS/Linux oder Download des Binärpakets für Linux x86_64/aarch64 bzw. macOS Apple Silicon.
  — <https://github.com/huggingface/hf-mount>
2. Ein öffentliches Modell oder einen Datensatz als schreibgeschützten Pfad einhängen: `hf-mount start repo openai-community/gpt2 /tmp/gpt2`; für eine private Ressource `HF_TOKEN` oder `--hf-token` übergeben.
  — <https://huggingface.co/docs/hub/main/models-downloading>
3. Für veränderliche Checkpoints, Logs und Artefakte einen Bucket einhängen: `hf-mount start --hf-token $HF_TOKEN bucket username/my-bucket /mnt/data`.
  — <https://huggingface.co/docs/hub/storage-buckets-access>
4. Mounts mit `hf-mount status` prüfen und mit `hf-mount stop <mount-path>` beenden; Logs liegen unter `~/.hf-mount/logs/`.
  — <https://github.com/huggingface/hf-mount>

## Bewährte Vorgehensweisen {#best-practices}

- Standardmäßig NFS verwenden: Es erfordert weder Root-Rechte, Kernel-Erweiterungen noch systemseitige FUSE-Abhängigkeiten; FUSE wählen, wenn eine engere Integration mit Kernel-Cache und Metadaten wichtig ist.
  — <https://github.com/huggingface/hf-mount>
- Den Mount nicht als verteiltes Dateisystem verwenden: Es gibt keine clientübergreifenden Sperren, gleichzeitige Schreibvorgänge werden nicht auf Konflikte geprüft, und veraltete Ansichten können bis zum Polling-Intervall bestehen bleiben.
  — <https://github.com/huggingface/hf-mount>
- Für interaktives Bearbeiten `--advanced-writes` aktivieren: Der Streaming-Modus blockiert übliche Unlink-und-Create-Speichervorgänge von Editoren und verwirft den Puffer bei einem Absturz vor `close()`.
  — <https://github.com/huggingface/hf-mount>
- Für HF Jobs und Spaces verwaltete Volume-Mounts bevorzugen, sofern kein eigenständiger Host-Mount benötigt wird.
  — <https://huggingface.co/docs/hub/storage-buckets-access>

## Durch Folgendes ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Der genaue Tag oder Commit, der dem Stand von hf-mount am 2026-03-25 entspricht, ist anhand der verfügbaren primären Seiten nicht bestätigt. Die offizielle Ankündigung ist auf 2026-03-24 datiert und dient daher als Klärungsquelle für das Ereignis vom 2026-03-25, nicht als eigenständiges Ereignis.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/huggingface/hf-mount | GitHub - huggingface/hf-mount | 2026-09-05 |
| https://huggingface.co/changelog/hf-mount | Einführung von hf-mount | 2026-09-05 |
| https://huggingface.co/docs/hub/main/models-downloading | Herunterladen von Modellen | 2026-09-05 |
| https://huggingface.co/docs/hub/storage-buckets-access | Zugriffsmuster | 2026-09-05 |
| https://github.com/huggingface/hf-mount/releases | Releases · huggingface/hf-mount | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:hf-mount`, Thread `hf-mount-development`, 1 datiertes Ereignis vom 2026-03-25 bis 2026-03-25.
- **Praktischer Hinweis:** Stand 2026-03-25 können Praktiker das GitHub-Repository hf-mount als Ausgangspunkt für die Evaluierung des Projekts nutzen; Funktionsumfang und Reife sollten dabei anhand der primären Dokumentation überprüft werden.
- **Konfidenz:** mittel. Datierte Ersetzungen oberhalb sind maßgeblich für die Frage, was veraltet ist.

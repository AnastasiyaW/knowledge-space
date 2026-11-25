---
title: "PixVerse CLI — Terminal-Generierung"
category: projects
date: 2026-03-17
tags: [pixverse, pixverse-cli, project, terminal-generation]
aliases: ["PixVerse CLI"]
level: 2
source_sha256: 220e74f8bd162b6af8b18cb8ad78b7c06a714a5f8b38a38ee1dc25ac7228a818
translation: machine
translated_at: '2026-10-24'
---
# PixVerse CLI — Terminal-Generierung {#pixverse-cli-terminal-generation}

**Entwicklungslinie:** `project:pixverse-cli` · Strang `terminal-generation`  
**Letztes Ereignis:** 2026-03-17 · 1 datiertes seit 2026-03-17 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

PixVerse CLI ist eine Kommandozeilenschnittstelle für PixVerse-Abonnenten, mit der Videos, Bilder und Audiodateien aus Prompts oder Referenzen erzeugt werden können.

- Medienerzeugung aus Textprompts und Referenzdateien.
- JSON-Ausgabe für Skripte und Agenten-Pipelines.
- Aufgaben- und Asset-Verwaltung über dedizierte CLI-Befehle.

Voraussetzung ist Node.js 22.12+; die Generierung verbraucht Guthaben des Kontos. Das Tool passt zu Automatisierungs-Workflows, allerdings müssen wir die CLI-Version festschreiben und vor Batch-Läufen Guthaben und verfügbare Parallelitätsslots prüfen.

## Entwicklungslinie {#development-line}

- **2026-03-17 — PixVerse stellte eine terminalorientierte Generierungsschnittstelle vor.** PixVerse öffnete am 2026-03-17 den Kommandozeilenzugang zu seiner Bild- und Videogenerierung. Ein verlinkter ClawHub-Eintrag verbreitete die Schnittstelle für Terminal-Workflows. Das Projekt verlagerte die Generierung vom Webzugang ins Terminal.

## Was sich geändert hat {#what-changed}

2026-03-17 — PixVerse CLI wurde mit terminalbasierter Medienerzeugung verknüpft, der Link bestätigt aber nicht das Veröffentlichungsdatum.  
2026-03-31 — PixVerse kündigte die CLI und die Skills-Bibliothek für Entwickler- und Agenten-Workflows an.  
2026-07-13 — Der offizielle praktische Leitfaden beschrieb Video, Bilder, Stimme, Musik, JSON-Ausgabe und Idempotenz-Schlüssel für Produktionspipelines.  
2026-09-05 — Die aktuelle offizielle README nennt Node.js 22.12+, einen OAuth-Device-Flow, V6 als Standard-Videomodell und eine erweiterte Liste unterstützter Modelle.

## So nutzen wir es {#how-to-use-this}

Stand 2026-03-17 können wir PixVerse über das Terminal für Bild- und Videogenerierung verwenden; Einrichtung und Produktionsgrenzen müssen wir aber zuerst in der offiziellen Dokumentation prüfen.

1. Paket mit npm installieren oder direkt ausführen und anschließend die CLI-Version prüfen.
  — <https://github.com/PixVerseAI/cli>
2. `pixverse auth login` ausführen, die OAuth-Authentifizierung im Browser abschließen und den Status mit `pixverse auth status` prüfen.
  — <https://github.com/PixVerseAI/cli>
3. Guthaben und verfügbare Parallelitätsslots mit `pixverse account info` und `pixverse account slots` prüfen, bevor Batches eingereiht werden.
  — <https://github.com/PixVerseAI/cli>
4. Medien mit `pixverse create video` oder `pixverse create image` erzeugen; für Automatisierung `--json` übergeben, die Task-ID speichern, mit `pixverse task wait` warten und mit `pixverse asset download` herunterladen.
  — <https://github.com/PixVerseAI/cli>

## Bewährte Vorgehensweisen {#best-practices}

- Modell, Qualität, Dauer und Seitenverhältnis explizit setzen, da die unterstützten Optionen vom Modus und vom Modell abhängen.
  — <https://github.com/PixVerseAI/cli>
- Für Batch-Wiederholungen `--idempotency-key` übergeben; mit `--no-wait` Jobs parallel absenden, ihre IDs speichern und sie gebündelt abfragen.
  — <https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal>
- `--json` in Skripten und Agentenläufen aktiviert lassen, damit stdout maschinenlesbar bleibt, während Fortschritt und Fehler getrennt ausgegeben werden.
  — <https://github.com/PixVerseAI/cli>
- Vor großen Läufen `pixverse --version` ausführen und `pixverse create <mode> --help` prüfen; die CLI erst nach Verifizierung der Änderungen aktualisieren.
  — <https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2026-03-17: Wir dürfen dies nicht als bestätigtes Startdatum behandeln; die erste Verfügbarkeitsankündigung erfolgte am 2026-03-31.
- 2026-09-05: Die Node.js-20-Anforderung aus der veröffentlichten Skills-Karte ist veraltet; die aktuelle offizielle README verlangt Node.js 22.12+.
- 2026-09-05: Die Beschränkung auf Video und Bilder ist unvollständig; die aktuelle CLI dokumentiert zusätzlich Stimme, Musik, Aufgaben, Assets und Workspaces.

## Weiterhin unbekannt {#still-unknown}

- Die offizielle Quelle bestätigt nicht, dass der ursprüngliche Link vom 2026-03-17 an diesem Tag veröffentlicht wurde: Der aktuelle praktische Leitfaden ist auf 2026-07-13 datiert, die offizielle Verfügbarkeitsankündigung der CLI auf 2026-03-31.
- Die ClawHub-Karte nennt Node.js 20+, während die aktuelle offizielle README Node.js 22.12+ angibt; für die Installation sollten wir der README oder der Hilfe des installierten Pakets folgen.
- Dem Antwortschema des Systems fehlen die getrennten Felder event_findings und new_events; relevante Klarstellungen stehen in what_changed, supersedes und unknowns.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal | PixVerse CLI: Generate AI Videos and Images in Terminal | 2026-09-05 |
| https://clawhub.ai/PixVerse-Official/pixverse-ai-image-and-video-generator | PixVerse AI Image and Video Generator | 2026-09-05 |
| https://github.com/PixVerseAI/cli | PixVerseAI/cli — official command-line interface | 2026-09-05 |
| https://pixverse.ai/en/blog/pixverse-evolves-from-creation-tool-to-production-platform | PixVerse Evolves From Creation Tool to Production Platform With New Studio and Developer Releases | 2026-09-05 |

## Agenten-Brief {#agent-brief}

- **Gegenstand:** `project:pixverse-cli`, Strang `terminal-generation`, 1 datiertes Ereignis 2026-03-17 → 2026-03-17.
- **Praktischer Hinweis:** Stand 2026-03-17 sollten Praktiker einen terminalbasierten PixVerse-Workflow für Bild- und Videogenerierung in Betracht ziehen, dabei aber Einrichtung, unterstützte Operationen und Produktionstauglichkeit in der offiziellen Dokumentation prüfen, bevor sie sich darauf verlassen.
- **Konfidenz:** mittel. Die datierten Einträge unter „Durch diesen Eintrag ersetzt“ sind maßgeblich dafür, was veraltet ist.

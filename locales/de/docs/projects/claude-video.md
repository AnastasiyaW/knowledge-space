---
title: "claude-video"
category: projects
date: 2026-07-27
tags: [claude-video, claude-video-development, claude_video, project]
aliases: ["claude-video", "claude-video (watch)"]
level: 2
source_sha256: dcc1d4301bee72642b4103abcdbe5704ddee8a28a07625e474ba8a47c86132bd
translation: machine
translated_at: '2026-10-24'
---
# claude-video {#claude-video}

**Entwicklungslinie:** `project:claude-video` · Thread `claude-video-development`  
**Letztes Ereignis:** 2026-07-27 · 1 datiert seit 2026-07-27 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was ist das {#what-it-is}

claude-video ist ein `/watch`-Skill für Videoanalyse für Agenten.

- Eingabe: nimmt eine URL oder eine lokale Datei entgegen.
- Extraktion: zieht Frames und Untertitel heraus.
- Audio-Fallback: verwendet Whisper, wenn Untertitel fehlen.
- Übergabe der Ergebnisse: gibt die Ausgabe an den Agenten weiter.

Das Standardlimit für lange Videos liegt bei bis zu 100 Frames; der Modus `token-burner` ist unbegrenzt. Das Werkzeug eignet sich für Bildschirmaufnahmen, Videoclips und gezielte Zeitstempel, die Kontextkosten steigen jedoch mit der Anzahl der Frames.

## Entwicklungslinie {#development-line}

- **2026-07-27 — claude-video-Repository öffentlich referenziert.** Am 2026-07-27 verlinkte ein Eintrag auf das GitHub-Repository bradautomates/claude-video. Dies ist die früheste öffentliche Referenz in der Projekthistorie und liefert eine konkrete Quelle zur Prüfung.

## Was sich geändert hat {#what-changed}

- 2026-07-27 — Repository-Link erfasst. Primäre Quellen zeigen für genau dieses Datum keinen separaten Commit und kein separates Release.
- 2026-06-29 — Version 0.2.0 ergänzte vier Detailmodi, Frame-Deduplizierung, automatisches Aufteilen langer Audiodateien für Whisper sowie ein portables Skill-Paket für mehrere Hosts.

## Verwendung {#how-to-use-this}

Ab 2026-07-27 sollte das verlinkte GitHub-Repository bradautomates/claude-video als Quelle für Implementierungs- und Nutzungsdetails betrachtet werden.

1. Installiere den Skill für Claude Code über den Marketplace oder für Codex und andere Agent-Skills-Hosts mit `npx skills add bradautomates/claude-video -g`.
  — <https://github.com/bradautomates/claude-video>
2. Führe `/watch <URL-or-path> <question>` aus. Unterstützt werden URLs, die yt-dlp verarbeitet, sowie lokale MP4-, MOV-, MKV- und WebM-Dateien.
  — <https://github.com/bradautomates/claude-video>
3. Übergib `--start` und `--end` für einen gezielten Ausschnitt. Dadurch werden Frames dichter abgetastet, während weniger Kontext-Tokens verbraucht werden.
  — <https://github.com/bradautomates/claude-video>
4. Wähle `transcript`, `efficient`, `balanced` oder `token-burner`. Fehlen Untertitel, setze einen Groq-Schlüssel für `whisper-large-v3` oder einen OpenAI-Schlüssel für `whisper-1`.
  — <https://github.com/bradautomates/claude-video>

## Bewährte Methoden {#best-practices}

- Grenze das Zeitfenster mit `--start` und `--end` ein, wenn es um einen bestimmten Moment geht, statt das gesamte Video zu durchsuchen.
  — <https://github.com/bradautomates/claude-video>
- Beginne mit `transcript` bei Videos mit Untertiteln oder mit `efficient` für einen schnellen visuellen Durchgang; verwende `token-burner` nur in Fällen, die die Kosten vieler Frames rechtfertigen.
  — <https://github.com/bradautomates/claude-video>
- Lass die Frame-Deduplizierung aktiviert: Standardmäßig verwirft sie nahezu identische Frames, bevor das Limit angewendet wird.
  — <https://github.com/bradautomates/claude-video>
- Hänge keine Kommentare an den Wert von `WATCH_DETAIL` an: Dies führte zuvor zu einem stillen Rückfall auf den Standardmodus, behoben in Commit 83da59f.
  — <https://github.com/bradautomates/claude-video/commit/83da59f>

## Durch diesen Stand ersetzt {#superseded-by-this}

- 2026-04-24 — Der eigenständige Wrapper `commands/watch.md` und das nicht in sich geschlossene Skill-Layout wurden in Version 0.2.0 durch das Paket `skills/watch/` ersetzt.
- 2026-04-24 — Die Windows-Anleitung mit `python3` ist veraltet: Unter Windows werden Skripte mit `python` ausgeführt.
- 2026-04-24 — Das frühe feste Limit `--max-frames=80` wurde durch Limits ersetzt, die an den Detailmodus gekoppelt sind.

## Weiterhin unbekannt {#still-unknown}

- Das datierte Ereignis liefert nur die Repository-URL. Es wurde kein Release oder Commit vom 2026-07-27 aus einer Erstquelle gefunden, daher gibt es für dieses Datum keine quellengestützte Ergänzung.
- Das Schema enthält keine Felder `event_findings` und `new_events`; das Release vom 2026-06-29 bleibt daher unter `what_changed` und wird nicht als eigenes strukturiertes Ereignis geführt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/bradautomates/claude-video | bradautomates/claude-video — README und aktuelle Nutzungsdokumentation | 2026-09-05 |
| https://raw.githubusercontent.com/bradautomates/claude-video/main/CHANGELOG.md | claude-video-Changelog — Version 0.2.0 vom 2026-06-29 | 2026-09-05 |
| https://github.com/bradautomates/claude-video/commit/83da59f | Fix WATCH_DETAIL silently falling back to default | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:claude-video`, Thread `claude-video-development`, 1 datiertes Ereignis 2026-07-27 → 2026-07-27.
- **Praktischer Hinweis:** Ab 2026-07-27 sollte das verlinkte GitHub-Repository bradautomates/claude-video als Quelle für Implementierungs- und Nutzungsdetails betrachtet werden.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.

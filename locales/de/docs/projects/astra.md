---
title: "Topaz Labs Astra — Astra-Entwicklung"
category: projects

tags: [astra, astra-development, project, topaz-labs:astra]
aliases: ["Topaz Labs Astra"]
level: 2
source_sha256: dfecd1ea7de78d2326fd689b2a096cc7e479d93d7e600f5fb8b10bd0a5f62e30
translation: machine
translated_at: '2026-10-24'
---
# Topaz Labs Astra — Astra-Entwicklung {#topaz-labs-astra-astra-development}

**Entwicklungslinie:** `project:astra` · Thread `astra-development`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Topaz Labs Astra ist ein Cloud-Tool für KI-Videoersteller und Restaurierung.
Es bietet zwei Modi: Creative fügt neue Details hinzu, und Precise erhält die ursprüngliche Struktur.
Aktuelle Modelle und das Rendering sind bereits in Topaz for Web enthalten.
Die eigenständige Astra-Oberfläche wird am 2026-09-30 geschlossen.
Wählen Sie Precise für kontrollierte Restaurierung, Creative für gezielte generative Überarbeitung, und prüfen Sie jedes Ergebnis.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht aufgeschrieben; das Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

- 2025-06-25 — Astra lief als eigenständige Abo-Web-App und nicht als Funktion von Topaz Video. Der Schwerpunkt lag auf generativem kreativem Upscaling, um neues visuelles Material zu erstellen. Community-Beiträge von diesem Tag zeigen einen geteilten Workflow: lokales Starlight Mini für die Grundarbeit und Astra für Fragmente, die eine kreative Rekonstruktion benötigen. Dies belegt das öffentliche Startdatum nicht.
- 2025-12-24 — Das Realism Update fügte Astra Starlight Precise 2, Scene Controls und Batch-Rendering hinzu.
- 2026-02-20 — Das Local Update fügte Astra die Cloud-Version Starlight Fast 2, Scene Controls und Batch Rendering hinzu.
- 2026-03-31 — Das Precision Update fügte die Cloud-Version Starlight Precise 2.5 hinzu, für sauberere Gesichter, Stoffe und Text beim Upscaling von KI-Video auf 4K.
- 2026-05-19 — Das Workflows Update fügte Astra das Modell Hyperion 2 SDR-to-HDR hinzu.
- 2026-09-03 — Topaz hat die Astra-Modelle und -Bibliotheken in Topaz for Web verschoben. Abonnements, Credits und Verarbeitungskosten werden übernommen. Die Astra-Oberfläche wird am 2026-09-30 abgeschaltet.

## Verwendung {#how-to-use-this}

Zum Stand 2025-06-25 wird keine Änderung des Workflows für die Praxis vorgeschlagen: Der datierte Link allein belegt keine verifizierte Tatsache zur Produktentwicklung.

1. Öffnen Sie Topaz for Web und melden Sie sich mit Ihrem Topaz-Konto an; Dateien und Credits wurden bereits von Astra übernommen.
  — <https://www.topazlabs.com/web/faq>
2. Laden Sie ein H.264-MP4-Video hoch; führen Sie zuerst eine CFR-Konvertierung durch, wenn die Bildrate variabel ist.
  — <https://docs.topazlabs.com/astra/quick-start>
3. Wählen Sie Precise, um das Originalmaterial zu erhalten, oder Creative, um Details zu überarbeiten. Setzen Sie in Astra 2 Creativity und Sharpness auf Werte von 1 bis 5 und formulieren Sie einen beschreibenden Prompt statt Befehlen.
  — <https://docs.topazlabs.com/astra/modes-and-models>
4. Legen Sie Render-Parameter und Bereich fest, starten Sie die Verarbeitung, warten Sie auf den Abschluss und laden Sie die Ausgabe herunter.
  — <https://docs.topazlabs.com/astra/quick-start>

## Bewährte Praktiken {#best-practices}

- Teilen Sie Aufgaben nach Ziel auf: Precise restauriert das Originalmaterial, Creative erzeugt neue Details.
  — <https://www.topazlabs.com/astra>
- Prüfen Sie Gesichter, kleinen Text und Hintergrundobjekte Bild für Bild: Nutzertests vom 2025-06-25 zeigten Verzerrungen bei entfernten Gesichtern und Text nach der kreativen Rekonstruktion.
  — <https://community.topazlabs.com/t/starlight-mini-astra/92744>
- Testen Sie einen kurzen Clip vor einem vollständigen Render: Frühe Nutzertests zeigten, dass Astra auch bei kurzen Vorschauen Credits verbrauchte.
  — <https://community.topazlabs.com/t/topaz-video-ai-and-astra/92566>

## Hierdurch ersetzt {#superseded-by-this}

- 2025-06-25: Astra als Desktop-Funktion von Topaz Video zu behandeln, ist veraltet; es war eine eigenständige Abo-Web-App.
- 2026-09-03: Anweisungen, nur über Astra zu arbeiten, sind veraltet; Modelle, Bibliothek und Credits befinden sich nun in Topaz for Web, und die Astra-Oberfläche wird am 2026-09-30 geschlossen.

## Weiterhin unbekannt {#still-unknown}

- Der Quelltext des Beitrags vom 2025-06-25 ist für automatisierte Prüfung nicht verfügbar; daher können wir nicht verifizieren, ob es sich um eine Startankündigung, eine Rezension oder einen Link zu einem aktiven Dienst handelte.
- Das Antwortschema enthält keine Felder event_findings und new_events, daher stehen datierte Änderungen in what_changed.
- Keine datierte primäre Ankündigung bestätigt einen öffentlichen Start am 2025-06-25; eine Antwort von Topaz-Mitarbeitenden an diesem Tag bestätigt nur die eigenständige Abo-Web-App.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://community.topazlabs.com/t/topaz-video-ai-and-astra/92566 | Topaz Video AI and Astra | 2026-09-05 |
| https://community.topazlabs.com/t/starlight-mini-astra/92744 | Starlight Mini + Astra | 2026-09-05 |
| https://docs.topazlabs.com/astra/quick-start | Quick Start | 2026-09-05 |
| https://docs.topazlabs.com/astra/modes-and-models | Modes and Models | 2026-09-05 |
| https://www.topazlabs.com/astra | Astra - Creative Video Upscaling for AI Videos up to 4K Quality | 2026-09-05 |
| https://www.topazlabs.com/updates | Topaz Labs | Updates | 2026-09-05 |
| https://www.topazlabs.com/updates/realism | Topaz Labs | Realism Update | 2026-09-05 |
| https://www.topazlabs.com/updates/local | Topaz Labs | Local Update | 2026-09-05 |
| https://www.topazlabs.com/updates/precision | Topaz Labs | Precision Update | 2026-09-05 |
| https://www.topazlabs.com/web/faq | Astra to Web | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:astra`, Thread `astra-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Zum Stand 2025-06-25 wird keine Änderung des Workflows für die Praxis vorgeschlagen: Der datierte Link allein belegt keine verifizierte Tatsache zur Produktentwicklung.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

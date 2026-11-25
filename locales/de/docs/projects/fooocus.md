---
title: "Fooocus"
category: projects
date: 2023-09-12
tags: [fooocus, fooocus-development, fooocus_v2, project]
aliases: ["Fooocus"]
level: 3
source_sha256: 2b5d416246237494ff95b6235c0d4fb3f1c9cc513b895f4e459b4ac948d9d967
translation: machine
translated_at: '2026-10-24'
---
# Fooocus {#fooocus}

**Entwicklungslinie:** `project:fooocus` · Thread `fooocus-development`  
**Letztes Ereignis:** 2023-09-12 · 2 datierte Ereignisse seit 2023-08-13 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Fooocus ist ein lokaler, offline lauffähiger SDXL-Bildgenerator für Kreative, die einen einfacheren, prompt-orientierten Workflow als mit ComfyUI wünschen.

- Text-zu-Bild mit Stilen und Prompt-Erweiterung.
- Variationen, Upscaling, Inpainting/Outpainting, Image Prompt und Face Swap.
- Voreinstellungen für allgemeine, realistische und Anime-Bilder.

## Entwicklungslinie {#development-line}

- **2023-08-13 — Fooocus-Repository und Windows-Release-Archiv verlinkt.** Am 2023-08-13 haben wir Fooocus mit seinem GitHub-Repository und dem Windows-64-Bit-Release-Archiv verknüpft. Damit ist ein öffentlich verteilbares Artefakt in der Fooocus-Entwicklungslinie dokumentiert.
- **2023-09-12 — Fooocus-Entwicklungsdiskussion verlinkt.** Am 2023-09-12 haben wir die Fooocus-Entwicklungslinie mit der GitHub Discussion #347 verknüpft. Dies verbindet den Thread mit der Geschichte der Fooocus-v2-Ära, wobei wir den Inhalt der Diskussion selbst nicht untersucht haben.

## Was sich geändert hat {#what-changed}

2023-08-13 — Fooocus wurde öffentlich als Version 1 verfügbar. Das Update-Log markiert v1.0.15 als öffentlich verfügbar.

2023-09-12 — Fooocus 2.0.0 ersetzte die Textverarbeitungs-Engine, ergänzte Prompting mit mehreren Stilen und benannte Prompt Expansion und Raw Mode in Fooocus V2 um. Der Maintainer berichtete, dass V2 V1 in 87/100 Standardergebnissen und in 81/100 Tests zum Prompt-Verständnis übertraf; bewertet wurde von zwei Personen.

2026-09-04 (heute gefunden, kein Veröffentlichungsdatum) — Upstream beschreibt Fooocus als nur SDXL unterstützend, mit eingeschränktem LTS und nur Fehlerbehebungen. Release v2.5.5 ist derzeit als Latest markiert und enthält einen Fix für Inpainting in Colab.

## Wie man das nutzt {#how-to-use-this}

Ab 2023-08-13 das öffentliche GitHub-Repository und das Windows-Verteilungsartefakt verwenden. Ab 2023-09-12 die verlinkte Entwicklungsdiskussion konsultieren, bevor man sich auf Verhalten der v2-Ära verlässt.

1. Prüfen, ob ein SDXL-Workflow zur Aufgabe passt; Fooocus ist nicht der gepflegte Weg für Flux oder andere neuere Architekturen.
  — <https://github.com/lllyasviel/Fooocus>
2. Unter Windows das offizielle Download-Paket nutzen, entpacken und `run.bat` ausführen. Unter Linux das Repository klonen, die gepinnten Anforderungen in Conda oder einer Python-3.10-venv installieren und danach `entry_with_update.py` ausführen.
  — <https://github.com/lllyasviel/Fooocus>
3. Den ersten Start die ausgewählten Modelle herunterladen lassen und dann die Voreinstellung default, anime oder realistic verwenden, entweder in der UI oder mit `--preset anime` / `--preset realistic`.
  — <https://github.com/lllyasviel/Fooocus>
4. Einen Prompt schreiben, bei Bedarf Stile oder Advanced-Einstellungen wählen und Input Image für Variation, Upscaling, Inpainting/Outpainting oder Image-Prompt-Workflows nutzen.
  — <https://github.com/lllyasviel/Fooocus>
5. Die UI lokal halten, sofern kein Fernzugriff nötig ist. Für `--listen` oder `--share` eine `auth.json` hinzufügen, da der Zugriff standardmäßig nicht authentifiziert ist.
  — <https://github.com/lllyasviel/Fooocus>

## Best Practices {#best-practices}

- Nur aus dem offiziellen GitHub-Repository oder über dessen verlinkte Downloads installieren; Upstream warnt, dass ähnlich benannte Fooocus-Websites gefälscht sind.
  — <https://github.com/lllyasviel/Fooocus>
- Fooocus als stabiles SDXL-Werkzeug behandeln. Für Flux oder Arbeit mit neueren Modellen der Empfehlung des Upstreams folgen und stattdessen WebUI Forge, ComfyUI oder SwarmUI verwenden.
  — <https://github.com/lllyasviel/Fooocus>
- Beim Wechseln der Voreinstellung die benötigten Modelle vollständig herunterladen lassen. `--always-download-new-model` verwenden, wenn eine Voreinstellung das fehlende Modell nachladen soll, statt stillschweigend auf ein älteres zurückzufallen.
  — <https://github.com/lllyasviel/Fooocus>
- Jede netzwerkexponierte UI mit `auth.json` absichern. Weder `--listen` noch `--share` aktivieren standardmäßig eine Authentifizierung.
  — <https://github.com/lllyasviel/Fooocus>
- Bereitgestellte Seitenverhältnisse gegenüber beliebigen benutzerdefinierten Auflösungen bevorzugen, sofern die positionale Kodierung von SDXL nicht verstanden ist.
  — <https://github.com/lllyasviel/Fooocus/blob/main/update_log.md>

## Hiermit ersetzt {#superseded-by-this}

- 2023-08-13 — das derzeit als Latest markierte Release v2.5.5 ersetzt den öffentlichen Stand von Version 1.
- 2023-09-12 — Fooocus 2.0 und sein Stil `Fooocus V2` ersetzen die Hinweise zur Textverarbeitung aus V1 sowie das UI-Label „Prompt Expansion and Raw Mode“; diesen Stil deaktivieren, wenn V1-Ausgaben reproduziert werden sollen.
- 2026-09-04 (heute gefunden) — auf offizielle Fooocus-Unterstützung für Flux oder eine andere neue Architektur zu warten, ist heute überholt: Upstream ist LTS mit reinen Fehlerbehebungen und verweist Flux-Nutzer auf andere Werkzeuge.

## Noch unbekannt {#still-unknown}

- Wir haben das direkte Windows-Archiv unter https://github.com/lllyasviel/Fooocus/releases/download/release/Fooocus_win64_1-1-10.7z nicht geprüft; Inhalt, Prüfsumme und genaue Paketversion sind unbestätigt.
- Das Upstream-Update-Log markiert v1.0.15 als öffentlich verfügbar, ohne Kalenderdatum; der genaue Veröffentlichungszeitpunkt ist daher unbestätigt.
- Hinter `fooocus` und `fooocus_v2` steht kein eigenständiges Produkt: Die offizielle Diskussion identifiziert Letzteres als Fooocus 2.0.0, nicht als anderen Gegenstand.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/lllyasviel/Fooocus | Fooocus-Repository und README | 2026-09-04 |
| https://github.com/lllyasviel/Fooocus/discussions/347 | [Major Update] Fooocus 2.0.0 — Discussion #347 | 2026-09-04 |
| https://github.com/lllyasviel/Fooocus/blob/main/update_log.md | Fooocus-Update-Log | 2026-09-04 |
| https://github.com/lllyasviel/Fooocus/releases/tag/v2.5.5 | Fooocus-Release v2.5.5 | 2026-09-04 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:fooocus`, Thread `fooocus-development`, 2 datierte Ereignisse 2023-08-13 → 2023-09-12.
- **Praxishinweis:** Ab 2023-08-13 können Praktiker Fooocus als Projekt mit öffentlich verlinkter GitHub-Quelle und Windows-Verteilungsartefakt betrachten; ab 2023-09-12 sollten sie die verlinkte Entwicklungsdiskussion konsultieren, bevor sie sich auf Verhalten der v2-Ära verlassen.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.

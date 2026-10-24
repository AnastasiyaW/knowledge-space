---
title: "DMX"
category: projects
date: 2026-04-09
tags: [dmx, dmx-format-release, dmx_format_release, project]
aliases: ["DMX"]
level: 2
source_sha256: 29584239a69cbc51a6923baf08040ea2a96d2019b1f78655605238cdcde8a8a9
translation: machine
translated_at: '2026-10-24'
---
# DMX {#dmx}

**Entwicklungslinie:** `project:dmx` · Thread `dmx-format-release`  
**Letztes Ereignis:** 2026-04-09 · 1 datiertes Ereignis seit 2026-04-09 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

DMX ist ein Python-Paket für Teams, die safetensors-Modelle verteilen: verlustfreie `.dmx`-Archive, basisrelative `.dmxd`-Deltas, Round-Trip-Verifikation und eingebettete Lineage-Metadaten. Einschränkung: Jedes bis einschließlich 1.5.3 aufgeführte PyPI-Release ist zurückgezogen (yanked), daher ist es keine sichere, ungepinnte Abhängigkeit für Produktivumgebungen.

## Entwicklungslinie {#development-line}

- **2026-04-09 — DMX wurde öffentlich als Kompressionsformat für KI-Modellgewichte vorgestellt.** Am 2026-04-09 wurde DMX öffentlich über einen Beitrag in der ComfyUI-Community vorgestellt, der auf ein GitHub-Repository und ein Hugging-Face-Profil verlinkte. Die verlinkten Materialien beschreiben das Projekt als Kompression von KI-Modellgewichten. Die verfügbaren Belege belegen weder technische Spezifikationen, Reifegrad des Releases noch unterstützte Integrationen.

## Was sich geändert hat {#what-changed}

2026-04-09 — DMX wurde als CLI-orientierter Kompressor für Modellspeicherung und -übertragung veröffentlicht; die Paket-Historie vom Release-Tag verzeichnet die Versionen 0.4.0 und 0.5.0, die später zurückgezogen wurden. Der ursprüngliche Workflow erforderte die Dekompression zurück in safetensors vor der Nutzung in ComfyUI; der Launch nannte 9,1 GB auf 1,8 GB, 7,2 GB auf 1,5 GB sowie +0,16 % Perplexität bei Llama 3 8B. 2026-04-10 — PyPI-Version 0.6.0 wurde veröffentlicht und später zurückgezogen. 2026-04-11 — PyPI-Version 0.7.0 wurde veröffentlicht und später zurückgezogen. 2026-04-19 — PyPI-Versionen 1.0.0 und 1.1.0 wurden veröffentlicht und später zurückgezogen; die spätere Paketdokumentation beschreibt verlustfreie Archive, Deltas, Provenienz und eine GPU-Laufzeitumgebung. 2026-04-20 bis 2026-04-25 — Versionen 1.2.0 bis 1.5.3 wurden veröffentlicht und alle später zurückgezogen. Ein Qwen2.5-3B-Instruct-Delta demonstriert den neueren Verteilungsweg: 2,88 GB int16-Delta gegenüber einem vollständigen Modell mit 13,59 GB, es erfordert jedoch die exakte Qwen2.5-3B-Basis und einen zusammengeführten Export als Einzeldatei.

## Anwendung {#how-to-use-this}

Stand 2026-04-09 können Praktiker, die Speicherung oder Übertragung von Modellgewichten evaluieren, DMX als neu angekündigtes Kompressionsformat-Projekt betrachten, sollten aber Implementierungsdetails und Kompatibilität in seinem Repository prüfen, bevor sie es einsetzen.

1. Keine ungepinnte aktuelle Version installieren: Zuerst ein bestimmtes Wheel auswählen und prüfen, da die aufgeführten Releases zurückgezogen sind.
  — <https://pypi.org/project/dmx-compress/>
2. Für ein verlustfreies Archiv `dmx compress model.safetensors model.dmx` ausführen und anschließend mit `dmx verify model.safetensors model.dmx` nachweisen.
  — <https://pypi.org/project/dmx-compress/>
3. Einen portablen Checkpoint mit `dmx decompress model.dmx restored.safetensors` wiederherstellen; die wiederhergestellten safetensors in Werkzeugen verwenden, die DMX nicht nativ laden.
  — <https://pypi.org/project/dmx-compress/>
4. Für das veröffentlichte Qwen-Delta die exakte Basis Qwen/Qwen2.5-3B beschaffen, `dmx delta-reconstruct` anwenden und anschließend die rekonstruierten safetensors im Zielframework laden.
  — <https://huggingface.co/Senat1/dmx-qwen2.5-3b-instruct-delta>

## Bewährte Vorgehensweisen {#best-practices}

- Den Originalcheckpoint behalten und vor dem Löschen oder Verteilen eines DMX-Artefakts eine Round-Trip-Verifikation durchführen.
  — <https://pypi.org/project/dmx-compress/>
- Ein Delta als an seinen angegebenen Basis-Checkpoint gebunden behandeln; eine Rekonstruktion mit einer anderen Basis wird voraussichtlich fehlschlagen.
  — <https://huggingface.co/Senat1/dmx-qwen2.5-3b-instruct-delta>
- Für den Workflow vom 9. April DMX als Kompression für Festplatte und Download einplanen, nicht als Reduzierung des ComfyUI-VRAM-Bedarfs; das native Laden in ComfyUI war damals nur ein Roadmap-Punkt.
  — <https://www.reddit.com/r/comfyui/comments/1saeezm/i_built_a_compression_format_for_ai_model_weights/>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2026-04-09 — Die Angabe, DMX sei nur ein externer Speicherkompressor, ist gegenüber späteren Paketaussagen zu einer Laufzeitunterstützung für komprimierte Residenz veraltet; diese Aussagen sind für eine produktive Einführung jedoch nicht ausreichend reproduzierbar.
- 2026-04-09 — Die Anweisung, mit einem nativen ComfyUI-Node zu rechnen, ist als aktuelle Anleitung überholt: wiederhergestellte safetensors verwenden, sofern keine separat verifizierte Integration verfügbar ist.

## Weiterhin unbekannt {#still-unknown}

- Das angeforderte Antwortschema enthält keine Felder `event_findings` oder `new_events`; die ereignisspezifischen Ergänzungen und spätere datierte Ereignisse sind daher in `what_changed` abgebildet.
- Die ursprüngliche GitHub-Repository-URL lieferte bei der Prüfung 404; Repository-Code, Changelog und aktuelle Betreuung konnten daher nicht unabhängig geprüft werden.
- Das PyPI-README nennt Laufzeit-Benchmarks und Unterstützungsaussagen, seine öffentliche technische und Benchmark-Dokumentation ist jedoch als ausstehend gekennzeichnet; diese Messwerte sind als Aussagen der Betreiber zu behandeln, nicht als unabhängig reproduzierte Ergebnisse.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://www.reddit.com/r/comfyui/comments/1saeezm/i_built_a_compression_format_for_ai_model_weights/ | Ich habe ein Kompressionsformat für KI-Modellgewichte gebaut — 60–80 % kleiner, brauche Hilfe beim Testen | 2026-09-05 |
| https://github.com/willjriley/dmx | Repository willjriley/dmx (bei Beobachtung 404) | 2026-09-05 |
| https://huggingface.co/Senat1/dmx-qwen2.5-3b-instruct-delta | DMX-Delta für Qwen2.5-3B-Instruct | 2026-09-05 |
| https://pypi.org/project/dmx-compress/ | dmx-compress auf PyPI | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:dmx`, Thread `dmx-format-release`, 1 datiertes Ereignis 2026-04-09 → 2026-04-09.
- **Praktischer Hinweis:** Stand 2026-04-09 können Praktiker, die Speicherung oder Übertragung von Modellgewichten evaluieren, DMX als neu angekündigtes Kompressionsformat-Projekt betrachten, sollten aber Implementierungsdetails und Kompatibilität in seinem Repository prüfen, bevor sie es einsetzen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

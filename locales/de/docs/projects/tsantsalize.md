---
title: "TSANTSALIZE — Öffentliche Verfügbarkeit des Modells"
category: projects
date: 2026-06-19
tags: [ltx_2_3, project, public-model-availability, tsantsalize]
aliases: ["TSANTSALIZE"]
level: 2
source_sha256: a623c9c229d820c65742abcf41b4b5646bd4940c8bd972a005035800256b3e07
translation: machine
translated_at: '2026-10-24'
---
# TSANTSALIZE — Öffentliche Verfügbarkeit des Modells {#tsantsalize-public-model-availability}

**Entwicklungslinie:** `project:tsantsalize` · Thread `public-model-availability`  
**Letztes Ereignis:** 2026-06-19 · 1 datiertes Ereignis seit 2026-06-19 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

TSANTSALIZE ist ein IC-LoRA für Video-zu-Video-Anwendungen mit LTX-2.3 für ComfyUI-Nutzer, die einen gezielten Effekt mit verkleinertem Kopf bei einer sprechenden Person erzielen möchten.

- Formt das sprechende Subjekt anhand eines Referenzclips um.
- Hält die Sprachverarbeitung außerhalb des Adapters, in einem mitgelieferten Audio-Workflow.

## Entwicklungslinie {#development-line}

- **2026-06-19 — Hugging-Face-Modellressource TSANTSALIZE erfasst.** TSANTSALIZE wurde als LTX-2.3-IC-LoRA zum Verkleinern des Kopfes eines sprechenden Subjekts eingesetzt. Die Release-Notiz ist auf 2026-06-18 datiert und gibt Video-zu-Video mit First-Frame-Conditioning an. Die Stimmveränderung bleibt in einer workflowseitigen Audiokette.

## Was sich geändert hat {#what-changed}

2026-06-19: TSANTSALIZE wurde als LTX-2.3-IC-LoRA zum Verkleinern des Kopfes eines sprechenden Subjekts eingesetzt. Die Release-Notiz ist auf 2026-06-18 datiert und gibt Video-zu-Video mit First-Frame-Conditioning an. Die Stimmveränderung bleibt in einer workflowseitigen Audiokette.

## So wird es verwendet {#how-to-use-this}

Prüfen Sie das verlinkte Hugging-Face-Repository auf die dokumentierte öffentliche Modellressource TSANTSALIZE vom 2026-06-19 und verifizieren Sie unabhängig davon die Dateien, die Lizenz und die Nutzungshinweise.

1. Laden Sie den TSANTSALIZE-Checkpoint und den mitgelieferten ComfyUI-Workflow aus dem Modell-Repository herunter.
  — <https://huggingface.co/TheBurgstall/tsantsalize>
2. Führen Sie es mit einem LTX-2.3-kompatiblen ComfyUI-Video-zu-Video-Workflow und einem Referenzclip mit einer sprechenden Person aus; der Adapter verändert die Stimme selbst nicht.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
3. Für eine leichte Proportionsänderung verwenden Sie eine LoRA-Stärke um 0,5; für den beabsichtigten Effekt verwenden Sie die vom Ersteller angegebene Einstellung 1,2. Fügen Sie `tsantsalize` zum Prompt hinzu; `tiny head` kann helfen.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
4. Verwenden Sie die mitgelieferten Audio-Nodes separat, wenn veränderte Audioausgabe gewünscht ist: Der Workflow wendet Pitch-Shifting, Hochpassfilterung für Gesang und MelBand-RoFormer-Separation an.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
5. Prüfen Sie vor dem Einsatz auf einer aktuellen LTX-Installation, dass Adapter, Basismodell, Nodes und Workflow-Version zusammenpassen; LTX dokumentiert die Versionsübereinstimmung als Voraussetzung für IC-LoRAs.
  — <https://docs.ltx.io/open-source-model/usage-guides/ic-lo-ra>

## Best Practices {#best-practices}

- Beginnen Sie mit einer einzelnen Person, die direkt in die Kamera spricht. Der Ersteller berichtet bei anderem Material von deutlich weniger vorhersehbaren Ergebnissen.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
- Halten Sie die Stärke für den vollen Effekt bei höchstens 1,2, und verwenden Sie etwa 0,5, wenn nur eine kleine Anpassung gewünscht ist. Werte über 1,2 führten in den Tests des Erstellers zu Identitätsverschiebungen.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
- Behandeln Sie negative Stärke nicht als erprobten Weg, Köpfe zu vergrößern: Der Ersteller hat dies für diesen Adapter nicht getestet und berichtet, dass es bei früheren IC-LoRAs gescheitert sei.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
- Passen Sie Auflösung und Bildrate des Referenzvideos an die Generierung an, testen Sie zuerst einen einfachen Clip und vergleichen Sie die Ausgabe mit und ohne Adapter, bevor Sie eine komplexe Einstellung versuchen.
  — <https://docs.ltx.io/open-source-model/usage-guides/ic-lo-ra>

## Durch dieses ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Der genaue Checkpoint-Dateiname, die Lizenz, die unveränderliche Revision, das Workflow-JSON und alle Abhängigkeiten von Custom Nodes konnten aus dem Modell-Repository nicht unabhängig ermittelt werden.
- Es wurde kein datierter Port, Nachfolger, Benchmark oder verifizierter Kompatibilitätstest mit LTX-2.5 gefunden.
- Die vom Ersteller angegebene LoRA-Stärke 1,2 ist nicht nachweislich gleichwertig mit der aktuellen LTX-2.5-Steuerung `attention_strength`, die auf einer Skala von 0 bis 1,0 dokumentiert ist.
- Die Release-Notiz ist auf 2026-06-18 datiert, das erfasste Ereignis auf 2026-06-19; die Belege lassen nicht erkennen, ob der 19. Juni eine eigenständige Modellrevision oder die spätere Verbreitung derselben Veröffentlichung war.
- Die Snapshots der Hugging-Face-Suche widersprechen sich: Ein Snapshot des Modellkatalogs führt TSANTSALIZE als am 2026-06-18 aktualisiert, ein Profil-Snapshot sagt, es sei fünf Tage zuvor aktualisiert worden, ohne Kalenderdatum oder Revision. Das reicht nicht aus, um ein späteres datiertes Ereignis zu begründen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/TheBurgstall/tsantsalize | Modell-Repository TheBurgstall/tsantsalize | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/ | TSANTSALIZE — the most useless IC-LoRA you'll download today | 2026-09-05 |
| https://docs.ltx.io/open-source-model/usage-guides/ic-lo-ra | IC-LoRA | LTX Documentation | 2026-09-05 |
| https://docs.ltx.io/open-source-model/integration-tools/ic-lo-ra-adapters | IC-LoRA Adapters | LTX Documentation | 2026-09-05 |
| https://huggingface.co/TheBurgstall | TheBurgstall | Hugging Face | 2026-09-05 |
| https://huggingface.co/TheBurgstall/models | TheBurgstall-Modelle | Hugging Face | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:tsantsalize`, Thread `public-model-availability`, 1 datiertes Ereignis vom 2026-06-19 → 2026-06-19.
- **Praktischer Hinweis:** Ab dem 2026-06-19 sollten Anwender das verlinkte Hugging-Face-Repository als erfasste öffentliche Modellressource TSANTSALIZE prüfen und dabei die aktuellen Dateien, die Lizenz und die Nutzungshinweise unabhängig verifizieren.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

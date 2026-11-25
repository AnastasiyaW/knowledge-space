---
title: "Canon UltraReal"
category: projects
date: 2026-07-19
tags: [canon-ultrareal, canon-ultrareal-public-model-listing, project]
aliases: ["Canon UltraReal"]
level: 2
source_sha256: 5cd58ca0f6f7196ab1666dc6da2a1bc1dd4369e5b617b13fcc298d7ec6dc3190
translation: machine
translated_at: '2026-10-24'
---
# Canon UltraReal {#canon-ultrareal}

**Entwicklungsstrang:** `project:canon-ultrareal` · Thread `canon-ultrareal-public-model-listing`  
**Letztes Ereignis:** 2026-07-19 · 1 datiertes seit 2026-07-19 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Canon UltraReal ist ein LoRA unter Apache-2.0 für Text-zu-Bild-Workflows mit Krea-2-Raw, trainiert auf Fotografien der Canon 1Ds. Bei 114 MB passt es Farbwiedergabe, Motivfreistellung und Bokeh für Brennweiten von 28 mm, 50 mm, 100 mm und 500 mm an. Es wirkt als eng gefasster Kamera-Look-Adapter und nicht als eigenständiger Checkpoint oder allgemeines Realismus-Modell.

## Entwicklungsstrang {#development-line}

- **2026-07-19 — Canon UltraReal wurde öffentlich auf Civitai und Hugging Face gelistet.** Civitai und Hugging Face haben am 2026-07-19 öffentliche Modellseiten hinzugefügt. Das markiert einen Meilenstein der öffentlichen Verbreitung des Projekts, wobei die Quelle keine Version, Gewichtsänderung, Release Notes oder den Originaltext der Meldung nennt.

## Was sich geändert hat {#what-changed}

2026-07-19 — Canon UltraReal wurde als LoRA für Krea-2-Raw verfügbar; die primäre Modellkarte definiert das Repository, das Basismodell, die Trainingsquelle Canon 1Ds und die empfohlene Stärke von 0.8.

Es wurde kein separat datiertes Nachfolge-Release verifiziert. Die einzige gehostete Gewichtsdatei ist canon_krea2.safetensors (114 MB; SHA-256 3295dec59ab1195631fe9b3dd3493ba9c1546056da86179cc3119c4b029420ce).

## So wird es verwendet {#how-to-use-this}

Ab 2026-07-19 lassen sich Canon UltraReal über die verlinkten Civitai- und Hugging-Face-Seiten finden; Version und Nutzungsdetails sollten direkt auf diesen Ressourcen überprüft werden.

1. Diffusers, Transformers und Accelerate installieren bzw. aktualisieren, dann Danrisi/Canon_UltraReal mit DiffusionPipeline auf CUDA laden; bfloat16 verwenden, sofern unterstützt.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
2. Krea-2-Raw als Basismodell festlegen und die LoRA-Stärke auf 0.8 setzen.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
3. Prompts mit c2n0n beginnen, die Szene beschreiben und Brennweiten-Hinweise wie 28mm oder 50mm ergänzen.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>

## Bewährte Vorgehensweisen {#best-practices}

- Mit einer LoRA-Stärke von 0.8 beginnen und erst nach dem Vergleich der Ausgaben mit dem beabsichtigten Motiv und der Komposition anpassen.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
- Brennweiten bewusst wählen: Die Trainingsbilder umfassen 28 mm, 50 mm, 100 mm und 500 mm, daher verschiebt sich der Charakter mit den Objektiv-Hinweisen und dem Bildausschnitt.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
- Bei Krea-2-Raw bleiben; die Modellkarte belegt keine Kompatibilität mit anderen Basismodellen.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>

## Hierdurch ersetzt {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die Civitai-Spiegel-URL für das Ereignis vom 2026-07-19 konnte nicht geladen werden; Versionsmetadaten, Veröffentlichungszeitstempel und Hinweise zum Workflow sind daher nicht verifiziert.
- Keine Quelle aus erster Hand stimmt direkt mit dem Veröffentlichungszeitstempel vom 2026-07-19 überein. Die primäre Modellkarte bestätigt den technischen Umfang und das Basismodell, nicht aber den genauen Eintrag zum Veröffentlichungstag.
- Das Ausgabeschema enthält keine Felder event_findings und new_events, daher erscheinen die Belege zu Ereignissen unter what_changed und unknowns.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/Danrisi/Canon_UltraReal | Danrisi/Canon_UltraReal · Hugging Face | 2026-09-05 |
| https://huggingface.co/Danrisi/Canon_UltraReal/blob/main/canon_krea2.safetensors | canon_krea2.safetensors · Danrisi/Canon_UltraReal | 2026-09-05 |
| https://huggingface.co/Danrisi/Canon_UltraReal/commit/847c2a1cc7e191f5b3d4451deec984044f4ceabc | Modell über HuggingFace Uploader aktualisiert · Danrisi/Canon_UltraReal | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:canon-ultrareal`, Thread `canon-ultrareal-public-model-listing`, 1 datiertes Ereignis 2026-07-19 → 2026-07-19.
- **Praktischer Hinweis:** Ab 2026-07-19 sollten Anwender die verlinkten Civitai- und Hugging-Face-Seiten als dokumentierte öffentliche Fundstellen für Canon UltraReal nutzen und die genaue Version sowie die Nutzungsdetails direkt auf diesen Ressourcen überprüfen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

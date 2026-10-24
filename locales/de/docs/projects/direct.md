---
title: "DIRECT"
category: projects
date: 2026-06-09
tags: [direct, direct-development, project]
aliases: ["DIRECT"]
level: 2
source_sha256: f4f89f42e1d7dc9cc4b1ed4be4bc61319841badb78de7bef16429624422e766a
translation: machine
translated_at: '2026-10-24'
---
Wait — I need to be careful. The instructions say @@CODE_<n>@@ placeholders exist, but the input contains none. So I simply translate. Let me produce the translation now.

---
title: DIRECT
category: projects
date: 2026-06-09
tags: [direct, direct-development, project]
aliases: ["DIRECT"]
---

# DIRECT {#direct}

**Entwicklungslinie:** `project:direct` · Thread `direct-development`  
**Letztes Ereignis:** 2026-06-09 · 1 datiertes seit 2026-06-09 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

DIRECT ist ein posensteuerbares System zum Einfügen von Objekten für Compositing, das ein Referenzobjekt in einen Hintergrund platziert.

- Erscheinungsbild des Referenzobjekts: erhält das Erscheinungsbild des Referenzobjekts.
- 3D-Proxy: verwendet einen rekonstruierten 3D-Proxy für die Pose.
- Szenenkontext: berücksichtigt den Szenenkontext.

Das initiale Gewichtspaket hat 987 MB, benötigt aber externe FLUX-, TRELLIS-, SigLIP2- und RMBG-Komponenten. Verwenden Sie es als lokalen, GPU-gestützten Compositing-Workflow und nicht als eigenständiges gehostetes Modell.

## Entwicklungslinie {#development-line}

- **2026-06-09 — Projektressourcen von DIRECT wurden verlinkt.** Am 2026-06-09 verlinkte eine Nachricht der DIRECT-Entwicklungslinie die Projektwebsite, das Quell-Repository und die Hugging-Face-Seite. Zusammengenommen deuten diese datierten Links auf einen öffentlichen Projektmeilenstein hin, der für die Entwicklungshistorie geeignet ist. Wir haben den Ankündigungstext und den genauen Status jeder verlinkten Ressource nicht geprüft.

## Was sich geändert hat {#what-changed}

- **2026-05** — DIRECT wurde für die ICML 2026 angenommen; Repository und Projektseite wurden verfügbar.
- **2026-06-04** — DIRECT-Paper v1 erschien auf arXiv und definierte den Workflow aus Referenzobjekt, 3D-Proxy und Hintergrund.
- **2026-06-09** — superGong veröffentlichte das initiale DIRECT-Image-to-Image-Modell.
- **2026-06-30** — Aktivität der Autoren verzeichnete die Veröffentlichung und Aktualisierung von DIRECT-dataset.
- **2026-07** — Das Repository gibt an, dass Trainingsdaten, Trainingscode und Preprocessing-Code veröffentlicht wurden; ein Tag wird nicht genannt.

## Verwendung {#how-to-use-this}

1. Klonen Sie das Repository, erstellen Sie die getestete Python-3.10.18-Umgebung, installieren Sie PyTorch 2.4.0 mit CUDA 11.8 und installieren Sie anschließend die Anforderungen und DIRECT.
  — <https://github.com/Gong1130/DIRECT>
2. Akzeptieren Sie vor dem ersten Start die Lizenzen für die gated Modelle FLUX.1-Fill-dev und RMBG-2.0 und authentifizieren Sie sich dann bei Hugging Face oder setzen Sie HF_TOKEN, damit die benötigten Modelle heruntergeladen werden können.
  — <https://github.com/Gong1130/DIRECT>
3. Führen Sie `python demo/demo.py --gradio_port 7860 --viser_port 8081` aus; die Oberfläche segmentiert und rekonstruiert das Referenzobjekt und erlaubt anschließend, seine 3D-Pose im Hintergrund zu verändern.
  — <https://huggingface.co/superGong/DIRECT>
4. Auf einer entfernten Maschine leiten Sie beide Ports 7860 und 8081 weiter, bevor Sie die lokale Gradio-Oberfläche öffnen.
  — <https://github.com/Gong1130/DIRECT>

## Best Practices {#best-practices}

- Verwenden Sie den von den Autoren getesteten Stack aus Python 3.10.18, PyTorch 2.4.0 und CUDA 11.8; setzen Sie CUDA_HOME, falls kompilierte Erweiterungen das Toolkit nicht finden.
  — <https://github.com/Gong1130/DIRECT>
- Planen Sie den vollständigen Abhängigkeitsstapel ein: Das DIRECT-Paket mit 987 MB enthält nur die eigenen Gewichte, nicht die benötigten FLUX-, TRELLIS-, SigLIP2- und Hintergrundentfernungsmodelle.
  — <https://huggingface.co/superGong/DIRECT>
- Prüfen Sie vor dem Einsatz die Bedingungen für kommerzielle Nutzung: Die Repository-Lizenz erlaubt nichtkommerzielle Nutzung und verweist kommerzielle Nutzer an die Mitwirkenden.
  — <https://github.com/Gong1130/DIRECT/blob/main/LICENSE.txt>

## Hiermit überholt {#superseded-by-this}

- 2026-07: Die Annahme aus dem Juni, DIRECT enthalte nur Inferenzcode, eine Demo und Gewichte, ist überholt; das Repository gibt an, dass Trainingsdaten, Trainingscode und Preprocessing-Code veröffentlicht wurden.

## Weiterhin unbekannt {#still-unknown}

- Die Release-Notiz des Repositorys vom Juli nennt keinen genauen Tag, daher kann dieses Release nicht als zeitgestempeltes neues Ereignis erfasst werden.
- Die README enthält weiterhin TODO-Punkte für Assets, die laut dem datierten News-Abschnitt veröffentlicht wurden; kein unveränderlicher Release-Tag löst diese Inkonsistenz eindeutig auf.
- Wir haben keinen unabhängigen, aktuellen Benchmark und keinen lokalen End-to-End-Lauf gefunden; Leistungsangaben bleiben von den Autoren berichtet.
- Die gefundene chinesischsprachige Berichterstattung ist eine Methodenzusammenfassung, kein unabhängiger chinesischer Einrichtungsleitfaden, Fehlerbericht oder Benchmark.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://gong1130.github.io/DIRECT/ | DIRECT-Projektseite | 2026-09-07 |
| https://github.com/Gong1130/DIRECT | Gong1130/DIRECT-Repository und Release-Notizen | 2026-09-07 |
| https://huggingface.co/superGong/DIRECT | superGong/DIRECT-Modellkarte | 2026-09-07 |
| https://huggingface.co/superGong/activity/all | superGong Hugging-Face-Aktivität | 2026-09-07 |
| https://huggingface.co/superGong/DIRECT/tree/2ec64cedd13ed7f2f81edf836ce6a90d503c3683 | DIRECT-Initialmodell-Revision | 2026-09-07 |
| https://arxiv.org/abs/2606.06601 | DIRECT-arXiv-Paper | 2026-09-07 |
| https://github.com/Gong1130/DIRECT/blob/main/LICENSE.txt | DIRECT-Lizenz | 2026-09-07 |
| https://hyper.ai/cn/papers/2606.06601 | Vereinfacht-chinesische DIRECT-Methodenzusammenfassung | 2026-09-07 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:direct`, Thread `direct-development`, 1 datiertes Ereignis 2026-06-09 → 2026-06-09.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Verwendung und Best Practices oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Überholungsvermerke sind maßgeblich dafür, was veraltet ist.

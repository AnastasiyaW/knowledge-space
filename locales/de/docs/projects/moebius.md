---
title: "Moebius — Öffentliche Verfügbarkeit"
category: projects
date: 2026-06-20
tags: [moebius, project, public-availability]
aliases: ["Moebius"]
level: 2
source_sha256: 89dfa8260f92c0d93775e5579ec444d6cfca943fd653b19f2c44943a7e72298d
translation: machine
translated_at: '2026-10-24'
---
# Moebius — Öffentliche Verfügbarkeit {#moebius-public-availability}

**Entwicklungslinie:** `project:moebius` · Thread `public-availability`  
**Letztes Ereignis:** 2026-06-20 · 1 datiertes Ereignis seit 2026-06-20 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Moebius ist ein offenes Framework für Image-Inpainting für Entwickler, die ein Bild und eine passende Maske bereitstellen.
- Vortrainierte Checkpoints sowie Checkpoints für Places2, CelebA-HQ und FFHQ für domänenspezifische Auffüllungen.
- Inferenzpfad über das Repository für skriptgesteuerte lokale Läufe.
- Ladepfad über Hugging Face Diffusers für die Integration in Pipelines.

Es läuft mit 226M Parametern bei 26,01 ms pro Schritt auf der vom Autorenteam getesteten GPU. Es arbeitet als Spezialist für maskierte Auffüllungen und Objektentfernung, nicht als gehosteter Universaldienst für Generierung.

## Entwicklungslinie {#development-line}

- **2026-06-20 — Die Projektressourcen von Moebius wurden öffentlich geteilt.** Am 2026-06-20 verlinkte eine Nachricht zu Moebius die Projektwebseite, das GitHub-Repository und die Hugging-Face-Seite. Wir werten dies als wesentlichen Meilenstein der öffentlichen Verfügbarkeit, da es Leser auf die öffentlich zugänglichen Ressourcen des Projekts verweist, während sich der genaue Release-Stand oder die Fähigkeiten allein anhand der übermittelten Links nicht feststellen lassen.

## Was sich geändert hat {#what-changed}

2026-06-20 — Moebius war als Projektseite, öffentliches Repository und Hugging-Face-Modell verfügbar; Material der Urheber beschreibt es als 0.22B-Spezialisten für Image-Inpainting.

Ereignisbefund für 2026-06-20 — Die Repository-Ankündigung vom 18. Juni 2026 besagt, dass der Umfang Trainingscode, Inferenzcode und öffentliche Gewichte mit Checkpoints für die Varianten pretrained, Places2, CelebA-HQ und FFHQ umfasste; es handelte sich nicht um ein paketiertes GitHub-Release.

Neue Ereignisse: 2026-06-16 — Das Repository wurde laut seinen datierten Projektnachrichten erstmals öffentlich eingereicht. 2026-06-17 — arXiv v1 (2606.19195) wurde eingereicht; sie dokumentiert das LλMI-Backbone und die Latent-Space-Multi-Granularity-Distillation. 2026-06-18 — Die Autoren kündigten die Annahme bei ECCV 2026 an und veröffentlichten das Preprint, den Code und die Gewichte. 2026-06-19 — Das Projekt meldete das Erreichen des täglichen Spitzenplatzes Nr. 1 auf Hugging Face; dies ist ein Sichtbarkeitsnachweis, keine Modellrevision. 2026-06-25 — Das Projekt meldete einen Wochenrang 4/105 auf Hugging Face; dies ist ein Sichtbarkeitsnachweis, keine Modellrevision.

## Verwendung {#how-to-use-this}

Stand 2026-06-20 sollten Praktiker die Projekt-, Code- und Hugging-Face-Seiten von Moebius als Ausgangspunkt für die Evaluation heranziehen; allein diese Belege begründen weder eine bestimmte Version, Fähigkeit, Lizenz noch eine Empfehlung für den Einsatz.

1. Repository klonen, die dokumentierte Umgebung anlegen und die festgelegten Abhängigkeiten installieren, bevor der Repository-Workflow verwendet wird.
  — <https://github.com/hustvl/Moebius>
2. VAE sowie den vortrainierten oder aufgabenspezifischen Checkpoint herunterladen und dabei die dokumentierte Verzeichnisstruktur der Gewichte beibehalten.
  — <https://github.com/hustvl/Moebius>
3. Jedes Quellbild und seine Maske in getrennte Verzeichnisse mit übereinstimmenden Dateinamen legen und anschließend `infer.infer_moebius` mit der gewählten Modellkonfiguration, dem Checkpoint, den Eingabeverzeichnissen, dem Ausgabeverzeichnis, dem CFG-Wert, der Batchgröße und der Anzahl der Worker ausführen.
  — <https://github.com/hustvl/Moebius>
4. Für den Hub-Pfad diffusers, transformers und accelerate installieren und anschließend `hustvl/Moebius` über `DiffusionPipeline` laden; die Ausgabe vor dem Einsatz für maskierte Bearbeitung gegen den Repository-Pfad validieren.
  — <https://huggingface.co/hustvl/Moebius>

## Best Practices {#best-practices}

- Für Inpainting den Image-und-Masken-Inferenzpfad des Repositorys verwenden; Dateistruktur und Befehl kodieren den maskenbasierten Workflow explizit.
  — <https://github.com/hustvl/Moebius>
- Einen Checkpoint wählen, der zur Bilddomäne passt – Places2 für natürliche Szenen, CelebA-HQ oder FFHQ für Porträts – und Benchmark-Aussagen nicht als Beleg für eine fremde Domäne behandeln.
  — <https://hustvl.github.io/Moebius/>
- Bei der Reproduktion des Workflows die im Repository aufgeführten Versionen von Torch, Diffusers, Transformers und flash-linear-attention festschreiben; die Hub-Seite zeigt ein separates generisches Diffusers-Beispiel.
  — <https://github.com/hustvl/Moebius>
- Die gemeldeten 26,01 ms pro Schritt und die Beschleunigung um mehr als das 15-Fache als Benchmark-Aussagen der Autoren behandeln, nicht als Garantie für Latenz im Betrieb.
  — <https://arxiv.org/abs/2606.19195>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-06-18 — Die Aussage, Moebius sei nur ein Paper oder eine Projektseite, ist veraltet: Materialien der Urheber besagen, dass Code und Gewichte veröffentlicht wurden.
- 2026-09-05 — Die Empfehlung, ein GitHub-Release-Artefakt zu installieren, ist nicht gedeckt: Die Releases-Seite des Repositorys zeigt keine Releases. Stattdessen Quellcode-Checkout und Hub-Checkpoints verwenden.

## Weiterhin ungeklärt {#still-unknown}

- Die Hugging-Face-Seite nennt als Modelllizenz MIT, während die README des Repositorys für Code und vortrainierte Gewichte Apache-2.0 angibt. Vor einem kommerziellen Einsatz die vorgesehene Lizenz bei den Maintainern bestätigen.
- Das bereitgestellte Schema enthält keine Felder event_findings oder new_events; deren erforderlicher Inhalt ist in what_changed enthalten.
- Für die angegebene Aussage von 26,01 ms pro Schritt bzw. die Beschleunigung um mehr als das 15-Fache wurde keine unabhängige Reproduktion auf Hardware gefunden.
- Das generische Hugging-Face-Diffusers-Beispiel wirkt nur promptbasiert, während das Repository Image-und-Masken-Inpainting dokumentiert; die genaue Maskierungsschnittstelle der Hub-Pipeline wurde nicht unabhängig verifiziert.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://hustvl.github.io/Moebius/ | Moebius-Projektseite | 2026-09-05 |
| https://github.com/hustvl/Moebius | hustvl/Moebius-Repository | 2026-09-05 |
| https://huggingface.co/hustvl/Moebius | hustvl/Moebius-Modellkarte | 2026-09-05 |
| https://arxiv.org/abs/2606.19195 | Moebius: 0.2B Lightweight Image Inpainting Framework with 10B-Level Performance | 2026-09-05 |
| https://github.com/hustvl/Moebius/releases | Moebius-GitHub-Releases | 2026-09-05 |

## Kurzbriefing für Agenten {#agent-brief}

- **Gegenstand:** `project:moebius`, Thread `public-availability`, 1 datiertes Ereignis 2026-06-20 → 2026-06-20.
- **Praktischer Hinweis:** Stand 2026-06-20 sollten Praktiker die Projekt-, Code- und Hugging-Face-Seiten von Moebius als Ausgangspunkt für die Evaluation heranziehen; allein diese Belege begründen weder eine bestimmte Version, Fähigkeit, Lizenz noch eine Empfehlung für den Einsatz.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

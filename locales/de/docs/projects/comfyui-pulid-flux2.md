---
title: "ComfyUI-PuLID-Flux2 — PuLID-Flux2-Integration für ComfyUI"
category: projects
date: 2026-03-16
tags: [comfyui-pulid-flux2, project, pulid, pulid-flux2-comfyui-integration]
aliases: ["ComfyUI-PuLID-Flux2"]
level: 2
source_sha256: 612b7404a3d7c1221ef00238edf37e2547cede6dcb877a80196856aee5417d8c
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI-PuLID-Flux2 — PuLID-Flux2-Integration für ComfyUI {#comfyui-pulid-flux2-pulid-flux2-comfyui-integration}

**Entwicklungslinie:** `project:comfyui-pulid-flux2` · Thread `pulid-flux2-comfyui-integration`  
**Letztes Ereignis:** 2026-03-16 · 1 datiertes Ereignis seit 2026-03-16 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

ComfyUI-PuLID-Flux2 ist eine Adaption von PuLID für ComfyUI und FLUX.2. Sie lädt die InsightFace-AntelopeV2-, EVA-CLIP- und PuLID-Gewichte und wendet die Identität anschließend vor dem Sampling auf das Modell an. Funktionen: Klein 4B/9B und Dev, Gesichtsauswahl per Index, Debug-Ansicht, fertiger Klein-Workflow. Einschränkung: EVA-CLIP lädt automatisch etwa 800 MB nach, und Training-Skripte wurden als instabil entfernt. Fazit: geeignet für identitätserhaltende Porträt-Workflows; dafür sollten native Flux.2-Gewichte verwendet und die Kompatibilität des jeweiligen Modells geprüft werden.

## Entwicklungslinie {#development-line}

- **2026-03-16 — Setup-Ressourcen für ComfyUI-PuLID-Flux2 wurden verlinkt.** Am 2026-03-16 wurde das ComfyUI-PuLID-Flux2-Repository zusammen mit seinem Workflow-Verzeichnis und den externen PuLID- und antelopev2-Modellressourcen verlinkt. Dies markiert einen praktischen Integrationsbezugspunkt für das Projekt, die vorliegenden Belege belegen jedoch weder ein Release, eine Version noch eine konkrete Implementierungsänderung.

## Was sich geändert hat {#what-changed}

2026-03-16 — v0.2.1 behob eine Dimension-Mismatch beim Wechsel zwischen Flux.2 Klein und Dev; am selben Tag wurden Verbindung und Namen im Beispiel-Workflow korrigiert. 2026-03-17 — der dtype-Konflikt FP16/BF16 wurde behoben. 2026-03-20 — v0.3.0 behob Single Blocks, half/bfloat16, den Sigma-Bereich und EVA-CLIP 3D; zudem wurde eine Training-Pipeline für Vast.ai ergänzt. 2026-03-21 — v0.4.0 ergänzte safetensors, Gewichte auf Hugging Face und aktualisierte Einstellungen. 2026-03-25—2026-03-28 — v0.5.0 ergänzte neue Gewichte; v0.6.0 ergänzte native v1/v2; v0.6.2 stellte die Unterstützung für Dev32 wieder her. 2026-03-30 und 2026-04-24 — eine Umgehung der Erkennung über model_function_wrapper sowie ein Schutz gegen kumulatives Monkey-Patching von block.forward wurden eingeführt.

## Anwendung {#how-to-use-this}

Ab dem 2026-03-16 sollten Anwender beim Vorbereiten eines ComfyUI-PuLID-Flux2-Setups die verlinkten Projekt-Workflows zusammen mit den referenzierten PuLID- und antelopev2-Modellquellen verwenden. Exakte Versions- und Installationsanforderungen sind separat zu prüfen.

1. Klonen Sie den Custom Node nach ComfyUI/custom_nodes und installieren Sie die angegebenen Abhängigkeiten; führen Sie die vollständige requirements.txt nicht in einer bereits laufenden ComfyUI-Installation aus.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2>
2. Laden Sie den nativen PuLID-Flux2-Checkpoint herunter und legen Sie ihn in ComfyUI/models/pulid/ ab.
  — <https://huggingface.co/Fayens/Pulid-Flux2>
3. Legen Sie die AntelopeV2-Dateien in ComfyUI/models/insightface/models/antelopev2/ ab.
  — <https://huggingface.co/MonsterMMORPG/InstantID_Models/tree/main/models/antelopev2>
4. Importieren Sie den Klein-Workflow und verbinden Sie das Referenzfoto, das Flux.2-Modell, das PuLID-Modell, EVA-CLIP und InsightFace mit Apply PuLID Flux.2.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2/tree/main/workflows>

## Best Practices {#best-practices}

- Beginnen Sie mit einer Stärke von 1.0. Die Dokumentation des Autors nennt 1.4 als empfohlene Einstellung, der Wert sollte jedoch erst nach visueller Prüfung von Identität und Artefakten erhöht werden.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2>
- Verwenden Sie für Flux.2 die nativen Checkpoint-Gewichte v1/v2 und nicht die ursprünglichen PuLID-FLUX-v0.9.x-Gewichte: Letztere gehören zu einer früheren FLUX-Linie.
  — <https://huggingface.co/Fayens/Pulid-Flux2>
- Installieren Sie eva_clip nicht direkt von GitHub; der Loader des Projekts bezieht EVA-CLIP automatisch.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-03-16: Die Anleitung für Workflows, die davon ausgingen, dass Klein und Dev ohne Neuaufbau des PuLID-Moduls gewechselt werden können, ist veraltet; v0.2.1 behob die Dimension-Mismatch.
- 2026-03-17: Harte Annahmen über einen einzigen FP16/BF16-Pfad sind veraltet; der dtype-Konflikt wurde behoben.
- 2026-03-26: Die Anleitung vor den nativen Gewichten ist für Flux.2 durch die nativen PuLID-Flux2-Gewichte v1/v2 abgelöst.

## Weiterhin ungeklärt {#still-unknown}

- Die erforderlichen Felder event_findings und new_events fehlen im bereitgestellten Ausgabeschema; ihre prüfbare Chronologie ist in what_changed enthalten. Für das Ereignis vom 2026-03-16 liefert die GitHub-Historie ein eigenes Datum und eine genaue Korrektur: v0.2.1 behob die Dimension-Mismatch zwischen Klein und Dev, und der Workflow erhielt eine Korrektur der Verbindung.
- Das Repository meldet Unterstützung für Klein und Dev, stellt jedoch weder einen unabhängigen Identitäts-Benchmark, ein VRAM-Profil noch eine Stabilitätsgarantie für alle FLUX.2-Varianten bereit.
- Das ursprüngliche guozinan/PuLID veröffentlicht PuLID-FLUX-v0.9.0/v0.9.1 für die frühe FLUX-Linie; dies ist nicht derselbe Checkpoint wie die nativen PuLID-Flux2-v1/v2-Gewichte.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/iFayens/ComfyUI-PuLID-Flux2 | iFayens/ComfyUI-PuLID-Flux2 README | 2026-09-05 |
| https://github.com/iFayens/ComfyUI-PuLID-Flux2/commits/main | iFayens/ComfyUI-PuLID-Flux2 Commit-Historie | 2026-09-05 |
| https://github.com/iFayens/ComfyUI-PuLID-Flux2/tree/main/workflows | ComfyUI-PuLID-Flux2 Workflows | 2026-09-05 |
| https://huggingface.co/Fayens/Pulid-Flux2 | Fayens/Pulid-Flux2 Modell-Repository | 2026-09-05 |
| https://huggingface.co/MonsterMMORPG/InstantID_Models/tree/main/models/antelopev2 | MonsterMMORPG/InstantID_Models AntelopeV2-Dateien | 2026-09-05 |
| https://huggingface.co/guozinan/PuLID | guozinan/PuLID Model Card | 2026-09-05 |

## Agent Brief {#agent-brief}

- **Gegenstand:** `project:comfyui-pulid-flux2`, Thread `pulid-flux2-comfyui-integration`, 1 datiertes Ereignis vom 2026-03-16 bis 2026-03-16.
- **Praktischer Hinweis:** Ab dem 2026-03-16 sollten Anwender beim Vorbereiten eines ComfyUI-PuLID-Flux2-Setups die verlinkten Projekt-Workflows zusammen mit den referenzierten PuLID- und antelopev2-Modellquellen verwenden. Exakte Versions- und Installationsanforderungen sind separat zu prüfen.
- **Konfidenz:** hoch. Die datierten Supersedes-Einträge oben sind maßgeblich dafür, was veraltet ist.

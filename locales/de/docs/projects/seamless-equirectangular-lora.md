---
title: "Seamless-Equirectangular LTX-2.3 LoRA — Seamless-Equirectangular-LoRA-Veröffentlichung"
category: projects
date: 2026-07-07
tags: [project, seamless-equirectangular-lora, seamless-equirectangular-lora-release]
aliases: ["Seamless-Equirectangular LTX-2.3 LoRA"]
level: 2
source_sha256: 644814fd98da6afc7dc664c3d06d991abe915e2c327509fbb80100339ae86610
translation: machine
translated_at: '2026-10-24'
---
# Seamless-Equirectangular LTX-2.3 LoRA — Seamless-Equirectangular-LoRA-Veröffentlichung {#seamless-equirectangular-ltx-23-lora-seamless-equirectangular-lora-release}

**Entwicklungslinie:** `project:seamless-equirectangular-lora` · Thread `seamless-equirectangular-lora-release`  
**Letztes Ereignis:** 2026-07-07 · 1 datiertes seit 2026-07-07 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Seamless-Equirectangular LTX-2.3 LoRA ist ein Adapter mit Rang 128 zur Erzeugung von 360°-Equirectangular-Videos in LTX-2.3 über ComfyUI.

Funktionen:

- Text-to-Video mit dem Trigger `Equirectangular`;
- Beseitigung der Naht durch Circular VAE und Per-Step-Latent-Roll;
- Behandlung der Pole durch EquiRoPE und geometrischen CFG;
- Outpaint eines gewöhnlichen Videos auf 360° über einen separaten VR-Outpaint-Workflow.

Einschränkung: Die LoRA wurde über 15 000 Schritte trainiert; laut Angaben des Autors erzeugt die Basis-LTX-2.3 ohne sie keine Equirectangular-Ausgabe, und ein gehosteter Inference-Provider existiert nicht.

Fazit: Dies ist eine praktische lokale ComfyUI-Pipeline und kein eigenständiges Cloud-Modell.

## Entwicklungslinie {#development-line}

- **2026-07-07 — Öffentliche Ressourcen für Seamless-Equirectangular LTX-2.3 LoRA verlinkt.** Seamless-Equirectangular LTX-2.3 LoRA und ComfyUI-Node-Pack. Die Modellkarte präzisiert die Adapterparameter: Rang 128, 15 000 Schritte, Trigger `Equirectangular`. Das Repository präzisiert, dass die LoRA für die Equirectangular-Darstellung zuständig ist, während Circular VAE und Per-Step-Roll die Naht schließen. Spätere aktuelle README-Materialien ergänzen Unterstützung für Krea2 und MiniMax H3, doch die Primärseiten liefern kein verlässliches Datum dieser Erweiterungen, weshalb sie keinem eigenen datierten Ereignis zugeordnet werden.

## Was sich geändert hat {#what-changed}

2026-07-07 — Das zusammengehörige Paket wurde veröffentlicht: Seamless-Equirectangular LTX-2.3 LoRA und ComfyUI-Node-Pack. Die Modellkarte präzisiert die Adapterparameter: Rang 128, 15 000 Schritte, Trigger `Equirectangular`. Das Repository präzisiert, dass die LoRA für die Equirectangular-Darstellung zuständig ist, während Circular VAE und Per-Step-Roll die Naht schließen. Spätere aktuelle README-Materialien ergänzen Unterstützung für Krea2 und MiniMax H3, doch die Primärseiten liefern kein verlässliches Datum dieser Erweiterungen, weshalb sie keinem eigenen datierten Ereignis zugeordnet werden.

## Verwendung {#how-to-use-this}

Ab 2026-07-07 sollten Praktiker die verlinkte Hugging-Face-LoRA und die ComfyUI-Erweiterung als zusammengehörigen Ausgangspunkt betrachten, wenn sie nahtlose Equirectangular-Workflows für LTX-2.3 evaluieren.

1. Installieren Sie ComfyUI-Seamless-Equirectangular im Verzeichnis custom nodes von ComfyUI und starten Sie ComfyUI neu.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular>
2. Laden Sie den Adapter wie eine gewöhnliche LTX-2.3-LoRA und fügen Sie dem Prompt das Wort `Equirectangular` hinzu.
  — <https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA>
3. Öffnen Sie den beigefügten T2V-Workflow und verwenden Sie das Node-Pack: Es ergänzt EquiRoPE, geometrischen CFG, Per-Step-Roll, Circular VAE und Wrapped Noise.
  — <https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA>
4. Um ein perspektivisches Video auf 360° zu erweitern, verwenden Sie den separaten VR-Outpaint-Workflow und ComfyUI-VR-Outpaint-Tools; diese LoRA wird gemeinsam mit der VR-Outpaint-IC-LoRA angewendet.
  — <https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA>

## Bewährte Praktiken {#best-practices}

- Beginnen Sie für LTX mit LoRA + Per-Step-Roll + Circular VAE: Die Positionspatches verbessern die Geometrie, ersetzen aber nicht die LoRA.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>
- Bei wiederkehrenden oder spiegelsymmetrischen Objekten verwenden Sie `dual_average` nicht; wechseln Sie zu `random_per_step` oder deaktivieren Sie den Roll.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>
- Setzen Sie für schnelle Schwenks `start_percent` auf 0.2–0.3, damit zuerst die Szenenstruktur festgelegt und danach die Naht behandelt wird.
  — <https://github.com/Betrachtung/...>
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>
- Betrachten Sie Latent- oder Image-Seam-Blend nicht als Korrektur nicht übereinstimmender Objekte: Er ist nur ein schmaler kosmetischer Fallback für einen verbleibenden Farbsprung.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>

## Dadurch ersetzt {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die Primärseiten liefern keine verlässlichen Daten für die späteren Erweiterungen Krea2 und MiniMax H3, weshalb sie nicht als neue datierte Ereignisse erfasst sind.
- Aussagen zur Qualität, zum Produktionseinsatz und zum Vergleich der Komponenten stammen vom Projektautor; in den verwendeten Quellen gibt es keine unabhängige, reproduzierbare Bewertung.
- Der erfasste Link wurde nicht verwendet: Die Seite ließ sich über den verfügbaren Webzugriff nicht öffnen.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA | TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA — Model Card | 2026-09-05 |
| https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular | Burgstall-labs/ComfyUI-Seamless-Equirectangular | 2026-09-05 |
| https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md | ComfyUI-Seamless-Equirectangular README | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:seamless-equirectangular-lora`, Thread `seamless-equirectangular-lora-release`, 1 datiertes Ereignis 2026-07-07 → 2026-07-07.
- **Praktischer Hinweis:** Ab 2026-07-07 sollten Praktiker die verlinkte Hugging-Face-LoRA und die ComfyUI-Erweiterung als zusammengehörigen Ausgangspunkt betrachten, wenn sie nahtlose Equirectangular-LTX-2.3-Workflows evaluieren.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich für die Frage, was veraltet ist.

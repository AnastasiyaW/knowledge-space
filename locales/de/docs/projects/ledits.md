---
title: "LEDITS"
category: projects
date: 2023-12-03
tags: [ledits, ledits-development, project]
aliases: ["LEDITS", "LEDITS++"]
level: 3
source_sha256: a4211dc7eccce2b28451d39f784dbc13643455f220f87387a5208d1f17a23643
translation: machine
translated_at: '2026-10-24'
---
# LEDITS {#ledits}

**Entwicklungslinie:** `project:ledits` · Thread `ledits-development`  
**Letztes Ereignis:** 2023-12-03 · 2 datierte Ereignisse seit 2023-07-04 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

LEDITS ist eine Pipeline zur Bildbearbeitung, mit der echte Bilder über semantische Textprompts verändert werden, statt einen generischen img2img-Durchlauf zu verwenden.

- Inversion: Invertiert das Eingabebild vor der Bearbeitung.
- Guidance: Wendet ein oder mehrere Konzept-Prompts an.
- Masking: Verwendet implizite Masken, um Änderungen auf relevante Bereiche zu beschränken.
- Integration: Stellt Stable-Diffusion- und SDXL-Pipelines in Diffusers bereit.

Der ursprüngliche LEDITS-Space ist pausiert, und die Diffusers-Implementierung garantiert keine perfekte Inversion. Verwende LEDITS++ lokal für semantische Bearbeitungen mit Stable Diffusion oder SDXL; verwende die Implementierung der Autoren, wenn die Treue der Inversion das Ergebnis sein muss.

## Entwicklungslinie {#development-line}

- **2023-07-04 — Öffentliche LEDITS-Demo und Hugging-Face-Space wurden verlinkt.** Am 2023-07-04 verlinkte der LEDITS-Entwicklungsthread eine öffentliche Web-Demo, den Hugging-Face-Space und das Repository editing-images/ledits. Diese Links belegen weder den Umfang einer Veröffentlichung noch eine Modellversion oder Fähigkeiten.
- **2023-12-03 — Öffentliche LEDITS++-Demo und Hugging-Face-Space wurden verlinkt.** Am 2023-12-03 verlinkte der Thread eine öffentliche LEDITS++-Demo, den Hugging-Face-Space und das Repository editing-images/leditsplusplus. Außerdem verlinkte er zurück auf LEDITS. Diese Links bestätigen die genaue technische Beziehung zwischen LEDITS und LEDITS++ nicht.

## Was sich geändert hat {#what-changed}

- 2023-07-04 — LEDITS kombinierte Edit-Friendly-DDPM-Inversion mit SEGA-Semantic-Guidance für die Bearbeitung echter Bilder auf Stable Diffusion v1.5.
- 2023-12-03 — LEDITS++ führte SDE-DPM-Solver++-Inversion, implizites Masking pro Bearbeitung und native gleichzeitige Bearbeitungen ein.

## Verwendung {#how-to-use-this}

Stand 2023-12-03 sollte man die ursprünglichen öffentlichen LEDITS-Artefakte von den separat verlinkten LEDITS++-Artefakten unterscheiden und für die jeweils gewünschte Variante den passenden Hugging-Face-Space oder das passende Repository konsultieren.

1. Wähle `LEditsPPPipelineStableDiffusion` für Stable Diffusion oder `LEditsPPPipelineStableDiffusionXL` für SDXL und lade anschließend einen kompatiblen Basis-Checkpoint auf CUDA.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
2. Rufe `invert(image=...)` für jedes neue Ausgangsbild auf, bevor du die Bearbeitungs-Pipeline ausführst; die Bearbeitung verwendet immer die letzte Inversion.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
3. Verwende `source_prompt` nur, wenn geführte Inversion hilft; ein leerer Source-Prompt deaktiviert diese Führung.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
4. Übergib einen oder mehrere `editing_prompt`-Werte und stimme `reverse_editing_direction`, `edit_guidance_scale` und `edit_threshold` auf diese Prompts ab; die Richtung steuert, ob jedes Konzept verstärkt oder abgeschwächt wird.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
5. Prüfe die Rekonstruktion der Inversion und das Bearbeitungsergebnis; wenn exakte Inversion erforderlich ist, verwende das Repository der Autoren statt der Diffusers-Implementierung.
  — <https://github.com/ml-research/ledits_pp>

## Bewährte Vorgehensweisen {#best-practices}

- Verwende einen geseedeten `torch.Generator`, wenn du Parameteränderungen vergleichst, damit die Inversion deterministisch ist.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
- Betrachte `skip` als Regler für die Bearbeitungsstärke: Niedrigere Werte führen zu stärkeren Änderungen am Eingabebild.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
- Setze `edit_threshold` entsprechend dem Bearbeitungsbereich: Verwende einen kleineren Wert für Änderungen am gesamten Bild, etwa Style Transfer, und einen Wert proportional zur betroffenen Region bei lokalen Bearbeitungen.
  — <https://arxiv.org/html/2311.16711v1>
- Behalte standardmäßig die implizite Schnittmengenmaske bei; ergänze `user_mask` nur, wenn die automatische Maske nicht zur gewünschten Region passt.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
- Für Forschungsreproduktion oder eine harte Anforderung an die Rekonstruktionstreue bevorzuge die Implementierung der Autoren, da deren README angibt, dass Diffusers keine perfekte Inversion garantiert.
  — <https://github.com/ml-research/ledits_pp>

## Dadurch abgelöst {#superseded-by-this}

- 2023-07-04 — Den ursprünglichen LEDITS-Gradio-Space als operativen Einstiegspunkt zu nutzen, ist veraltet: Der Space ist pausiert; er sollte als historischer Code erhalten bleiben und nicht als verlässlicher Workflow dienen.
- 2023-12-03 — Ausschließliche Nutzung der gehosteten Demo ist veraltet: Seit 2024-03-15 stellt Diffusers LEDITS++-Pipeline-APIs für Stable Diffusion und SDXL bereit.
- 2023-12-03 — Das perfekte Rekonstruktionsergebnis des Papers als pauschale Bibliotheksgarantie zu behandeln, ist veraltet: Die Autoren geben an, dass die Diffusers-Implementierung keine perfekte Inversion garantiert.

## Weiterhin unbekannt {#still-unknown}

- Die Primärquellen kennzeichnen LEDITS++ nicht explizit als versionierten Nachfolger der LEDITS-Demo von 2023; sie werden hier als eng verwandte Arbeit behandelt, nicht als belegte Produktversionslinie.
- Der LEDITS++-Space wird mit „Running on Zero“ angezeigt, bei dieser Prüfung wurde jedoch keine Bildgenerierung ausgeführt; das ist kein Nachweis für verlässliche gehostete Verfügbarkeit.
- Es wurde kein aktueller modellübergreifender Vergleich mit neueren Allzweck-Bildbearbeitungswerkzeugen gefunden; daher wird nicht behauptet, dass LEDITS++ außerhalb seiner Stable-Diffusion- und SDXL-Integration weiterhin das Beste seiner Klasse ist.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://arxiv.org/html/2307.00522 | LEDITS: Real Image Editing with DDPM Inversion and Semantic Guidance | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/ledits | LEDITS Space | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/ledits/tree/main | Quellcode-Baum des LEDITS Space | 2026-09-04 |
| https://arxiv.org/html/2311.16711v1 | LEDITS++: Limitless Image Editing using Text-to-Image Models, arXiv v1 | 2026-09-04 |
| https://leditsplusplus-project.static.hf.space/index.html | LEDITS++-Projektseite | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/leditsplusplus | LEDITS++ Space | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/leditsplusplus/tree/main | Quellcode-Baum des LEDITS++ Space | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp | Diffusers-API für die LEDITS++-Pipeline | 2026-09-04 |
| https://github.com/ml-research/ledits_pp | ml-research/ledits_pp, offizielle Implementierung | 2026-09-04 |
| https://huggingface.co/papers/2311.16711 | Hugging-Face-Paper-Seite für LEDITS++ | 2026-09-04 |
| https://huggingface.co/posts/sayakpaul/117997091400234 | Ankündigung des Diffusers-0.27.0-Release | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:ledits`, Thread `ledits-development`, 2 datierte Ereignisse vom 2023-07-04 bis 2023-12-03.
- **Praktischer Hinweis:** Stand 2023-12-03 sollten Anwender die ursprünglichen öffentlichen LEDITS-Artefakte von den separat verlinkten LEDITS++-Artefakten unterscheiden und für die gewünschte Variante den entsprechenden Hugging-Face-Space oder das entsprechende Repository konsultieren.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

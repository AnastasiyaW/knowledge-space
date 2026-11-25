---
title: "Stable Diffusion"
category: projects
date: 2022-07-26
tags: [dataset, project, stable-diffusion, stable-diffusion-development, stable_diffusion, stable_diffusion_v2_2_2_xl_beta]
aliases: ["Stable Diffusion", "Stable Diffusion 3"]
level: 3
source_sha256: 7b48d1917ab34df24f8db0096fcde9547314281d2418410f69c90bf42f011089
translation: machine
translated_at: '2026-10-24'
---
# Stable Diffusion {#stable-diffusion}

**Entwicklungslinie:** `project:stable-diffusion` · Thread `stable-diffusion-development`  
**Letztes Ereignis:** 2022-07-26 · 1 datiertes Ereignis seit 2022-07-26 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Stable Diffusion ist eine Familie generativer Bildmodelle für Künstler und Entwickler, die die Wahl zwischen Selbsthosting und einer API benötigen, statt eines geschlossenen Dienstes wie Midjourney.

- Text-zu-Bild und Bild-zu-Bild
- ControlNet zur Steuerung über Canny, Tiefe oder Unschärfe
- Varianten Large, Turbo, Medium und Flash

Die SD-3.5-API liefert Bilder mit 1 MP, Standard 1024×1024; Bild-zu-Bild-Eingaben akzeptieren bis zu 10 MiB.

Für neue Integrationen sollte SD 3.5 statt früherer SD3- oder SDXL-Beta-Bezeichner verwendet werden.

## Entwicklungslinie {#development-line}

- **2022-07-26 — Meilenstein: Anmeldung zum Stable-Diffusion-Beta-Zugang.** Am 2022-07-26 verlinkte der Stable-Diffusion-Eintrag auf das Beta-Anmeldeformular von Stability AI. Das stützt die Beibehaltung eines Beta-Zugangsmeilensteins, belegt aber weder eine veröffentlichte Modellversion noch Berechtigung oder Funktionsumfang.

## Was sich geändert hat {#what-changed}

2022-07-26 — Die Beta-Registrierung bedeutete begrenzte Tests und keine öffentliche Veröffentlichung der Gewichte; der Forschungszugang wurde am 2022-08-10 geöffnet, die öffentliche Veröffentlichung folgte am 2022-08-22.

2023-03-09 — Der NeuralPic-Link nennt keinen Datensatz, kein Modell und kein Stable-Diffusion-Release; die Produktänderung ist nicht bestätigt.

2023-03-25 — Der Eintrag `stable_diffusion_v2_2_2_xl_beta` hat keine URL, daher lassen sich Datum und Änderung nicht überprüfen. Am 2023-04-13 fügte die offizielle API die Engine `stable-diffusion-xl-beta-v2-2-2` für SDXL-Beta und DreamStudio hinzu.

2024-03-07 — Der Link verweist nur auf ein X-Profil; der konkrete Beitrag lässt sich nicht überprüfen. Der offizielle Status von SD3 in diesem Zeitraum war Early Preview und Warteliste, mit Varianten von 800M bis 8B Parametern.

2024-03-13 — Der konkrete X-Beitrag ist zur Prüfung nicht verfügbar; daraus ergibt sich keine bestätigte Modell- oder API-Änderung.

Am 2024-06-12 wurde SD3 Medium für die REST-API und den Gewichtsdownload veröffentlicht; am 2024-10-22 erschienen SD 3.5 Large und Large Turbo, und am 2024-10-29 folgte SD 3.5 Medium.

Ab dem 2025-04-17 werden SD3-API-Bezeichner automatisch auf die entsprechenden SD-3.5-Varianten umgeleitet. In der aktiven Liste der Core Models vom 2026-05-20 bleiben SD 3.5 Medium, Large und Large Turbo erhalten.

## Verwendung {#how-to-use-this}

Für den historischen Eintrag vom 2022-07-26 sollte die Beta-Anmeldung – nicht eine bestätigte öffentliche Veröffentlichung – als operativer Zugangsweg gelten; aktuelle Verfügbarkeit und Bedingungen sind separat zu prüfen.

1. Pfad wählen: API für eine verwaltete Integration oder lokales Hosting für Kontrolle über die Infrastruktur. Für Qualität mit 1 MP Large nehmen, für Geschwindigkeit Large Turbo oder Flash, und für geringeren Ressourcenbedarf Medium.  
  — <https://platform.stability.ai/docs/api-reference>
2. Für die API ein Konto und einen Schlüssel anlegen und den Schlüssel ausschließlich im Authorization-Header übergeben.  
  — <https://platform.stability.ai/docs>
3. Einen Multipart-POST an `/v2beta/stable-image/generate/sd3` senden, mit `prompt`, `model` und `output_format`; für Bild-zu-Bild das Quellbild, `strength` und `mode=image-to-image` übergeben.  
  — <https://platform.stability.ai/docs/api-reference>
4. Für lokale Läufe die Gewichtslizenz akzeptieren, `diffusers`, `transformers` und `accelerate` installieren, `StableDiffusion3Pipeline` laden und die Ausgabebilder speichern.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
5. Um die Komposition an Referenzbilder zu binden, SD3.5 Large ControlNet mit einem Canny-, Tiefen- oder Unschärfe-Konditionsbild verwenden.  
  — <https://github.com/Stability-AI/sd3.5>

## Bewährte Praktiken {#best-practices}

- API-Schlüssel nicht speichern oder committen: den Schlüssel im Authorization-Header übergeben und bei Verdacht auf Leck rotieren.  
  — <https://platform.stability.ai/docs>
- Für wiederholbare Vergleiche einen expliziten Seed setzen: er steuert die Zufälligkeit der Generierung.  
  — <https://platform.stability.ai/docs/api-reference>
- Bei SD 3.5 Medium Prompts auf 256 T5-Tokens begrenzen: längere Anfragen riskieren Randartefakte. Skip Layer Guidance für Struktur und Anatomie verwenden.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- Bei knappem VRAM die offizielle 4-Bit-Quantisierung und CPU-Offloading verwenden, statt beliebiger Gewichtsaustausche.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- Vor kommerziellem Selbsthosting die Lizenz prüfen: die Community License gilt für Unternehmen mit weniger als 1 Mio. USD Jahresumsatz; darüber ist eine Enterprise License erforderlich.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- In der Produktion eigene Inhaltssicherheits-Guardrails hinzufügen: Trainingsfilter verhindern keine schädlichen Ausgaben.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>

## Hierdurch überholt {#superseded-by-this}

- 2022-07-26: die Aufnahme auf die Beta-Warteliste wurde durch die öffentliche Veröffentlichung von Stable Diffusion am 2022-08-22 überholt.
- 2023-04-13: Engine-Grenzen und der Name `stable-diffusion-xl-beta-v2-2-2` gelten für die historische SDXL-Beta, nicht für aktuelle API-Routen.
- 2024-02—03: das Warten auf die SD3 Early Preview wurde durch die Veröffentlichungen von SD3 und SD 3.5 überholt.
- 2025-04-17: API-Anleitungen für `sd3-large`, `sd3-large-turbo` und `sd3-medium` sind veraltet, da Anfragen auf SD 3.5 umgeleitet werden.

## Weiterhin unbekannt {#still-unknown}

- Der Inhalt des Beta-Anmeldeformulars vom 2022-07-26 ist nicht verfügbar; seine Rolle als vorläufiger Zugang beruht auf späteren offiziellen Ankündigungen.
- Der NeuralPic-Link vom 2023-03-09 verbindet das Ereignis nicht mit einem bestimmten Stable-Diffusion-Datensatz, Checkpoint oder Release.
- Der Eintrag vom 2023-03-25 hat keine URL: der Name ähnelt der späteren SDXL-Beta-API-Engine, belegt aber nicht, dass sie an diesem Datum erschien.
- X-Links vom 2024-03-07 und 2024-03-13 lieferten keinen Inhalt; Änderungen an Modell, Lizenz oder Verwaltung bleiben ungeprüft.
- Die Tags `dataset`, `stable_diffusion` und `stable_diffusion_v2_2_2_xl_beta` könnten einen unbestätigten Datensatz-Link, eine inoffizielle Beta-Spur und offizielle Modellveröffentlichungen vermischen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://stability.ai/beta-signup-form | Stability AI Beta-Anmeldeformular — bei der Prüfung nicht abrufbar | 2026-09-04 |
| https://twitter.com/EMostaque | Emad Mostaque auf X — bei der Prüfung nicht abrufbar | 2026-09-04 |
| https://twitter.com/EMostaque/status/1767662732797411433 | Emad Mostaque, Beitrag 1767662732797411433 — bei der Prüfung nicht abrufbar | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-launch-announcement | Stable Diffusion Launch-Ankündigung | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-public-release | Stable Diffusion Public Release | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-xl-beta-available-for-api-customers-and-dreamstudio-users | Stable Diffusion XL Beta verfügbar für API-Kunden und DreamStudio-Nutzer | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-3 | Stable Diffusion 3 | 2026-09-04 |
| https://platform.stability.ai/docs/release-notes | Stability AI Developer Platform Release Notes | 2026-09-04 |
| https://stability.ai/core-models | Stability AI Core Models | 2026-09-04 |
| https://platform.stability.ai/docs | Stability AI API: Getting Started | 2026-09-04 |
| https://platform.stability.ai/docs/api-reference | StabilityAI REST API (v2beta) | 2026-09-04 |
| https://huggingface.co/stabilityai/stable-diffusion-3.5-medium | stabilityai/stable-diffusion-3.5-medium Model Card | 2026-09-04 |
| https://github.com/Stability-AI/sd3.5 | Stability-AI/sd3.5 | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:stable-diffusion`, Thread `stable-diffusion-development`, 1 datiertes Ereignis 2022-07-26 → 2022-07-26.
- **Praktischer Hinweis:** Für den historischen Eintrag vom 2022-07-26 sollte die Beta-Anmeldung – nicht eine bestätigte öffentliche Veröffentlichung – als operativer Zugangsweg gelten; aktuelle Verfügbarkeit und Bedingungen sind separat zu prüfen.
- **Konfidenz:** mittel. Die datierten Überholungsangaben oben sind maßgeblich dafür, was veraltet ist.

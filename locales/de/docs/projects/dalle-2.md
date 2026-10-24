---
title: "DALL-E 2 — Kommerzielle Verbreitung"
category: projects
date: 2022-06-22
tags: [dalle-2, dalle-2-commercial-adoption, dalle_2_commercial_adoption, dalle_2_commercialization, project]
aliases: ["DALL-E 2"]
level: 2
source_sha256: 0c865eba5a16695412424a0a1757f07c7c1d035eda7ae9030186c2f89ba7ce4a
translation: machine
translated_at: '2026-10-24'
---
# DALL-E 2 — Kommerzielle Verbreitung {#dall-e-2-commercial-adoption}

**Development line:** `project:dalle-2` · thread `dalle-2-commercial-adoption`  
**Letztes Ereignis:** 2022-06-22 · 1 datiertes Ereignis seit 2022-06-22 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

DALL-E 2 — OpenAIs Prompt-zu-Bild-Modell von 2022, heute eine veraltete Abhängigkeit und kein nutzbares API-Produkt mehr.

- Bilderzeugung aus Textprompts
- redaktionelle Bildworkflows für frühe kommerzielle Experimente

## Entwicklungslinie {#development-line}

- **2022-06-22 — Cosmopolitan dokumentierte ein Titelbild-Experiment mit DALL-E 2.** Am 2022-06-22 dokumentierte Cosmopolitan ein Titelbild-Experiment mit DALL-E 2. Es zeigte das System in einem kommerziellen redaktionellen Kontext. Die Links belegen keine Kooperationsbedingungen und keinen darüber hinausgehenden kommerziellen Umfang.

## Was sich geändert hat {#what-changed}

Am 2022-06-22 nutzte Cosmopolitan DALL-E 2 in einem redaktionellen Titelbild-Workflow. Menschliche Art Directors platzierten den Zeitschriftenkopf (Masthead) und die Titelzeilen manuell, weil generierter Text unzuverlässig war.
Am 2022-06-30 beschrieb ein datierter Bericht eine Nutzerumfrage zu Preisen im Zusammenhang mit Monetarisierung, nicht einen veröffentlichten Preis oder einen allgemeinen Launch. Den vollständigen Berichtstext konnten wir bei der Prüfung nicht lesen.
Am 2026-09-04 markierte OpenAI DALL-E 2 als veraltet (deprecated) und entfernte es aus der API. Für Bilderzeugung und Bildbearbeitung empfiehlt OpenAI GPT-Image-2.
Das redaktionelle Experiment und die Abkündigung des Modells können wir verifizieren, die Details der Preisumfrage nicht. Die Entwicklungslinie endet mit der Abkündigung, nicht mit einem aktuellen DALL-E-2-Produktpfad.

## Verwendung {#how-to-use-this}

Stand 2022-06-22 sehen wir, dass DALL-E 2 in den kommerziellen redaktionellen Einsatz übergeht. Aus dem nicht verifizierten Nutzerbericht vom 2022-06-30 leiten wir keine offizielle Preis- oder Lizenzpolitik ab.

1. Inventarisieren Sie Altlast-Workflows, die `dall-e-2` nennen. Senden Sie keine neuen Anfragen mehr an dieses Modell, da OpenAI es aus der API entfernt hat.
  — <https://developers.openai.com/api/docs/models/dall-e-2>
2. Für einzelne Prompt-zu-Bild-Erzeugung oder einmalige Bearbeitung stellen Sie den Workflow über die Image API auf `gpt-image-2` um.
  — <https://developers.openai.com/api/docs/guides/image-generation>
3. Für dialogorientierte oder iterative Bildbearbeitung verwenden Sie das Bilderzeugungs-Tool der Responses API, damit Bearbeitungen den Bildkontext behalten.
  — <https://developers.openai.com/api/docs/guides/image-generation>

## Best Practices {#best-practices}

- Behandeln Sie dies als Migration und nicht als Modellwahl, da OpenAI für unterstützte Bilderzeugung und Bildbearbeitung GPT-Image-2 empfiehlt.
  — <https://developers.openai.com/api/docs/models/dall-e-2>
- Verwenden Sie die Image API für einmalige Aufgaben und die Responses API für mehrstufige, bearbeitbare Abläufe.
  — <https://developers.openai.com/api/docs/guides/image-generation>
- Formulieren Sie im Ersatz-Workflow explizite Vorgaben, arbeiten Sie in kleinen Iterationen mit jeweils einer Änderung und nennen Sie unveränderte Details erneut, damit sich Bilder nicht verschieben.
  — <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>
- Legen Sie Ausgabegröße und Qualität bewusst fest: Der Prompting-Leitfaden behandelt Ausgabegrößen über 2560×1440 bei GPT-Image-2 als experimentell.
  — <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>

## Dadurch überholt {#superseded-by-this}

- 2022-06-22: DALL-E 2 als verfügbare Option für neue kommerzielle redaktionelle Workflows zu betrachten, ist veraltet, da OpenAI das API-Modell bis 2026-09-04 entfernt hat.
- 2022-06-30: Preisumfragen oder Warteliste-Recherche als Weg zum DALL-E-2-Zugang zu betrachten, ist veraltet. Unterstützte Integrationen sollten GPT-Image-2 verwenden.

## Weiterhin unbekannt {#still-unknown}

- Wir konnten die Reddit-Preisumfrage vom 2022-06-30 nicht abrufen. Ihr Wortlaut, die Teilnehmenden, Preise und das kommerzielle Ergebnis bleiben daher unverifiziert.
- Die beiden historischen Entwicklungsstränge scheinen dasselbe Produkt zu betreffen: redaktionelle Verbreitung und geplante Monetarisierung.
- Wir haben bestätigt, dass das API-Modell entfernt wurde. Nicht verifiziert haben wir, ob ein archivierter Front-End-Zugang noch existiert. Dieser bietet jedoch keinen unterstützten Integrationspfad.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://developers.openai.com/api/docs/models/dall-e-2 | DALL·E 2 Model | OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/models/gpt-image-2 | GPT-Image-2 Model | OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/image-generation | Bilderzeugung | OpenAI API | 2026-09-04 |
| https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide | Prompting-Leitfaden für GPT-Image-Generierungsmodelle | 2026-09-04 |
| https://www.cosmopolitan.com/lifestyle/a40314356/dall-e-2-artificial-intelligence-cover/ | DALL-E 2 entwirft erstmals ein Magazin-Titelbild für Cosmopolitan | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:dalle-2`, thread `dalle-2-commercial-adoption`, 1 datiertes Ereignis, 2022-06-22 → 2022-06-22.
- **Praxishinweis:** Stand 2022-06-22 konnten Praktiker erkennen, dass DALL-E 2 in sichtbare redaktionelle Nutzung eintrat. Aus dem nicht verifizierten Nutzerbericht vom 2022-06-30 sollten sie jedoch keine offizielle Preis- oder Lizenzpolitik ableiten.
- **Konfidenz:** mittel. Maßgeblich dafür, was veraltet ist, sind die datierten Angaben unter „Dadurch überholt“.

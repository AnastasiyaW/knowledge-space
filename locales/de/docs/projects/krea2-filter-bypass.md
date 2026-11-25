---
title: "Krea2 Filter Bypass"
category: projects
date: 2026-07-02
tags: [krea2-filter-bypass, project]
aliases: ["Krea2 Filter Bypass"]
level: 2
source_sha256: 6e53a5f6d2a1808199f996b7b0a22271076f93bfe760a79614022c98356e06a1
translation: machine
translated_at: '2026-10-24'
---
# Krea2 Filter Bypass {#krea2-filter-bypass}

**Entwicklungslinie:** `project:krea2-filter-bypass` · Thread `krea2-filter-bypass`  
**Letztes Ereignis:** 2026-07-02 · 1 datiertes Ereignis seit 2026-07-02 · **Recherchiert:** 2026-09-05 · Konfidenz: medium

## Was es ist {#what-it-is}

Krea2 Filter Bypass — LoRA `fedor_bypass.safetensors` für Krea 2: Angegeben werden Änderungen an zwei Komponenten von `txtfusion.projector`, das Nullbleiben der übrigen zehn und die Funktion zusammen mit anderen LoRAs; die Grenze liegt bei einer Dateigröße von 1,024 Byte, und die Aussagen über die Aufhebung von Beschränkungen und das Ausbleiben von Stildrift sind durch keinen unabhängigen, reproduzierbaren Test bestätigt. Fazit: Dies ist ein enges Community-Experiment, kein offizieller Modus von Krea und kein Ersatz für die Prüfung der Plattformregeln.

## Entwicklungslinie {#development-line}

- **2026-07-02 — Öffentliche Modell- und Diskussionslinks zu Krea2 Filter Bypass erfasst.** Am 2026-07-02 verknüpfte der datierte Eintrag Krea2 Filter Bypass mit einer Civitai-Modellseite und einer Reddit-Diskussion. Zusammen markieren diese öffentlichen Links einen wesentlichen, nach außen gerichteten Entwicklungspunkt des Projekts, auch wenn die zugrunde liegenden Beiträge nicht unabhängig geprüft wurden.

## Was sich geändert hat {#what-changed}

2026-07-02 — veröffentlicht Krea2 Filter Bypass [Fedor], FP32-Datei `fedor_bypass.safetensors` für Krea 2 mit Deltas nur für die Spalten 9 und 10.

## Wie man es verwendet {#how-to-use-this}

Ab 2026-07-02 sollten Praktiker Krea2 Filter Bypass als ein Projekt mit öffentlichem Modell- und Diskussionsnachweis behandeln und die verlinkten Seiten unabhängig überprüfen, bevor sie sich auf ein behauptetes Verhalten oder eine Kompatibilität verlassen.

1. Prüfen Sie, ob die Verwendung einer solchen Änderung in Ihrer lokalen, lizenzierten Pipeline und nach den Regeln des Modells zulässig ist; übertragen Sie sie nicht in Dienste, in denen sie verpflichtende Beschränkungen umgehen würde.
  — <https://civitai.red/models/2746817/krea2-filter-bypass-fedor?modelVersionId=3089754>
2. Für die Forschungsreproduktion halten Sie Datei, Hash, Basismodell, Seed, Prompt und Generierungsparameter fest; das Quellskript legt den Zielschlüssel `diffusion_model.txtfusion.projector.diff` und die beiden Deltas fest.
  — <https://github.com/CliffNodes/fedor_bypass/blob/main/build_fedor_bypass.py>
3. Vergleichen Sie den Basislauf und den geänderten Lauf mit identischem Seed und vollständigem Satz an Einstellungen; übertragen Sie Qualitätsaussagen nicht von einem einzelnen Bild auf eine Produktionspipeline.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ukh334/i_extracted_the_values_of_krea_2_safery_filters/>

## Best Practices {#best-practices}

- Behandeln Sie die Aussage über das Ausbleiben von Stildrift als Hypothese und führen Sie einen A/B-Test mit identischen Seeds und Einstellungen durch: Die Vergleichsteilnehmer beschreiben die Varianten als ähnlich, aber nicht identisch.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ul38ei/made_yet_another_bypass_filter_for_krea_2_this/>
- Prüfen Sie Inhalt und Herkunft kleiner Gewichtsdateien und nicht nur den Namen: Der veröffentlichte Generator erzeugt einen Tensor `[1,12]` und füllt nur die Positionen 9 und 10.
  — <https://github.com/CliffNodes/fedor_bypass/blob/main/build_fedor_bypass.py>
- Kombinieren Sie unbekannte Bypass-Änderungen nicht mit einem Checkpoint oder einer LoRA, in die eine ähnliche Änderung bereits eingebettet ist: Die Community-Analyse weist darauf hin, dass Stärke und Wirkung vom Prompt und vom Stack abhängen.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ukh334/i_extracted_the_values_of_krea_2_safery_filters/>

## Hierdurch überholt {#superseded-by-this}

- 2026-07-18 — Die Darstellung von Fedor als funktional neuer Bypass gegenüber FilterBypass2 ist überholt: Die spätere Beschreibung reduziert den Unterschied auf die Genauigkeit der Werte und nicht auf einen neuen Mechanismus.
- 2026-07-18 — Die Empfehlung, das Fehlen eines Einflusses auf den Stil als mathematisch garantiert anzusehen, darf ohne unabhängigen A/B-Test nicht als betriebliche Regel verwendet werden.

## Weiterhin unbekannt {#still-unknown}

- Es gibt keine Primärquelle von Krea, die bestätigt, dass die Spalten 9 und 10 tatsächlich den Mechanismus des Safety-Filters darstellen oder dass die Änderung nach Lizenz und Nutzungsbedingungen zulässig ist.
- Es gibt keinen unabhängigen, reproduzierbaren Benchmark, der das behauptete Ausbleiben von Stildrift, eine verbesserte Prompt-Adhärenz oder eine Überlegenheit der FP32-Variante gegenüber FilterBypass2 bestätigt.
- Das Datum 2026-07-18 ist das Aktualisierungsdatum der Civitai-Seite; ein genaues Änderungsprotokoll, getrennt von der aktuellen Beschreibung, ist nicht verfügbar.
- Die Quellen beschreiben dieselbe Zweivektor-Variante und benachbarte Bypass-Dateien, nicht zwei verschiedene gleichnamige Entwicklungen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://civitai.red/models/2746817/krea2-filter-bypass-fedor?modelVersionId=3089754 | Krea2 Filter Bypass [Fedor] - Krea2 Bypass [Fedor] | Krea 2 LoRA | Civitai | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ul38ei/made_yet_another_bypass_filter_for_krea_2_this/ | Ein weiterer Bypass-Filter für Krea 2 gemacht – dieser scheint die Filter gut zu umgehen und jede Art von Verzerrung zu verhindern | 2026-09-05 |
| https://github.com/CliffNodes/fedor_bypass | CliffNodes/fedor_bypass | 2026-09-05 |
| https://github.com/CliffNodes/fedor_bypass/blob/main/build_fedor_bypass.py | fedor_bypass/build_fedor_bypass.py at main | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ukh334/i_extracted_the_values_of_krea_2_safery_filters/ | Ich habe die Werte der Krea 2 Safety-Filter-Bypass-Dateien extrahiert, damit Sie es nicht müssen | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:krea2-filter-bypass`, Thread `krea2-filter-bypass`, 1 datiertes Ereignis 2026-07-02 → 2026-07-02.
- **Praktischer Hinweis:** Ab 2026-07-02 sollten Praktiker Krea2 Filter Bypass als ein Projekt mit öffentlichem Modell- und Diskussionsnachweis behandeln und die verlinkten Seiten unabhängig überprüfen, bevor sie sich auf ein behauptetes Verhalten oder eine Kompatibilität verlassen.
- **Konfidenz:** medium. Die datierten Überholungsvermerke oben sind maßgeblich dafür, was veraltet ist.

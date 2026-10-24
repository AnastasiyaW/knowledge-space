---
title: "Realism Enhancer Krea2"
category: projects
date: 2026-06-29
tags: [project, realism-enhancer-krea2]
aliases: ["Realism Enhancer Krea2"]
level: 2
source_sha256: 813acd0cd1a7d53387720e7711d47056b8cb9313ec6c0a1ccdca8033d7627168
translation: machine
translated_at: '2026-10-24'
---
# Realism Enhancer Krea2 {#realism-enhancer-krea2}

**Entwicklungslinie:** `project:realism-enhancer-krea2` · Thread `realism-enhancer-krea2`  
**Letztes Ereignis:** 2026-06-29 · 1 datiertes Ereignis seit 2026-06-29 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Realism Enhancer Krea2 ist ein LoRA in Version 1.0 und kein Checkpoint. Es richtet sich an Krea-2-Nutzer, die eine alternative visuelle Behandlung testen.

- KREA_2-LoRA: wird direkt als Modell-Adapter angewendet.
- Vergleich eines Drittanbieters: liefert einen dokumentierten Test bei Stärke 0,6.

Die ursprünglichen Listing-Metadaten und die Lizenz waren nicht abrufbar. Wir verwenden das Modell als kontrollierten visuellen Modifikator, nicht als nachgewiesenes Korrekturmodell.

## Entwicklungslinie {#development-line}

- **2026-06-29 — Modellversion von Realism Enhancer Krea2 vermerkt.** Am 2026-06-29 tauchte ein Civitai-Link für Realism Enhancer Krea2 mit der Modellversions-ID 3065628 auf. Damit wird das Projekt an einen bestimmten öffentlichen Modellversions-Verweis zu diesem Datum gebunden. Der verfügbare Link allein belegt weder den Veröffentlichungsstatus, den Inhalt, die Lizenzierung noch die behaupteten Effekte des Modells.

## Was sich geändert hat {#what-changed}

- 2026-06-25 — Ein Spiegel-Hoster datiert v1.0 als erstellt und nennt die safetensors-Datei. Dies sind sekundäre Metadaten und kein unabhängig verifizierter Zeitpunkt der ursprünglichen Veröffentlichung.
- 2026-06-29 — Civitai.red listete den exakten Modellversions-Verweis. Die Domain war bereits eine offizielle Oberfläche des vollständigen Civitai-Katalogs, der Zeitstempel der Ressource war jedoch nicht abrufbar.
- 2026-07-06 — Ein Krea-2-Vergleich eines Drittanbieters testete das Modell bei einer LoRA-Stärke von 0,6. Das Ergebnis veränderte sich sichtbar, allerdings konnte der Tester keine bestimmte Fehlerkategorie benennen, die verbessert wurde.

Eine spätere Version oder ein Nachfolger ist durch die zugänglichen Quellen nicht belegt.

## So verwenden Sie es {#how-to-use-this}

Ab dem 2026-06-29 sollten Vergleiche und Reproduzierbarkeitsnotizen an Civitai-Modellversion 3065628 gebunden werden, nicht nur an den Projektnamen. Prüfen Sie Metadaten und Lizenzierung vor der Verwendung unabhängig.

1. Verwenden Sie einen lokalen Krea-2-Pfad, etwa ComfyUI. Führen Sie Turbo für die Inferenz erst aus, nachdem der LoRA-Loader die Datei akzeptiert hat. Krea dokumentiert ComfyUI-Unterstützung und die Verwendung von RAW-zu-Turbo-LoRAs, nicht jedoch die Kompatibilität mit genau diesem Asset.
  — <https://github.com/krea-ai/krea-2>
2. Ordnen Sie das vorgesehene Asset der Version 1.0 anhand des Dateinamens SummerVibesHM_krea2_epoch8.safetensors zu und prüfen Sie die Herkunft, bevor Sie es laden.
  — <https://prompthero.com/ai-models/realism-enhancer-krea2-2727284-download/realism-enhancer-krea2-v10>
3. Erstellen Sie einen Vergleich mit aus und ein und verwenden Sie 0,6 als anfängliche Teststärke, nicht als verbindliche Einstellung.
  — <https://www.techno-edge.net/article/2026/07/06/5256.html>
4. Gehen Sie nicht davon aus, dass die gehostete Krea-App heruntergeladene safetensors-Dateien importieren kann. Die Dokumentation beschreibt kompatible Stile aus der Krea-Stilbibliothek. Verwenden Sie den lokalen Weg, sofern Ihr Konto eigene Importe ausdrücklich unterstützt.
  — <https://www.krea.ai/docs/user-guide/features/krea-2>

## Best Practices {#best-practices}

- Halten Sie den Prompt fest und ändern Sie jeweils nur einen Einflussfaktor, damit sich die visuelle Veränderung eindeutig zuordnen lässt.
  — <https://www.krea.ai/docs/user-guide/features/krea-2>
- Behandeln Sie das Ergebnis bei 0,6 als Ausgangspunkt und prüfen Sie das Aus-/Ein-Paar selbst. Der verfügbare Vergleich zeigte eine große Veränderung, aber kein belegtes Verbesserungsziel.
  — <https://www.techno-edge.net/article/2026/07/06/5256.html>
- Wenn Sie mit einem Charakter-LoRA kombinieren, prüfen Sie auf veränderte Proportionen, bevor Sie die Stärke erhöhen. Community-Nutzer berichten von später Schedule-Anwendung oder einem reinen Gesichts-Verfeinerungsdurchlauf als Gegenmaßnahmen; für dieses Asset sind das aber keine Garantien.
  — <https://www.reddit.com/r/StableDiffusion/comments/1vcxql0/what_is_your_preferred_realism_lora_stack_for/>
- Übertragen Sie die Rechte eines Reprint-Hosts nicht auf das Originalasset. Holen Sie kommerzielle Nutzungsbedingungen direkt beim ursprünglichen Listing oder beim Ersteller ein.
  — <https://tensor.art/models/1017914439195749656/Realism-Enhancer-Krea2-v1.0>

## Abgelöst durch {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Das ursprüngliche Civitai-Listing und seine API-Antwort konnten hier nicht abgerufen werden. Ursprünglicher Ersteller, Lizenz, Berechtigungen, Trigger-Wort, Rang, Hash, Trainingsdetails sowie Erstellungs- und Veröffentlichungszeitstempel bleiben unverifiziert.
- Der Verweis vom 2026-06-29 belegt für sich allein nicht, dass an diesem Datum eine Veröffentlichung stattfand.
- Krea dokumentiert seine eigene Stilbibliothek, aber nicht den Import dieses beliebigen safetensors-Assets in die gehostete App oder die API.
- Für genau dieses Modell bzw. diese Version wurde keine verlässliche vereinfacht-chinesische Quelle gefunden; ähnlich benannte Krea-2-Realismus-LoRAs sind nicht als Aliase verifiziert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://civitai.red/models/2727284/realism-enhancer-krea2?modelVersionId=3065628 | Realism Enhancer Krea2 — Modell 2727284, Version 3065628 | 2026-09-06 |
| https://civitai.tech/articles/28369/two-front-doors-civitaicom-civitaired-and-whats-next | Zwei Eingänge: Civitai.com, Civitai.red und was als Nächstes kommt | 2026-09-06 |
| https://tensor.art/models/1017914439195749656/Realism-Enhancer-Krea2-v1.0 | Realism Enhancer Krea2 - v1.0 | 2026-09-06 |
| https://prompthero.com/ai-models/realism-enhancer-krea2-2727284-download/realism-enhancer-krea2-v10 | Realism Enhancer Krea2 | v1.0 | PromptHero | 2026-09-06 |
| https://www.techno-edge.net/article/2026/07/06/5256.html | 生成AIグラビアをグラビアカメラマンが作るとどうなる？第70回：Krea 2の勢いがもうどうにも止まらない | 2026-09-06 |
| https://github.com/krea-ai/krea-2 | Krea 2 (K2) — offizieller Inferenzcode | 2026-09-06 |
| https://www.krea.ai/docs/user-guide/features/krea-2 | Krea 2 — Benutzerhandbuch | 2026-09-06 |
| https://www.reddit.com/r/StableDiffusion/comments/1vcxql0/what_is_your_preferred_realism_lora_stack_for/ | What is your preferred Realism LoRA stack for Krea2? | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:realism-enhancer-krea2`, Thread `realism-enhancer-krea2`, 1 datiertes Ereignis 2026-06-29 → 2026-06-29.
- **Praktischer Hinweis:** Ab dem 2026-06-29 Vergleiche und Reproduzierbarkeitsnotizen an Civitai-Modellversion 3065628 binden statt nur auf den Projektnamen zu verweisen; Metadaten und Lizenzierung vor der Verwendung unabhängig prüfen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

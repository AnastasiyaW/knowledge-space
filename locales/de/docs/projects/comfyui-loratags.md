---
title: "ComfyUI-LoraTags"
category: projects

tags: [comfyui-loratags, comfyui_loratags, project]
aliases: ["ComfyUI-LoraTags"]
level: 2
source_sha256: 463da6b1f74db8c8f2424e0f40d8a0aa58ac5f5fac3f926c05f984769e9875d5
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI-LoraTags {#comfyui-loratags}

**Entwicklungslinie:** `project:comfyui-loratags` · Thread `comfyui-loratags`  
**Letztes Ereignis:** - · 0 datierte Einträge seit - · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ComfyUI-LoraTags ist ein Paar aus Knoten für ComfyUI-Nutzer, die mehrere LoRAs kombinieren und deren Trigger-Wörter nicht verlieren wollen. — LoRA Loader (LoraTags): lädt einen LoRA-Stack und gibt MODEL, CLIP und TAGS aus. — CLIP Text Encode (Auto-Tags): fügt dem Text-Prompt vor dem Kodieren eine TAGS-Zeile hinzu. — Tag Manager: fragt bei Civitai anhand des SHA-256-Hashes der Datei den Modellnamen, die ursprünglichen Trigger, bis zu vier Vorschaubilder und einen Link zum Modell ab; benutzerdefinierte Tags werden daneben gespeichert. Befund und Einschränkung: Das Repository zeigt 16 Commits, veröffentlicht keine Releases, und die Installation über ComfyUI Manager ist weiterhin als künftig gekennzeichnet. Fazit: ein früher, für die lokale Installation brauchbarer Knoten, aber kein Ersatz für einen bewährten LoRA-Loader mit langer Kompatibilitätshistorie.

## Entwicklungslinie {#development-line}

- Der datierte Verlauf ist noch nicht aufgearbeitet; das Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

2026-07-15 — Der frühe Zugang zu ComfyUI-LoraTags wurde vom Autor angekündigt; dies ist ein separates, früheres Ereignis. 2026-07-23 — ComfyUI-LoraTags erschien als Paket aus zwei Knoten: Der Loader sammelt die aktiven LoRAs und ihre Tags in TAGS, und Auto-Tags gibt sie in das Conditioning. Das primäre README präzisiert fehlende Details: Die Suche erfolgt über den SHA-256 der `.safetensors`-Datei, liefert bis zu vier Vorschaubilder zurück, und die Datenbank wird in `lora_master_tags.json` gespeichert. Eine spätere datierte Version oder ein Release geht aus den Primärquellen nicht hervor.

## Anwendung {#how-to-use-this}

Stand 2026-07-23 ist das verlinkte GitHub-Repository nur als Ausgangspunkt für weitergehende Recherche zu behandeln; aus diesem Datensatz dürfen keine unterstützte Installation, kein Release und keine Funktionsänderung abgeleitet werden.

1. Klonen Sie das Repository nach `ComfyUI/custom_nodes/`, starten Sie anschließend ComfyUI neu und führen Sie ein hartes Neuladen der Seite durch (`Ctrl+Shift+R`).
  — <https://github.com/iiTzMYUNG/ComfyUI-LoraTags>
2. Fügen Sie `LoRA Loader (LoraTags)` und `CLIP Text Encode (Auto-Tags)` hinzu; verbinden Sie den TAGS-Ausgang des Loaders mit dem Eingang `tags` des Encoders.
  — <https://github.com/iiTzMYUNG/ComfyUI-LoraTags>
3. Fügen Sie LoRA-Zeilen hinzu, wählen Sie `.safetensors`-Dateien aus, legen Sie die Stärke fest und aktivieren Sie die gewünschten Zeilen; im Tag Manager holen Sie die Tags von Civitai oder fügen eigene hinzu.
  — <https://github.com/iiTzMYUNG/ComfyUI-LoraTags>

## Best Practices {#best-practices}

- Bearbeiten Sie `lora_stack_data` nicht manuell: Es wird von der UI des Knotens serialisiert.
  — <https://comfy.icu/node/LoraLoaderMasterDB>
- Führen Sie nach einem Update des Knotens ein hartes Neuladen durch: Seine Oberfläche wird aus JavaScript geladen, und ein veralteter Cache kann die Anzeige beschädigen.
  — <https://comfy.icu/node/LoraLoaderMasterDB>
- Prüfen Sie aktive LoRAs, ihre Stärke (`strength`) und Dateipfade: Eine deaktivierte Zeile, eine Stärke von 0 oder eine verschobene Datei wird nicht angewendet.
  — <https://comfy.icu/node/LoraLoaderMasterDB>
- Achten Sie bei großen Stacks auf die Länge des Prompts: Auto-Tags fügt die Trigger in denselben CLIP-Kontext ein.
  — <https://comfy.icu/node/CLIPTextEncodeWithTags>

## Hiervon abgelöst {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Die GitHub-Historie bestätigt 16 Commits, die zugängliche Primärseite zeigte jedoch weder deren einzelne Daten noch Nachrichten; ein späterer datierter Eintrag wird nicht behauptet.
- Auf der Repository-Seite ist kein GitHub-Release aufgeführt, daher lässt sich kein versionierter Release-Verlauf bestätigen.
- Die Ausgangsanfrage verlangt `event_findings` und `new_events`, das erforderliche Antwortschema enthält jedoch keine Felder dafür; die datierten Befunde sind unter `what_changed` erhalten.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/iiTzMYUNG/ComfyUI-LoraTags | GitHub — iiTzMYUNG/ComfyUI-LoraTags README | 2026-09-05 |
| https://comfy.icu/node/LoraLoaderMasterDB | ComfyUI Cloud — LoRA Loader (LoraTags) | 2026-09-05 |
| https://comfy.icu/node/CLIPTextEncodeWithTags | ComfyUI Cloud — CLIP Text Encode (Auto-Tags) | 2026-09-05 |
| https://www.patreon.com/cw/iiTzMYUNG/sitemap?l=it-IT | iiTzMYUNG Patreon-Sitemap | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:comfyui-loratags`, Thread `comfyui-loratags`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-07-23 ist das verlinkte GitHub-Repository nur als Ausgangspunkt für weitergehende Recherche zu behandeln; aus diesem Datensatz dürfen keine unterstützte Installation, kein Release und keine Funktionsänderung abgeleitet werden.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

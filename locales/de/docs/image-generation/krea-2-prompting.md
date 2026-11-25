---
title: "Prompting für Krea 2"
description: "Referenz zum Prompting für das Open-Weights-Modell Krea 2: ein englischer Absatz mit früh genanntem Medium und beschriebenem Licht, Guidance zwischen den Konventionen umgerechnet, kein Negative Prompt bei Turbo, ein Limit von 507 Tokens außerhalb von ComfyUI sowie adapterspezifische Prompts für Edits und Box-Layouts."
category: techniques
tags: [krea-2, prompting, text-to-image, comfyui, diffusers, cfg, lora, inpainting, bbox]
aliases: ["Krea 2 prompts", "Krea-2-Turbo prompting", "Krea 2 CFG", "Krea 2 negative prompt"]
level: 3
source_sha256: 93b8415b6b3215748626d69407e2286f13e1d46bc55cefdaf02ccc2b18b94371
translation: machine
translated_at: '2026-10-24'
---
# Prompting für Krea 2 {#krea-2-prompting}

Das Open-Weights-Modell Krea 2 gibt es in zwei Varianten: Krea-2-Turbo für Bilder und Krea-2-Raw für LoRA-Training. Krea-2-Turbo ist ein destilliertes 8-Step-Modell. Krea-2-Raw ist die nicht destillierte Basis. Ein 12B-DiT liest Prompts laut Turbo-Model-Card über einen Qwen3-VL-4B-Instruct-Text-Encoder, reagiert also auf schlichtes, beschreibendes Englisch und nicht auf Tag-Salat. Quellen geprüft am 2026-09-30, darunter die Krea2-Pipeline in diffusers und die native Krea-2-Unterstützung in ComfyUI. Das gehostete Krea 2 Medium/Large in der krea.ai-App und API ist eine eigene Oberfläche; die Release-Historie steht unter [[krea-2]].

Fakten aus Code, Cards und Dokumentation verlinken auf ihre Quelle. Unsere eigenen Läufe sind mit *in our tests* markiert; sie nutzen kleine Stichproben, ein bis drei Seeds pro Zelle. Betrachten Sie sie als Richtungsangabe, nicht als Benchmark.

## Einstellungen, bevor der Prompt zählt {#settings-before-any-prompt-matters}

Falsche Guidance zerstört das Bild, bevor die Formulierung eine Rolle spielt. Der Krea-Referenzcode und diffusers verwenden eine eigene Guidance-Konvention. ComfyUI, SGLang und DiffSynth verwenden das Standard-CFG.

| | Turbo (Bilder erzeugen) | Raw (Basis; nicht für finale Bilder) |
|---|---|---|
| Steps | 8 | 52 (README, Card) |
| Guidance, Krea- / diffusers-Konvention | **0.0** | 3.5 |
| Gleich in ComfyUI / SGLang / DiffSynth | **cfg 1.0** | cfg 4.5 |
| ComfyUI-Sampler | `euler`, `simple`, denoise 1 | `euler` |
| Timestep-Shift | mu 1.15, in der Modellkonfiguration von ComfyUI eingebaut | auflösungsabhängig |
| Größe | 1K bis 2K | bis etwa 1K |
| Negative Prompt | wird nie ausgewertet | wird verwendet |

**Umrechnungsregel:** Standard-CFG = 1 + Krea-g. Krea berechnet `cond + g * (cond - uncond)`; ComfyUI berechnet `uncond + cfg * (cond - uncond)`. Der diffusers-Docstring nennt die Äquivalenz direkt („the usual CFG formulation with scale `1 + guidance_scale`“).

- Krea/diffusers `0.0` = ComfyUI `1.0`; Krea `3.5` = ComfyUI `4.5`.
- **ComfyUI cfg 0 = unkonditionales Sampling.** Der Sampler ignoriert den Prompt. Mindestens ein Community-Guide für ComfyUI gibt cfg 0.0 an, indem er Kreas Konvention übernimmt.
- diffusers und die CLI `inference.py` von Krea verwenden standardmäßig 28 Steps / Guidance 4.5 (Krea-Konvention): Standardwerte des Basis-Checkpoints, nicht Turbo-Werte. Übergeben Sie die Turbo-Werte explizit.
- Über 8 Steps und cfg 1.0 bei Turbo hinaus ist das ungetestetes Terrain: Wir haben keinen kontrollierten Vergleich mit mehr Steps oder mit ComfyUI cfg 1.2 bis 1.5 gefunden.

### diffusers (Turbo) {#diffusers-turbo}

```python
import torch
from diffusers import Krea2Pipeline

# Gated repo: accept the Krea 2 Community License on the model page and log in first.
pipe = Krea2Pipeline.from_pretrained("krea/Krea-2-Turbo", torch_dtype=torch.bfloat16).to("cuda")

image = pipe(
    prompt,
    num_inference_steps=8,
    guidance_scale=0.0,      # Krea convention; equals ComfyUI cfg 1.0
    width=1248, height=832,  # multiples of 16
).images[0]
image.save("krea2_turbo.png")
```

### ComfyUI (Turbo) {#comfyui-turbo}

```yaml
# Official template image_krea2_turbo_t2i: files and KSampler values
diffusion_model: krea2_turbo_fp8_scaled.safetensors
text_encoder: qwen3vl_4b_fp8_scaled.safetensors   # CLIP type: krea2
vae: qwen_image_vae.safetensors
KSampler: {steps: 8, cfg: 1.0, sampler_name: euler, scheduler: simple, denoise: 1.0}
negative: ConditioningZeroOut   # never computed at cfg 1.0 anyway
model_sampling_node: none       # shift 1.15 is in the model config
```

## Größe und Seitenverhältnis {#size-and-aspect-ratio}

- **Seitenlängen in Vielfachen von 16.** Kreas `sampling.py` rundet nach oben auf und gibt einen Hinweis aus; diffusers rundet nach oben mit einer Warnung im Log; der AnyPaint-Edit-Adapter verlangt eine Leinwand mit Vielfachen von 16.
- **Turbo 1K bis 2K, Raw bis etwa 1K.** Das Pretraining lief mit 256/512/1024 px in Batches mit gleichem Seitenverhältnis.
- **1K-Stufen** (Kreas gehostete Größenliste, alle Vielfache von 16): 1024x1024, 1184x896, 1248x832, 1376x768, 928x1152, 832x1248, 768x1376.
- Für 2K auf Turbo eine 1K-Größe mit etwa 1.41 multiplizieren und auf 16 runden. Das ist abgeleitet, nicht von Krea veröffentlicht.

```python
def krea_2k(w: int, h: int, scale: float = 2 ** 0.5) -> tuple[int, int]:
    """Scale a 1K ladder size to ~2 MP and snap both sides to multiples of 16."""
    return (int(round(w * scale / 16)) * 16, int(round(h * scale / 16)) * 16)

krea_2k(1248, 832)  # (1760, 1184)
```

## Form des Text-zu-Bild-Prompts {#text-to-image-prompt-form}

Krea legt die Regel in `docs/prompting.md` und im Prompt für die LLM-Erweiterung `docs/expansion.txt` fest: natürliche Sprache in einem zusammenhängenden Absatz. Längere, spezifische Beschreibungen funktionieren besser, kurze laufen aber ebenfalls.

- **Ein Absatz, keine Aufzählungen, Überschriften, JSON oder Markdown.** Der unten stehende bbox-LoRA-Block ist die einzige Ausnahme.
- **Das Medium früh nennen.** Schreiben Sie „An editorial portrait photograph of...“ oder „A macro photograph of...“. Der Erweiterungs-Prompt behandelt „photo of“ als Medium, das erhalten bleiben soll.
- **Jedes Subjekt mit seinen eigenen Attributen und Handlungen zusammenhalten.** Verwenden Sie konkrete räumliche Wörter: left, right, foreground, behind, holding.
- **Das Licht immer beschreiben.** Qualität und Richtung angeben („soft window light from the left“, „harsh noon sun“, „warm low sunlight from the right“). Jedes offizielle Fotobeispiel tut das.
- **Fotorealismus.** Konkrete Oberflächendetails und kleine Unvollkommenheiten angeben (Hautporen, zarte Sommersprossen, abstehende Haare, abgewetzte Schuhe, verschlissene Vinylsitze), Einstellungsgröße und Tiefenschärfe (medium close-up, shallow depth of field), Filmkorn oder Bewegungsunschärfe, wo gewünscht. Der technische Report sagt, Bewegungsunschärfe und Weichzeichnung seien bewusst in den Daten belassen worden. Objektivangaben („85mm at f/2“) stehen in einem Provider-Guide und sind in beide Richtungen unbelegt.
- **Text im Bild.** Exakte Wörter in doppelte Anführungszeichen setzen und kurz halten. Nebensächlicher Hintergrundtext ist unzuverlässig; verzerrter Text ist ein benannter Fehlermodus.
- **Beschreibende Komma-Listen liegen im Verteilungsbereich des Modells.** 8 von 20 offiziellen Turbo-Beispielen sind kommaseparierte Deskriptorlisten, und mehrere Widget-Prompts auf den Cards enden mit einem `, <style tag>`.
- **Keine Qualitäts-Floskeln, keine Gewichtungen.** „masterpiece, best quality, 8k“ taucht in keinem offiziellen Beispiel auf; die `(word:1.2)`-Gewichtung soll laut einer Community-Quelle nicht zuverlässig funktionieren.
- **Sagen, was da ist, statt „kein X“.** „an unlit torch“ schreiben, nicht „a torch without flame“; „an empty courtyard at dawn“, nicht „a courtyard, no people“.
- **Dokumentiert ist nur Englisch.** Die Card deklariert `language: en`. Nicht-englische Wörter nur als zu rendernden Text in Anführungszeichen verwenden und selbst das als ungetestet behandeln.

### Beispiel-Prompts {#example-prompts}

```text
A candid street photograph of a young woman standing on a cracked asphalt sidewalk in a courtyard
of five-storey panel apartment blocks, gray facades with uneven glazed balconies, laundry drying on
a line, old poplar trees behind her. She wears a white t-shirt and a denim jacket and squints
slightly in the late afternoon sun, a few flyaway hairs catching the light. Warm low sunlight from
the right, soft shadows, slightly faded colors, eye-level medium shot, everyday documentary feel,
realistic film photograph.
```

```text
A close-up photograph of a hand-painted wooden shop sign reading "OPEN" hanging on a brass hook
beside a green door with chipped paint, morning sun raking from the left across the wood grain,
shallow depth of field, the street behind softly out of focus.
```

### Umformulierungen {#rewrites}

| Statt | Schreiben Sie |
|---|---|
| `masterpiece, best quality, 8k, (sharp:1.3)` | konkretes Detail: „fine skin pores, crisp fabric weave, sharp focus on the eyes“ |
| „a Paris street, no people“ | eine Szene ohne Menschenmenge: „a quiet cobbled side street at dawn, shutters closed“ |
| „torch without flame“ | „an unlit torch“ |
| Negative Prompt „blurry, deformed“ auf Turbo | nichts: er wird nicht ausgewertet; den gewünschten Fokus positiv beschreiben |
| Russische oder gemischtsprachige Beschreibung | englische Beschreibung; zitierte Wörter nur für zu rendernden Text |

### Verworfener Folklore {#rejected-folklore}

- **„Die offizielle Caption-Reihenfolge von Krea“** (Subject -> Appearance -> Props -> Composition -> Environment -> Lighting -> Aesthetic, oft „in two paragraphs“). Sie stammt aus einem Community-Beitrag im Diskussions-Tab des Modells und wurde von einem ComfyUI-Node als „the official system prompt“ neu verpackt. Kreas tatsächlicher System-Prompt verlangt einen Absatz ohne feste Abschnittsreihenfolge. Die Reihenfolge ist eine harmlose Gewohnheit, kein trainiertes Format.
- **„CFG 0.0 in ComfyUI“** für Turbo: siehe die Umrechnungsregel oben.
- **Negative Prompts auf Turbo:** siehe den nächsten Abschnitt.
- **Gehostete Regler auf Open Weights:** Kreativitätsstufen, Schieberegler, Moodboards und Stilreferenzen gibt es nur im gehosteten Medium/Large. fals „Krea 2 Prompting Guide“ stammt vor der offenen Veröffentlichung und zielt auf gehostete Modelle.
- **„Beide Varianten wurden auf 2048 trainiert“:** Raw ist bis 1K dokumentiert; die Pretraining-Stufen endeten bei 1024.

## Token-Budget und Sprache {#token-budget-and-language}

Der Encoder umhüllt den Prompt mit einer festen System-Vorlage („Describe the image by detailing the color, shape, size, texture, quantity, text, spatial relationships of the objects and background“). Krea-Referenzcode, diffusers und DiffSynth füllen auf oder kürzen auf 512 Positionen, nachdem das 34-Token-Systempräfix entfernt wurde; ein 5-Token-Assistenten-Suffix folgt dem Prompt.

- **Obergrenze für den Nutzer-Prompt: etwa 507 Tokens** im Krea-Referenzcode, in diffusers und in DiffSynth. Der Teil darüber wird stillschweigend abgeschnitten.
- **ComfyUI kürzt nicht** (sein Qwen3-VL-Tokenizer hat keine 512-Grenze). Derselbe lange Prompt verhält sich in den Laufzeitumgebungen unterschiedlich.
- Prompts unter etwa 500 Tokens halten und das Wesentliche an den Anfang stellen.
- Gemessene Raten mit dem Qwen-Tokenizer: Englisch etwa 1.3 bis 1.4 Tokens pro Wort (etwa 360 bis 390 Wörter passen in das Limit); das längste offizielle Beispiel hat 252 Tokens. Das offizielle „mouse“-Beispiel mit 84 Wörtern hat auf Englisch 108 Tokens; eine russische Übersetzung brauchte 215 Tokens, 2.0x.

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-VL-4B-Instruct")  # the encoder Krea 2 uses
n = len(tok(prompt)["input_ids"])
print(n, "tokens;", "over the 507 cap" if n > 507 else "fits")
```

## Negative Prompts und Unterdrückung {#negative-prompts-and-suppression}

- **Turbo wertet bei seinen Einstellungen den Negative Prompt nie aus.** Kreas Sampler überspringt den unkonditionalen Zweig bei Guidance 0; ComfyUI überspringt ihn bei cfg 1.0 (`uncond + 1 * (cond - uncond) = cond`); diffusers ignoriert `negative_prompt`, wenn `guidance_scale <= 0` ist; fals Turbo-API hat kein Negative-Feld. Negativlisten, die aus LoRA-Cards der Raw-Ära kopiert wurden („airbrushed, plastic skin, waxy“), bewirken auf Turbo nichts.
- **Raw mit echtem CFG (ComfyUI cfg > 1) verwendet den Negative Prompt.** Der Standard ist der leere String.
- **Verneinung im positiven Prompt ist unzuverlässig.** In unseren Tests ergab ein Straßenhintergrund mit „an empty ... street, no people, no passers-by“ 16 zusätzliche Gesichter gegenüber 13 ohne die Formulierung (ein Vergleich, ein Seed pro Zelle): Die Phrase entfernte keine Menschen, und ein einzelner Vergleich kann nicht zeigen, dass sie welche hinzufügt.

Um etwas auf Turbo zu unterdrücken:

1. Positiv umformulieren („unlit torch“, „empty courtyard at dawn“).
2. Eine Szene wählen, die das Unerwünschte nicht nahelegt: Eine sonnige Stadtstraße bringt Passanten (Abhilfe nicht per A/B-Test geprüft).
3. Den Community-Node NAG (Normalized Attention Guidance) verwenden, der negative Steuerung bei cfg 1.0 über Attention ermöglicht; Standardwerte phi 4.0, tau 2.5, alpha 0.25.
4. Raw mit echtem CFG verwenden und in Kauf nehmen, dass Raw langsamer ist und nicht auf finale Bilder abgestimmt ist.

## LoRA-Trigger {#lora-triggers}

**Den Trigger dort platzieren, wo ihn die Captions des LoRA-Trainings hatten.** LoRAs auf Raw trainieren, auf Turbo einsetzen.

- **Offizielle Krea-Stil-LoRAs:** eine beschreibende Phrase am **Ende** des Prompts, Stärke 1.0 laut Cards (das ComfyUI-Template liefert 0.8 und hängt den Trigger mit `", "` an).

| Repo | Trigger (am Ende anhängen) |
|---|---|
| `krea/Krea-2-LoRA-darkbrush` | `monochrome ink wash style` |
| `krea/Krea-2-LoRA-dotmatrix` | `monochrome stippling style` |
| `krea/Krea-2-LoRA-kidsdrawing` | `naive expressive sketch style` |
| `krea/Krea-2-LoRA-neondrip` | `textured abstract style` |
| `krea/Krea-2-LoRA-rainywindow` | `rainy window style` |
| `krea/Krea-2-LoRA-retroanime` | `purple retro anime style` |
| `krea/Krea-2-LoRA-softwatercolor` | `Art Deco watercolor style` |
| `krea/Krea-2-LoRA-sunsetblur` | `ethereal motion blur style` |
| `krea/Krea-2-LoRA-vintagetarot` | `vintage tarot style` |

- **Charakter-LoRAs**, trainiert mit einem namensähnlichen Token: Token zuerst, als Subjekt verwendet, dann stabile Merkmale, dann die Szene. Unsere Präfixform: `character_<id>_person, woman, in her twenties, dark hair, long hair, <scene prose>`.
- **Community-Realismus-LoRAs** unterscheiden sich: Manche nehmen keinen Trigger, manche ein Präfix, manche ein Suffix. Die Position der jeweiligen Card des LoRA entnehmen, nicht Blog-Tabellen.
- Keine Stilwörter stapeln, die gegen eine Stil-LoRA arbeiten. fal erlaubt höchstens 3 LoRAs pro Aufruf, Skalierung 0 bis 4.
- **Captions für eigene LoRAs** (diffusers-Krea-2-DreamBooth-Guide): Bei einem Stil den Inhalt beschreiben, der nicht eingebrannt werden soll, und eine beschreibende Trigger-Phrase ergänzen; bei einem Charakter ist ein Trigger-Wort in Ordnung, wenn die Captions Klasse, Kleidung, Pose, Umgebung und Licht nennen, aber nicht das Gesicht.

## Edits brauchen einen Adapter {#edits-need-an-adapter}

Das reine Krea 2 hat **keinen referenzkonditionierten Edit-Pfad**. Der DiT hat keinen Eingang für Referenz-Latents oder Inpainting, daher wird eine VAE-Referenz, die über das einfache `CLIPTextEncode` oder den Qwen-Image-Edit-Encode-Node eingespeist wird, stillschweigend verworfen. Die uns bekannten Edit-Wege sind eine Adapter-LoRA samt ihrem Patch-Node.

| Aufgabe | Adapter | Prompt |
|---|---|---|
| Hintergrund ersetzen, Person behalten | AnyPaint (K/V-Cache an) | Nur der neue Hintergrund plus „matching the existing light“. Niemals die behaltene Person |
| Ein Objekt in eine Region malen | AnyPaint, Region = weiße Maske | Das Objekt in schlichter Prosa plus passendes Licht |
| Instruktions-Edit (umfärben, Stil ändern) | `ComfyUI-Krea2-Ostris-Edit`-Edit-LoRAs, `comfyui-krea2edit` | Imperative Anweisung: „recolor the car to matte black“ |
| Geschwärzten Bereich füllen | `krea2-inpaint-edit`-LoRA auf den Ostris-Edit-Nodes | Was die Region füllt; bei Referenzgröße samplen (siehe unten) |
| Neues Bild per Boxen anlegen | Koordinaten im Prompt; bbox-LoRA optional | JSON-Boxen, siehe nächsten Abschnitt |

- **Maskenkonvention:** weiß = neu erzeugen, schwarz = behalten. Leinwand in Vielfachen von 16.
- **Mit dem Krea2Edit-Adapter die Ausgabe bei höchstens etwa 2 MP halten** (laut seiner README, einzelne Quelle): Oberhalb seines Trainingsbereichs kann Inhalt der Quelle durchbluten. AnyPaint nennt keine solche Grenze.
- **Entfernungen:** Dieselben Hinweise sagen, dass das destillierte Turbo bei cfg 1 das Motiv tendenziell neu zeichnet, und empfehlen Raw, cfg 3 (Standardkonvention), etwa 20 Steps (einzelne Quelle).

### Hintergrundersetzung: nur den neuen Hintergrund beschreiben {#background-replacement-describe-only-the-new-background}

```text
A rain-washed evening street in an old European city, warm shop windows and wet cobblestones
reflecting orange light, soft haze in the distance, matching the existing light.
```

- Schreiben Sie den neuen Hintergrund und bitten Sie darum, dass sich das Licht anpasst. Erwähnen Sie die behaltene Person überhaupt nicht: weder das Charakter-Token noch „the woman in front“ oder „behind her“. Menschen im Hintergrund sind in Ordnung, wenn Sie sie wollen.
- Die AnyPaint-Card selbst verlangt „a prompt describing the complete desired output image“. Nur der Hintergrund ist unsere Praxis; einen kontrollierten A/B-Vergleich der beiden Varianten haben wir nicht durchgeführt.
- *In our tests* (3 Renderings x 2 Hintergründe x 5 Edit-Adapter, Gesichtszahl außerhalb der Maske der behaltenen Person; Originale mit denselben Masken: 0): Eine zweite, kleinere Kopie der Person entstand vor allem durch die Sampling-Skalierung, nicht durch den Prompt. Das Entfernen der Person aus dem Prompt und das Weglassen der Charakter-LoRA verschob die zusätzlichen Gesichter nur von 30 auf 24/25.
- *In our tests* sah die Hauptursache nach Skalierung aus: Der Ostris-Edit-Encoder verkleinert die Referenz auf etwa 1 MP (`REF_LATENT_MAX_PIXELS = 1024*1024`), und das Sampling einer 2048er-Leinwand zeichnete die Person in Referenzgröße neu: Das Gesicht bei (1092, 726), 940 px breit, tauchte bei (546, 366) mit etwa 460 px Breite wieder auf. Sampling bei Referenzgröße und Hochskalieren des neuen Hintergrunds entfernte die Kopie; die zusätzlichen Gesichter sanken von 28 auf 12, fast alle davon Passanten, die der Straßen-Prompt verlangte.
- In denselben Läufen behielt AnyPaint die Person jedes Mal an ihrem Platz, daher ist es der Adapter, den wir für die Hintergrundersetzung verwenden.

### Regionales Inpainting {#region-inpaint}

- Die Region mit der Maske markieren und das Objekt in schlichter Prosa plus Licht benennen. Die Maske ist der Ort; der Prompt braucht keine Koordinaten.
- *In our tests* (AnyPaint, 2 Bilder x 3 Objekte x 2 Boxformen x 3 Seeds = 72): Die mittlere absolute Änderung außerhalb der Box blieb bei höchstens 1.06, innerhalb bei 15 bis 49. Das Hinzufügen der bbox-LoRA änderte nichts Messbares (Fahrrad 33.6 gegenüber 33.8, Hund 40.5 gegenüber 40.9, Pflanze 35.5 gegenüber 34.5).
- In denselben Tests erzeugte ein breiter, niedriger Streifen entlang des unteren Rands eines 9:16-Bildes die geringste Änderung (15 bis 26) bei zwei von drei Objekten; solche Boxen als verdächtig behandeln, bis sie per Augenschein oder Detektor geprüft sind.

## Box-Layout (bbox-LoRA) {#box-layout-bbox-lora}

Die krea2-bbox-LoRA (Civitai-Modell 2897864) nimmt Objektboxen als JSON in normierten Koordinaten von 0..1000, `[x1, y1, x2, y2]`, ohne Trigger-Wort. Der Format-Block der Card setzt einen Satz vor das JSON:

```text
The all objects uses the following bbox.
{"objects": {"a golden retriever sitting": [40, 500, 420, 1000], "a red bicycle": [560, 450, 980, 1000]}}
A sunny city park with a gravel path and tall linden trees, soft afternoon light, photograph.
```

- Der Autor der Card nennt das Format locker („can just write the coordinates“); die eingebetteten Beispiel-Prompts variieren die Reihenfolge, stellen das JSON manchmal ans Ende und lassen den Satz manchmal weg. Wichtig ist ein gültiger JSON-Block mit vernünftigen Boxen (x1 < x2, y1 < y2).
- Beispielstärke des Autors 0.75. Die Card merkt an, dass Motive tendenziell groß und zentriert erscheinen und dass das Basismodell Krea 2 Koordinaten nur manchmal befolgt und sie gelegentlich als Text ausgibt.
- Die offiziellen Erweiterungsregeln verbieten JSON in Prompts; dieser Block ist adapterspezifisch. Nicht zu gewöhnlichen Prompts hinzufügen.
- *In our tests* (6 gespiegelte Layouts x 4 Varianten x 2 Seeds; Treffer = Gesichtsmitte der Figur liegt innerhalb ihrer Box): einfache Worte 0/12, JSON-Koordinaten ohne LoRA 5/12, LoRA 0.75 3/12, LoRA 1.0 5/12. Kleine Figuren scheiterten in jeder Variante. Koordinaten allein im Text verschieben das Motiv bereits in Richtung seiner Box; die LoRA brachte bei dieser Stichprobengröße nichts Messbares. Die Platzierung ist ungefähr.

## Kamerawinkel-Adapter (krea2-anygles) {#camera-angle-adapter-krea2-anygles}

Eine Control-LoRA plus 4 ComfyUI-Nodes, die eine Person aus neuem Gierwinkel, neuer Höhe oder Distanz neu rendern, gesteuert durch eine Normal-Map von SAM 3D Body und einen festen Kamera-Satz („Same figure. Move the camera 310 degrees to the left relative to the input view.“). Einstellungen des Autors: 8 Steps, cfg 1, Stärke 1.0, 384 px Referenz, höchstens etwa 2 MP. Ein einfacher LoRA-Loader verwirft ihre Control-Projektion. Details, Lauf-Schritte und unser Orbit-Test: [[krea-2-anygles]].

## Stolperfallen {#gotchas}

- **Problem:** Ein Turbo-Bild ignoriert in ComfyUI den Prompt vollständig. -> **Lösung:** cfg ist 0 (Kreas „0.0“ übernommen). Auf cfg 1.0 setzen.
- **Problem:** Der Negative Prompt hat keine Wirkung. -> **Lösung:** Turbo bei cfg 1 berechnet ihn nie. Positiv umformulieren, den NAG-Node verwenden oder auf Raw mit echtem CFG wechseln.
- **Problem:** Das Ende eines langen Prompts wird in diffusers ignoriert, in ComfyUI aber nicht. -> **Lösung:** Der Referenz-Encoder kürzt bei etwa 507 Tokens, ComfyUI kürzt nicht. Auf unter etwa 500 kürzen und das Wesentliche an den Anfang stellen.
- **Problem:** Nach einer Hintergrundersetzung mit einem Inpaint-Edit-Adapter erscheint eine zweite, kleinere Kopie der Person. -> **Lösung:** Der Ostris-Edit-Encoder begrenzt die Referenz auf etwa 1 MP; in unseren Tests entfernte das Sampling bei dieser Größe und anschließendes Hochskalieren die Kopie. Alternativ AnyPaint verwenden.
- **Problem:** „no people“ liefert trotzdem Passanten. -> **Lösung:** In unserem einen Vergleich entfernte die Verneinung sie nicht. Einen Ort oder eine Tageszeit ohne Menschenmenge wählen (Abhilfe nicht per A/B-Test geprüft).
- **Problem:** Eine Stil-LoRA wirkt schwach. -> **Lösung:** Offizielle Stil-Trigger gehören ans Ende des Prompts; bei Community-LoRAs die Card prüfen.
- **Problem:** Die Krea-Dokumentation für gehostete Modelle rät davon ab, für finale fotorealistische Arbeiten „Turbo“ zu verwenden. -> **Lösung:** Diese Seite beschreibt das gehostete Medium Turbo; die Card des offenen Turbo zeigt fotorealistische Ergebnisse. Gehostete und offene Checkpoints sind öffentlich nicht eins zu eins zugeordnet.
- **Problem:** Eine Größe wie 1250x830 läuft in einem Tool und scheitert am Edit-Adapter. -> **Lösung:** Die Seitenlängen selbst vor jedem Lauf auf Vielfache von 16 einrasten.

## Siehe auch {#see-also}

- [[krea-2]] - Release-Historie, gehostete vs. offene Oberflächen
- [[krea2-realism]] - Linie der Community-Realismus-LoRAs für Krea 2
- [[krea-2-outpaint]] - Outpaint-Adapter für Krea 2
- [[krea-2-anygles]] - Kamerablick-Adapter für eine Person
- [[flux-klein-9b-inference]] - dieselbe Disziplin „Checkpoint und Laufzeit festpinnen“ für FLUX.2 [klein]
- [[diffusion-lora-training]] - LoRA-Training als versionsgebundenes Experiment
- [[object-removal-inpainting]] - Entfernen und Inpainting außerhalb von Krea
- [[flow-matching]] - die Sampler-Familie hinter Krea 2

## Quellen {#sources}

Offiziell:

- Krea-2-Repository, README (Turbo/Raw-Einstellungen, Vielfache von 16): https://github.com/krea-ai/krea-2
- Prompting-Guide: https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md
- System-Prompt der LLM-Erweiterung: https://github.com/krea-ai/krea-2/blob/main/docs/expansion.txt
- Encoder (Vorlage, 512 Positionen, Kürzung): https://github.com/krea-ai/krea-2/blob/main/encoder.py
- Sampler (Guidance-Formel, Auffüllen auf 16): https://github.com/krea-ai/krea-2/blob/main/sampling.py
- Model Card Turbo: https://huggingface.co/krea/Krea-2-Turbo
- Model Card Raw: https://huggingface.co/krea/Krea-2-Raw
- Technischer Report: https://www.krea.ai/blog/krea-2-technical-report
- Offizielle Stil-LoRA-Card (gleiches Muster für alle neun): https://huggingface.co/krea/Krea-2-LoRA-softwatercolor
- Gehostete Krea-2-Doku (nur gehostete Regler, Größenliste): https://www.krea.ai/docs/user-guide/features/krea-2

Serving-Code und Dokumentation:

- diffusers-Krea-2-Pipeline-Doku: https://huggingface.co/docs/diffusers/en/api/pipelines/krea2
- diffusers-Pipeline-Quelle (Guidance-Konvention, Rundung auf 16, Länge 512): https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/krea2/pipeline_krea2.py
- diffusers-Krea-2-LoRA-Trainingsguide: https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/README_krea2.md
- ComfyUI-Krea-2-Tutorial (Dateien, offizielle LoRA-Trigger): https://docs.comfy.org/tutorials/image/krea/krea-2
- Offizielles ComfyUI-Turbo-Template: https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_krea2_turbo_t2i.json
- ComfyUI-Krea-2-Text-Encoder (Template, Entfernen des Präfixes): https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/text_encoders/krea2.py
- ComfyUI-Qwen3-VL-Tokenizer (keine 512-Grenze): https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/text_encoders/qwen3vl.py
- ComfyUI-Sampler (cfg 1.0 überspringt uncond): https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/samplers.py
- SGLang-Krea-2-Cookbook: https://docs.sglang.io/cookbook/diffusion/Krea/Krea-2
- DiffSynth-Studio Krea 2: https://diffsynth-studio-doc.readthedocs.io/en/latest/Model_Details/Krea-2.html
- Qwen3-VL-4B-Instruct (Tokenizer zum Zählen): https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct

Anbieter:

- fal, Guide zu Open Weights: https://fal.ai/learn/tools/how-to-use-krea-2-open-source
- fal, Prompting-Guide für gehostete Modelle (vor der offenen Veröffentlichung): https://fal.ai/learn/tools/krea-2-prompting-guide
- fal-Turbo-Endpunkt (keine Felder für Steps, Guidance oder Negative; die LoRA-Variante nimmt bis zu 3 LoRAs): https://fal.ai/models/fal-ai/krea-2/turbo
- Scenario, Krea 2 essentials: https://help.scenario.com/articles/1463593157-krea-2-the-essentials

Adapter und Community:

- AnyPaint-Card: https://huggingface.co/yijunwang2/krea2-anypaint
- AnyPaint-ComfyUI-Nodes: https://github.com/alexw5702-afk/krea2-anypaint
- krea2-inpaint-edit-LoRA: https://huggingface.co/Cierpliwy/krea2-inpaint-edit
- Ostris-Edit-Nodes (Referenz bei etwa 1 MP): https://github.com/ostris/ComfyUI-Krea2-Ostris-Edit
- Krea2Edit-Nodes (Anweisungen, 2 MP, Entfernungen auf Raw): https://github.com/lbouaraba/comfyui-krea2edit
- bbox-LoRA-Card: https://civitai.com/models/2897864
- Code-Analyse des fehlenden Referenzpfads: https://github.com/ethanfel/ComfyUI-Krea2TextEncoder
- NAG-Node für Krea 2: https://github.com/iljung1106/ComfyUI-Krea2-NAG
- Herkunft der „offiziellen Caption-Reihenfolge“: https://huggingface.co/krea/Krea-2-Turbo/discussions/4
- Der Node, der sie neu verpackt: https://github.com/WaitWut/krea2-structured-prompt
- Verneinungsfehler („torch without flame“): https://huggingface.co/krea/Krea-2-Turbo/discussions/13
- Community-ComfyUI-Guide (nützlich, nennt aber cfg 0.0 für ComfyUI): https://www.instasd.com/post/krea-2-prompt-and-style-guide-comfyui
- Realismus-LoRA der Raw-Ära mit Negativliste: https://huggingface.co/inlineresearch/skin-lora-krea-2-raw
- krea2-anygles-Nodes: https://github.com/alexw5702-afk/krea2-anygles
- krea2-anygles-Card: https://huggingface.co/yijunwang2/krea2-anygles

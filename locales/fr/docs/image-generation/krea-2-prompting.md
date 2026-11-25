---
title: "Prompting avec Krea 2"
description: "Référence sur le prompting de Krea 2 en poids ouverts : un paragraphe unique en anglais, le médium mentionné en début de phrase et la lumière décrite, guidance convertie entre conventions, pas de prompt négatif sur Turbo, une limite de 507 tokens hors ComfyUI, et prompts spécifiques aux adaptateurs pour les éditions et les mises en page par boîtes."
category: techniques
tags: [krea-2, prompting, text-to-image, comfyui, diffusers, cfg, lora, inpainting, bbox]
aliases: ["Krea 2 prompts", "Krea-2-Turbo prompting", "Krea 2 CFG", "Krea 2 negative prompt"]
level: 3
source_sha256: 93b8415b6b3215748626d69407e2286f13e1d46bc55cefdaf02ccc2b18b94371
translation: machine
translated_at: '2026-10-24'
---
# Prompting avec Krea 2 {#krea-2-prompting}

Krea 2 en poids ouverts existe en deux variantes : Krea-2-Turbo pour la génération d'images et Krea-2-Raw pour l'entraînement de LoRA. Krea-2-Turbo est un modèle distillé en 8 étapes. Krea-2-Raw est la base non distillée. Un DiT de 12B lit les prompts via un encodeur de texte Qwen3-VL-4B-Instruct, d'après la fiche de Turbo ; il répond donc à une description simple et naturelle en anglais, et non à une liste de tags. Sources consultées le 2026-09-30, dont le pipeline Krea2 de diffusers et la prise en charge native de Krea 2 dans ComfyUI. Les modèles hébergés Krea 2 Medium/Large sur l'application et l'API krea.ai constituent une surface distincte ; voir [[krea-2]] pour l'historique des versions.

Les faits issus du code, des fiches et de la documentation renvoient à leur source. Nos propres essais sont signalés par *in our tests* ; ils portent sur de petits échantillons, un à trois seeds par cellule. Considérez-les comme une indication de tendance, et non comme des benchmarks.

## Réglages avant tout travail sur le prompt {#settings-before-any-prompt-matters}

Une mauvaise guidance casse l'image avant même que la formulation n'entre en jeu. Le code de référence de Krea et diffusers utilisent leur propre convention de guidance. ComfyUI, SGLang et DiffSynth utilisent le CFG standard.

| | Turbo (génération d'images) | Raw (base ; pas pour les images finales) |
|---|---|---|
| Étapes | 8 | 52 (README, fiche) |
| Guidance, convention Krea / diffusers | **0.0** | 3.5 |
| Équivalent dans ComfyUI / SGLang / DiffSynth | **cfg 1.0** | cfg 4.5 |
| Échantillonneur ComfyUI | `euler`, `simple`, denoise 1 | `euler` |
| Décalage de timestep | mu 1.15, intégré à la configuration du modèle de ComfyUI | dépendant de la résolution |
| Taille | 1K à 2K | jusqu'à environ 1K |
| Prompt négatif | jamais évalué | utilisé |

**Règle de conversion :** CFG standard = 1 + g de Krea. Krea calcule `cond + g * (cond - uncond)` ; ComfyUI calcule `uncond + cfg * (cond - uncond)`. La docstring de diffusers énonce directement l'équivalence (« la formulation CFG habituelle avec l'échelle `1 + guidance_scale` »).

- Krea/diffusers `0.0` = ComfyUI `1.0` ; Krea `3.5` = ComfyUI `4.5`.
- **ComfyUI cfg 0 = échantillonnage inconditionnel.** L'échantillonneur ignore le prompt. Au moins un guide communautaire pour ComfyUI indique cfg 0.0 en reprenant la convention de Krea.
- La CLI `inference.py` de diffusers et celle de Krea utilisent par défaut 28 étapes et une guidance de 4.5 (convention Krea) : ce sont les valeurs par défaut du checkpoint de base, et non celles de Turbo. Passez explicitement les valeurs de Turbo.
- Au-delà de 8 étapes et de cfg 1.0 sur Turbo, on sort des cas testés : nous n'avons trouvé aucune comparaison contrôlée portant sur davantage d'étapes ou sur ComfyUI cfg 1.2 à 1.5.

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

## Taille et format {#size-and-aspect-ratio}

- **Côtés en multiples de 16.** `sampling.py` de Krea arrondit par excès et affiche un avertissement ; diffusers arrondit par excès avec un avertissement journalisé ; l'adaptateur d'édition AnyPaint exige une toile dont les dimensions sont multiples de 16.
- **Turbo de 1K à 2K, Raw jusqu'à environ 1K.** Le pré-entraînement a été réalisé en 256/512/1024 px, par lots de même format.
- **Échelle 1K** (liste de tailles hébergée par Krea, toutes multiples de 16) : 1024x1024, 1184x896, 1248x832, 1376x768, 928x1152, 832x1248, 768x1376.
- Pour le 2K sur Turbo, multipliez une taille 1K par environ 1.41 et arrondissez au multiple de 16. Cette valeur est dérivée, et non publiée par Krea.

```python
def krea_2k(w: int, h: int, scale: float = 2 ** 0.5) -> tuple[int, int]:
    """Scale a 1K ladder size to ~2 MP and snap both sides to multiples of 16."""
    return (int(round(w * scale / 16)) * 16, int(round(h * scale / 16)) * 16)

krea_2k(1248, 832)  # (1760, 1184)
```

## Forme du prompt de génération d'images {#text-to-image-prompt-form}

Krea pose la règle dans `docs/prompting.md` et dans le prompt d'expansion LLM `docs/expansion.txt` : utiliser un langage naturel, en un paragraphe cohérent. Les descriptions longues et précises fonctionnent mieux, même si les courtes restent acceptées.

- **Un paragraphe, sans puces, titres, JSON ni markdown.** Le bloc de LoRA bbox ci-dessous est la seule exception.
- **Nommer le médium en début de phrase.** Écrivez « An editorial portrait photograph of... » ou « A macro photograph of... ». Le prompt d'expansion traite « photo of » comme un médium à conserver.
- **Garder chaque sujet avec ses propres attributs et actions.** Utilisez des termes spatiaux concrets : left, right, foreground, behind, holding.
- **Toujours décrire la lumière.** Précisez la qualité et la direction (« soft window light from the left », « harsh noon sun », « warm low sunlight from the right »). Chaque exemple photo officiel le fait.
- **Photoréalisme.** Précisez les détails de surface concrets et les petites imperfections (pores de la peau, taches de rousseur discrètes, mèches rebelles, chaussures éraflées, sièges en vinyle usés), le type de plan et la profondeur de champ (medium close-up, shallow depth of field), le grain du film ou le flou de mouvement si souhaité. Le rapport technique indique que le flou de mouvement et le flou doux ont été conservés volontairement dans les données. Les numéros d'objectif (« 85mm at f/2 ») apparaissent dans un guide d'un fournisseur et ne sont démontrés ni dans un sens ni dans l'autre.
- **Texte dans l'image.** Placez les mots exacts entre guillemets doubles et gardez-les courts. Le texte secondaire en arrière-plan n'est pas fiable ; un texte déformé est un mode d'échec documenté.
- **Les listes descriptives séparées par des virgules sont dans la distribution.** 8 des 20 exemples Turbo officiels sont des listes de descripteurs séparés par des virgules, et plusieurs prompts de widgets des fiches se terminent par un `, <style tag>`.
- **Pas de formules de qualité génériques, pas de poids.** « masterpiece, best quality, 8k » n'apparaît dans aucun exemple officiel ; la pondération `(word:1.2)` ne fonctionnerait pas de façon fiable (une source communautaire).
- **Décrire ce qui est présent plutôt que « no X ».** Écrivez « an unlit torch », et non « a torch without flame » ; « an empty courtyard at dawn », et non « a courtyard, no people ».
- **Seul l'anglais est documenté.** La fiche déclare `language: en`. Ne gardez des mots non anglais que comme texte à rendre, entre guillemets, et considérez même cet usage comme non testé.

### Exemples de prompts {#example-prompts}

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

### Réécritures {#rewrites}

| Au lieu de | Écrire |
|---|---|
| `masterpiece, best quality, 8k, (sharp:1.3)` | détails concrets : « fine skin pores, crisp fabric weave, sharp focus on the eyes » |
| « a Paris street, no people » | une scène sans foule : « a quiet cobbled side street at dawn, shutters closed » |
| « torch without flame » | « an unlit torch » |
| prompt négatif « blurry, deformed » sur Turbo | rien : il n'est pas évalué ; décrivez positivement la mise au point souhaitée |
| description en russe ou en langue mixte | description en anglais ; mots entre guillemets uniquement pour le texte rendu |

### Folklore écarté {#rejected-folklore}

- **« L'ordre officiel de légende de Krea »** (Sujet -> Apparence -> Accessoires -> Composition -> Environnement -> Éclairage -> Esthétique, souvent « en deux paragraphes »). Il provient d'un message communautaire dans l'onglet discussion du modèle, et un nœud ComfyUI l'a reconditionné comme « le prompt système officiel ». Le véritable prompt système de Krea demande un paragraphe unique, sans ordre de sections imposé. Cet ordre est une habitude sans danger, et non un format appris.
- **« CFG 0.0 dans ComfyUI »** pour Turbo : voir la règle de conversion ci-dessus.
- **Prompts négatifs sur Turbo :** voir la section suivante.
- **Contrôles hébergés sur les poids ouverts :** les niveaux de créativité, curseurs, moodboards et références de style n'existent que dans Medium/Large hébergés. Le « Krea 2 Prompting Guide » de fal précède la publication ouverte et cible les modèles hébergés.
- **« Les deux variantes ont été entraînées en 2048 » :** Raw est documenté jusqu'à 1K ; les étapes de pré-entraînement se sont arrêtées à 1024.

## Budget de tokens et langue {#token-budget-and-language}

L'encodeur enveloppe le prompt dans un gabarit système fixe (« Describe the image by detailing the color, shape, size, texture, quantity, text, spatial relationships of the objects and background »). Le code de référence de Krea, diffusers et DiffSynth complètent ou tronquent à 512 positions après avoir retiré le préfixe système de 34 tokens ; un suffixe assistant de 5 tokens suit le prompt.

- **Plafond du prompt utilisateur : environ 507 tokens** dans le code de référence de Krea, diffusers et DiffSynth. La partie au-delà est coupée silencieusement.
- **ComfyUI ne tronque pas** (son tokenizer Qwen3-VL n'a pas de plafond de 512). Un même prompt long se comporte donc différemment selon le runtime.
- Gardez les prompts sous environ 500 tokens et placez l'essentiel en premier.
- Taux mesurés avec le tokenizer Qwen : en anglais, environ 1.3 à 1.4 token par mot (environ 360 à 390 mots tiennent dans le plafond) ; le plus long exemple officiel fait 252 tokens. L'exemple officiel « mouse » de 84 mots fait 108 tokens en anglais ; une traduction en russe en a demandé 215, soit 2.0x.

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-VL-4B-Instruct")  # the encoder Krea 2 uses
n = len(tok(prompt)["input_ids"])
print(n, "tokens;", "over the 507 cap" if n > 507 else "fits")
```

## Prompts négatifs et suppression {#negative-prompts-and-suppression}

- **Turbo, avec ses réglages, n'évalue jamais le négatif.** L'échantillonneur de Krea saute la branche inconditionnelle à guidance 0 ; ComfyUI la saute à cfg 1.0 (`uncond + 1 * (cond - uncond) = cond`) ; diffusers ignore `negative_prompt` lorsque `guidance_scale <= 0` ; l'API Turbo de fal n'a pas de champ négatif. Les listes négatives recopiées des fiches LoRA de l'ère Raw (« airbrushed, plastic skin, waxy ») ne font rien sur Turbo.
- **Raw avec un CFG réel (ComfyUI cfg > 1) utilise le négatif.** La valeur par défaut est la chaîne vide.
- **La négation dans le prompt positif n'est pas fiable.** Dans nos tests, un fond de rue avec « an empty ... street, no people, no passers-by » a donné 16 visages supplémentaires contre 13 sans cette formulation (une comparaison, une seed par cellule) : cela n'a pas retiré les personnes, et une seule comparaison ne permet pas d'affirmer qu'elle les ajoute.

Pour supprimer un élément sur Turbo :

1. Reformulez positivement (« unlit torch », « empty courtyard at dawn »).
2. Choisissez une scène qui n'appelle pas l'élément indésirable : une rue de ville ensoleillée attire les passants (remède non testé en A/B).
3. Utilisez le nœud communautaire NAG (Normalized Attention Guidance), qui assure un contrôle négatif à cfg 1.0 via l'attention ; valeurs par défaut phi 4.0, tau 2.5, alpha 0.25.
4. Utilisez Raw avec un CFG réel, en acceptant que Raw soit plus lent et non réglé pour les images finales.

## Déclencheurs de LoRA {#lora-triggers}

**Placez le déclencheur là où les légendes d'entraînement de cette LoRA le plaçaient.** Entraînez les LoRA sur Raw, utilisez-les sur Turbo.

- **LoRA de style officielles de Krea :** une expression descriptive à la **fin** du prompt, force 1.0 sur les fiches (le gabarit ComfyUI livre 0.8 et ajoute le déclencheur avec `", "`).

| Dépôt | Déclencheur (à ajouter à la fin) |
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

- **LoRA de personnage** entraînées avec un jeton de type nom : jeton en premier, utilisé comme sujet, puis traits stables, puis scène. Notre forme de préfixe : `character_<id>_person, woman, in her twenties, dark hair, long hair, <scene prose>`.
- **LoRA de réalisme communautaires** diffèrent : certaines n'ont pas de déclencheur, d'autres un préfixe, d'autres un suffixe. Prenez la position indiquée sur la fiche de cette LoRA, et non dans des tableaux de blogs.
- Ne cumulez pas des mots de style qui s'opposent à une LoRA de style. fal autorise au maximum 3 LoRA par appel, avec une échelle de 0 à 4.
- **Légendes pour vos propres LoRA** (guide DreamBooth de diffusers pour Krea 2) : pour un style, décrivez le contenu que vous ne voulez pas figer dans le modèle et ajoutez une expression déclencheur descriptive ; pour un personnage, un mot déclencheur convient si les légendes nomment la classe, les vêtements, la pose, le cadre et la lumière, mais pas le visage.

## Les éditions nécessitent un adaptateur {#edits-need-an-adapter}

Krea 2 de base n'a **pas de chemin d'édition conditionné par une référence**. Le DiT ne dispose d'aucune entrée de latent de référence ni d'inpainting : une référence VAE passée par un `CLIPTextEncode` classique ou par le nœud d'encodage de Qwen-Image-Edit est donc silencieusement ignorée. Les chemins d'édition que nous connaissons reposent sur une LoRA d'adaptateur accompagnée de son nœud de patch.

| Tâche | Adaptateur | Prompt |
|---|---|---|
| Remplacer l'arrière-plan, garder la personne | AnyPaint (cache K/V activé) | Uniquement le nouvel arrière-plan plus « matching the existing light ». Jamais la personne conservée |
| Peindre un objet dans une zone | AnyPaint, zone = masque blanc | L'objet en prose simple plus la lumière à assortir |
| Édition par instruction (recolorer, restyler) | LoRA d'édition `ComfyUI-Krea2-Ostris-Edit`, `comfyui-krea2edit` | Instruction impérative : « recolor the car to matte black » |
| Remplir une zone noircie | LoRA `krea2-inpaint-edit` sur les nœuds d'édition Ostris ; échantillonner à la taille de la référence (voir ci-dessous) | Ce qui doit remplir la zone |
| Composer une nouvelle image par boîtes | Coordonnées dans le prompt ; LoRA bbox facultative | Boîtes JSON, voir la section suivante |

- **Convention de masque :** blanc = régénérer, noir = conserver. Toile en multiples de 16.
- **Avec l'adaptateur Krea2Edit, gardez la sortie à 2 MP ou moins** (son README, source unique) : au-delà de sa plage d'entraînement, du contenu source peut s'infiltrer. AnyPaint n'indique aucune limite de ce type.
- **Suppressions :** les mêmes notes indiquent que Turbo distillé à cfg 1 tend à redessiner le sujet et recommandent Raw, cfg 3 (convention standard), environ 20 étapes (source unique).

### Remplacement d'arrière-plan : décrire uniquement le nouvel arrière-plan {#background-replacement-describe-only-the-new-background}

```text
A rain-washed evening street in an old European city, warm shop windows and wet cobblestones
reflecting orange light, soft haze in the distance, matching the existing light.
```

- Décrivez le nouvel arrière-plan et demandez que la lumière s'y accorde. Ne mentionnez pas du tout la personne conservée : ni le jeton de personnage, ni « the woman in front », ni « behind her ». Des personnes en arrière-plan sont acceptables si vous les voulez.
- La fiche d'AnyPaint demande elle-même « a prompt describing the complete desired output image ». L'arrière-plan seul est notre pratique ; un A/B contrôlé entre les deux n'a pas été réalisé.
- *In our tests* (3 rendus x 2 arrière-plans x 5 adaptateurs d'édition, nombre de visages hors masque de la personne conservée ; originaux avec les mêmes masques : 0) : une seconde copie, plus petite, de la personne provenait surtout de l'échelle d'échantillonnage et non du prompt. Retirer la personne du prompt et supprimer la LoRA de personnage n'a fait baisser les visages supplémentaires que de 30 à 24/25.
- *In our tests*, la cause principale semblait être l'échelle : l'encodeur d'édition Ostris réduit la référence à environ 1 MP (`REF_LATENT_MAX_PIXELS = 1024*1024`), et échantillonner une toile de 2048 a redessiné la personne à l'échelle de la référence : le visage en (1092, 726), large de 940 px, est réapparu en (546, 366), large d'environ 460 px. Échantillonner à la taille de la référence puis agrandir le nouvel arrière-plan a supprimé la copie ; les visages supplémentaires sont passés de 28 à 12, presque tous des passants que le prompt de rue demandait.
- Dans les mêmes essais, AnyPaint a conservé la personne à sa place à chaque fois : c'est donc l'adaptateur que nous utilisons pour le remplacement d'arrière-plan.

### Inpainting de zone {#region-inpaint}

- Marquez la zone avec le masque et nommez l'objet en prose simple, plus la lumière. Le masque indique l'emplacement ; le prompt n'a pas besoin de coordonnées.
- *In our tests* (AnyPaint, 2 images x 3 objets x 2 formes de boîte x 3 seeds = 72) : la variation absolue moyenne hors de la boîte est restée égale ou inférieure à 1.06, et de 15 à 49 à l'intérieur. Ajouter la LoRA bbox n'a rien changé de mesurable (vélo 33.6 contre 33.8, chien 40.5 contre 40.9, plante 35.5 contre 34.5).
- Dans ces mêmes tests, une bande large et basse le long du bas d'une image 9:16 a produit la variation la plus faible (15 à 26) pour deux objets sur trois ; considérez de telles boîtes comme suspectes tant qu'elles n'ont pas été vérifiées à l'œil ou avec un détecteur.

## Mise en page par boîtes (LoRA bbox) {#box-layout-bbox-lora}

La LoRA bbox krea2 (modèle Civitai 2897864) prend des boîtes d'objets au format JSON, en coordonnées normalisées 0..1000, `[x1, y1, x2, y2]`, sans mot déclencheur. Le bloc Format de la fiche place une phrase avant le JSON :

```text
The all objects uses the following bbox.
{"objects": {"a golden retriever sitting": [40, 500, 420, 1000], "a red bicycle": [560, 450, 980, 1000]}}
A sunny city park with a gravel path and tall linden trees, soft afternoon light, photograph.
```

- L'auteur de la fiche qualifie le format de souple (« can just write the coordinates ») ; les exemples de prompts intégrés varient l'ordre, placent parfois le JSON en dernier et omettent parfois la phrase. Ce qui compte, c'est un bloc JSON valide avec des boîtes cohérentes (x1 < x2, y1 < y2).
- Force d'exemple de l'auteur : 0.75. La fiche note que les sujets ont tendance à être rendus grands et centrés, et que Krea 2 de base ne suit les coordonnées que par moments et peut les imprimer sous forme de texte.
- Les règles d'expansion officielles interdisent le JSON dans les prompts ; ce bloc est propre à l'adaptateur. Ne l'ajoutez pas aux prompts ordinaires.
- *In our tests* (6 mises en page symétriques x 4 variantes x 2 seeds ; réussite = centre du visage du personnage à l'intérieur de sa boîte) : mots simples 0/12, coordonnées JSON sans LoRA 5/12, LoRA 0.75 3/12, LoRA 1.0 5/12. Les petites silhouettes ont échoué dans toutes les variantes. Les coordonnées seules dans le texte déplacent déjà le sujet vers sa boîte ; la LoRA n'a rien ajouté de mesurable à cette taille d'échantillon. Le placement reste approximatif.

## Adaptateur d'angle de caméra (krea2-anygles) {#camera-angle-adapter-krea2-anygles}

Une Control-LoRA et 4 nœuds ComfyUI qui redessinent une personne sous un nouveau lacet, une élévation ou une distance, pilotés par une carte de normales SAM 3D Body et une phrase de caméra fixe (« Same figure. Move the camera 310 degrees to the left relative to the input view. »). Réglages de l'auteur : 8 étapes, cfg 1, force 1.0, référence de 384 px, au plus environ 2 MP. Un chargeur LoRA classique supprime sa projection de contrôle. Détails, étapes d'exécution et notre test d'orbite : [[krea-2-anygles]].

## Pièges {#gotchas}

- **Problème :** une image Turbo ignore totalement le prompt dans ComfyUI. -> **Correctif :** le cfg vaut 0 (le « 0.0 » de Krea recopié). Réglez cfg 1.0.
- **Problème :** le prompt négatif n'a aucun effet. -> **Correctif :** Turbo à cfg 1 ne le calcule jamais. Reformulez positivement, utilisez le nœud NAG, ou passez à Raw avec un CFG réel.
- **Problème :** la fin d'un prompt long est ignorée dans diffusers mais pas dans ComfyUI. -> **Correctif :** l'encodeur de référence tronque vers 507 tokens et ComfyUI ne tronque pas. Raccourcissez sous environ 500 et placez l'essentiel en premier.
- **Problème :** une seconde copie, plus petite, de la personne apparaît après un remplacement d'arrière-plan avec un adaptateur d'édition par inpainting. -> **Correctif :** l'encodeur d'édition Ostris plafonne la référence à environ 1 MP ; dans nos tests, échantillonner à cette taille puis agrandir a supprimé la copie. Ou utilisez AnyPaint.
- **Problème :** « no people » donne tout de même des passants. -> **Correctif :** dans notre unique comparaison, la négation ne les a pas retirés. Choisissez un lieu ou un moment de la journée sans foule (remède non testé en A/B).
- **Problème :** une LoRA de style paraît faible. -> **Correctif :** les déclencheurs de style officiels vont à la fin du prompt ; consultez la fiche pour les LoRA communautaires.
- **Problème :** la documentation hébergée de Krea déconseille « Turbo » pour un travail photoréaliste final. -> **Correctif :** cette page décrit Medium Turbo hébergé ; la fiche du Turbo ouvert montre des sorties photoréalistes. Les checkpoints hébergés et ouverts ne correspondent pas publiquement un à un.
- **Problème :** une taille comme 1250x830 fonctionne dans un outil et échoue avec l'adaptateur d'édition. -> **Correctif :** ramenez vous-même les côtés à des multiples de 16 avant toute exécution.

## Voir aussi {#see-also}

- [[krea-2]] - historique des versions, surfaces hébergées vs ouvertes
- [[krea2-realism]] - lignée de LoRA de réalisme communautaires pour Krea 2
- [[krea-2-outpaint]] - adaptateur d'outpainting pour Krea 2
- [[krea-2-anygles]] - adaptateur de point de vue caméra pour une personne
- [[flux-klein-9b-inference]] - la même discipline « figer le checkpoint et le runtime » pour FLUX.2 [klein]
- [[diffusion-lora-training]] - l'entraînement de LoRA comme expérience liée à une version
- [[object-removal-inpainting]] - suppression et inpainting hors Krea
- [[flow-matching]] - la famille d'échantillonneurs derrière Krea 2

## Sources {#sources}

Officielles :

- Dépôt Krea 2, README (réglages Turbo/Raw, multiples de 16) : https://github.com/krea-ai/krea-2
- Guide de prompting : https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md
- Prompt système d'expansion LLM : https://github.com/krea-ai/krea-2/blob/main/docs/expansion.txt
- Encodeur (gabarit, 512 positions, troncature) : https://github.com/krea-ai/krea-2/blob/main/encoder.py
- Échantillonneur (formule de guidance, complétion à 16) : https://github.com/krea-ai/krea-2/blob/main/sampling.py
- Fiche modèle Turbo : https://huggingface.co/krea/Krea-2-Turbo
- Fiche modèle Raw : https://huggingface.co/krea/Krea-2-Raw
- Rapport technique : https://www.krea.ai/blog/krea-2-technical-report
- Fiche de LoRA de style officielle (même modèle pour les neuf) : https://huggingface.co/krea/Krea-2-LoRA-softwatercolor
- Documentation Krea 2 hébergé (contrôles réservés à l'hébergement, liste des tailles) : https://www.krea.ai/docs/user-guide/features/krea-2

Code et documentation de service :

- Documentation du pipeline Krea 2 de diffusers : https://huggingface.co/docs/diffusers/en/api/pipelines/krea2
- Source du pipeline diffusers (convention de guidance, arrondi à 16, longueur 512) : https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/krea2/pipeline_krea2.py
- Guide d'entraînement LoRA Krea 2 pour diffusers : https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/README_krea2.md
- Tutoriel ComfyUI Krea 2 (fichiers, déclencheurs LoRA officiels) : https://docs.comfy.org/tutorials/image/krea/krea-2
- Gabarit Turbo officiel de ComfyUI : https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_krea2_turbo_t2i.json
- Encodeur de texte Krea 2 de ComfyUI (gabarit, retrait du préfixe) : https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/text_encoders/krea2.py
- Tokenizer Qwen3-VL de ComfyUI (pas de plafond de 512) : https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/text_encoders/qwen3vl.py
- Échantillonneur ComfyUI (cfg 1.0 saute l'inconditionnel) : https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/samplers.py
- Cookbook SGLang Krea 2 : https://docs.sglang.io/cookbook/diffusion/Krea/Krea-2
- DiffSynth-Studio Krea 2 : https://diffsynth-studio-doc.readthedocs.io/en/latest/Model_Details/Krea-2.html
- Qwen3-VL-4B-Instruct (tokenizer pour le comptage) : https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct

Fournisseurs :

- fal, guide des poids ouverts : https://fal.ai/learn/tools/how-to-use-krea-2-open-source
- fal, guide de prompting des modèles hébergés (antérieur à la publication ouverte) : https://fal.ai/learn/tools/krea-2-prompting-guide
- Point d'accès Turbo de fal (pas de champ steps, guidance ou négatif ; la variante LoRA accepte jusqu'à 3 LoRA) : https://fal.ai/models/fal-ai/krea-2/turbo
- Scenario, les essentiels de Krea 2 : https://help.scenario.com/articles/1463593157-krea-2-the-essentials

Adaptateurs et communauté :

- Fiche AnyPaint : https://huggingface.co/yijunwang2/krea2-anypaint
- Nœuds ComfyUI AnyPaint : https://github.com/alexw5702-afk/krea2-anypaint
- LoRA krea2-inpaint-edit : https://huggingface.co/Cierpliwy/krea2-inpaint-edit
- Nœuds d'édition Ostris (référence d'environ 1 MP) : https://github.com/ostris/ComfyUI-Krea2-Ostris-Edit
- Nœuds Krea2Edit (instructions, 2 MP, suppressions sur Raw) : https://github.com/lbouaraba/comfyui-krea2edit
- Fiche de la LoRA bbox : https://civitai.com/models/2897864
- Analyse de code du chemin de référence manquant : https://github.com/ethanfel/ComfyUI-Krea2TextEncoder
- Nœud NAG pour Krea 2 : https://github.com/iljung1106/ComfyUI-Krea2-NAG
- Origine de « l'ordre officiel des légendes » : https://huggingface.co/krea/Krea-2-Turbo/discussions/4
- Le nœud qui le reconditionne : https://github.com/WaitWut/krea2-structured-prompt
- Échec de la négation (« torch without flame ») : https://huggingface.co/krea/Krea-2-Turbo/discussions/13
- Guide communautaire ComfyUI (utile, mais donne cfg 0.0 pour ComfyUI) : https://www.instasd.com/post/krea-2-prompt-and-style-guide-comfyui
- LoRA de réalisme de l'ère Raw avec liste négative : https://huggingface.co/inlineresearch/skin-lora-krea-2-raw
- Nœuds krea2-anygles : https://github.com/alexw5702-afk/krea2-anygles
- Fiche krea2-anygles : https://huggingface.co/yijunwang2/krea2-anygles

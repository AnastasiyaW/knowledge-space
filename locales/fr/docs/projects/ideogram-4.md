---
title: "Ideogram 4"
category: projects
tags: [ideogram, ideogram-4, ideogram-4-development, ideogram_4, project]
aliases: ["Ideogram 4"]
level: 3
source_sha256: 2ed9e9afc883dffbcc3c45325b99edeb6b3ecaa38d31c0cace7db4c0da021395
translation: machine
translated_at: '2026-10-24'
---
# Ideogram 4 {#ideogram-4}

**Ligne de développement :** `project:ideogram-4` · fil `ideogram-4-development`  
**Événements :** 2 datés, 2026-06-04 → 2026-07-14 · **Recherche :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

Ideogram 4 est un modèle d'image à entrées JSON structurées, destiné aux designers et développeurs qui ont besoin d'un contrôle précis du texte, de la composition et de la palette. Il remplace les workflows reposant sur des prompts plats et génériques.

- rend du texte littéral dans l'image et une typographie multilingue
- place objets et texte à l'aide de boîtes englobantes normalisées
- contrôle les palettes, l'éclairage, le style et la composition via JSON
- fonctionne avec des poids quantifiés soumis à accès restreint, l'API Ideogram, ComfyUI, ainsi que des dérivés de vitesse fal distincts

## Ligne de développement {#development-line}

- **2026-06-04 — Source d'Ideogram 4, variantes de modèle et intégration ComfyUI enregistrées.** Le code d'inférence et les poids FP8/NF4 soumis à accès restreint sont devenus publics. La version introduisait un contrôle JSON structuré pour le texte, les palettes et la mise en page par boîtes englobantes. ComfyUI a annoncé un support dès le jour zéro.
- **2026-07-14 — Variantes Ideogram v4 Instant et Fast enregistrées.** `ideogram-v4-instant` est un checkpoint BF16 pre-QAD à 8 étapes. `ideogram-v4-fast` est un checkpoint FP4/QAD à 20 étapes. Les deux sont développés par fal à partir de la base FP8 d'Ideogram et suppriment le CFG à l'exécution.

## Ce qui a changé {#what-changed}

2026-06-04 — Ideogram 4.0 est entré dans le workflow local. La publication officielle est datée du 2026-06-03. Le code d'inférence et les poids FP8/NF4 soumis à accès restreint sont devenus publics. Ils fournissent un contrôle JSON structuré pour le texte, les palettes et la mise en page par boîtes englobantes. ComfyUI a annoncé un support dès le jour zéro.

2026-07-14 — fal a ajouté deux dérivés distincts à distillation de vitesse, plutôt qu'une nouvelle version canonique d'Ideogram. `ideogram-v4-instant` est un checkpoint BF16 pre-QAD à 8 étapes. `ideogram-v4-fast` est un checkpoint FP4/QAD à 20 étapes. Les deux sont développés par fal à partir de la base FP8 d'Ideogram et suppriment le CFG à l'exécution.

Constaté aujourd'hui, 2026-09-04 — la documentation officielle désigne toujours l'endpoint canonique Ideogram 4.0. Il accepte soit `text_prompt`, soit `json_prompt`. Il prend en charge des sorties en 1K/2K et les vitesses Default/Turbo/Quality. `FLASH` figure dans la liste mais renvoie actuellement HTTP 400. La licence actuelle distingue les poids publics à usage non commercial, l'usage commercial via API, l'auto-hébergement sous licence et les conditions Enterprise.

## Comment l'utiliser {#how-to-use-this}

Nous évaluons Ideogram 4 via les chemins liés (source, variantes de modèle, ComfyUI) après le 2026-06-04. Nous comparons séparément les variantes Instant et Fast après le 2026-07-14 lorsque nous choisissons une voie d'accès à Ideogram 4.

1. Commencez par choisir le mode de déploiement et la voie de licence. Utilisez l'API hébergée pour la génération commerciale. N'utilisez les poids quantifiés publics que pour la recherche, l'évaluation, le prototypage ou un usage personnel, sauf si vous obtenez des droits d'auto-hébergement commercial.
  — <https://ideogram.ai/licensing/>
2. Pour la génération hébergée, appelez `POST /v1/ideogram-v4/generate` avec une `Api-Key` et exactement un des deux champs `text_prompt` ou `json_prompt`. Sélectionnez 1K ou 2K, puis Default, Turbo ou Quality, et téléchargez rapidement l'image renvoyée.
  — <https://developer.ideogram.ai/api-reference/generate-images/generate-v4>
3. Commencez l'exploration avec `text_prompt`, qui active Magic Prompt. Passez à `json_prompt` lorsque la palette, la mise en page ou le texte littéral doivent respecter votre spécification.
  — <https://developer.ideogram.ai/api-reference/generate-images/generate-v4>
4. Pour les designs contrôlés, construisez `high_level_description`, `style_description` et `compositional_deconstruction`. Utilisez des éléments `text` typés, des valeurs `text` littérales et des coordonnées `bbox` normalisées si nécessaire.
  — <https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md>
5. Pour l'inférence locale du modèle de base, acceptez la restriction d'accès sur Hugging Face et authentifiez-vous avec `hf auth login`. Installez le dépôt officiel, choisissez le checkpoint NF4 ou FP8, puis exécutez le point d'entrée d'inférence fourni.
  — <https://github.com/ideogram-oss/ideogram4>
6. Pour un workflow à base de nœuds, utilisez le support d'Ideogram 4 dans ComfyUI et sa structure de prompt JSON, plutôt que d'aplatir la mise en page en prompt en prose.
  — <https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui>
7. Pour une voie fal explicitement orientée latence, configurez `FAL_KEY` côté serveur et appelez `ideogram/v4/instant`. Conservez l'identification de ses résultats comme dérivé fal, et non comme sortie de la base Ideogram 4.0.
  — <https://fal.ai/models/ideogram/v4/instant/api>

## Bonnes pratiques {#best-practices}

- Pour un rendu exact du texte, placez le texte littéral dans un élément JSON `text` ou mettez-le entre guillemets dans la prose. Limitez chaque chaîne à environ 5 à 7 mots et privilégiez les mots aux petits symboles numériques.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Respectez l'ordre des clés JSON requis, utilisez des valeurs de palette en majuscules `#RRGGBB` et exécutez le CaptionVerifier avant de valider une recette de prompt locale.
  — <https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md>
- Limitez une composition à cinq éléments ou moins. Traitez les boîtes englobantes comme des guides avec une marge plutôt que comme des recadrages, et décrivez le sol ou le plan de fond comme `background`.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Utilisez `V4_QUALITY_48` pour les rendus locaux finaux. Comparez les préréglages Default à 20 étapes et Turbo à 12 étapes avec vos propres images d'acceptation avant de sacrifier la qualité au profit de la vitesse.
  — <https://github.com/ideogram-oss/ideogram4/blob/main/docs/inference.md>
- Ne déployez pas les checkpoints publics à des fins commerciales par présomption. Les conditions actuelles réservent cet usage à l'API hébergée ou à une licence self-serve/Enterprise.
  — <https://ideogram.ai/licensing/>
- Conservez les sorties du modèle de base et des dérivés fal dans des jeux d'évaluation séparés. Instant est un dérivé à 8 étapes et à branche unique développé par fal, et non une exécution du modèle de base identique au checkpoint.
  — <https://huggingface.co/fal/ideogram-v4-instant>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-03/04 — La consigne selon laquelle Ideogram ne devait être utilisé que comme service hébergé fermé est obsolète pour la recherche et le prototypage. Le code d'inférence officiel et les poids publics quantifiés soumis à accès restreint ont rendu l'usage local possible. Cela ne confère pas de droits d'auto-hébergement commercial.
- 2026-06-18 — Les recettes de prompts plats et riches en adjectifs ne constituent plus la valeur par défaut pour la précision avec Ideogram 4. Le JSON structuré est la voie privilégiée pour le contrôle de la typographie, de la palette et de la mise en page.
- 2026-07-14 — Considérer fal Instant ou Fast comme un successeur canonique de type Ideogram 4.1 est obsolète. Ce sont des dérivés fal à distillation de vitesse, et non un remplacement du checkpoint de base 4.0.

## Points encore inconnus {#still-unknown}

- Les deux entrées datées concernent une même famille de modèles de base Ideogram. Les éléments de juillet sont des dérivés de vitesse rédigés par fal, et non une publication officielle du modèle central d'Ideogram.
- Aucune source examinée ne fournit d'évaluation indépendante montrant que les variantes fal à 8 ou 20 étapes préservent la fidélité typographique et de mise en page du modèle de base 4.0 pour des charges de production.
- Les pages officielles publiques examinées n'identifient aucun checkpoint de base Ideogram 4.1 ou ultérieur versionné. L'absence de ces informations sur ces pages ne prouve pas qu'il n'existe aucune révision privée ou non annoncée.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://ideogram.ai/news/ideogram-4.0/ | Ideogram 4.0 Press Release | Ideogram | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technical Details: Open model at the forefront of design | 2026-09-04 |
| https://github.com/ideogram-oss/ideogram4 | GitHub - ideogram-oss/ideogram4: Ideogram 4: Open image model at the forefront of design | 2026-09-04 |
| https://huggingface.co/ideogram-ai/ideogram-4-nf4 | ideogram-ai/ideogram-4-nf4 · Hugging Face | 2026-09-04 |
| https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui | Ideogram 4.0 Day-0 Support in ComfyUI: Open Weights and Structured Control | 2026-09-04 |
| https://huggingface.co/fal/ideogram-v4-instant | fal/ideogram-v4-instant · Hugging Face | 2026-09-04 |
| https://huggingface.co/fal/ideogram-v4-fast | fal/ideogram-v4-fast · Hugging Face | 2026-09-04 |
| https://developer.ideogram.ai/api-reference/generate-images/generate-v4 | Generate with Ideogram 4.0 | Ideogram | Documentation | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4-json-prompting/ | How to JSON prompt for Ideogram 4.0 | 2026-09-04 |
| https://ideogram.ai/licensing/ | Licensing | Ideogram | 2026-09-04 |
| https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md | ideogram4/docs/prompting.md at main · ideogram-oss/ideogram4 · GitHub | 2026-09-04 |
| https://github.com/ideogram-oss/ideogram4/blob/main/docs/inference.md | ideogram4/docs/inference.md at main · ideogram-oss/ideogram4 · GitHub | 2026-09-04 |
| https://fal.ai/models/ideogram/v4/instant/api | V4.0q [instant] Text to Image API Docs | fal | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ideogram-4`, fil `ideogram-4-development`, 2 événements datés du 2026-06-04 au 2026-07-14.
- **Note pratique :** Évaluer Ideogram 4 via les chemins liés (source, variantes de modèle, ComfyUI) après le 2026-06-04. Comparer séparément les variantes Instant et Fast après le 2026-07-14 lors du choix d'une voie d'accès à Ideogram 4.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.

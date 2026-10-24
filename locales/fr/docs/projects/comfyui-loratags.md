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

**Ligne de développement :** `project:comfyui-loratags` · fil `comfyui-loratags`  
**Dernier événement :** - · 0 daté(s) depuis - · **Recherché le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

ComfyUI-LoraTags — une paire de nœuds pour les utilisateurs de ComfyUI qui veulent assembler plusieurs LoRA sans perdre leurs trigger words. — LoRA Loader (LoraTags) : charge une pile de LoRA et fournit MODEL, CLIP et TAGS. — CLIP Text Encode (Auto-Tags) : ajoute la chaîne TAGS au prompt texte avant l'encodage. — Tag Manager : à partir du SHA-256 du fichier, demande à Civitai le nom du modèle, les triggers d'origine, jusqu'à quatre aperçus et le lien vers le modèle ; les tags utilisateur sont stockés à côté. Mesure et limite : le dépôt affiche 16 commits, ne publie aucune release, et l'installation via ComfyUI Manager est toujours indiquée comme future. Verdict : c'est un nœud précoce, utilisable pour une installation locale, et non un remplacement d'un LoRA loader éprouvé, avec un long historique de compatibilité.

## Ligne de développement {#development-line}

- La ligne datée n'a pas encore été rédigée ; les éléments connus figurent dans les sections ci-dessous.

## Changements {#what-changed}

2026-07-15 — l'accès anticipé à ComfyUI-LoraTags a été annoncé par l'auteur ; il s'agit d'un événement distinct et antérieur. 2026-07-23 — ComfyUI-LoraTags est apparu sous forme de paquet de deux nœuds : le Loader rassemble les LoRA actives et leurs tags dans TAGS, et Auto-Tags les transmet au conditioning. Le README principal précise les détails manquants : la recherche s'effectue par SHA-256 du `.safetensors`, renvoie jusqu'à quatre aperçus, et la base est enregistrée dans `lora_master_tags.json`. Les documents primaires ne montrent ni version datée ultérieure ni release.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-23, considérez le dépôt GitHub lié comme une piste pour des recherches complémentaires uniquement ; n'en déduisez pas une installation, une release ou une évolution de fonctionnalité prises en charge à partir de cette fiche.

1. Clonez le dépôt dans `ComfyUI/custom_nodes/`, puis redémarrez ComfyUI et effectuez un rafraîchissement forcé de la page (`Ctrl+Shift+R`).
  — <https://github.com/iiTzMYUNG/ComfyUI-LoraTags>
2. Ajoutez `LoRA Loader (LoraTags)` et `CLIP Text Encode (Auto-Tags)` ; reliez la sortie TAGS du loader à l'entrée `tags` de l'encodeur.
  — <https://github.com/iiTzMYUNG/ComfyUI-LoraTags>
3. Ajoutez des lignes LoRA, sélectionnez les fichiers `.safetensors`, réglez la force et activez les lignes voulues ; dans Tag Manager, récupérez les tags depuis Civitai ou ajoutez les vôtres.
  — <https://github.com/iiTzMYUNG/ComfyUI-LoraTags>

## Bonnes pratiques {#best-practices}

- Ne modifiez pas `lora_stack_data` à la main : il est sérialisé par l'interface du nœud.
  — <https://comfy.icu/node/LoraLoaderMasterDB>
- Après une mise à jour du nœud, effectuez un rafraîchissement forcé : son interface est chargée depuis JavaScript, et un cache obsolète peut casser l'affichage.
  — <https://comfy.icu/node/LoraLoaderMasterDB>
- Vérifiez les LoRA actives, leur strength et leurs chemins de fichiers : une ligne désactivée, une strength à 0 ou un fichier déplacé ne seront pas appliqués.
  — <https://comfy.icu/node/LoraLoaderMasterDB>
- Surveillez la longueur du prompt avec une pile importante : Auto-Tags ajoute les triggers dans le même contexte CLIP.
  — <https://comfy.icu/node/CLIPTextEncodeWithTags>

## Remplacé par ceci {#superseded-by-this}

- Rien de marqué comme obsolète pour l'instant.

## Points inconnus {#still-unknown}

- L'historique GitHub confirme 16 commits, mais la page primaire accessible ne montre ni leurs dates ni leurs messages individuels ; aucune modification datée ultérieure n'est affirmée.
- Aucune release GitHub n'est listée sur la page du dépôt ; une chronologie de versions ne peut donc pas être confirmée.
- La demande source mentionne `event_findings` et `new_events`, mais le schéma de réponse requis ne prévoit aucun champ pour eux ; les constats datés sont conservés dans `what_changed`.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/iiTzMYUNG/ComfyUI-LoraTags | GitHub — iiTzMYUNG/ComfyUI-LoraTags README | 2026-09-05 |
| https://comfy.icu/node/LoraLoaderMasterDB | ComfyUI Cloud — LoRA Loader (LoraTags) | 2026-09-05 |
| https://comfy.icu/node/CLIPTextEncodeWithTags | ComfyUI Cloud — CLIP Text Encode (Auto-Tags) | 2026-09-05 |
| https://www.patreon.com/cw/iiTzMYUNG/sitemap?l=it-IT | Plan du site Patreon de iiTzMYUNG | 2026-09-05 |

## Note pour l'agent {#agent-brief}

- **Sujet :** `project:comfyui-loratags`, fil `comfyui-loratags`, 0 événement daté - → -.
- **Note pratique :** Au 2026-07-23, considérez le dépôt GitHub lié comme une piste pour des recherches complémentaires uniquement ; n'en déduisez pas une installation, une release ou une évolution de fonctionnalité prises en charge à partir de cette fiche.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

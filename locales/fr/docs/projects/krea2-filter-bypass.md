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

**Ligne de développement :** `project:krea2-filter-bypass` · fil `krea2-filter-bypass`  
**Dernier événement :** 2026-07-02 · 1 événement daté depuis le 2026-07-02 · **Recherche :** 2026-09-05 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

Krea2 Filter Bypass — LoRA `fedor_bypass.safetensors` pour Krea 2 : il annonce la modification de deux composantes de `txtfusion.projector`, le maintien des dix autres à zéro et un fonctionnement combiné avec d'autres LoRA ; limite : un fichier de 1 024 octets. Les affirmations de suppression des restrictions et d'absence de dérive stylistique ne sont pas confirmées par un test indépendant reproductible. Verdict : il s'agit d'une expérimentation communautaire restreinte, et non d'un mode officiel de Krea ni d'un remplacement de la vérification des règles de la plateforme.

## Ligne de développement {#development-line}

- **2026-07-02 — Enregistrement du modèle public Krea2 Filter Bypass et des liens de discussion.** Le 2026-07-02, l'enregistrement daté reliait Krea2 Filter Bypass à une page de modèle Civitai et à une discussion Reddit. Pris ensemble, ces liens publics marquent un point de développement public important pour le projet, même si les publications sous-jacentes n'ont pas fait l'objet d'une recherche indépendante.

## Ce qui a changé {#what-changed}

2026-07-02 — publication de Krea2 Filter Bypass [Fedor], fichier FP32 `fedor_bypass.safetensors` pour Krea 2, avec des deltas uniquement pour les colonnes 9 et 10.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-02, les praticiens devraient considérer Krea2 Filter Bypass comme disposant d'un historique public de modèle et de discussion, tout en vérifiant de manière indépendante les pages liées avant de se fier à un comportement ou à une compatibilité annoncés.

1. Vérifiez si l'utilisation de cette modification est autorisée dans votre pipeline local et sous licence, ainsi que selon les règles du modèle ; ne la transférez pas vers des services où elle contournerait des restrictions obligatoires.
  — <https://civitai.red/models/2746817/krea2-filter-bypass-fedor?modelVersionId=3089754>
2. Pour une reproduction en recherche, consignez le fichier, le hash, le modèle de base, le seed, le prompt et les paramètres de génération ; la source définit la clé cible `diffusion_model.txtfusion.projector.diff` et les deux deltas.
  — <https://github.com/CliffNodes/fedor_bypass/blob/main/build_fedor_bypass.py>
3. Comparez l'exécution de base et l'exécution modifiée avec le même seed et le même ensemble complet de réglages ; ne transposez pas les conclusions sur la qualité, tirées d'une seule image, à un pipeline de production.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ukh334/i_extracted_the_values_of_krea_2_safery_filters/>

## Bonnes pratiques {#best-practices}

- Considérez l'affirmation d'absence de dérive stylistique comme une hypothèse et effectuez un test A/B avec les mêmes seeds et réglages : les participants à la comparaison décrivent les variantes comme proches, mais non identiques.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ul38ei/made_yet_another_bypass_filter_for_krea_2_this/>
- Vérifiez le contenu et l'origine des petits fichiers de poids, et pas seulement leur nom : le générateur publié crée un tenseur `[1,12]` et ne remplit que les positions 9 et 10.
  — <https://github.com/CliffNodes/fedor_bypass/blob/main/build_fedor_bypass.py>
- Ne combinez pas des modifications de contournement inconnues avec un checkpoint ou une LoRA qui intègre déjà une modification similaire : l'analyse communautaire note que l'intensité et l'effet dépendent du prompt et de l'empilement.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ukh334/i_extracted_the_values_of_krea_2_safery_filters/>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-07-18 — la présentation de Fedor comme un bypass fonctionnellement nouveau par rapport à FilterBypass2 est obsolète : une description ultérieure réduit la différence à la précision des valeurs, et non à un nouveau mécanisme.
- 2026-07-18 — la recommandation de considérer l'absence d'effet sur le style comme mathématiquement garantie ne doit pas être utilisée comme règle d'exploitation sans test A/B indépendant.

## Points encore inconnus {#still-unknown}

- Aucune source primaire de Krea ne confirme que les colonnes 9 et 10 correspondent précisément à un mécanisme de filtre de sécurité, ni que la modification est autorisée par la licence et les règles d'utilisation.
- Aucun benchmark indépendant et reproductible ne confirme l'absence annoncée de dérive stylistique, une meilleure adhérence au prompt, ni la supériorité de la variante FP32 sur FilterBypass2.
- La date du 2026-07-18 correspond à la date de mise à jour de la page Civitai ; le journal des modifications précis, distinct de la description actuelle, n'est pas disponible.
- Les sources décrivent la même variante à deux vecteurs et les fichiers de bypass voisins, et non deux développements distincts portant le même nom.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://civitai.red/models/2746817/krea2-filter-bypass-fedor?modelVersionId=3089754 | Krea2 Filter Bypass [Fedor] - Krea2 Bypass [Fedor] | Krea 2 LoRA | Civitai | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ul38ei/made_yet_another_bypass_filter_for_krea_2_this/ | Made yet another bypass filter for Krea 2 -- this one seems to work well at just defeating the filters and preventing any type of warping | 2026-09-05 |
| https://github.com/CliffNodes/fedor_bypass | CliffNodes/fedor_bypass | 2026-09-05 |
| https://github.com/CliffNodes/fedor_bypass/blob/main/build_fedor_bypass.py | fedor_bypass/build_fedor_bypass.py at main | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ukh334/i_extracted_the_values_of_krea_2_safery_filters/ | I extracted the values of Krea 2 Safety Filters Bypass Files, so you don't have to | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:krea2-filter-bypass`, fil `krea2-filter-bypass`, 1 événement daté du 2026-07-02 au 2026-07-02.
- **Note pratique :** À partir du 2026-07-02, les praticiens devraient considérer Krea2 Filter Bypass comme disposant d'un historique public de modèle et de discussion, tout en vérifiant de manière indépendante les pages liées avant de se fier à un comportement ou à une compatibilité annoncés.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

---
title: "ComfyUI KSampler Matrix Lab — Référence du dépôt"
category: projects
date: 2026-06-05
tags: [comfyui-ksampler-matrix-lab, comfyui_ksampler_matrix_lab, project, repository-reference]
aliases: ["ComfyUI KSampler Matrix Lab"]
level: 2
source_sha256: 58db1761192ab2ed7c2383768c0af73b5559958ebece342911c2d0d272268048
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI KSampler Matrix Lab — Référence du dépôt {#comfyui-ksampler-matrix-lab-repository-reference}

**Ligne de développement :** `project:comfyui-ksampler-matrix-lab` · fil `repository-reference`  
**Dernier événement :** 2026-06-05 · 1 événement daté depuis le 2026-06-05 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

ComfyUI KSampler Matrix Lab — deux nœuds ComfyUI destinés aux artistes et aux évaluateurs de modèles : KSampler Matrix Lab compare des combinaisons sampler/scheduler, Model Matrix Lab compare les checkpoints installés. Limites : jusqu'à 9 emplacements de sampler, 9 emplacements de scheduler et 20 emplacements de modèle ; la génération s'exécute séquentiellement. Verdict : utilisable pour des tests visuels contrôlés, mais la compatibilité dépend toujours de la version locale de ComfyUI, des modèles et des custom nodes.

## Ligne de développement {#development-line}

- **2026-06-05 — Référence au dépôt ComfyUI KSampler Matrix Lab.** Le 2026-06-05, cette ligne de développement a été reliée au dépôt GitHub de ComfyUI KSampler Matrix Lab. Ce lien daté établit une référence publique du dépôt pour le projet, mais le contenu de la publication, l'état du dépôt, les fonctionnalités et le statut des versions n'ont pas fait l'objet de recherches.

## Ce qui a changé {#what-changed}

2026-06-05 — l'extension était disponible sous forme de package custom node pour des grilles comparatives sampler/scheduler étiquetées ; le lancement public de l'auteur est daté du 2026-06-04 et décrivait le comportement en graine identique, en graine incrémentée, l'en-tête de métadonnées et les cellules d'erreur.

## Mode d'emploi {#how-to-use-this}

Au 2026-06-05, les praticiens doivent examiner le dépôt lié avant de considérer ComfyUI KSampler Matrix Lab comme un composant de workflow utilisable ; son installation, son comportement et sa maturité restent non vérifiés.

1. Cloner le dépôt dans `ComfyUI/custom_nodes`, puis redémarrer ComfyUI.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>
2. Ajouter `KSampler Matrix Lab` ou `Model Matrix Lab` depuis la catégorie des extensions et le connecter à un workflow de génération classique.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>
3. Connecter la sortie unique `IMAGE` du nœud à Preview Image ou Save Image ; éventuellement, charger le fichier JSON de workflow fourni.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>

## Bonnes pratiques {#best-practices}

- Garder fixes le prompt, le modèle, le latent et la graine lors de la comparaison des réglages de sampler et de scheduler ; n'utiliser l'incrément de graine par cellule que si l'on teste aussi la variation.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>
- Borner la matrice avec `max_combinations` ; réduire le nombre de samplers ou de schedulers sélectionnés avant d'augmenter cette limite.
  — <https://www.runcomfy.com/comfyui-nodes/ComfyUI-KSampler-Matrix-Lab/k-sampler-matrix-lab>
- Conserver les étiquettes et l'en-tête d'exécution activés lorsque les résultats seront relus ou partagés, et inspecter les cellules d'erreur lorsque la continuation est activée.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points inconnus {#still-unknown}

- Le dépôt ne comporte aucune version étiquetée, et la vue d'ensemble accessible de première main n'expose pas de journal des modifications fiable, daté et commit par commit, au-delà de la publication initiale de juin 2026.
- Aucun test d'exécution indépendant sur une installation locale récente de ComfyUI n'était disponible ; la compatibilité actuelle est donc documentée et non vérifiée en exécution.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab | GitHub — btitkin/ComfyUI-KSampler-Matrix-Lab | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1twjm31/comfyui_node_to_compare_multiple_samplers_and/ | ComfyUI node to compare multiple samplers and schedulers at once | 2026-09-05 |
| https://www.runcomfy.com/comfyui-nodes/ComfyUI-KSampler-Matrix-Lab/k-sampler-matrix-lab | KSampler Matrix Lab | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:comfyui-ksampler-matrix-lab`, fil `repository-reference`, 1 événement daté du 2026-06-05 → 2026-06-05.
- **Note pratique :** Au 2026-06-05, les praticiens doivent examiner le dépôt lié avant de considérer ComfyUI KSampler Matrix Lab comme un composant de workflow utilisable ; son installation, son comportement et sa maturité restent non vérifiés.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

---
title: "MiniMax-H3 Turbo LoRA"
category: projects
date: 2026-08-06
tags: [minimax-h3-turbo-lora, minimax_h3_turbo_lora, project]
aliases: ["MiniMax-H3 Turbo LoRA"]
level: 2
source_sha256: 806ab26f3197dcf77473d6886509367823a094edbc3813fdb6ad37beb1a37ca5
translation: machine
translated_at: '2026-10-24'
---
# MiniMax-H3 Turbo LoRA {#minimax-h3-turbo-lora}

**Ligne de développement :** `project:minimax-h3-turbo-lora` · fil `minimax-h3-turbo-lora`  
**Dernier événement :** 2026-08-06 · 1 événement daté depuis le 2026-08-06 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

MiniMax-H3 Turbo LoRA est un adaptateur communautaire accompagné de nœuds ComfyUI pour les workflows text-to-video et image-to-video de MiniMax-H3.

- Échantillonnage conjoint audio-vidéo avec moins d'étapes.
- Prise en charge de base des modèles H3 complets et élagués (pruned).
- Sampler personnalisé pour des planifications distinctes de l'audio et de la vidéo.

En pratique, l'échantillonnage demande au minimum 4 étapes, avec une préférence pour 6 à 8 étapes ; l'audio et les mouvements intenses restent au stade de l'aperçu. Utilisez-le pour des itérations rapides, mais validez les plans à mouvement rapide par rapport au workflow de base.

## Ligne de développement {#development-line}

- **2026-08-06 — Ensemble de ressources MiniMax-H3 Turbo LoRA documenté.** Le 2026-08-06, la documentation a relié la ressource de modèle MiniMax-H3 Turbo LoRA à un Space de démonstration, à un dépôt d'intégration ComfyUI et à une ressource de modèle orientée ComfyUI. Cela établit un workflow accessible couvrant la distribution du modèle, la démonstration et l'usage dans ComfyUI. Les ressources liées ne permettent pas à elles seules d'établir leurs dates de publication, versions, auteurs ou affirmations de performance respectifs.

## Changements {#what-changed}

- 2026-08-06 — L'intégration publique ComfyUI a ajouté le loader Turbo LoRA et le sampler 4 étapes, puis la prise en charge des bases élaguées et à courbe, l'application de l'adaptateur à l'exécution et un interrupteur low-VRAM.
- 2026-08-07 — Le checkpoint EMA v4 à l'étape 600 est devenu la recommandation par défaut ; les consignes ont restreint l'échantillonnage pratique à 4–8 étapes et conservé le v1 à l'étape 850 uniquement pour les mouvements intenses à quatre étapes.
- 2026-08-08 — L'intégration des nœuds a corrigé une incohérence d'injection AdaLN pour le conditionnement par référence audio.
- 2026-08-10 — L'intégration a corrigé le calcul du segment de modulation via la recherche dans la table temporelle AdaLN.
- 2026-08-12 — L'intégration a fusionné un correctif de ligne AdaLN pour la référence audio.
- 2026-08-14 — L'intégration a fusionné une contribution amont supplémentaire ; maintenez le nœud personnalisé à jour.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-08-06, évaluez MiniMax-H3 Turbo LoRA via le modèle lié et le chemin d'intégration ComfyUI, plutôt que comme un checkpoint isolé ; vérifiez la compatibilité actuelle, les licences et les prérequis d'installation avant toute utilisation.

1. Installez `Larryvrh/ComfyUI-MiniMax-H3-Turbo` avec ComfyUI-Manager ou clonez-le dans `ComfyUI/custom_nodes`, puis redémarrez ComfyUI.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>
2. Téléchargez le fichier `.safetensors` du Turbo LoRA dans `ComfyUI/models/loras/` et installez le modèle de base MiniMax-H3, les VAE et l'encodeur de texte.
  — <https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora>
3. Partez d'un workflow officiel H3 text-to-video ou image-to-video ; placez le nœud Turbo LoRA entre le loader de modèle de diffusion et `SamplerCustomAdvanced`, puis alimentez ce sampler depuis MiniMax-H3 Turbo Sampler.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>
4. Réglez le scheduler sur `simple`, la force à 1.0, et commencez à 6–8 étapes ; n'utilisez 4 étapes que lorsque la vitesse prime sur la qualité de mouvement.
  — <https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora>

## Bonnes pratiques {#best-practices}

- Utilisez `minimax_h3_turbo_v4_step600_ema.safetensors` pour la plupart des plans ; réservez le v1 à l'étape 850 aux mouvements inhabituellement rapides et intenses, à exactement quatre étapes.
  — <https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora>
- Gardez `low_vram` désactivé pour une application à l'exécution plus nette ; activez-le seulement après un échec par manque de mémoire, en acceptant une sortie plus floue sur les bases quantifiées.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>
- Conservez le Turbo Sampler dans le graphe lors des mises à jour de ComfyUI : il s'adapte à la prise en charge native de `ModelSamplingAV` et préserve une planification audio correcte sur les anciennes versions.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>

## Remplacé par {#superseded-by-this}

- 2026-08-07 — Le v1 à l'étape 850 n'est plus la valeur par défaut générale ; le v4 EMA à l'étape 600 est préféré, sauf pour les clips à mouvement intense en quatre étapes.
- 2026-08-06 — Les consignes antérieures limitaient l'adaptateur aux bases H3 non élaguées ; le nœud personnalisé a ajouté la prise en charge des variantes élaguées et à courbe.

## Points encore inconnus {#still-unknown}

- L'adaptateur et son nœud sont des publications communautaires, et non un produit officiel MiniMax Turbo.
- Aucun benchmark indépendant établissant un classement universel de qualité ou de vitesse selon le GPU, la résolution, la durée et le type de mouvement n'a été trouvé.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora | larryvrh/MiniMax-H3-Turbo-Lora · Hugging Face | 2026-09-05 |
| https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo | Larryvrh/ComfyUI-MiniMax-H3-Turbo · GitHub | 2026-09-05 |
| https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo/commits/main/ | Commit history for Larryvrh/ComfyUI-MiniMax-H3-Turbo · GitHub | 2026-09-05 |

## Fiche pour l'agent {#agent-brief}

- **Sujet :** `project:minimax-h3-turbo-lora`, fil `minimax-h3-turbo-lora`, 1 événement daté du 2026-08-06 au 2026-08-06.
- **Note pratique :** À partir du 2026-08-06, évaluez MiniMax-H3 Turbo LoRA via le modèle lié et le chemin d'intégration ComfyUI plutôt que comme un checkpoint isolé ; vérifiez la compatibilité actuelle, les licences et les prérequis d'installation avant toute utilisation.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

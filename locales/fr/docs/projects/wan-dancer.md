---
title: "Wan-Dancer"
category: projects
date: 2026-07-14
tags: [project, wan-dancer, wan-dancer-development, wan_dancer]
aliases: ["Wan-Dancer"]
level: 3
source_sha256: 08cddcd0a6b79356af28a9fa68215576bec9cd8d032ebfddf159bd794de40251
translation: machine
translated_at: '2026-10-24'
---
# Wan-Dancer {#wan-dancer}

**Ligne de développement :** `project:wan-dancer` · fil `wan-dancer-development`  
**Dernier événement :** 2026-07-14 · 1 événement daté depuis le 2026-07-14 · **Recherche effectuée le :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

Wan-Dancer est un système de génération de vidéos de danse à partir de musique, basé sur un modèle de 14B paramètres, destiné aux créateurs qui ont besoin d'un long clip chorégraphié à partir d'un portrait, d'une piste musicale et d'un prompt de style, plutôt que d'assembler manuellement des clips courts.

- Planification globale des images clés à partir de la piste complète.
- Affinage local pour la continuité temporelle.
- Prompts de style pour la danse classique chinoise, la K-Pop, le street dance, le tap et les danses latines.

La sortie annoncée est en 720p et 30 fps pour plus d'une minute. Les auteurs ont testé leur code sur 8 GPU NVIDIA A800 80 Go. Nous utilisons le pipeline des auteurs pour des travaux contrôlés de longue durée, et non comme un flux de travail validé sur GPU unique ou en démonstration brute.

## Ligne de développement {#development-line}

- **2026-07-14 — Les ressources du projet Wan-Dancer ont été rendues publiques.** Le 2026-07-14, des liens publics sont apparus pour le site du projet Wan-Dancer, le dépôt source, la page de modèle Hugging Face et le studio ModelScope. Cela marque une étape de diffusion du projet. Ces liens n'établissent ni affirmations techniques, ni détails de version, ni formulation de l'annonce originale.

## Modifications {#what-changed}

Wan-Dancer — ligne de développement.

- 2026-05-09 — ComfyUI a fusionné le support de base de WanDancer avant la publication publique du modèle ; cela reflète l'historique d'implémentation et non la disponibilité publique des artefacts.
- 2026-07-10 — arXiv v1 a publié la méthode hiérarchique de génération de danse à partir de musique.
- 2026-07-13 — Wan-AI a annoncé la publication des poids de Wan-Dancer-14B et du code d'inférence.
- 2026-07-14 — Le dépôt officiel a publié un commit de mise à jour des liens, et une publication de la communauté ModelScope a documenté un parcours Studio portrait-et-musique.
- 2026-07-17 — arXiv a publié la v3 sans décrire de changements de comportement ou de poids dans ses métadonnées.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-14, consultez la page de projet liée pour le code source et les distributions officielles du modèle, puis vérifiez l'accès, la licence et les instructions avant de l'adopter.

1. Clonez Wan-Video/Wan-Dancer, créez l'environnement virtuel et installez l'ensemble de dépendances figé indiqué dans le README. La plateforme de référence est Ubuntu 22.04, Python 3.10.14 et CUDA 12.4.
  — <https://github.com/Wan-Video/Wan-Dancer>
2. Téléchargez Wan-AI/Wan-Dancer-14B avec huggingface-cli dans un répertoire de modèles local contrôlé.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
3. Préparez image_path, music_path et un prompt_path global ; les familles de prompts couvrent la danse classique chinoise, la K-Pop, le street dance, le tap et les danses latines.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
4. Exécutez gen_video_global.sh et enregistrez la vidéo globale générée avec sa graine et ses paramètres.
  — <https://github.com/Wan-Video/Wan-Dancer>
5. Transmettez ce résultat comme global_video_path à gen_video_local.sh avec le prompt local correspondant, afin que l'affinage local dispose de sa vidéo de base.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
6. Pour ComfyUI, mettez ComfyUI à jour, ouvrez son modèle Wan-Dancer et placez les modèles global/local, le LoRA, l'encodeur de texte, le modèle CLIP-Vision et le VAE dans les dossiers de modèle nommés. Ce modèle évolue en amont et n'a pas été vérifié localement ici.
  — <https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_dancer.json>

## Bonnes pratiques {#best-practices}

- Fixez la graine d'une comparaison à l'autre afin que les exécutions restent reproductibles.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
- Traitez la génération globale et locale comme un seul pipeline, et ne remplacez jamais le global_video_path requis par un clip sans rapport.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
- Augmentez le nombre d'étapes d'inférence pour les vidéos plus longues ; les auteurs suggèrent 48 étapes plutôt que de considérer l'exemple local à 24 étapes comme universel.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
- N'évaluez pas la qualité brute par rapport à la galerie du projet, car les vidéos affichées ont subi un post-traitement.
  — <https://humanaigc.github.io/wan-dancer-project/>
- Commencez avec la valeur par défaut de 5 secondes du modèle ComfyUI et surveillez la VRAM, car l'échantillonnage de 149 images d'un coup demande beaucoup de mémoire.
  — <https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_dancer.json>
- Ne considérez pas le système de test des auteurs (8 × A800 80 Go) comme un minimum pour GPU unique, car il sert d'environnement de référence et non de plancher matériel.
  — <https://github.com/Wan-Video/Wan-Dancer>

## Remplacé par ceci {#superseded-by-this}

- Considérer le 2026-07-14 comme la date de première publication publique des poids et du code d'inférence de Wan-Dancer ; la fiche officielle du modèle date cette publication du 2026-07-13.

## Points non établis {#still-unknown}

- La page directe du Studio ModelScope n'exposait pas de contrôles en direct ; ses champs actuels, ses valeurs par défaut, sa politique d'accès et ses limites ne sont donc pas vérifiés.
- Aucune source des auteurs n'a publié de VRAM minimale pour GPU unique, de durée d'exécution ou de reproduction de bout en bout ; la seule configuration rapportée est 8 × A800 80 Go.
- Les vidéos affichées ont subi un post-traitement et n'ont pas été reproduites de façon indépendante ; la durée et la qualité annoncées ne sont donc pas des garanties de production.
- La filiation des points de contrôle et la compatibilité entre Wan-Dancer-14B et les ressources wan2.2_dancer du modèle ComfyUI restent non vérifiées.
- Le statut du support ComfyUI reste incertain : la fiche officielle du modèle indique une intégration incomplète, alors que ComfyUI a fusionné un modèle fonctionnel.
- Les sources consultées ne montrent aucune mise à jour officielle des fonctionnalités ou des poids de Wan-Dancer après le 2026-07-17, bien que des versions non indexées puissent exister.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://humanaigc.github.io/wan-dancer-project/ | Page du projet Wan-Dancer | 2026-09-06 |
| https://github.com/Wan-Video/Wan-Dancer | Dépôt officiel Wan-Video/Wan-Dancer | 2026-09-06 |
| https://github.com/Wan-Video/Wan-Dancer/commits/main/ | Historique des commits Wan-Video/Wan-Dancer | 2026-09-06 |
| https://huggingface.co/Wan-AI/Wan-Dancer-14B | Fiche de modèle Wan-AI/Wan-Dancer-14B | 2026-09-06 |
| https://arxiv.org/abs/2607.09581 | Wan-Dancer : A Hierarchical Framework for Minute-scale Coherent Music-to-Dance Generation | 2026-09-06 |
| https://modelscope.csdn.net/6a55a9d210ee7a33f28d3bfc.html | ModelScope Community : annonce open-source de Wan-Dancer | 2026-09-06 |
| https://github.com/Comfy-Org/ComfyUI/pull/13813 | Pull request ComfyUI #13813 : Support Wan-Dancer | 2026-09-06 |
| https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_dancer.json | Modèle de workflow Wan-Dancer Comfy-Org sur main | 2026-09-06 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:wan-dancer`, fil `wan-dancer-development`, 1 événement daté du 2026-07-14 au 2026-07-14.
- **Note pratique :** Au 2026-07-14, les praticiens peuvent utiliser la page de projet liée pour trouver le code source de Wan-Dancer et les ressources officielles de distribution du modèle, puis vérifier l'accès actuel, la licence et les instructions d'utilisation avant de l'adopter.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

---
title: "ARDY — Disponibilité publique"
category: projects
date: 2026-07-15
tags: [ardy, project, public-availability]
aliases: ["ARDY"]
level: 2
source_sha256: a37db083f4cb6c1709fedc2d10adb712859fbab1fc038492f5d89aa2c11aae56
translation: machine
translated_at: '2026-10-24'
---
# ARDY — Disponibilité publique {#ardy-public-availability}

**Ligne de développement :** `project:ardy` · fil `public-availability`  
**Dernier événement :** 2026-07-15 · 1 daté depuis le 2026-07-15 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

ARDY est un système de diffusion autorégressive pour le mouvement humanoïde en temps réel sur les squelettes Core et Unitree G1.

- Invites textuelles en flux : guident le mouvement du personnage à la volée.
- Trajectoires racine et points de passage : orientent la trajectoire dans l'espace.
- Images clés du corps entier : fixent des poses à des images précises.
- Contraintes articulaires éparses : maintiennent des membres individuels pendant le mouvement.

Il est livré avec quatre points de contrôle de 326M paramètres et génère jusqu'à huit secondes de mouvement par sortie. Utilisez-le pour des prototypes et des travaux d'intégration sous Linux avec GPU NVIDIA, et non comme outil d'animation DCC prêt à l'emploi.

## Ligne de développement {#development-line}

- **2026-07-15 — Les ressources publiques du projet ARDY ont été reliées.** Le 2026-07-15, ARDY a été relié à sa page de projet NVIDIA Research, à son dépôt source, à sa collection Hugging Face et à son Space Hugging Face interactif. Ces liens relient le projet à ses points d'entrée de recherche, de code, de modèle et de prise en main. Les seules dates de liens n'établissent pas la formulation exacte de l'annonce, la version, les capacités ou le statut de publication.

## Ce qui a changé {#what-changed}

2026-07-15 — La page du projet ARDY, le code officiel, la collection de points de contrôle et la démo interactive sont devenus disponibles ; la publication couvre les squelettes Core et Unitree G1, plutôt qu'un modèle de personnage générique unique.

Le 2026-07-15, le dépôt officiel lié précise quatre points de contrôle publiés le 2026-07-10 : des modèles Core à 20 FPS avec des horizons de 8 ou 40 images et des modèles Unitree G1 à 25 FPS avec des horizons de 8 ou 52 images. La fiche modèle NVIDIA date le point de contrôle Core à 40 images du 2026-07-10, lui attribue 326M de paramètres et indique qu'il a été entraîné sur 630 heures de capture de mouvement Bones Rigplay 1.

2026-07-09 — l'article ARDY associé a été publié sur arXiv, décrivant la représentation hybride mouvement racine/latent corporel et le débruiteur transformeur en deux étapes. 2026-07-10 — NVIDIA a publié les quatre points de contrôle pré-entraînés sous le NVIDIA Open Model Agreement.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-15, évaluez ARDY via sa page de projet, son dépôt source, sa collection Hugging Face et son Space interactif, tout en vérifiant directement les workflows pris en charge et les versions.

1. Créez un environnement Python 3.10+ sous Linux, installez une version de PyTorch compatible avec CUDA, puis installez ARDY ; l'installation officielle a principalement été testée sur Ubuntu 22.04 avec une RTX 4090, le pilote 575 et Python 3.11.
  — <https://github.com/nv-tlabs/ardy>
2. Obtenez l'accès à Meta-Llama-3-8B-Instruct et authentifiez-vous auprès de Hugging Face, car l'encodeur de texte d'ARDY dépend de ce modèle à accès restreint.
  — <https://github.com/nv-tlabs/ardy>
3. Exécutez `python scripts/run_demo.py`, ouvrez `http://localhost:2333`, chargez un point de contrôle, puis contrôlez le mouvement par texte, points de passage, touches de vitesse ou contraintes cinématiques.
  — <https://github.com/nv-tlabs/ardy>
4. Choisissez un point de contrôle propre au squelette : Core pour le squelette de personnage à 27 articulations, ou G1 pour Unitree G1 ; utilisez les FPS et l'horizon indiqués plutôt que de considérer les variantes comme interchangeables.
  — <https://huggingface.co/nvidia/ARDY-Core-RP-20FPS-Horizon40>

## Bonnes pratiques {#best-practices}

- Installez PyTorch avant ARDY afin que la version CUDA corresponde au GPU et au pilote ; n'utilisez l'extra TensorRT que lorsque ses exigences de pilote et d'index de paquets sont satisfaites.
  — <https://github.com/nv-tlabs/ardy>
- Désactivez initialement le post-traitement : il peut réduire le glissement des pieds et améliorer le respect des contraintes, mais il est plus lent et désactivé par défaut.
  — <https://github.com/nv-tlabs/ardy>
- Réglez la longueur d'historique selon la tâche : un historique plus court s'adapte plus vite aux invites ou contraintes modifiées ; un historique plus long améliore la continuité sémantique et les transitions.
  — <https://github.com/nv-tlabs/ardy>
- Validez une intégration propre au cas d'usage avant déploiement ; la fiche modèle identifie Linux et les architectures NVIDIA Ampere, Hopper et Blackwell comme environnements pris en charge.
  — <https://huggingface.co/nvidia/ARDY-Core-RP-20FPS-Horizon40>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- L'espace Hugging Face hébergé n'a pas pu être consulté pendant la recherche ; sa disponibilité actuelle et son interface n'ont donc pas été vérifiées.
- Aucune note de version datée n'a été trouvée pour la publication du 2026-07-15 elle-même ; l'événement du 15 juillet est attesté par les pages officielles du projet, du dépôt et du modèle, tandis que les dates de publication des points de contrôle sont explicitement le 2026-07-10.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://research.nvidia.com/labs/sil/projects/ardy/ | ARDY: Interactive Human Motion Generation | 2026-09-05 |
| https://github.com/nv-tlabs/ardy | Official implementation of ARDY | 2026-09-05 |
| https://huggingface.co/collections/nvidia/ardy | ARDY — collection NVIDIA | 2026-09-05 |
| https://huggingface.co/nvidia/ARDY-Core-RP-20FPS-Horizon40 | Fiche modèle ARDY-Core-RP-20FPS-Horizon40 | 2026-09-05 |
| https://arxiv.org/abs/2607.08741 | ARDY: Autoregressive Diffusion with Hybrid Representation for Interactive Human Motion Generation | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:ardy`, fil `public-availability`, 1 événement daté du 2026-07-15 au 2026-07-15.
- **Note pratique :** Au 2026-07-15, les praticiens doivent utiliser ensemble la page de projet ARDY, le dépôt source, la collection Hugging Face et le Space interactif comme points de départ pour évaluer ou essayer le projet, tout en vérifiant de manière indépendante le workflow pris en charge et les versions exacts.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

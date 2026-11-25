---
title: "GenMM"
category: projects
date: 2023-06-02
tags: [genmm, genmm-development, project]
aliases: ["GenMM"]
level: 2
source_sha256: a13baecfc849b590a051ba38845647dc36fca6de36407b1f4e2bff34b4411bd4
translation: machine
translated_at: '2026-10-24'
---
# GenMM {#genmm}

**Ligne de développement :** `project:genmm` · fil `genmm-development`  
**Dernier événement :** 2023-06-02 · 1 événement daté depuis le 2023-06-02 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

GenMM — une base de code de recherche présentée à SIGGRAPH 2023, destinée aux animateurs techniques qui ont besoin de nouvelles séquences de mouvement squelettique à partir d'un ou de quelques clips d'exemple, et non d'un modèle texte-vers-mouvement.

- Synthétise des variantes diversifiées, complète des mouvements, suit des poses-clés, crée des boucles, réassemble des mouvements entre squelettes hétérogènes et modifie les trajectoires de locomotion.
- La pile locale documentée est Python 3.8, PyTorch 1.12.1 et CUDA 11.3 ; les auteurs indiquent environ 0,05 s par mouvement sur un Tesla V100 et 0,2 s sur un Apple M1.

## Ligne de développement {#development-line}

- **2023-06-02 — publication des supports publics de GenMM.** Le 2023-06-02, le projet a publié sa page de projet, son dépôt source et un lien vers la démo. Cette étape a ouvert des points d'entrée pour l'évaluation du projet, même si le texte source indisponible ne permet pas d'établir avec certitude la nature exacte de la publication ni les détails techniques.

## Ce qui a changé {#what-changed}

2023-06-02 — GenMM a été mis en ligne avec une page de projet, un dépôt source et une démo navigateur, en tant que système de synthèse de mouvement par l'exemple, sans entraînement. La page documente la complétion de mouvement, le guidage par poses-clés, la création de boucles, le réassemblage et la locomotion. 2023-07-13 — l'entrée ne fournit que le point d'accès existant de la démo navigateur. Elle n'identifie ni nouveau modèle, ni nouvelle version de paquet, ni nouvelle fonctionnalité ; il ne s'agit donc pas d'une version logicielle confirmée. 2026-09-04 — l'URL GitHub d'origine redirige vers liyuuuu98/GenMM ; la page des versions actuelle expose une seule pré-version de l'extension Blender, v0.0.1. La page de version consultée n'indique que « 29 Jul 12:48 », sans année ; aucune date de publication complète n'est donc attribuée.

## Comment l'utiliser {#how-to-use-this}

À partir du 2023-06-02, nous pouvions utiliser la page de projet publique de GenMM, le dépôt source et la démo comme points d'entrée pour l'évaluation ; le lien de démo du 2023-07-13 ne suffit pas, à lui seul, à établir un autre changement pratique.

1. Clonez le dépôt et reproduisez l'environnement documenté : Python 3.8, PyTorch 1.12.1, CUDA 11.3, docker/requirements.txt et torch-scatter==2.1.1.
  — <https://github.com/wyysf-98/GenMM>
2. Fournissez un clip de mouvement BVH et exécutez python run_random_generation.py -i <clip.bvh> ; utilisez run_random_generation.py pour configurer la synthèse plus en détail.
  — <https://github.com/wyysf-98/GenMM>
3. Pour Blender, installez les paquets Python listés dans le Python fourni avec Blender, installez le ZIP de l'extension via Préférences > Extensions > Installer, puis sélectionnez un armature et ouvrez le panneau GenMM.
  — <https://github.com/wyysf-98/GenMM>
4. Pour la démo web, sélectionnez un exemple avec Next, utilisez Generate et Controls, puis réglez frames, noise_sigma, loop, patch_size, coarse_ratio, pyr_factor et le nombre d'étapes d'optimisation.
  — <https://github.com/wyysf-98/GenMM_demo>
5. Si la démo partagée reste en attente indéfiniment, dupliquez son Space Hugging Face, obtenez votre propre URL d'API et remplacez api_url dans Controls.
  — <https://github.com/wyysf-98/GenMM_demo>

## Bonnes pratiques {#best-practices}

- Épinglez ou conteneurisez les versions documentées de Python, PyTorch et CUDA avant de modifier les dépendances. Les instructions officielles ne fournissent pas de matrice de compatibilité plus récente.
  — <https://github.com/wyysf-98/GenMM>
- Validez le mouvement final dans un flux de travail tenant compte du rig, et pas seulement dans le visualiseur du navigateur. La page du projet signale que son analyseur FBX Three.js ne dispose d'aucune correction du contact des pieds et peut produire des artefacts.
  — <https://weiyuli.xyz/GenMM/>
- Lorsque la démo partagée est lente, utilisez un Space dupliqué avec votre propre URL d'API plutôt que de relancer sans cesse le point d'accès partagé fonctionnant sur CPU.
  — <https://github.com/wyysf-98/GenMM_demo>

## Remplacé par ceci {#superseded-by-this}

- 2023-06-02 — la liste de contrôle de publication du README n'est plus valable comme déclaration de disponibilité : le dépôt contient désormais l'exécuteur local, et GitHub répertorie la pré-version v0.0.1 de l'extension Blender.
- 2023-07-13 — un flux de travail reposant uniquement sur la démo navigateur est obsolète pour un travail répété : la documentation officielle propose désormais une voie de récupération par Space copié avec API privée, et signale les artefacts du visualiseur et les blocages du CPU partagé.

## Points encore inconnus {#still-unknown}

- Aucune source officielle consultée aujourd'hui ne fournit de matrice de compatibilité Python, PyTorch, CUDA ou Blender testée en 2026.
- L'entrée du 2023-07-13 ne donne que l'URL existante de la démo. Sans son texte source, nous ne pouvons attribuer à cette date aucune capacité ou version distincte.
- La page des versions actuelle affiche v0.0.1 comme pré-version et indique « 29 Jul 12:48 », mais la vue consultée n'expose pas l'année.
- La démo navigateur nécessite JavaScript ; la génération de bout en bout en direct n'a pas été vérifiée dans cette recherche.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://weiyuli.xyz/GenMM/ | Example-based Motion Synthesis via Generative Motion Matching | 2026-09-04 |
| https://github.com/wyysf-98/GenMM | GitHub — liyuuuu98/GenMM | 2026-09-04 |
| https://weiyuli.xyz/GenMM_demo/ | synthèse de mouvement par patchs | 2026-09-04 |
| https://github.com/wyysf-98/GenMM_demo | GitHub — liyuuuu98/GenMM_demo | 2026-09-04 |
| https://github.com/wyysf-98/GenMM/releases | GitHub — GenMM releases | 2026-09-04 |

## Brief d'agent {#agent-brief}

- **Sujet :** `project:genmm`, fil `genmm-development`, 1 événement daté, du 2023-06-02 au 2023-06-02.
- **Note pratique :** À partir du 2023-06-02, les praticiens pouvaient utiliser la page de projet publique de GenMM, le dépôt source et la démo comme points d'entrée pour l'évaluation ; le lien de démo du 2023-07-13 ne suffit pas, à lui seul, à établir un autre changement pratique.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

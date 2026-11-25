---
title: "Align3R"
category: projects
date: 2024-12-18
tags: [align3r, project]
aliases: ["Align3R"]
level: 3
source_sha256: c7268ca9e1707e7202875a9c89bc1494829f67928d928cca77441aa0693e87e5
translation: machine
translated_at: '2026-10-24'
---
# Align3R {#align3r}

**Ligne de développement :** `project:align3r` · fil `align3r`  
**Dernier événement :** 2024-12-18 · 2 événements datés depuis 2024-12-06 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Align3R est un code de recherche destiné à reconstruire une vidéo dynamique à partir d'une seule caméra.

- aligne la profondeur monoculaire image par image avec un modèle DUSt3R affiné
- produit des cartes de profondeur temporellement cohérentes, des nuages de points dynamiques et les poses de caméra
- prend en charge les chemins de points de contrôle Depth Pro et Depth Anything V2

## Ligne de développement {#development-line}

- **2024-12-06 — Les ressources publiques du projet Align3R ont été liées.** Le 2024-12-06, Align3R a publié une page de projet officielle, un dépôt de code source public et une page de projet complémentaire. Ces liens établissent des ressources de code publiques sans détailler le contenu de la publication.
- **2024-12-18 — Align3R a été relié à un Hugging Face Space hébergé.** Le 2024-12-18, une entrée de suivi relative à Align3R renvoyait vers la page de projet précédente et vers un Hugging Face Space d'Align3R. Ce lien indique un point d'accès hébergé, mais la source ne décrit aucune modification de la démonstration.

## Changements {#what-changed}

2024-12-06 — Align3R est apparu comme une méthode publiée sur arXiv, accompagnée d'une page de projet, du code source et de nuages de points reconstruits. Elle combine des a priori de profondeur monoculaire avec l'alignement et l'optimisation DUSt3R pour la vidéo dynamique. 2024-12-18 — un Space Align3R interactif est devenu disponible en parallèle du code local ; il fonctionne à la date du jour. Constaté aujourd'hui (2026-09-04) — le README principal indique la version 1.0.2 et le statut CVPR 2025 Highlight. L'affinement avec PromptDA est terminé ; l'évaluation sur scènes statiques, davantage de données d'entraînement réelles, ainsi que la prédiction de pose de caméra et de correspondances de points restent en suspens.

## Mode d'emploi {#how-to-use-this}

Au 2024-12-06, les praticiens pouvaient trouver les documents du projet Align3R et le code source ; au 2024-12-18, ils peuvent aussi consulter le Hugging Face Space pour un accès hébergé.

1. Clonez le dépôt officiel, créez l'environnement Conda Python 3.11 documenté, installez une version de PyTorch/CUDA compatible, puis installez les dépendances.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
2. Compilez l'extension CUDA RoPE de CroCo dans croco/models/curope avant d'exécuter l'inférence.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
3. Choisissez Depth Pro ou Depth Anything V2, installez la pile de profondeur correspondante, puis récupérez le point de contrôle Align3R correspondant et le poids de base DUSt3R.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
4. Renseignez les espaces réservés d'entrée, de sortie et de séquence dans demo.sh, puis exécutez-le sur le GPU choisi ; le lanceur fourni utilise un intervalle de 50.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/demo.sh>
5. Utilisez un fichier MP4 ou un répertoire d'images JPG/PNG ; la démonstration génère la profondeur monoculaire, reconstruit la scène et écrit les poses, les paramètres intrinsèques, les cartes de profondeur, les masques, les cartes de confiance et les sorties RGB.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/tool/demo.py>
6. Pour un affinement à la résolution d'origine, installez PromptDA séparément et exécutez demo_refine.sh ; utilisez la commande viser fournie pour inspecter les nuages de points.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>

## Bonnes pratiques {#best-practices}

- Épinglez un commit du dépôt et consignez l'ensemble exact des points de contrôle pour la reproductibilité : aucun artefact de publication GitHub n'est publié.
  — <https://github.com/jiah-cloud/Align3R/releases>
- Compilez l'extension CUDA RoPE personnalisée après l'installation des dépendances ; un environnement pip simple n'est pas l'environnement d'exécution documenté.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
- Gardez cohérents l'a priori de profondeur choisi, son point de contrôle Align3R et le paramètre d'évaluation depth_prior_name.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
- Établissez une référence avec demo.sh avant d'ajouter l'affinement PromptDA, qui dispose d'une procédure d'installation distincte.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
- Avant de signaler des résultats sur Sintel, vérifiez la séparation clean/final dans la copie de travail ; un ticket ouvert signale cette incohérence.
  — <https://github.com/jiah-cloud/Align3R/issues/27>
- Examinez les conditions CC BY-NC-SA 4.0 du dépôt avant de le retenir pour un usage commercial.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>

## Remplacé par {#superseded-by-this}

- 2024-12-06 : « préprint arXiv uniquement » n'est plus une description valable du statut ; le dépôt qualifie Align3R de CVPR 2025 Highlight et fournit du code v1.0.2 exécutable.
- 2024-12-18 : Aucun remplacement ni aucune dépréciation vérifiés du Space interactif ; il demeure une voie de démonstration secondaire plutôt que le flux de travail local reproductible.

## Points non résolus {#still-unknown}

- Aucun reçu actuel concernant le GPU, le pilote, le téléchargement des modèles ou une reconstruction de bout en bout n'a été obtenu ; la compatibilité à l'exécution et la qualité sur une vidéo cible restent non vérifiées.
- Le libellé 1.0.2 du README n'identifie pas un paquet ou un ensemble de points de contrôle immuable, car le dépôt ne possède aucun artefact de publication GitHub.
- La reproduction du benchmark MPI-Sintel présente une ambiguïté non résolue sur la séparation clean/final, signalée dans un ticket ouvert.
- Le README officiel renvoie vers le même Hugging Face Space ; les deux entrées datées ne semblent donc pas porter sur des sujets distincts. Il n'est pas indiqué si le code du Space déployé correspond exactement à la branche main.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/abs/2412.03079 | Align3R: Aligned Monocular Depth Estimation for Dynamic Videos — arXiv | 2026-09-04 |
| https://igl-hkust.github.io/Align3R.github.io/ | Align3R — page de projet officielle | 2026-09-04 |
| https://igl-hkust.github.io/Align3R.github.io/page1.html | Align3R — nuages de points reconstruits | 2026-09-04 |
| https://github.com/jiah-cloud/Align3R | jiah-cloud/Align3R — dépôt officiel | 2026-09-04 |
| https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md | README d'Align3R — branche main | 2026-09-04 |
| https://raw.githubusercontent.com/jiah-cloud/Align3R/main/demo.sh | Lanceur de démonstration d'Align3R — branche main | 2026-09-04 |
| https://raw.githubusercontent.com/jiah-cloud/Align3R/main/tool/demo.py | Implémentation de la démonstration d'Align3R — branche main | 2026-09-04 |
| https://huggingface.co/spaces/cyun9286/Align3R | Align3R — Hugging Face Space | 2026-09-04 |
| https://github.com/jiah-cloud/Align3R/releases | Versions d'Align3R | 2026-09-04 |
| https://github.com/jiah-cloud/Align3R/issues/27 | Ticket n° 27 d'Align3R — confusion sur la séparation du jeu de données Sintel | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:align3r`, fil `align3r`, 2 événements datés du 2024-12-06 au 2024-12-18.
- **Remarque pratique :** Au 2024-12-06, les praticiens pouvaient trouver les documents du projet Align3R et son code source ; au 2024-12-18, ils doivent aussi consulter le Hugging Face Space lié pour un accès hébergé au projet.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

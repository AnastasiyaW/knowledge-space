---
title: "NeumaTex"
category: projects
date: 2026-07-02
tags: [neumatex, neumatex-development, project]
aliases: ["NeumaTex"]
level: 2
source_sha256: ead82f3d0463ae85af49c9cac6975261efa895183df43f189241f8df2e1fd3ca
translation: machine
translated_at: '2026-10-24'
---
# NeumaTex {#neumatex}

**Ligne de développement :** `project:neumatex` · fil `neumatex-development`  
**Dernier événement :** 2026-07-02 · 1 événement daté depuis le 2026-07-02 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

NeuMatEx est un pipeline de recherche destiné aux équipes de graphisme et de création d'actifs 3D. Il transforme un modèle 3D connu et des images multi-vues en un matériau neuronal rééclairable, plutôt qu'en cartes de textures PBR.

- prédit la couleur de base, les latents du matériau neuronal et l'incertitude avec le Large Material Reconstruction Model (LMRM)
- affine le résultat par rendu inverse par traçage de chemins guidé par l'incertitude
- modélise le vernis (clearcoat), le voile (haze), la poussière, le duvet (fuzz) et la diffusion au-delà des lobes PBR fixes

## Ligne de développement {#development-line}

- **2026-07-02 — Page projet NeumaTex partagée.** Initialisation par LMRM suivie d'un rendu inverse guidé par l'incertitude, visant des matériaux rééclairables dont les effets spéculaires seraient autrement intégrés à la couleur de base PBR.

## Changements {#what-changed}

2026-07-02 — NeuMatEx a été présenté comme une méthode d'extraction de matériaux neuronaux à partir de vues multiples : initialisation par LMRM suivie d'un rendu inverse guidé par l'incertitude, visant des matériaux rééclairables dont les effets spéculaires seraient autrement intégrés à la couleur de base PBR.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-02, les praticiens doivent consulter la page projet NeumaTex avant de s'appuyer sur le projet ou de l'adopter ; le simple lien fourni n'établit pas de capacités spécifiques ni de consignes d'utilisation.

1. Évaluer d'abord l'adéquation : la méthode documentée nécessite un modèle 3D fourni et un ensemble d'images multi-vues, et non une image unique quelconque.
  — <https://nvlabs.github.io/neumatex/>
2. Pour une réimplémentation de recherche, reproduire les deux étapes : prédire la couleur de base, les latents neuronaux et l'incertitude avec LMRM, puis affiner avec un rendu inverse Monte-Carlo guidé par l'incertitude.
  — <https://arxiv.org/abs/2606.26715>
3. Ne pas prévoir encore d'installation ou d'exécution d'inférence classique : la page projet officielle ne renvoie actuellement vers l'article, le PDF complémentaire, la vidéo et le BibTeX, mais ni dépôt source ni téléchargement de modèle.
  — <https://nvlabs.github.io/neumatex/>

## Bonnes pratiques {#best-practices}

- Utiliser des observations multi-vues calibrées et, si possible, une géométrie, des poses et un éclairage connus ; l'article note que la récupération par rendu inverse est sensible aux données ambiguës ou mal calibrées.
  — <https://arxiv.org/abs/2606.26715>
- Conserver l'étape d'optimisation au moment du test guidée par l'incertitude ; l'ablation rapportée montre qu'elle améliore la décomposition du matériau par rapport à la seule initialisation en propagation directe (feed-forward) et réduit l'éclairage intégré.
  — <https://arxiv.org/abs/2606.26715>
- Vérifier les résultats de rééclairage et inspecter les matériaux réels hors domaine pour détecter les artefacts spéculaires résiduels, en particulier les teintes rougeâtres et les artefacts dans les creux.
  — <https://arxiv.org/abs/2606.26715>

## Remplacé par cette entrée {#superseded-by-this}

- Rien d'marqué comme obsolète pour l'instant.

## Inconnues restantes {#still-unknown}

- Aucun dépôt source public, point de contrôle (checkpoint), licence, exigence matérielle ni procédure d'exécution reproductible n'a été trouvé sur la page projet officielle consultée le 2026-09-05.
- Le rapport du 2026-07-02 indiquait que le code source n'était pas encore publié ; sa disponibilité en dehors des sources consultées ici n'est pas vérifiée.
- L'orthographe d'affichage fournie est « NeumaTex » ; la page projet officielle et le titre arXiv utilisent « NeuMatEx ».
- event_findings: [{"event_date":"2026-07-02","finding":"Le nom officiel de l'ouvrage référencé est NeuMatEx, abréviation de l'article Extracting Neural Materials from Multi-view Images ; il s'agit de arXiv:2606.26715, par Kim Youwang, Jon Hasselgren, Peter Kocsis, Andrea Weidlich, Tae-Hyun Oh et Jacob Munkberg. La méthode nécessite un modèle 3D et des images multi-vues, et non un générateur de textures à partir d'une seule image.","source_date":"2026-06-25","source_url":"https://arxiv.org/abs/2606.26715"},{"event_date":"2026-07-02","finding":"Un rapport contemporain précise la limite pratique de diffusion : le code source n'avait pas été publié, de sorte que l'annonce ne mettait pas à disposition de paquet public exécutable.","source_date":"2026-07-02","source_url":"https://nnets.ru/news/nvidia-predstavila-neumatex-novyj-metod-3d-tekstur-po-foto"}]
- new_events: [{"date":"2026-06-25","finding":"La prépublication arXiv v1 a été publiée, établissant la méthode de recherche avant sa couverture du 2 juillet : initialisation par LMRM plus rendu inverse guidé par l'incertitude pour les matériaux neuronaux.","source_date":"2026-06-25","source_url":"https://arxiv.org/abs/2606.26715"}]

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://nvlabs.github.io/neumatex/ | Extracting Neural Materials from Multi-view Images | 2026-09-05 |
| https://arxiv.org/abs/2606.26715 | Extracting Neural Materials from Multi-view Images | 2026-09-05 |
| https://nnets.ru/news/nvidia-predstavila-neumatex-novyj-metod-3d-tekstur-po-foto | NVIDIA представила NeumaTex: новый метод 3D-текстур по фото. | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:neumatex`, fil `neumatex-development`, 1 événement daté du 2026-07-02 au 2026-07-02.
- **Note pratique :** Au 2026-07-02, les praticiens doivent consulter la page projet NeumaTex avant de s'appuyer sur le projet ou de l'adopter ; le simple lien fourni n'établit pas de capacités spécifiques ni de consignes d'utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

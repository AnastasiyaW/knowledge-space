---
title: "FLOAT"
category: projects
date: 2025-07-21
tags: [float, float-public-releases, model_releases, project]
aliases: ["FLOAT"]
level: 3
source_sha256: ee43d90ef7842cc0e4a6c6f515bf382d58f3c6d058c5ba89b85f49163d4a9fcb
translation: machine
translated_at: '2026-10-24'
---
# FLOAT {#float}

**Ligne de développement :** `project:float` · fil `float-public-releases`  
**Dernier événement :** 2025-07-21 · 2 entrées datées depuis 2024-12-05 · **Recherche effectuée le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

FLOAT est une implémentation de recherche en PyTorch qui anime un portrait unique, principalement de face, à partir d'un signal audio de parole.

- Génération du mouvement dans un espace latent de mouvement appris, avec flow matching.
- Animation des mouvements des lèvres, de la tête et de l'expressivité à partir de l'audio.
- Redirection des émotions et édition du mouvement de tête au moment de l'inférence.

Le paquet publié ne fait que de l'inférence, est destiné à la recherche et à un usage non commercial, et a été testé sous Linux avec des GPU A100 et V100.

Utilisez-le pour des démonstrations de recherche reproductibles, et non comme une pile de talking-head déployable commercialement.

## Ligne de développement {#development-line}

- **2024-12-05 — La page projet de FLOAT a été rendue publique.** FLOAT est apparu comme une méthode de génération de portrait parlant piloté par l'audio, basée sur le flow matching, avec un espace latent de mouvement orthogonal et une émotion pilotée par la parole.
- **2025-07-21 — Le dépôt de FLOAT et des liens vers des ressources complémentaires sont apparus.** Le dépôt officiel et le chemin de téléchargement manuel des checkpoints pointaient vers ce chemin d'inférence exécutable ; nous n'avons identifié aucune nouvelle version nommée du modèle.

## Ce qui a changé {#what-changed}

FLOAT est passé d'une méthode publiée à un paquet d'inférence exécutable, puis à un article ICCV révisé, plutôt qu'à une version produit numérotée.

- 2024-12-05 : FLOAT a été présenté comme une méthode de génération de portrait parlant piloté par l'audio, basée sur le flow matching, avec un espace latent de mouvement orthogonal et une émotion pilotée par la parole.
- 2025-02-17 : le dépôt officiel a publié le code d'inférence et les checkpoints sous une licence non commerciale, rendant la méthode exécutable.
- 2025-06-26 : le projet a annoncé l'acceptation à ICCV 2025.
- 2025-07-21 : le dépôt officiel et le chemin de téléchargement manuel des checkpoints pointaient vers ce chemin d'inférence exécutable ; nous ne relevons aucune nouvelle version nommée du modèle.
- 2025-09-19 : l'arXiv v5 a révisé l'article ; il n'annonce pas de nouvelle publication d'inférence.
- 2025-11-10 : l'historique de la branche principale montre un commit de mise à jour, mais son effet fonctionnel n'est pas documenté et GitHub ne répertorie aucune release.

Il n'existe ni série de versions de modèle étiquetées, ni code d'entraînement publié.

Considérez le dépôt et ses checkpoints comme un dépôt de code de recherche ponctuel, et non comme un canal de release maintenu.

## Comment l'utiliser {#how-to-use-this}

Au 2025-07-21, consultez le dépôt officiel de FLOAT, la ressource complémentaire liée et la page projet pour évaluer ou reproduire FLOAT ; vérifiez séparément le contenu exact des artefacts et les conditions d'utilisation.

1. Clonez le dépôt officiel, créez son environnement Conda avec Python 3.8.5, puis installez le build PyTorch CUDA 11.8 documenté ainsi que les dépendances.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
2. Téléchargez les checkpoints avec `sh download_checkpoints.sh` et placez les fichiers principaux de FLOAT, Wav2Vec2 et du modèle d'émotion vocale dans l'arborescence de checkpoints documentée.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
3. Préparez un portrait mono-visage, principalement de face, et une piste de parole ; commencez avec le recadrage automatique du visage activé.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
4. Exécutez `generate.py` sur un périphérique CUDA avec `--ref_path`, `--aud_path`, `--seed 15`, `--a_cfg_scale 2`, `--e_cfg_scale 1` et `--ckpt_path ./checkpoints/float.pth`.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
5. Pour une expression explicite, ajoutez `--emo` avec l'une des valeurs angry, disgust, fear, happy, neutral, sad ou surprise ; ajustez `--e_cfg_scale` seulement après une exécution par défaut.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>

## Bonnes pratiques {#best-practices}

- Commencez par un portrait de face. Le modèle a été entraîné sur des distributions de pose de tête frontales, et les entrées non frontales peuvent réduire la qualité.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Gardez le recadrage automatique activé, sauf si une comparaison mesurée justifie `--no_crop` ; le désactiver peut réduire les performances, tandis que le recadrage par défaut peut ajouter des bordures noires.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Extrayez les voix avant l'inférence lorsque l'audio contient beaucoup de musique de fond ; les auteurs recommandent ClearVoice pour cette préparation.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Commencez le guidage émotionnel avec la valeur par défaut de 1 ; les auteurs suggèrent 5 à 10 uniquement lorsqu'une expression plus marquée est nécessaire.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Limitez l'usage à la recherche et ne prévoyez pas de fine-tuning à partir de la version officielle : sa licence est non commerciale et les auteurs indiquent que le code d'entraînement ne sera pas publié.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>

## Remplacé par ce document {#superseded-by-this}

- Avant le 2025-02-17 : indications selon lesquelles FLOAT n'était qu'une méthode décrite dans un article ou une page projet, nécessitant d'attendre le code d'inférence officiel et les poids. Remplacé par la publication officielle du code d'inférence et des checkpoints.
- 2024-12-05 : une description limitée à la méthode ne constitue plus une configuration suffisante. Remplacée par les instructions officielles du README concernant l'environnement, les checkpoints, le prétraitement et la CLI ; le lien vers les checkpoints du 2025-07-21 mène à ce paquet exécutable et ne constitue pas la preuve d'un modèle nouvellement versionné.

## Toujours inconnu {#still-unknown}

- Le lien fourni vers les checkpoints sur Google Drive n'a pas pu être lu de façon indépendante ; son contenu, sa somme de contrôle et la question de savoir s'il a changé après le 2025-07-21 restent non vérifiés.
- Aucune documentation de FLOAT en chinois simplifié émanant des auteurs n'existe ; les résultats en chinois de tiers n'ont pas été utilisés comme preuves.
- Le commit le plus récent visible, daté du 2025-11-10, est seulement étiqueté « update » ; aucun changelog émanant des auteurs n'explique son effet fonctionnel.
- Le matériel officiel n'indique pas la durée d'entrée prise en charge, la résolution de sortie, la consommation de VRAM ni la compatibilité au-delà de la configuration testée Linux A100/V100.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://deepbrainai-research.github.io/float/ | Page projet FLOAT | 2026-09-04 |
| https://github.com/deepbrainai-research/float | Dépôt GitHub officiel de FLOAT | 2026-09-04 |
| https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md | README de FLOAT sur la branche principale | 2026-09-04 |
| https://arxiv.org/abs/2412.01064 | FLOAT: Generative Motion Latent Flow Matching for Audio-driven Talking Portrait | 2026-09-04 |
| https://github.com/deepbrainai-research/float/commits/main/ | Historique des commits de la branche principale de FLOAT | 2026-09-04 |
| https://github.com/deepbrainai-research/float/releases | Releases GitHub de FLOAT | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:float`, fil `float-public-releases`, 2 événements datés du 2024-12-05 au 2025-07-21.
- **Note pratique :** Au 2025-07-21, les praticiens doivent consulter le dépôt officiel de FLOAT et la ressource complémentaire liée, en plus de la page projet, lorsqu'ils évaluent ou reproduisent FLOAT ; vérifiez séparément le contenu exact des artefacts et les conditions d'utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

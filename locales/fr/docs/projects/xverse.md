---
title: "XVerse — Ressources publiques et démo"
category: projects
date: 2025-11-12
tags: [project, public-resources-and-demo, xverse]
aliases: ["XVerse"]
level: 2
source_sha256: 25a6e07a1c4e062cc5ea0f1089979a1cc165f0c32957dc1a63182aa7585660a9
translation: machine
translated_at: '2026-10-24'
---
# XVerse — Ressources publiques et démo {#xverse-public-resources-and-demo}

**Ligne de développement :** `project:xverse` · fil `public-resources-and-demo`  
**Dernier événement :** 2025-11-12 · 2 événements datés depuis 2025-06-30 · **Recherche :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

XVerse est une implémentation ouverte basée sur FLUX.1-dev, destinée aux artistes et aux développeurs qui ont besoin d'une génération text-to-image contrôlable avec une ou plusieurs références. Fonctionnalités : séparation de l'identité des sujets ; contrôle de la pose, du style et de l'éclairage ; Gradio local et CLI ; XVerseBench. Limite : le mode de base nécessite 24 Go de VRAM pour deux conditions, tandis que le mode avec CPU offload en nécessite 16 Go pour trois, au prix d'une perte de vitesse notable. Verdict : applicable en local pour la personnalisation multi-sujets, mais la démo web publiée affiche actuellement une runtime error.

## Ligne de développement {#development-line}

- **2025-06-30 — Les ressources publiques de XVerse ont été reliées.** L'article a été publié le 2025-06-26 et le code a été publié le 2025-06-26 ; le modèle applique une modulation de flux de texte spécifique aux tokens dans le DiT. Complément à l'événement : l'article cite le preprint exact arXiv:2506.21416 et les auteurs de ByteDance ; XVerseBench comprend 20 identités humaines, 74 objets, 45 animaux et 300 prompts de test (page du projet, sans date de publication propre).
- **2025-11-12 — Le Hugging Face Space de XVerse a été mis en avant.** Le dépôt date la publication de la démo au 2025-07-10. Lors de la vérification du 2026-09-05, le Space renvoie une runtime error ; il ne peut donc pas être considéré comme un chemin d'accès fonctionnel.

## Ce qui a changé {#what-changed}

2025-06-30 — lancement public de XVerse : l'article a été publié le 2025-06-26 et le code a été publié le 2025-06-26 ; le modèle applique une modulation de flux de texte spécifique aux tokens dans le DiT. Complément à l'événement : l'article cite le preprint exact arXiv:2506.21416 et les auteurs de ByteDance ; XVerseBench comprend 20 identités humaines, 74 objets, 45 animaux et 300 prompts de test (page du projet, sans date de publication propre). 2025-11-12 — le lien menait au Hugging Face Space officiel, mais cela ne signale pas une nouvelle version du modèle : le dépôt date la publication de la démo au 2025-07-10. Lors de la vérification du 2026-09-05, le Space renvoie une runtime error ; il ne peut donc pas être considéré comme un chemin d'accès fonctionnel.

Nouveaux événements indépendants : 2025-07-08 — ajout de l'inférence low-VRAM, annoncée pour 24 Go de VRAM ; 2025-07-10 — publication du Hugging Face Space ; 2025-07-18 — ajout de modèles de diffusion quantifiés et de group offload, avec un lancement annoncé à partir de 16 Go de VRAM ; 2025-09-19 — travail accepté à NeurIPS 2025. Ces quatre dates figurent dans le journal des modifications du dépôt officiel.

## Comment l'utiliser {#how-to-use-this}

À partir du 2025-06-30, les praticiens pouvaient trouver ensemble le projet officiel, les ressources de code et de modèle de XVerse ; à partir du 2025-11-12, ils doivent aussi vérifier le Hugging Face Space officiel, point d'entrée interactif public, tout en considérant la date de lancement ou de modification du Space comme non vérifiée.

1. Cloner le dépôt, créer un environnement Python 3.10.16, installer PyTorch 2.6.0/CUDA 12.4 figés, les requirements, FlashAttention et httpx, puis télécharger les checkpoints et ajouter séparément model_ir_se50.pth.
  — <https://github.com/bytedance/XVerse>
2. Définir les chemins vers Florence-2, SAM2, InsightFace, CLIP, FLUX.1-dev, DPG-VQA et DINO ; lancer l'interface locale avec la commande python run_gradio.py.
  — <https://github.com/bytedance/XVerse>
3. Pour un lancement reproductible, transmettre prompt, images, légendes et indicateurs idips à inference_single_sample.py ; pour plusieurs références, les nombres d'images, de captions et d'idips doivent correspondre.
  — <https://github.com/bytedance/XVerse>
4. En cas de manque de mémoire, activer use_low_vram ou use_lower_vram ; pour les FLUX quantifiés, utiliser la voie bnb-nf4 ou GGUF documentée et recalibrer les poids.
  — <https://github.com/bytedance/XVerse>

## Bonnes pratiques {#best-practices}

- Incluez dans le prompt principal une description précise de chaque référence active, ou utilisez ENT1/ENT2 : sans cela, la génération échoue.
  — <https://github.com/bytedance/XVerse>
- N'activez pas le CPU offload sans nécessité : la documentation avertit explicitement d'une baisse de vitesse importante.
  — <https://github.com/bytedance/XVerse>
- Après être passé à un FLUX quantifié, recalibrez weight_id, weight_ip et les scales LoRA : la quantification peut dégrader le résultat.
  — <https://github.com/bytedance/XVerse>
- Pour évaluer des modifications, lancez le script XVerseBench fourni ; il enregistre les résultats dans results.
  — <https://github.com/bytedance/XVerse>

## Remplacé par ceci {#superseded-by-this}

- 2025-07-08 : l'exigence précédente du mode complet, plus gourmand en mémoire, est en partie remplacée par le mode low-VRAM à 24 Go, pour jusqu'à deux conditions.
- 2025-07-18 : les recommandations low-VRAM du 2025-07-08 sont étendues à la quantification et au group offload ; le minimum annoncé passe à 16 Go de VRAM pour jusqu'à trois conditions.
- 2026-09-05 : la recommandation d'utiliser le Space officiel comme chemin de travail est obsolète jusqu'au rétablissement du service, la page affichant une runtime error ; le lancement local reste le chemin documenté.

## Toujours inconnu {#still-unknown}

- Le README officiel indique que l'implémentation ComfyUI et le Benchmark Leaderboard ne sont pas encore publiés ; il est impossible de confirmer l'existence d'un chemin ComfyUI pris en charge.
- Le Hugging Face Space, dans l'événement fourni du 2025-11-12, ne contient pas de changelog daté propre ; il est donc impossible d'établir de façon fiable ce qui a changé ce jour-là, au-delà de la présence du lien vers la démo.
- Le nom XVerse est aussi utilisé par l'organisation sans lien xverse pour des modèles de langage ; dans cette histoire, il ne s'agit que de ByteDance XVerse pour la génération d'images.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://bytedance.github.io/XVerse/ | XVerse: Consistent Multi-Subject Control of Identity and Semantic Attributes via DiT Modulation | 2026-09-05 |
| https://github.com/bytedance/XVerse | ByteDance/XVerse official implementation | 2026-09-05 |
| https://huggingface.co/ByteDance/XVerse/tree/main | ByteDance/XVerse model repository | 2026-09-05 |
| https://huggingface.co/spaces/ByteDance/XVerse | ByteDance XVerse Hugging Face Space | 2026-09-05 |
| https://arxiv.org/abs/2506.21416 | XVerse: Consistent Multi-Subject Control of Identity and Semantic Attributes via DiT Modulation | 2026-09-05 |
| https://raw.githubusercontent.com/bytedance/XVerse/main/README.md | XVerse README | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:xverse`, fil `public-resources-and-demo`, 2 événements datés du 2025-06-30 au 2025-11-12.
- **Note pratique :** à partir du 2025-06-30, les praticiens pouvaient trouver ensemble le projet officiel, les ressources de code et de modèle de XVerse ; à partir du 2025-11-12, ils doivent aussi vérifier le Hugging Face Space officiel, point d'entrée interactif public, tout en considérant la date de lancement ou de modification du Space comme non vérifiée.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

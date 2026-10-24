---
title: "FreeToken"
category: projects

tags: [freetoken, freetoken-development, project]
aliases: ["FreeToken"]
level: 2
source_sha256: 242ce2cdc9b5d5683400ed42e84d5e77d319a1dc9bf93e7640c3e2c0f597e6e1
translation: machine
translated_at: '2026-10-24'
---
# FreeToken {#freetoken}

**Ligne de développement :** `project:freetoken` · fil `freetoken-development`  
**Dernier événement :** - · 0 daté depuis - · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

FreeToken est un serveur d'inférence open source permettant d'exécuter de grands modèles Mixture-of-Experts sur des PC grand public, en alternative à vLLM et SGLang.

- Compatibilité client avec les API OpenAI, Anthropic et Responses.
- Déchargement CPU-GPU, cache d'experts et format de poids FTW pour faire tenir les modèles en mémoire.
- Connexions CLI, application de bureau et agents de codage pour les workflows locaux.

La configuration officielle requiert x86_64, NVIDIA Ampere/RTX 30 ou plus récent, un pilote r580+ et suffisamment de RAM système libre pour les experts. Le projet évolue rapidement : testez votre GPU et votre modèle spécifiques avant de vous y fier.

## Ligne de développement {#development-line}

- L'événement daté n'est pas encore rédigé ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

- 2026-08-19 : la version GitHub v0.1.2 a été publiée sous le tag `9db1a39` avec sept fichiers joints et une publication PyPI corrigée.
- 2026-08-23 : les mainteneurs ont publié une FAQ et une feuille de route ; le support officiel vise NVIDIA/x86_64, tandis que macOS, AMD, aarch64, le parallélisme de tenseurs, la vision et une prise en charge élargie du format GGUF restent prévus.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-19, aucun changement de workflow pour les praticiens ne peut être validé à partir des seuls liens datés ; consultez la page du projet et le dépôt avant de vous fier à FreeToken.

1. Vérifiez les prérequis pour Linux x86_64, GPU NVIDIA, pilote r580+ et Python 3.10+, puis créez un environnement et installez `freetoken[accel]` avec uv.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md>
2. Lancez `ft serve --model <chemin-local-ou-identifiant-HF>` ; par défaut, le serveur écoute sur `127.0.0.1:1919`.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>
3. Vérifiez l'installation avec `ft --version` et une requête vers `/v1/chat/completions`, puis connectez un client compatible OpenAI.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md>

## Bonnes pratiques {#best-practices}

- Mesurez la bande passante CPU et PCIe avec `ft bench bw` avant de choisir un backend, afin de calibrer le déchargement MoE.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>
- Prévoyez de la RAM libre en fonction de la taille des poids d'experts pour les modèles MoE ; pour Qwen3.6-35B-A3B en bf16, la FAQ indique environ 70 Go.
  — <https://github.com/FlashML-org/FreeToken/issues/84>
- N'exposez pas le serveur au réseau sans configuration explicite ; l'adresse d'écoute par défaut est `127.0.0.1`. Vérifiez d'abord la réponse en local.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>

## Remplacé par ceci {#superseded-by-this}

- Rien de marqué comme obsolète pour l'instant.

## Toujours inconnu {#still-unknown}

- Les fichiers de publication principaux ne confirment ni le jeu de fonctionnalités ni la maturité de la version Windows Desktop ; les instructions pip officielles couvrent Linux.
- Les affirmations des articles sur les performances et le support matériel manquent de benchmarks indépendants pour des modèles, GPU ou charges de travail spécifiques.
- event_findings_placeholder

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/FlashML-org/FreeToken/releases | FreeToken releases | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken | FlashML-org/FreeToken README | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md | Guide d'installation de FreeToken | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md | Référence CLI de FreeToken | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/issues/84 | FAQ de FreeToken | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/issues/79 | Feuille de route de FreeToken (2026) | 2026-09-05 |
| https://arxiv.org/abs/2608.16157 | FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:freetoken`, fil `freetoken-development`, 0 événement daté - → -.
- **Remarque pratique :** Au 2026-08-19, aucun changement de workflow pour les praticiens ne peut être validé à partir des seuls liens datés ; consultez la page du projet et le dépôt avant de vous fier à FreeToken.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

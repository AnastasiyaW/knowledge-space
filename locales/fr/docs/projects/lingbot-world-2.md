---
title: "LingBot-World 2.0"
category: projects
date: 2026-07-09
tags: [lingbot-world, lingbot-world-2, lingbot-world-2-development, project]
aliases: ["LingBot-World 2.0"]
level: 2
source_sha256: 7a51723070bff0da9e3c7aa8ee04c60cd512f8076efc2bd7fe527217edb07f2d
translation: machine
translated_at: '2026-10-24'
---
# LingBot-World 2.0 {#lingbot-world-20}

**Ligne de développement :** `project:lingbot-world-2` · fil `lingbot-world-2-development`  
**Dernier événement :** 2026-07-09 · 1 événement daté depuis le 2026-07-09 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

LingBot-World 2.0, également appelé LingBot-World-Infinity, génère des mondes vidéo navigables à partir d'images destinés aux chercheurs et aux développeurs. Il prend en charge la diffusion en continu sans limite, le conditionnement par actions et un harnais d'agent pilote ou réalisateur. Le point de contrôle local public est `robbyant/lingbot-world-v2-14b-causal-fast` (14B). Le dépôt documente une inférence 480p multi-GPU, tandis que Reactor héberge `reactor/lingbot-world-2` en 1664×960 et 48 ips. Nous utilisons Reactor pour les prototypes et la version du dépôt 14B pour la recherche non commerciale, et non pour un déploiement auto-hébergé en temps réel.

## Ligne de développement {#development-line}

- **2026-07-09 — Les ressources publiques de développement de LingBot-World 2.0 ont été liées.** Le 2026-07-09, un enregistrement a relié LingBot-World 2.0 à sa page de projet, à son dépôt GitHub, à sa collection Hugging Face et à sa page Reactor. Cela marque une étape publique, bien que la source ne détaille ni le contenu de la version, ni ses capacités, ni son état opérationnel.

## Changements {#what-changed}

- **2026-07-08** — Le rapport technique est paru sur arXiv, décrivant le modèle 14B et un homologue 1.3B prévu.
- **2026-07-09** — LingBot-World 2.0 a publié son rapport, son code et ses modèles. Le point de contrôle ouvert opérationnel était `lingbot-world-v2-14b-causal-fast`. Les variantes 14B causal-pretrain, 14B bidirectionnelle et 1.3B restaient listées comme TODO. La version a ajouté la génération causale sur longue durée, une variante distillée en temps réel, des contrôles par actions et par texte, la prise en charge multijoueur et un harnais pilote/réalisateur.
- **2026-07-10** — Le dépôt a renommé une classe causale pour la maintenance du code, sans nouvelle capacité.
- **2026-07-14** — Le dépôt a révisé une description de prompt vidéo dans la documentation, sans nouvelle publication de modèle.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-09, considérez LingBot-World 2.0 comme une ligne distincte. Consultez la page de projet, le dépôt, la collection de modèles et la documentation Reactor avant de l'adopter.

1. Pour un prototype hébergé, générez une application Reactor avec `npx create-reactor-app my-lingbot-world-2-app --model=lingbot-world-2`.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
2. Ouvrez une session avec le nom de modèle `reactor/lingbot-world-2`, importez une image de référence, définissez un prompt textuel, puis envoyez `start`. La génération échoue tant que l'image et le prompt ne sont pas tous deux présents.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
3. Pilotez le monde en cours avec les déplacements longitudinaux et latéraux, les commandes de regard ou `set_camera_pose`. Mettez à jour les conditions en cours de flux avec `set_prompt`.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
4. Pour une inférence locale de recherche, clonez le dépôt, installez les dépendances avec Torch 2.4+ et FlashAttention, téléchargez `robbyant/lingbot-world-v2-14b-causal-fast`, puis exécutez la commande causale rapide multi-GPU fournie ou `run_fast.sh`.
  — <https://github.com/robbyant/lingbot-world-v2>

## Bonnes pratiques {#best-practices}

- Séparez les prompts en couches : base, caméra, mouvement, événement et contrôle vertical. Gardez chaque couche sur un seul axe de contrôle afin que les prompts n'entrent pas en conflit avec le mouvement actif.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide>
- Limitez la longueur totale du prompt à environ 2 000 caractères. Réduisez les clauses d'événement avant l'identité de base ou les règles de contrôle.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide>
- Traitez le mouvement comme un état persistant et envoyez une commande d'arrêt explicite. Les impulsions courtes peuvent manquer la frontière de segment.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
- Ne vous attendez pas à un code de déploiement officiel pour le modèle ouvert. Le dépôt le retient, et la licence est CC BY-NC-SA 4.0 pour un usage non commercial.
  — <https://github.com/robbyant/lingbot-world-v2>

## Remplacé par {#superseded-by-this}

- **2026-07-09** — Les notes de LingBot-World 1.0 sont obsolètes sur Reactor. World 2 les remplace par une navigation à deux axes, des poses de caméra et un pilotage des prompts en cours de flux.
- **2026-07-09** — Attendre que chaque modèle 14B et 1.3B annoncé soit téléchargeable est obsolète. Seul le point de contrôle 14B causal-fast est public ; le reste reste en TODO.

## Points encore inconnus {#still-unknown}

- Le billet du 9 juillet affirme que le modèle temps réel fonctionne en 720p à 60 ips, alors que Reactor indique 1664×960 à 48 ips. Les sources ne fournissent aucune comparaison directe.
- Le dépôt retient le code de déploiement. Les exigences matérielles, la pile de service et la latence pour un service officiel en temps réel restent non documentées.
- L'article arXiv décrit un homologue 1.3B, mais la liste TODO du dépôt du 9 juillet ne fournit ni poids ni code téléchargeables pour le 1.3B.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://technology.robbyant.com/lingbot-world-v2 | Page de projet LingBot-World 2.0 | 2026-09-05 |
| https://github.com/robbyant/lingbot-world-v2 | Robbyant/lingbot-world-v2 | 2026-09-05 |
| https://huggingface.co/collections/robbyant/lingbot-world-v2 | Collection LingBot-World-V2 | 2026-09-05 |
| https://www.reactor.inc/lingbot-world-2 | LingBot World 2 — Reactor | 2026-09-05 |
| https://arxiv.org/abs/2607.07534 | Infinite Worlds with Versatile Interactions | 2026-09-05 |
| https://github.com/robbyant/lingbot-world-v2/commits/main | Historique des commits LingBot-World-V2 | 2026-09-05 |
| https://huggingface.co/robbyant/lingbot-world-v2-14b-causal-fast | robbyant/lingbot-world-v2-14b-causal-fast | 2026-09-05 |
| https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview | Vue d'ensemble LingBot World 2 | 2026-09-05 |
| https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide | Guide des prompts LingBot World 2 | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:lingbot-world-2`, fil `lingbot-world-2-development`, 1 événement daté du 2026-07-09 au 2026-07-09.
- **Note pratique :** À partir du 2026-07-09, considérez LingBot-World 2.0 comme une ligne distincte. Consultez la page de projet, le code, la collection et la documentation produit avant l'adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

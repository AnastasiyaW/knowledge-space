---
title: "JoyCaption"
category: projects
tags: [joycaption, joycaption-development, project]
aliases: ["JoyCaption"]
level: 3
source_sha256: 38b6b311ece1c22445c25055f730b547794ba2874c24c41f31396e5dd992cbbf
translation: machine
translated_at: '2026-10-24'
---
# JoyCaption {#joycaption}

**Ligne de développement :** `project:joycaption` · fil `joycaption-development`  
**Événements :** 2 datés, 2024-09-26 → 2025-05-13 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

JoyCaption est un VLM open source de légendage d'images destiné aux créateurs de jeux de données pour modèles de diffusion, et une alternative locale aux API de légendage payantes comme GPT-4o.

- Produit des légendes descriptives et des légendes factuelles concises.
- Génère des prompts de style diffusion et plusieurs formats de listes de tags.
- S'exécute via Transformers, un script batch ou un endpoint compatible OpenAI de vLLM.

## Ligne de développement {#development-line}

- **2024-09-26 — Enregistrement du Hugging Face Space de JoyCaption Alpha One.** Le 2024-09-26, JoyCaption a été lancé sous la forme du Hugging Face Space fancyfeast/joy-caption-alpha-one. La démo a établi Alpha One, sans détails publics sur le modèle ni notes de version.
- **2025-05-13 — Enregistrement des références publiques de JoyCaption Beta One.** Le 2025-05-13, JoyCaption a ajouté Beta One avec un dépôt GitHub, un Hugging Face Space, une page de modèle Hugging Face et un article Civitai. Ces liens ont établi Beta One, sans comparaisons techniques avec Alpha One.

## Évolutions {#what-changed}

Ligne de développement de JoyCaption :

- 2024-09-26 — Alpha One a été lancé sous la forme d'un Hugging Face Space public pour le légendage interactif.
- 2025-05-13 — Beta One a ajouté le modèle téléchargeable, une démo mise à jour et des scripts locaux ; il améliore le suivi des instructions par rapport à Alpha Two, mais reste en bêta.
- Constaté aujourd'hui — le README officiel présente toujours Beta One comme version actuelle ; GitHub Releases ne contient aucune version packagée, et le projet n'a pas annoncé de version 1.0.

## Mode d'emploi {#how-to-use-this}

Depuis le 2024-09-26, nous disposions du Hugging Face Space d'Alpha One comme référence ; depuis le 2025-05-13, nous suivons Beta One à travers son dépôt, son Space, sa page de modèle et son article, plutôt que l'ancien lien Alpha.

1. Essayez d'abord la démo officielle de Beta One et inspectez le mode de sortie et le prompt généré avant d'automatiser un flux de travail.
  — <https://github.com/fpgaminer/joycaption>
2. Pour une utilisation locale, chargez `fancyfeast/llama-joycaption-beta-one-hf-llava` avec Transformers, envoyez un message combinant image et texte, lancez la génération, puis décodez uniquement les tokens nouvellement générés.
  — <https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava>
3. Choisissez `Descriptive Caption` pour un texte d'entraînement détaillé ou `Straightforward` pour des étiquettes concises et concrètes ; exprimez la longueur et le ton selon la forme de prompt documentée.
  — <https://github.com/fpgaminer/joycaption>
4. Pour un jeu de données, exécutez `batch-caption.py` avec `--glob` ou `--filelist`, ainsi que `--prompt` ou un `--prompt-file` pondéré ; les légendes sont écrites dans des fichiers `.txt` adjacents.
  — <https://github.com/fpgaminer/joycaption/blob/main/scripts/README.md>
5. Pour un endpoint applicatif, servez Beta One avec vLLM et appelez son API de chat-completions compatible OpenAI.
  — <https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava>

## Bonnes pratiques {#best-practices}

- Passez `--model` explicitement dans les tâches batch : la documentation du script utilise encore Alpha Two par défaut, donc accepter cette valeur peut sélectionner un modèle plus ancien.
  — <https://github.com/fpgaminer/joycaption/blob/main/scripts/README.md>
- Commencez par les modes Descriptive ou Straightforward ; le mainteneur les présente comme les plus utiles et qualifie plusieurs autres modes de moins stables.
  — <https://github.com/fpgaminer/joycaption>
- Auditez les étiquettes utilisées pour l'entraînement ou pour des décisions, en particulier pour les sujets multiples, les relations gauche/droite, l'OCR et le suivi des instructions ; Beta One documente des échecs résiduels et des artefacts.
  — <https://github.com/fpgaminer/joycaption>
- Dans les intégrations LLaVA directes, conservez le chemin de template de chat documenté et inspectez les identifiants d'entrée afin que les tokens BOS dupliqués ne dégradent pas la sortie.
  — <https://github.com/fpgaminer/joycaption>
- Utilisez une quantification 8 bits ou 4 bits lorsque le bfloat16 natif ne tient pas en mémoire, plutôt que de supposer que le modèle est léger.
  — <https://github.com/fpgaminer/joycaption>

## Remplacé par {#superseded-by-this}

- 2024-09-26 — JoyCaption Alpha One : remplacé, pour les nouveaux travaux, par Beta One, que le README officiel présente toujours comme le modèle actuel.
- 2024-09-26 — Attentes de l'ère Alpha en matière de légendage fiable : remplacées par le flux de travail Beta One, plus performant, mais sans revendication de fiabilité 1.0.

## Inconnues {#still-unknown}

- Aucune annonce officielle n'établit l'existence d'une version postérieure à Beta One ni ne confirme une maintenance active après les mises à jour du modèle et de la démo en 2025.
- L'article de version cité https://civitai.com/articles/14672 a renvoyé une erreur pendant la recherche ; ses notes de version n'ont donc pas été utilisées.
- Le Space Beta One hébergé est listé comme « Running on Zero » ; il n'a pas été exécuté, donc la disponibilité en direct, le temps de démarrage à froid et la qualité des sorties n'ont pas été testés de manière indépendante.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/fpgaminer/joycaption | JoyCaption — dépôt GitHub officiel et README | 2026-09-04 |
| https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava | llama-joycaption-beta-one-hf-llava — fiche de modèle Hugging Face | 2026-09-04 |
| https://github.com/fpgaminer/joycaption/blob/main/scripts/README.md | Documentation de batch-caption.py de JoyCaption — GitHub | 2026-09-04 |
| https://huggingface.co/spaces/fancyfeast/joy-caption-beta-one | Joy Caption Beta One — Hugging Face Space | 2026-09-04 |
| https://huggingface.co/spaces/fancyfeast/joy-caption-alpha-one | Joy Caption Alpha One — Hugging Face Space | 2026-09-04 |
| https://github.com/fpgaminer/joycaption/releases | Versions de JoyCaption — GitHub | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:joycaption`, fil `joycaption-development`, 2 événements datés du 2024-09-26 au 2025-05-13.
- **Note pratique :** Depuis le 2024-09-26, les praticiens pouvaient utiliser le Hugging Face Space d'Alpha One comme référence publique de JoyCaption ; depuis le 2025-05-13, ils doivent aussi consulter le dépôt, le Space, la page de modèle et l'article Beta One liés, plutôt que de s'appuyer uniquement sur l'ancienne référence Alpha.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

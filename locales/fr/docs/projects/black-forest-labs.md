---
title: "FLUX.1-Kontext-dev-onnx — FLUX.1 Kontext ONNX et édition"
category: projects
date: 2025-07-03
tags: [black-forest-labs, black_forest_labs, flux-kontext, flux_kontext, project]
aliases: ["FLUX.1-Kontext-dev-onnx", "Kontext Komposer"]
level: 3
source_sha256: ff1af75935176435b33e1c982a54a2bfc1ec65324d2659af4c6836937aedf54c
translation: machine
translated_at: '2026-10-24'
---
# FLUX.1-Kontext-dev-onnx — FLUX.1 Kontext ONNX et édition {#flux1-kontext-dev-onnx-flux1-kontext-onnx-and-editing}

**Ligne de développement :** `project:black-forest-labs` · fil `flux-kontext`  
**Dernier événement :** 2025-07-03 · 1 événement daté depuis le 2025-07-03 · **Recherche :** 2026-09-04 · confiance : moyenne

## Description {#what-it-is}

FLUX.1-Kontext-dev-onnx est l'export ONNX de FLUX.1 Kontext [dev] destiné aux runtimes locaux.

- Édition d'images à partir d'instructions textuelles.
- Modifications locales et globales, avec préservation du personnage ou du style au fil des itérations.
- Exports du modèle en BF16, FP8 et FP4 (SVDQuant).

## Ligne de développement {#development-line}

- **2025-07-03 — Black Forest Labs a publié le dépôt ONNX de FLUX.1 Kontext dev.** La version officielle proposait des exports BF16, FP8 et FP4 (SVDQuant) du modèle de base public Kontext [dev]. Il s'agit d'un format de packaging pour des poids existants, et non d'une nouvelle version du modèle de base.

## Changements {#what-changed}

2025-07-03 — FLUX.1-Kontext-dev-onnx : Black Forest Labs a fourni des exports BF16, FP8 et FP4 (SVDQuant) du modèle public Kontext [dev]. Il s'agit d'une option de packaging pour runtime et non d'une nouvelle version du modèle de base.

2025-07-11 — Préréglages BFL Playground et Kontext Komposer : l'éditeur web a ajouté l'édition guidée par texte sans code, et une publication communautaire a documenté des préréglages de prompts. Aucune de ces sources n'introduit de poids ONNX, d'API ni de révision du modèle.

Constaté aujourd'hui (2026-09-04) — BFL maintient Kontext disponible en tant qu'outil de génération précédente. Les sorties restent à 1 MP. BFL recommande FLUX.2 pour les nouveaux projets nécessitant des sorties allant jusqu'à 4 MP, des éditions à références multiples ou un contrôle plus précis.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-07-03, commencez l'évaluation par le dépôt ONNX. Vérifiez les révisions du modèle et la prise en charge par le runtime avant toute intégration.

1. Ouvrez le dépôt ONNX officiel, connectez-vous et acceptez la licence FLUX.1 [dev] Non-Commercial License (accès restreint) avant de télécharger les fichiers.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
2. Choisissez BF16, FP8 ou FP4 (SVDQuant) pour un runtime pris en charge. La fiche ne fournit aucun extrait de code spécifique au modèle ; vérifiez la prise en charge avant d'utiliser un workflow générique Diffusion Single File.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
3. Utilisez les poids canoniques de Kontext [dev] lorsque ONNX n'est pas nécessaire. Installez Diffusers, chargez le pipeline, puis transmettez une image d'entrée et un prompt d'édition.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/tree/main>
4. Pour une évaluation hébergée, ouvrez la route d'édition originale du Playground et connectez-vous. Lors de la vérification d'aujourd'hui, elle redirige vers l'authentification BFL, puis vers le Playground du tableau de bord.
  — <https://playground.bfl.ai/image/edit>
5. Choisissez FLUX.2 plutôt que de démarrer une nouvelle intégration Kontext lorsqu'un projet de production nécessite une sortie supérieure à 1 MP ou plusieurs références.
  — <https://help.bfl.ai/articles/5186006235-what-is-flux-1-kontext>

## Bonnes pratiques {#best-practices}

- Formulez une seule modification visuelle explicite à la fois, par exemple « Change the car color to red », puis inspectez le résultat avant la modification suivante.
  — <https://docs.bfl.ai/kontext/kontext_image_editing>
- Indiquez à la fois le texte source et le texte de remplacement pour les modifications de texte dans l'image. Utilisez des cadres d'annotation contrastés lorsqu'une modification de texte nécessite un repositionnement ou un redimensionnement ciblé.
  — <https://docs.bfl.ai/kontext/kontext_image_editing>
- Gardez les chaînes d'édition courtes et sauvegardez les bons résultats intermédiaires. BFL signale une dégradation visible après six éditions itératives ; repartez donc d'une image propre plutôt que de prolonger indéfiniment une même chaîne.
  — <https://bfl.ai/blog/flux-1-kontext>
- Considérez les poids dev comme non commerciaux et non destinés à la production par défaut. Mettez en place un filtrage ou une revue manuelle, et respectez les exigences applicables en matière de provenance.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
- Pratique communautaire : construisez des préréglages sous forme de modèles de prompts modifiables qui préservent le sujet tout en modifiant le contexte, la scène, le style, les vêtements ou l'arrière-plan. Ce ne sont pas des contrôles officiels du modèle.
  — <https://www.reddit.com/r/StableDiffusion/comments/1lx8lot/kontext_presets_all_system_prompts/>

## Remplacé par {#superseded-by-this}

- L'accès par e-mail en bêta privée du 2025-05-29 a pris fin avec la publication des poids ouverts au public le 2025-06-26. L'accès passe désormais par le flux de licence Hugging Face à accès restreint.
- Les indications du 2025-07-11 décrivant l'URL d'édition du Playground comme un point d'entrée non authentifié sont obsolètes. Telle qu'observée le 2026-09-04, elle redirige vers l'authentification BFL puis vers le tableau de bord.
- Les recommandations de l'époque 2025 consistant à construire de nouvelles éditions haute résolution ou multi-références avec Kontext sont remplacées par la recommandation de BFL d'utiliser FLUX.2. Kontext reste disponible ; il n'a pas été retiré.

## Points encore inconnus {#still-unknown}

- L'artefact ONNX du 2025-07-03 et les documents navigateur et préréglages du 2025-07-11 partagent le nom de famille Kontext, mais rien ne prouve qu'il s'agit d'un seul produit. Le premier est une distribution locale ; le second couvre un éditeur hébergé et une couche de prompts communautaire.
- Kontext Komposer apparaît dans les publications communautaires comme libellé de préréglage, par exemple « Komposer : Teleport ». Aucune source de première main ne l'établit comme produit, version ou composant officiel de BFL, ni comme élément du dépôt ONNX.
- La fiche officielle du modèle ONNX ne fournit aucun exemple de runtime de bout en bout. Nous devons fournir un pipeline ONNX personnalisé compatible ou utiliser la voie Diffusers documentée.
- Le texte daté original de la source n'est pas disponible ; nous ne pouvons donc pas reconstruire ses affirmations exactes, le statut d'approbation par BFL ni les révisions d'export à partir des seuls liens.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx | black-forest-labs/FLUX.1-Kontext-dev-onnx · Hugging Face | 2026-09-04 |
| https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/tree/main | black-forest-labs/FLUX.1-Kontext-dev at main · Hugging Face | 2026-09-04 |
| https://bfl.ai/blog/flux-1-kontext-dev | FLUX.1 Kontext [dev] - Open Weights for Image Editing | Black Forest Labs | 2026-09-04 |
| https://bfl.ai/blog/flux-1-kontext | Introducing FLUX.1 Kontext and the BFL Playground | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/kontext/kontext_image_editing | Image Editing | Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/5186006235-what-is-flux-1-kontext | What is FLUX.1 Kontext? | Black Forest Labs Knowledge Base | 2026-09-04 |
| https://playground.bfl.ai/image/edit | Black Forest Labs - Frontier AI Lab | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/1lx8lot/kontext_presets_all_system_prompts/ | Kontext Presets - All System Prompts : r/StableDiffusion | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:black-forest-labs`, fil `flux-kontext`, 1 événement daté du 2025-07-03 au 2025-07-03.
- **Remarque pratique :** à partir du 2025-07-03, les praticiens qui évaluent cette ligne doivent commencer par le dépôt ONNX lié comme artefact de déploiement, puis vérifier séparément la révision du modèle et la prise en charge par le runtime avant intégration.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

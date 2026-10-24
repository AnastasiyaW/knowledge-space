---
title: "Krea AI"
category: projects
date: 2025-04-30
tags: [krea, krea-ai, krea-ai-creative-workflows, krea-ai-video, project]
aliases: ["Krea AI", "Krea.ai"]
level: 3
source_sha256: b4fe4abd601da41ee852e04be16e8f2b64ba37d7375538fb8b3876887e759ade
translation: machine
translated_at: '2026-10-24'
---
# Krea AI {#krea-ai}

**Ligne de développement :** `project:krea-ai` · fil `krea-ai-creative-workflows`  
**Dernier événement :** 2025-04-30 · 4 événements datés depuis 2024-05-23 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Krea AI est un espace de travail dans le navigateur pour les images, la vidéo et la 3D, couvrant la génération, l'édition ciblée, l'amélioration, l'animation et l'entraînement de LoRA.

Fonctionnalités :
- Génération : création d'images à partir de prompts et d'images de référence, avec les modèles de Krea et de tiers.
- Édition et animation : modification de zones, animation d'images fixes et agrandissement des sorties.
- Entraînement : création de styles, de personnages ou de produits réutilisables avec LoRA.
- Contrôles Krea 2 : gestion de la référence de style maison, des moodboards et de la direction créative.

L'accès gratuit fournit 100 unités de calcul par jour, avec un accès limité à la vidéo, à la 3D, à l'agrandissement et aux LoRA ; les générations payantes incluent une licence commerciale. Nous l'utilisons comme surface d'itération multi-modèles et comme voie de contrôle de style Krea 2, et non comme modèle unique et figé ni comme outil gratuit illimité.

## Ligne de développement {#development-line}

- **2024-05-23 — Une route Krea AI Video v1 a été mentionnée.** Le 2024-05-23, la source datée renvoyait vers la route Video v1 de Krea AI. Cela établit que Video v1 était mentionnée pour Krea AI à cette date. Les éléments disponibles ne permettent pas de vérifier ses fonctionnalités exactes, son statut de lancement ni sa disponibilité.
- **2024-11-08 — Une route d'entraînement Krea AI a été mentionnée.** Le 2024-11-08, la source datée renvoyait vers la route d'entraînement de Krea AI. Cela établit qu'un workflow d'entraînement était mentionné pour Krea AI à cette date. Le lien CG Event associé ne fournit aucun détail produit vérifiable supplémentaire.
- **2024-12-13 — Une route d'édition Krea AI a été mentionnée.** Le 2024-12-13, la source datée renvoyait vers la route d'édition de Krea AI. Cela établit qu'un workflow d'édition était mentionné pour Krea AI à cette date. Les éléments disponibles ne confirment ni ses opérations exactes, ni son statut de sortie, ni sa disponibilité.
- **2025-04-30 — Une route d'amélioration Krea AI a été mentionnée.** Le 2025-04-30, la source datée renvoyait vers la route enhancer de Krea AI. Cela établit qu'un workflow d'amélioration était mentionné pour Krea AI à cette date. Les éléments disponibles ne confirment ni la méthode d'amélioration exacte, ni les affirmations de qualité, ni la disponibilité.

## Évolutions {#what-changed}

- 2024-04-09 — Une entrée de la page d'accueil de Krea est enregistrée, mais aucun détail de version daté ne subsiste pour établir un changement produit distinct.
- 2024-05-23 — Krea Video Open Beta est ouverte à tous, avec l'ajout d'une animation basée sur une timeline, avec keyframes et prompts image/texte.
- 2024-11-08 — Krea commence le déploiement de Train pour les modèles personnalisés de personnages, de styles et de produits.
- 2024-12-13 — Krea Editor entre en open beta gratuite, faisant passer le produit de la seule génération vers l'intervention ciblée sur les images.
- 2024-12-19 — Les entraînements personnalisés arrivent dans Krea Editor pour un placement de produit appris dans les images.
- 2025-04-29 — Krea Stage ajoute le rendu GPT-4o pour des vues alternatives d'une scène 3D contrôlée.
- 2025-04-30 — Krea Enhancer ajoute un nouveau modèle d'amélioration et une intégration Topaz, portant le plafond d'agrandissement annoncé à 22K.

## Mode d'emploi {#how-to-use-this}

Au 2025-04-30, nous considérons Krea AI comme des workflows distincts de vidéo, d'entraînement, d'édition et d'amélioration, et nous choisissons la route nommée correspondant à la tâche plutôt que de nous fier à la seule page d'accueil.

1. Ouvrez Image, rédigez un prompt avec le sujet, la composition, le style, l'éclairage ou importez des images de référence ; choisissez un modèle et un format, puis comparez les variations.
  — <https://www.krea.ai/features/ai-image-generator>
2. Pour Krea 2, utilisez des références de style ou un moodboard pour guider la direction visuelle, et contrôlez l'intensité d'action des références sur le résultat.
  — <https://www.krea.ai/blog/krea-2-api-launch>
3. Utilisez Krea 2 Turbo pour explorer rapidement les prompts, les références et les moodboards ; passez la direction retenue en Medium ou Large lorsque l'adhérence exacte au style ou le fini final compte.
  — <https://www.krea.ai/blog/krea-2-turbo>
4. Pour un style, un personnage ou un produit réutilisable, ouvrez Train, créez un LoRA à partir d'au moins trois images apparentées, relisez les légendes, puis sélectionnez le LoRA terminé dans Image.
  — <https://www.krea.ai/blog/krea-2-lora-training>
5. Ouvrez Edit depuis une image générée ou importez-en une, sélectionnez uniquement la zone à modifier avec un rectangle, un pinceau ou une sélection d'objet, décrivez la modification et itérez depuis la bande d'historique.
  — <https://www.krea.ai/blog/krea-edit>
6. Pour la livraison finale, importez l'image retenue dans Enhancer, lancez Enhance, inspectez le résultat et téléchargez la sortie.
  — <https://www.krea.ai/enhancer>
7. Pour animer une image fixe, ouvrez une image générée ou importée dans Video et définissez le mouvement et la direction de caméra avec le modèle image-vers-vidéo choisi.
  — <https://www.krea.ai/features/ai-image-generator>

## Bonnes pratiques {#best-practices}

- Gardez un jeu de données LoRA ciblé. Pour un personnage, variez l'angle, l'expression, l'éclairage et l'arrière-plan ; pour un style, gardez un langage visuel cohérent sans répéter une même composition.
  — <https://www.krea.ai/blog/krea-2-lora-training>
- Relisez les légendes automatiques et nommez explicitement les détails qui ne doivent pas être appris ; commencez par un seul personnage, un seul style ou une seule identité de produit plutôt que de mélanger les concepts.
  — <https://www.krea.ai/blog/krea-2-lora-training>
- Utilisez Turbo pour les explorations rapides et Medium ou Large pour les rendus finaux ; Turbo conserve les contrôles mais n'est pas le choix recommandé pour une fidélité maximale de l'image finale.
  — <https://www.krea.ai/blog/krea-2-turbo>
- Gardez le prompt fixe en ne modifiant qu'un Generative Slider à la fois. Utilisez la créativité Raw ou Low pour les prompts précis, et Medium ou High seulement lorsqu'une interprétation délibérée est souhaitée.
  — <https://www.krea.ai/blog/generative-sliders>
- Modifiez la plus petite zone nécessaire et préservez le reste du cadre ; utilisez l'historique d'édition plutôt que de régénérer l'image entière après chaque révision.
  — <https://www.krea.ai/blog/krea-edit>
- Pour un travail local avec Krea 2, entraînez les LoRA sur Raw et exécutez-les sur Turbo ; utilisez Raw pour le fine-tuning ou la recherche plutôt que comme point de contrôle d'inférence finale par défaut.
  — <https://www.krea.ai/krea-2-open-source>
- Comparez les sorties entre modèles lorsque le texte lisible ou le respect strict des consignes compte, car la précision du texte et l'adhérence aux consignes varient selon le modèle.
  — <https://www.krea.ai/features/ai-image-generator>

## Remplacé par {#superseded-by-this}

- 2026-03-09 — Le workflow open beta de Krea Editor de 2024 est historique ; l'actuel Krea Edit est un éditeur régional reconstruit, avec déplacements d'objets, relighting, contrôles de caméra/objectif et historique des révisions.
- 2026-05-28 — La restriction bêta initiale des LoRA Krea 2 réservée aux plans Max/Business du 2026-05-21 a été suivie d'une annonce du changelog élargissant la disponibilité ; l'accès effectif dépend toujours des limites du compte et du plan.
- 2026-06-23 — Les consignes ne concernant que Krea 2 hébergé sont obsolètes : les poids de Krea 2 Raw et de Krea 2 Turbo sont disponibles en parallèle des routes hébergées de l'outil Image et de l'API.
- 2026-08-28 — Veo 2 et Veo 3 ont été retirés de l'outil Video et de l'API de Krea ; Veo 3.1 ou Veo 3.1 Lite sont les remplacements annoncés.

## Points encore inconnus {#still-unknown}

- La mention de la page d'accueil du 2024-04-09 n'a pas de note de version Krea datée et récupérable ; aucune version produit n'est donc affirmée pour cette date.
- Plusieurs détails de 2024 sont reconstitués à partir de comptes rendus de l'époque citant des publications de Krea, car les anciennes URLs de l'application Krea redirigent désormais ou n'exposent plus le contenu historique des versions.
- La disponibilité des LoRA Krea 2 dépend du moment et du plan : le blog du 21 mai parle d'une bêta Max/Business, le changelog du 28 mai d'un accès élargi, et la tarification actuelle ne confirme qu'un accès limité aux LoRA dans l'offre gratuite.
- Aucune archive de notes de version en chinois publiée par Krea n'a été trouvée sur les routes consultées ; les sources en chinois n'ont pas servi à dater la chronologie.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.theaivideocreator.ai/p/create-stunning-videos-with-keyframes-and-text-prompts-with-this-free-tool-b1558e46bd4d | Krea Video anime des images avec des keyframes et des prompts | 2026-09-04 |
| https://note.com/takion0105/n/n3276dd936bcc | Weekly Report 2024/11/13 (wed) | 2026-09-04 |
| https://ai-weekly.ai/newsletter-12-17-2024/ | AI-Weekly for Tuesday, December 17, 2024 - Issue 143 | 2026-09-04 |
| https://ai-weekly.ai/newsletter-12-24-2024/ | AI-Weekly for Tuesday, December 24, 2024 - Issue 144 | 2026-09-04 |
| https://note.com/omusubi__chan/n/n324c507c7a33 | AIで3D空間をリアルな画像に！「Krea Stage」とChatGPTの連携が実現 | 2026-09-04 |
| https://ai-weekly.ai/newsletter-05-06-2025/ | AI-Weekly for Tuesday, May 6, 2025 - Issue 163 | 2026-09-04 |
| https://www.krea.ai/blog/ship-week | Announcing Krea Ship Week | 2026-09-04 |
| https://www.krea.ai/blog/introducing-teams | Krea Teams : la collaboration créative simplifiée | 2026-09-04 |
| https://www.kimp.io/kimps-picks-june-13th/ | KIMP’s Picks June 13th: Weekly Highlights In Design, Marketing, AI, & More | 2026-09-04 |
| https://www.krea.ai/blog/flux-krea-open-source-release | Releasing Open Weights for FLUX.1 Krea | 2026-09-04 |
| https://www.krea.ai/blog/krea-realtime-14b | Krea Realtime 14B : génération vidéo IA en temps réel et de longue durée | 2026-09-04 |
| https://www.krea.ai/blog/krea-edit | Krea Edit : édition régionale, colorisation et relighting de toute image | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-image-model | What Is Krea 2? Krea's Foundation Image Model | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-lora-training | Krea 2 LoRA training is now available | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-api-launch | Krea 2 API : transfert de style, moodboards et tarification | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-turbo | Krea 2 Turbo : générer des images en 2 secondes | 2026-09-04 |
| https://www.krea.ai/blog/generative-sliders | Introducing Generative Sliders | 2026-09-04 |
| https://www.krea.ai/docs/changelog | Krea changelog | 2026-09-04 |
| https://www.krea.ai/krea-2-open-source | Krea 2 Open Source | 2026-09-04 |
| https://www.krea.ai/features/ai-image-generator | Générateur d'images IA : créer à partir de texte ou d'images de référence | 2026-09-04 |
| https://www.krea.ai/enhancer | Amélioration d'image IA gratuite, amélioration de photo et upscaler | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:krea-ai`, fil `krea-ai-creative-workflows`, 4 événements datés du 2024-05-23 au 2025-04-30.
- **Note pratique :** Au 2025-04-30, les praticiens doivent considérer Krea AI comme un ensemble de workflows vidéo, d'entraînement, d'édition et d'amélioration proposés séparément, et choisir la route nommée correspondant à la tâche plutôt que de se fier à la seule page d'accueil.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

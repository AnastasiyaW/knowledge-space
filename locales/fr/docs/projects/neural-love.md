---
title: "neural.love"
category: projects
date: 2022-12-23
tags: [neural-love, neural-love-image-tools, neural_love, project]
aliases: ["neural.love"]
level: 2
source_sha256: 2b80f2b536c39377748de8467c7c52670c00f669b3cfae4c6f9b7a07a154f7bb
translation: machine
translated_at: '2026-10-24'
---
# neural.love {#neurallove}

**Ligne de développement :** `project:neural-love` · fil `neural-love-image-tools`  
**Dernier événement :** 2022-12-23 · 2 dates depuis 2022-09-09 · **Recherche :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

neural.love est une plateforme web et API destinée aux créateurs qui ont besoin de génération d'images par IA, de traitement d'image et de flux de travail média.

- Génération texte-vers-image avec options de modèle, de style, de prompt, de mise en page, de HD et d'image d'entrée.
- Traitement d'image pour agrandir, accentuer, coloriser, restaurer et désrogner (uncrop).
- Flux de travail de création vidéo.

La limite par défaut documentée de l'API est de 300 requêtes par cinq minutes, et les travaux payants consomment des crédits. Nous l'utilisons pour des travaux courants et bornés, mais nous ne en faisons pas une nouvelle dépendance de production à long terme tant que la propriété et la continuité du support ne sont pas confirmées.

## Ligne de développement {#development-line}

- **2022-09-09 — neural.love a publié un lien vers une route et une documentation de génération d'art par IA.** La route AI Art Generator était présente ; une liste publique antérieure fait de cette date un jalon de visibilité, et non un lancement initial confirmé.
- **2022-12-23 — neural.love a publié un lien vers une route dédiée de désrognage d'image (uncrop).** La route Uncrop était présente ; son modèle d'origine, ses paramètres, son prix et ses limites restent non vérifiés.

## Ce qui a changé {#what-changed}

- 2022-09-09 : La route AI Art Generator était présente ; une liste publique antérieure fait de cette date un jalon de visibilité, et non un lancement initial confirmé.
- 2022-12-23 : La route Uncrop était présente ; son modèle d'origine, ses paramètres, son prix et ses limites restent non vérifiés.
- 2023-08-28 : Le texte-vers-image NL 1.01 et un mode HD mis à jour sont en ligne, avec des mises à jour de remix image-vers-image, de catégories, de recherche et de thème sombre.
- 2023-10-16 : Uncrop 2.0 a ciblé les artefacts et la conversion de rapport d'aspect.
- 2024-09-11 : Uncrop 4 a ajouté trois variantes par entrée et conservé l'outpainting en une ou deux passes.
- 2024-11-11 : MiniMax Video 01 a apporté au produit la génération image-vers-vidéo et texte-vers-vidéo.
- 2025-03-22 : La suite a ajouté l'édition d'image par commandes textuelles, des récits d'images agentiques, la génération texte-vers-vidéo à partir de références de sujet, Imgen 3, et un commutateur de désactivation de l'enrichissement des prompts.
- 2026-03-12 : Le propriétaire a mis en vente le produit, la marque, le domaine, la base de code et les supports d'exploitation, et a indiqué qu'il n'y investirait plus de manière significative.

## Comment l'utiliser {#how-to-use-this}

À la date du 2022-12-23, les praticiens doivent considérer la gamme d'outils d'image visible de neural.love comme couvrant à la fois la génération d'art par IA et une route dédiée de désrognage, tout en vérifiant le périmètre fonctionnel de l'époque avant de s'appuyer sur l'un ou l'autre flux de travail.

1. Pour la génération d'images dans le navigateur, ouvrez AI Art Generator, choisissez un modèle et un style, affinez le prompt, puis générez.
  — <https://neural.love/ai-art-generator>
2. Pour l'accès à l'API, connectez-vous, ouvrez Settings, générez un jeton API et envoyez-le en tant que jeton Bearer.
  — <https://docs.neural.love/>
3. Pour la génération d'images via l'API, envoyez un POST vers /v1/ai-art/generate avec des valeurs explicites pour prompt, style, layout, amount, isHd et isPublic ; conservez orderId et interrogez jusqu'à la fin du traitement.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
4. Pour le traitement via l'API, obtenez une URL de téléversement présignée, téléversez la source, puis créez une commande de traitement d'image ; utilisez image_uncrop seul avec outpainting ou aspect_ratio et interrogez la commande renvoyée.
  — <https://docs.neural.love/ai-images-processing-api>
5. Pour l'outpainting dans le navigateur, utilisez la route Uncrop en ligne pour étendre les bordures ou modifier le rapport d'aspect d'une image, puis inspectez le résultat généré avant de l'utiliser.
  — <https://neural.love/uncrop>

## Bonnes pratiques {#best-practices}

- Estimez les crédits avec les mêmes paramètres de génération avant de soumettre un travail payant.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
- Interrogez les commandes à intervalles croissants, par exemple 30, 45, 60, 90 et 150 secondes, plutôt que de boucler serrément.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
- Définissez isPublic explicitement et exécutez un test canari non sensible avant de traiter des contenus privés ; la documentation actuelle donne des valeurs par défaut contradictoires.
  — <https://docs.neural.love/faq>
- Gardez image_uncrop dans son propre travail de traitement ; l'API indique qu'il ne peut pas être combiné avec d'autres paramètres d'image.
  — <https://docs.neural.love/ai-images-processing-api>
- Considérez Uncrop comme une extension créative, et non comme une reconstruction historique : le produit avertit que les entrées sont réduites en résolution, que les résultats varient et que l'exactitude historique n'est pas son objectif.
  — <https://neural.love/blog/uncrop-4-image-expansion>
- Remplacez les identifiants déployés avant de générer un nouveau jeton API, car un seul jeton est actif par compte et un nouveau jeton désactive l'ancien.
  — <https://docs.neural.love/>

## Remplacé par ceci {#superseded-by-this}

- 2022-09-09 comme date de disponibilité publique initiale d'AI Art Generator — obsolète depuis 2022-08-23.
- Les instructions antérieures à Uncrop 4 comme guide actuel — obsolètes depuis 2024-09-11.
- Le fait que le propriétaire actuel investisse encore de manière significative dans le produit — obsolète depuis 2026-03-12.

## Toujours inconnu {#still-unknown}

- Aucune note de lancement datée émanant de neural.love n'a été trouvée pour le lien AI Art Generator du 2022-09-09 ni pour le lien Uncrop du 2022-12-23 ; leur modèle d'origine, leurs entrées, leur prix et leurs limites restent non vérifiés.
- La route historique https://docs.neural.love/docs n'a pas pu être récupérée aujourd'hui ; son contenu de 2022 a peut-être été déplacé, mais il n'est pas vérifié ici.
- La documentation API actuelle est contradictoire sur la visibilité par défaut des générations artistiques : le tutoriel indique que toutes les générations sont publiques par défaut, tandis que la FAQ indique que les générations API sont privées par défaut.
- L'avis de mise en vente ne donne ni date de clôture, ni acquéreur, ni plan de transition, ni engagement de support, ni SLA pour l'API.
- Une recherche en chinois simplifié n'a trouvé aucune corroboration datée et émanant de neural.love pour les deux routes de 2022.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://neural.love/ai-art-generator | AI Art Generator & AI Image Generator | neural.love | 2026-09-04 |
| https://neural.love/uncrop | Uncrop Image Online – Extend Photos for Free | neural.love | 2026-09-04 |
| https://docs.neural.love/ | Getting Started | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api | How to generate AI art with neural.love API | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/ai-images-processing-api | AI Images Processing API | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/faq | neural.love API - Frequently Asked Questions | The neural.love API Developer Hub | 2026-09-04 |
| https://akinix.com/forums/topic/209-curated-ai-art-generator-by-neurallove/ | Curated AI art generator by neural.love - General discussions - Akinix | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/xev8ds | Free stable diffusion generation website – neural.love | 2026-09-04 |
| https://neural.love/blog/new-text-to-image-model-and-future-roadmap | New text-to-image model is here & Future Roadmap | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/uncrop-2-0-feature-update | Feature Update: Uncrop 2.0 – Less Glitches | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/uncrop-4-image-expansion | Introducing Uncrop 4: Expand Your Images Like Never Before | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/video-generation-launch | Introducing Video Generation: Transform Images into Motion with neural.love | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/march-2025-release-notes | Product Updates: March 2025 Release Notes | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/neural-love-is-for-sale | neural.love assets are for sale | neural.love blog about AI stuff | 2026-09-04 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:neural-love`, fil `neural-love-image-tools`, 2 événements datés du 2022-09-09 au 2022-12-23.
- **Note pratique :** À la date du 2022-12-23, les praticiens doivent considérer la gamme d'outils d'image visible de neural.love comme couvrant à la fois la génération d'art par IA et une route dédiée de désrognage, tout en vérifiant le périmètre fonctionnel de l'époque avant de s'appuyer sur l'un ou l'autre flux de travail.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité quant à ce qui est obsolète.

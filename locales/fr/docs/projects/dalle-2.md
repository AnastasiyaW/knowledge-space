---
title: "DALL-E 2 — Adoption commerciale"
category: projects
date: 2022-06-22
tags: [dalle-2, dalle-2-commercial-adoption, dalle_2_commercial_adoption, dalle_2_commercialization, project]
aliases: ["DALL-E 2"]
level: 2
source_sha256: 0c865eba5a16695412424a0a1757f07c7c1d035eda7ae9030186c2f89ba7ce4a
translation: machine
translated_at: '2026-10-24'
---
# DALL-E 2 — Adoption commerciale {#dall-e-2-commercial-adoption}

**Ligne de développement :** `project:dalle-2` · fil `dalle-2-commercial-adoption`  
**Dernier événement :** 2022-06-22 · 1 événement daté depuis le 2022-06-22 · **Recherche :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

DALL-E 2 — le modèle de génération d'images à partir de prompts textuels d'OpenAI, publié en 2022, désormais une dépendance héritée plutôt qu'un produit API utilisable.

- génération d'images à partir de prompts textuels
- workflows éditoriaux d'images pour les premières expérimentations commerciales

## Ligne de développement {#development-line}

- **2022-06-22 — Cosmopolitan a documenté une expérimentation de couverture avec DALL-E 2.** Le 2022-06-22, Cosmopolitan a documenté une expérimentation de couverture utilisant DALL-E 2. Elle montrait le système dans un contexte éditorial commercial. Les liens n'établissent ni conditions de collaboration ni périmètre commercial plus large.

## Ce qui a changé {#what-changed}

Le 2022-06-22, Cosmopolitan a utilisé DALL-E 2 dans un workflow de couverture éditoriale. Les directeurs artistiques humains ont placé manuellement le bandeau et les titres de couverture, car le texte généré n'était pas fiable.
Le 2022-06-30, un rapport daté décrivait une enquête auprès des utilisateurs sur la tarification, relative à la monétisation, et non un prix publié ni un lancement général. Nous n'avons pas pu lire le texte intégral du rapport lors de la relecture.
Le 2026-09-04, OpenAI a marqué DALL-E 2 comme obsolète et l'a retiré de l'API, et recommande GPT-Image-2 pour la génération et l'édition.
Nous pouvons vérifier l'expérimentation éditoriale et le retrait du modèle, mais pas les détails de l'enquête sur les prix. La ligne de développement se termine par un retrait, et non par un chemin d'accès actuel à un produit DALL-E 2.

## Comment l'utiliser {#how-to-use-this}

Au 2022-06-22, nous constatons l'entrée de DALL-E 2 dans un usage éditorial commercial. Nous n'inférons pas de politique officielle de prix ou de licence à partir du rapport utilisateur non vérifié du 2022-06-30.

1. Inventoriez les workflows hérités qui mentionnent `dall-e-2` ; n'envoyez plus de nouvelles requêtes à ce modèle, car OpenAI l'a retiré de l'API.
  — <https://developers.openai.com/api/docs/models/dall-e-2>
2. Pour la génération d'image unique à partir d'un prompt ou l'édition ponctuelle, migrez le workflow vers `gpt-image-2` via l'Image API.
  — <https://developers.openai.com/api/docs/guides/image-generation>
3. Pour l'édition d'image conversationnelle ou itérative, utilisez l'outil de génération d'images de la Responses API afin que les modifications conservent le contexte de l'image.
  — <https://developers.openai.com/api/docs/guides/image-generation>

## Bonnes pratiques {#best-practices}

- Traitez ceci comme une migration, et non comme un choix de modèle, car OpenAI recommande GPT-Image-2 pour la génération et l'édition d'images prises en charge.
  — <https://developers.openai.com/api/docs/models/dall-e-2>
- Utilisez l'Image API pour les tâches ponctuelles et la Responses API pour les flux éditables en plusieurs tours.
  — <https://developers.openai.com/api/docs/guides/image-generation>
- Dans le workflow de remplacement, rédigez des contraintes explicites, effectuez de petites itérations à changement unique et reformulez les détails inchangés afin que les images ne dérivent pas.
  — <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>
- Définissez délibérément la taille et la qualité de sortie : le guide de prompting considère les tailles de sortie supérieures à 2560×1440 comme expérimentales pour GPT-Image-2.
  — <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>

## Remplacé par ceci {#superseded-by-this}

- 2022-06-22 : considérer DALL-E 2 comme un choix disponible pour de nouveaux workflows éditoriaux commerciaux est obsolète, car OpenAI a retiré le modèle de l'API au 2026-09-04.
- 2022-06-30 : considérer l'enquête sur les prix ou une recherche de liste d'attente comme une voie d'accès à DALL-E 2 est obsolète ; les intégrations prises en charge doivent utiliser GPT-Image-2.

## Encore inconnu {#still-unknown}

- Nous n'avons pas pu récupérer l'enquête Reddit sur les prix du 2022-06-30 ; sa formulation, ses répondants, ses prix et son résultat commercial restent donc non vérifiés.
- Les deux fils de développement historiques semblent couvrir le même produit : adoption éditoriale et monétisation envisagée.
- Nous avons confirmé que le modèle a été retiré de l'API, mais nous n'avons pas vérifié si un accès front-end d'archive existe encore ; cela n'offre pas de voie d'intégration prise en charge.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://developers.openai.com/api/docs/models/dall-e-2 | Modèle DALL·E 2 | OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/models/gpt-image-2 | Modèle GPT-Image-2 | OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/image-generation | Génération d'images | OpenAI API | 2026-09-04 |
| https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide | Guide de prompting des modèles de génération d'images GPT | 2026-09-04 |
| https://www.cosmopolitan.com/lifestyle/a40314356/dall-e-2-artificial-intelligence-cover/ | DALL-E 2 réalise sa toute première couverture de magazine pour Cosmopolitan | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:dalle-2`, fil `dalle-2-commercial-adoption`, 1 événement daté du 2022-06-22 au 2022-06-22.
- **Note pratique :** Au 2022-06-22, les praticiens pouvaient constater l'entrée de DALL-E 2 dans un usage éditorial visible, mais ne doivent pas inférer de politique officielle de prix ou de licence à partir du rapport utilisateur non vérifié du 2022-06-30.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.

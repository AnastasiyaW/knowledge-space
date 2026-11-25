---
title: "Ideogram"
category: projects
date: 2025-07-31
tags: [ideogram, ideogram_3_0, model-and-product-releases, project]
aliases: ["Ideogram"]
level: 3
source_sha256: b5e23fb4486cb3f224942a11c8c94d19136378e6c39f6fc1ab65eeeb2a5939cb
translation: machine
translated_at: '2026-10-24'
---
# Ideogram {#ideogram}

**Ligne de développement :** `project:ideogram` · fil `model-and-product-releases`  
**Dernier événement :** 2025-07-31 · 3 événements datés depuis 2024-03-01 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Ideogram est une plateforme de génération d'images destinée aux designers, aux équipes de contenu et aux développeurs qui ont besoin de texte lisible, d'un contrôle de la composition et de modifications itératives.

- Ideogram 4.0 : génération en 2K, contrôle de la mise en page, éléments modifiables et poids ouverts.
- Web et API : génération, Remix, inpainting, manipulation de l'arrière-plan et des objets, upscaling et Custom Models.

L'API hébergée pour la version 4.0 affiche 0,03 $ / 0,06 $ / 0,10 $ par image selon les niveaux Turbo / Default / Quality. Elle convient aux ressources graphiques qui nécessitent des corrections, des changements d'échelle et des révisions, plutôt qu'à une génération à partir d'un seul prompt.

## Ligne de développement {#development-line}

- **2024-03-01 — Ideogram annonce Ideogram 1.0.** Modèle public de texte vers image, axé sur la typographie dans les images, le respect du prompt et Magic Prompt ; la page officielle de sortie est datée du 2024-02-28.
- **2025-03-26 — Ideogram annonce Ideogram 3.0.** Style Reference avec jusqu'à trois images, Style Code pour réappliquer les styles, Batch Generation, et meilleure gestion du texte graphique et de la mise en page.
- **2025-07-31 — Ideogram publie la page de sa fonctionnalité Character.** Une image de référence pour préserver l'identité d'un personnage d'une scène à l'autre ; le masquage, Magic Fill et Remix rejoignent le flux de travail Character.

## Évolutions {#what-changed}

- 2024-03-01 — Ideogram 1.0 : modèle public de texte vers image axé sur la typographie dans les images, le respect du prompt et Magic Prompt ; la page officielle de sortie est datée du 2024-02-28.
- 2024-08-21 — Ideogram 2.0 : ajout des styles Realistic, Design, 3D et Anime, du contrôle de palette, d'une application iOS, d'une API en bêta et de la recherche publique d'images.
- 2025-03-26 — Ideogram 3.0 : Style Reference avec jusqu'à trois images, Style Code pour réappliquer les styles, Batch Generation, et meilleure gestion du texte graphique et de la mise en page.
- 2025-07-31 — Ideogram Character : une image de référence pour préserver l'identité d'un personnage d'une scène à l'autre ; le masquage, Magic Fill et Remix rejoignent le flux de travail Character.
- 2026-06-03 — Ideogram 4.0 fait passer la ligne active à un modèle à poids ouverts, avec des descriptions de scène en JSON, un contrôle de palette et des boîtes englobantes optionnelles.
- 2026-06-18 — La documentation officielle confirme que les anciens prompts en texte libre peuvent se comporter différemment en 4.0 ; le JSON structuré est requis pour une couleur, un texte et une mise en page exacts.

## Mode d'emploi {#how-to-use-this}

Au 2025-07-31, les praticiens doivent consulter le flux de travail Character actuel d'Ideogram lorsqu'ils évaluent ses options de génération d'images ; les liens datés fournis établissent les jalons de versions et une section produit Character, mais pas les détails de mise en œuvre.

1. Ouvrez Ideogram, connectez-vous et commencez dans Creative avec Ideogram 4.0 ; Studio et les outils utilitaires y sont également disponibles.
  — <https://ideogram.ai/>
2. Pour un premier concept, décrivez la scène en texte naturel détaillé : Magic Prompt en direct d'Ideogram 4.0 transforme automatiquement le texte simple en description structurée.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
3. Si la couleur, la composition ou la typographie doivent être exactes, utilisez du JSON avec high_level_description, style_description, background et elements ; précisez le texte littéral et bbox pour les lettrages.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
4. Après un bon résultat, enregistrez style_code et seed : le premier verrouille le style visuel, le second permet des variations contrôlées de composition.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
5. Pour une série avec un sujet constant, ouvrez Character, importez un portrait net, décrivez la scène, puis ajustez le masque, Magic Fill ou Remix selon les besoins.
  — <https://ideogram.ai/features/character/>
6. Pour une intégration produit, configurez une clé API et appelez POST /v1/ideogram-v4/generate ; la référence Character dans le guide de démarrage actuel s'exécute comme un appel v3 distinct.
  — <https://developer.ideogram.ai/ideogram-api/api-overview>

## Bonnes pratiques {#best-practices}

- En 4.0, remplacez les descriptions d'ambiance vagues par des précisions : source de lumière, technique, palette, objets et leur disposition.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Suivez le cycle suivant : texte simple pour explorer les idées, style_code pour verrouiller un style réussi, et JSON pour les exigences strictes de marque.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Placez le lettrage demandé entre guillemets doubles, limitez chaque extrait de texte à 5–7 mots, et choisissez le niveau Quality pour une typographie où les erreurs sont critiques.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Ne bâtissez pas de flux de production sur Random Style : la documentation le marque comme obsolète ; utilisez un Style Code enregistré ou une Style Reference personnalisée pour des résultats reproductibles.
  — <https://docs.ideogram.ai/using-ideogram/generation-settings/styles>
- Pour Character, utilisez un portrait net et bien éclairé, de face ou en trois quarts, et ajustez le masque pour conserver ou remplacer les cheveux, les vêtements et les accessoires.
  — <https://ideogram.ai/features/character/>

## Remplacé par ce qui suit {#superseded-by-this}

- 2024-03-01 — considérer Ideogram 1.0 comme le modèle phare actif est obsolète : la ligne actuelle est Ideogram 4.0.
- 2025-03-26 — parcourir les styles via Random ou les « 4.3 billion presets » est obsolète : la documentation actuelle marque le mode Random comme déprécié.
- 2025-03-26 — s'appuyer sur de longs prompts en texte libre pour une typographie et une mise en page exactes est obsolète dans Ideogram 4.0 : une sortie stricte exige du JSON structuré, des éléments de texte et des boîtes englobantes.

## Points encore inconnus {#still-unknown}

- L'entrée du 2024-08-21 ne contient que l'URL de la page d'accueil : la page officielle de sortie confirme la date et le contenu d'Ideogram 2.0, mais la formulation d'origine de l'entrée n'est pas disponible.
- Les anciennes URL officielles /1.0, /2.0 et /3.0 redirigent désormais vers de nouvelles pages ; la vérification à long terme des affirmations historiques nécessite des captures d'archives distinctes.
- La documentation actuelle de l'API décrit la génération de base avec v4, alors que l'exemple de référence Character utilise encore v3 ; la documentation publique ne confirme pas l'existence d'un point d'accès v4 dédié à Character.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://about.ideogram.ai/1.0 | Ideogram 1.0, Feb 2024 | 2026-09-04 |
| https://about.ideogram.ai/2.0 | Ideogram 2.0 | 2026-09-04 |
| https://about.ideogram.ai/3.0 | Ideogram 3.0 | 2026-09-04 |
| https://about.ideogram.ai/character | Ideogram Character | 2026-09-04 |
| https://ideogram.ai/ | Ideogram | AI apps and models in one platform | 2026-09-04 |
| https://ideogram.ai/models/3.0/ | Ideogram 3.0 — Realism, design, and consistent styles | 2026-09-04 |
| https://ideogram.ai/models/4.0/ | Ideogram 4.0 | Ideogram | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technical Details: Open model at the forefront of design | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4-json-prompting/ | How to JSON prompt for Ideogram 4.0 | 2026-09-04 |
| https://ideogram.ai/features/character/ | Character Consistency from One Photo: Free AI Headshot Generator | Ideogram | 2026-09-04 |
| https://docs.ideogram.ai/using-ideogram/generation-settings/styles | Style Reference | Ideogram | 2026-09-04 |
| https://developer.ideogram.ai/ideogram-api/api-overview | API Overview | Ideogram | Documentation | 2026-09-04 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:ideogram`, fil `model-and-product-releases`, 3 événements datés du 2024-03-01 au 2025-07-31.
- **Note pratique :** Au 2025-07-31, les praticiens doivent consulter le flux de travail Character actuel d'Ideogram lorsqu'ils évaluent ses options de génération d'images ; les liens datés fournis établissent les jalons de versions et une section produit Character, mais pas les détails de mise en œuvre.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour déterminer ce qui est obsolète.

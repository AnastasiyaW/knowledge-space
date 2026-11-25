---
title: "Ideogram"
category: projects
tags: [ideogram, ideogram_3_0, model-and-product-releases, project]
aliases: ["Ideogram"]
level: 3
source_sha256: 4b19c1dc95877f9796f35755807757307dbf9dce9b06d99ebebcca8acbf049b1
translation: machine
translated_at: '2026-10-24'
---
# Ideogram {#ideogram}

**Ligne de développement :** `project:ideogram` · fil `model-and-product-releases`  
**Événements :** 3 datés, 2024-03-01 → 2025-07-31 · **Recherché le :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

Ideogram est une plateforme de génération d'images destinée aux designers, aux équipes de contenu et aux développeurs qui ont besoin d'un texte lisible, d'un contrôle de la composition et d'une édition itérative.

- Ideogram 4.0 : génération en 2K, contrôle de la mise en page, éléments modifiables et poids ouverts.
- Web et API : génération, Remix, inpaint, édition de l'arrière-plan et des objets, upscale et Custom Models.

Le tarif de l'API hébergée pour la 4.0 est de 0,03 $ / 0,06 $ / 0,10 $ par image pour les niveaux Turbo, Default et Quality. Choisissez Ideogram pour des visuels de design qui doivent être corrigés, reproduits et édités, plutôt que pour une génération à partir d'un seul prompt.

## Ligne de développement {#development-line}

- **2024-03-01 — Ideogram annonce Ideogram 1.0.** Modèle public de génération texte-image axé sur le texte dans les images, le respect du prompt et Magic Prompt ; la page officielle de sortie est datée du 2024-02-28.
- **2025-03-26 — Ideogram annonce Ideogram 3.0.** Style Reference prend en charge jusqu'à trois images, Style Code réapplique des styles, Batch Generation arrive, avec une gestion améliorée du texte graphique et de la mise en page.
- **2025-07-31 — Ideogram publie sa page de fonctionnalité Character.** Une seule référence préserve l'identité du personnage d'une scène à l'autre ; le masquage, Magic Fill et Remix sont intégrés au flux de travail des personnages.

## Ce qui a changé {#what-changed}

- **2024-03-01 — Ideogram 1.0 :** modèle public de génération texte-image axé sur le texte dans les images, le respect du prompt et Magic Prompt ; la page officielle de sortie est datée du 2024-02-28.
- **2024-08-21 — Ideogram 2.0 :** ajout des modes Realistic, Design, 3D et Anime, du contrôle de palette, d'une application iOS, d'une API bêta et de la recherche publique d'images ; confirmé sur la page officielle de sortie.
- **2025-03-26 — Ideogram 3.0 :** Style Reference avec jusqu'à trois images, Style Code pour réutiliser des styles, Batch Generation, et gestion renforcée du texte graphique et de la mise en page.
- **2025-07-31 — Ideogram Character :** une seule image de référence préserve l'identité du personnage d'une scène à l'autre ; le masquage, Magic Fill et Remix font désormais partie du flux de travail des personnages.
- **2026-06-03 :** Ideogram 4.0 a fait passer la ligne active vers un modèle à poids ouverts, avec descriptions de scène en JSON, palettes de couleurs et boîtes englobantes facultatives.
- **2026-06-18 :** le guide officiel confirme que les anciens prompts en texte libre peuvent se comporter différemment avec la 4.0 ; une couleur, un texte et un placement précis exigent du JSON structuré.

## Comment l'utiliser {#how-to-use-this}

Au 2025-07-31, les praticiens doivent vérifier le flux de travail Character actuel d'Ideogram lorsqu'ils évaluent ses options de génération d'images ; les liens datés fournis établissent les jalons de version et une zone produit Character, mais pas les détails de mise en œuvre.

1. Ouvrez Ideogram, connectez-vous et commencez dans Creative avec Ideogram 4.0 ; Studio et les outils utilitaires se trouvent dans la même interface.
  — <https://ideogram.ai/>
2. Décrivez la scène en texte simple pour le concept initial ; la version en ligne d'Ideogram 4.0 utilise Magic Prompt pour transformer le texte simple en une description structurée.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
3. Utilisez du JSON avec high_level_description, style_description, background et elements pour une couleur, une composition ou un texte précis ; indiquez le texte littéral et la bbox pour les lettrages.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
4. Enregistrez le style_code et le seed après un bon résultat : style_code verrouille le style visuel, tandis que seed permet des variations de composition contrôlées.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
5. Pour une série avec le même personnage, ouvrez Character, importez un portrait net, décrivez la scène, puis ajustez le masque, Magic Fill ou Remix selon les besoins.
  — <https://ideogram.ai/features/character/>
6. Pour une intégration produit, configurez une clé d'API et appelez POST /v1/ideogram-v4/generate ; le guide de démarrage actuel présente la référence Character comme un appel v3 distinct.
  — <https://developer.ideogram.ai/ideogram-api/api-overview>

## Bonnes pratiques {#best-practices}

- Avec la 4.0, remplacez les termes d'ambiance vagues par des détails concrets : source de lumière, support, palette, objets et placement dans l'espace.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Suivez le cycle : texte simple pour la recherche du concept initial, style_code pour figer un rendu, JSON pour les exigences de marque précises.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Placez le lettrage demandé entre guillemets doubles, limitez chaque extrait à environ 5 à 7 mots, et sélectionnez Quality pour une typographie sensible aux erreurs.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Ne bâtissez pas de flux de travail actuels sur Random Style, car Ideogram l'a marqué comme obsolète ; utilisez plutôt des codes de style enregistrés ou une Style Reference personnalisée.
  — <https://docs.ideogram.ai/using-ideogram/generation-settings/styles>
- Pour Character, utilisez un portrait net et bien éclairé, de face ou de trois quarts, et modifiez le masque pour conserver ou remplacer les cheveux, les vêtements ou les accessoires.
  — <https://ideogram.ai/features/character/>

## Remplacé par ceci {#superseded-by-this}

- 2024-03-01 — Considérer Ideogram 1.0 comme le modèle principal actif est obsolète ; la version actuelle est Ideogram 4.0.
- 2025-03-26 — Trouver des styles via le mode Random et ses 4,3 milliards de préréglages est obsolète ; la documentation actuelle marque le mode Random comme déprécié.
- 2025-03-26 — S'appuyer sur de longs prompts en texte libre pour obtenir un texte et une mise en page précis est obsolète pour Ideogram 4.0 ; des résultats stricts exigent du JSON structuré, des éléments de texte et une bbox.

## Toujours inconnu {#still-unknown}

- L'entrée du 2024-08-21 ne contient que l'adresse de la page d'accueil principale ; la page officielle de sortie confirme la date et le contenu d'Ideogram 2.0, mais le texte original de l'annonce n'est pas disponible.
- Les anciennes URL officielles /1.0, /2.0 et /3.0 redirigent désormais vers de nouvelles pages ; la conservation à long terme des affirmations historiques nécessite des instantanés archivés distincts.
- L'API actuelle présente la génération standard sur v4, alors que l'exemple de référence Character utilise encore v3 ; la documentation publique ne confirme pas l'existence d'un point d'accès v4 dédié à Character.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://about.ideogram.ai/1.0 | Ideogram 1.0, février 2024 | 2026-09-04 |
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

## Fiche pour l'agent {#agent-brief}

- **Sujet :** `project:ideogram`, fil `model-and-product-releases`, 3 événements datés du 2024-03-01 au 2025-07-31.
- **Remarque pratique :** Au 2025-07-31, les praticiens doivent vérifier le flux de travail Character actuel d'Ideogram lorsqu'ils évaluent ses options de génération d'images ; les liens datés fournis établissent les jalons de version et une zone produit Character, mais pas les détails de mise en œuvre.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

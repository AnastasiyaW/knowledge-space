---
title: "Roblox"
category: organizations
date: 2026-02-05
tags: [model_releases, organization, roblox, roblox-ai, roblox-ai-creation]
aliases: ["Roblox"]
level: 2
source_sha256: d3b73c7600218dfd36b3e274e4dc3066248989fa0262e0d6f47076969f50d0fa
translation: machine
translated_at: '2026-10-24'
---
# Roblox {#roblox}

**Ligne de développement :** `organization:roblox` · fil `roblox-ai-creation`  
**Dernier événement :** 2026-02-05 · 2 événements datés depuis 2023-02-18 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Roblox est une plateforme de jeux et Roblox Studio pour les développeurs. Dans cette ligne, Cube fournit : un Cube 3D v0.5 local pour générer des fichiers OBJ à partir de texte ; GenerationService pour un Body1 statique ou un Car5 composite directement dans l'expérience ; CubePart pour des parties nommées destinées au code de jeu. L'inférence rapide locale nécessite 24 Go de VRAM, l'inférence standard 16 Go. La génération 4D reste en beta, et les documents actuels décrivent explicitement Car5 et Body1. Conclusion : utilisez GenerationService pour des objets Roblox dont le schéma est conçu à l'avance, et Cube 3D v0.5 pour des prototypes locaux, et non pour un générateur de scènes arbitraires promis mais pas encore démontré.

## Ligne de développement {#development-line}

- **2023-02-18 — Wired fait état de la direction de Roblox en matière d'IA générative.** Le 2023-02-18, Wired a publié un article reliant Roblox à l'IA générative et à son univers de jeux. La source datée et liée marque une première étape publique dans la direction de développement de l'IA générative chez Roblox, bien que les éléments fournis n'établissent pas de produit ou de capacité spécifique livrée.
- **2026-02-05 — Roblox renforce la création avec le modèle de fondation Cube.** Le schéma définit les parties, et les scripts s'adaptent à leur taille et à leur forme.

## Évolutions {#what-changed}

2023-02-18 — Roblox a testé la saisie en langage naturel pour créer et modifier le code, l'apparence et le comportement d'objets de jeu ; il s'agissait d'une ligne expérimentale précoce. 2025-03-17 — Roblox a présenté et ouvert Cube 3D v0.1 : un modèle et un code de démarrage pour le text-to-shape, ainsi qu'un Mesh Generation en beta dans Studio et une API Lua. 2025-07 (trouvé aujourd'hui) — Cube 3D v0.5 est devenu la valeur par défaut actuelle du dépôt : la correspondance au texte et le contrôle de la bounding box ont été améliorés. 2026-02-05 — La beta de la génération 4D a déplacé l'accent d'un maillage statique vers un modèle fonctionnel multi-composants : le schéma définit les parties, et les scripts s'adaptent à leur taille et à leur forme. 2026-05-28 (trouvé aujourd'hui) — CubePart a ajouté la génération et la segmentation de parties nommées à partir d'un schéma ouvert défini par l'utilisateur ; l'accès direct dans Studio est encore annoncé comme futur.

## Mode d'emploi {#how-to-use-this}

À la date du 2026-02-05, les praticiens qui évaluent les outils de création Roblox devraient traiter Roblox Cube comme une voie de modèle de fondation documentée séparément, et consulter les ressources officielles, GitHub et Hugging Face liées pour les modalités d'accès et d'utilisation actuelles.

1. Pour un objet dans Roblox, utilisez `GenerationService:GenerateModelAsync` avec `TextPrompt` et un schéma ; commencez par `Car5` ou `Body1`, documentés.
  — <https://create.roblox.com/docs/reference/engine/classes/GenerationService>
2. Traitez le résultat avec `pcall`, puis mettez à l'échelle et positionnez le modèle, fixez ses parties, et seulement ensuite connectez le comportement de jeu.
  — <https://create.roblox.com/docs/reference/engine/classes/GenerationService>
3. Pour la génération locale text-to-3D, clonez `Roblox/cube`, installez les dépendances dans un environnement virtuel, téléchargez les poids `Roblox/cube3d-v0.5` et lancez `cube3d.generate` ; le résultat est enregistré au format OBJ.
  — <https://github.com/Roblox/cube>
4. Si l'objet doit respecter un encombrement donné, passez `--bounding-box-xyz` ; pour vérifier le rendu visuel, utilisez les exemples du dépôt ou un rendu turntable.
  — <https://github.com/Roblox/cube>

## Bonnes pratiques {#best-practices}

- Concevez d'abord le schéma à partir des noms de parties dont dépend le code de jeu ; pour une voiture, il s'agit de la carrosserie et des roues séparées, et non d'un maillage monolithique.
  — <https://about.roblox.com/newsroom/2026/05/cubepart-roblox-open-vocabulary-part-controllable-3d-generator>
- Commencez les nouvelles intégrations locales avec Cube 3D v0.5, et réservez v0.1 à la reproduction d'anciens résultats.
  — <https://github.com/Roblox/cube>
- Prévoyez au minimum 16 Go de VRAM, ou 24 Go pour `--fast-inference` ; en cas de décodage lent, réduisez `resolution-base` dans la plage 4.0–9.0.
  — <https://github.com/Roblox/cube>
- Ne définissez pas de bounding box extrêmes sans vérification : v0.5 peut produire des composants disjoints ou diagonaux.
  — <https://github.com/Roblox/cube>
- Ne publiez pas un résultat CubePart sans vérifier les intersections et les relations spatiales entre parties : Roblox indique explicitement que le chevauchement et la distinction des directions nécessitent encore des améliorations.
  — <https://about.roblox.com/newsroom/2026/05/cubepart-roblox-open-vocabulary-part-controllable-3d-generator>

## Éléments rendus obsolètes {#superseded-by-this}

- 2023-02-18 — Se baser sur l'expérience précoce de génération de code et d'objets en langage naturel comme contrat de travail est obsolète ; elle a été remplacée par les Cube et GenerationService documentés.
- 2025-03-17 — Utiliser Cube 3D v0.1 comme valeur par défaut actuelle est obsolète depuis la sortie de Cube 3D v0.5 en juillet 2025.
- 2025-03-17 — Supposer uniquement un flux de travail statique à maillage unique est obsolète pour l'intégration Roblox : la beta 4D a ajouté Car5 et Body1, mais n'a pas démontré un flux général à schéma arbitraire.
- 2026-09-04 — `GenerationService:GenerateMeshAsync` est marqué comme déprécié ; une nouvelle intégration doit utiliser `GenerateModelAsync`.

## Points non élucidés {#still-unknown}

- La génération 4D est indiquée comme beta ; les sources actuelles ne confirment pas la disponibilité par région, par compte, les quotas ou le coût pour une expérience donnée.
- La fonction AI Assistant au niveau de l'entreprise et la ligne d'API de modèles Cube sont liées, mais cela ne constitue pas la liste complète des fonctions d'IA de Roblox ; les étapes pratiques ci-dessus ne concernent que Cube, CubePart et GenerationService.
- CubePart est présenté comme une future fonction de Roblox Studio, mais les sources trouvées ne donnent pas de date de sortie publique dans Studio ni d'API Studio dédiée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.wired.com/story/roblox-generative-ai-gaming-universe/ | Roblox Is Bringing Generative AI to Its Gaming Universe | WIRED | 2026-09-04 |
| https://about.roblox.com/newsroom/2025/03/introducing-roblox-cube | Introducing Roblox Cube: Our Core Generative AI System for 3D and 4D | Roblox | 2026-09-04 |
| https://about.roblox.com/newsroom/2026/02/accelerating-creation-powered-roblox-cube-foundation-model | Accelerating Creation, Powered by Roblox’s Cube Foundation Model | Roblox | 2026-09-04 |
| https://github.com/Roblox/cube | Cube: Generative AI System for 3D | 2026-09-04 |
| https://huggingface.co/Roblox/cube3d-v0.1 | Roblox/cube3d-v0.1 · Hugging Face | 2026-09-04 |
| https://about.roblox.com/newsroom/2026/05/cubepart-roblox-open-vocabulary-part-controllable-3d-generator | CubePart: An Open-Vocabulary Part-Controllable 3D Generator | Roblox | 2026-09-04 |
| https://create.roblox.com/docs/reference/engine/classes/GenerationService | GenerationService | Documentation - Roblox Creator Hub | 2026-09-04 |
| https://create.roblox.com/docs/zh-cn/parts/model-generation | Génération de modèles | Documentation - Hub de créateurs Roblox | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `organization:roblox`, fil `roblox-ai-creation`, 2 événements datés du 2023-02-18 au 2026-02-05.
- **Note pratique :** À la date du 2026-02-05, les praticiens qui évaluent les outils de création Roblox devraient traiter Roblox Cube comme une voie de modèle de fondation documentée séparément, et consulter les ressources officielles, GitHub et Hugging Face liées pour les modalités d'accès et d'utilisation actuelles.
- **Confiance :** élevée. Les éléments obsolètes datés ci-dessus font autorité pour déterminer ce qui est périmé.

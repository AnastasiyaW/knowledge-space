---
title: "Vibe Coding XR"
category: projects
date: 2026-03-26
tags: [project, vibe-coding-xr, vibe-coding-xr-launch]
aliases: ["Vibe Coding XR"]
level: 3
source_sha256: 53f3e62a38eab191eb92092d537d0cf504c50a82b1afe8011bf193512a7d1d56
translation: machine
translated_at: '2026-10-24'
---
# Vibe Coding XR {#vibe-coding-xr}

**Ligne de développement :** `project:vibe-coding-xr` · fil `vibe-coding-xr-launch`  
**Dernier événement :** 2026-03-26 · 1 événement daté depuis le 2026-03-26 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Vibe Coding XR est un workflow assisté par Gemini destiné aux designers et développeurs qui ont besoin d'un prototype WebXR avant de s'engager sur Unity ou Unreal. Il associe le Gem XR Blocks hébergé à la bibliothèque open source XR Blocks.

- Brief textuel ou vocal vers une scène WebXR interactive et sensible à la physique.
- Itération dans une réalité simulée sur ordinateur, puis déploiement direct sur Android XR.
- Entrée par les mains, perception de la pièce, interface spatiale, intégration de l'IA et chemin SDK pour le code personnalisé.

Le SDK cible Chrome v136+. Le Gem hébergé reste en bêta. Les taux de réussite publiés mesurent une exécution headless sans erreur, et non l'utilisabilité sur casque ou la fidélité des interactions.

Utilisez-le pour valider rapidement des interactions spatiales et des concepts de produit. Testez ensuite l'application générée sur le matériel cible, puis renforcez-la comme du code WebXR classique.

## Ligne de développement {#development-line}

- **2026-03-26 — Vibe Coding XR a été présenté avec XR Blocks et une ressource Gemini.** Brief en langage naturel vers une scène WebXR générée, simulation sur ordinateur, puis déploiement sur Android XR.

## Évolutions {#what-changed}

- 2025-10-09 — XR Blocks a été lancé comme fondation WebXR ouverte, avec un Reality Model sémantique pour les utilisateurs, les environnements physiques, les interfaces, l'IA et les agents.
- 2026-03-26 — Vibe Coding XR a transformé cette fondation en workflow Gemini/Gem XR Blocks : brief en langage naturel vers une scène WebXR générée, simulation sur ordinateur, puis déploiement sur Android XR.
- 2026-05-13 — XR Blocks v0.14.1 a livré une version corrective du Gem XR Blocks pour Gemini Canvas, incluant des correctifs du focus de saisie et du redimensionnement dans le simulateur.
- 2026-06-30 — XR Blocks v0.17.0 a ajouté le contrôle incarné et à distance, les tests fonctionnels headless et une perception embarquée étendue.
- 2026-07-17 — XR Blocks v0.18.0 a ajouté les mains d'agent, les gestes de la tête, un contexte de scène structuré pour les LLM et la navigation dans le simulateur.
- 2026-08-25 — XR Blocks v0.21.0 a amélioré les ancres Android XR et la robustesse des sessions WebXR, ajouté la perception par webcam sur ordinateur, et modifié l'endpoint Flash par défaut du SDK pour gemini-3.7-flash ; la v0.21.1 a suivi le même jour comme dernier correctif.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-26, évaluez XR Blocks avec la ressource Gemini associée lorsque vous explorez le prototypage XR assisté par l'IA. Considérez les détails de capacité et de disponibilité comme non vérifiés tant que les documents sources n'ont pas été examinés.

1. Ouvrez le Gem XR Blocks dans Chrome sur ordinateur ou sur un casque Android XR, puis décrivez la scène visée, les objets, la disposition spatiale et les interactions, en langage naturel ou à la voix.
  — <https://research.google/blog/vibe-coding-xr-accelerating-ai-xr-prototyping-with-xr-blocks-and-gemini/>
2. Prévisualisez l'application générée dans l'environnement de réalité simulée sur ordinateur, puis affinez le prompt ou le code avant de vous appuyer sur le matériel du casque.
  — <https://research.google/blog/vibe-coding-xr-accelerating-ai-xr-prototyping-with-xr-blocks-and-gemini/>
3. Sur Android XR, sélectionnez Enter XR et vérifiez le comportement de la main, du pincement, de la perception et de la physique dans l'environnement physique visé.
  — <https://research.google/blog/vibe-coding-xr-accelerating-ai-xr-prototyping-with-xr-blocks-and-gemini/>
4. Pour une application personnalisée, clonez XR Blocks, exécutez `npm ci`, puis utilisez `npm run serve` pour les exemples ou `npm run dev` pour le mode surveillance du SDK et le serveur local.
  — <https://github.com/google/xrblocks/blob/main/README.md>
5. Lorsque vous ajoutez des fonctionnalités Gemini cloud à une application XR Blocks personnalisée, obtenez une clé API et protégez-la ; les exemples non liés à l'IA n'en nécessitent pas.
  — <https://github.com/google/xrblocks/blob/main/README.md>

## Bonnes pratiques {#best-practices}

- Utilisez le Pro Mode pour les travaux avancés de perception, d'animation et d'interaction par la main, puis vérifiez le résultat. Lors de l'évaluation de mars, gemini-3.1-pro High a atteint 95,5 % de pass@1, contre 87,8 % pour gemini-3-flash High. Ces résultats concernent des modèles en préversion et ne garantissent pas le comportement actuel du Gem hébergé.
  — <https://arxiv.org/pdf/2603.24591>
- Intégrez dans le prompt l'échelle de la pièce, les proportions à taille humaine, les distances d'interaction, les gestes d'entrée et le comportement attendu, plutôt que de demander une scène générique.
  — <https://research.google/blog/vibe-coding-xr-accelerating-ai-xr-prototyping-with-xr-blocks-and-gemini/>
- Utilisez le simulateur sur ordinateur pour les itérations rapides, mais testez la version finale candidate sur un appareil Android XR. La détection de profondeur, l'interaction par la main et la physique s'évaluent au mieux sur le matériel.
  — <https://research.google/blog/vibe-coding-xr-accelerating-ai-xr-prototyping-with-xr-blocks-and-gemini/>
- Considérez une exécution headless sans erreur comme un critère de viabilité du code, et non comme une preuve d'utilisabilité, de qualité visuelle ou de fidélité des interactions.
  — <https://arxiv.org/pdf/2603.24591>
- Prévoyez les autorisations de caméra, de suivi des mains et WebXR. Le traitement des capteurs reste sur l'appareil pour les chemins WebXR et LiteRT documentés, tandis que les fonctionnalités IA de Gemini envoient des données aux services Gemini.
  — <https://github.com/google/xrblocks/blob/main/README.md>

## Remplacé par {#superseded-by-this}

- 2026-08-25 — Considérer le Gem XR Blocks v0.11.0 et son benchmark de mars sur modèles en préversion comme référence actuelle du SDK est obsolète ; le SDK public est passé à la v0.21.1.
- 2026-08-25 — Supposer que gemini-3-flash est l'endpoint Flash par défaut du SDK est obsolète ; la v0.21.0 a modifié ce défaut pour gemini-3.7-flash.

## Points encore inconnus {#still-unknown}

- L'URL Gemini partagée fournie, https://gemini.google.com/gem/71ee80f488a4?usp=sharing, n'a renvoyé aucun contenu public lisible lors de la vérification. Ses conditions d'accès, sa disponibilité et son lien avec le Gem XR Blocks en bêta restent non vérifiés.
- Les métriques de gemini-3.1-pro et gemini-3-flash figurant dans l'article proviennent de modèles en préversion de mars 2026. La page d'accueil publique n'a pas exposé la correspondance actuelle des modèles du Gem hébergé.
- Aucun benchmark de bout en bout de la v0.21.x comparable à VCXR60 n'a été trouvé. Les nouvelles fonctionnalités du SDK n'établissent pas d'amélioration mesurée par rapport à la référence de recherche v0.11.0.
- Nous n'avons exécuté aucune application générée sur un ordinateur local ni sur un casque Android XR au cours de cette recherche.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://research.google/blog/vibe-coding-xr-accelerating-ai-xr-prototyping-with-xr-blocks-and-gemini/ | Vibe Coding XR: Accelerating AI + XR prototyping with XR Blocks and Gemini | 2026-09-05 |
| https://arxiv.org/pdf/2603.24591 | Vibe Coding XR: Accelerating AI + XR Prototyping with XR Blocks and Gemini, arXiv PDF v2 | 2026-09-05 |
| https://github.com/google/xrblocks | Dépôt google/xrblocks | 2026-09-05 |
| https://github.com/google/xrblocks/blob/main/README.md | README de XR Blocks | 2026-09-05 |
| https://github.com/google/xrblocks/releases | Versions de XR Blocks | 2026-09-05 |
| https://research.google/blog/xr-blocks-accelerating-ai-xr-innovation/ | XR Blocks: Accelerating AI + XR innovation | 2026-09-05 |
| https://xrblocks.github.io/gem/ | Gem of XR Blocks for Gemini Canvas (beta) | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:vibe-coding-xr`, fil `vibe-coding-xr-launch`, 1 événement daté du 2026-03-26 au 2026-03-26.
- **Note pratique :** À partir du 2026-03-26, les praticiens doivent évaluer XR Blocks avec la ressource Gemini associée lorsqu'ils explorent le prototypage XR assisté par l'IA, en considérant les détails de capacité et de disponibilité comme non vérifiés tant que les documents sources n'ont pas été examinés.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

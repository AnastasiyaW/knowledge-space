---
title: "Apple — Apple AI : des publications de recherche aux capacités produit"
category: organizations
tags: [apple, apple-ai-research-to-product, apple_gaudi, apple_intelligence, open_source_release, organization]
aliases: ["Apple"]
level: 2
source_sha256: 39e133c36ad4a05d3879f19bbd549bd750d1264d2601271c88f0c4cea7b9b7e9
translation: machine
translated_at: '2026-10-24'
---
# Apple — Apple AI : des publications de recherche aux capacités produit {#apple-apple-ai-research-releases-to-product-capabilities}

**Ligne de développement :** `organization:apple` · fil `apple-ai-research-to-product`  
**Événements :** 3 datés, 2022-08-05 → 2026-06-09 · **Recherche effectuée :** 2026-09-03 · confiance : moyenne

## Ce que c'est {#what-it-is}

Apple est une entreprise de matériel et de plateformes logicielles dont la surface d'IA utilisable est Apple Intelligence, destinée aux personnes disposant de matériel Apple compatible, et Swift, destiné aux équipes qui créent des applications tenant compte du système. - Sur les appareils : fonctionnalités d'écriture, d'image, de recherche, de traduction, de notification et Shortcuts. - Dans les applications : Foundation Models pour la génération typée et l'utilisation d'outils ; App Intents pour Siri, Spotlight et Shortcuts. Limite : la prise en charge varie selon l'appareil, le système d'exploitation, la langue et la région ; les appareils iPhone, iPad, Mac et Vision Pro éligibles nécessitent 7 Go de stockage. Verdict : utiliser Apple Intelligence comme intégration de plateforme soumise à conditions ; considérer GAUDI et NeuMan comme du code de recherche distinct datant de 2022.

## Ligne de développement {#development-line}

- **2022-08-05 — Apple a publié le dépôt Gaudi de machine learning.** Le 2022-08-05, Apple a publié publiquement le dépôt ml-gaudi sur GitHub. Il s'agit d'une publication publique datée d'un projet de recherche en machine learning d'Apple, qui fait partie de l'historique de développement IA de l'organisation.
- **2022-08-17 — Apple a publié le dépôt Neuman de machine learning.** Le 2022-08-17, Apple a publié publiquement le dépôt ml-neuman sur GitHub. Il s'agit d'une publication distincte et datée de travaux de machine learning d'Apple, qui témoigne d'une activité de recherche IA publique continue.
- **2026-06-09 — Apple a annoncé de nouvelles capacités d'Apple Intelligence pour les expériences du quotidien.** Le 2026-06-09, Apple a annoncé des capacités d'Apple Intelligence destinées aux expériences du quotidien. La page Apple Newsroom associée et la vidéo qui l'accompagne en font une étape importante, orientée produit, dans l'historique de développement IA d'Apple.

## Ce qui a changé {#what-changed}

Ligne de développement Apple : - 2022-08-05 — GAUDI a rendu disponible du code de recherche Apple pour la génération de scènes 3D génératives représentées par des champs de radiance, avec conditionnement à partir de texte ou d'images RGB. Il s'agissait d'une implémentation de recherche, et non d'une API de plateforme. - 2022-08-17 — NeuMan a mis à disposition une implémentation de référence permettant de reconstruire un arrière-plan et une personne animable à partir d'une seule vidéo. Son environnement documenté (Python 3.7, PyTorch 1.8 et CUDA) en fait un flux de reproduction, et non un environnement d'exécution sur appareil Apple. - 2026-06-09 — La publication d'Apple du 8 juin a annoncé la prochaine architecture d'Apple Intelligence, avec de nouvelles fonctionnalités système et la construction de raccourcis Shortcuts en langage naturel. La publication décrivait les fonctionnalités de l'ère iOS 27 comme étant en test développeur, en bêta publique ou disponibles à l'automne, et non comme un déploiement mondial achevé. - Constat du jour (2026-09-03) — La voie développeur actuelle d'Apple repose sur Foundation Models et App Intents ; le support Apple documente les conditions matérielles, de stockage, linguistiques et régionales qui conditionnent la disponibilité des fonctionnalités.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-09, les praticiens qui suivent Apple doivent distinguer ses publications publiques de recherche en machine learning de ses annonces d'Apple Intelligence orientées produit, tout en considérant les deux comme des éléments de preuve liés de l'activité IA de l'entreprise.

1. Vérifiez le matériel, le système d'exploitation, l'espace de stockage libre, la langue de l'appareil et de Siri, ainsi que la disponibilité régionale. Mettez à jour l'appareil, activez Apple Intelligence dans Réglages > Apple Intelligence et Siri, puis laissez-le connecté au Wi-Fi et sur secteur pendant le téléchargement des modèles sur l'appareil.
  — <https://support.apple.com/en-ie/121115>
2. Pour une application Swift, commencez par Foundation Models lorsque la fonctionnalité nécessite une génération de langage ou multimodale, une sortie structurée ou des appels d'outils ; choisissez le modèle ou le fournisseur adapté à la tâche plutôt que de supposer qu'un modèle embarqué convient à toutes les charges de travail.
  — <https://developer.apple.com/apple-intelligence/>
3. Exposez les actions et le contenu de l'application via App Intents et les entités, afin qu'ils puissent être découverts par Siri, Spotlight et Shortcuts.
  — <https://developer.apple.com/apple-intelligence/>
4. Pour une automatisation personnelle, utilisez l'action Use Model de Shortcuts, choisissez un type de sortie que l'action suivante peut consommer, et testez l'ensemble du flux avec de véritables entités d'applications.
  — <https://developer.apple.com/videos/play/wwdc2025/260/>

## Bonnes pratiques {#best-practices}

- Conditionnez l'intégration et les parcours de fonctionnalités au matériel, au système d'exploitation, au stockage, à la langue et à la région réels ; ne présentez jamais une fonctionnalité non prise en charge comme disponible.
  — <https://support.apple.com/en-ie/121115>
- Utilisez la génération guidée pour les sorties typées, testez des prompts variés sur des échantillons représentatifs et évaluez les résultats avant de vous appuyer sur une fonctionnalité pilotée par un modèle.
  — <https://developer.apple.com/documentation/technologyoverviews/generative-models?changes=_2%2C_2>
- N'exposez aux flux de travail des modèles que les propriétés d'entités utiles, prévoyez des actions Find ou une indexation pour la découverte, et fournissez des résumés de paramètres et des suggestions pour Spotlight et Shortcuts.
  — <https://developer.apple.com/videos/play/wwdc2025/260/>
- Maintenez les capacités de juin 2026 derrière des vérifications de disponibilité : la publication d'Apple les qualifie de tests, de bêta ou de déploiement ultérieur dans l'année, et signale des variations selon la langue et la région.
  — <https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/>

## Remplacé par ceci {#superseded-by-this}

- 2022-08-05/2022-08-17 : GAUDI et NeuMan ne servent plus de référence pour intégrer une fonctionnalité IA sur la plateforme Apple. Foundation Models et App Intents constituent la voie actuelle ; les dépôts restent pertinents uniquement pour leurs problèmes distincts de recherche et de reproduction.
- Statut de l'aperçu du 2026-06-08 : l'hypothèse selon laquelle chaque fonctionnalité IA d'iOS 27 ou de Siri était généralement disponible est obsolète. L'annonce d'Apple qualifie les nouvelles fonctionnalités de tests, de bêta ou de disponibilité ultérieure dans l'année, et maintient des limites régionales et linguistiques.

## Points encore inconnus {#still-unknown}

- GAUDI, NeuMan et Apple Intelligence ne relèvent pas d'une filiation produit unique et documentée. Aucune source de première main consultée aujourd'hui ne relie l'un ou l'autre des dépôts de 2022 au produit ou au SDK Apple Intelligence.
- La page de juin 2026 décrit toujours les fonctionnalités de l'ère iOS 27 comme des tests, une bêta ou une disponibilité à l'automne à venir. Aucune note de version postérieure à l'annonce n'a été trouvée qui prouve que chaque fonctionnalité annoncée est active dans chaque région au 2026-09-03.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/apple/ml-gaudi | GAUDI: A Neural Architect for Immersive 3D Scene Generation — apple/ml-gaudi | 2026-09-03 |
| https://github.com/apple/ml-neuman | NeuMan: Neural Human Radiance Field from a Single Video — apple/ml-neuman | 2026-09-03 |
| https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/ | Apple Intelligence brings powerful AI capabilities into everyday experiences | 2026-09-03 |
| https://developer.apple.com/apple-intelligence/ | Apple Intelligence — Apple Developer | 2026-09-03 |
| https://support.apple.com/en-ie/121115 | How to get Apple Intelligence — Apple Support | 2026-09-03 |
| https://developer.apple.com/documentation/technologyoverviews/generative-models?changes=_2%2C_2 | Generative models and machine learning — Apple Developer Documentation | 2026-09-03 |
| https://developer.apple.com/videos/play/wwdc2025/260/ | Develop for Shortcuts and Spotlight with App Intents — WWDC25 | 2026-09-03 |

## Brief agent {#agent-brief}

- **Sujet :** `organization:apple`, fil `apple-ai-research-to-product`, 3 événements datés du 2022-08-05 au 2026-06-09.
- **Note pratique :** Au 2026-06-09, les praticiens qui suivent Apple doivent distinguer ses publications publiques de recherche en machine learning de ses annonces d'Apple Intelligence orientées produit, tout en considérant les deux comme des éléments de preuve liés de l'activité IA de l'entreprise.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.

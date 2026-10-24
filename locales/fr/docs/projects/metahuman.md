---
title: "MetaHuman"
category: projects
date: 2022-06-10
tags: [metahuman, metahuman-development-and-applications, metahuman_applications, project]
aliases: ["MetaHuman"]
level: 2
source_sha256: cfee1a85a578910e84b8296956887cca055e57d05bff12ebfdf9a655a4523309
translation: machine
translated_at: '2026-10-24'
---
# MetaHuman {#metahuman}

**Ligne de développement :** `project:metahuman` · fil `metahuman-development-and-applications`  
**Dernier événement :** 2022-06-10 · 1 événement daté depuis 2022-06-10 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

MetaHuman est un framework Unreal Engine destiné aux artistes de personnages, aux équipes de production virtuelle et aux développeurs de jeux vidéo.

- Création d'assets : construit des assets modifiables de visage, de corps, de cheveux, de vêtements et de matériaux.
- Conformation de maillage : ajuste des scans, des sculptures et d'autres maillages à un MetaHuman prêt pour l'animation.
- Assemblage pour la cible : empaquette les assets pour des cibles cinématographiques ou temps réel.

## Ligne de développement {#development-line}

- **2022-06-10 — La mise à jour MetaHuman a introduit l'import de tête personnalisée.** Nous suivons des repères sur un maillage facial personnalisé texturé et le faisons correspondre dans le cloud à la topologie de MetaHuman. Le système renvoie un personnage entièrement riggé. La version ajoutait 23 coiffures (grooms), dix boucles d'animation faciale, six poses corporelles, cinq poses faciales, et la compatibilité rigging et retargeting avec UE5.

## Ce qui a changé {#what-changed}

- **2022-06-10** — Mesh to MetaHuman a été lancé dans le plugin MetaHuman pour Unreal Engine. Nous suivons des repères sur un maillage facial personnalisé texturé et le faisons correspondre dans le cloud à la topologie de MetaHuman. Il renvoie un personnage entièrement riggé. La version ajoutait 23 coiffures (grooms), dix boucles d'animation faciale, six poses corporelles, cinq poses faciales, et la compatibilité rigging et retargeting avec UE5.
- **2022-06-21** — La vidéo liée ne peut actuellement être ni récupérée ni identifiée de manière fiable ; aucune affirmation de version n'est donc rattachée à cette date.
- **2023-06-15** — MetaHuman Animator a ajouté la résolution de performance faciale haute fidélité à partir d'une capture par iPhone ou par caméra stéréo montée sur casque.
- **2024-03-28** — MetaHuman est devenu disponible dans UEFN. Unreal Engine 5.4 a introduit la voie CLO/Marvelous Designer pour les vêtements dynamiques.
- **2025-06-03** — MetaHuman 5.6 a quitté l'Early Access et a déplacé Creator, Animator et Mesh to MetaHuman dans Unreal Engine. Il a ajouté des corps paramétriques, des Outfit Assets, l'animation en temps réel à partir de caméras ou d'audio compatibles, ainsi qu'une licence plus large.
- **2026-06-17** — MetaHuman 5.8 a ajouté Mesh to MetaHuman pour le corps entier, MetaHuman Crowds, ainsi que d'autres composants technologiques en open source.

## Comment l'utiliser {#how-to-use-this}

À partir du 2022-06-10, nous pouvons évaluer le workflow d'import de tête personnalisée de MetaHuman pour les humains numériques, au lieu de le considérer comme limité aux présets de personnages par défaut.

1. Installez Unreal Engine avec MetaHuman Creator Core Data, puis activez le plugin MetaHuman Creator dans le projet.
  — <https://dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-creator-in-unreal-engine>
2. Créez un asset MetaHuman Character dans le Content Browser, modifiez son visage, son corps et ses matériaux, puis assemblez-le pour la cible Unreal visée.
  — <https://dev.epicgames.com/documentation/metahuman/metahuman-creator-in-unreal-engine>
3. Pour un scan ou une sculpture, importez le maillage et créez une MetaHuman Identity. Suivez une pose neutre, lancez Identity Solve, puis riggez automatiquement ou conformez le résultat dans le workflow Creator intégré au moteur.
  — <https://dev.epicgames.com/documentation/metahuman/from-mesh>
4. Si vous voulez faire évoluer un personnage web plus ancien, utilisez le chemin Migrate ou Import and Migrate de Quixel Bridge plutôt que de continuer à le modifier comme un asset web hérité.
  — <https://dev.epicgames.com/documentation/metahuman/metahuman-creator-migration-guide-in-unreal-engine>

## Bonnes pratiques {#best-practices}

- Utilisez un FBX ou un OBJ texturé avec une sclérotique visible. Choisissez OBJ pour les maillages de plus de 200 000 sommets, car l'import FBX peut être beaucoup plus lent.
  — <https://dev.epicgames.com/documentation/metahuman/from-mesh>
- Utilisez une pose neutre de face, avec des traits du visage bien visibles. N'ajoutez des vues de profil que pour corriger des oreilles ou des narines mal ajustées.
  — <https://dev.epicgames.com/documentation/metahuman/from-mesh>
- Pour les réseaux restreints, ajoutez à la liste d'autorisation les endpoints S3 requis ainsi que les services de synthèse de texture et de rigging automatique d'Epic, avant de construire un workflow de production.
  — <https://dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-creator-in-unreal-engine>

## Remplacé par ceci {#superseded-by-this}

- 2022-06-09 — Le workflow centré sur l'application web de MetaHuman Creator en Early Access est obsolète pour les nouveaux projets UE 5.6+. Creator est intégré à Unreal Engine.
- 2025-06-03 — Mesh to MetaHuman ne crée plus de nouveau personnage dans l'application web MetaHuman Creator. Créez plutôt l'identité et conformez-la dans Unreal Engine.

## Toujours inconnu {#still-unknown}

- L'URL YouTube du 2022-06-21 n'a pas pu être récupérée ni rattachée à un titre, un auteur ou une date de publication. Son lien avec la chronologie de développement du produit MetaHuman n'est donc pas vérifié.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://www.fxguide.com/fxfeatured/huge-update-for-metahuman-import-your-own-head/ | Huge update for MetaHuman: import your own head! | 2026-09-05 |
| https://www.metahuman.com/news/new-release-brings-mesh-to-metahuman-to-unreal-engine-and-much-more | New release brings Mesh to MetaHuman to Unreal Engine, and much more! | 2026-09-05 |
| https://www.metahuman.com/news/delivering-high-quality-facial-animation-in-minutes-metahuman-animator-is-now-available?lang=en-US | Delivering high-quality facial animation in minutes, MetaHuman Animator is now available! | 2026-09-05 |
| https://www.metahuman.com/news/metahuman-comes-to-uefn-dynamic-clothing-with-marvelous-designer-and-more | MetaHuman comes to UEFN, dynamic clothing with Marvelous Designer and more | 2026-09-05 |
| https://www.metahuman.com/news/metahuman-leaves-early-access-with-a-feature-packed-new-release | MetaHuman leaves Early Access with a feature-packed new release | 2026-09-05 |
| https://forums.unrealengine.com/t/metahuman-5-8-released/2729288 | MetaHuman 5.8 Released! | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-creator-in-unreal-engine | Getting Started with MetaHuman Creator in Unreal Engine | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/metahuman-creator-in-unreal-engine | MetaHuman Creator in Unreal Engine | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/from-mesh | From Mesh | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/metahuman-creator-migration-guide-in-unreal-engine | MetaHuman Creator Migration Guide in Unreal Engine | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:metahuman`, fil `metahuman-development-and-applications`, 1 événement daté, du 2022-06-10 au 2022-06-10.
- **Note pratique :** À partir du 2022-06-10, nous pouvons évaluer le workflow d'import de tête personnalisée de MetaHuman lors de la planification de la création d'humains numériques, au lieu de le considérer comme limité à ses présets de personnages par défaut.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

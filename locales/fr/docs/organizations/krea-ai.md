---
title: "Krea AI — Génération de vidéo"
category: organizations
tags: [krea-ai, krea_ai, organization, video-generation]
aliases: ["Krea AI"]
level: 2
source_sha256: af9fbb456f5c8ef5ca6d2bcb02392b62b2f5843fd3d2b81581a8a1f580c6d183
translation: machine
translated_at: '2026-10-24'
---
# Krea AI — Génération de vidéo {#krea-ai-video-generation}

**Ligne de développement :** `organization:krea-ai` · fil `video-generation`  
**Événements :** 3 datés, 2025-04-16 → 2025-08-29 · **Recherche effectuée le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Krea AI est une boîte à outils dans le navigateur, destinée aux designers et aux équipes vidéo, qui permet de générer, modifier, améliorer et animer des images et des vidéos, ainsi que d'entraîner des styles réutilisables.

- **Image et Vidéo :** choisissez son propre modèle Krea 2 ou un modèle tiers selon la tâche.
- **Realtime :** utilisez un canevas avec génération en direct à partir d'un texte, d'un dessin, d'une webcam ou de l'écran.
- **Edit, Enhancer et Train :** effectuez des modifications locales, agrandissez des images et entraînez un LoRA pour un style, un personnage ou un produit.

La documentation d'un rendu vidéo standard indique 5 à 12 secondes, 1 à 10 minutes et à partir de 1 000 crédits de calcul.

Krea est un espace de travail permettant de comparer des modèles et d'itérer rapidement sur les visuels. Avant une tâche précise, vérifiez le choix du modèle, les limites de crédits et l'état de Stage.

## Ligne de développement {#development-line}

- **2025-04-16 — Krea AI a publié une expérience vidéo avec un identifiant OL Flux.** Le 2025-04-16, un lien daté de Krea AI pointait vers son expérience vidéo, avec des paramètres d'URL identifiant une variante OL Flux. Il s'agit d'une étape importante de la ligne de développement de la génération vidéo chez Krea AI. Les liens n'établissent ni les détails des capacités, ni la disponibilité, ni la formulation du lancement.
- **2025-04-18 — Krea AI a relié son interface produit Stage.** Le 2025-04-18, un lien daté de Krea AI pointait vers le parcours produit Stage de l'entreprise. Il s'agit d'une étape importante de la ligne vidéo, car elle identifie une interface produit distincte. Les liens n'établissent ni l'ensemble des fonctionnalités de Stage, ni sa disponibilité, ni si cette date correspond à son lancement.
- **2025-08-29 — Krea AI a publié une annonce pour Realtime Video.** Le 2025-08-29, Krea AI a publié une page de blog dont l'URL identifie une annonce pour Realtime Video. Il s'agit d'une évolution importante de la ligne de génération vidéo de l'entreprise. Les liens n'établissent ni son modèle de fonctionnement, ni les conditions de déploiement, ni les détails des fonctionnalités.

## Ce qui a changé {#what-changed}

Krea AI est passé d'interfaces Video et Stage séparées à une boîte à outils dotée de son propre modèle et d'un flux de travail temps réel contrôlable.

- **2025-04-16 :** Video était documentée, mais la version exacte ne peut pas être retrouvée à partir de l'ancienne URL avec le paramètre `ol_flux`, car elle mène désormais à une interface modifiée.
- **2025-04-18 :** Stage proposait un flux expérimental de scène 3D : créer une scène à partir d'un texte, ajouter et déplacer des objets, puis exporter en glTF. La confirmation des détails est secondaire, car la spécification historique n'est plus disponible à l'URL d'origine.
- **2025-08-29 :** Realtime Video a ajouté une génération plus rapide que la lecture, avec un canevas, du texte, une webcam et la capture d'écran. L'annonce initiale est datée du 2025-08-27.
- **2025-10-20 :** Krea a publié Realtime 14B, un modèle autorégressif pour la vidéo temps réel de longue durée. L'entreprise annonce 11 fps sur un B200 et des premières images en environ une seconde.
- **2026-05-12 et 2026-05-21 :** Krea 2 est devenu son propre modèle de fondation pour les images, suivi de l'entraînement LoRA en bêta pour Max et Business.
- **2026-09-04 :** La documentation actuelle décrit Krea comme une boîte à outils comprenant Image, Video, Realtime, Edit, Enhancer et Train, et non comme un seul générateur.

## Comment l'utiliser {#how-to-use-this}

À partir du 2025-08-29, les praticiens qui évaluent Krea AI devraient inclure son interface Realtime Video dans leurs comparaisons de flux de travail et vérifier de manière indépendante l'accès actuel, le comportement et les capacités.

1. Ouvrez Krea et choisissez Image ou Video pour un rendu standard. Utilisez Realtime lorsque la composition nécessite une direction en direct.  
   — [Guide Krea](https://www.krea.ai/docs/user-guide/get-started/what-is-krea)
2. Dans Video, choisissez un modèle, définissez le prompt, le format, la durée et la résolution, et ajoutez les images de début et de fin si nécessaire.  
   — [Modèles vidéo](https://www.krea.ai/docs/user-guide/features/video)
3. Dans Realtime, saisissez un prompt, puis dessinez, déplacez des personnages, importez une référence ou fournissez un flux de webcam ou d'écran. Choisissez Image ou Video comme sortie.  
   — [Realtime](https://www.krea.ai/docs/user-guide/features/realtime)
4. Pour un style, un personnage ou un produit reproductible, ouvrez Train. Importez au moins trois images, choisissez Krea 2 Medium ou Large, vérifiez les légendes et connectez le LoRA finalisé dans Image.  
   — [Entraînement LoRA de Krea 2](https://www.krea.ai/blog/krea-2-lora-training)
5. Pour modifier une zone, ouvrez Edit. Sélectionnez-la avec un rectangle, un pinceau ou la sélection automatique, puis décrivez le remplacement. Poursuivez l'historique des modifications étape par étape.  
   — [Krea Edit](https://www.krea.ai/blog/krea-edit)

## Bonnes pratiques {#best-practices}

- Comparez plusieurs modèles avec le même prompt. Choisissez en fonction du mouvement, du contrôle et de la conservation du personnage requis, et non du nom du modèle.  
  — [Modèles vidéo](https://www.krea.ai/docs/user-guide/features/video)
- Commencez par des tests de 5 à 10 secondes, à moindre coût ; n'augmentez la durée et la résolution qu'après avoir choisi une direction.  
  — [Modèles vidéo](https://www.krea.ai/docs/user-guide/features/video)
- Décrivez explicitement l'action et le mouvement de caméra. Utilisez des images de début et de fin, et assemblez d'abord les scènes complexes à partir d'images séparées.  
  — [Modèles vidéo](https://www.krea.ai/docs/user-guide/features/video)
- Utilisez Realtime pour la composition et les tests rapides. Utilisez Image classique lorsque vous avez besoin d'un rendu réfléchi, piloté par le prompt, sans dessin.  
  — [Realtime](https://www.krea.ai/docs/user-guide/features/realtime)
- Pour un LoRA, gardez un premier jeu de données restreint mais varié en angles, éclairages et arrière-plans. Vérifiez les légendes à la main et n'augmentez pas le nombre d'étapes sans raison.  
  — [Entraînement LoRA de Krea 2](https://www.krea.ai/blog/krea-2-lora-training)

## Remplacé par ceci {#superseded-by-this}

- **2025-04-16** — La conclusion recommandant un modèle vidéo à partir de l'ancien paramètre `ol_flux` est obsolète. Choisissez le modèle dans le sélecteur actuel et vérifiez-le avec le même test.
- **2025-04-18** — L'instruction consistant à traiter Stage comme un point d'entrée autonome documenté est obsolète. Sa spécification historique n'est plus disponible à l'URL d'origine ; l'ancien flux de travail doit donc être revérifié.
- **2025-08-29** — Considérer l'annonce de Realtime Video comme l'état final de la fonction est obsolète. Elle a évolué vers Realtime 14B le 2025-10-20, puis vers le flux de travail Realtime actuel, basé sur un canevas.

## Points encore inconnus {#still-unknown}

- La sortie exacte du produit du 2025-04-16 n'est pas confirmée. L'URL Video subsiste, mais son contenu historique et la signification du paramètre `ol_flux` ne sont pas disponibles.
- Stage est confirmé comme un outil 3D expérimental distinct en avril 2025, mais on ignore s'il a été renommé, déplacé ou fermé par la suite. La page `/stage` actuelle ne fournit pas de spécification lisible.
- Les trois dates concernent une même entreprise mais des interfaces produit différentes : Video, Stage et Realtime. Il ne s'agit pas de trois entreprises indépendantes, mais le devenir de Stage reste flou.
- Les documents principaux actuels sont incohérents : la page d'accueil présente encore Krea 1 comme modèle principal, alors que les publications de 2026 positionnent Krea 2 comme son propre modèle de fondation.
- L'accès aux modèles, aux offres, aux crédits et aux restrictions régionales n'a pas été vérifié pour un compte spécifique. Les chiffres de la documentation sont indicatifs et ne garantissent pas l'offre applicable.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.krea.ai/video?kr_v=ol&krex=ol_flux | Krea Video | 2026-09-04 |
| https://www.krea.ai/stage | Krea Stage | 2026-09-04 |
| https://cgworld.jp/flashnews/01-202504-KreaStage.html | KREAに3Dシーン生成機能「Krea Stage」が追加 | 2026-09-04 |
| https://www.krea.ai/blog/announcing-realtime-video | Announcing Realtime Video | 2026-09-04 |
| https://www.krea.ai/blog/krea-realtime-14b | Krea Realtime 14B: Real-Time, Long-Form AI Video Generation | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-image-model | Introducing Krea 2 | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-lora-training | Krea 2 LoRA training is now available | 2026-09-04 |
| https://www.krea.ai/docs/user-guide/get-started/what-is-krea | What is Krea? | 2026-09-04 |
| https://www.krea.ai/docs/user-guide/features/video | Video Models | Krea Documentation | 2026-09-04 |
| https://www.krea.ai/docs/user-guide/features/realtime | Realtime | Krea Documentation | 2026-09-04 |
| https://www.krea.ai/blog/krea-edit | A New, More Powerful Krea Edit | 2026-09-04 |

## Fiche pour agent {#agent-brief}

- **Sujet :** `organization:krea-ai`, fil `video-generation`, 3 événements datés du 2025-04-16 au 2025-08-29.
- **Remarque pratique :** À partir du 2025-08-29, les praticiens qui évaluent Krea AI devraient inclure son interface Realtime Video dans leurs comparaisons de flux de travail, tout en vérifiant de manière indépendante l'accès actuel, le comportement et les capacités.
- **Confiance :** moyenne. Les entrées datées remplacées ci-dessus déterminent ce qui est obsolète.

---
title: "Hedra — Développement produit de Hedra"
category: organizations
tags: [hedra, hedra-product-development, hedra_release, organization, product_releases]
aliases: ["Hedra"]
level: 2
source_sha256: 344314acd4111229551acdc1aa2a8ba9594250ca30f2a41eddc33d4e5327ef2c
translation: machine
translated_at: '2026-10-24'
---
# Hedra — Développement produit de Hedra {#hedra-hedra-product-development}

**Ligne de développement :** `organization:hedra` · fil `hedra-product-development`  
**Événements :** 3 datés, 2025-04-02 → 2026-02-20 · **Date de recherche :** 2026-09-03 · confiance : moyenne

## Ce que c'est {#what-it-is}

Hedra — un flux de travail unique pour les personnes qui, autrement, combineraient un service d'avatars parlants, un générateur de vidéos, un outil vocal et une API de modèles. — Agent et Studio pour l'image, la vidéo, la parole, l'édition, les références et les instructions réutilisables. — Modèles de personnages de première partie : Character 3, Avatar et Omnia ; l'API expose également des modèles d'image, de vidéo et d'audio. Limite : Character 3 accepte image, texte et audio pour des vidéos allant jusqu'à 10 minutes ; Omnia est destiné à de courts clips d'environ huit secondes en 1080p. Verdict : à utiliser lorsque la performance du personnage et un flux de création et d'API partagé comptent ; choisir et valider le modèle pour chaque tâche plutôt que de considérer tous les modes vidéo comme interchangeables.

## Ligne de développement {#development-line}

- **2025-04-02 — La route publique de l'application vidéo de Hedra a été citée.** Le 2025-04-02, une référence datée de Hedra citait la route publique `/app/video`. Cela consigne un point d'entrée public du produit vidéo dans la ligne de développement, alors que le lien seul n'établit ni sa date de lancement, ni ses capacités, ni ses conditions d'accès.
- **2025-07-24 — La route publique de l'application avatar de Hedra a été citée.** Le 2025-07-24, une référence datée de Hedra citait la route publique `/app/avatar`. Cela consigne un point d'entrée du produit avatar dans la ligne de développement, sans affirmer une version, un modèle, un flux de travail ou un changement de disponibilité spécifique.
- **2026-02-20 — Hedra a relié une documentation de démarrage rapide pour développeurs aux points d'entrée des applications.** Le 2026-02-20, une référence datée de Hedra incluait sa route d'accueil de l'application et la documentation de démarrage rapide pour développeurs. Cela consigne une surface de documentation publique pour développeurs à côté des points d'entrée du produit, mais n'établit ni le contenu, ni la date de publication, ni la disponibilité d'une API ou d'une fonctionnalité.

## Ce qui a changé {#what-changed}

2024-08-17 — La page d'accueil de Hedra a été enregistrée, mais aucun texte de version ne subsiste avec cet événement ; un changement de produit précis ne peut pas être reconstitué de façon sûre. 2025-03-07 — Character 3 a remplacé Character 2 en mars 2025. Il a modifié le cœur vidéo des personnages de Hedra pour utiliser conjointement image, texte et audio pour la synchronisation labiale et l'animation des personnages. 2025-04-02 — La route /app/video enregistrée est désormais un espace de travail Vidéo avec des outils manuels. Le dossier disponible n'établit pas de version distincte au-delà de ce point d'entrée à la création vidéo. 2025-07-24 — La route /app/avatar enregistrée redirige désormais vers /app/home, qui ouvre un espace de travail Agent. C'est la preuve d'un point d'entrée modifié, et non la preuve que le modèle Hedra Avatar actuel a été lancé en juillet 2025. 2026-02-20 — Un démarrage rapide pour développeurs a été enregistré. Sa version actuelle exige un compte payant, une clé API, des crédits et une demande de liste de modèles avant toute génération ; il s'agit de la documentation actuelle, et non d'une preuve de son état exact de février 2026. 2026-02-05 — Hedra a lancé Omnia, ajoutant le mouvement de scène, des environnements dynamiques et le contrôle directionnel de la caméra à la vidéo de personnages conditionnée par l'audio. 2026-09-04 (constaté aujourd'hui) — Hedra est désormais organisé autour d'un flux de travail Agent/Studio et d'une API pour développeurs, plutôt que seulement comme un terrain d'essai de vidéos de personnages.

## Comment l'utiliser {#how-to-use-this}

À la date du 2026-02-20, les praticiens qui évaluent Hedra doivent consulter ses points d'entrée publics d'application et son démarrage rapide pour développeurs avant de supposer quels flux de travail vidéo, avatar ou développeur sont disponibles.

1. Pour un travail dans Studio, créez un Space, énoncez l'objectif, le public, le format de sortie, les contraintes et la matière de référence, puis examinez et dirigez les itérations sur le canevas.
  — <https://www.hedra.com/docs/pages/app/getting-started/overview>
2. Pour une vidéo de personnage qui parle, préparez un portrait et un audio propre ; utilisez un flux de travail avatar lorsque l'audio pilote la synchronisation labiale et le mouvement.
  — <https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video>
3. Pour Omnia, fournissez une image et un audio, puis dirigez explicitement le mouvement du sujet, la caméra et l'arrière-plan dans le prompt.
  — <https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model>
4. Pour le travail avec l'API, utilisez un compte payant, créez une clé API avec suffisamment de crédits et demandez le catalogue de modèles actuel avant de choisir un modèle.
  — <https://www.hedra.com/docs/pages/developer/getting_started/quickstart>
5. Téléversez les ressources requises, soumettez la génération et interrogez son statut jusqu'à ce qu'elle soit terminée et renvoie la ressource de sortie.
  — <https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video>

## Bonnes pratiques {#best-practices}

- Utilisez un portrait rapproché net et bien éclairé ainsi qu'un audio vocal propre ; décrivez la diction et un mouvement mesuré lorsque la performance visée est précise.
  — <https://www.hedra.com/models/video/hedra/character-3>
- Pour Omnia, utilisez un seul sujet, une direction de caméra explicite, le format 16:9, un audio clair et au rythme posé, et assemblez les travaux plus longs à partir de courts clips d'environ huit secondes en 1080p.
  — <https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model>
- Consultez le catalogue de modèles avant la génération et vérifiez son slug, ses exigences d'entrée, sa durée, sa résolution et sa tarification ; privilégiez le slug stable à un identifiant de modèle propre à un environnement.
  — <https://www.hedra.com/docs/api-reference/public/list-models>
- Considérez la génération comme asynchrone : interrogez le statut et n'utilisez la ressource renvoyée qu'après l'achèvement.
  — <https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video>

## Remplacé par ceci {#superseded-by-this}

- Mars 2025 — Character 2 est remplacé par Character 3 pour le modèle de vidéo de personnages central de Hedra.
- 2025-07-24 — Ne pas utiliser /app/avatar comme chemin d'entrée stable et actuel : constaté le 2026-09-04, il redirige vers /app/home.
- Février 2026 — La recommandation qui ne considère Hedra que comme un outil d'avatar parlant à caméra fixe est incomplète : Omnia ajoute une caméra dirigée et le mouvement de l'environnement, avec une limite de clips courts.
- 2026-09-04 — La recommandation qui ne considère Hedra que comme un simple terrain d'essai vidéo web est obsolète : la documentation actuelle expose un espace de travail Agent, des outils média manuels et une API pour développeurs.

## Toujours inconnu {#still-unknown}

- L'événement du 2024-08-17 ne contient qu'une URL de page d'accueil ; sa revendication de version précise n'est pas disponible.
- L'événement du 2025-03-07 n'a pas d'URL extraite ; son rattachement à Character 3 repose donc sur la date de publication de mars 2025 indiquée sur la page officielle du modèle, et non sur un texte d'événement conservé.
- Les références de route des 2025-04-02 et 2025-07-24 ne conservent pas assez de texte pour identifier une version ou un lancement de fonctionnalité distinct.
- L'URL du statut X liée n'a pas pu être récupérée, et http://hedra.com/app/home n'a renvoyé aucune page lisible ; aucune des deux n'est utilisée comme preuve factuelle.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.hedra.com/ | Hedra — Visual Inference Models and Infrastructure | 2026-09-04 |
| https://www.hedra.com/app/video | Hedra Video Playground | 2026-09-04 |
| https://www.hedra.com/app/avatar | Hedra Agent — General Visual Intelligence | 2026-09-04 |
| https://www.hedra.com/docs/pages/developer/getting_started/quickstart | Hedra API Quickstart Guide | 2026-09-04 |
| https://www.hedra.com/docs/pages/app/getting-started/overview | Meet Hedra Agent | 2026-09-04 |
| https://www.hedra.com/models/video/hedra/character-3 | Hedra Character 3: Omnimodal Character Video | 2026-09-04 |
| https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model | Hedra Omnia: Unified AI Video for Character-Driven Content | 2026-09-04 |
| https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video | Generate an Avatar Video | 2026-09-04 |
| https://www.hedra.com/docs/api-reference/public/list-models | List Available AI Models | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `organization:hedra`, fil `hedra-product-development`, 3 événements datés du 2025-04-02 → 2026-02-20.
- **Note pratique :** À la date du 2026-02-20, les praticiens qui évaluent Hedra doivent consulter ses points d'entrée publics d'application et son démarrage rapide pour développeurs avant de supposer quels flux de travail vidéo, avatar ou développeur sont disponibles.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.

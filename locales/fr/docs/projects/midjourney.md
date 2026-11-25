---
title: "Midjourney"
category: projects
date: 2025-04-04
tags: [midjourney, midjourney-beta-access, midjourney-model-and-feature-releases, midjourney_blend_command, midjourney_v4, midjourney_v5, project, releases]
aliases: ["Midjourney"]
level: 3
source_sha256: af03fc429e02812f57852a31c4ce74a65f57fae81841a6ee4c6bb1db9a84b678
translation: machine
translated_at: '2026-10-24'
---
# Midjourney {#midjourney}

**Ligne de développement :** `project:midjourney` · fil `midjourney-model-and-feature-releases`  
**Dernier événement :** 2025-04-04 · 6 événements datés depuis 2022-07-12 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

Midjourney est un générateur d'images et de vidéos par abonnement, destiné à la direction artistique, au travail de concept et à l'itération visuelle rapide.

- Génère des images fixes à partir de prompts textuels, d'images de référence, de références de style, de personnalisation et de références du Edit Model.
- Prend en charge les variations, l'inpainting, l'outpainting, l'extension de canevas et la transformation d'une image fixe en vidéo de 5 secondes.

## Ligne de développement {#development-line}

- **2022-07-12 — Midjourney ouvre l'accès bêta.** Le 2022-07-12, l'accès bêta commence avec un lien raccourci, sans détails publics sur l'éligibilité ni sur le déploiement.
- **2022-11-07 — Midjourney présente la V4.** Le 2022-11-07, Midjourney publie la V4 avec des liens officiels et une couverture externe ; les conditions d'accès exactes ne sont pas précisées.
- **2023-01-16 — Midjourney documente la commande Blend.** Le 2023-01-16, Blend apparaît comme une étape visible pour les utilisateurs, sans URL source conservée pour son déploiement.
- **2023-03-09 — Midjourney ouvre l'évaluation de préproduction de la V5.** Les rendus deviennent plus photographiques et correspondent plus étroitement aux prompts, bien que les utilisateurs aient eu besoin de prompts plus longs pour l'esthétique visée.
- **2023-03-16 — Midjourney documente la V5.** Le 2023-03-16, la V5 marque une étape majeure du modèle, sans URL conservée pour la date de sortie ou la disponibilité des fonctionnalités.
- **2025-04-04 — Midjourney publie la V7 Alpha.** Le 2025-04-04, Midjourney renvoie vers la mise à jour officielle V7 Alpha et les pages Imagine, marquant l'étape sans détailler l'ensemble des règles de compte.

## Ce qui a changé {#what-changed}

- **2022-07-12** — La note sur l'accès bêta ne dispose pas de source accessible ; la documentation officielle place la V3 comme modèle par défaut à partir de juillet 2022.
- **2022-07-26** — Aucune URL conservée ni changement de produit corroboré.
- **2022-11-07** — La V4, publiée en novembre 2022, introduit une nouvelle base de code et une nouvelle architecture d'IA, avec une cohérence accrue, une meilleure gestion des détails, le prompt par image et les multi-prompts.
- **2023-01-16** — La date de lancement de Blend ne peut pas être vérifiée indépendamment ; `/blend` reste disponible sur Discord pour combiner 2 à 5 images.
- **2023-03-09** — La préproduction de la V5 correspond à la sortie de la V5 en mars 2023 : rendus plus photographiques et correspondance plus étroite avec les prompts, bien que des prompts plus longs puissent être nécessaires pour l'esthétique visée.
- **2023-03-16** — Aucune URL conservée ne distingue cette mention de la V5 du déploiement de la V5 de mars.
- **2023-05-03** — Un signalement communautaire évoquait un nouveau blocage des prompts en V5.1. L'historique officiel date la V5.1 du 4 mai 2023 et mentionne une esthétique par défaut renforcée, une meilleure cohérence, une interprétation du langage naturel et `--tile` ; l'affirmation précise de blocage n'est pas vérifiée.
- **2023-08-22** — Aucune URL conservée n'appuie un changement de produit distinct.
- **2025-04-04** — La V7 Alpha est ouverte aux tests, avec la personnalisation activée par défaut, le Draft Mode et une meilleure cohérence entre prompt et image ; certaines fonctions d'édition ont d'abord basculé vers la V6.
- **2025-06-17** — La V7 devient le modèle par défaut.
- **2026-04-14 / 2026-06-10** — La V8.1 est lancée, puis devient le modèle par défaut, avec des générations plus rapides et des images 2K HD en option.
- **2026-07-24** — La V8.2 devient le modèle par défaut. Son Edit Model remplace V7 Omni Reference, Character Reference et Retexture dans le flux de travail V8 actuel.

## Comment l'utiliser {#how-to-use-this}

Au 2025-04-04, considérez les versions de modèle de Midjourney et les versions alpha comme des cibles de flux de travail distinctes : vérifiez la disponibilité actuelle sur les pages officielles de mise à jour et Imagine avant d'adopter une version en production.

1. Créez un compte ou connectez-vous, choisissez une formule d'abonnement et ouvrez la page Create.  
  — <https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide>
2. Saisissez un prompt visuel concis dans la barre Imagine et soumettez-le pour générer un premier ensemble d'images.  
  — <https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web>
3. Conservez la V8.2 comme modèle par défaut, ou fixez un modèle avec `--v #` lorsqu'un projet nécessite un comportement reproductible propre à une version.  
  — <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>
4. Ajoutez jusqu'à quatre images de référence, ou modifiez une image existante à l'aide d'instructions écrites via le Edit Model de la V8.  
  — <https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model>
5. Choisissez un résultat prometteur, puis réalisez des variations Subtle ou Strong plutôt que de repartir de zéro.  
  — <https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations>
6. Lorsqu'un mouvement est nécessaire, utilisez une image fixe comme première image et générez une vidéo de 5 secondes ; choisissez réfléchiment les réglages de mouvement et de planification, car la vidéo consomme davantage de temps GPU.  
  — <https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video>

## Bonnes pratiques {#best-practices}

- Rédigez des descriptions visuelles courtes et concrètes ; n'incluez que les éléments qui comptent : sujet, médium, cadre, éclairage, couleur, ambiance et composition.  
  — <https://docs.midjourney.com/docs/prompts>
- Traitez les prompts par image comme une influence plutôt que comme une copie : décrivez en texte chaque élément final requis, et utilisez l'Editor pour les modifications précises.  
  — <https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts>
- Pour un rendu cohérent, utilisez une Style Reference pour le style et décrivez le sujet souhaité comme contenu, et non comme une instruction de modification de la référence.  
  — <https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference>
- Utilisez `--seed` pour comparer des modifications de prompt à partir d'un point de départ V8 quasi identique ; ne considérez pas un seed comme un verrou de style ou de personnage réutilisable.  
  — <https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds>
- Créez un profil de Personalization ou un Moodboard pour les esthétiques récurrentes d'un projet ; des sélections d'images plus réfléchies améliorent l'adéquation du profil.  
  — <https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization>
- Ne téléversez que des images dont vous détenez les droits d'utilisation, et maintenez les modifications d'images externes dans le cadre des règles du service et du droit applicable.  
  — <https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor>

## Remplacé par ceci {#superseded-by-this}

- Les règles d'accès bêta 2022 et V3 sont obsolètes pour un usage par défaut : commencez par un abonnement sur la page web Create ou via le bot Discord.
- La V8.2 remplace les recommandations par défaut pour la V4, la V5 et la V5.1 ; ne fixez `--v` que lorsqu'un projet requiert un comportement hérité.
- Les conseils Blend de 2023 ne correspondent plus au flux de travail web : utilisez plusieurs prompts par image sans texte sur le web ; `/blend` reste réservé à Discord.
- Le Edit Model remplace V7 Omni Reference, V6 Character Reference et Retexture dans le flux de travail V8.
- La V8.2 remplace la V7 comme modèle par défaut ; la V7 reste une version héritée sélectionnable, et non le modèle par défaut actuel.

## Toujours inconnu {#still-unknown}

- Les affirmations liées à l'événement d'accès bêta du 2022-07-12, ainsi qu'aux événements non reliés des 2022-07-26, 2023-03-16 et 2023-08-22, ne peuvent pas être reconstituées à partir des éléments disponibles.
- Le lien raccourci, la page de préproduction de la V5, le message Discord lié, le message Reddit lié et la page DTF liée n'ont pas pu être récupérés lors de cette session de recherche ; leurs affirmations n'ont pas été utilisées comme preuves factuelles.
- La documentation officielle actuelle date la sortie de la V7 au 2025-04-03, tandis que l'annonce de la V7 Alpha est datée du 2025-04-04 ; l'écart d'un jour reste non résolu.
- Les tarifs actuels des formules et les quotas d'utilisation n'ont pas été relevés ; nous ne recommandons donc pas de formule d'abonnement particulière.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features | Legacy Features – Midjourney | 2026-09-04 |
| https://updates.midjourney.com/v7-alpha/ | V7 Alpha | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version | Version – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide | Getting Started Guide – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web | Creating on Web – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model | Edit Model – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations | Variations – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video | Video – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/docs/prompts | Prompt Basics – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts | Image Prompts – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference | Style Reference – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds | Seeds – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization | Personalization – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor | Editor – Midjourney | 2026-09-04 |

## Brief de l'agent {#agent-brief}

- **Sujet :** `project:midjourney`, fil `midjourney-model-and-feature-releases`, 6 événements datés du 2022-07-12 au 2025-04-04.
- **Note pratique :** Au 2025-04-04, les praticiens doivent considérer les versions de modèle de Midjourney et les versions alpha comme des cibles de flux de travail distinctes : vérifiez la disponibilité actuelle via les pages officielles de mise à jour et Imagine avant d'adopter une version dans un flux de travail de production.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

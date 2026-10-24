---
title: "Midjourney"
category: projects
date: 2025-04-04
tags: [midjourney, midjourney-beta-access, midjourney-model-and-feature-releases, midjourney_blend_command, midjourney_v4, midjourney_v5, project, releases]
aliases: ["Midjourney"]
level: 3
source_sha256: f9a618d75004f7088f5ad1b51b9b74e22b82c6ce60ba5e751ee7dc27351d0025
translation: machine
translated_at: '2026-10-24'
---
# Midjourney {#midjourney}

**Ligne de développement :** `project:midjourney` · fil `midjourney-model-and-feature-releases`  
**Dernier événement :** 2025-04-04 · 6 entrées datées depuis 2022-07-12 · **Recherche :** 2026-09-04 · fiabilité : moyenne

## Présentation {#what-it-is}

Midjourney est un générateur d'images et de vidéos par abonnement, destiné à la direction artistique, au travail de concept et à l'itération visuelle rapide.

- Génère des images fixes à partir de prompts textuels, d'images de référence, de références de style, de personnalisation et de références Edit Model.
- Prend en charge les variations, l'inpainting, l'outpainting, l'extension de canevas et la transformation d'une image fixe en vidéo de 5 secondes.

## Ligne de développement {#development-line}

- **2022-07-12 — Accès bêta à Midjourney documenté.** Les archives mentionnaient un élément sur l'accès bêta avec un lien raccourci, mais ce lien ne permet pas de vérifier l'éligibilité, le périmètre ni le fonctionnement.
- **2022-11-07 — Introduction de Midjourney V4.** Les archives renvoyaient vers le site officiel et une couverture externe de Midjourney V4, sans établir les fonctionnalités exactes ni les conditions d'accès.
- **2023-01-16 — Commande Blend de Midjourney documentée.** Les archives mentionnaient une entrée sur la commande Blend, sans URL source permettant de vérifier son fonctionnement ou son déploiement.
- **2023-03-09 — Ouverture en phase de test de V5.** Les sorties devenaient plus photographiques et respectaient plus fidèlement les prompts, même si des prompts plus longs étaient parfois nécessaires pour obtenir l'esthétique voulue.
- **2023-03-16 — Midjourney V5 documenté.** Les archives mentionnaient une étape de V5, sans URL permettant de confirmer la date, les fonctionnalités ou la disponibilité.
- **2025-04-04 — Sortie de Midjourney V7 Alpha.** Les archives renvoyaient vers la page officielle de mise à jour V7 Alpha et la page officielle Imagine, mais ces liens n'établissent ni l'ensemble complet des fonctionnalités ni les règles d'accès.

## Évolutions {#what-changed}

Le 2022-07-12, la note sur l'accès bêta ne disposait d'aucune confirmation accessible ; l'historique officiel place V3 comme modèle par défaut à partir de juillet 2022. Le 2022-07-26, aucune URL ni aucun changement de produit n'a été conservé. Le 2022-11-07, V4 a introduit une nouvelle base de code et une nouvelle architecture d'IA, améliorant la cohérence, le traitement des détails, le prompt image et les multi-prompts après sa sortie de novembre 2022. Le 2023-01-16, un événement Blend a été consigné sans date de lancement indépendante ; `/blend` reste disponible dans Discord pour combiner 2 à 5 images. Le 2023-03-09, la phase de test de V5 correspond à la sortie de V5 de mars 2023, avec des sorties plus photographiques et un respect plus étroit des prompts, des prompts plus longs étant nécessaires pour certaines esthétiques. Le 2023-03-16, aucune URL conservée ne permet de distinguer cette mention du déploiement de V5 de mars. Le 2023-05-03, un signalement de la communauté faisait état d'un nouveau blocage des prompts en V5.1 ; l'historique officiel date V5.1 du 4 mai 2023, avec une esthétique par défaut renforcée, une meilleure cohérence, une interprétation du langage naturel et `--tile`, la politique de blocage restant non vérifiée. Le 2023-08-22, aucune URL conservée n'étaye un changement de produit. Le 2025-04-04, V7 Alpha a été lancée avec la personnalisation par défaut, le Draft Mode et une meilleure cohérence entre prompt et image, certaines fonctions d'édition revenant temporairement à V6. Le 2025-06-17 (trouvé aujourd'hui), V7 est devenue le modèle par défaut. Les 2026-04-14 et 2026-06-10 (trouvé aujourd'hui), V8.1 a été lancée puis est devenue le modèle par défaut, avec des générations plus rapides et des images 2K HD en option. Le 2026-07-24 (trouvé aujourd'hui), V8.2 est devenue le modèle par défaut, et son Edit Model a remplacé Omni Reference V7, Character Reference et Retexture dans le flux de travail V8.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-04-04, considérez les versions de modèles et les versions alpha comme des cibles de workflow distinctes : vérifiez la disponibilité sur les pages officielles de mise à jour et Imagine avant d'adopter une version en production.

1. Connectez-vous ou créez un compte, choisissez une formule d'abonnement, puis ouvrez la [page Create](https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide).
2. Saisissez un prompt visuel concis dans la barre Imagine pour générer un premier lot d'images, comme décrit dans [Creating on Web](https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web).
3. Utilisez V8.2 par défaut, ou fixez un modèle avec `--v #` via [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version) lorsque la reproductibilité compte.
4. Fournissez jusqu'à quatre images de référence ou modifiez une image à l'aide d'un texte avec [Edit Model](https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model).
5. Choisissez un résultat satisfaisant, puis générez des [Variations](https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations) Subtle ou Strong plutôt que de repartir de zéro.
6. Pour le mouvement, transformez une image fixe en image initiale d'une [Video](https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video) de 5 secondes ; choisissez délibérément les réglages de mouvement et de planification, car la vidéo consomme davantage de temps GPU.

## Bonnes pratiques {#best-practices}

- Rédigez des descriptions visuelles courtes et concrètes, ne couvrant que les éléments clés : sujet, technique, cadre, éclairage, couleur, ambiance et composition, conformément à [Prompt Basics](https://docs.midjourney.com/docs/prompts).
- Considérez les [Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts) comme une source d'influence plutôt que comme des copies exactes : décrivez chaque élément requis en texte et utilisez l'Editor pour les retouches fines.
- Utilisez une [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference) pour définir l'apparence, et formulez le sujet comme un contenu nouveau plutôt que comme une instruction de modification de la référence.
- Utilisez `--seed` pour comparer des ajustements de prompt à partir d'un point de départ V8 identique, selon [Seeds](https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds) ; n'utilisez pas les seeds comme verrou de personnage ou de style.
- Construisez un profil de Personalization ou un Moodboard selon [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization) pour les styles récurrents d'un projet ; une sélection d'images soignée donne une correspondance plus précise.
- Ne téléversez que des images dont vous détenez les droits, et assurez-vous que les modifications externes respectent les règles du service et le droit applicable, selon [Editor](https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor).

## Remplacé par {#superseded-by-this}

- Les règles d'accès de la bêta 2022 et de V3 ne sont plus valables pour un usage quotidien : le travail actuel commence par un abonnement et la page web Create ou le bot Discord.
- Les consignes désignant V4, V5 ou V5.1 comme modèle par défaut sont remplacées par V8.2 ; ne fixez `--v` que lorsqu'une sortie héritée est nécessaire.
- Les instructions Blend de 2023 ne s'appliquent pas à l'interface web : sur le web, transmettez plusieurs prompts image sans texte ; `/blend` reste réservé à Discord.
- Les consignes relatives à Omni Reference V7, Character Reference V6 et Retexture sont remplacées par Edit Model de V8.
- V7 comme modèle par défaut est remplacé par V8.2 ; V7 reste sélectionnable comme modèle hérité.

## Points non élucidés {#still-unknown}

- Les affirmations sous-jacentes à la note sur l'accès bêta du 2022-07-12, ainsi qu'aux entrées sans lien des 2022-07-26, 2023-03-16 et 2023-08-22, ne peuvent pas être reconstituées à partir des éléments disponibles.
- Le lien raccourci, la page de test de V5, le message Discord, la publication Reddit et la page DTF étaient inaccessibles pendant la recherche et ne servent pas de justificatif factuel.
- La documentation actuelle date la sortie de V7 au 2025-04-03, alors que l'annonce de V7 Alpha est datée du 2025-04-04 ; la raison de cet écart d'un jour reste non résolue.
- Les tarifs actuels des abonnements et les quotas d'utilisation n'ont pas été relevés ; aucune formule particulière n'est donc recommandée.

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

## Brief pour agent {#agent-brief}

- **Sujet :** `project:midjourney`, fil `midjourney-model-and-feature-releases`, 6 événements datés du 2022-07-12 au 2025-04-04.
- **Note pratique :** Au 2025-04-04, les praticiens doivent considérer les versions de modèles Midjourney et les versions alpha comme des cibles de workflow distinctes : vérifiez la disponibilité actuelle sur les pages officielles de mise à jour et Imagine avant d'adopter une version dans un workflow de production.
- **Fiabilité :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.

---
title: "D-ID — Surfaces produit publiques"
category: organizations
tags: [d-id, d_id_studio, organization, product_release, public-product-surfaces]
aliases: ["D-ID"]
level: 2
source_sha256: ca2345995e7b1dd0102f835334e0983976f5ba95558ea5de4254026ee9d953ee
translation: machine
translated_at: '2026-10-24'
---
# D-ID — Surfaces produit publiques {#d-id-public-product-surfaces}

**Ligne de développement :** `organization:d-id` · fil `public-product-surfaces`  
**Événements :** 2 datés, 2022-08-01 → 2023-03-09 · **Recherche effectuée :** 2026-09-03 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

D-ID est une plateforme destinée aux équipes qui ont besoin soit d'une vidéo de présentateur générée, soit d'un agent visuel en direct sur un site web. — Crée des vidéos d'avatar parlant à partir d'une image, d'un texte ou d'un audio, ainsi que de la traduction vidéo. — Crée des agents WebRTC dotés d'un avatar, d'une voix, d'instructions pour LLM et, en option, d'une base de connaissances RAG. — Propose Studio, une API, un embed pour site web et un SDK client. Limite : la génération vidéo est asynchrone, tandis que les agents intégrés exigent des clés client restreintes aux domaines approuvés. Verdict : choisissez d'abord la voie vidéo ou la voie temps réel ; D-ID n'est plus seulement une démo de photo parlante.

## Ligne de développement {#development-line}

- **2022-08-01 — Surface de démonstration publique de D-ID enregistrée.** Le 2022-08-01, l'enregistrement scellé pointait vers une démo de D-ID hébergée sur son sous-domaine create. Cela établit une surface de démonstration tournée vers le public dans la ligne de développement de l'entreprise, sans établir la fonctionnalité exacte de la démo ni son statut de lancement.
- **2023-03-09 — Surface produit de chat de D-ID enregistrée.** Le 2023-03-09, l'enregistrement scellé pointait vers un point d'accès de chat de D-ID sur son sous-domaine chat. Cela indique une surface produit publique distincte après l'enregistrement précédent de la démo, mais n'établit ni ses capacités, ni ses conditions de diffusion, ni son lien avec la démo.

## Ce qui a changé {#what-changed}

2022-08-01 : `create.d-id.com/demo/` était le point d'entrée de la démo Studio. Son titre actuel identifie Creative Reality Studio, mais l'état d'origine de la démo n'est plus inspectable. 2022-09-19 (trouvé aujourd'hui) : D-ID a officiellement lancé Creative Reality Studio comme flux de travail en libre-service permettant de transformer une image en vidéo avec présentateur, faisant sortir le produit du seul réenactment vidéo réservé aux entreprises. 2023-03-07 (trouvé aujourd'hui) : D-ID a lancé la bêta de chat.D-ID, qui combine son humain numérique en streaming avec ChatGPT pour une conversation face à face. 2023-03-09 : `chat.d-id.com/` était la voie d'accès enregistrée à ce produit conversationnel ; elle redirige désormais vers la page AI Agents de D-ID. 2026-02-04 (trouvé aujourd'hui) : V4 Expressive Avatars est arrivé dans Studio et dans l'API, ajoutant la sélection de sentiment pour la vidéo générée. Aujourd'hui : D-ID documente deux voies distinctes — les Videos asynchrones et les Agents temps réel avec WebRTC, configuration LLM et bases de connaissances RAG. Verdict : la ligne de développement va d'un outil libre-service image-vers-présentateur à une plateforme comportant des produits séparés de vidéo préenregistrée et d'agents conversationnels.

## Comment l'utiliser {#how-to-use-this}

À partir du 2022-08-01, les praticiens pouvaient évaluer D-ID via une surface de démonstration publique ; à partir du 2023-03-09, ils devraient traiter son point d'accès de chat comme une surface produit distincte lors de l'évaluation des flux de travail disponibles, dans l'attente d'une recherche sur sources primaires.

1. Choisissez d'abord le flux de travail : utilisez Videos pour une sortie d'avatar asynchrone, ou Realtime pour un agent visuel conversationnel.
  — <https://docs.d-id.com/docs/quickstart>
2. Pour une vidéo V4, soumettez un ID d'avatar et le script texte ou audio requis au point d'accès Expressives ; vous pouvez éventuellement définir le sentiment, l'arrière-plan, l'URL de résultat ou le webhook.
  — <https://docs.d-id.com/reference/createv4video>
3. Pour un agent, créez-le avec un présentateur, une voix, un fournisseur/modèle LLM et des instructions ; conservez l'ID d'agent renvoyé.
  — <https://docs.d-id.com/docs/agent-quickstart>
4. Interrogez l'agent jusqu'à ce que son statut soit `done`, créez une clé client limitée à un domaine, puis utilisez le SDK client pour se connecter, discuter et se déconnecter.
  — <https://docs.d-id.com/docs/agent-session-quickstart>
5. Utilisez l'Agents Embed à script unique pour une interface web préconstruite ; utilisez plutôt le SDK lorsque l'application a besoin d'un contrôle programmatique de la mise en page et du comportement.
  — <https://docs.d-id.com/docs/embed-overview>

## Bonnes pratiques {#best-practices}

- Traitez `status: done` et l'URL de la vidéo d'attente renvoyée comme le critère de disponibilité avant d'ouvrir des sessions temps réel.
  — <https://docs.d-id.com/docs/agent-quickstart>
- Restreignez chaque clé client frontend aux domaines autorisés exacts ; elle n'est valide que depuis ces origines.
  — <https://docs.d-id.com/docs/agent-session-quickstart>
- Choisissez l'embed pour une intégration à code minimal, et le SDK uniquement lorsque l'application a besoin d'un contrôle complet de l'interface et du cycle de vie.
  — <https://docs.d-id.com/docs/embed-overview>
- Pour un LLM personnalisé en production, utilisez le streaming ; D-ID documente le mode sans streaming comme une option de débogage plutôt que comme un mode de production.
  — <https://docs.d-id.com/docs/llms-overview>

## Remplacé par ce qui suit {#superseded-by-this}

- 2022-08-01 — Le cadrage « démo seulement » est obsolète pour le choix d'un produit : la documentation actuelle de D-ID sépare les Videos asynchrones des Agents temps réel.
- 2023-03-09 — `chat.d-id.com/` en tant que point d'entrée Chat autonome est remplacé dans les faits : l'URL redirige désormais vers la page produit AI Agents actuelle.
- 2022–2023 — Les recommandations qui décrivent D-ID uniquement comme un outil de vidéo à présentateur à partir d'une seule image sont incomplètes lorsque le besoin réel est un agent visuel intégré et en direct.

## Points restant inconnus {#still-unknown}

- La date de la démo du 2022-08-01 précède l'annonce datée du lancement de Studio par D-ID, le 2022-09-19 ; elle peut donc correspondre à une démo précoce ou limitée plutôt qu'au lancement public. L'état exact n'est pas vérifié.
- Le contenu original de la page `create.d-id.com/demo/` n'est pas consultable aujourd'hui ; seul son titre actuel peut être récupéré.
- Les entrées Studio-demo et Chat correspondent à deux lignes produit différentes — vidéo asynchrone et conversation temps réel — au sein de D-ID, et non à des entreprises distinctes. Leur relation produit historique exacte et leur calendrier de dépréciation ne peuvent pas être reconstitués à partir des deux URL d'origine seulement.
- Les tarifs actuels, la disponibilité régionale et les exigences de politique de consentement n'ont pas été évalués dans cette recherche.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://create.d-id.com/demo/ | D-ID Creative Reality Studio | 2026-09-04 |
| https://chat.d-id.com/ | AI Agents : créer un agent visuel interactif | 2026-09-04 |
| https://www.d-id.com/news/d-id-launches-creative-reality-studio-self-service-video-creation-platform-with-hyper-real-ai-presenters/ | D-ID lance Creative Reality Studio, une plateforme de création vidéo en libre-service avec des présentateurs IA hyperréalistes | 2026-09-04 |
| https://www.d-id.com/news/press-release-chat-d-id-enables-anyone-to-talk-face-to-face-with-ai/ | Communiqué de presse : chat.D-ID permet à chacun de dialoguer face à face avec une IA | 2026-09-04 |
| https://docs.d-id.com/docs/quickstart | Démarrage rapide | 2026-09-04 |
| https://docs.d-id.com/reference/createv4video | Créer une vidéo | 2026-09-04 |
| https://docs.d-id.com/docs/agent-quickstart | Agents | 2026-09-04 |
| https://docs.d-id.com/docs/agent-session-quickstart | Sessions d'agent | 2026-09-04 |
| https://docs.d-id.com/docs/embed-overview | Présentation — Agents Embed | 2026-09-04 |
| https://docs.d-id.com/docs/llms-overview | Présentation — LLM | 2026-09-04 |
| https://www.d-id.com/resources/product-updates/expressive-avatars-are-live-in-d-id-studio/ | Expressive Avatars est disponible dans D-ID Studio | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `organization:d-id`, fil `public-product-surfaces`, 2 événements datés 2022-08-01 → 2023-03-09.
- **Note pratique :** À partir du 2022-08-01, les praticiens pouvaient évaluer D-ID via une surface de démonstration publique ; à partir du 2023-03-09, ils devraient traiter son point d'accès de chat comme une surface produit distincte lors de l'évaluation des flux de travail disponibles, dans l'attente d'une recherche sur sources primaires.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

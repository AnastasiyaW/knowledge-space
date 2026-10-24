---
title: "Vidu"
category: projects
tags: [project, vidu]
aliases: ["Vidu"]
level: 3
source_sha256: 0a69386393932110f35bf1e510e297607a8beebae0e5ac6c7d150c66875ed875
translation: machine
translated_at: '2026-10-24'
---
# Vidu {#vidu}

**Ligne de développement :** `project:vidu` · fil `vidu`  
**Événements :** 6 datés, 2024-04-27 → 2026-07-29 · **Recherche :** 2026-09-03 · confiance : moyenne

## Ce que c'est {#what-it-is}

Vidu — produit hébergé de génération vidéo de ShengShu, destiné aux créateurs et aux développeurs qui réalisent des plans contrôlés. — Texte vers vidéo, image vers vidéo, première et dernière image, et vidéo à références multiples. — Les fonctions de l'API couvrent aussi les modèles, l'extension, la synchronisation labiale, la synchronisation du mouvement, l'agrandissement et l'audio. Limite : le texte vers vidéo Q3 produit des séquences de 1 à 16 secondes ; la création est asynchrone et facturée en crédits. Verdict : l'utiliser pour les plans générés et la continuité assurée par des références, puis conserver le montage et le contrôle qualité habituels pour la séquence finale.

## Ligne de développement {#development-line}

- **2024-04-27 — Vidu fait ses débuts comme modèle de texte vers vidéo.** Le 2024-04-27, ShengShu Technology et Tsinghua ont présenté Vidu comme modèle de texte vers vidéo. La presse de l'époque décrivait la génération en un clic de vidéos 1080p d'une durée pouvant atteindre 16 secondes.
- **2024-08-29 — Vidu Studio devient le point d'accès commercial web documenté.** Au 2024-08-29, le registre renvoyait vers le site de Vidu Studio, présenté comme point d'accès commercial à Vidu. Les données disponibles identifient le site, mais n'établissent pas une version particulière de fonctionnalités à cette date.
- **2025-04-22 — La version Vidu Q1 ajoute les transitions de la première à la dernière image.** Le 2025-04-22, le registre de Vidu renvoyait à la version Vidu Q1 de ShengShu, publiée la veille. Cette version introduisait les transitions de la première à la dernière image, une musique de fond générée à partir du texte, des améliorations pour l'animation et une sortie 1080p de cinq secondes.
- **2025-07-10 — Vidu rend disponible un flux de travail Character-to-Video.** Au 2025-07-10, Vidu proposait un parcours de création Character-to-Video, qui établit une manière de créer une vidéo à partir de références. Les éléments disponibles ne permettent pas de déterminer si cette date correspond au lancement de la fonctionnalité, à la publication d'un tutoriel ou à la mise à jour d'un lien.
- **2025-09-21 — Les canaux russe et iPhone de Vidu entrent dans le registre.** Au 2025-09-21, le registre renvoyait vers le site web en langue russe de Vidu et vers la fiche de l'application iPhone. Ces liens attestent la disponibilité des canaux à cette date, mais n'établissent pas la date de lancement initiale de l'application.
- **2026-07-29 — La plateforme développeur de Vidu devient un canal produit documenté.** Le 2026-07-29, le registre renvoyait vers la plateforme développeur de Vidu et vers ses chemins de rétention, consignant un canal de distribution destiné aux développeurs à côté de l'outil de création web. Le guide et la page de rétention fournis n'ont pas pu être lus ; cette entrée n'attribue donc à la date aucune version précise de l'API, de modèle ou de tarification.

## Ce qui a changé {#what-changed}

Ligne de développement de Vidu : — 2024-04-27 : Vidu a été annoncé par l'université Tsinghua et ShengShu comme modèle de texte vers vidéo ; la presse de l'époque décrivait une sortie 1080p pouvant atteindre 16 secondes. — 2024-08-29 : le registre renvoyait vers vidu.studio ; des sources indépendantes indiquent que le produit web mondial était déjà en ligne au 2024-08-02, avec le texte vers vidéo et l'image vers vidéo. La page d'accueil ne fournit aucune modification archivée de fonctionnalités pour le 29 août lui-même. — 2024-09-16 : le registre renvoyait vers un parcours de création Text2Video, mais le lien enregistré est mal formé et l'ancien parcours ne peut plus être affiché aujourd'hui ; l'accès web au texte vers vidéo est attesté, sans qu'une version précise puisse être identifiée. — 2024-11-25 : le registre ne renvoyait à nouveau que la page d'accueil. Une reproduction datée de seconde main de l'annonce officielle de ShengShu sur WeChat situe Vidu 1.5 au 2024-11-13, avec un contrôle par référence multi-sujets à partir d'une à trois images ; il s'agit probablement d'un contexte de la période, et non d'une correspondance prouvée avec la publication du 25 novembre. — 2025-04-22 : Vidu Q1 a été lancé mondialement le 2025-04-21, ce qui a orienté le produit vers des transitions contrôlables, une saisie à plusieurs éléments et une génération de son synchronisée. — 2025-07-10 : le registre utilisait Character2Video, l'ancien flux de travail à référence de personnage. Son successeur actuel est Reference to Video, avec une à sept références pour contrôler le sujet, la scène, le style, la caméra et les effets. — 2025-09-21 : le registre a ajouté la fiche de l'application iPhone. Cela atteste une distribution mobile, et non une sortie de modèle ni une date de lancement vérifiée de l'application. — 2026-07-29 : le registre est passé aux adresses de la plateforme API et de rétention. L'ancien chemin de rétention envoie désormais vers la connexion puis une erreur 404 ; la politique de confidentialité publique de l'API est entrée en vigueur le 2026-04-29. Aucune modification de modèle ne peut être attribuée avec certitude à l'entrée du 29 juillet. — Constaté aujourd'hui : le journal de l'API de Vidu enregistre Reference-to-Video avec une à sept images le 2025-08-26, et des variantes Q3 sur ce point d'accès le 2026-04-13 ; la carte actuelle des modèles répertorie Q3, Q2 et Q1.

## Comment l'utiliser {#how-to-use-this}

Au 2026-09-03, utiliser vidu.com plutôt que vidu.studio comme point d'entrée canonique pour les créateurs ; choisir Q3, Q2, Q1 ou Vidu 2.0 selon le flux de travail, au lieu de traiter Vidu comme un outil uniquement texte vers vidéo ou uniquement Q1, et recourir à Reference to Video ou à la plateforme développeur lorsque ces flux sont nécessaires.

1. 1. Ouvrir Vidu et choisir le mode de génération qui correspond au plan : texte, image, référence ou première/dernière image.
  — <https://www.vidu.com/>
2. 2. Pour un personnage, un objet ou une scène récurrents, choisir Reference to Video ; importer une à sept images de référence, rédiger le prompt d'action, définir la résolution et le format, puis générer et télécharger.
  — <https://go.vidu.com/ai-reference-to-video>
3. 3. Pour un travail via l'API, se connecter à Vidu Platform, créer une clé d'API nommée, ajouter des crédits et consulter l'utilisation dans le tableau de bord.
  — <https://platform.vidu.com/docs/quick-start>
4. 4. Soumettre une requête de génération avec un modèle pris en charge, un prompt, une durée, un format, une résolution et une URL de rappel ; utiliser le texte vers vidéo lorsqu'aucune image d'ouverture n'est nécessaire.
  — <https://platform.vidu.com/docs/text-to-video>
5. 5. Conserver l'identifiant de la tâche et interroger son état jusqu'à ce qu'elle soit réussie ou échouée, avant de transmettre l'URL de création renvoyée à l'étape suivante du flux.
  — <https://platform.vidu.com/docs/tasks-list>
6. 6. Pour les lots, soumettre les requêtes dans la limite de concurrence de l'organisation et prévoir le temps d'attente en file, au lieu de considérer toutes les requêtes comme des rendus simultanés.
  — <https://platform.vidu.com/docs/usage-and-limits>

## Bonnes pratiques {#best-practices}

- Utiliser Reference to Video pour assurer la continuité d'identité et de scène sur plusieurs plans ; utiliser Image to Video pour animer une image unique ou un plan simple à images clés.
  — <https://go.vidu.com/ai-reference-to-video>
- Préparer un jeu de références comprenant les vues de face, de dos et en pied, ainsi que les accessoires ou arrière-plans récurrents ; rédiger des prompts explicites et documentés pour les personnages récurrents.
  — <https://www.vidu.com/blog/how-to-maintain-character-consistency-in-ai-videos>
- Traiter les plans générés comme des matériaux de montage : affiner les images clés ou les composites à l'extérieur lorsque la continuité exacte est importante.
  — <https://www.vidu.com/blog/how-to-maintain-character-consistency-in-ai-videos>
- Garder les clés d'API hors du navigateur et du code côté client ; Vidu met explicitement en garde contre leur exposition à cet endroit.
  — <https://platform.vidu.com/docs/quick-start>
- Utiliser les rappels ou l'interrogation des tâches, et dimensionner en fonction de la concurrence par défaut de cinq tâches à l'échelle de l'organisation, plutôt que de relancer les travaux en file d'attente.
  — <https://platform.vidu.com/docs/usage-and-limits>
- Ne recourir à la génération en heures creuses que si l'échéance peut tolérer un délai allant jusqu'à 48 heures ; c'est moins coûteux, mais différé.
  — <https://platform.vidu.com/docs/image-to-video>
- Filtrer en amont les requêtes susceptibles d'enfreindre la politique et ne pas soumettre à nouveau à répétition des entrées modérées, car des violations répétées peuvent entraîner la suspension d'un compte.
  — <https://platform.vidu.com/docs/content-moderation>

## Remplacé par ce qui suit {#superseded-by-this}

- 2024-04-27 — considérer Vidu comme une simple annonce de recherche en texte vers vidéo n'est plus valable ; c'est désormais un produit web et une API développeur proposant plusieurs modes de génération.
- 2024-08-29 et 2024-11-25 — considérer vidu.studio comme le point d'entrée stable n'est plus valable ; le site redirige désormais vers https://www.vidu.com/.
- 2025-04-22 — considérer Vidu Q1 comme le modèle le plus récent n'est plus valable ; la carte actuelle des modèles répertorie Q3, Q2 et Q1.
- 2025-07-10 — Character2Video comme nom de produit et flux de travail actuels est remplacé par Reference to Video.
- 2026-07-29 — considérer /retention comme un point de terminaison public de politique n'est plus valable ; l'ancien chemin mène désormais à la connexion puis à une erreur 404, tandis que la politique publique se trouve à /docs/privacy-policy.

## Toujours inconnu {#still-unknown}

- Le registre ne contient aucun texte source ; les entrées ne reposant que sur la page d'accueil ou sur un chemin ne peuvent donc pas être rattachées de manière fiable à une version précise, sans page archivée ni note de version.
- L'article WeChat original de 2024, la publication officielle sur X de 2025, les anciennes pages Text2Video et Character2Video, ainsi que la page Feishu n'ont pas pu être affichés lors de cette passe de recherche.
- Le lien du 2024-11-25 peut se rapporter à Vidu 1.5, mais le seul lien direct enregistré était la page d'accueil ; cette association est contextuelle, non prouvée.
- La fiche de l'App Store atteste une fiche mobile, mais non sa date de lancement ; elle indique SILICONWORLD PTE. LTD. comme fournisseur, alors que sa déclaration de confidentialité désigne ShengShu AI HK Limited, et le lien entre les deux n'est pas résolu ici.
- Les capacités et limites actuelles proviennent principalement de la documentation du fournisseur ; aucun test indépendant de la qualité, de la fiabilité, des licences ou de la disponibilité régionale n'a été effectué.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.vidu.com/ | Générateur de vidéos IA pour texte, image et vidéos de référence \| Vidu AI | 2026-09-03 |
| https://go.vidu.com/ai-reference-to-video | Reference to Video AI — Garder les personnages cohérents | Vidu AI | 2026-09-03 |
| https://platform.vidu.com/docs/quick-start | Démarrage rapide | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/function-list | Liste des fonctions | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/text-to-video | Texte vers vidéo | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/image-to-video | Image vers vidéo | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/tasks-list | Obtenir la liste des tâches | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/usage-and-limits | Utilisation et limites | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/content-moderation | Modération du contenu | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/update | Avis de mise à jour | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/model-map | Carte des modèles | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/privacy-policy | Politique de confidentialité | Vidu API | 2026-09-03 |
| https://www.vidu.com/blog/how-to-maintain-character-consistency-in-ai-videos | Comment maintenir la cohérence des personnages dans les vidéos IA | Vidu AI | 2026-09-03 |
| https://english.www.gov.cn/information/202404/27/content_WS662cfb3fc6d0868f4e8e6822.html | China-developed text-to-video large AI model unveiled in Beijing | 2026-09-03 |
| https://www.nsfc.gov.cn/p1/3381/4121/2826/68583.html | 我国自研视频大模型面向全球上线 | 2026-09-03 |
| https://www.aihub.cn/news/vidu-1-5/ | 生数科技正式发布Vidu 1.5版本，限时免费体验 | 2026-09-03 |
| https://www.prnewswire.com/news-releases/vidu-q1-model-launches-globally-offering-unmatched-realistic-vfx-capabilities-from-generating-cinematic-transitions-to-high-fidelity-sound-effects-with-just-a-few-simple-inputs-302433278.html | Vidu Q1 Model Launches Globally | 2026-09-03 |
| https://apps.apple.com/ru/app/vidu-ai-video-generator/id6742448149 | Vidu - Генератор Видео с ИИ | App Store | 2026-09-03 |
| https://mp.weixin.qq.com/s/xAEYGIoJ0EzhszfmXno3UA | Page source WeChat du lancement de Vidu (non affichée par le robot d'exploration) | 2026-09-03 |
| https://www.vidu.studio/ | Générateur de vidéos IA pour texte, image et vidéos de référence \| Vidu AI (redirection depuis vidu.studio) | 2026-09-03 |
| https://www.vidu.studio/create/text2video | Ancien parcours Vidu Text2Video (non affiché par le robot d'exploration) | 2026-09-03 |
| https://x.com/ViduAI_official/status/1914303116209697051 | Publication ViduAI_official (texte source indisponible pour le robot d'exploration) | 2026-09-03 |
| https://www.vidu.com/ru/create/character2video | Ancien parcours Vidu Character2Video (non affiché par le robot d'exploration) | 2026-09-03 |
| https://shengshu.feishu.cn/wiki/AYDDwwLuEiNYe9kWDWYctPxHn9Q | Page source du wiki Feishu de ShengShu (non accessible lors de cette lecture) | 2026-09-03 |
| https://platform.vidu.com/ | Page d'accueil de Vidu Platform (non affichée par le robot d'exploration) | 2026-09-03 |
| https://platform.vidu.com/retention | Chemin de rétention de Vidu Platform (redirige actuellement vers la connexion puis une erreur 404) | 2026-09-03 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:vidu`, fil `vidu`, 6 événements datés du 2024-04-27 au 2026-07-29.
- **Note pratique :** Au 2026-09-03, utiliser vidu.com plutôt que vidu.studio comme point d'entrée canonique pour les créateurs ; choisir Q3, Q2, Q1 ou Vidu 2.0 selon le flux de travail, au lieu de traiter Vidu comme un outil uniquement texte vers vidéo ou uniquement Q1, et recourir à Reference to Video ou à la plateforme développeur lorsque ces flux sont nécessaires.
- **Confiance :** moyenne. Les mentions datées de remplacement ci-dessus font foi pour déterminer ce qui est obsolète.

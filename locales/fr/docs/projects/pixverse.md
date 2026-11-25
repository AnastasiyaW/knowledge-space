---
title: "PixVerse — Disponibilité publique"
category: projects
date: 2025-04-29
tags: [pixverse, project, public-availability]
aliases: ["PixVerse"]
level: 2
source_sha256: c1715fe0325eb7d12d4eac5444f8e8429f24aa5b20df5977274848427040b189
translation: machine
translated_at: '2026-10-24'
---
# PixVerse — Disponibilité publique {#pixverse-public-availability}

**Ligne de développement :** `project:pixverse` · fil `public-availability`  
**Dernier événement :** 2025-04-29 · 2 entrées datées depuis le 2024-02-09 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

PixVerse est une plateforme propriétaire de génération de vidéos destinée aux créateurs et aux équipes.

- Génération de texte vers vidéo et d'image vers vidéo
- Modèles et contrôles de transitions
- Synchronisation labiale (lip sync)
- Accès par API et CLI

La version V6 génère des clips allant jusqu'à 15 secondes en 1080p, avec une logique multi-plans et un audio natif. Elle convient à la vidéo courte, mais les anciennes recommandations relatives aux versions V2 et V3 ne s'appliquent pas à la gamme actuelle.

## Ligne de développement {#development-line}

- **2024-02-09 — Site public de PixVerse.** Le 2024-02-09, PixVerse a été relié au site public pixverse.ai. Cette entrée a établi un point d'accès web public pour le projet. Le lien seul ne confirme ni une date de lancement, ni une version, ni des capacités.
- **2025-04-29 — Application web PixVerse et fiche iOS.** Le 2025-04-29, des références pointaient vers l'application web PixVerse et une fiche sur l'App Store iOS, en complément du site. Les parcours web et iOS étaient tous deux disponibles à cette date. Ces références ne confirment pas si l'un ou l'autre parcours a été lancé, a changé de version ou a gagné une capacité particulière à cette date.

## Évolutions {#what-changed}

- **2024-02-09 :** Le service web a servi de premier point d'entrée vers PixVerse. Des rétrospectives ultérieures situent la sortie de la V2, fondée sur l'architecture DiT, en février 2024.
- **2024-10-30 :** Après la sortie de la V3 le 29 octobre, la plateforme a ajouté LipSync, Effect, Extend, un outil Style mis à jour et 5 formats d'image (aspect ratios).
- **2025-04-29 :** PixVerse a publié un MCP pour l'intégration API. Cela a fait passer l'outil d'un générateur web grand public à une interface pour agents et code.

## Mode d'emploi {#how-to-use-this}

Évaluez PixVerse à partir de son application web et de sa fiche iOS au 2025-04-29, plutôt que sur le seul lien vers la page d'accueil. Vérifiez directement la disponibilité et les fonctionnalités actuelles.

1. Ouvrez PixVerse, sélectionnez V6, puis choisissez entre la génération de texte vers vidéo ou l'animation d'image.
  — <https://pixverse.ai/en/model/pixverse-v6>
2. Définissez la durée, la résolution et le format d'image en fonction du canal de diffusion avant de lancer la génération.
  — <https://pixverse.ai/en/model/pixverse-v6>
3. Décrivez le sujet, la scène, le mouvement de caméra, la lumière et l'audio, puis générez et vérifiez la stabilité du mouvement, la cohérence des personnages et le son.
  — <https://pixverse.ai/en/model/pixverse-v6>
4. Pour l'API, générez une clé API, envoyez un AI-trace-ID unique pour chaque tâche, conservez le video_id et récupérez le fichier dès que le statut passe de 5 à 1.
  — <https://docs.platform.pixverse.ai/quick-start-796052m0>

## Bonnes pratiques {#best-practices}

- Pour l'image vers vidéo, utilisez une seule image de référence claire, aux contours nets et à la composition lisible, et précisez directement le mouvement de caméra.
  — <https://pixverse.ai/en/model/pixverse-v6>
- Détaillez la scène de manière précise (sujet, décor, action, caméra, éclairage et son) ; des prompts vagues réduisent le contrôle sur le résultat.
  — <https://pixverse.ai/en/model/pixverse-v6>
- Conservez les traits essentiels du personnage d'un plan à l'autre, et vérifiez un court clip de test avant de générer une séquence complète.
  — <https://pixverse.ai/en/model/pixverse-v6>
- Ne réutilisez pas un AI-trace-ID : un identifiant identique ne créera pas une nouvelle tâche de génération.
  — <https://docs.platform.pixverse.ai/quick-start-796052m0>

## Remplacé par {#superseded-by-this}

- **2024-02-09 :** Considérer PixVerse comme un simple générateur web autonome est obsolète. Le service couvre désormais le web, l'API, la CLI, une interface pour agents et plusieurs modèles.
- **2024-10-30 :** Les recommandations pour la V3 ne reflètent pas les limites de la V6, soit jusqu'à 15 secondes en 1080p, avec une logique multi-plans et un son natif.
- **2025-04-29 :** Le MCP constituait une première étape d'intégration. La surface d'API actuelle comprend des modèles et fonctions plus récents, détaillés dans le journal des modifications.

## Points encore inconnus {#still-unknown}

- Le texte des 3 publications d'origine est absent : les sources ultérieures ne confirment le lien entre le 2024-02-09 et la date exacte de sortie de la V2 qu'au niveau du mois.
- Les liens d'origine app.pixverse.ai/home et de l'App Store ont renvoyé une erreur 404, et le lien raccourci t.co n'a pas pu être résolu : leur contenu est donc omis.
- Les informations sur la V3 reposent sur une synthèse secondaire citant WeChat, la publication WeChat principale n'ayant pas été directement accessible pour vérification.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://pixverse.ai/ | The Generative Core Behind Digital Worlds and Experiences | PixVerse | 2026-09-04 |
| https://en.tmtpost.com/post/7842608 | PixVerse Releases World's First Real-Time World Model for Interactive Video | TMTPOST | 2026-09-04 |
| https://www.aihub.cn/news/pixverse-v3/ | 爱诗科技发布PixVerse V3，模型能力重磅提高，多种玩法上线 | AIHub | 2026-09-04 |
| https://docs.platform.pixverse.ai/change-logs-906383m0 | Changelogs | PixVerse Platform Docs | 2026-09-04 |
| https://pixverse.ai/en/model/pixverse-v6 | PixVerse V6 AI Video Generator for 1080p Creative Workflows | PixVerse | 2026-09-04 |
| https://docs.platform.pixverse.ai/quick-start-796052m0 | Quick Start | PixVerse Platform Docs | 2026-09-04 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `project:pixverse`, fil `public-availability`, 2 événements datés du 2024-02-09 au 2025-04-29.
- **Note pratique :** Au 2025-04-29, évaluez PixVerse à partir de son application web et de sa fiche iOS, et non comme une simple référence à la page d'accueil ; vérifiez indépendamment la disponibilité et les capacités actuelles.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.

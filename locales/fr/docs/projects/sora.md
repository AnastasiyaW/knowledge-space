---
title: "Sora"
category: projects
date: 2025-09-30
tags: [project, sora, sora-access-expansion, sora-public-development]
aliases: ["Sora", "Sora 2"]
level: 4
source_sha256: 2ca1a62c4b1655791975cd267fc0edb7f40d8bca2f33eea8d646fdeae8facaa9
translation: machine
translated_at: '2026-10-24'
---
# Sora {#sora}

**Ligne de développement :** `project:sora` · fil `sora-public-development`  
**Dernier événement :** 2025-09-30 · 4 événements datés depuis 2024-02-15 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

Sora est la famille de modèles d'OpenAI permettant de générer, d'étendre et de modifier de courtes vidéos avec audio à partir de prompts textuels ou d'images.

- Texte vers vidéo : génère une vidéo à partir de prompts textuels.
- Génération guidée par image : crée une vidéo à partir d'images de référence.
- Persistance des personnages : réutilise des personnages cohérents d'une génération à l'autre.
- Extension : allonge des clips vidéo existants.
- Modification ciblée : modifie des sections spécifiques d'une vidéo.
- Téléchargement MP4 : exporte les générations terminées sous forme de fichiers vidéo.

Sora 2 et Sora 2 Pro prennent en charge des clips de 16 et 20 secondes ; l'API est dépréciée et sera arrêtée le 2026-09-24. Démarrer de nouveaux travaux de production avec cette API est provisoire et risqué ; les intégrations existantes nécessitent un plan de migration et une exportation des résultats.

## Ligne de développement {#development-line}

- **2024-02-15 — OpenAI a présenté publiquement Sora.** Le 2024-02-15, OpenAI a publié la page de présentation du projet Sora, marquant son introduction publique. Un lien social associé indiquait une discussion publique concomitante, sans contenu de publication fourni. Nous retenons ce fait comme premier jalon public du projet.
- **2024-12-09 — OpenAI a documenté les pays prenant en charge Sora.** Sora Turbo a été lancé sur sora.com pour les abonnés ChatGPT Plus et Pro, avec des clips allant jusqu'à 1080p et 20 secondes, storyboard, remix, blend et extension. Le déploiement excluait initialement le Royaume-Uni, la Suisse et l'EEE.
- **2024-12-09 — Sora a fait l'objet d'une présentation publique du service et de la vidéo.** Sora Turbo a été lancé sur sora.com pour ChatGPT Plus et Pro, prenant en charge des clips allant jusqu'à 1080p et 20 secondes, storyboard, remix, blend et extension. L'accès initial excluait le Royaume-Uni, la Suisse et l'EEE.
- **2025-09-30 — Sora a exposé une destination Explore sur ChatGPT.** Cette version a ajouté la génération vidéo et audio, le contrôle de réalisation multi-plans, les personnages et une application iOS sociale distincte. Sora 2 Pro proposait des exports 1080p de meilleure qualité.

## Évolutions {#what-changed}

- **2024-02-15 :** OpenAI a présenté Sora comme un transformeur de diffusion de recherche utilisant des patchs spatio-temporels. Le rapport technique confirmait des durées, résolutions et ratios d'aspect variables, avec un maximum revendiqué d'une minute de vidéo HD, mais aucun produit n'était disponible publiquement.
- **2024-03-14 :** Un entretien avec la CTO Mira Murati, publié le 2024-03-13, a confirmé une sortie publique prévue en 2024, tandis que les données d'entraînement, les erreurs et la sécurité restaient des questions ouvertes.
- **2024-12-09 :** L'aperçu de recherche est devenu le modèle de production Sora Turbo sur sora.com pour ChatGPT Plus et Pro. Au lancement, Plus incluait jusqu'à 50 vidéos en 480p ou moins en 720p, tandis que Pro offrait un volume dix fois supérieur. Il générait des clips allant jusqu'à 1080p et 20 secondes avec storyboard, remix, blend et extension. Le déploiement excluait initialement le Royaume-Uni, la Suisse et l'EEE.
- **2024-12-21 :** La publication X référencée n'a pas pu être vérifiée ; aucun ajout confirmé n'est donc retenu pour cette date.
- **2025-02-27 :** OpenAI a étendu la disponibilité de Sora à l'UE, au Royaume-Uni, à la Suisse, à la Norvège, au Liechtenstein et à l'Islande.
- **2025-09-30 :** OpenAI a publié Sora 2 avec génération vidéo et audio, contrôle multi-plans, personnages et une application iOS sociale autonome. L'API de production a introduit `sora-2` et `sora-2-pro` pour des clips de 16 et 20 secondes, Sora 2 Pro fournissant des exports 1080p de meilleure qualité.
- **2026-03-25 :** La page X référencée n'a pas pu se charger, ce qui ne permet aucune clarification indépendante et datée pour ce jour.
- **2026-04-26 :** OpenAI a mis fin aux versions web et mobile de Sora.
- **2026-09-05 :** L'API reste documentée mais dépréciée, son arrêt étant prévu le 2026-09-24.

## Mode d'emploi {#how-to-use-this}

Depuis le 2024-12-09, vérifiez la disponibilité de Sora par pays sur le service public plutôt que de supposer que l'annonce de février 2024 impliquait un accès universel.

1. Si vous avez besoin de nouvelles générations avant la date d'arrêt, vérifiez que la courte durée de vie de l'API convient à votre produit. Utilisez `sora-2` pour des itérations rapides et `sora-2-pro` pour l'export en 1080p.
  — <https://developers.openai.com/api/docs/guides/video-generation>
2. Créez une tâche asynchrone via `POST /videos`, en spécifiant le modèle, le prompt textuel, les dimensions et la durée.
  — <https://developers.openai.com/api/docs/guides/video-generation>
3. Recevez le résultat via le webhook `video.completed` ou `video.failed`, puis téléchargez le fichier MP4 avec `GET /videos/{video_id}/content`.
  — <https://developers.openai.com/api/docs/guides/video-generation>
4. Pour les contenus créés dans les anciennes versions web ou applicatives fermées de Sora, ouvrez `sora.chatgpt.com/sunset`, sélectionnez Export et attendez la confirmation par e-mail.
  — <https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation>

## Bonnes pratiques {#best-practices}

- Commencez par des clips courts et de faible résolution pour tester les prompts, le mouvement et la composition ; réservez les rendus en 1080p et plus longs aux exports finaux.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Précisez le type de plan, le sujet, l'action, l'environnement et l'éclairage afin d'éviter les détails indésirables.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Gérez les événements `video.failed` et écoutez les webhooks plutôt que d'interroger l'API en boucle dans les pipelines de production.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Ne soumettez pas de visages humains, de personnalités publiques, de personnages protégés par le droit d'auteur ni de musique, car les limites actuelles de l'API les rejettent.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Exportez vos travaux passés et évitez toute nouvelle dépendance à l'API Sora sans plan de migration avant le 2026-09-24.
  — <https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation>

## Remplacé par {#superseded-by-this}

- 2024-02-15 : la recherche sur Sora avec une génération revendiquée d'une minute ne décrit pas l'API Sora 2 disponible.
- 2024-12-09 : Sora Turbo et ses limites par niveau ont été remplacés par Sora 2 et Sora 2 Pro, et ne servent plus de référence pour l'intégration.
- 2025-09-30 : les instructions d'utilisation de Sora via les applications iOS ou web sont devenues obsolètes le 2026-04-26, date de fermeture de ces produits.
- 2026-09-24 : toute recommandation de créer de nouvelles dépendances vers l'API Sora Videos devient obsolète après l'arrêt prévu.

## Points encore inconnus {#still-unknown}

- Le contenu de la publication X du 2024-12-21, située à `https://x.com/rohanjamin/status/1870525134664278331?s=46&t=AR_orbfYSU6RyY_sYcnmhQ`, était indisponible pour vérification ; nous ne pouvons donc pas confirmer une extension d'accès ou une autre sortie.
- Le compte `https://x.com/soraofficialapp` n'a pas pu s'ouvrir le 2026-03-25 ; il peut être lié à une application ou à un identifiant distinct plutôt qu'à des changements de modèle ou d'API.
- La documentation officielle confirme le calendrier d'arrêt de l'API, mais les appels d'API en direct effectués lors de cette passe n'ont pas permis de le vérifier.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://openai.com/index/video-generation-models-as-world-simulators/ | Video generation models as world simulators | 2026-09-05 |
| https://www.youtube.com/watch?v=mAUpxN-EIgU | OpenAI's Sora Made Me Crazy AI Videos—Then the CTO Answered (Most of) My Questions | 2026-09-05 |
| https://openai.com/index/sora-is-here/ | Sora is here | 2026-09-05 |
| https://techcrunch.com/2025/02/27/openais-sora-is-now-available-in-the-eu-uk/ | OpenAI’s Sora is now available in the EU, UK | 2026-09-05 |
| https://openai.com/index/sora-2/ | Sora 2 is here | 2026-09-05 |
| https://developers.openai.com/api/docs/guides/video-generation | Video generation with Sora | 2026-09-05 |
| https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | What to know about the Sora discontinuation | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:sora`, fil `sora-public-development`, 4 événements datés du 2024-02-15 au 2025-09-30.
- **Note pratique :** Depuis le 2024-12-09, les praticiens doivent vérifier la disponibilité actuelle de Sora par pays et utiliser le service public de Sora plutôt que de supposer que l'annonce de février 2024 impliquait un accès universel.
- **Confiance :** élevée. Les remplacements datés ci-dessus font référence pour déterminer ce qui est obsolète.

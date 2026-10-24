---
title: "Perceptron Mk1 — Première publication publique"
category: projects
date: 2026-05-14
tags: [initial-public-release, perceptron-mk1, perceptron_mk1, project]
aliases: ["Perceptron Mk1"]
level: 3
source_sha256: 6518c2541f51f09ac3623e8fd2d16be1dce4eb15ea99d083d96f20c8c73f6666
translation: machine
translated_at: '2026-10-24'
---
# Perceptron Mk1 — Première publication publique {#perceptron-mk1-initial-public-release}

**Ligne de développement :** `project:perceptron-mk1` · fil `initial-public-release`  
**Dernier événement :** 2026-05-14 · 1 événement daté depuis le 2026-05-14 · **Recherche effectuée le :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

Perceptron Mk1 est un modèle fermé de vision et langage destiné aux équipes qui ajoutent l'analyse d'images et de vidéos à leurs API. Ce n'est pas un générateur de vidéos.

- Entrée multimodale : accepte le texte, les images et les vidéos.
- Sortie structurée : renvoie du texte accompagné d'annotations spatiales ou temporelles.
- Tâches visuelles : prend en charge les questions-réponses, l'OCR, la détection d'objets, la génération de légendes, le découpage de séquences vidéo à partir d'événements et les exemples visuels en contexte.
- Configuration : définit `vision_config` pour le raisonnement et l'ancrage typé.

## Ligne de développement {#development-line}

- **2026-05-14 — Présentation publique de Perceptron Mk1.** Le 2026-05-14, Perceptron Mk1 est apparu sur une page de présentation publique. L'article renvoie vers une démo, la documentation et une page de modèle OpenRouter, ce qui marque une étape de développement public importante. Ces liens ne suffisent pas à établir les capacités du modèle, sa conception technique ou les conditions d'accès.

## Ce qui a changé {#what-changed}

2026-05-14 — Perceptron a publié l'annonce de Mk1 ; l'historique officiel des versions date le lancement effectif au 2026-05-12. Cette version ajoute l'entrée image et vidéo, un contexte de 32K, le raisonnement, les spécifications du modèle et des guides vidéo. 2026-06-09 — Un point de terminaison dédié `/v1/detect` a été ajouté pour la détection ancrée directe à partir de catégories, d'exemples ou de requêtes exhaustives. 2026-06-15 — Une API Files a été ajoutée, permettant de réutiliser des références d'images et de vidéos téléversées dans plusieurs requêtes. 2026-06-22 — Les complétions de chat acceptent désormais des `video_frames` horodatés en ligne, comme alternative à une URL de vidéo.

## Mode d'emploi {#how-to-use-this}

Au 2026-05-14, commencez par la documentation publique et la démo, puis vérifiez la disponibilité actuelle sur OpenRouter ainsi que les conditions d'utilisation avant toute adoption.

1. Ouvrez la démo, connectez-vous si vous y êtes invité, et testez une requête concrète sur un échantillon avant l'intégration.
  — <https://www.perceptron.inc/demo>
2. Créez une clé d'API Perceptron, sélectionnez `perceptron-mk1`, puis utilisez le SDK Python, cURL ou un client compatible OpenAI.
  — <https://docs.perceptron.inc/>
3. Envoyez le texte accompagné d'un fichier JPEG, PNG, WebP, MP4 ou WebM à l'API de complétions de chat.
  — <https://docs.perceptron.inc/>
4. Définissez le contrat de résultat dès le départ : activez le mode de réflexion pour les tâches de raisonnement, ou demandez les annotations `point`, `box`, `polygon` ou `clip` pour obtenir une sortie ancrée.
  — <https://docs.perceptron.inc/perceptron-mk1/models/perceptron-mk1>
5. Pour les fichiers réutilisés dans plusieurs requêtes, téléversez-les une seule fois et référencez l'identifiant du fichier ; chaque fichier est limité à 128 MiB.
  — <https://docs.perceptron.inc/perceptron-mk1/guides/files>
6. En solution alternative routée, sélectionnez `perceptron/perceptron-mk1` via OpenRouter et consultez la fiche actuelle du modèle avant tout déploiement.
  — <https://openrouter.ai/perceptron/perceptron-mk1>

## Bonnes pratiques {#best-practices}

- Utilisez des requêtes observables et des demandes de sortie typées : noms de classes explicites pour la détection, et prédicat d'événement exact pour le découpage.
  — <https://docs.perceptron.inc/perceptron-mk1/best-practices/prompting-reference>
- Activez le mode de réflexion pour les questions-réponses textuelles, l'OCR, la génération de légendes et les extraits ; désactivez-le pour la localisation par `point`, `box` et `polygon`.
  — <https://docs.perceptron.inc/perceptron-mk1/models/perceptron-mk1>
- Pour les extraits vidéo, demandez le moment ou la plage exacts ; traitez un horodatage unique renvoyé comme un instant approximatif, et non comme un intervalle de durée nulle.
  — <https://docs.perceptron.inc/perceptron-mk1/capabilities/video-clipping>
- Limitez strictement les délais d'attente interactifs et `max_tokens` ; redimensionnez les médias côté client et respectez `Retry-After` avec une gigue après une erreur 429.
  — <https://docs.perceptron.inc/perceptron-mk1/guides/scaling>
- Stockez les clés dans des variables d'environnement ou un gestionnaire de secrets, supprimez les données personnelles des requêtes et des journaux conservés, et protégez les exemples annotés comme des images propriétaires.
  — <https://docs.perceptron.inc/perceptron-mk1/best-practices/security>

## Remplacé par {#superseded-by-this}

- 2026-06-22 — Aucun remplacement documenté : le journal public des modifications décrit les capacités de juin comme des ajouts, sans déprécier Mk1, les complétions de chat ni l'entrée `video_url`.

## Points encore inconnus {#still-unknown}

- L'article de lancement fourni, à l'adresse `https://www.perceptron.inc/blog/introducing-perceptron-mk1`, a renvoyé une erreur 403 lors de cette vérification ; son texte et son horodatage de publication n'ont donc pas été utilisés comme preuve principale.
- La date du 2026-05-14 correspond peut-être à la parution de l'article plutôt qu'au lancement effectif du produit ; l'indisponibilité du texte privé empêche de le confirmer.
- Aucune révision ultérieure de Mk1 n'apparaît dans le journal public des modifications après le 2026-06-22, bien que des changements de service non documentés restent possibles.
- La documentation officielle indique un contexte de 32K, tandis qu'OpenRouter affiche 33K ; OpenRouter précise par ailleurs 32 768 jetons, ce qui semble relever d'un arrondi plutôt que d'un conflit réel.
- Aucune version en chinois simplifié publiée par l'éditeur n'a été trouvée. La synthèse chinoise citée corrobore les affirmations de lancement sans valider de manière indépendante les performances annoncées par le fournisseur.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://www.perceptron.inc/demo | Démo Perceptron | 2026-09-06 |
| https://docs.perceptron.inc/ | Démarrage rapide - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/models/perceptron-mk1 | Perceptron Mk1 - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/changelog | Journal des modifications - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/best-practices/prompting-reference | Référence des requêtes - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/capabilities/video-clipping | Découpage vidéo - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/guides/files | Fichiers - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/guides/scaling | Guide de montée en charge - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/best-practices/security | Sécurité - Perceptron Docs | 2026-09-06 |
| https://openrouter.ai/perceptron/perceptron-mk1 | Perceptron Mk1 - API Pricing & Providers | OpenRouter | 2026-09-06 |
| https://b.coolplus.me/archives/ai--2026-05-13 | AI 新闻摘要 2026-05-13 - 酷加的博客 | 2026-09-06 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:perceptron-mk1`, fil `initial-public-release`, 1 événement daté, du 2026-05-14 au 2026-05-14.
- **Note pratique :** Au 2026-05-14, testez d'abord la documentation publique et la démo, puis vérifiez la disponibilité actuelle sur OpenRouter ainsi que les conditions d'utilisation avant toute adoption.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.

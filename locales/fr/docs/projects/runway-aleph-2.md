---
title: "Aleph 2.0 — Runway Aleph"
category: projects
date: 2026-05-23
tags: [project, runway-aleph, runway-aleph-2]
aliases: ["Aleph 2.0"]
level: 3
source_sha256: b8bb32f71a4710812a36a5db71e0ac2de98b73252e692a68ee6ef3662c591edb
translation: machine
translated_at: '2026-10-24'
---
# Aleph 2.0 — Runway Aleph {#aleph-20-runway-aleph}

**Ligne de développement :** `project:runway-aleph-2` · fil `runway-aleph`  
**Dernier événement :** 2026-05-23 · 1 événement daté depuis le 2026-05-23 · **Recherche effectuée le :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

Aleph 2.0 est l'éditeur in-context de Runway pour les séquences vidéo existantes, conçu pour les équipes qui doivent modifier un produit, un arrière-plan, un éclairage ou un style sans refaire le plan.

- Propagation des images clés sur les images pertinentes et dans les séquences multi-plans.
- Génération vidéo à partir d'une vidéo et d'un texte, avec une image de guidage facultative.
- Export en MP4, ProRes, séquence PNG ou SDR 10 bits ; le HDR nécessite une étape de conversion distincte.

Les entrées vont de 2 à 30 secondes, jusqu'à 1080p et 30 i/s ; le tarif de l'API Dev est de 28 crédits par seconde, avec un minimum de 56 crédits. Nous l'utilisons pour des retouches fidèles à la source ; testez les ajouts complexes en mouvement avant de promettre une livraison.

## Ligne de développement {#development-line}

- **2026-05-23 — Runway a présenté Aleph 2.0.** Le 2026-05-23, un lien produit daté, publié par Runway, identifiait Aleph 2.0 comme une étape de développement de la ligne Aleph. Ce lien nomme le produit, mais n'établit aucune capacité spécifique, aucune condition de disponibilité, aucun tarif ni aucune modification technique précise.

## Historique des changements {#what-changed}

- 2026-05-21 — Aleph 2.0 a été lancé avec Edit Studio pour les forfaits payants sur ordinateur et web, ajoutant la vidéo 1080p de 30 secondes, les modifications localisées pilotées par image et la propagation multi-plans.
- 2026-05-23 — La page produit fournie pour Aleph 2.0 consigne le périmètre actuel du produit, mais n'est pas datée et n'établit ni version distincte ni modification à cette date.
- 2026-06-02 — Aleph 2.0 est arrivé dans Runway Dev sous le nom `aleph2` pour l'édition vidéo-à-vidéo avec texte et images clés horodatées.
- 2026-06-22 — Aleph 2.0 est devenu disponible sous forme de nœud d'images clés horodatées dans Figma Weave.
- 2026-07-14 — Aleph 2.0 est devenu appelable via l'outil Edit Video de Runway MCP.
- 2026-07-30 — Runway Dev a supprimé `gen4_aleph` ; les appelants de l'API doivent migrer vers `aleph2`.
- 2026-08-10 — Edit Studio a ajouté l'export ProRes 4444 avec audio PCM et l'export en séquence PNG pour les modifications d'Aleph 2.0 sur le clip complet.
- 2026-08-20 — Aleph 2.0 a ajouté la livraison Rec.709 SDR 10 bits ; il ne rend toujours pas de HDR natif.

## Mode d'emploi {#how-to-use-this}

1. Ouvrez Edit Studio dans l'application web de bureau de Runway et partez d'un clip vidéo existant.
  — <https://runway.com/news/introducing-aleph-2-and-edit-studio>
2. Importez un clip de 2 à 30 secondes, jusqu'à 1080p et 30 i/s maximum.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
3. Choisissez une image clé où la cible est clairement visible : un plan large pour un changement d'environnement, un plan rapproché pour un changement de détail.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
4. Rédigez une action et la transformation souhaitée ; ajoutez une image de référence uniquement si elle aide à guider le sujet, le produit ou le style.
  — <https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide>
5. Prévisualisez et affinez la modification de l'image clé, sélectionnez la version retenue, puis générez la vidéo.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
6. Choisissez MP4, ProRes ou séquence PNG avant une génération sur le clip complet ; une modification sur une plage renvoie toujours du MP4.
  — <https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats>

## Bonnes pratiques {#best-practices}

- Commencez par une consigne courte et ciblée : un verbe d'action plus la transformation demandée ; ajoutez des détails uniquement si nécessaire.
  — <https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide>
- Prévisualisez l'image clé modifiée avant de payer la génération vidéo, et itérez sur la modification de l'image jusqu'à obtenir le bon résultat.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
- Utilisez Extra motion uniquement lorsque le nouveau mouvement est absent à la fois du clip d'origine et de l'image clé modifiée.
  — <https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide>
- Pour une extension du format d'image, utilisez un clip mono-plan sans coupure et vérifiez que la prévisualisation conserve la composition d'origine.
  — <https://help.runwayml.com/hc/en-us/articles/52264567609363-Expanding-a-video-s-aspect-ratio-with-Edit-Studio>
- Sélectionnez le format de livraison avant la génération : il ne peut pas être modifié ensuite, et ProRes ou la séquence PNG exigent une modification sur le clip complet.
  — <https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats>
- Considérez un test indépendant portant sur sept scénarios comme indicatif : il a montré qu'Aleph est le plus performant pour les visuels de packshot conservateurs, le texte et les retouches, tandis que les nouveaux sujets complexes en mouvement ont nécessité un nettoyage.
  — <https://journal.everypixel.com/runway-aleph-2-vs-gemini-omni>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-02 — Privilégiez `aleph2` plutôt que l'alias d'API obsolète `aleph2_alpha`.
- 2026-07-30 — `gen4_aleph` n'est plus un identifiant de modèle utilisable dans Runway Dev ; les appels échouent et doivent passer à `aleph2`.
- 2026-08-20 — Ne prévoyez pas de HDR natif avec Aleph 2.0 : sa sortie API actuelle est en SDR 10 bits, le HDR exigeant ensuite `/v1/video_to_hdr`.

## Points encore inconnus {#still-unknown}

- La page produit fournie n'est pas datée ; son contenu exact au 2026-05-23 ne peut donc pas être reconstitué. Le lancement daté est le 2026-05-21.
- La filiation reste non vérifiée, car plusieurs clés de sujet partagent le même historique ; ne revendiquez aucune relation de prédécesseur tant que cela n'a pas été examiné.
- Aucune documentation officielle d'Aleph 2.0 en chinois simplifié n'a été trouvée ; les résultats en chinois étaient des tutoriels tiers et n'ont pas servi aux affirmations centrales.
- Le guide générique d'Edit Studio de Runway indique encore que Expand est « bientôt disponible », alors que son guide dédié Expand Ratio le présente comme actif ; la date d'activation est inconnue.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://runwayml.com/product/aleph-2 | Aleph 2.0 | Runway (redirige vers runway.com) | 2026-09-06 |
| https://runway.com/product/aleph-2 | Aleph 2.0 | Runway | 2026-09-06 |
| https://runway.com/news/introducing-aleph-2-and-edit-studio | Présentation d'Aleph 2.0 et d'Edit Studio | 2026-09-06 |
| https://docs.dev.runwayml.com/api-details/api_changelog/ | Journal des modifications et mises à jour de l'API | Runway Dev | 2026-09-06 |
| https://runway.com/news/aleph-2-in-figma-weave | Aleph 2.0 est désormais dans Figma Weave | 2026-09-06 |
| https://runway.com/changelog | Mises à jour du produit et journal des modifications | Runway AI | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio | Créer avec Edit Studio | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide | Guide de rédaction de consignes pour Aleph 2.0 | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats | Exporter des vidéos aux formats ProRes et séquence PNG | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/52264567609363-Expanding-a-video-s-aspect-ratio-with-Edit-Studio | Étendre le format d'image d'une vidéo avec Edit Studio | 2026-09-06 |
| https://docs.dev.runwayml.com/guides/models/ | Modèles d'IA disponibles | Runway Dev | 2026-09-06 |
| https://docs.dev.runwayml.com/guides/pricing/ | Tarifs et coûts de l'API | Runway Dev | 2026-09-06 |
| https://journal.everypixel.com/runway-aleph-2-vs-gemini-omni | Runway Aleph 2 contre Gemini Video Omni | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:runway-aleph-2`, fil `runway-aleph`, 1 événement daté du 2026-05-23 au 2026-05-23.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

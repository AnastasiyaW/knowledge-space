---
title: "Snapchat"
category: projects
date: 2022-06-06
tags: [project, snapchat, snapchat-lenses, snapchat-lenses-and-filters, snapchat_crying_filter]
aliases: ["Snapchat"]
level: 2
source_sha256: 17efafda8744c864dc33894eae346c33db6e884e13c0d56cddc736f1c98cce0e
translation: machine
translated_at: '2026-10-24'
---
# Snapchat {#snapchat}

**Ligne de développement :** `project:snapchat` · fil `snapchat-lenses-and-filters`  
**Dernier événement :** 2022-06-06 · 1 événement daté depuis 2022-06-06 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Snapchat est une application d'appareil photo et la plateforme de RA Lens Studio, destinée aux utilisateurs, aux créateurs et aux développeurs : Face Lenses, World Lenses, modèles, scripting, SnapML, et publication vers Snapchat, Camera Kit et Spectacles.

Les Lenses soumises sont limitées à 8 Mo, avec une limite pouvant aller jusqu'à 10 Mo pour un modèle SnapML. Lens Studio permet de créer des effets de RA, et non de recréer un filtre viral précis et ancien.

## Ligne de développement {#development-line}

- **2022-06-06 — Un lien vers une Lens Snapchat a été consigné dans la ligne de développement.** Le 2022-06-06, un message a relayé l'URL d'une Lens Snapchat accompagnée d'une référence source. Les liens datés établissent l'existence d'un élément Snapchat lié aux Lenses dans cette ligne de développement, mais n'établissent ni sa fonctionnalité, ni son auteur, ni son statut de publication.

## Changements {#what-changed}

2022-05-12 — Crying Lens est devenu un effet de RA Snapchat largement commenté ; un rapport tiers indique son lancement le 6 mai et plus de 1 milliard d'utilisations au 12 mai.

2022-06-06 — Une page Snapchat Lens autonome a été citée, mais nous n'avons pas pu vérifier de manière indépendante son nom, son auteur ni ses fonctionnalités ; un lien avec Crying Lens reste non confirmé.

2022-12-06 — Snap a décrit la plateforme comme un moyen de publier des Lenses non seulement sur Snapchat, mais aussi via Camera Kit et pour Spectacles, et a indiqué plus de 3 millions de Lenses de RA créées.

## Mode d'emploi {#how-to-use-this}

Au 2022-06-06, les praticiens qui suivent les travaux sur Snapchat devraient inclure les URL de Lens comme surface concrète d'implémentation ou de distribution, tout en évitant de consigner dans le registre des affirmations non étayées sur le comportement ou le statut d'une Lens.

1. Connectez-vous à Lens Studio via Snapchat et choisissez un modèle pour une Lens simple, ou partez de zéro ; les outils mobiles et web s'adressent aux créateurs occasionnels, tandis que le bureau sert aux développements complexes.
  — <https://help.snapchat.com/hc/en-gb/articles/7012330991124-How-can-I-create-Lenses-for-Snapchat>
2. Définissez le nom, la plateforme et la taille du projet ; pour les Lenses mobiles, visez la limite de 8 Mo et vérifiez les contrôles de validation intégrés.
  — <https://developers.snap.com/lens-studio/publishing/configuring/configuring-project-info?lang=en-US>
3. Dans Lens Studio, cliquez sur Publish, créez ou sélectionnez une organisation et un Lens Folder, puis soumettez la Lens comme nouveau projet ou mettez à jour un projet existant.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>
4. Choisissez Upload and Publish pour publier dans Snapchat, ou Upload to Lens Folder si la Lens n'est nécessaire que pour une distribution ultérieure via Camera Kit ou Business Manager.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>

## Bonnes pratiques {#best-practices}

- Vérifiez les performances, la compatibilité des appareils et la conformité aux politiques avant la soumission : la publication fait l'objet de validations, de tests automatisés et d'une revue de contenu.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>
- Ne copiez pas de modèles ML ni de Lenses virales ; utilisez un aperçu clair, définissez des Lens Hints et compressez les ressources. La documentation recommande de viser une taille inférieure à 8 Mo.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>
- N'ajoutez pas de tags hors sujet : ils font l'objet d'une modération et n'améliorent pas la portée de la Lens.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>

## Remplacé par ce qui suit {#superseded-by-this}

- Avant le 2022-12-06 : l'idée que les Lenses ne sont destinées qu'à Snapchat ; Snap a également documenté l'utilisation d'effets de RA publiés dans Camera Kit et sur Spectacles.
- Avant Lens Studio 5 actuel : une approche exclusivement sur ordinateur pour tous les créateurs ; la prise en charge actuelle distingue le bureau pour les projets de RA complexes des outils mobiles et web pour la création personnelle.

## Points encore inconnus {#still-unknown}

- Crying Lens et le lien vers la Lens du 2022-06-06 peuvent constituer des sujets distincts au sein de Snapchat : la page Lens autonome n'était pas accessible pour un examen indépendant.
- Aucune source primaire de Snap indiquant une date de sortie pour Crying Lens n'a été trouvée ; le lancement du 6 mai et l'indicateur d'utilisation initial sont confirmés par une source secondaire du 12 mai 2022.
- Nous ne pouvons pas confirmer si la Lens spécifique du lien du 2022-06-06 est encore disponible aujourd'hui.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.bustle.com/life/how-to-use-crying-filter-snapchat-tiktok-instagram | How To Use The Crying Filter On Snapchat, TikTok, Instagram & More | 2026-09-05 |
| https://www.tmz.com/2022/05/12/snapchat-new-crying-face-filter-not-inspired-by-amber-heard/ | Snapchat's New Crying Face Filter NOT Inspired by Amber Heard | 2026-09-05 |
| https://help.snapchat.com/hc/en-gb/articles/7012330991124-How-can-I-create-Lenses-for-Snapchat | How can I create Lenses for Snapchat? | 2026-09-05 |
| https://developers.snap.com/lens-studio/home | Lens Studio | 2026-09-05 |
| https://developers.snap.com/lens-studio/publishing/configuring/configuring-project-info?lang=en-US | Configuring Project Settings | 2026-09-05 |
| https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens | Submitting Your Lens | 2026-09-05 |
| https://newsroom.snap.com/lens-fest-2022 | Lens Fest 2022: Celebrating Five Years of the Snap AR Community | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:snapchat`, fil `snapchat-lenses-and-filters`, 1 événement daté, du 2022-06-06 au 2022-06-06.
- **Note pratique :** Au 2022-06-06, les praticiens qui suivent les travaux sur Snapchat devraient inclure les URL de Lens comme surface concrète d'implémentation ou de distribution, tout en évitant de consigner dans le registre des affirmations non étayées sur le comportement ou le statut d'une Lens.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.

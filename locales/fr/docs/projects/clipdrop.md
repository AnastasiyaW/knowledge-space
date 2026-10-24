---
title: "Clipdrop"
category: projects
tags: [clipdrop, clipdrop-image-editing, project]
aliases: ["Clipdrop", "Clipdrop Relight"]
level: 3
source_sha256: 87589727ded8a35926419f0bef798e16270f97cd9f6b06e28f75bd591f6d5b65
translation: machine
translated_at: '2026-10-24'
---
# Clipdrop {#clipdrop}

**Ligne de développement :** `project:clipdrop` · fil `clipdrop-image-editing`  
**Événements :** 2 datés, 2022-09-09 → 2023-04-08 · **Recherché le :** 2026-09-04 · confiance : moyenne

## Description {#what-it-is}

Clipdrop est une boîte à outils d'images dans le navigateur destinée aux créateurs, qui combine la retouche de type Photoshop avec des générateurs web distincts.

- Suppression de l'arrière-plan et des objets : supprimer ou remplacer les arrière-plans, objets, personnes et textes
- Relighting : ajuster l'éclairage d'images existantes à l'aide de sources lumineuses virtuelles
- Amélioration d'image : agrandir, réduire le bruit, recadrer vers l'extérieur, redimensionner et générer à partir de texte
- Reimagine : générer des variations dans Jasper Document Editor avec un forfait Business

Clipdrop recense neuf outils web dans le navigateur ; le quota gratuit de Relight est de 20 utilisations par période de 24 heures.

Nous utilisons les outils web directs pour les retouches ponctuelles et Jasper pour le flux de travail Reimagine encore disponible.

## Ligne de développement {#development-line}

- **2022-09-09 — Clipdrop lance Relight.** Téléverser une image, positionner des sources lumineuses virtuelles, puis télécharger le résultat.
- **2023-04-08 — Clipdrop lance Stable Diffusion Reimagine.** Créer plusieurs nouvelles variations à partir d'une image source plutôt que de la reproduire à l'identique.

## Évolutions {#what-changed}

Clipdrop a fait passer l'édition d'images de pages web autonomes à une répartition entre les outils web de Clipdrop et l'éditeur de Jasper.

- 2022-09-09 — Relight était la fonctionnalité suivie : téléverser une image, positionner des sources lumineuses virtuelles, puis télécharger le résultat.
- 2023-04-08 — Stable Diffusion Reimagine était la fonctionnalité suivie : créer plusieurs nouvelles variations à partir d'une image source plutôt que de la reproduire à l'identique.
- 2026-09-04 — l'URL autonome de Reimagine redirige vers la page d'accueil de Clipdrop, et Reimagine est absent du catalogue web de Clipdrop, qui compte neuf outils ; Jasper le documente dans Document Editor, réservé aux utilisateurs du forfait Business.
- 2026-09-04 — le site de Clipdrop indique qu'InitML a été acquise par Stability en février 2023, puis vendue à Jasper en février 2024.

Le catalogue direct actuel conserve Relight mais pas Reimagine.

Les anciens liens vers Reimagine sont des points d'entrée obsolètes, et non la preuve que la fonctionnalité a disparu.

## Comment l'utiliser {#how-to-use-this}

Au 2023-04-08, nous suivons Clipdrop pour le relighting et les flux de réimagination Stable Diffusion, mais il faut vérifier la disponibilité et le comportement actuels avant de choisir l'un ou l'autre outil.

1. Ouvrir le catalogue direct de Clipdrop et choisir l'outil à fonction unique qui correspond à la retouche.
  — <https://clipdrop.co/tools>
2. Pour Relight, téléverser l'image source sur la page Relight.
  — <https://clipdrop.co/relight>
3. Déplacer les sources lumineuses virtuelles, évaluer le résultat et télécharger la version retenue.
  — <https://clipdrop.co/relight>
4. Pour Reimagine, ajouter ou téléverser une image dans Jasper Document Editor, la survoler, choisir Edit, puis sélectionner Reimagine ; Jasper indique qu'il s'agit d'un outil réservé au forfait Business.
  — <https://help.jasper.ai/hc/en-us/articles/25074326466971-How-to-Add-Images-to-Your-Jasper-Content>
5. Avant un lot, vérifier le quota actuel et le niveau de résolution ; Relight gratuit est indiqué à 20 utilisations par période de 24 heures, et Relight haute résolution en Pro à 1 000 par période de 24 heures.
  — <https://clipdrop.co/pricing>

## Bonnes pratiques {#best-practices}

- Utiliser Reimagine pour produire des variations, et non pour préserver l'original : il crée des images inspirées de l'entrée et ne reproduit pas ses pixels.
  — <https://stability.ai/news-updates/stable-diffusion-reimagine>
- Pour Cleanup, peindre légèrement au-delà de l'objet indésirable et inclure ses ombres ; Clipdrop indique qu'un masque plus large améliore la reconstruction.
  — <https://clipdrop.co/cleanup>
- Considérer l'ancienne URL autonome de Reimagine comme une redirection, puis utiliser Jasper Document Editor plutôt que de bâtir un flux de travail autour de l'ancienne page.
  — <https://help.jasper.ai/hc/en-us/articles/25074326466971-How-to-Add-Images-to-Your-Jasper-Content>
- Anticiper les volumes avant la production : le quota public gratuit pour Relight, Cleanup et l'agrandissement x2 est de 20 utilisations par période de 24 heures.
  — <https://clipdrop.co/pricing>

## Remplacé par ce document {#superseded-by-this}

- 2023-04-08 — le flux de travail autonome de la page web Stable Diffusion Reimagine est obsolète : son URL Clipdrop redirige désormais vers la page d'accueil ; l'accès documenté actuel passe par Jasper Document Editor > Edit > Reimagine, pour les utilisateurs du forfait Business.
- 2022-09-09 — considérer Clipdrop comme un produit indépendant d'InitML est obsolète : le site actuel de Clipdrop indique qu'InitML a été acquise par Stability en 2023 et vendue à Jasper en 2024.

## Points non élucidés {#still-unknown}

- La source fournie ne contenait aucun contenu vérifiable de manière indépendante, elle ne permet donc d'appuyer aucune affirmation.
- Aucune page officielle actuelle n'a permis de localiser une interface Reimagine autonome publique ni d'indiquer son quota actuel ; l'accès vérifié actuel est Jasper Document Editor, pour les utilisateurs du forfait Business.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://clipdrop.co/ | Create stunning visuals in seconds with AI. | 2026-09-04 |
| https://clipdrop.co/tools | Tools — Clipdrop | 2026-09-04 |
| https://clipdrop.co/relight | Clipdrop - Relight | 2026-09-04 |
| https://clipdrop.co/stable-diffusion-reimagine | Create stunning visuals in seconds with AI. (redirigé depuis Stable Diffusion Reimagine) | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-reimagine | Stable Diffusion Reimagine — Stability AI | 2026-09-04 |
| https://help.jasper.ai/hc/en-us/articles/25074326466971-How-to-Add-Images-to-Your-Jasper-Content | How to Add Images to Your Jasper Content — Jasper Help Center | 2026-09-04 |
| https://clipdrop.co/cleanup | Clipdrop - Cleanup | 2026-09-04 |
| https://clipdrop.co/pricing | Clipdrop - pricing | 2026-09-04 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:clipdrop`, fil `clipdrop-image-editing`, 2 événements datés, 2022-09-09 → 2023-04-08.
- **Note pratique :** Au 2023-04-08, les praticiens doivent considérer que Clipdrop dispose de références publiques datées pour les flux de travail de relighting et de réimagination Stable Diffusion, tout en vérifiant la disponibilité et le comportement actuels avant de choisir l'un ou l'autre outil.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

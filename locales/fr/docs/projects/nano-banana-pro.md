---
title: "Nano Banana Pro"
category: projects
date: 2025-11-26
tags: [nano-banana-pro, nano_banana, nano_banana_pro, project]
aliases: ["Nano Banana Pro"]
level: 3
source_sha256: 7c2d1d95e155f2e69f13faaa901f3475c03c87082f25f8a4613ab822538263ad
translation: machine
translated_at: '2026-10-24'
---
# Nano Banana Pro {#nano-banana-pro}

**Ligne de développement :** `project:nano-banana-pro` · fil `nano-banana-pro`  
**Dernier événement :** 2025-11-26 · 2 événements datés depuis 2025-11-20 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

Nano Banana Pro est le modèle d'image Gemini 3 Pro de Google, destiné aux créateurs et aux développeurs qui produisent des ressources visuelles complexes.

- Génère et modifie des images à partir d'entrées textuelles et d'images.
- Prend en charge l'ancrage avec Google Search, le rendu de texte, la localisation, la composition à partir de plusieurs références et une sortie pouvant atteindre 4K.
- L'identifiant API stable est `gemini-3-pro-image` ; il accepte 65 536 jetons en entrée et renvoie jusqu'à 32 768 jetons en sortie, avec jusqu'à six références d'objets haute fidélité, cinq références de personnages ou 14 références au total, selon l'usage.

## Ligne de développement {#development-line}

- **2025-11-20 — Google présente Nano Banana Pro.** Le 2025-11-20, Google a publié un article officiel sur son blog IA pour Nano Banana Pro et a rendu le modèle accessible dans Google AI Studio. Il s'agit du point d'introduction public de Nano Banana Pro dans cette ligne de développement.
- **2025-11-26 — Google publie des recommandations de prompts pour Nano Banana Pro.** Le guide de prompts associé est daté du 2025-11-20 et explique l'usage ; il n'annonce pas de révision.

## Changements {#what-changed}

- 2025-11-20 — Nano Banana Pro est lancé sous le nom de Gemini 3 Pro Image ; son point de terminaison de préversion dans l'API Gemini était `gemini-3-pro-image-preview`.
- 2025-11-26 — Aucune sortie distincte de modèle n'est confirmée : le guide de prompts associé est daté du 2025-11-20 et explique l'usage plutôt que d'annoncer une révision.
- 2025-12-01 — Search AI Mode étend Nano Banana Pro à davantage de pays anglophones pour les abonnés Google AI Pro et Ultra.
- 2025-12-17 — Search étend l'accès à Nano Banana Pro à davantage de personnes aux États-Unis.
- 2025-12-23 — Google annonce la disponibilité dans Gemini, Search AI Mode, NotebookLM, Workspace, Flow, Mixboard, AI Studio, Vertex AI et d'autres surfaces pour développeurs.
- 2026-04-20 — Les abonnements Google AI Pro et Ultra ajoutent des limites AI Studio plus élevées ainsi que l'accès à Nano Banana Pro.
- 2026-05-28 — `gemini-3-pro-image` devient l'identifiant API en disponibilité générale (GA) ; l'identifiant de préversion est déprécié, avec une date d'arrêt fixée au 25 juin 2026.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-11-20, il était possible d'utiliser Nano Banana Pro via Google AI Studio ; à partir du 2025-11-26, il convient de suivre les recommandations de prompts spécifiques au modèle publiées par Google.

1. Dans Gemini Apps : avec un forfait Google AI, créez une image avec Nano Banana 2 ou Nano Banana 2 Lite, puis choisissez More → Redo with Pro pour la passe détaillée ; le quota quotidien peut bloquer cette nouvelle génération.
  — <https://support.google.com/gemini/answer/14286560?hl=en-Documentation>
2. Dans Search AI Mode : sélectionnez Pro, choisissez Image, puis Create Images ; décrivez l'image ou importez-en une à modifier. La disponibilité est réservée à l'anglais et dépend du compte, de l'âge, du forfait et du pays.
  — <https://support.google.com/websearch/answer/16649374?co=GENIE.Platform%3DDesktop&hl=en-EN>
3. Dans l'API Gemini : appelez le modèle stable `gemini-3-pro-image` avec des entrées textuelles et/ou des images, puis traitez sa sortie d'image et de texte.
  — <https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image?authuser=00>
4. Modification : fournissez une image accompagnée d'une demande de modification directe, puis poursuivez la même conversation pour les modifications suivantes.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>
5. Livraison : définissez `response_format.type` sur `image` et demandez les valeurs `aspect_ratio` et `image_size` nécessaires lorsque le cadrage ou la résolution de sortie comptent.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>

## Bonnes pratiques {#best-practices}

- Choix du modèle : réservez-le aux ressources et instructions professionnelles complexes ; utilisez Nano Banana 2 lorsque l'équilibre général entre coût et latence est plus important.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>
- Prompts : précisez le sujet, la composition, l'action, le lieu, le style et une instruction de modification directe.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Composition : indiquez explicitement le format, la caméra, l'éclairage, l'emplacement du texte et les contraintes factuelles.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Références : nommez le rôle de chaque image importée, par exemple la pose, le style ou l'arrière-plan.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Modifications : itérez dans une conversation multi-tours plutôt que de recommencer à chaque révision.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>
- Sorties : vérifiez de manière indépendante les petits textes, l'orthographe, les faits présents dans les schémas, les traductions, les mélanges complexes et la cohérence des personnages avant toute utilisation.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Entrées : n'importez que des images pour lesquelles vous disposez des droits nécessaires.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>

## Remplacé par {#superseded-by-this}

- 2026-05-28 — Utilisez `gemini-3-pro-image-preview` pour une nouvelle intégration de l'API Nano Banana Pro. Remplacé par le point de terminaison GA `gemini-3-pro-image` ; le point de terminaison de préversion devait être arrêté le 2026-06-25.

## Inconnues restantes {#still-unknown}

- Le lien profond historique vers AI Studio `https://aistudio.google.com/prompts/new_chat?model=nano-banana-pro` nécessite une connexion ; sa présélection de modèle et son quota actuels n'ont donc pas pu être vérifiés à partir d'une page publique.
- L'accès grand public varie selon le compte, le forfait Google AI, la langue, l'âge, le pays et les quotas quotidiens susceptibles d'évoluer ; cela n'établit pas l'éligibilité d'un compte particulier.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://blog.google/technology/ai/nano-banana-pro/ | Présentation de Nano Banana Pro | 2026-09-04 |
| https://blog.google/products/gemini/prompting-tips-nano-banana-pro/ | 7 conseils pour tirer le meilleur parti de Nano Banana Pro | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/changelog | Notes de version | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image?authuser=00 | Gemini 3 Pro image | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/image-generation?authuser=00 | Génération d'images | Gemini API | Google AI for Developers | 2026-09-04 |
| https://blog.google/products-and-platforms/products/search/gemini-3-ai-mode-more-countries/ | Gemini 3 et Nano Banana Pro dans la Recherche arrivent dans davantage de pays à travers le monde. | 2026-09-04 |
| https://blog.google/products-and-platforms/products/search/google-ai-mode-update-gemini-3-flash/ | Gemini 3 Flash se déploie dans le monde entier dans la Recherche Google | 2026-09-04 |
| https://blog.google/products-and-platforms/products/gemini/where-to-use-nano-banana-pro/ | Où utiliser Nano Banana Pro | 2026-09-04 |
| https://blog.google/innovation-and-ai/technology/developers-tools/google-one-ai-studio/ | Commencez à coder avec AI Studio grâce à votre abonnement Google AI. | 2026-09-04 |
| https://support.google.com/gemini/answer/14286560?hl=en-Documentation | Générer et modifier des images avec Gemini Apps - Ordinateur - Aide Gemini Apps | 2026-09-04 |
| https://support.google.com/websearch/answer/16649374?co=GENIE.Platform%3DDesktop&hl=en-EN | Créer et modifier des images dans la Recherche Google - Ordinateur - Aide Recherche Google | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:nano-banana-pro`, fil `nano-banana-pro`, 2 événements datés du 2025-11-20 au 2025-11-26.
- **Note pratique :** À partir du 2025-11-20, les praticiens pouvaient utiliser Nano Banana Pro via Google AI Studio ; à partir du 2025-11-26, ils doivent suivre les recommandations de prompts spécifiques au modèle publiées par Google.
- **Confiance :** élevée. Les entrées « Remplacé par » datées font foi pour ce qui est obsolète.

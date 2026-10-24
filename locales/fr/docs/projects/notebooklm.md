---
title: "NotebookLM"
category: projects
date: 2025-07-30
tags: [google_io_2024, notebooklm, notebooklm-development, project]
aliases: ["NotebookLM"]
level: 3
source_sha256: fa74b0873bf3b40203099e8f73ed2a87996fb9737d856701a9fdeb9ada171904
translation: machine
translated_at: '2026-10-24'
---
# NotebookLM {#notebooklm}

**Ligne de développement :** `project:notebooklm` · fil `notebooklm-development`  
**Dernier événement :** 2025-07-30 · 1 événement daté depuis 2025-07-30 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

NotebookLM, désormais appelé Gemini Notebook, est l'espace de travail de Google destiné aux étudiants, aux analystes et aux équipes, qui travaillent exclusivement à partir de documents sélectionnés.

- Chat : répond à partir des sources sélectionnées, avec citations en ligne.
- Studio : crée des rapports, des tableaux de données, des cartes mentales, des fiches de révision, des quiz, des cartes mentales, des aperçus audio/vidéo, des infographies et des présentations.
- Limites : 50 sources par carnet gratuit, jusqu'à 500 000 mots ou 200 Mo chacune, avec une utilisation basée sur le calcul, variable selon l'abonnement.

## Ligne de développement {#development-line}

- **2025-07-30 — NotebookLM a introduit les Video Overviews et des améliorations de Studio.** Google a mis à jour NotebookLM le 2025-07-30 avec les Video Overviews et des améliorations de Studio, ce qui permet de produire plusieurs résultats par carnet, et non plus un seul artefact par type.

## Évolutions {#what-changed}

- 2023-07-12 — NotebookLM a été lancé à partir de Project Tailwind, sous la forme d'un petit déploiement de Google Labs aux États-Unis, pour répondre à partir de documents sélectionnés, avec citations.
- 2024-05-14 — L'événement I/O a présenté en avant-première les Audio Overviews, qui utilisent Gemini pour transformer les sources importées en une discussion verbale interactive.
- 2025-05-19 — Les applications iOS et Android ont ajouté les Audio Overviews hors ligne, l'interaction avec l'hôte et la capture de sources via la feuille de partage.
- 2025-07-30 — Les Video Overviews et un Studio amélioré ont permis d'enregistrer plusieurs résultats au lieu d'un seul artefact par type.
- 2025-08-25 — Les Video Overviews ont été étendues à plus de 80 langues, avec des Audio Overviews plus longues dans ces langues.
- 2026-03-04 — Les Cinematic Video Overviews ont ajouté un format en anglais, réservé aux abonnés Google AI Ultra de 18 ans et plus, réalisé avec Gemini 3, Nano Banana Pro et Veo 3.
- 2026-04-08 — Les carnets ont été synchronisés entre Gemini et NotebookLM, en reliant la structure des projets et le contexte des conversations entre les deux applications.
- 2026-07-03 — Les Short Video Overviews ont été annoncées comme des explications verticales d'environ 60 secondes à partir des sources, l'annonce sous-jacente étant datée du 2026-06-30.
- 2026-07-16 — Le produit a été renommé Gemini Notebook, a reçu un ordinateur cloud sécurisé pour l'exécution native de code sur les offres éligibles, et a élargi son rôle au sein de l'écosystème Google.
- 2026-09-02 — L'utilisation est passée à des limites basées sur le calcul, qui tiennent compte de la complexité du prompt et des fonctionnalités, du modèle, de la longueur des conversations et du quota.

## Comment l'utiliser {#how-to-use-this}

À partir du 2025-07-30, les praticiens devraient envisager les Video Overviews et Studio lorsqu'ils choisissent les résultats de NotebookLM et les flux de travail de l'espace de travail, sous réserve de leur disponibilité dans leur compte.

1. Ouvrez notebook.google.com, créez un carnet par projet et ajoutez l'ensemble de sources qui définit les réponses attendues.
  — <https://support.google.com/gemininotebook/answer/16206563>
2. N'importez que des contenus que vous êtes autorisé à utiliser : fichiers pris en charge, contenus Google, URL web, vidéos YouTube dotées de sous-titres publics ou conversations Gemini sélectionnées.
  — <https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-GB>
3. Dans Chat, sélectionnez les sources pertinentes, posez une question précise et ouvrez chaque citation en ligne pour lire l'extrait cité dans son contexte.
  — <https://support.google.com/gemininotebook/answer/16179559?hl=en&ref_topic=16164070>
4. Dans Studio, générez un rapport ou un tableau de données à partir de l'ensemble de sources, puis exportez-le vers Docs ou Sheets si cela est pertinent.
  — <https://support.google.com/gemininotebook/answer/16206563>
5. Pour une relecture visuelle, créez une Video Overview et définissez son format, sa langue et son prompt de pilotage avant la génération.
  — <https://support.google.com/gemininotebook/answer/16454555?hl=en&ref_topic=16164070>
6. Si vous travaillez aussi avec Gemini, utilisez sa vue des carnets inter-applications pour assurer la continuité, mais conservez les conclusions strictement ancrées dans les sources dans Gemini Notebook.
  — <https://support.google.com/gemininotebook/answer/17003757?hl=en&ref_topic=16164070>

## Bonnes pratiques {#best-practices}

- Réservez un carnet à un projet délimité : les carnets sont indépendants et ne peuvent pas accéder aux informations les uns des autres.
  — <https://support.google.com/gemininotebook/answer/16206563>
- Sélectionnez les sources pertinentes et posez des questions ciblées ; examinez les extraits cités dans leur contexte plutôt que de faire confiance à des réponses trop fluides.
  — <https://support.google.com/gemininotebook/answer/16179559?hl=en&ref_topic=16164070>
- Considérez la vidéo générée comme une aide à l'étude, et non comme une preuve définitive : les voix et les visuels peuvent présenter des dysfonctionnements ou énoncer des faits de manière inexacte.
  — <https://support.google.com/gemininotebook/answer/16454555?hl=en&ref_topic=16164070>
- Considérez le partage comme un accès aux données sources : les lecteurs peuvent consulter les sources partagées, et Chat View ne révoque pas entièrement cet accès.
  — <https://support.google.com/gemininotebook/answer/16206563>
- Séparez l'ancrage de Gemini et celui de Gemini Notebook : Gemini Notebook s'appuie strictement sur les sources, tandis que Gemini peut accéder à la recherche et aux outils.
  — <https://support.google.com/gemininotebook/answer/17003757?hl=en&ref_topic=16164070>
- Planifiez en tenant compte de quotas variables, basés sur le calcul : les limites actuelles peuvent se réinitialiser toutes les cinq heures, jusqu'à atteindre la limite hebdomadaire.
  — <https://support.google.com/gemininotebook/answer/17670842?hl=en&ref_topic=16164070>
- Laissez les Video Overviews se générer de manière asynchrone et revenez les consulter plus tard : la génération peut prendre plus de 30 minutes.
  — <https://support.google.com/gemininotebook/answer/16454555?hl=en&ref_topic=16164070>

## Remplacé par ce qui suit {#superseded-by-this}

- 2025-07-29 — Le flux de travail Studio à un résultat par type.
- 2025-08-25 — Les Video Overviews uniquement en anglais.
- 2026-07-16 — NotebookLM comme nom officiel actuel du produit.
- 2026-09-02 — Les tableaux de quotas numériques fixes comme méthode stable de planification de l'utilisation.

## Points encore inconnus {#still-unknown}

- Une page de statut liée au 2026-07-03 n'a pas pu être récupérée. Son identifiant de statut encode un horodatage du 2026-06-30, mais l'attribution par des sources secondaires ne permet pas de vérifier le libellé d'origine.
- Aucune annonce datée et émanant de Google sur NotebookLM n'a été trouvée pour les affirmations de 2024 concernant la version du modèle, le nombre de pays ou l'augmentation de la limite de sources.
- La disponibilité exacte varie selon le compte, l'abonnement, la région et l'âge ; Google indique que l'accès aux fonctionnalités et les limites peuvent changer.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://blog.google/innovation-and-ai/technology/ai/notebooklm-google-ai/ | Introducing NotebookLM | 2026-09-04 |
| https://blog.google/intl/en-africa/products/explore-get-answers/google-io-2024-an-io-for-a-new-generation/ | Google I/O 2024: An I/O for a new generation | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/google-io-2024-100-announcements/ | 100 things we announced at I/O 2024 | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/notebooklm-app/ | Understand anything, anywhere with the new NotebookLM app | 2026-09-04 |
| https://blog.google/technology/google-labs/notebooklm-video-overviews-studio-upgrades/ | What’s new in NotebookLM: Video Overviews and an upgraded Studio | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-labs/notebook-lm-audio-video-overviews-more-languages-longer-content/ | NotebookLM's Video Overviews are now available in 80 languages | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/notebooklm/generate-your-own-cinematic-video-overviews-in-notebooklm/ | Generate your own Cinematic Video Overviews in NotebookLM. | 2026-09-04 |
| https://blog.google/intl/en-ie/products/notebooks-gemini-notebooklm/ | Try notebooks in Gemini to easily keep track of projects | 2026-09-04 |
| https://9to5google.com/2026/06/30/notebooklm-short-video-overviews/ | NotebookLM adding Short Video Overviews with Nano Banana 2 Lite | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/ | Start building with Nano Banana 2 Lite and Gemini Omni Flash | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/ | NotebookLM is now Gemini Notebook | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16164461?hl=en | Learn about Gemini Notebook | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16206563 | Create a notebook in Gemini Notebook | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-GB | Add or discover new sources for your notebook | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16179559?hl=en&ref_topic=16164070 | Use chat in Gemini Notebook | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16454555?hl=en&ref_topic=16164070 | Generate Video Overviews in Gemini Notebook | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/17670842?hl=en&ref_topic=16164070 | Manage your Gemini Notebook usage limits | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/17003757?hl=en&ref_topic=16164070 | Notebooks in Gemini Apps | 2026-09-04 |
| https://notebooklm.google/ | Gemini Notebook | AI Research Tool & Thinking Partner | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:notebooklm`, fil `notebooklm-development`, 1 événement daté, du 2025-07-30 au 2025-07-30.
- **Note pratique :** À partir du 2025-07-30, les praticiens devraient envisager les Video Overviews et Studio lorsqu'ils choisissent les résultats de NotebookLM et les flux de travail de l'espace de travail, sous réserve de leur disponibilité dans leur compte.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.

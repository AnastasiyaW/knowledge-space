---
title: "Fooocus"
category: projects
date: 2023-09-12
tags: [fooocus, fooocus-development, fooocus_v2, project]
aliases: ["Fooocus"]
level: 3
source_sha256: 2b5d416246237494ff95b6235c0d4fb3f1c9cc513b895f4e459b4ac948d9d967
translation: machine
translated_at: '2026-10-24'
---
# Fooocus {#fooocus}

**Ligne de développement :** `project:fooocus` · fil `fooocus-development`  
**Dernier événement :** 2023-09-12 · 2 événements datés depuis 2023-08-13 · **Recherché :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

Fooocus est un générateur d'images SDXL local et hors ligne, destiné aux créatifs qui souhaitent un flux de travail plus simple, centré sur le prompt, que ComfyUI.

- Texte vers image avec styles et expansion de prompt.
- Variations, upscale, inpaint/outpaint, Image Prompt et échange de visages.
- Préréglages général, réaliste et anime.

## Ligne de développement {#development-line}

- **2023-08-13 — Dépôt Fooocus et artefact de version Windows liés.** Le 2023-08-13, nous avons lié Fooocus à son dépôt GitHub et à l'archive de version Windows 64 bits. Cela consigne un artefact distribuable public dans la ligne de développement de Fooocus.
- **2023-09-12 — Discussion de développement de Fooocus liée.** Le 2023-09-12, nous avons lié la ligne de développement de Fooocus à la discussion GitHub n° 347. Cela relie le fil à l'historique de l'ère Fooocus v2, bien que nous n'ayons pas examiné le contenu de la discussion elle-même.

## Ce qui a changé {#what-changed}

2023-08-13 — Fooocus est passé à son état public v1. Le journal des mises à jour indique que la version v1.0.15 est disponible publiquement.

2023-09-12 — Fooocus 2.0.0 a remplacé le moteur de traitement de texte, ajouté la gestion de prompts multi-styles, et renommé Prompt Expansion et Raw Mode en Fooocus V2. Le mainteneur a rapporté que V2 surpassait V1 avec 87/100 résultats par défaut et 81/100 tests de compréhension de prompt, évalués par deux personnes.

2026-09-04 (trouvé aujourd'hui, pas une date de sortie) — l'amont décrit Fooocus comme SDXL uniquement, LTS limité et correctifs de bogues uniquement. La version v2.5.5 est actuellement marquée Latest et contient un correctif d'inpaint pour Colab.

## Comment l'utiliser {#how-to-use-this}

Depuis le 2023-08-13, utilisez le dépôt GitHub public et l'artefact de distribution Windows. Depuis le 2023-09-12, consultez la discussion de développement liée avant de vous fier au comportement de l'ère v2.

1. Vérifiez qu'un flux de travail SDXL convient à la tâche ; Fooocus n'est pas la voie maintenue pour Flux ni pour d'autres architectures plus récentes.
  — <https://github.com/lllyasviel/Fooocus>
2. Sous Windows, utilisez le téléchargement officiel, extrayez-le et lancez `run.bat`. Sous Linux, clonez le dépôt, installez les dépendances épinglées dans Conda ou dans un venv Python 3.10, puis lancez `entry_with_update.py`.
  — <https://github.com/lllyasviel/Fooocus>
3. Laissez le premier lancement télécharger les modèles sélectionnés, puis utilisez le préréglage par défaut, anime ou réaliste dans l'interface ou avec `--preset anime` / `--preset realistic`.
  — <https://github.com/lllyasviel/Fooocus>
4. Rédigez un prompt, choisissez des styles ou les réglages avancés si nécessaire, et utilisez Input Image pour les workflows de variation, upscale, inpaint/outpaint ou Image Prompt.
  — <https://github.com/lllyasviel/Fooocus>
5. Gardez l'interface en local sauf si un accès distant est nécessaire. Pour `--listen` ou `--share`, ajoutez un `auth.json`, car l'accès n'est pas authentifié par défaut.
  — <https://github.com/lllyasviel/Fooocus>

## Bonnes pratiques {#best-practices}

- Installez uniquement depuis le dépôt GitHub officiel ou ses téléchargements liés ; l'amont avertit que les sites web Fooocus au nom similaire sont frauduleux.
  — <https://github.com/lllyasviel/Fooocus>
- Traitez Fooocus comme un outil SDXL stable. Pour Flux ou les travaux sur des modèles plus récents, suivez la recommandation de l'amont d'utiliser plutôt WebUI Forge, ComfyUI ou SwarmUI.
  — <https://github.com/lllyasviel/Fooocus>
- Lors d'un changement de préréglage, laissez les modèles requis finir de se télécharger. Utilisez `--always-download-new-model` si un préréglage doit récupérer son modèle manquant plutôt que de revenir silencieusement à un ancien modèle.
  — <https://github.com/lllyasviel/Fooocus>
- Protégez toute interface exposée au réseau avec `auth.json`. Ni `--listen` ni `--share` n'activent l'authentification par défaut.
  — <https://github.com/lllyasviel/Fooocus>
- Privilégiez les proportions d'image fournies plutôt que des résolutions personnalisées arbitraires, sauf si le codage positionnel de SDXL est bien compris.
  — <https://github.com/lllyasviel/Fooocus/blob/main/update_log.md>

## Remplacé par ceci {#superseded-by-this}

- 2023-08-13 — la version v2.5.5 actuellement marquée Latest remplace l'état public v1.
- 2023-09-12 — Fooocus 2.0 et son style `Fooocus V2` remplacent les consignes de traitement de texte V1 ainsi que le libellé d'interface « Prompt Expansion and Raw Mode » ; désactivez ce style pour tenter de reproduire une sortie V1.
- 2026-09-04 (trouvé aujourd'hui) — attendre un support officiel de Flux ou d'une autre nouvelle architecture par Fooocus est aujourd'hui obsolète : l'amont est en LTS avec correctifs uniquement et oriente les utilisateurs de Flux ailleurs.

## Toujours inconnu {#still-unknown}

- Nous n'avons pas inspecté l'archive Windows directe à l'adresse https://github.com/lllyasviel/Fooocus/releases/download/release/Fooocus_win64_1-1-10.7z ; son contenu, sa somme de contrôle et la version exacte du packaging restent non confirmés.
- Le journal des mises à jour amont indique que la version v1.0.15 est disponible publiquement sans date calendaire ; son horodatage exact de sortie reste donc non confirmé.
- Aucun produit distinct ne se cache derrière `fooocus` et `fooocus_v2` : la discussion officielle identifie ce dernier comme Fooocus 2.0.0, et non comme un sujet différent.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/lllyasviel/Fooocus | Dépôt Fooocus et README | 2026-09-04 |
| https://github.com/lllyasviel/Fooocus/discussions/347 | [Mise à jour majeure] Fooocus 2.0.0 — Discussion #347 | 2026-09-04 |
| https://github.com/lllyasviel/Fooocus/blob/main/update_log.md | Journal des mises à jour de Fooocus | 2026-09-04 |
| https://github.com/lllyasviel/Fooocus/releases/tag/v2.5.5 | Version Fooocus v2.5.5 | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:fooocus`, fil `fooocus-development`, 2 événements datés du 2023-08-13 au 2023-09-12.
- **Note pratique :** Depuis le 2023-08-13, les praticiens pouvaient considérer que Fooocus disposait d'un emplacement source GitHub publiquement lié et d'un artefact de distribution Windows ; depuis le 2023-09-12, ils doivent consulter la discussion de développement liée avant de se fier au comportement de l'ère v2.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour déterminer ce qui est obsolète.

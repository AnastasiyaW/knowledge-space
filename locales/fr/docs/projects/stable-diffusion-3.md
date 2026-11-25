---
title: "Stable Diffusion 3"
category: projects
date: 2024-02-22
tags: [project, stable-diffusion-3]
aliases: ["Stable Diffusion 3", "Stable Diffusion 3 Medium"]
level: 2
source_sha256: f285f052d3e242d89cf829682aaab4f9c7738883573c2c590297a330558ee807
translation: machine
translated_at: '2026-10-24'
---
# Stable Diffusion 3 {#stable-diffusion-3}

**Ligne de développement :** `project:stable-diffusion-3` · fil `stable-diffusion-3`  
**Dernier événement :** 2024-02-22 · 1 événement daté depuis 2024-02-22 · **Vérifié le :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

Stable Diffusion 3 est une famille de modèles text-to-image MMDiT de Stability AI, disponibles pour ComfyUI, Diffusers et via API. Fonctionnalités : génération à partir de texte, compositions complexes, typographie, image-to-image via les pipelines compatibles. SD3 Medium est un modèle de 2B paramètres, à accès restreint (gated) ; les organisations à usage commercial dont le chiffre d'affaires annuel dépasse 1 M$ doivent disposer d'une licence Enterprise. Verdict : SD3 Medium est disponible, mais Stability AI a elle-même reconnu que la première version ouverte de la série n'avait pas répondu aux attentes, et a publié SD 3.5 comme lignée de remplacement.

## Ligne de développement {#development-line}

- **2024-02-22 — Stability AI a annoncé Stable Diffusion 3.** Gamme annoncée de 0,8B à 8B, avec diffusion transformer et flow matching.

## Ce qui a changé {#what-changed}

2024-02-22 — Stability AI a ouvert une liste d'attente pour un aperçu anticipé de Stable Diffusion 3 : gamme annoncée de 0,8B à 8B, avec diffusion transformer et flow matching. 2024-06-03 — Le lien enregistré renvoie vers un lien court Reddit devenu inaccessible ; il est impossible de vérifier à partir de celui-ci une modification concrète du modèle. 2024-06-12 — Les poids ouverts de Stable Diffusion 3 Medium, modèle de 2B paramètres, ont été publiés. 2024-10-22 — Stable Diffusion 3.5 Large et 3.5 Large Turbo ont été publiés ; la société a explicitement indiqué que SD3 Medium de juin ne correspondait pas à ses attentes. 2024-10-29 — Stable Diffusion 3.5 Medium a rejoint la gamme.

## Mode d'emploi {#how-to-use-this}

À partir du 2024-02-22, les praticiens doivent considérer Stable Diffusion 3 comme un projet officiellement annoncé et suivre les actualités officielles et les pages du projet pour les mises à jour vérifiées.

1. Créez un compte Hugging Face, acceptez les conditions d'accès au dépôt restreint et téléchargez les poids de SD3 Medium ou une version Diffusers compatible.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
2. Pour une exécution locale dans ComfyUI, utilisez les workflows officiels fournis ; si les poids sont livrés séparément, placez les trois encodeurs de texte avec le modèle.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
3. Pour Python, mettez à jour Diffusers, chargez StableDiffusion3Pipeline depuis le dépôt stable-diffusion-3-medium-diffusers et déplacez le pipeline sur CUDA.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
4. Avant tout déploiement commercial, vérifiez le chiffre d'affaires de l'organisation : au-delà de 1 M$ par an d'usage commercial, une Enterprise License est requise.
  — <https://stability.ai/license>

## Bonnes pratiques {#best-practices}

- Pour des résultats reproductibles, transmettez un torch.Generator avec une seed fixe ; Diffusers l'utilise pour un échantillonnage déterministe des latents.
  — <https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3>
- Ne mélangez pas les paquets de poids : la variante sans T5XXL nécessite des encodeurs séparés, et la variante FP8 de T5XXL constitue un compromis entre qualité et consommation de ressources.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
- Pour un nouveau projet, comparez SD3 Medium avec SD 3.5 : SD 3.5 a été publiée après la reconnaissance des défauts de la première version ouverte de SD3.
  — <https://stability.ai/news-updates/introducing-stable-diffusion-3-5>

## Éléments rendus obsolètes {#superseded-by-this}

- 2024-10-22 : la recommandation de démarrer un nouveau projet avec SD3 Medium est devenue obsolète pour la plupart des cas d'usage ; Stability AI a présenté SD 3.5 après avoir reconnu que la version ouverte de juin ne correspondait pas aux attentes.
- 2024-06-12 : le statut de SD3 en tant que preview/liste d'attente est devenu obsolète après la publication ouverte des poids de SD3 Medium.

## Points inconnus {#still-unknown}

- Le lien court Reddit de l'événement du 2024-06-03 a renvoyé une Internal Error ; son message d'origine, son auteur et l'affirmation précise ne sont donc pas vérifiés.
- L'historique regroupe Stable Diffusion 3 et Stable Diffusion 3 Medium : il s'agit d'une seule ligne de produits, mais Medium est une version précise de 2B paramètres, et non l'ensemble complet des variantes annoncées en février 2024.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://stability.ai/news/stable-diffusion-3 | Stable Diffusion 3 — Stability AI | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/s/xBOocPBskt | Lien court Reddit pour l'événement du 2024-06-03 | 2026-09-05 |
| https://stability.ai/news-updates/stable-diffusion-3-medium | Announcing the Open Release of Stable Diffusion 3 Medium | 2026-09-05 |
| https://huggingface.co/stabilityai/stable-diffusion-3-medium | stabilityai/stable-diffusion-3-medium — Hugging Face | 2026-09-05 |
| https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3 | Stable Diffusion 3 pipeline — Diffusers documentation | 2026-09-05 |
| https://stability.ai/news-updates/introducing-stable-diffusion-3-5 | Introducing Stable Diffusion 3.5 — Stability AI | 2026-09-05 |
| https://stability.ai/license | Stability AI License | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:stable-diffusion-3`, fil `stable-diffusion-3`, 1 événement daté, du 2024-02-22 au 2024-02-22.
- **Note pratique :** À partir du 2024-02-22, les praticiens doivent considérer Stable Diffusion 3 comme un projet officiellement annoncé et suivre les actualités officielles et les pages du projet pour les mises à jour vérifiées.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.

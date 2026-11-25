---
title: "ideogram-4-GGUF — Ideogram 4"
category: projects
date: 2026-06-11
tags: [ideogram-4, ideogram-4-gguf, project]
aliases: ["ideogram-4-GGUF"]
level: 2
source_sha256: bb11827f1097ee02f691c05eedb135802aaf53f658c6da835d2ebc4a70ac44a7
translation: machine
translated_at: '2026-10-24'
---
# ideogram-4-GGUF — Ideogram 4 {#ideogram-4-gguf-ideogram-4}

**Ligne de développement :** `project:ideogram-4-gguf` · fil `ideogram-4`  
**Dernier événement :** 2026-06-11 · 1 événement daté depuis le 2026-06-11 · **Recherche :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

ideogram-4-GGUF est une paire de poids GGUF Q4_0 pour les composantes de diffusion principale et inconditionnelle d'Ideogram 4.0, conçue pour des exécutions locales plutôt que via l'API.

- Modèle de base : Ideogram 4.0, DiT de 9,3B.
- Runtime : stable-diffusion.cpp.
- Dépendances : Qwen3-VL-8B-Instruct au format GGUF et VAE Flux2 AE.

Le fichier principal Q4_0 occupe 5,64 Go. Il ne s'agit ni d'un checkpoint officiel d'Ideogram, ni d'une configuration ComfyUI prête à l'emploi.

Il convient à une expérimentation en CLI avec stable-diffusion.cpp. Pour une production reproductible, vérifiez les versions exactes des quatre composantes ainsi que la licence du modèle de base.

## Ligne de développement {#development-line}

- **2026-06-11 — Dépôt GGUF d'Ideogram 4 relié sur Hugging Face.** Conversions GGUF Q4_0 de deux composantes de diffusion d'Ideogram 4.0 pour stable-diffusion.cpp.

## Ce qui a changé {#what-changed}

2026-06-11 — Le lien atteste de la disponibilité de leejet/ideogram-4-GGUF : conversions GGUF Q4_0 de deux composantes de diffusion d'Ideogram 4.0 pour stable-diffusion.cpp.

## Mode d'emploi {#how-to-use-this}

Depuis le 2026-06-11, les praticiens peuvent utiliser le dépôt Hugging Face relié comme source candidate pour les artefacts GGUF d'Ideogram 4, tout en vérifiant indépendamment ses fichiers, sa licence, sa provenance et la compatibilité avec le runtime avant toute utilisation.

1. Téléchargez les deux fichiers Q4_0 liés : `ideogram4-Q4_0.gguf` (conditionnel) et `ideogram4_uncond-Q4_0.gguf` (inconditionnel).
  — <https://huggingface.co/leejet/ideogram-4-GGUF>
2. Compilez ou téléchargez un `sd-cli` compatible depuis stable-diffusion.cpp ; le projet affirme prendre en charge Ideogram4 et le format GGUF.
  — <https://github.com/leejet/stable-diffusion.cpp>
3. Transmettez les deux fichiers de diffusion, la version GGUF de Qwen3-VL-8B-Instruct et `flux2_ae.safetensors` à `sd-cli` ; le prompt doit être un JSON valide suivant l'exemple de la fiche du modèle.
  — <https://huggingface.co/leejet/ideogram-4-GGUF>

## Bonnes pratiques {#best-practices}

- Rédigez des prompts JSON structurés plutôt que des chaînes de texte simples, car le pipeline source a été entraîné sur ce schéma et le valide.
  — <https://ideogram.ai/blog/ideogram-4.0/>
- Épinglez les versions du runtime et de tous les poids dépendants, car stable-diffusion.cpp avertit explicitement que les options et API de la CLI changent souvent.
  — <https://github.com/leejet/stable-diffusion.cpp>
- Vérifiez la licence originale d'Ideogram 4.0 avant tout usage commercial, car la fiche GGUF l'hérite au lieu de définir la sienne.
  — <https://huggingface.co/leejet/ideogram-4-GGUF>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-03 — Aucune variante GGUF locale n'existait avant Ideogram 4.0 ; la version de base officielle fournissait des poids FP8 et NF4 ouverts, mais pas ce paquet GGUF tiers.
- 2026-06-04 — L'hypothèse selon laquelle Ideogram 4 ne peut pas fonctionner dans stable-diffusion.cpp est obsolète ; le runtime a annoncé la prise en charge d'Ideogram4.

## Toujours inconnu {#still-unknown}

- Aucune source primaire indépendante et datée ne confirme la date de publication de la conversion GGUF pour l'événement du 2026-06-11 : la fiche publique du modèle reflète l'état du dépôt, tandis que le profil Hugging Face indique une mise à jour le 2026-06-07.
- Les empreintes exactes, la compatibilité actuelle de stable-diffusion.cpp avec ces fichiers et la qualité de sortie par rapport aux poids FP8 et NF4 d'origine restent non vérifiées.
- La version officielle d'Ideogram 4.0 publiée le 2026-06-03 et le paquet GGUF tiers sont deux entités distinctes : la première a publié le modèle de base, le second l'a converti pour un runtime précis.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://huggingface.co/leejet/ideogram-4-GGUF | leejet/ideogram-4-GGUF | 2026-09-05 |
| https://github.com/leejet/stable-diffusion.cpp | leejet/stable-diffusion.cpp | 2026-09-05 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technical Details: Open model at the forefront of design | 2026-09-05 |
| https://ideogram.ai/news/ideogram-4.0/ | Ideogram releases 4.0, a frontier image model with open weights, and a new brand for the company | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ideogram-4-gguf`, fil `ideogram-4`, 1 événement daté 2026-06-11 → 2026-06-11.
- **Note pratique :** Depuis le 2026-06-11, les praticiens peuvent utiliser le dépôt Hugging Face relié comme source candidate pour les artefacts GGUF d'Ideogram 4, tout en vérifiant indépendamment ses fichiers, sa licence, sa provenance et la compatibilité avec le runtime avant toute utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

---
title: "Qwen3.8-27B-Cold-Fusion — Dérivés de Qwen"
category: projects
date: 2026-08-20
tags: [project, qwen-derivatives, qwen3-8-27b-cold-fusion]
aliases: ["Qwen3.8-27B-Cold-Fusion"]
level: 2
source_sha256: 9205c6a196f6959c1aa8855fb49203f6ad8e07c634e65e7bcf7fec48dcde127b
translation: machine
translated_at: '2026-10-24'
---
# Qwen3.8-27B-Cold-Fusion — Dérivés de Qwen {#qwen38-27b-cold-fusion-qwen-derivatives}

**Ligne de développement :** `project:qwen3-8-27b-cold-fusion` · fil `qwen-derivatives`  
**Dernier événement :** 2026-08-20 · 1 événement daté depuis le 2026-08-20 · **Recherche :** 2026-09-05 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

Qwen3.8-27B-Cold-Fusion-GAIN-V1.1 est un fine-tune tiers de Qwen3.8-27B, publié sous forme de quantifications GGUF pour l'inférence locale.

- Texte : génère du texte localement.
- Images : traite les images lorsque le mmproj est présent.
- Raisonnement : propose trois niveaux de raisonnement.
- Quantification : fournit des quants standard et MTP.

MTP nécessite de vérifier le taux d'acceptation des tokens sur votre matériel spécifique. Testez-le localement face au Qwen3.8-27B officiel, sur vos propres tâches, plutôt que de vous fier aux benchmarks publiés par l'auteur.

## Ligne de développement {#development-line}

- **2026-08-20 — Artefact GGUF de Qwen3.8-27B-Cold-Fusion référencé.** Publication GGUF sous Apache-2.0 avec quants standard et MTP, dont Q4_K_M.

## Ce qui a changé {#what-changed}

2026-08-20 — DavidAU/Qwen3.8-27B-Cold-Fusion-GAIN-V1.1-NM-DAU-NEO-MAX-MTP-GGUF publié : publication GGUF sous Apache-2.0 avec quants standard et MTP, dont Q4_K_M.

La fiche du modèle ajoute le nom complet, trois modes de raisonnement (xhigh, medium, low), un contexte de 256k et une exigence distincte de mmproj pour les images. La fiche accessible n'affiche aucune date de publication ; nous n'avançons donc pas de date source plus précise.

Nous n'avons trouvé aucune nouvelle étape datée liée au développement de ce modèle spécifique.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-20, évaluez l'artefact GGUF référencé comme un dérivé distinct de Qwen, en vérifiant sa provenance, sa configuration et ses capacités avant utilisation.

1. Installez llama.cpp et lancez le build Q4_K_M choisi avec `llama serve -hf …:Q4_K_M`, puis vérifiez les sorties sur votre tâche.
  — <https://huggingface.co/DavidAU/Qwen3.8-27B-Cold-Fusion-GAIN-V1.1-NM-DAU-NEO-MAX-MTP-GGUF>
2. Pour une exécution locale rapide, lancez `ollama run hf.co/…:Q4_K_M`.
  — <https://huggingface.co/DavidAU/Qwen3.8-27B-Cold-Fusion-GAIN-V1.1-NM-DAU-NEO-MAX-MTP-GGUF>
3. Pour traiter des images, téléchargez un fichier mmproj compatible et placez-le à côté du GGUF.
  — <https://huggingface.co/DavidAU/Qwen3.8-27B-Cold-Fusion-GAIN-V1.1-NM-DAU-NEO-MAX-MTP-GGUF>

## Bonnes pratiques {#best-practices}

- Comparez les builds standard et MTP sur votre matériel ; utilisez la quantification standard si le taux d'acceptation des tokens tombe sous 50 %.
  — <https://huggingface.co/DavidAU/Qwen3.8-27B-Cold-Fusion-GAIN-V1.1-NM-DAU-NEO-MAX-MTP-GGUF>
- Pour MTP, gardez une température non supérieure à 1 et une pénalité de répétition à 1 afin que la vitesse ne se dégrade pas.
  — <https://huggingface.co/DavidAU/Qwen3.8-27B-Cold-Fusion-GAIN-V1.1-NM-DAU-NEO-MAX-MTP-GGUF>
- Testez le modèle sur vos propres tâches avant déploiement, car le changement de raisonnement est important.
  — <https://huggingface.co/DavidAU/Qwen3.8-27B-Cold-Fusion-GAIN-V1.1-NM-DAU-NEO-MAX-MTP-GGUF>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- La fiche du modèle ne fournit ni date de création ni historique de commits ; nous ne pouvons donc pas dater la publication plus précisément que le 2026-08-20.
- Les affirmations de l'auteur sur la performance préservée, la baisse du nombre de tokens de réflexion et les gains de benchmark n'ont fait l'objet d'aucune vérification indépendante reproductible.
- Aucune révision ni aucun commit spécifique ne relie les poids Cold-Fusion au Qwen/Qwen3.8-27B officiel.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://huggingface.co/DavidAU/Qwen3.8-27B-Cold-Fusion-GAIN-V1.1-NM-DAU-NEO-MAX-MTP-GGUF | DavidAU/Qwen3.8-27B-Cold-Fusion-GAIN-V1.1-NM-DAU-NEO-MAX-MTP-GGUF — Hugging Face | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.8-27B | Qwen/Qwen3.8-27B — Hugging Face | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:qwen3-8-27b-cold-fusion`, fil `qwen-derivatives`, 1 événement daté du 2026-08-20 au 2026-08-20.
- **Note pratique :** Au 2026-08-20, évaluez l'artefact GGUF référencé comme un dérivé distinct de Qwen, en vérifiant sa provenance, sa configuration et ses capacités avant utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

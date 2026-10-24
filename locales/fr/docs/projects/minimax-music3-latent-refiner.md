---
title: "MiniMax Music 3 Latent Refiner"
category: projects
date: 2026-08-23
tags: [minimax-music3-latent-refiner, minimax_music3_latent_refiner, project]
aliases: ["MiniMax Music 3 Latent Refiner"]
level: 2
source_sha256: 7e0fffcab0d714c93acea460d94e85461852b654521842c624c7adcab8e3c4ba
translation: machine
translated_at: '2026-10-24'
---
# MiniMax Music 3 Latent Refiner {#minimax-music-3-latent-refiner}

**Ligne de développement :** `project:minimax-music3-latent-refiner` · fil `minimax-music3-latent-refiner`  
**Dernier événement :** 2026-08-23 · 1 événement daté depuis le 2026-08-23 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

MiniMax Music 3 Latent Refiner est un checkpoint communautaire destiné à restaurer des fichiers audio existants, et non un générateur de musique à partir de texte.

- Réparation audio : nettoie les pistes audio endommagées.
- Fidélité : préserve l'interprétation, le tempo, les voix et l'arrangement.
- Exécution : fonctionne via MiniMax Music 3 DAV.
- Interfaces : disponible via CLI, Python, l'intégration Diffusers et ComfyUI.

Testé uniquement sur CUDA en FP32 ; des dommages importants en dehors du pipeline d'entraînement détruisent des informations irrécupérables.

Utilisez-le comme étape de post-traitement pour l'audio de MiniMax Music 3, avec des contrôles d'écoute, et jamais comme remplacement des enregistrements originaux ou d'un pipeline de génération de musique à partir de texte.

## Ligne de développement {#development-line}

- **2026-08-23 — MiniMax Music 3 Latent Refiner v0.10 a été lié sur Hugging Face.** Le 2026-08-23, un lien Hugging Face vers BornSaint/minimax-music3-latent-refiner-v0.10 a été enregistré. Le lien vers l'artefact versionné indique une étape concrète, la v0.10, dans la ligne de développement de MiniMax Music 3 Latent Refiner, bien que ses capacités et ses modifications n'aient pas été établies à partir des éléments disponibles.

## Modifications {#what-changed}

- **2026-08-23** — La page `BornSaint/minimax-music3-latent-refiner-v0.10` est apparue, mais le lien enregistré ne confirme pas à lui seul une version fonctionnelle ni ses spécifications.
- **2026-09-01** — Publication de la v0.10 à l'adresse `terminusresearch/minimax-music3-latent-refiner-v0.10` : un checkpoint bridge-hybrid de 137 253 888 paramètres, à l'étape 1000, destiné à restaurer l'audio dans les latents DAV.

## Mode d'emploi {#how-to-use-this}

Au 2026-08-23, considérez l'artefact v0.10 lié comme une version candidate à inspecter et à évaluer, plutôt que de supposer qu'une version antérieure du latent refiner reste à jour.

1. Clonez le dépôt avec Git LFS, créez un environnement Python et installez le paquet en mode éditable.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
2. Exécutez `minimax-music3-refine input.wav refined.wav` pour un traitement de fichier de base.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
3. Pour Python, chargez `MiniMaxMusic3RefinerPipeline`, transmettez la forme d'onde et la fréquence d'échantillonnage, puis enregistrez le tenseur audio renvoyé.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
4. Pour ComfyUI, installez le nœud personnalisé, redémarrez ComfyUI et ouvrez le workflow inclus ; utilisez le chargeur du refiner, le chargeur de l'encodeur DAV et le nœud de raffinement latent.
  — <https://github.com/bghira/minimax-music3-latent-refiner>

## Bonnes pratiques {#best-practices}

- Utilisez des fenêtres de 30 secondes avec un recouvrement latent de deux secondes : le checkpoint a été entraîné sur des fenêtres de 30 secondes, qui constituent la référence de qualité indiquée.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
- Privilégiez CUDA et FP32 : c'est la précision de la version vérifiée. Ne considérez pas l'exemple en bfloat16 des instructions Hub générées automatiquement comme un mode confirmé pour ce pipeline audio.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
- Vérifiez le résultat à l'oreille, et ne vous attendez pas à récupérer des informations détruites par des dommages importants en dehors du pipeline d'entraînement.
  — <https://github.com/bghira/minimax-music3-latent-refiner>

## Remplacé par {#superseded-by-this}

- 2026-08-23 — Les instructions de la page `BornSaint/minimax-music3-latent-refiner-v0.10`, qui montrent un prompt d'image et `pipe(prompt).images[0]`, ne constituent pas une manière valide d'exécuter un refiner audio.
- 2026-09-01 — L'identifiant de version actif dans le code source et la fiche modèle est `terminusresearch/minimax-music3-latent-refiner-v0.10` ; ne le remplacez pas par la page BornSaint portant le même nom.

## Points inconnus {#still-unknown}

- `BornSaint/minimax-music3-latent-refiner-v0.10` affiche actuellement un extrait de génération d'image incohérent, alors qu'il renvoie vers `terminusresearch` dans la section ComfyUI. Sans instantané historique, nous ne pouvons pas vérifier ce qui y a été publié le 2026-08-23.
- La publication de la v0.10 est confirmée par un commit affiché quatre jours avant la vérification du 2026-09-05 ; la date du 2026-09-01 est déduite de cet horodatage relatif.
- Il n'existe ni évaluations indépendantes de la qualité, ni tests sur différents types de dommages, ni mesures de VRAM.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/BornSaint/minimax-music3-latent-refiner-v0.10 | BornSaint/minimax-music3-latent-refiner-v0.10 — Hugging Face | 2026-09-05 |
| https://github.com/bghira/minimax-music3-latent-refiner | bghira/minimax-music3-latent-refiner — GitHub | 2026-09-05 |
| https://huggingface.co/terminusresearch/minimax-music3-latent-refiner-v0.10/commit/8806b37005e090f1b3443759aa03563a5105d4d9 | Publication du latent refiner MiniMax Music 3 v0.10 — commit Hugging Face 8806b37 | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:minimax-music3-latent-refiner`, fil `minimax-music3-latent-refiner`, 1 événement daté du 2026-08-23 au 2026-08-23.
- **Note pratique :** Au 2026-08-23, les praticiens doivent considérer l'artefact v0.10 lié comme une version candidate à inspecter et à évaluer, plutôt que de supposer qu'une version antérieure du latent refiner reste à jour.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

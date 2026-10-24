---
title: "Zeta-Chroma"
category: projects
date: 2026-03-18
tags: [project, zeta-chroma, zeta-chroma-base-model]
aliases: ["Zeta-Chroma"]
level: 3
source_sha256: f9b1b4cc021096a768c39cdc94f4b65d40477ee0abb6ae5aa30982f77f4f5c84
translation: machine
translated_at: '2026-10-24'
---
# Zeta-Chroma {#zeta-chroma}

**Ligne de développement :** `project:zeta-chroma` · fil `zeta-chroma-base-model`  
**Dernier événement :** 2026-03-18 · 1 événement daté depuis le 2026-03-18 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Zeta-Chroma est un diffusion transformer pixel-space pour la génération text-to-image, dérivé de Tongyi-MAI/Z-Image.

- Il génère l'image directement en RGB et n'utilise pas de VAE.
- Il est distribué sous licence Apache-2.0.
- Il fonctionne dans ComfyUI ; SD.Next a ajouté la prise en charge le 28.04.2026.

Ordre de grandeur : le checkpoint BF16 publié pèse environ 13 GB.

Verdict : le modèle convient à la génération expérimentale, mais reste en WIP, avec des poids remplacés régulièrement et une qualité instable.

## Ligne de développement {#development-line}

- **2026-03-18 — Enregistrement de l'artefact de base Zeta-Chroma.** Le 2026-03-18, la ligne de développement Zeta-Chroma a enregistré un lien vers un artefact Safetensors dans le dépôt Hugging Face du projet. Les URL de réseaux sociaux et de discussions du dépôt associées rattachent cet élément à la même ligne de projet. Les liens fournis n'établissent ni les capacités, ni l'entraînement, ni la licence, ni les conditions de publication de l'artefact.

## Évolutions {#what-changed}

18.03.2026 — un checkpoint précoce, `zeta-chroma-base-x0-pixel-dino-distance.safetensors`, est devenu disponible ; une description ultérieure du dépôt précise que Zeta-Chroma est un modèle text-to-image WIP basé sur Tongyi-MAI/Z-Image.

01.03.2026 — le propriétaire du dépôt exigeait de convertir le checkpoint précoce au format Comfy avant de le charger dans ComfyUI.

23.04.2026 — cette exigence est devenue obsolète : un utilisateur de ComfyUI a indiqué que la version actuelle charge le modèle sans conversion séparée.

28.04.2026 — SD.Next a publié la prise en charge de Zeta-Chroma et a noté que le modèle nécessite un grand nombre d'étapes pour obtenir un résultat acceptable.

09–10.06.2026 — le dépôt a reçu des poids BF16 mis à jour, `full_1024_20M_dataset_run` ; un fichier a été renommé, passant de la variante `dino-distance-1024` à `no-dino-1024`.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-18, les praticiens qui évaluent Zeta-Chroma devraient suivre l'artefact Safetensors de base lié comme un candidat daté, et vérifier les métadonnées du dépôt ainsi que la discussion associée avant de s'y fier.

1. Téléchargez le checkpoint actuel depuis le dépôt Zeta-Chroma et placez-le dans le répertoire `diffusion_models` de votre installation.
  — <https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md>
2. Dans une version actuelle de ComfyUI, chargez le modèle directement ; pour les anciennes versions, vérifiez la compatibilité, car la première instruction exigeait une conversion des poids.
  — <https://huggingface.co/lodestones/Zeta-Chroma/discussions/9>
3. Commencez avec 1024 px de côté, Euler, un scheduler standard, un CFG de 4 à 7 et environ 20 étapes ; si le résultat est faible, augmentez le nombre d'étapes.
  — <https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md>

## Bonnes pratiques {#best-practices}

- Considérez le modèle comme expérimental : notez le hash du checkpoint et du workflow, car les poids du dépôt sont mis à jour pendant l'entraînement.
  — <https://huggingface.co/lodestones/Zeta-Chroma/tree/main>
- Ne branchez pas de VAE et ne reportez pas les LoRA de Z-Image : pour Zeta-Chroma, ce schéma est incompatible.
  — <https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md>
- Pour les poids actuels, privilégiez davantage d'étapes plutôt qu'une génération courte habituelle : un entraînement précoce peut donner des résultats faibles ou hallucinés.
  — <https://github.com/vladmandic/sdnext/discussions/4808>

## Éléments remplacés {#superseded-by-this}

- 01.03.2026 — la conversion séparée de `zeta-chroma-base-x0-pixel-dino-distance.safetensors` au format Comfy ne constitue plus une recommandation générale valable : le 23.04.2026, il a été signalé qu'un chargement direct fonctionne dans la version actuelle de ComfyUI.
- 09–10.06.2026 — le nom `zeta-chroma-base-x0-pixel-dino-distance-1024.safetensors` a été remplacé par `zeta-chroma-base-x0-pixel-no-dino-1024.safetensors` ; ne sélectionnez pas le fichier uniquement d'après son ancien nom.

## Points non vérifiés {#still-unknown}

- Le message du 18.03.2026 n'est pas accessible en lecture sur X ; sa formulation exacte n'est donc pas confirmée. La date est attestée par l'identifiant du message, et la description technique par d'autres sources.
- Le dépôt ne propose pas de version stable ni de tag de publication immuable ; la branche actuelle contient des mises à jour de poids en cours.
- Le signalement d'un chargement direct sans conversion est un témoignage d'utilisateur, et non une garantie documentée de ComfyUI pour toutes les versions.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/lodestones/Zeta-Chroma/blob/main/zeta-chroma-base-x0-pixel-dino-distance.safetensors | zeta-chroma-base-x0-pixel-dino-distance.safetensors — Zeta-Chroma | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/tree/main | Dépôt de modèle lodestones/Zeta-Chroma | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/raw/main/README.md | README de Zeta-Chroma | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/discussions/9 | Existe-t-il un workflow fonctionnel pour ce modèle ? | 2026-09-05 |
| https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md | SwarmUI obscure model support: Zeta Chroma | 2026-09-05 |
| https://github.com/vladmandic/sdnext/discussions/4808 | SD.Next Release 2026-04-28 | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/commit/53a5aa59f875b3b9ee31ef1a6afb9a480f9c62f1 | full_1024_20M_dataset_run (bf16) | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/commit/eb27e547dcf324b4ecf219ea3fdd9e913422d5cb | Rename zeta-chroma-base-x0-pixel-dino-distance-1024.safetensors to zeta-chroma-base-x0-pixel-no-dino-1024.safetensors | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:zeta-chroma`, fil `zeta-chroma-base-model`, 1 événement daté, du 2026-03-18 au 2026-03-18.
- **Note pratique :** Au 2026-03-18, les praticiens qui évaluent Zeta-Chroma devraient suivre l'artefact Safetensors de base lié comme un candidat daté, et vérifier les métadonnées du dépôt ainsi que la discussion associée avant de s'y fier.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

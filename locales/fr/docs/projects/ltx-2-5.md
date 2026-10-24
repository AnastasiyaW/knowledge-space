---
title: "LTX-2.5 — LTX Video"
category: projects
date: 2026-08-11
tags: [ltx-2-5, ltx-video, project]
aliases: ["LTX-2.5"]
level: 3
source_sha256: 0e46f32e9ae83c764df19afae2ec9ac426d0902ae6ab15ea4dbc81415edba868
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.5 — LTX Video {#ltx-25-ltx-video}

**Ligne de développement :** `project:ltx-2-5` · fil `ltx-video`  
**Dernier événement :** 2026-08-11 · 1 événement daté depuis le 2026-08-11 · **Recherche effectuée le :** 2026-09-07 · confiance : moyenne

## Présentation {#what-it-is}

LTX-2.5 est une famille de modèles audio-vidéo de 22B développée par Lightricks, destinée aux configurations locales avec ComfyUI et Python, ou à la génération hébergée.

- Génération vidéo et audio synchronisée à partir d'un conditionnement par texte, image, vidéo et audio.
- Outillage local pour la vidéo-vers-vidéo, LoRA/IC-LoRA, HDR et les chemins de fine-tuning.
- Accès à l'API hébergée via `ltx-2-5-fast` et `ltx-2-5-pro`, sans retake, extend ni reframe.

Le guide technique local exige un GPU NVIDIA avec 32 Go+ de VRAM, 32 Go de RAM, 100 Go d'espace libre, CUDA 12.7+ et Python 3.12+. La page produit indique séparément un minimum de 16 Go. Utilisez LTX-2.5 lorsque le son synchronisé, l'auto-hébergement ou l'adaptation locale sont importants. Conservez LTX-2.3 pour un workflow hébergé nécessitant retake, extend ou reframe.

## Ligne de développement {#development-line}

- **2026-08-11 — Les liens officiels vers le modèle et l'application LTX-2.5 ont été partagés.** Le 2026-08-11, un élément daté du fil LTX Video renvoyait vers la page officielle du modèle LTX-2.5 et vers l'application LTX. Cela marque un modèle LTX-2.5 précis et son chemin d'accès officiel. Les éléments disponibles ne permettent pas de déterminer s'il s'agissait d'un lancement, d'une mise à jour ou d'un changement de disponibilité.

## Changements {#what-changed}

- 2026-08-10 — `ltx-2-5-fast` a obtenu une durée automatique pour le text-to-video et l'image-to-video, avant la version nommée.
- 2026-08-11 — LTX a introduit les variantes hébergées Fast et Pro pour le text-to-video, l'image-to-video et l'audio-to-video ; LTX-2 v1.2.0 a ajouté le runtime local 2.5 et la prise en charge de l'entraînement.
- 2026-08-12 — ComfyUI a ajouté, dès le premier jour, des modèles LTX-2.5 et deux routes : poids locaux et Partner Nodes hébergés.
- 2026-08-16 — Les anciens identifiants d'API `ltx-2-fast` et `ltx-2-pro` ont été supprimés, rendant la migration vers 2.3 ou 2.5 obligatoire.
- 2026-08-18 — L'audio-to-video a obtenu les paliers de résolution Fast 4K et Pro 1080p.
- 2026-08-19 — L'audio-to-video a obtenu des contrôles de fréquence d'images, de dernière image et de mouvement de caméra.
- 2026-08-25 — LTX-2 v1.3.0 a modifié le DFR local avec le 4K en tuiles, l'exécution multi-GPU, le décodage tenant compte des keyframes et de nouveaux drapeaux DFR.
- 2026-09-02 — `ltx-2-5-pro` a été étendu au 1440p/4K et au 48 fps pour le text-to-video, l'image-to-video et l'audio-to-video.

## Mode d'emploi {#how-to-use-this}

1. Choisissez d'abord la surface d'utilisation. Utilisez `ltx-2-5-fast` pour la rapidité et un coût réduit, ou `ltx-2-5-pro` pour une fidélité supérieure sur les routes hébergées text-to-video, image-to-video ou audio-to-video. Utilisez un chemin local si vous avez besoin d'auto-hébergement ou d'adaptation.
  — <https://docs.ltx.io/models/ltx-2-5>
2. Pour une requête image-to-video hébergée, transmettez `duration: null` uniquement lorsque la dernière image n'est pas fixée. La durée automatique ne peut pas être combinée avec `last_frame_uri`.
  — <https://docs.ltx.io/models/ltx-2-5>
3. Pour le chemin local visuel, installez `ComfyUI-LTXVideo`, sélectionnez un modèle LTX-2.5, téléchargez les fichiers correspondants listés, ajoutez un prompt ou des références, puis lancez la tâche.
  — <https://docs.ltx.io/open-source-model/getting-started/quick-start>
4. Pour du code ou de l'automatisation, clonez LTX-2, exécutez `uv sync`, obtenez l'accès au dépôt du modèle, téléchargez les composants séparés et indiquez le chemin de chaque composant à `ltx-pipelines`.
  — <https://docs.ltx.io/open-source-model/integration-tools/pytorch-api>
5. Pour la génération locale, gardez la largeur et la hauteur divisibles par 32. Utilisez un nombre d'images de la forme `8n + 1`, ou omettez ce nombre pour laisser la tête de durée de LTX-2.5 le choisir.
  — <https://docs.ltx.io/open-source-model/integration-tools/pytorch-api>

## Bonnes pratiques {#best-practices}

- Gardez les composants du checkpoint cohérents, en particulier l'encodeur de texte Gemma 4 affiné spécifiquement pour LTX. Ne remplacez pas par le Gemma 4 standard de Google.
  — <https://github.com/Lightricks/LTX-2/blob/main/packages/ltx-trainer/docs/configuration-reference.md>
- Démarrez le modèle ComfyUI text-to-video à 768x512, 97 images et 24 fps. N'augmentez la durée ou la résolution qu'une fois que le matériel gère la base, et fixez le seed lorsque vous avez besoin de reproduire un résultat.
  — <https://docs.ltx.io/open-source-model/usage-guides/text-to-video>
- Rédigez les prompts sous forme de scène chronologique. Nommez le plan, la scène, l'action, le personnage, le mouvement de caméra et l'audio. Réécrivez les prompts issus d'autres modèles vidéo plutôt que de copier leurs balises ou leur syntaxe de découpage.
  — <https://docs.ltx.io/open-source-model/usage-guides/prompting-guide>
- Pour un travail multi-plans natif, utilisez un paragraphe chronologique. Nommez explicitement chaque coupe, rappelez les identifiants récurrents et la continuité audio, et privilégiez deux à quatre plans par génération.
  — <https://docs.ltx.io/open-source-model/usage-guides/prompting-guide>
- Utilisez le pipeline natif en deux étapes pour la production locale. Utilisez le pipeline distillé pour la vitesse ou les traitements par lots.
  — <https://docs.ltx.io/open-source-model/integration-tools/pytorch-api>
- Dimensionnez le travail local selon la base technique : 32 Go+ de VRAM NVIDIA, 32 Go de RAM, 100 Go de stockage, CUDA 12.7+ et Python 3.12+. Validez le workflow réel sur le matériel cible.
  — <https://docs.ltx.io/open-source-model/getting-started/system-requirements>

## Remplacé par {#superseded-by-this}

- 2026-08-16 — Les identifiants de modèles d'API `ltx-2-fast` et `ltx-2-pro` restent valides. Source : https://docs.ltx.io/api-changelog/2026/8/16
- 2026-08-18 — L'audio-to-video sur `ltx-2-5-fast` est limité au 1080p. Source : https://docs.ltx.io/api-changelog/2026/8/18
- 2026-08-19 — L'audio-to-video ne permet pas de définir la fréquence d'images, le mouvement de caméra ou une dernière image. Source : https://docs.ltx.io/api-changelog/2026/8/19
- 2026-09-02 — LTX-2.5 Pro est limité au 720p/1080p. Source : https://docs.ltx.io/api-changelog/2026/9/2
- 2026-08-25 — Le DFR utilise `--checkpoint-path`, `--distilled-lora` et `--temporal-upsample-rounds`. Source : https://github.com/Lightricks/LTX-2/blob/main/CHANGELOG.md

## Points encore inconnus {#still-unknown}

- Une deuxième entrée LTX-2.5 non résolue, datée du 2026-08-12, utilise la clé provisoire `ltx_2_5` et des URL Hugging Face différentes. Elle pourrait couvrir un artefact en aval plutôt que cette version de base. Ne fusionnez pas son historique sans une identité exacte vérifiée.
- Les noms d'API hébergée `fast`/`pro` et les noms de checkpoints locaux `dev`/`distilled` sont des surfaces documentées distinctes. Aucune source de première main trouvée ici ne déclare de correspondance un-à-un entre eux.
- Les sources de première main divergent sur la VRAM locale : la page produit indique 16 Go minimum, tandis que la page technique des exigences système indique 32 Go+. Aucune réconciliation n'a été trouvée ; cette dernière valeur est retenue comme base pratique.
- L'URL fournie de l'application hébergée n'a pas donné de documentation lisible lors de cette recherche. Les contrôles actuels de l'interface, le parcours de compte et la tarification n'ont pas été vérifiés de manière indépendante.
- La piste de recherche en chinois simplifié a produit des pages communautaires, mais aucune source de pratique LTX-2.5 vérifiée, datée et reproductible. Aucune affirmation de paramètre en chinois n'est incluse.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ltx.io/model/ltx-2-5 | LTX-2.5: LTX's Latest AI Open-Source Foundation Model | LTX | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/10 | August 10, 2026 | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/11 | August 11, 2026 | LTX Documentation | 2026-09-07 |
| https://github.com/Lightricks/LTX-2/releases/tag/v1.2.0 | Release v1.2.0 · Lightricks/LTX-2 · GitHub | 2026-09-07 |
| https://blog.comfy.org/p/ltx-25-day-0-support-in-comfyui | LTX-2.5 Day-0 Support in ComfyUI | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/16 | August 16, 2026 | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/18 | August 18, 2026 | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/19 | August 19, 2026 | LTX Documentation | 2026-09-07 |
| https://github.com/Lightricks/LTX-2/blob/main/CHANGELOG.md | LTX-2/CHANGELOG.md at main · Lightricks/LTX-2 · GitHub | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/9/2 | September 2, 2026 | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/models/ltx-2-5 | LTX-2.5 | LTX Documentation | 2026-09-07 |
| https://huggingface.co/Lightricks/LTX-2.5 | Lightricks/LTX-2.5 · Hugging Face | 2026-09-07 |
| https://docs.ltx.io/open-source-model/getting-started/quick-start | Quick Start | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/usage-guides/text-to-video | Text-to-Video Workflow for Beginners | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/integration-tools/pytorch-api | PyTorch API | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/getting-started/system-requirements | System Requirements | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/usage-guides/prompting-guide | Prompting Guide | LTX Documentation | 2026-09-07 |
| https://github.com/Lightricks/LTX-2/blob/main/packages/ltx-trainer/docs/configuration-reference.md | LTX-2 trainer configuration reference · Lightricks/LTX-2 · GitHub | 2026-09-07 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ltx-2-5`, fil `ltx-video`, 1 événement daté du 2026-08-11 au 2026-08-11.
- **Note pratique :** Voir les sections d'usage et de pratique sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les mentions « remplacé par » datées font autorité pour ce qui est obsolète.

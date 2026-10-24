---
title: "HunyuanVideo-I2V — Disponibilité publique du projet"
category: projects
date: 2025-03-06
tags: [hunyuanvideo, hunyuanvideo-i2v, project, public-project-availability]
aliases: ["HunyuanVideo-I2V"]
level: 3
source_sha256: c42bc1ab2ea59f8357ef40f9d5875b4cc0f50918a2d75e02a86dd7aa3ab79e29
translation: machine
translated_at: '2026-10-24'
---
# HunyuanVideo-I2V — Disponibilité publique du projet {#hunyuanvideo-i2v-public-project-availability}

**Ligne de développement :** `project:hunyuanvideo-i2v` · fil `public-project-availability`  
**Dernier événement :** 2025-03-06 · 1 événement daté depuis le 2025-03-06 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

HunyuanVideo-I2V est la pile locale de génération d'image vers vidéo de Tencent, publiée en 2025, destinée aux équipes qui ont besoin d'une génération guidée par la première image plutôt que d'une API hébergée.

- Entrées : image de référence et conditionnement par prompt textuel.
- Composants : code PyTorch officiel, poids pré-entraînés, échantillonnage, entraînement LoRA et inférence multi-GPU xDiT.
- Sortie : génération vidéo jusqu'à 720p et 129 images (environ cinq secondes).

Le guide officiel pour un seul GPU indique une consommation de pointe de 60 Go de VRAM, et les tests ont été réalisés sur 80 Go.

La pile d'origine reste exécutable, mais les nouveaux déploiements devraient comparer la ligne I2V plus récente HunyuanVideo-1.5 avant de s'engager sur le matériel et le travail d'intégration.

## Ligne de développement {#development-line}

- **2025-03-06 — Publication publique du projet HunyuanVideo-I2V.** Tencent a publié le code d'inférence et les poids du modèle.

## Modifications {#what-changed}

HunyuanVideo-I2V débute par une version locale en 720p, corrige ses poids initiaux et ajoute l'inférence multi-GPU.

- 2025-03-06 : Tencent a publié le code d'inférence et les poids du modèle.
- 2025-03-07 : Tencent a remplacé l'état de la publication après la correction d'un bogue de changement d'identifiant ; les poids corrigés font référence pour la cohérence de la première image.
- 2025-03-09 : Tencent n'a publié aucun code, poids ou changement de version officiel distinct daté de ce jour ; aucune modification d'implémentation ne peut être vérifiée.
- 2025-03-11 : Tencent a mis à jour le code d'entraînement et d'inférence LoRA après la correction du bogue.
- 2025-03-13 : Tencent a publié l'inférence parallèle xDiT.
- 2025-11-21 : Tencent a publié la ligne séparée HunyuanVideo-1.5 T2V/I2V, avec des points de contrôle I2V en 480p et 720p ; elle n'est pas documentée comme une continuation directe de ce dépôt.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-03-06, les praticiens devraient utiliser comme points de départ de référence pour HunyuanVideo-I2V la page officielle Hugging Face et le dépôt GitHub de Tencent indiqués ci-dessous, et attendre le contenu archivé des mises à jour avant d'agir sur les annonces ultérieures.

1. Vérifiez que la pile d'origine convient à la machine : Linux et un GPU NVIDIA compatible CUDA sont requis ; prévoyez 60 Go de VRAM en pointe pour le 720p, la configuration testée étant de 80 Go.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
2. Clonez le dépôt officiel, créez son environnement Python 3.11.9 et installez les dépendances PyTorch/CUDA et les requirements documentés ; utilisez le conteneur CUDA 12 publié si cela correspond au déploiement.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
3. Téléchargez les poids officiels actuels de HunyuanVideo-I2V depuis la fiche modèle de Tencent et examinez la Tencent Hunyuan Community License avant utilisation.
  — <https://huggingface.co/tencent/HunyuanVideo-I2V>
4. Exécutez sample_image2video.py avec HYVideo-T/2, --i2v-mode, le chemin de l'image de référence, un prompt concis, la résolution 720p, le nombre d'étapes d'échantillonnage, la durée de la vidéo et un chemin de sortie ; activez le déchargement CPU si nécessaire pour une génération haute résolution.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
5. Choisissez délibérément un mouvement stable ou dynamique : le mode stable utilise --i2v-stability avec --flow-shift 7.0 ; une sortie dynamique utilise stability désactivé avec --flow-shift 17.0. Définissez une graine lorsque le résultat doit être reproductible.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
6. Pour un effet personnalisé, préparez des données d'entraînement vidéo-légende, exécutez le script d'entraînement LoRA fourni, puis chargez le fichier safetensors produit via --use-lora et --lora-path pendant l'inférence.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>

## Bonnes pratiques {#best-practices}

- Ne conservez pas les poids de lancement du 6 mars : utilisez les poids corrigés annoncés après la correction du changement d'identité.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Gardez le prompt court et concret : précisez le sujet et l'action, puis ajoutez l'arrière-plan ou la caméra seulement si nécessaire ; des prompts trop détaillés peuvent introduire des transitions indésirables.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Utilisez un flow shift de 7 avec le mode stable pour un mouvement plus régulier, et un flow shift de 17 avec le mode stable désactivé lorsque le mouvement compte davantage que la stabilité.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Dimensionnez le matériel à partir du minimum documenté de 60 Go plutôt que de supposer que le déchargement CPU rend le flux 720p économe en VRAM ; la configuration officielle testée est de 80 Go.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Pour les effets LoRA, placez un déclencheur sous forme de syntagme ou de courte phrase directement dans chaque légende vidéo ; entraînez en 360p, puis utilisez le LoRA obtenu pour l'inférence en 720p.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>

## Remplacé par {#superseded-by-this}

- Les poids initiaux de HunyuanVideo-I2V du 2025-03-06 sont remplacés par les poids corrigés du 2025-03-07, car la version open source initiale pouvait modifier l'identité.
- Le choix de déploiement du 2025-03-06 est daté, sans être formellement déprécié : HunyuanVideo-1.5 a été publié le 2025-11-21 comme ligne T2V/I2V distincte et plus récente de Tencent, avec des points de contrôle I2V en 480p et 720p. Évaluez-la pour les nouveaux déploiements, mais ne supposez pas la compatibilité des points de contrôle ou des flux de travail.

## Points encore inconnus {#still-unknown}

- L'événement du 9 mars ne peut pas être rattaché à une version amont distincte à partir des sources primaires ; la page source indiquée n'était pas accessible.
- Tencent ne documente pas HunyuanVideo-1.5 comme une mise à niveau directe ou un remplacement formel de HunyuanVideo-I2V.
- Les sources n'indiquent aucun engagement de maintenance actuel, aucune période de support ni aucune disponibilité d'API hébergée pour la pile HunyuanVideo-I2V d'origine.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news | README et actualités de HunyuanVideo-I2V — Tencent-Hunyuan sur GitHub | 2026-09-04 |
| https://huggingface.co/tencent/HunyuanVideo-I2V | Fiche modèle tencent/HunyuanVideo-I2V — Hugging Face | 2026-09-04 |
| https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5 | README de HunyuanVideo-1.5 — Tencent-Hunyuan sur GitHub | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:hunyuanvideo-i2v`, fil `public-project-availability`, 1 événement daté du 2025-03-06 au 2025-03-06.
- **Note pratique :** À partir du 2025-03-06, les praticiens devraient utiliser comme points de départ de référence pour HunyuanVideo-I2V la page officielle Hugging Face et le dépôt GitHub de Tencent indiqués, et attendre le contenu archivé des mises à jour avant d'agir sur les annonces ultérieures.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour déterminer ce qui est obsolète.

---
title: "Tencent"
category: organizations
date: 2025-12-29
tags: [ai-research-releases, organization, tencent, tencent_arc]
aliases: ["Tencent"]
level: 2
source_sha256: 2d1f4ec67910e8a5fc3c0dd39de9b3edbf38ae43ce8db575d1d6f702289935e8
translation: machine
translated_at: '2026-10-24'
---
# Tencent {#tencent}

**Ligne de développement :** `organization:tencent` · fil `ai-research-releases`  
**Dernier événement :** 2025-12-29 · 1 événement daté depuis 2025-12-29 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Tencent commercialise des plateformes grand public, du cloud, du marketing, des paiements et des services numériques auprès des consommateurs et des entreprises.

- Les gammes de produits destinées aux consommateurs et aux entreprises sont distinctes.
- DSR Suite de TencentARC est un paquet VLM sous licence Apache-2.0, dérivé de Qwen2.5-VL-7B, destiné au raisonnement sur la géométrie des objets et leurs relations dans le temps, dans des vidéos.
- Il comprend un jeu d'entraînement de 50K questions-réponses, un benchmark de 1 484 questions-réponses, un modèle BF16 de 9B et un Geometry Selection Module.

## Ligne de développement {#development-line}

- **2025-12-29 — Tencent ARC a publié les dépôts de code et de modèle de DSR Suite.** Nous disposons du code et des poids pour le raisonnement spatial dynamique dans les vidéos, avec DSR-Train, DSR-Bench et GSM sur une base Qwen2.5-VL-7B.

## Évolutions {#what-changed}

Ligne de développement de Tencent :

- 2023-05-02 — Tencent Cloud a présenté une plateforme de production de humains numériques à faible volume d'échantillons, sous forme de flux de travail d'avatar en libre-service. Selon ce communiqué, elle pouvait utiliser une vidéo de parole de trois minutes et 100 phrases vocales. Cela concerne un produit de Tencent Cloud, et non DSR Suite.
- 2025-12-29 — TencentARC a publié DSR Suite en tant que recherche ouverte. Il fournit le code et les poids pour le raisonnement spatial dynamique dans les vidéos, à l'aide de DSR-Train, DSR-Bench et GSM sur une base Qwen2.5-VL-7B.
- 2025-12-25 au 2026-02-21 — Le dépôt date l'article et le code du 2025-12-25 et indique l'acceptation à CVPR 2026 le 2026-02-21. Cela modifie la reconnaissance académique, et non la disponibilité en tant que produit Tencent géré.

## Mode d'emploi {#how-to-use-this}

Au 2025-12-29, commencez par le modèle DSR Suite publié et les dépôts sources, puis vérifiez les capacités et les conditions de licence avant toute adoption.

1. Choisissez d'abord la gamme de produits Tencent concernée : Tencent n'est pas un point d'accès développeur unique, et son catalogue public distingue les services grand public, Tencent Cloud et les produits marketing.
  — <https://www.tencent.com/what-we-create/>
2. Pour une inférence locale de DSR Suite, suivez le chargeur Transformers de la fiche du modèle pour AutoProcessor et Qwen2_5_VLForConditionalGeneration_Spatial, en chargeant TencentARC/DSR_Suite-Model avec device_map="auto".
  — <https://huggingface.co/TencentARC/DSR_Suite-Model>
3. Pour une vérification reproductible, téléchargez DSR-Bench sous la forme benchmark.parquet, indiquez les chemins locaux des vidéos et du fichier parquet dans VLMEvalKit, puis exécutez sa tâche Spatial-Reasoning.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md>
4. Pour le fine-tuning, créez l'environnement Python 3.11 dédié au modèle, installez les dépendances du modèle, obtenez les données vidéo/légendes et, optionnellement, DSR-Train, convertissez les paires questions-réponses, définissez les chemins des questions-réponses, des vidéos et du checkpoint Pi3, puis exécutez train.sh.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/model/README.md>

## Bonnes pratiques {#best-practices}

- Exécutez la génération de données et l'entraînement du modèle dans des environnements séparés, car les dépendances diffèrent.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md>
- Prévoyez un hébergement local des poids BF16 de 9B plutôt que de supposer un point d'accès hébergé ; la fiche du modèle consultée ne mentionne aucun fournisseur d'inférence.
  — <https://huggingface.co/TencentARC/DSR_Suite-Model>
- N'évaluez avec DSR-Bench qu'après avoir obtenu les vidéos référencées et défini les deux chemins locaux ; le fichier parquet du benchmark ne fournit pas directement les fichiers vidéo.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md>
- Pour une génération personnalisée de questions-réponses, supprimez les scènes statiques avant la génération et configurez l'accès à l'API : les scripts de curation nécessitent votre propre point d'accès et votre propre jeton.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/data/README.md>

## Remplacé par ceci {#superseded-by-this}

- Aucun remplacement de produit vérifié : la publication DSR Suite du 2025-12-29 n'est pas documentée comme successeur de la plateforme de humains numériques à faible volume d'échantillons de Tencent Cloud du 2023-05-02.
- 2026-02-21 : l'acceptation à CVPR 2026 remplace la description de l'article de 2025 comme simple publication antérieure à l'acceptation ; elle n'établit pas l'existence d'un nouveau service géré.

## Inconnues {#still-unknown}

- Le communiqué 2023 de Tencent Cloud sur les humains numériques et la publication 2025 DSR Suite de TencentARC concernent des produits et des équipes différents ; aucune source consultée n'établit de API commune, de filiation de produit ou de relation de remplacement.
- Aucune page publique officielle actuelle n'a été vérifiée concernant l'accès, le prix, la disponibilité régionale ou le statut de support de la plateforme de humains numériques de 2023.
- Les sources consultées de DSR Suite n'indiquent ni une version de Transformers testée, ni une exigence en mémoire GPU, ni un chemin de déploiement sur Tencent Cloud.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.tencent.com/who-we-are/ | Who we are - Tencent | 2026-09-04 |
| https://www.tencent.com/what-we-create/ | What we create - Tencent | 2026-09-04 |
| https://m.jiemian.com/article/9312569.html | 腾讯云公布小样本数智人生产平台，花费千元即可自行制作数字人 | 2026-09-04 |
| https://huggingface.co/TencentARC/DSR_Suite-Model | TencentARC/DSR_Suite-Model | 2026-09-04 |
| https://github.com/TencentARC/DSR_Suite | TencentARC/DSR_Suite | 2026-09-04 |
| https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md | DSR_Suite README | 2026-09-04 |
| https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/model/README.md | DSR_Suite model training README | 2026-09-04 |
| https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/data/README.md | DSR_Suite data generation README | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `organization:tencent`, fil `ai-research-releases`, 1 événement daté du 2025-12-29 au 2025-12-29.
- **Note pratique :** Au 2025-12-29, les praticiens qui évaluent les travaux de Tencent ARC devraient commencer par le modèle DSR Suite publié et les dépôts sources, puis vérifier indépendamment ses capacités et ses conditions de licence avant toute adoption.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

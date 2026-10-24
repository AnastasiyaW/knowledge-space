---
title: "SeedVR2"
category: projects
date: 2026-07-30
tags: [project, seedvr, seedvr2, seedvr2-development-and-distribution]
aliases: ["SeedVR2"]
level: 3
source_sha256: 3da1feb253c4ca8b1a33799ddf3b980865c7f2a141e899527e2c4644b3b5d443
translation: machine
translated_at: '2026-10-24'
---
# SeedVR2 {#seedvr2}

**Ligne de développement :** `project:seedvr2` · fil `seedvr2-development-and-distribution`  
**Dernier événement :** 2026-07-30 · 3 événements datés depuis le 2025-06-09 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

SeedVR2 est le successeur de SeedVR pour la restauration de vidéos et d'images sans prompt : upscaling en une seule étape, fenêtrage d'attention adaptatif, modèles 3B et 7B, ainsi qu'une distillation 1.44B tierce destinée aux équipements moins puissants. Limite : l'exécution officielle est conçue pour une inférence GPU multi-processus ; la variante 1.4B ne prend en charge que les images et nécessite un support de chargeur ComfyUI distinct. Verdict : pour une fidélité maximale, privilégiez les versions officielles 3B/7B ; la 1.4B est un compromis délibéré entre vitesse et niveau de détail.

## Ligne de développement {#development-line}

- **2025-06-09 — Lien vers la page projet de SeedVR2.** Le 2025-06-09, un lien vers la page projet de SeedVR2 a été enregistré. Ce lien datant établit un point de référence public pour le projet, mais n'établit pas à lui seul une publication, une disponibilité des modèles ou des détails d'implémentation.
- **2025-06-11 — Liens vers les dépôts de code et de modèles SeedVR.** Le 2025-06-11, des liens vers le dépôt source ByteDance-Seed/SeedVR et vers le dépôt de modèles SeedVR sur Hugging Face ont été enregistrés. Il s'agit d'un événement de distribution et de référence amont pour la ligne SeedVR2, bien que les liens fournis ne prouvent pas à eux seuls la relation exacte entre SeedVR et SeedVR2, ni l'état de publication à cette date.
- **2026-07-30 — Lien vers le paquet ComfyUI de SeedVR2-1.4B.** Le 2026-07-30, un dépôt Hugging Face nommé SeedVR2-1.4B et son répertoire ComfyUI ont été liés. Cela enregistre une voie de distribution pratique orientée ComfyUI pour ce modèle, bien que les liens datés ne permettent pas de vérifier son origine, son exhaustivité ni sa compatibilité.

## Évolutions {#what-changed}

2025-06-09 — SeedVR2 est présenté comme une restauration vidéo par diffusion adversariale en une seule étape ; les dimensions d'entrée doivent être multiples de 32. 2025-06-11 — création du dépôt officiel contenant le code d'exécution et les modèles checkpoints SeedVR2-3B/7B. 2026-07-30 — publication d'une distillation tierce à 6 couches, 1.44B, de SeedVR2-7B, avec intégration prête à l'emploi dans ComfyUI pour l'upscaling d'images fixes.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-30, il convient de considérer SeedVR2 comme une voie de déploiement versionnée : consultez d'abord les références officielles du projet et du dépôt, puis évaluez de manière indépendante le paquet ComfyUI 1.4B lié avant de l'utiliser dans un workflow.

1. Pour une exécution officielle, clonez le dépôt, créez un environnement Python 3.10, puis installez les requirements, FlashAttention et un Apex compatible.
  — <https://github.com/ByteDance-Seed/SeedVR>
2. Téléchargez le checkpoint officiel, par exemple ByteDance-Seed/SeedVR2-3B, dans le dossier local ckpts/ via snapshot_download.
  — <https://github.com/ByteDance-Seed/SeedVR>
3. Lancez projects/inference_seedvr2_3b.py avec torchrun en spécifiant le dossier d'entrée, la résolution de sortie, la seed et le degré de sequence-parallel ; les dimensions d'entrée doivent être multiples de 32.
  — <https://github.com/ByteDance-Seed/SeedVR>
4. Pour la variante 1.4B dans ComfyUI, placez le checkpoint ComfyUI dans models/diffusion_models, le VAE dans models/vae, copiez le dossier support dans custom_nodes, puis redémarrez ComfyUI.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B>
5. Chargez le workflow prêt à l'emploi, commencez à 4× ; utilisez un seul pas, CFG 1, Euler/simple et denoise 1.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B/blob/main/comfyui/seedvr2_1.4b_upscale_image.json>

## Bonnes pratiques {#best-practices}

- N'utilisez pas le checkpoint 1.4B avec le chargeur SeedVR2 standard : ses six blocs nécessitent une branche de détection d'architecture ajoutée.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B>
- Pour ComfyUI, prenez le checkpoint du sous-répertoire comfyui/ et non celui de la racine : il contient les tenseurs de conditionnement exigés par le chargeur.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B>
- Commencez à 4× ; 8× dégrade la qualité. Ne dépassez pas 512 pour le VAE tile_size ; en cas de manque de mémoire, réduisez-le à 256.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B/blob/main/comfyui/seedvr2_1.4b_upscale_image.json>
- Vérifiez le résultat sur des dégradations légères et de petites résolutions : le projet officiel met en garde contre la sur-accentuation des détails, ainsi que contre une faible robustesse face aux dégradations sévères et aux grands mouvements.
  — <https://github.com/ByteDance-Seed/SeedVR>

## Remplacé par {#superseded-by-this}

- Non confirmé : SeedVR (CVPR 2025) n'a pas été déclaré obsolète ; le dépôt officiel continue de conserver SeedVR et SeedVR2 comme modèles distincts.
- 2026-07-30 : la distillation 1.4B ne remplace pas les versions officielles 3B/7B en matière de fidélité ; elle est destinée aux contraintes de mémoire et de latence.

## Toujours inconnu {#still-unknown}

- SeedVR2-1.4B est une distillation tierce de lvladikov, et non un checkpoint officiel de ByteDance Seed ; ses mesures chiffrées et ses comparaisons ne constituent pas une validation indépendante.
- Dans la référence historique à ByteDance-Seed/SeedVR-Models, l'URL actuelle redirige vers SeedVR2-3B ; l'état exact de l'arborescence initiale du modèle au 2025-06-11 n'a donc pas pu être reconstitué à partir de cette page.
- La documentation officielle décrit une exécution multi-GPU ; la prise en charge pratique du single-GPU, de l'offload et de ComfyUI relève d'implémentations communautaires distinctes et n'est pas confirmée par cette instruction officielle.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://iceclear.github.io/projects/seedvr2/ | SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training | 2026-09-05 |
| https://arxiv.org/abs/2506.05301 | SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training | 2026-09-05 |
| https://github.com/ByteDance-Seed/SeedVR | ByteDance-Seed/SeedVR — Repo for SeedVR2 and SeedVR | 2026-09-05 |
| https://huggingface.co/ByteDance-Seed/SeedVR-Models/tree/main | ByteDance-Seed/SeedVR2-3B model tree | 2026-09-05 |
| https://huggingface.co/lvladikov/SeedVR2-1.4B | lvladikov/SeedVR2-1.4B | 2026-09-05 |
| https://huggingface.co/lvladikov/SeedVR2-1.4B/tree/main/comfyui | SeedVR2-1.4B ComfyUI files | 2026-09-05 |
| https://huggingface.co/lvladikov/SeedVR2-1.4B/blob/main/comfyui/seedvr2_1.4b_upscale_image.json | SeedVR2-1.4B ComfyUI upscale workflow | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1va0dxy/seedvr214b_a_6layer_distillation_of_seedvr27b/ | SeedVR2-1.4B — a 6-layer distillation of SeedVR2-7B | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:seedvr2`, fil `seedvr2-development-and-distribution`, 3 événements datés du 2025-06-09 au 2026-07-30.
- **Note pratique :** Au 2026-07-30, il convient de considérer SeedVR2 comme une voie de déploiement versionnée : consultez d'abord les références officielles du projet et du dépôt, puis évaluez de manière indépendante le paquet ComfyUI 1.4B lié avant de l'utiliser dans un workflow.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

<!-- authored-live-update:8c58cec247991662f3b16a987bbace4205f20ba435517274aa6d2da0aaa171bb -->
# SeedVR2 TensorRT Studio {#seedvr2-tensorrt-studio}

VRGDG SeedVR2 TensorRT Studio est une application Windows autour de SeedVR2, et non une publication officielle de ByteDance. Sa page publique se trouve dans le [dépôt du créateur](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio). La page GitHub Releases ne contenait aucune version lors de la vérification ; l'installation et les mises à jour proviennent donc de la branche `main` du dépôt. [Releases](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/releases)

Le Studio utilise une intégration SeedVR2 compatible, dérivée du projet ComfyUI de NumZ. Le créateur indique que ses propres ajouts comprennent le passage à l'encodeur TensorRT, la capture des latents et un chemin rapide qui s'arrête avant le décodage VAE. Il s'agit d'une couche d'encapsulation et d'intégration. [Mentions des tiers](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/THIRD_PARTY_NOTICES.md)

## Ce qu'apporte le workflow {#what-the-workflow-adds}

- Un court aperçu avant le rendu complet.
- Vues original, restauré, comparaison par balayage (wipe) et côte à côte.
- Décodage VAE TensorRT local sur les cartes NVIDIA RTX prises en charge.
- Dossiers de sortie distincts par tâche, contenant les médias, les manifestes et les journaux.
- Segments reprenables pour une vidéo longue.

L'ordre prévu est simple : charger un clip, choisir la cible, produire un aperçu représentatif, utiliser la vue wipe ou côte à côte, puis inspecter les visages, les taches de rousseur, les grains de beauté et autres marques permanentes avant le rendu complet. [Workflow](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/README.md)

Le chemin TensorRT expose des lots temporels de 5 et 21. Il s'agit de choix de groupes de trames au sein d'un même rendu. Ils ne prouvent pas que le Studio dispose d'une file de traitement par lots de plusieurs fichiers. Un ticket ouvert le 2 septembre demandait le traitement successif de plusieurs fichiers ; le traitement par lots multi-fichiers doit donc être considéré comme non vérifié pour l'instant. [Tickets](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/issues)

## Limites de l'installation {#installation-boundary}

L'installation fournie cible Windows 11, un pilote NVIDIA RTX à jour et au moins 35 Go d'espace libre. Elle construit localement les plans de moteur TensorRT pour le GPU et l'environnement d'exécution TensorRT installés. Ne copiez pas de fichiers de plan TensorRT provenant d'un autre GPU ou d'un autre environnement d'exécution. [Guide d'installation](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/docs/INSTALLATION.md)

Si le décodage TensorRT échoue après la passe de restauration, le Studio indique qu'il peut relancer le décodage des latents sauvegardés avec son décodeur Stable. Cela évite de répéter la restauration, mais il s'agit d'un chemin de repli, et non d'une preuve de la même vitesse ni du même résultat que le décodage accéléré. [Workflow](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/README.md)

## Le découpage en segments exige une vérification de la sortie {#chunking-needs-an-output-check}

La documentation propose un choix automatique des segments ou des segments manuels de 30 secondes à 30 minutes. Les segments terminés sont censés survivre à une interruption, et la reprise redémarre à la première section non achevée.

Ce comportement de reprise ne prouve pas que le fichier assemblé est exploitable. Un ticket ouvert décrit une entrée de 60 secondes découpée en deux segments : les deux fichiers de segments se lisaient correctement, mais la vidéo assemblée se figeait à mi-parcours. Le rapporteur indique que cela se produisait avant les correctifs de taille de fichier et ignore si la correction y est liée. Considérez ce défaut comme non résolu pour la branche `main` actuelle. Notre recommandation avant livraison est de vérifier la durée finale, la durée audio, chaque jonction et un décodage complet. [Ticket n° 30](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/issues/30)

## L'exemple de la RTX 5090 {#the-rtx-5090-example}

Le créateur signale une seule exécution : un clip de 8 secondes en 360p porté en 2K en environ 8 minutes sur une RTX 5090 avec 7B Sharp FP16. Il faut la considérer comme un scénario publié unique, et non comme un benchmark. La source ne donne pas assez de détails sur la fréquence d'images, le lot temporel, le pilote, la version de TensorRT, la dégradation de la source ou la validation de la sortie pour permettre d'en prédire les performances pour une autre tâche. [README](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/README.md)

Il existe aussi des risques de configuration initiale. Un ticket signale un dépassement de mémoire (OOM) lors de l'export ONNX CUDA, pendant l'allocation de 38 050 725 888 octets sur un GPU disposant de 25 756 696 576 octets au total, puis un repli vers un export CPU. Un commentateur Reddit signale également un scintillement après l'ajout de filtres supplémentaires. Il s'agit dans les deux cas de signalements liés à des configurations ou à des utilisateurs précis, et non d'une limite ou d'un préréglage universel. [Ticket n° 26](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/issues/26) · [Retour de la communauté](https://www.reddit.com/r/comfyui_elite/comments/1w6muu7/seedvr2_video_upscaler_suite_github_linked_in_post/)

## Toujours inconnu {#still-unknown_1}

Aucune version packagée du Studio n'a été trouvée. Aucun benchmark indépendant du Studio ni aucune file multi-fichiers vérifiée n'a été trouvé. Les éléments en chinois simplifié restent incomplets : la recherche bornée n'a trouvé que des pages d'annuaire et d'agrégation, et non un document en chinois maintenu par le créateur ni un rapport d'exploitation reproductible en chinois.


<!-- Retained base: 10a1a74b58eb65fd5b18c6a04e3d1b0dcadb09ea; article blob: 19e5cf206339f2bebe4cc872fb877cca05957b85 -->

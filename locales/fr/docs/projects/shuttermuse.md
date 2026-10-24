---
title: "ShutterMuse"
category: projects
date: 2026-07-03
tags: [project, shuttermuse]
aliases: ["ShutterMuse"]
level: 2
source_sha256: 631f96242f53e44accefc3b894fa6e007301503e9f871f13eff7a7060e6838f8
translation: machine
translated_at: '2026-10-24'
---
# ShutterMuse {#shuttermuse}

**Ligne de développement :** `project:shuttermuse` · fil `shuttermuse`  
**Dernier événement :** 2026-07-03 · 1 événement daté depuis le 2026-07-03 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

ShutterMuse est un assistant de photographie au moment de la capture, destiné aux photographes et aux sujets de portrait.

- Évaluation du cadrage : évalue le cadrage.
- Affinement des zones de composition : affine les zones de composition.
- Guidage de pose COCO-17 : guide les poses de portrait.

Le point de contrôle publié comporte 9 milliards de paramètres en BF16, et le projet ne déclare aucune licence pour son code source. Il convient à la recherche et à l'évaluation en local, et non à un service hébergé prêt pour la production.

## Ligne de développement {#development-line}

- **2026-07-03 — Les liens publics du projet ShutterMuse ont été partagés.** Le 2026-07-03, ShutterMuse a partagé les liens d'un site du projet, d'un dépôt GitHub et d'une page Hugging Face. Ces liens attestent une présence publique sur un site, un dépôt de sources et une plateforme de modèles. Ils n'établissent pas une publication, une version, une capacité ou un résultat technique précis.

## Modifications {#what-changed}

- 2026-06-24 — ShutterMuse a introduit CaptureGuide-Bench, un jeu de données de développement de 130 000 échantillons, ainsi qu'un MLLM unifié entraîné par ajustement fin supervisé et par apprentissage par renforcement.
- 2026-07-03 — La documentation de ShutterMuse a mis en lien la page du projet, le code et le modèle. Le README ne date la publication du code, du benchmark et des poids qu'à 2026-06 ; une version distincte de juillet n'est donc pas vérifiée.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-03, considérez ShutterMuse comme un projet disposant de références publiques vers un site, un code source et un modèle. Vérifiez les capacités et versions exactes auprès de ces sources avant toute utilisation.

1. Clonez le dépôt, créez son environnement Conda Python 3.10 et installez les dépendances déclarées.
  — <https://github.com/lijayuTnT/ShutterMuse>
2. Préparez le point de contrôle Qwen-VL de base ou fusionné, ainsi que le LoRA/point de contrôle ShutterMuse. Ne laissez le chemin LoRA vide que pour un point de contrôle entièrement fusionné.
  — <https://github.com/lijayuTnT/ShutterMuse>
3. Exécutez quick_start.sh avec --side photographer pour le guidage de cadrage, ou avec --side subject pour le guidage de pose. Inspectez la prédiction JSON et la visualisation WebP.
  — <https://github.com/lijayuTnT/ShutterMuse>
4. Pour l'évaluation, téléchargez CaptureGuide-Bench dans Benchmark/ et lancez une seule cible d'évaluation officielle à la fois.
  — <https://huggingface.co/datasets/ShutterMuse/CaptureGuide-Bench>

## Bonnes pratiques {#best-practices}

- Choisissez délibérément le flux photographe ou sujet : ils produisent des guidages différents et exigent des entrées différentes.
  — <https://github.com/lijayuTnT/ShutterMuse>
- Traitez les scripts d'entraînement comme des modèles de lancement. Définissez explicitement les chemins locaux du modèle, du jeu de données, du GPU et des sorties avant de les exécuter.
  — <https://github.com/lijayuTnT/ShutterMuse>
- Figez les révisions du dépôt et des poids pour les expériences. Le dépôt contient actuellement des commits mais aucune publication versionnée.
  — <https://github.com/lijayuTnT/ShutterMuse>
- Vérifiez vos droits avant tout déploiement commercial ou redistribution. Le benchmark est réservé à un usage de recherche et la section de licence du dépôt reste incomplète.
  — <https://huggingface.co/datasets/ShutterMuse/CaptureGuide-Bench>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- Aucun journal des modifications exact ni aucune version étiquetée n'identifie un modèle, un dépôt ou une révision de benchmark publiés spécifiquement le 2026-07-03. Le README de première main ne date la publication des ressources qu'à 2026-06.
- La section de licence du dépôt indique qu'elle reste à ajouter. Les droits commerciaux et de redistribution du code et des poids ne sont pas établis ici.
- Aucun fournisseur d'inférence hébergée n'est répertorié pour le modèle à la date d'observation.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://lijayutnt.github.io/ShutterMuse/ | ShutterMuse : guidage photographique au moment de la capture avec des MLLM | 2026-09-05 |
| https://github.com/lijayuTnT/ShutterMuse | GitHub - lijayuTnT/ShutterMuse | 2026-09-05 |
| https://huggingface.co/ShutterMuse/ShutterMuse | ShutterMuse/ShutterMuse · Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2606.25763 | ShutterMuse : guidage photographique au moment de la capture avec des MLLM | 2026-09-05 |
| https://huggingface.co/datasets/ShutterMuse/CaptureGuide-Bench | ShutterMuse/CaptureGuide-Bench | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:shuttermuse`, fil `shuttermuse`, 1 événement daté du 2026-07-03 au 2026-07-03.
- **Note pratique :** Au 2026-07-03, les praticiens peuvent considérer ShutterMuse comme un projet disposant de références publiques vers un site, un code source et une distribution de modèle, en vérifiant ses capacités et versions exactes auprès de ces sources avant toute utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.

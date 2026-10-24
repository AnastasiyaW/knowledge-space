---
title: "DIRECT"
category: projects
date: 2026-06-09
tags: [direct, direct-development, project]
aliases: ["DIRECT"]
level: 2
source_sha256: f4f89f42e1d7dc9cc4b1ed4be4bc61319841badb78de7bef16429624422e766a
translation: machine
translated_at: '2026-10-24'
---
# DIRECT {#direct}

**Ligne de développement :** `project:direct` · fil `direct-development`  
**Dernier événement :** 2026-06-09 · 1 daté depuis le 2026-06-09 · **Recherche :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

DIRECT est un système d'insertion d'objets contrôlable par la pose, destiné aux outils de composition qui placent un objet de référence dans un arrière-plan.

- Apparence de référence : préserve l'apparence de la référence.
- Proxy 3D : utilise un proxy 3D reconstruit pour la pose.
- Contexte de la scène : conditionne sur le contexte de la scène.

Son paquet de poids initial fait 987 Mo, mais il nécessite des composants externes : FLUX, TRELLIS, SigLIP2 et RMBG. Utilisez-le comme un flux de composition local accéléré par GPU, et non comme un modèle hébergé autonome.

## Ligne de développement {#development-line}

- **2026-06-09 — Les ressources du projet DIRECT ont été publiées.** Le 2026-06-09, un message de la ligne de développement de DIRECT a diffusé les liens vers le site du projet, le dépôt source et la page Hugging Face. Pris ensemble, ces liens datés indiquent une étape publique du projet, digne de figurer dans l'historique du développement. Nous n'avons pas examiné le texte de l'annonce ni l'état exact de chaque ressource liée.

## Ce qui a changé {#what-changed}

- **2026-05** — DIRECT a été accepté à ICML 2026 ; son dépôt et sa page de projet sont devenus disponibles.
- **2026-06-04** — La version 1 de l'article DIRECT est parue sur arXiv, en définissant le flux de travail basé sur l'objet de référence, le proxy 3D et l'arrière-plan.
- **2026-06-09** — superGong a publié le modèle initial Image-to-Image de DIRECT.
- **2026-06-30** — L'activité de l'auteur indique la publication et la mise à jour du jeu de données DIRECT-dataset.
- **2026-07** — Le dépôt indique que les données d'entraînement, le code d'entraînement et le code de prétraitement ont été publiés ; il ne donne pas de jour précis.

## Mode d'emploi {#how-to-use-this}

1. Clonez le dépôt, créez l'environnement Python 3.10.18 testé, installez PyTorch 2.4.0 avec CUDA 11.8, puis installez les dépendances et DIRECT.
  — <https://github.com/Gong1130/DIRECT>
2. Avant la première exécution, acceptez les licences restreintes de FLUX.1-Fill-dev et RMBG-2.0, puis authentifiez-vous auprès de Hugging Face ou définissez HF_TOKEN afin que les modèles requis puissent être téléchargés.
  — <https://github.com/Gong1130/DIRECT>
3. Exécutez `python demo/demo.py --gradio_port 7860 --viser_port 8081` ; l'interface segmente et reconstruit l'objet de référence, puis vous permet de manipuler sa pose 3D dans l'arrière-plan.
  — <https://huggingface.co/superGong/DIRECT>
4. Sur une machine distante, redirigez les ports 7860 et 8081 avant d'ouvrir l'interface Gradio locale.
  — <https://github.com/Gong1130/DIRECT>

## Bonnes pratiques {#best-practices}

- Utilisez la pile testée par les auteurs, à savoir Python 3.10.18, PyTorch 2.4.0 et CUDA 11.8 ; définissez CUDA_HOME si les extensions compilées ne trouvent pas la boîte à outils.
  — <https://github.com/Gong1130/DIRECT>
- Prévoyez l'ensemble complet des dépendances : le paquet DIRECT de 987 Mo ne contient que ses propres poids, et non les modèles requis FLUX, TRELLIS, SigLIP2 et de suppression d'arrière-plan.
  — <https://huggingface.co/superGong/DIRECT>
- Vérifiez les conditions d'utilisation commerciale avant tout déploiement : la licence du dépôt autorise l'usage non commercial et invite les utilisateurs commerciaux à contacter les contributeurs.
  — <https://github.com/Gong1130/DIRECT/blob/main/LICENSE.txt>

## Éléments remplacés par ceci {#superseded-by-this}

- 2026-07 : l'hypothèse, valable pour juin uniquement, selon laquelle DIRECT ne comportait que du code d'inférence, une démo et des poids, n'est plus valable ; le dépôt indique que les données d'entraînement, le code d'entraînement et le code de prétraitement ont été publiés.

## Points encore inconnus {#still-unknown}

- La note de version de juillet du dépôt ne porte pas de jour exact ; cette publication ne peut donc pas être consignée comme un événement horodaté.
- Le README contient encore des puces TODO pour des ressources que sa section d'actualités datée indique comme publiées ; aucune étiquette de version immuable ne permet de résoudre proprement cette incohérence.
- Nous n'avons trouvé ni benchmark indépendant et actuel, ni exécution locale de bout en bout ; les performances annoncées restent celles déclarées par les auteurs.
- La couverture en chinois trouvée est un résumé de la méthode, et non un guide d'installation indépendant, un rapport de défaillance ou un benchmark.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://gong1130.github.io/DIRECT/ | Page du projet DIRECT | 2026-09-07 |
| https://github.com/Gong1130/DIRECT | Dépôt Gong1130/DIRECT et notes de version | 2026-09-07 |
| https://huggingface.co/superGong/DIRECT | Fiche du modèle superGong/DIRECT | 2026-09-07 |
| https://huggingface.co/superGong/activity/all | Activité de superGong sur Hugging Face | 2026-09-07 |
| https://huggingface.co/superGong/DIRECT/tree/2ec64cedd13ed7f2f81edf836ce6a90d503c3683 | Révision initiale du modèle DIRECT | 2026-09-07 |
| https://arxiv.org/abs/2606.06601 | Article DIRECT sur arXiv | 2026-09-07 |
| https://github.com/Gong1130/DIRECT/blob/main/LICENSE.txt | Licence de DIRECT | 2026-09-07 |
| https://hyper.ai/cn/papers/2606.06601 | Résumé de la méthode DIRECT en chinois simplifié | 2026-09-07 |

## Brief agent {#agent-brief}

- **Sujet :** `project:direct`, fil `direct-development`, 1 événement daté, du 2026-06-09 au 2026-06-09.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

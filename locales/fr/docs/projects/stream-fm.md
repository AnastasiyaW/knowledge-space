---
title: "Stream.FM"
category: projects
date: 2026-05-14
tags: [project, stream-fm, stream-fm-development, stream_fm]
aliases: ["Stream.FM"]
level: 3
source_sha256: 00b978984b5aa8aaa9acac66ab98cff536406c97bcabd0eaf2434dd0beb0316e
translation: machine
translated_at: '2026-10-24'
---
# Stream.FM {#streamfm}

**Ligne de développement :** `project:stream-fm` · fil `stream-fm-development`  
**Dernier événement :** 2026-05-14 · 1 événement daté depuis le 2026-05-14 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Stream.FM est une base de code de recherche en PyTorch, sous licence AGPL-3.0, destinée aux ingénieurs en apprentissage automatique audio qui développent une restauration de la parole trame par trame.

- Amélioration de la parole et déréverbération
- Post-filtrage de codecs, extension de bande passante et récupération de phase STFT
- Vocodage Mel via l'implémentation MelFlow apparentée et incluse

## Ligne de développement {#development-line}

- **2026-05-14 — Les ressources du projet Stream.FM ont été liées.** Le 2026-05-14, Stream.FM a été relié à un site d'exemples, à un dépôt source GitHub et à un dossier Google Drive. Ensemble, ces références établissent un ensemble public de ressources du projet pour cette ligne, sans toutefois établir une version publiée et versionnée, ni le contenu des documents complémentaires.

## Modifications {#what-changed}

- 2025-09-18 — MelFlow, le travail apparenté sur le vocodeur Mel en flux, intégré par la suite à Stream.FM, est paru sous forme de prépublication sur arXiv.
- 2025-12-22 — Stream.FM est paru sous forme de prépublication sur arXiv.
- 2026-04-21 — La v3 sur arXiv est devenue la dernière révision répertoriée de l'article Stream.FM.
- 2026-05-05 — Les auteurs ont présenté, lors d'ICASSP, l'amélioration conjointe de la parole en temps réel et l'extension de bande passante.
- 2026-05-11 — Le code source initial public de Stream.FM et MelFlow a été commité.
- 2026-05-13 — La licence AGPL-3.0 a été ajoutée au dépôt source.
- 2026-05-14 — La page du projet, le dépôt et les liens vers le dossier de points de contrôle ont été enregistrés ensemble ; aucun commit en amont distinct ni aucune GitHub Release ne sont attestés pour cette date.
- 2026-05-23 — La maintenance des citations du dépôt n'a modifié que la documentation.
- 2026-06-05 — Le dernier push en amont visible n'a mis à jour que la citation TASL de Stream.FM.

## Mode d'emploi {#how-to-use-this}

Consultez ensemble le site d'exemples, le dépôt et les documents du Drive lorsque vous évaluez Stream.FM à la date du 2026-05-14. Aucune procédure d'installation, aucun résultat ni aucune version publiée n'est encore vérifié.

1. Créez un environnement Python 3.10+ et installez les dépendances documentées à partir d'un index de wheels PyTorch CUDA correspondant au runtime CUDA local.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
2. Téléchargez un point de contrôle depuis le dossier Google Drive documenté vers un répertoire local de checkpoints, à l'aide de la commande gdown maintenue.
  — <https://drive.google.com/drive/folders/1u2QKjGAdxblQVV8-qmifSM9AwhT86LER>
3. Choisissez la configuration de tâche correspondant à l'architecture du point de contrôle, puis lancez inference.py avec un répertoire d'entrée de fichiers WAV, un répertoire de sortie, le solveur et le chemin du point de contrôle.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
4. Pour une intégration en flux trame par trame, implémentez l'initialisation de l'état et les appels à forward_step autour du backbone CausalNCSNpp, plutôt que de vous attendre à un serveur de streaming prêt à l'emploi.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>

## Bonnes pratiques {#best-practices}

- Commencez avec le solveur 5xeuler suggéré par les auteurs, et n'augmentez le parallélisme GPU que si la machine cible dispose de ces GPU.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
- Assurez la correspondance entre la configuration Hydra et l'architecture du point de contrôle ; le chemin d'inférence documenté exige ce couplage.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
- Pour le streaming, évaluez les CUDA graphs et le wrapper torch.compile par défaut sur le matériel cible, plutôt que de supposer que la latence décrite dans l'article se transpose telle quelle.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
- Mesurez la latence de bout en bout sur le matériel cible ; le résultat publié de 48 ms correspond à une configuration de recherche mesurée, et non à une garantie indépendante du matériel.
  — <https://arxiv.org/abs/2512.19442>
- Ne chargez que des points de contrôle de confiance : l'inférence utilise torch.load avec weights_only=False.
  — <https://raw.githubusercontent.com/sp-uhh/streamfm/main/inference.py>
- Examinez les obligations de la licence AGPL-3.0 avant d'intégrer le code du dépôt dans un produit ou un service réseau.
  — <https://github.com/sp-uhh/streamfm/blob/main/LICENSE>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-05-14 — Correction : il s'agit de la date à laquelle les liens ont été enregistrés, et non d'une version amont de Stream.FM attestée séparément ; le code source public a commencé le 2026-05-11 et GitHub ne répertorie aucune version publiée.
- 2026-05-23 — La maintenance du dépôt limitée aux citations ne constitue pas une preuve d'une nouvelle version du modèle, du point de contrôle ou du runtime.
- 2026-06-05 — La mise à jour de la citation TASL ne concerne que la documentation ; aucune version ultérieure officielle du modèle, du jeu de données ou du paquet n'a été trouvée dans les sources consultées.

## Inconnues restantes {#still-unknown}

- Le dossier Drive lié n'a pas pu être énuméré ici ; son inventaire des points de contrôle au 2026-05-14, ses empreintes, sa disponibilité et son contenu ne sont donc pas vérifiés.
- La licence AGPL-3.0 est vérifiée pour le code source du dépôt ; aucune licence distincte ni fiche modèle pour les poids hébergés sur Drive n'a été vérifiée.
- Les résultats de latence de l'article ne prouvent ni la latence sur le dispositif cible, ni celle des entrées-sorties audio, ni la latence en production.
- Aucune GitHub Release, aucun artefact de paquet ni aucun manifeste de version des points de contrôle n'a été trouvé ; les adoptants doivent consigner le commit source exact et l'identité du point de contrôle qu'ils utilisent.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://sp-uhh.github.io/streamfm_examples/ | Stream.FM | Real-Time Streamable Generative Speech Restoration with Flow Matching | 2026-09-05 |
| https://github.com/sp-uhh/streamfm | sp-uhh/streamfm | 2026-09-05 |
| https://drive.google.com/drive/folders/1u2QKjGAdxblQVV8-qmifSM9AwhT86LER | Dossier de points de contrôle Stream.FM | 2026-09-05 |
| https://arxiv.org/abs/2512.19442 | Real-Time Streamable Generative Speech Restoration with Flow Matching — arXiv:2512.19442 | 2026-09-05 |
| https://arxiv.org/abs/2509.15085 | Real-Time Streaming Mel Vocoding with Generative Flow Matching — arXiv:2509.15085 | 2026-09-05 |
| https://cmsworkshops.com/ICASSP2026/view_demosession.php?mid=55 | Liste des démonstrations ICASSP 2026 (Show-and-Tell) | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/17ec317c3974e1a4b0b4e3ebfe2a3a99fbbd616c | Code public initial de Stream.FM et MelFlow — 17ec317 | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/c4b9c2b | Commit c4b9c2b de sp-uhh/streamfm | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/1a8226884432a17c7b71945a4b7d3c015dfe6cc8 | Commit 1a822688 de sp-uhh/streamfm | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/ab2700c1154acc5c2ce67a5344182028336413f5 | Commit ab2700c de sp-uhh/streamfm | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/blob/main/README.md | README.md — sp-uhh/streamfm | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/blob/main/LICENSE | LICENSE — sp-uhh/streamfm | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/releases | Releases — sp-uhh/streamfm | 2026-09-05 |
| https://raw.githubusercontent.com/sp-uhh/streamfm/main/inference.py | inference.py — sp-uhh/streamfm | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:stream-fm`, fil `stream-fm-development`, 1 événement daté du 2026-05-14 au 2026-05-14.
- **Note pratique :** Au 2026-05-14, les praticiens qui évaluent Stream.FM doivent consulter ensemble le site d'exemples, le dépôt source et les documents complémentaires du Drive ; aucune procédure d'installation, aucun résultat ni aucune version publiée n'est encore vérifié.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

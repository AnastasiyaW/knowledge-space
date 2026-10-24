---
title: "DMX"
category: projects
date: 2026-04-09
tags: [dmx, dmx-format-release, dmx_format_release, project]
aliases: ["DMX"]
level: 2
source_sha256: 29584239a69cbc51a6923baf08040ea2a96d2019b1f78655605238cdcde8a8a9
translation: machine
translated_at: '2026-10-24'
---
# DMX {#dmx}

**Ligne de développement :** `project:dmx` · fil `dmx-format-release`  
**Dernier événement :** 2026-04-09 · 1 événement daté depuis le 2026-04-09 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

DMX est un paquet Python destiné aux équipes qui distribuent des modèles safetensors : archives `.dmx` sans perte, deltas `.dmxd` relatifs à une base, vérification d'aller-retour et métadonnées de lignée intégrées. Limite : toutes les versions publiées sur PyPI jusqu'à 1.5.3 incluse ont été retirées (yanked), ce qui en fait une dépendance de production non sûre si elle n'est pas épinglée.

## Ligne de développement {#development-line}

- **2026-04-09 — DMX a été présenté publiquement comme un format de compression des poids de modèles d'IA.** Le 2026-04-09, DMX a été présenté publiquement via un message de la communauté ComfyUI renvoyant vers un dépôt GitHub et un profil Hugging Face. Les documents liés identifient le projet comme concernant la compression des poids de modèles d'IA. Les éléments disponibles n'établissent pas ses spécifications techniques, sa maturité de version ni les intégrations prises en charge.

## Ce qui a changé {#what-changed}

2026-04-09 — DMX a été lancé comme compresseur en ligne de commande destiné au stockage et au transfert de modèles ; l'historique des paquets publié le jour du lancement recense les versions 0.4.0 et 0.5.0, retirées par la suite. Le flux de travail initial exigeait une décompression vers safetensors avant toute utilisation dans ComfyUI ; le lancement annonçait 9,1 Go vers 1,8 Go, 7,2 Go vers 1,5 Go, et +0,16 % de perplexité sur Llama 3 8B. 2026-04-10 — La version 0.6.0 a été publiée sur PyPI, puis retirée. 2026-04-11 — La version 0.7.0 a été publiée sur PyPI, puis retirée. 2026-04-19 — Les versions 1.0.0 et 1.1.0 ont été publiées sur PyPI, puis retirées ; la documentation ultérieure du paquet décrit des archives sans perte, des deltas, la traçabilité des provenances et un runtime GPU. 2026-04-20 au 2026-04-25 — Les versions 1.2.0 à 1.5.3 ont été publiées, toutes retirées par la suite. Un delta Qwen2.5-3B-Instruct illustre la voie de distribution plus récente : 2,88 Go de delta int16 contre 13,59 Go pour le modèle complet, mais il exige la base Qwen2.5-3B exacte et un export fusionné en un seul fichier.

## Comment l'utiliser {#how-to-use-this}

Au 2026-04-09, les praticiens qui évaluent le stockage ou le transfert de poids de modèles peuvent considérer DMX comme un projet de format de compression récemment annoncé, mais doivent vérifier les détails d'implémentation et la compatibilité dans son dépôt avant de l'adopter.

1. Ne pas installer une version courante non épinglée : sélectionner et auditer d'abord une roue (wheel) spécifique, car les versions listées ont été retirées.
  — <https://pypi.org/project/dmx-compress/>
2. Pour une archive sans perte, exécuter `dmx compress model.safetensors model.dmx`, puis le prouver avec `dmx verify model.safetensors model.dmx`.
  — <https://pypi.org/project/dmx-compress/>
3. Restaurer un point de contrôle portable avec `dmx decompress model.dmx restored.safetensors` ; utiliser les safetensors restaurés dans les outils qui ne chargent pas DMX nativement.
  — <https://pypi.org/project/dmx-compress/>
4. Pour le delta Qwen publié, obtenir la base Qwen/Qwen2.5-3B exacte, appliquer `dmx delta-reconstruct`, puis charger les safetensors reconstruits dans le framework cible.
  — <https://huggingface.co/Senat1/dmx-qwen2.5-3b-instruct-delta>

## Bonnes pratiques {#best-practices}

- Conserver le point de contrôle original et exécuter une vérification d'aller-retour avant de supprimer ou de distribuer un artefact DMX.
  — <https://pypi.org/project/dmx-compress/>
- Considérer un delta comme lié à son point de contrôle de base déclaré ; la reconstruction devrait échouer avec une autre base.
  — <https://huggingface.co/Senat1/dmx-qwen2.5-3b-instruct-delta>
- Pour le flux de travail du 9 avril, considérer DMX comme une compression du disque et des téléchargements, et non comme une réduction de la VRAM de ComfyUI ; le chargement natif dans ComfyUI n'était alors qu'un point de feuille de route.
  — <https://www.reddit.com/r/comfyui/comments/1saeezm/i_built_a_compression_format_for_ai_model_weights/>

## Remplacé par ceci {#superseded-by-this}

- 2026-04-09 — La recommandation selon laquelle DMX n'était qu'un compresseur de stockage externe est obsolète par rapport aux affirmations ultérieures du paquet concernant la prise en charge d'un runtime à résidence compressée, affirmations qui restent insuffisamment reproductibles pour une adoption en production.
- 2026-04-09 — La recommandation de s'attendre à un nœud ComfyUI natif n'est plus une instruction valable : utiliser les safetensors restaurés, sauf si une intégration distincte et vérifiée est disponible.

## Points encore inconnus {#still-unknown}

- Le schéma de réponse demandé ne comporte pas de champs `event_findings` ni `new_events` ; les ajouts propres à chaque événement et les événements datés ultérieurs sont donc représentés dans `what_changed`.
- L'URL du dépôt GitHub d'origine a renvoyé une erreur 404 lors de la vérification ; le code du dépôt, le journal des modifications et la maintenance actuelle n'ont pas pu être audités de façon indépendante.
- Le README PyPI annonce des benchmarks d'exécution et des affirmations de prise en charge, mais sa documentation technique et de benchmark publique est signalée comme à venir ; ces mesures doivent être traitées comme des affirmations des mainteneurs et non comme des résultats reproduits de façon indépendante.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.reddit.com/r/comfyui/comments/1saeezm/i_built_a_compression_format_for_ai_model_weights/ | I built a compression format for AI model weights — 60-80% smaller, need help testing | 2026-09-05 |
| https://github.com/willjriley/dmx | dépôt willjriley/dmx (erreur 404 lors de l'observation) | 2026-09-05 |
| https://huggingface.co/Senat1/dmx-qwen2.5-3b-instruct-delta | DMX Delta pour Qwen2.5-3B-Instruct | 2026-09-05 |
| https://pypi.org/project/dmx-compress/ | dmx-compress sur PyPI | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:dmx`, fil `dmx-format-release`, 1 événement daté du 2026-04-09 au 2026-04-09.
- **Note pratique :** Au 2026-04-09, les praticiens qui évaluent le stockage ou le transfert de poids de modèles peuvent considérer DMX comme un projet de format de compression récemment annoncé, mais doivent vérifier les détails d'implémentation et la compatibilité dans son dépôt avant de l'adopter.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

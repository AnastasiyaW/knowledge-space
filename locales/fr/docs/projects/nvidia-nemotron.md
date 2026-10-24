---
title: "Nemotron 3.5 Lightning"
category: projects
date: 2026-08-12
tags: [nemotron-3-5-lightning, nvidia-nemotron, nvidia_nemotron, project]
aliases: ["Nemotron 3.5 Lightning"]
level: 2
source_sha256: 8c32a9d423cdaf66a2297b22822944e7d4e44eeaf762494f15c2faa268d229d6
translation: machine
translated_at: '2026-10-24'
---
# Nemotron 3.5 Lightning {#nemotron-35-lightning}

**Ligne de développement :** `project:nvidia-nemotron` · fil `nemotron-3-5-lightning`  
**Dernier événement :** 2026-08-12 · 1 événement daté depuis le 2026-08-12 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Nemotron 3.5 Lightning est un modèle MoE hybride de texte, avec 30B de paramètres au total et 3B actifs, destiné aux développeurs de systèmes agentiques, de chatbots et de RAG. Fonctionnalités : raisonnement avec commutateur thinking, utilisation d'outils, code, contexte long allant jusqu'à 1M de tokens, speculative decoding ; les variantes NVFP4 et BF16 sont disponibles. Limite pratique : le checkpoint NVFP4 occupe environ 22 GB ; NVIDIA indique qu'il peut être exécuté sur une seule DGX Spark ou sur un H100. Verdict : il s'agit d'un modèle d'exécution pour les appels agentiques fréquents, et non d'un remplacement d'un modèle plus grand pour la planification complexe.

## Ligne de développement {#development-line}

- **2026-08-12 — Publication du modèle public Nemotron 3.5 Lightning et des ressources du playground.** Le modèle NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 est sorti : un hybride Mamba-2/MoE/attention de 30B avec 3B actifs, utilisable commercialement, avec un contexte allant jusqu'à 1M de tokens ; il s'accompagne des variantes BF16 et NVFP4, de DSpark/DFlash pour le speculative decoding et d'un routage via NeMo Switchyard. La carte du modèle principale datant la sortie du 2026-08-11, l'événement du 12 août correspond au jour suivant de publication ou de diffusion, et non à un modèle distinct.

## Changements {#what-changed}

2026-08-12 : sortie du NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4, un hybride Mamba-2/MoE/attention de 30B avec 3B actifs, utilisable commercialement, avec un contexte allant jusqu'à 1M de tokens ; il s'accompagne des variantes BF16 et NVFP4, de DSpark/DFlash pour le speculative decoding et d'un routage via NeMo Switchyard. La carte du modèle principale datant la sortie du 2026-08-11, l'événement du 12 août correspond au jour suivant de publication ou de diffusion, et non à un modèle distinct. 2026-08-17 : NVIDIA a publié une analyse de la recette QAD pour NVFP4 : le checkpoint est passé d'environ 66 GB en BF16 à 22 GB ; il s'agit de documentation pour un checkpoint déjà sorti, et non d'une nouvelle version de base.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-08-12, les praticiens doivent considérer Nemotron 3.5 Lightning comme une gamme disposant d'artefacts de modèles publics, d'un playground hébergé et des outils Switchyard associés ; ils doivent choisir le modèle publié précis ou la voie de déploiement à partir de ces ressources, plutôt que de se fier à une republication non vérifiée.

1. Pour un prototype rapide, appelez l'API NVIDIA Build via un client compatible OpenAI avec le nom de modèle `nvidia/nemotron-3.5-lightning-30b-a3b` ; définissez `enable_thinking` et limitez le budget de raisonnement selon la tâche.
  — <https://build.nvidia.com/nvidia/nemotron-3.5-lightning-30b-a3b>
2. Pour un auto-hébergement, lancez le checkpoint NVFP4 avec vLLM ou SGLang, et utilisez le nom renvoyé par `/v1/models` dans un client compatible OpenAI.
  — <https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4>
3. Dans un système agentique, confiez à Lightning les actions massives — appels d'outils, vérification des résultats et mise en forme — et réservez la planification complexe à un modèle plus puissant.
  — <https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/>

## Bonnes pratiques {#best-practices}

- Commencez par mesurer la voie NVFP4/BF16 de référence sur vos propres tâches ; choisissez le speculative decoding en fonction de la concurrence : DSpark est recommandé pour la DGX Spark et une faible concurrence, MTP pour une concurrence moyenne et élevée.
  — <https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/>
- N'utilisez pas le routage comme un fallback implicite : définissez des règles explicites indiquant quelle classe de tâches va vers Lightning, et vérifiez la qualité et le coût des routes via Switchyard.
  — <https://github.com/NVIDIA-NeMo/Switchyard>
- Pour une contrainte de mémoire stricte, envisagez NVFP4 ; la recette QAD de NVIDIA vise à restaurer la qualité après une quantification agressive et doit être validée séparément sur les benchmarks agentiques cibles.
  — <https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/>

## Ce qui est remplacé {#superseded-by-this}

- 2026-08-17 : l'idée selon laquelle NVFP4 ne serait qu'une simple post-training quantization est obsolète pour le checkpoint officiel Lightning NVFP4 : NVIDIA décrit une distillation QAD appliquée par-dessus la PTQ.
- 2026-08-12 : pour l'exécution des étapes agentiques courantes et à haute fréquence, la recommandation antérieure d'utiliser le même grand modèle de raisonnement à chaque appel est remplacée par l'architecture « planification — modèle puissant, exécution — Lightning ».

## Points non établis {#still-unknown}

- Il est impossible, d'après les sources primaires disponibles, de déterminer précisément l'heure de publication des cinq liens du 12 août ; la carte du modèle indique la date de sortie du 2026-08-11, de sorte que l'écart d'un jour peut venir de l'heure de publication ou du fuseau horaire.
- Les déclarations de NVIDIA sur la vitesse et les benchmarks ne remplacent pas une mesure sur un matériel précis, une version de serveur donnée, une concurrence et un harnais agentique déterminés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 | NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 model card | 2026-09-05 |
| https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/ | NVIDIA Nemotron 3.5 Lightning Delivers Fast, Accurate Specialized Task Execution for Long-Running Agents | 2026-09-05 |
| https://build.nvidia.com/nvidia/nemotron-3.5-lightning-30b-a3b | nvidia/nemotron-3.5-lightning-30b-a3b on NVIDIA Build | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Switchyard | NVIDIA-NeMo/Switchyard | 2026-09-05 |
| https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/ | Developing Nemotron 3.5 Lightning NVFP4 with QAD Using NVIDIA Model Optimizer | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:nvidia-nemotron`, fil `nemotron-3-5-lightning`, 1 événement daté, du 2026-08-12 au 2026-08-12.
- **Note pratique :** À partir du 2026-08-12, les praticiens doivent considérer Nemotron 3.5 Lightning comme une gamme disposant d'artefacts de modèles publics, d'un playground hébergé et des outils Switchyard associés ; ils doivent choisir le modèle publié précis ou la voie de déploiement à partir de ces ressources, plutôt que de se fier à une republication non vérifiée.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.

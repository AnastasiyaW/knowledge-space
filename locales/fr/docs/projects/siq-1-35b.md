---
title: "SIQ-1-35B — Modèle public et démo"
category: projects
date: 2026-06-17
tags: [project, public-model-and-demo, siq-1-35b, siq_1_35b]
aliases: ["SIQ-1-35B"]
level: 3
source_sha256: 298e53c09186b395cb61bd1f7f411307c697c973cfa691b4a15fbf5b0af399c5
translation: machine
translated_at: '2026-10-24'
---
# SIQ-1-35B — Modèle public et démo {#siq-1-35b-public-model-and-demo}

**Ligne de développement :** `project:siq-1-35b` · fil `public-model-and-demo`  
**Dernier événement :** 2026-06-17 · 1 événement daté depuis le 2026-06-17 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

SIQ-1-35B — un finetune sous licence Apache-2.0 de Qwen/Qwen3.6-35B-A3B destiné au codage local, au raisonnement et à l'utilisation d'outils.

- Modes de chat avec et sans raisonnement (thinking et no-think)
- Distributions BF16 et GGUF
- Service local compatible OpenAI

## Ligne de développement {#development-line}

- **2026-06-17 — Le modèle public SIQ-1-35B et la démo d'agent ont été reliés.** Le 2026-06-17, SIQ-1-35B a été relié à une page de modèle publique sur Hugging Face et à un Space ZeroGPU de hermes-agent. Les dépôts autoresearch, parameter-golf et de benchmark y ont été reliés en parallèle. Ces liens confirment les fichiers publics, mais pas les affirmations de l'auteur sur les benchmarks.

## Modifications {#what-changed}

2026-06-17 — La fiche du modèle a renommé SIQ-1-35B en « SIQ-1-tiny-35b ». Elle présente le modèle comme un agent universel pour l'autoresearch, le codage et le raisonnement. La mise à jour a ajouté des graphiques de benchmarks, des profils de service, des prompts et un lien vers la démo, sans téléversement de poids enregistré ce jour-là.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-06-17, considérer SIQ-1-35B comme un modèle public accompagné d'une démo d'agent. Vérifier de manière indépendante les capacités et les affirmations de benchmark avant de s'y fier.

1. Commencer par le GGUF Q4_K_M en local : `llama serve -hf AlexWortega/SIQ-1-35B:Q4_K_M`, puis utiliser l'endpoint compatible OpenAI sur localhost.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
2. Pour les appels d'outils et le raisonnement, utiliser le profil llama.cpp documenté avec `--jinja`, le déchargement sur GPU et un contexte de 131072 tokens réparti sur quatre slots.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
3. Pour un service en BF16, utiliser la configuration SGLang documentée avec un parallélisme de tenseurs de 2 et les parseurs de raisonnement et d'appels d'outils Qwen3.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
4. Définir `enable_thinking=true`, `Reasoning effort: high` et une température de 0 pour le raisonnement complexe. Désactiver le raisonnement pour les réponses directes.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
5. Avant d'activer le décodage spéculatif MTP, récupérer le GGUF compagnon actuel et vérifier qu'il se charge avec la quantification du tronc choisie.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B/commit/cb6f95ec76411517babbfa6a854f7f0425313ff4>

## Bonnes pratiques {#best-practices}

- Garder `--jinja` activé pour llama.cpp : le modèle de chat Qwen documenté porte les balises de raisonnement et d'appels d'outils.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
- Présenter les résultats de benchmark avec la précision, le mode de prompt et les paramètres d'échantillonnage ; la fiche distingue la co-mesure Q4 de son résultat BF16.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
- Traiter MTP comme sensible à la version : le compagnon a été corrigé le 2026-06-23 après une couche draft incorrecte, et des utilisateurs ont signalé plus tôt des échecs de chargement.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B/discussions/2>
- Utiliser un runtime local plutôt que la démo ZeroGPU hébergée tant qu'elle n'est pas rétablie ; elle renvoyait une erreur d'exécution `libcuda.so.1` manquante lors de la consultation.
  — <https://huggingface.co/spaces/AlexWortega/hermes-agent-zerogpu>
- Ne pas présenter le test d'une heure sur un seul A6000 mentionné dans la fiche comme un résultat officiel du classement Parameter Golf ; ce projet limite les soumissions au classement à dix minutes sur 8×H100.
  — <https://github.com/openai/parameter-golf>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-17 — Le modèle est un `finetune`, et non un adaptateur. L'historique des publications corrige explicitement cette relation.
- 2026-06-23 — Les anciens compagnons DFlash ne contenant que le vocabulaire et les compagnons MTP avec la mauvaise couche sont obsolètes ; le dépôt les a remplacés par la couche MTP de Qwen3.6-35B-A3B et des noms de tenseurs mis à jour.

## Toujours inconnu {#still-unknown}

- Aucune évaluation indépendante des affirmations sur SIQ n'est disponible. Considérer les chiffres GPQA, autoresearch, codage et BullshitBench comme rapportés par l'auteur.
- SIQ-1-35B est le nom du dépôt, alors que sa fiche du 2026-06-17 appelle le même modèle SIQ-1-tiny-35b. L'historique des commits ne montre aucune identité de modèle distincte.
- Karpathy autoresearch et OpenAI Parameter Golf utilisent des configurations d'entraînement et d'évaluation différentes. Les sources ne montrent aucune filiation directe des données d'entraînement avec SIQ-1-35B.
- SIQ est étiqueté comme génération de texte alors que sa base Qwen3.6 est multimodale. La fiche du modèle ne confirme pas la prise en charge d'une entrée visuelle.
- L'échec de la démo ZeroGPU hébergée relève d'un problème du runtime hébergé, et non d'une preuve que le service local en GGUF ou en BF16 échoue.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/AlexWortega/SIQ-1-35B | Fiche du modèle AlexWortega/SIQ-1-35B | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/commits/d6a09a9f86bf21d60db5b575578a1df47d222adf/README.md | Historique des commits du README de SIQ-1-35B | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/commits/cb6f95ec76411517babbfa6a854f7f0425313ff4 | Historique des commits du dépôt SIQ-1-35B jusqu'à la correction MTP | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/commit/cb6f95ec76411517babbfa6a854f7f0425313ff4 | Commit de correction de la couche MTP depuis Qwen3.6-35B-A3B | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/discussions/2 | Discussion sur le chargement MTP de SIQ-1-35B | 2026-09-05 |
| https://huggingface.co/spaces/AlexWortega/hermes-agent-zerogpu | Hermes · Space ZeroGPU SIQ-1-35B | 2026-09-05 |
| https://github.com/karpathy/autoresearch | karpathy/autoresearch | 2026-09-05 |
| https://github.com/openai/parameter-golf | openai/parameter-golf | 2026-09-05 |
| https://github.com/petergpt/bullshit-benchmark | BullshitBench v2 | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:siq-1-35b`, fil `public-model-and-demo`, 1 événement daté du 2026-06-17 au 2026-06-17.
- **Note pratique :** À partir du 2026-06-17, considérer SIQ-1-35B comme disposant d'un artefact de modèle public relié et d'un point d'entrée de démo d'agent, tout en vérifiant de manière indépendante les capacités et les affirmations de benchmark avant de s'y fier.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

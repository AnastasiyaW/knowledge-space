---
title: "Qwopus3.6-27B-Coder-MTP"
category: projects
date: 2026-06-18
tags: [project, qwopus3-6-27b-coder-mtp, qwopus3-6-27b-coder-mtp-development, qwopus3_6]
aliases: ["Qwopus3.6-27B-Coder-MTP"]
level: 2
source_sha256: 3f6827bcf35f8e199e73df98f4d7a43f3f129d097e2ac091380b1717c59aab20
translation: machine
translated_at: '2026-10-24'
---
# Qwopus3.6-27B-Coder-MTP {#qwopus36-27b-coder-mtp}

**Ligne de développement :** `project:qwopus3-6-27b-coder-mtp` · fil `qwopus3-6-27b-coder-mtp-development`  
**Dernier événement :** 2026-06-18 · 1 événement daté depuis le 2026-06-18 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

Qwopus3.6-27B-Coder-MTP est un fine-tuning orienté code de Qwopus3.6-27B-v2, doté de têtes MTP de draft pour le travail sur dépôts en local.

- Génération de code pour des dépôts.
- Débogage et correction de code.
- Appels d'outils structurés.

Les quantifications GGUF disponibles vont de 13.5 GB (Q3_K_M) à 29 GB (Q8_0). Le score SWE-bench rapporté par la communauté est de 335/500 lors d'une exécution Q5_K_M en mode thinking désactivé, les autres suites étant en attente. Nous l'utilisons comme modèle de code local expérimental, et non comme référence de production validée de manière indépendante.

## Ligne de développement {#development-line}

- **2026-06-18 — Lien vers l'artefact GGUF de Qwopus3.6-27B-Coder-MTP.** Nous avons relié Qwopus3.6-27B-Coder-MTP-GGUF, sa base Qwopus3.6-27B-v2 et le workflow de conversion MTP vers GGUF de Qwen comme un seul chemin de décodage spéculatif en local.

## Changements {#what-changed}

2026-06-18 : Qwopus3.6-27B-Coder-MTP-GGUF, sa base Qwopus3.6-27B-v2 et le workflow de conversion MTP vers GGUF de Qwen ont été reliés comme un seul chemin de décodage spéculatif en local.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-06-18, considérez l'artefact GGUF lié comme un format de déploiement candidat pour Coder-MTP. Vérifiez la provenance, la compatibilité avec le runtime, la licence et les performances par rapport au modèle v2 lié avant toute utilisation.

1. Choisissez une quantification GGUF selon le stockage et la mémoire disponibles. Le dépôt liste les builds de Q3_K_M à Q8_0.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/tree/main>
2. Exécutez le GGUF dans une application locale compatible avec llama.cpp. La fiche du modèle cite llama.cpp, Ollama et LM Studio comme cibles compatibles.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF>
3. Gardez les définitions d'outils et le prompt système alignés sur le format d'entraînement pour les agents. Gérez côté client le texte placé à l'intérieur des balises <think>.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md>

## Bonnes pratiques {#best-practices}

- Considérez le score SWE-bench de 67.0 % rapporté comme la mesure d'une configuration unique, et non comme un classement inter-harnais. La fiche indique que la version est expérimentale et que les autres suites sont en attente.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md>
- Exécutez le preflight avant de télécharger les poids lors de la création ou du rééemballage d'un GGUF MTP. Une incohérence de configuration source/cible ou un espace disque insuffisant bloque la construction.
  — <https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md>
- Effectuez un test de fumée sur le GGUF avant l'envoi ou le déploiement. Utilisez un modèle source de têtes MTP correspondant plutôt que de supposer que les têtes se transfèrent d'une variante à l'autre.
  — <https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md>

## Remplacé par {#superseded-by-this}

- 2026-07-09 : un commit de nettoyage ayant écrasé l'historique du GGUF a remplacé l'historique granulaire précédent du dépôt. Il n'apporte aucune nouvelle capacité au modèle.

## Points encore inconnus {#still-unknown}

- Aucune source primaire datée ne prouve que les affirmations sur le benchmark, le débit ou la vitesse MTP étaient valides le 2026-06-18. Nous n'attachons pas ces affirmations à cet événement.
- Les métadonnées Hugging Face classent le GGUF comme image-text-to-text, Transformers et architecture CLIP de 0.5B, alors que le README décrit un GGUF de code de 27B. Ce conflit rend les exemples Transformers, vLLM et image non vérifiés pour le déploiement.
- Aucune reproduction indépendante du benchmark, matrice de compatibilité ni changelog de version n'existe pour le point de publication du 2026-06-18.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF | Fiche du modèle Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md | README de Qwopus3.6-27B-Coder-MTP-GGUF | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/tree/main | Arborescence des fichiers de Qwopus3.6-27B-Coder-MTP-GGUF | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-v2 | Fiche du modèle Jackrong/Qwopus3.6-27B-v2 | 2026-09-05 |
| https://github.com/R6410418/Jackrong-llm-finetuning-guide/tree/main/qwen-mtp-gguf | Répertoire du dépôt Qwen MTP GGUF Conversion Skill | 2026-09-05 |
| https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md | README de Qwen MTP GGUF Conversion Skill | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/commits/main | Historique des commits de Qwopus3.6-27B-Coder-MTP-GGUF | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:qwopus3-6-27b-coder-mtp`, fil `qwopus3-6-27b-coder-mtp-development`, 1 événement daté du 2026-06-18 au 2026-06-18.
- **Remarque pratique :** À partir du 2026-06-18, considérez l'artefact GGUF lié comme un format de déploiement candidat pour Coder-MTP. Vérifiez la provenance, la compatibilité avec le runtime, la licence et les performances par rapport au modèle v2 lié avant toute utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

---
title: "Nanbeige4.2-3B"
category: projects
date: 2026-07-26
tags: [nanbeige, nanbeige-4-2-3b, nanbeige4-2-3b, project]
aliases: ["Nanbeige4.2-3B"]
level: 4
source_sha256: a7cf0d95871eb75c04f082a590924f5152072ecbb113a0ee541930970c499aab
translation: machine
translated_at: '2026-10-24'
---
# Nanbeige4.2-3B {#nanbeige42-3b}

**Ligne de développement :** `project:nanbeige-4-2-3b` · fil `nanbeige4-2-3b`  
**Dernier événement :** 2026-07-26 · 1 événement daté depuis le 2026-07-26 · **Recherche effectuée le :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

Nanbeige4.2-3B est un modèle en BF16 destiné aux équipes prêtes à exécuter leur propre runtime et à valider les tâches cibles.

- Mode raisonnement pour le raisonnement en plusieurs étapes.
- Chat template pour des échanges structurés.
- Appels d'outils pour l'exécution de fonctions.
- Runtimes locaux compatibles avec Transformers, SGLang, vLLM et llama.cpp.

3B de paramètres hors embeddings, contre 4B sur la fiche du Hub ; la longueur de contexte annoncée atteint 262144 tokens.

Le modèle convient à des déploiements locaux maîtrisés, mais le code personnalisé et les contextes longs exigent une version épinglée et des tests dans l'environnement cible.

## Ligne de développement {#development-line}

- **2026-07-26 — Publication du modèle public Nanbeige4.2-3B et des ressources d'inférence.** Le 2026-07-26, une mise à jour de développement a référencé la page du modèle Nanbeige4.2-3B sur Hugging Face, une liste filtrée d'entrées liées de modèles de base quantifiés, ainsi qu'un espace d'inférence. Cela établit un point d'accès public daté pour le modèle et ses options de déploiement associées.

## Évolutions {#what-changed}

- 2026-07-21 — L'historique du Hub enregistre le commit initial et un envoi distinct de modeling_nanbeige.py, confirmant un accès anticipé au dépôt et au code, sans établir l'horodatage exact de l'ensemble des poids.
- 2026-07-24 — Nanbeige Lab a soumis la v1 du rapport technique sur arXiv.
- 2026-07-26 — configuration_nanbeige.py a été ajouté au dépôt.
- 2026-07-27 — Le support de Nanbeige4.2 a été fusionné dans la branche master de llama.cpp, mais l'exécution CI associée a échoué.
- 2026-07-28 — Le README a remplacé le lien vers le PDF local du rapport technique par un lien arXiv.
- 2026-08-14 — Un article indépendant a décrit des correctifs pour l'exécution via Transformers sur Apple Silicon/MPS.
- 2026-09-04 — La version stable llama.cpp v0.4.0 mentionne la prise en charge de nanbeige4.2-3B.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-26, les praticiens doivent consulter la page du modèle Nanbeige4.2-3B sur Hugging Face ainsi que les variantes quantifiées associées avant de choisir un artefact, et utiliser l'espace d'inférence lié pour évaluer la disponibilité de l'inférence accessible.

1. Créez un environnement local avec transformers==4.45.1, chargez AutoTokenizer avec use_fast=false, puis AutoModelForCausalLM avec torch_dtype="auto", device_map="auto" et trust_remote_code=true.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
2. Transmettez les messages via tokenizer.apply_chat_template avec add_generation_prompt=true, tokenisez sans tokens spéciaux, et commencez par une courte requête de génération.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
3. Pour un serveur compatible OpenAI, utilisez les forks SGLang nbg42 ou vLLM nanbeige42 spécifiés par le développeur, avec les parseurs nanbeige de raisonnement et d'appels d'outils.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
4. Pour un déploiement GGUF, prenez llama.cpp v0.4.0 comme base documentée, avec le support intégré de Nanbeige4.2-3B, et vérifiez la quantification choisie avec un test de fumée court.
  — <https://github.com/ggml-org/llama.cpp/releases>

## Bonnes pratiques {#best-practices}

- Vérifiez l'auteur et le code avant d'activer trust_remote_code, puis épinglez le hash de commit complet via revision : le Hub recommande cette pratique pour se protéger contre les modifications du code amont.
  — <https://huggingface.co/docs/transformers/models>
- Définissez preserve_thinking=false pour un chat standard ; définissez-le à true pour les tâches multi-étapes d'outils, bureautiques et de code. Utilisez le template avec tools et privilégiez tool_call_format="xml" pour les appels d'outils.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
- Ne considérez pas 262144 tokens comme un contexte garanti fonctionnel ; commencez par une courte exécution cible. Un article indépendant a signalé des problèmes avec le checkpoint d'origine sous Transformers sur Apple Silicon/MPS.
  — <https://arxiv.org/abs/2608.13987>
- Ne vous fiez pas à l'hypothèse obsolète selon laquelle llama.cpp standard ne prend pas en charge le modèle : épinglez v0.4.0 ou vérifiez séparément une version plus récente.
  — <https://github.com/ggml-org/llama.cpp/releases>

## Remplacé par ceci {#superseded-by-this}

- {"claim":"Dater la publication initiale de Nanbeige4.2-3B au 2026-07-26.","obsolete_since":"2026-09-06 (vérification historique)","source_url":"https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commits/main"}
- {"claim":"llama.cpp standard ne prend pas en charge Nanbeige4.2-3B.","obsolete_since":"2026-09-04","source_url":"https://github.com/ggml-org/llama.cpp/releases"}
- {"claim":"Le PDF local dans le README du Hub constitue la référence canonique du rapport technique.","obsolete_since":"2026-07-28","source_url":"https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commit/f56ec5a9650268aa098496734743c25ea778bd2d"}

## Points encore inconnus {#still-unknown}

- L'heure exacte de la première publication publique des poids n'a pas d'horodatage absolu : l'historique du Hub n'indique que le jour calendaire.
- L'espace inference-labs ne bénéficie d'aucune confirmation officielle, et nous n'avons pas pu vérifier son API, sa configuration matérielle ou ses sorties en direct.
- La fiche du modèle consultée ne mentionne aucun point d'accès fournisseur ; cela reflète l'état actuel et ne prouve pas l'absence d'hébergement externe.
- Nanbeige4.2-3B-DSpark officiel est décrit comme un modèle brouillon de 0,8B destiné à accélérer le modèle 3B, mais le Hub n'affiche que des dates relatives de commit ; une date de première publication absolue ne figure pas dans la chronologie.
- La VRAM minimale, la latence et la qualité en production pour des runtimes spécifiques n'ont pas été vérifiées par des tests directs.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B | Nanbeige/Nanbeige4.2-3B · Hugging Face | 2026-09-06 |
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commits/main | Commits · Nanbeige/Nanbeige4.2-3B | 2026-09-06 |
| https://arxiv.org/abs/2607.22083 | Nanbeige4.2-3B : Unlocking Agentic Capabilities in a Compact Model | 2026-09-06 |
| https://github.com/ggml-org/llama.cpp/actions/runs/30278196993 | model: Add support for Nanbeige4.2 (#25994) · ggml-org/llama.cpp@b77d646 · GitHub | 2026-09-06 |
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commit/f56ec5a9650268aa098496734743c25ea778bd2d | Update README.md · Nanbeige/Nanbeige4.2-3B at f56ec5a | 2026-09-06 |
| https://arxiv.org/abs/2608.13987 | Nanbeige4.2-3B on Apple Silicon: Fixing Deployment Bugs and Decreasing Looped Transformer Memory Overhead | 2026-09-06 |
| https://github.com/ggml-org/llama.cpp/releases | Releases · ggml-org/llama.cpp | 2026-09-06 |
| https://huggingface.co/docs/transformers/models | Loading models · Hugging Face | 2026-09-06 |
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B-DSpark | Nanbeige4.2-3B-DSpark · Hugging Face | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:nanbeige-4-2-3b`, fil `nanbeige4-2-3b`, 1 événement daté du 2026-07-26 au 2026-07-26.
- **Note pratique :** Au 2026-07-26, les praticiens doivent consulter la page du modèle Nanbeige4.2-3B sur Hugging Face ainsi que les variantes quantifiées associées avant de choisir un artefact, et utiliser l'espace d'inférence lié pour évaluer la disponibilité de l'inférence accessible.
- **Confiance :** moyenne. Les entrées datées de la section « Remplacé par ceci » font foi pour ce qui est obsolète.

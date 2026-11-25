---
title: "Ornith-1.5"
category: projects
date: 2026-08-20
tags: [ornith, ornith-1-5, project]
aliases: ["Ornith-1.5"]
level: 2
source_sha256: 7cc51670671e0f90b03a2189c82bba359d263a88830c8dde31f9d7b441e6c87b
translation: machine
translated_at: '2026-10-24'
---
# Ornith-1.5 {#ornith-15}

**Ligne de développement :** `project:ornith-1-5` · fil `ornith-1-5`  
**Dernier événement :** 2026-08-20 · 1 événement daté depuis le 2026-08-20 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Ornith-1.5 est une famille de modèles multimodaux sous licence MIT, destinée aux développeurs qui ont besoin d'un endpoint local compatible OpenAI plutôt que d'une API fermée. — 9B Dense pour un seul GPU et versions quantifiées. — 35B-A3B MoE avec environ 3B paramètres actifs par token. — 397B MoE pour le service multi-GPU. Le contexte de base va jusqu'à 262 144 tokens ; le 397B nécessite environ 800 Go en bf16. Verdict : le 35B-A3B est la variante pratique pour serveur, le 397B est la variante pour infrastructure à plusieurs accélérateurs.

## Ligne de développement {#development-line}

- **2026-08-20 — La page de sortie et la collection de modèles Ornith-1.5 ont été liées.** La gamme 9B Dense, 35B MoE et 397B MoE a étendu Ornith-1.0, de la génération de scaffold et de rollout à la génération conjointe de tâches, de scaffold et de rollout pour le RL.

## Ce qui a changé {#what-changed}

2026-08-20 — sortie d'Ornith-1.5 : la gamme 9B Dense, 35B MoE et 397B MoE a étendu Ornith-1.0, de la génération de scaffold et de rollout à la génération conjointe de tâches, de scaffold et de rollout pour le RL.

Complément à l'événement : le modèle 35B est nommé Ornith-1.5-35B-A3B et active environ 3B paramètres par token ; le modèle phare Ornith-1.5-397B est annoncé comme 397B MoE.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-08-20, les praticiens doivent considérer Ornith-1.5 comme une ligne de versions distincte et consulter la page officielle liée ainsi que la collection de modèles avant de choisir un checkpoint ou un workflow.

1. Choisissez le checkpoint : 9B pour un lancement compact, 35B-A3B pour le reasoning/coding sur serveur, 397B si un nœud multi-GPU est disponible.
  — <https://huggingface.co/collections/ornith-ai/ornith-15>
2. Pour le 35B-A3B, installez une version actuelle de vLLM ou SGLang et lancez un serveur compatible OpenAI avec un parser pour le reasoning et les tool calls.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
3. Connectez le client à l'endpoint local /v1 et lisez la réponse finale dans content, et la trace de raisonnement dans reasoning_content.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
4. Pour un simple test local du 9B, chargez le checkpoint via le pipeline Transformers ou lancez-le avec vLLM.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-9B/tree/main>

## Bonnes pratiques {#best-practices}

- Pour les tâches courantes, commencez avec temperature=0.6, top_p=0.95 et top_k=20 ; la valeur temperature=1.0 de l'auteur est destinée à la reproduction des benchmarks.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
- Utilisez un runtime non antérieur à Transformers 5.8.1, vLLM 0.19.1 ou SGLang 0.5.9 pour le 35B-A3B.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
- N'activez pas YaRN/RoPE scaling pour les requêtes courtes : la mise à l'échelle statique peut dégrader la qualité ; ajustez factor en fonction de la fenêtre de contexte réellement nécessaire.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>

## Remplacé par cette entrée {#superseded-by-this}

- 2026-08-20 — Ornith-1.5 remplace Ornith-1.0 comme gamme actuelle pour les tâches où la boucle complète d'auto-amélioration est importante ; Ornith-1.0 reste l'état précédent, et non un modèle supprimé.
- 2026-08-20 — pour le 35B, le nom actuel du checkpoint est Ornith-1.5-35B-A3B, et non le nom générique « Ornith-1.5-35B ».

## Points non vérifiés {#still-unknown}

- La première page d'Ornith est datée uniquement « Aug. 2026 » ; le jour exact 2026-08-20 est donc confirmé par l'événement d'entrée, mais pas séparément sur la page de l'auteur.
- Les benchmarks annoncés sont les résultats de l'équipe Ornith ; aucune reproduction indépendante n'existe dans les sources primaires utilisées.
- La variante mobile Ornith-1.5-9B est mentionnée dans l'annonce, mais sa fiche actuelle distincte et ses exigences d'exécution n'ont pas été vérifiées.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ornith.ai/ornith_1_5.html | Ornith-1.5: From Self-Scaffolding to Self-Improvement | 2026-09-05 |
| https://huggingface.co/collections/ornith-ai/ornith-15 | Ornith-1.5 - a ornith-ai Collection | 2026-09-05 |
| https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200 | ornith-ai/Ornith-1.5-35B-A3B | 2026-09-05 |
| https://huggingface.co/ornith-ai/Ornith-1.5-9B/tree/main | ornith-ai/Ornith-1.5-9B | 2026-09-05 |
| https://huggingface.co/ornith-ai/Ornith-1.5-397B/blame/main/README.md | README.md · ornith-ai/Ornith-1.5-397B | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ornith-1-5`, fil `ornith-1-5`, 1 événement daté du 2026-08-20 au 2026-08-20.
- **Note pratique :** À partir du 2026-08-20, les praticiens doivent considérer Ornith-1.5 comme une ligne de versions distincte et consulter la page officielle liée ainsi que la collection de modèles avant de choisir un checkpoint ou un workflow.
- **Confiance :** moyenne. Les entrées datées « Remplacé par cette entrée » font foi pour ce qui est obsolète.

---
title: "Llama 3.1"
category: projects
date: 2024-07-23
tags: [llama-3-1, project]
aliases: ["Llama 3.1"]
level: 3
source_sha256: d39ac0fb4d5c8a2b2545fae035645cd1c9a148ba8363b2ee034d2c7414f2e041
translation: machine
translated_at: '2026-10-24'
---
# Llama 3.1 {#llama-31}

**Ligne de développement :** `project:llama-3-1` · fil `llama-3-1`  
**Dernier événement :** 2024-07-23 · 1 événement daté depuis le 2024-07-23 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

Llama 3.1 — la famille statique 2024 de Meta, destinée aux équipes qui ont besoin d'une alternative téléchargeable et sous licence à une API de génération de texte hébergée.

- Variantes pré-entraînées et Instruct en 8B, 70B et 405B pour la génération de texte et de code, le chat multilingue, le RAG et les systèmes dotés d'outils.
- Contexte de 128K et huit langues prises en charge.
- Entrée et sortie en texte uniquement, connaissances limitées à décembre 2023 ; le 405B constitue un problème de déploiement multi-GPU.

## Ligne de développement {#development-line}

- **2024-07-23 — Les ressources officielles d'accès à Llama 3.1 sont devenues disponibles.** Le 2024-07-23, les ressources officielles de Llama 3.1 ont ouvert l'accès aux téléchargements de modèles, à Meta AI, à un dépôt de systèmes agentiques et à un modèle de chat hébergé. Cela a marqué la disponibilité effective de cette lignée pour les développeurs et les utilisateurs via ces canaux.

## Ce qui a changé {#what-changed}

- 2024-07-23 — Llama 3.1 a publié des modèles 8B et 70B améliorés ainsi qu'un modèle 405B, avec un contexte de 128K, huit langues prises en charge, la prise en charge de l'utilisation d'outils et des composants compagnons de sécurité et de système.
- 2024-09-25 — Llama 3.2 a ajouté des modèles de texte edge 1B/3B et des modèles de vision 11B/90B ; Llama 3.1 est resté limité au texte.
- 2024-12-06 — Llama 3.3 a introduit un modèle Instruct 70B ultérieur, en texte uniquement, avec un contexte de 128K.
- 2025-04-05 — Llama 4 Scout et Maverick ont introduit la nouvelle génération Llama de Meta, native multimodale et fondée sur une architecture à mélange d'experts.

## Comment l'utiliser {#how-to-use-this}

Au 2024-07-23, les équipes pouvaient évaluer Llama 3.1 via les canaux officiels de téléchargement, de chat et pour développeurs ; confirmez la variante exacte du modèle et les conditions d'utilisation à partir des documents officiels avant tout déploiement.

1. Vérifiez que l'entrée et la sortie en texte uniquement, la plage de tailles 8B/70B/405B et la prise en charge de huit langues conviennent à votre charge de travail ; choisissez un point de contrôle Instruct pour le chat d'assistant.
  — <https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md>
2. Demandez un accès restreint et acceptez la licence communautaire Llama 3.1 avant de télécharger les poids du modèle.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
3. Lancez un premier chat en local avec Transformers 4.43+ en utilisant l'identifiant officiel du modèle Instruct et un pipeline de génération de texte ou AutoModelForCausalLM.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
4. Envoyez des messages basés sur les rôles via tokenizer.apply_chat_template avant la génération, plutôt que d'assembler vous-même les jetons de contrôle de Llama.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
5. Servez le point de contrôle avec vLLM et appelez /v1/chat/completions pour obtenir un point d'accès local compatible OpenAI.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
6. Prévoyez un nœud équipé de 8 GPU H100 de 80 Go pour le 405B en FP8 ; utilisez une inférence multi-nœuds pour le point de contrôle 405B non quantifié.
  — <https://github.com/meta-llama/llama-cookbook/blob/main/getting-started/inference/local_inference/README.md>

## Bonnes pratiques {#best-practices}

- Utilisez un modèle Instruct pour le dialogue d'assistant ; conservez le modèle de base pré-entraîné pour l'adaptation ou pour d'autres tâches de génération de texte.
  — <https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md>
- Conservez le modèle de chat officiel avec apply_chat_template, y compris le prompt de génération.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
- Respectez la licence communautaire Llama 3.1 comme condition de diffusion : les documents et services distribués doivent mentionner l'attribution, et les produits dépassant 700 millions d'utilisateurs actifs mensuels nécessitent une licence distincte de Meta.
  — <https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct-FP8>
- Testez la sécurité et ajustez le modèle pour l'application, puis déployez des garde-fous autour du modèle et des outils externes ; ne déployez jamais le modèle seul.
  — <https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md>
- Ne dimensionnez pas le 405B à partir de son seul libellé de paramètres : distinguez le service mono-nœud en FP8 du service multi-nœuds non quantifié.
  — <https://github.com/meta-llama/llama-cookbook/blob/main/getting-started/inference/local_inference/README.md>

## Remplacé par la suite {#superseded-by-this}

- 2024-09-25 — Choisir Llama 3.1 pour la compréhension de texte ou d'images sur l'appareil est obsolète ; Llama 3.2 a introduit les voies texte edge 1B/3B et vision 11B/90B.
- 2024-12-06 — Comparer uniquement Llama 3.1 70B ou 405B pour un nouveau service texte 70B de Meta est obsolète ; Llama 3.3 70B Instruct est l'option ultérieure à 128K.
- 2025-04-05 — Présenter Llama 3.1 comme la génération Llama la plus récente de Meta est obsolète ; Llama 4 a ajouté la multimodalité native et les modèles à mélange d'experts.

## Inconnues actuelles {#still-unknown}

- Les liens vers la source et vers X n'ont fourni aucun texte exploitable lors de cette passe ; nous n'utilisons donc que leurs dates et URL, sans affirmations non vérifiées.
- Le lien historique llama-agentic-system redirige vers ogx-ai/llama-stack-apps ; cette page ne comporte pas de provenance datée de Meta, et nous ne la considérons donc pas comme une recommandation officielle actuelle de Meta.
- Nous avons trouvé une traduction chinoise publiée le même jour sur Hugging Face, mais aucune annonce primaire distincte de Meta ; nous ne formulons aucune affirmation sur la disponibilité ou la compatibilité propres à la Chine.
- Nous ne disposons ni de la charge de travail, ni du budget matériel, ni de la région cible, ni du contexte de licence ; nous ne retenons donc pas de taille précise de Llama 3.1 ni de remplaçant ultérieur.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ai.meta.com/blog/meta-llama-3-1/ | Présentation de Llama 3.1 : nos modèles les plus performants à ce jour | 2026-09-04 |
| https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md | Fiche modèle Llama 3.1 — meta-llama/llama-models | 2026-09-04 |
| https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct | meta-llama/Llama-3.1-8B-Instruct | 2026-09-04 |
| https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct-FP8 | meta-llama/Llama-3.1-405B-Instruct-FP8 | 2026-09-04 |
| https://github.com/meta-llama/llama-cookbook/blob/main/getting-started/inference/local_inference/README.md | Llama Cookbook — guide d'inférence locale | 2026-09-04 |
| https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/ | Llama 3.2 : révolutionner l'IA en périphérie et la vision avec des modèles ouverts et personnalisables | 2026-09-04 |
| https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/MODEL_CARD.md | Fiche modèle Llama 3.3 — meta-llama/llama-models | 2026-09-04 |
| https://ai.meta.com/blog/llama-4-multimodal-intelligence/ | La famille Llama 4 : le début d'une nouvelle ère d'innovation en IA native multimodale | 2026-09-04 |
| https://github.com/meta-llama/llama-agentic-system | URL llama-agentic-system, actuellement redirigée vers ogx-ai/llama-stack-apps | 2026-09-04 |
| https://huggingface.co/blog/zh/llama31 | Llama 3.1 : analyse des capacités multilingues et de contexte long des modèles 405B/70B/8B | 2026-09-04 |

## Brief d'agent {#agent-brief}

- **Sujet :** `project:llama-3-1`, fil `llama-3-1`, 1 événement daté du 2024-07-23 au 2024-07-23.
- **Remarque pratique :** Au 2024-07-23, les praticiens pouvaient évaluer Llama 3.1 via les canaux officiels de téléchargement, de chat et de ressources pour développeurs ; confirmez la variante exacte du modèle et les conditions applicables à partir des documents officiels avant tout déploiement.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

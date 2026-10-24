---
title: "Holo3"
category: projects
date: 2026-04-02
tags: [h-company-holo3, holo3-model-release, holo3_model_release, project]
aliases: ["Holo3"]
level: 2
source_sha256: d875ab9348fa863216805b8d6709e7b8bc6d6b327ab4a26ff2a30680c7ca14c8
translation: machine
translated_at: '2026-10-24'
---
# Holo3 {#holo3}

**Ligne de développement :** `project:h-company-holo3` · fil `holo3-model-release`  
**Dernier événement :** 2026-04-02 · 1 événement daté depuis le 2026-04-02 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Qu'est-ce que c'est {#what-it-is}

Holo3 est un modèle MoE multimodal destiné à l'utilisation d'un ordinateur (*computer use*). Il accepte du texte et jusqu'à cinq images, et renvoie une action ou une décision sous forme de texte pour les flux de travail d'agents. Les modèles API sont 35B-A3B et 122B-A10B, avec une fenêtre de contexte de 65 536 tokens. Les poids ouverts du modèle original 35B-A3B sont publiés sous licence Apache-2.0. Pour les nouvelles intégrations, commencez par la gamme actuelle Holo3.1 ; considérez Holo3 original comme un point de contrôle ouvert antérieur et compatible.

## Ligne de développement {#development-line}

- **2026-04-02 — H Company a publié le modèle Holo3.** Le 2026-04-02, H Company a publié Holo3 en tant que nouveau modèle. Les pages liées du projet, de l'API et du dépôt de modèles indiquent que la publication était destinée à la fois à un usage direct et à l'accès au modèle. Sans texte source ni recherche indépendante, les capacités exactes et les conditions de publication restent non confirmées.

## Ce qui a changé {#what-changed}

- 2026-04-02 — Poids ouverts Holo3-35B-A3B publiés ; la page de publication présente Holo3 comme un modèle d'utilisation d'ordinateur et désigne 122B-A10B comme modèle phare de l'API.
- 2026-04-15 — HoloTab a rendu le modèle disponible via une application d'agent de navigateur.
- 2026-04-28 — Holotron 3 Nano (30B-A3B) publié comme modèle distinct, plus rapide, pour les tâches d'automatisation informatique.
- 2026-06-01 — Holo3.1 a élargi la gamme avec les variantes 0.8B, 4B, 9B et 35B-A3B, l'appel de fonctions, la prise en charge mobile et des poids quantifiés utilisables en local.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-04-02, évaluez Holo3 à partir de la documentation du modèle et de l'API de H Company avant de le retenir pour un flux de travail ; vérifiez les capacités prises en charge et les conditions d'accès sur les pages liées.

1. Créez un compte Portal-H et une clé API ; le niveau gratuit donne un accès limité à l'API 35B-A3B.
  — <https://hcompany.ai/holo-models-api>
2. Utilisez `holo3-1-35b-a3b` pour des tâches bien définies et limitées dans le temps ; utilisez `holo3-122b-a10b` pour des scénarios complexes en plusieurs étapes, si les conditions commerciales et la tarification conviennent.
  — <https://hcompany.ai/holo-models-api>
3. Pour des exécutions locales de Holo3 original ouvert, téléchargez `Hcompany/Holo3-35B-A3B` via Transformers, vLLM ou SGLang, puis transmettez les messages dans le modèle de chat multimodal.
  — <https://huggingface.co/Hcompany/Holo3-35B-A3B>
4. Pour les configurations mobiles, l'appel de fonctions ou les poids quantifiés utilisables en local, passez à Holo3.1 et adaptez la taille et le format des poids au matériel cible.
  — <https://hcompany.ai/holo3.1>

## Bonnes pratiques {#best-practices}

- Choisissez 35B-A3B pour les automatisations sensibles à la latence, économiques et bien définies ; choisissez 122B-A10B pour des environnements nouveaux ou complexes en plusieurs étapes.
  — <https://hcompany.ai/holo-models-api>
- Vérifiez le format des poids et le runtime avant un déploiement local : Holo3 original est documenté pour Transformers, vLLM et SGLang ; Holo3.1 ajoute FP8, Q4 GGUF et NVFP4.
  — <https://huggingface.co/Hcompany/Holo3-35B-A3B>
- Ne considérez pas les garanties de non-conservation des données comme un substitut à l'examen des données : l'API ne stocke pas les prompts ni les réponses par défaut, mais les journaux conservent les métadonnées de compte et les tokens.
  — <https://hcompany.ai/holo-models-api>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-01 — Holo3.1 remplace Holo3 original comme gamme recommandée pour les configurations mobiles, l'appel de fonctions et les exécutions locales quantifiées.
- 2026-06-01 — Se limiter à une seule variante 35B-A3B est obsolète : les variantes 0.8B, 4B, 9B et 35B-A3B de Holo3.1 sont disponibles.

## Points encore inconnus {#still-unknown}

- Pour 122B-A10B, la page API actuelle indique une licence *Research only* (usage non commercial) ; les conditions d'accès et la licence à la date de publication du 2 avril ne sont pas confirmées séparément.
- Les sources publiques confirment la publication de Holo3-35B-A3B le 2 avril, alors que la page d'annonce principale est datée du 31 mars ; l'écart semble correspondre à la différence entre la date d'annonce et la date de publication des poids, mais l'heure exacte de publication n'est pas précisée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://hcompany.ai/holo3 | Holo3: Breaking the Computer Use Frontier — H Company, 31 mars 2026 | 2026-09-05 |
| https://hcompany.ai/holo-models-api | Holo Models API — H Company | 2026-09-05 |
| https://huggingface.co/Hcompany/Holo3-35B-A3B | Hcompany/Holo3-35B-A3B — Hugging Face | 2026-09-05 |
| https://hcompany.ai/holo3.1 | Holo3.1: Fast & Local Computer Use Agents — H Company, 1 juin 2026 | 2026-09-05 |
| https://hcompany.ai/meet-holotab | HoloTab — H Company, 15 avril 2026 | 2026-09-05 |
| https://hcompany.ai/holotron3 | Holotron 3 Nano — H Company, 28 avril 2026 | 2026-09-05 |

## Résumé pour agent {#agent-brief}

- **Sujet :** `project:h-company-holo3`, fil `holo3-model-release`, 1 événement daté du 2026-04-02 au 2026-04-02.
- **Note pratique :** À partir du 2026-04-02, les praticiens doivent évaluer Holo3 à partir de la documentation du modèle et de l'API de H Company avant de le sélectionner pour un flux de travail ; les capacités exactes prises en charge et les conditions d'accès doivent être vérifiées sur les pages liées.
- **Confiance :** élevée. Les mentions datées de remplacement ci-dessus font foi pour ce qui est obsolète.

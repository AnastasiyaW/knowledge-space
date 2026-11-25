---
title: "North"
category: projects
date: 2026-06-30
tags: [cohere, cohere-north, north-mini-code, project]
aliases: ["North"]
level: 2
source_sha256: 9f2decf3b570aaf683f04dc55cf02bbfd9b93dfa51c3c362bffece3411c57d20
translation: machine
translated_at: '2026-10-24'
---
# North {#north}

**Ligne de développement :** `project:cohere-north` · fil `north-mini-code`  
**Dernier événement :** 2026-06-30 · 1 événement daté depuis le 2026-06-30 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Cohere North Mini Code est un modèle texte sparse-MoE destiné aux ingénieurs qui ont besoin d'une alternative locale aux petits modèles agentiques de code.
- Génération de code.
- Exécution d'outils en terminal.
- Tâches agentiques en plusieurs étapes.
- Appels d'outils structurés.

30 milliards de paramètres au total, 3 milliards actifs, contexte de 256K, génération jusqu'à 64K tokens. Il convient aux harnais d'agents de codage contrôlés, mais nécessite un runtime compatible et une propagation correcte de l'état des outils et de la réflexion.

## Ligne de développement {#development-line}

- **2026-06-30 — CohereLabs a publié les pages du modèle North Mini Code 1.0 sur Hugging Face.** Le 2026-06-30, la ligne de développement renvoie vers les pages Hugging Face de North-Mini-Code-1.0 et d'une variante w4a16. Cette étape constitue une évolution notable de la distribution de la ligne North Mini Code, car elle identifie à la fois un artefact de modèle de base et une variante nommée séparément.

## Modifications {#what-changed}

- 2026-06-09 — Cohere a publié North-Mini-Code-1.0 sous licence Apache 2.0, premier modèle de la famille North destiné aux workflows agentiques, avec des poids en BF16, FP8 et W4A16.
- 2026-06-30 — Les dépôts du modèle de base North-Mini-Code-1.0 et de sa variante W4A16 ont été enregistrés, confirmant qu'il s'agit de formats d'une même publication et non de deux modèles distincts.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-06-30, vérifiez les pages Hugging Face distinctes de l'artefact de base North-Mini-Code-1.0 et de sa variante w4a16, plutôt que de supposer un paquet de modèle unique et indifférencié.

1. Chargez les poids de base via Transformers, appliquez le modèle de chat intégré aux messages et générez les réponses avec les paramètres d'échantillonnage de la fiche du modèle.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
2. Exécutez le modèle via vLLM et appelez `/v1/chat/completions` pour disposer d'un point d'accès local compatible OpenAI.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
3. Définissez des fonctions avec JSON Schema pour un agent utilisant des outils, transmettez les résultats des outils avec le rôle `tool` et poursuivez la génération.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>

## Bonnes pratiques {#best-practices}

- Réglez `temperature=1.0` et `top_p=0.95`, comme recommandé par Cohere pour la génération.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
- Transmettez le contenu de réflexion entrelacée aux étapes suivantes de l'agent et aux tours de conversation suivants, la fiche du modèle indiquant que cela améliore la qualité des sorties.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
- Vérifiez la compatibilité des versions de vLLM : la fiche du modèle précise vLLM main et `cohere_melody>=0.9.0` pour que les réponses soient analysées correctement.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-30 — Considérer North-Mini-Code-1.0 et North-Mini-Code-1.0-w4a16 comme des publications indépendantes est obsolète : W4A16 est un format de poids de North Mini Code 1.0.

## Points inconnus {#still-unknown}

- Les sources primaires confirment la publication du 2026-06-09, mais n'expliquent pas quelle modification distincte est intervenue le 2026-06-30 ; cette date peut correspondre à l'enregistrement des dépôts ou à la publication des liens plutôt qu'à une nouvelle publication de modèle.
- Le schéma de réponse du système ne comporte pas les champs `event_findings` et `new_events` ; les détails sur les publications antérieures et la clarification des événements figurent dans `what_changed` et `unknowns`.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/CohereLabs/North-Mini-Code-1.0 | CohereLabs/North-Mini-Code-1.0 · Hugging Face | 2026-09-05 |
| https://huggingface.co/CohereLabs/North-Mini-Code-1.0-w4a16 | CohereLabs/North-Mini-Code-1.0-w4a16 · Hugging Face | 2026-09-05 |
| https://cohere.com/blog/north-mini-code | North Mini Code: Agentic Coding for Developers | Cohere | 2026-09-05 |
| https://docs.cohere.com/v2/changelog | Release Notes | Cohere | 2026-09-05 |
| https://github.com/cohere-ai/cohere-developer-experience/blob/main/fern/pages/models/north/north-mini-code-1.0.mdx | north-mini-code-1.0.mdx | Cohere developer experience | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:cohere-north`, fil `north-mini-code`, 1 événement daté du 2026-06-30 au 2026-06-30.
- **Note pratique :** À partir du 2026-06-30, les praticiens qui évaluent North Mini Code doivent vérifier les pages Hugging Face distinctes de l'artefact de base North-Mini-Code-1.0 et de sa variante w4a16, plutôt que de supposer un paquet de modèle unique et indifférencié.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

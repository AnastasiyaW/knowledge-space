---
title: "Tencent Hunyuan — Publications des modèles Hunyuan"
category: projects
date: 2025-07-04
tags: [hunyuan, hunyuan-model-releases, project, tencent-hunyuan, tencent_hunyuan]
aliases: ["Hunyuan-A13B", "Tencent Hunyuan"]
level: 2
source_sha256: 1c002261b69a8bcfced9d5f1c4ded7b39ea6e7aa738ebb1425fed32b4816ee2f
translation: machine
translated_at: '2026-10-24'
---
# Tencent Hunyuan — Publications des modèles Hunyuan {#tencent-hunyuan-hunyuan-model-releases}

**Ligne de développement :** `project:tencent-hunyuan` · fil `hunyuan-model-releases`  
**Dernier événement :** 2025-07-04 · 2 événements datés depuis 2024-07-02 · **Recherche effectuée le :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

Tencent Hunyuan n'est pas un modèle unique et cohérent, mais une marque regroupant plusieurs familles incompatibles entre elles : HunyuanDiT pour la génération d'images et Hunyuan-A13B pour le texte, le raisonnement et l'appel d'outils (tool calling). Hunyuan-A13B : 80 Md de paramètres, 13 Md actifs, contexte de 256K. Conclusion pratique : pour un nouveau projet LLM, on retient A13B et son chemin de serving officiel ; DiT ne se choisit que pour maintenir un pipeline T2I existant.

## Ligne de développement {#development-line}

- **2024-07-02 — Des ressources Tencent Hunyuan liées à HunyuanDiT v1.2 ont été enregistrées.** Le 2024-07-02, l'enregistrement pointait vers la page du modèle HunyuanDiT-v1.2, vers le Space Hunyuan-Captioner et vers le profil Hugging Face de Tencent-Hunyuan. À partir des seuls liens, cela établit un historique daté de ressources publiques autour de HunyuanDiT v1.2 et des outils de légendage, mais ne permet pas de savoir si ces éléments ont été publiés ou mis à jour ce jour-là.
- **2025-07-04 — Des ressources Tencent Hunyuan A13B Instruct ont été enregistrées.** 80 Md de paramètres totaux et 13 Md actifs, modes thinking/no-thinking, contexte de 256K et chemins officiels Transformers, vLLM, SGLang et Docker.

## Ce qui a changé {#what-changed}

2024-07-02 — HunyuanDiT v1.2 était disponible sous forme de paquet de poids et de code pour la génération bilingue text-to-image ; il ne s'agit pas d'un LLM. 2024-07-08 — sortie de HYDiT/HunyuanDiT v1.2 ; le dépôt officiel distingue cette mise à jour des éléments publiés le 2 juillet. 2024-07-15 — ajout de workflows ComfyUI standardisés pour HunyuanDiT 1.1/1.2 et compatibilité avec les LoRA. 2025-06-27 — Tencent a ouvert Hunyuan-A13B-Pretrain, Instruct, Instruct-FP8 et Instruct-GPTQ-Int4 ; il s'agit d'une gamme LLM MoE distincte, et non d'une version suivante du DiT. 2025-07-04 — la pertinence de cette étape est confirmée par la sortie d'A13B : 80 Md de paramètres totaux et 13 Md actifs, modes thinking/no-thinking, contexte de 256K et chemins officiels Transformers, vLLM, SGLang et Docker.

## Comment l'utiliser {#how-to-use-this}

Au 2025-07-04, les praticiens doivent traiter les références publiques datées de Tencent Hunyuan comme des points de contrôle distincts : examiner les ressources HunyuanDiT v1.2/captioning pour la gamme d'images de 2024, et le modèle A13B Instruct ainsi que le dépôt de code pour la gamme de modèles de langage de 2025, plutôt que de supposer qu'il s'agit d'une implémentation unique et interchangeable.

1. Choisissez `tencent/Hunyuan-A13B-Instruct` pour un service de chat, de raisonnement ou d'appel d'outils ; chargez-le via Transformers avec `trust_remote_code=True` et le chat template standard.
  — <https://huggingface.co/tencent/Hunyuan-A13B-Instruct>
2. Pour une API locale compatible OpenAI, lancez A13B avec `vllm serve "tencent/Hunyuan-A13B-Instruct"`.
  — <https://huggingface.co/tencent/Hunyuan-A13B-Instruct>
3. Désactivez le raisonnement via `enable_thinking=False` ou le préfixe `/no_think` lorsque la latence compte davantage qu'un raisonnement détaillé.
  — <https://github.com/Tencent-Hunyuan/Hunyuan-A13B>
4. Pour un pipeline d'images HunyuanDiT existant, utilisez le pipeline Diffusers `Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers` ; une variante distillée est disponible pour une inférence plus rapide.
  — <https://github.com/Tencent-Hunyuan/HunyuanDiT>

## Bonnes pratiques {#best-practices}

- Ne mélangez pas les poids, l'API et les attentes de HunyuanDiT avec ceux d'A13B : il s'agit respectivement d'un transformeur de diffusion T2I et d'un LLM MoE.
  — <https://github.com/Tencent-Hunyuan/HunyuanDiT>
- Pour HunyuanDiT ControlNet, utilisez les poids de base distillés : ce sont eux qui ont servi à entraîner les poids ControlNet publiés.
  — <https://github.com/Tencent-Hunyuan/HunyuanDiT>
- Pour A13B en serving local, utilisez le conteneur officiel ou le backend documenté, et vérifiez le comportement du mode thinking sur vos propres tâches avant de l'intégrer dans un parcours agentique.
  — <https://github.com/Tencent-Hunyuan/Hunyuan-A13B>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- Les deux points datés concernent des modalités différentes : HunyuanDiT relève de la génération d'images, Hunyuan-A13B est un modèle de langage MoE. Rien ne prouve qu'A13B remplace DiT.
- Pour l'événement du 2024-07-02, aucune source primaire indépendante n'a été trouvée datant précisément la sortie de v1.2 au 2 juillet ; le journal officiel indique la sortie de v1.2 au 2024-07-08.
- event_findings: 2025-07-04 — le dépôt officiel date l'ouverture des quatre variantes A13B au 2025-06-27 ; source : https://github.com/Tencent-Hunyuan/Hunyuan-A13B. Nouveaux événements distincts : 2024-07-08 — sortie de HYDiT v1.2 ; 2024-07-15 — workflows ComfyUI et compatibilité LoRA ; source : https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.2.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.2 | Fiche du modèle Tencent-Hunyuan/HunyuanDiT-v1.2 | 2026-09-05 |
| https://github.com/Tencent-Hunyuan/HunyuanDiT | Tencent-Hunyuan/HunyuanDiT | 2026-09-05 |
| https://huggingface.co/tencent/Hunyuan-A13B-Instruct | Fiche du modèle tencent/Hunyuan-A13B-Instruct | 2026-09-05 |
| https://github.com/Tencent-Hunyuan/Hunyuan-A13B | Tencent-Hunyuan/Hunyuan-A13B | 2026-09-05 |
| https://developer.cloud.tencent.com/article/2536652?policyId=1003 | Tencent Hunyuan publie son premier modèle MoE open source à raisonnement hybride, aux performances élevées, avec seulement 13 Md de paramètres activés | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:tencent-hunyuan`, fil `hunyuan-model-releases`, 2 événements datés du 2024-07-02 au 2025-07-04.
- **Remarque pratique :** Au 2025-07-04, les praticiens doivent traiter les références publiques datées de Tencent Hunyuan comme des points de contrôle distincts : examiner les ressources HunyuanDiT v1.2/captioning pour la gamme d'images de 2024, et le modèle A13B Instruct ainsi que le dépôt de code pour la gamme de modèles de langage de 2025, plutôt que de supposer qu'il s'agit d'une implémentation unique et interchangeable.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

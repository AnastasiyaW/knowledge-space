---
title: "Huihui-Qwen3.8-27B-abliterated — Disponibilité publique du modèle"
category: projects
date: 2026-08-17
tags: [huihui-ai/huihui-qwen3.8-27b-abliterated, huihui-qwen3-8-27b-abliterated, project, public-model-availability]
aliases: ["Huihui-Qwen3.8-27B-abliterated"]
level: 2
source_sha256: 2330aa43f3e8ed29cb0650b16081ff13298e00d2ab6da0445e79bd2cc204f635
translation: machine
translated_at: '2026-10-24'
---
# Huihui-Qwen3.8-27B-abliterated — Disponibilité publique du modèle {#huihui-qwen38-27b-abliterated-public-model-availability}

**Ligne de développement :** `project:huihui-qwen3-8-27b-abliterated` · fil `public-model-availability`  
**Dernier événement :** 2026-08-17 · 1 événement daté depuis le 2026-08-17 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

Huihui-Qwen3.8-27B-abliterated est une variante abliterated du modèle de base Qwen3.8-27B, destinée aux développeurs qui ont besoin d'un checkpoint multimodal ouvert compatible avec Transformers, vLLM ou SGLang.

- Chat pour la génération de texte conversationnelle.
- Traitement d'images pour les entrées visuelles.
- Service compatible OpenAI pour les appels d'API distants.

Le filtrage de sécurité est nettement réduit, et la fiche du modèle recommande des environnements de recherche et contrôlés. Ce modèle ne remplace pas un modèle de production sûr.

## Ligne de développement {#development-line}

- **2026-08-17 — Huihui-Qwen3.8-27B-abliterated est devenu publiquement disponible sur Hugging Face.** L'artefact contient 18 fichiers safetensors et occupe 55,6 GB ; le README précise que le MTP et le composant de vision restent non modifiés.

## Ce qui a changé {#what-changed}

2026-08-17 — la révision vérifiée d42ca89 est épinglée : l'artefact contient 18 fichiers safetensors et occupe 55,6 GB ; le README précise que le MTP et le composant de vision restent non modifiés.

La fiche du modèle indique que l'ablation ne s'applique qu'aux couches 18 à 51, afin de préserver l'essentiel des performances d'origine. Nous pouvons épingler la version précédente à la révision d42ca89.

## Comment l'utiliser {#how-to-use-this}

Depuis le 2026-08-17, nous pouvons considérer Huihui-Qwen3.8-27B-abliterated comme une lignée de modèles publiquement accessible et évaluer l'artefact de modèle lié, les variantes quantifiées associées et le ZeroGPU Space ; les liens datés seuls ne permettent pas de choisir une variante précise ni de se fier à des affirmations de performance.

1. Pour des exécutions multimodales en local, charger AutoProcessor et AutoModelForMultimodalLM, formater les messages avec du texte et des images via le chat template, puis appeler generate.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
2. Pour un point de terminaison compatible OpenAI, installer vLLM, exécuter `vllm serve "huihui-ai/Huihui-Qwen3.8-27B-abliterated"`, puis envoyer les requêtes à `/v1/chat/completions`.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
3. Pour SGLang, exécuter `python3 -m sglang.launch_server --model-path "huihui-ai/Huihui-Qwen3.8-27B-abliterated"`, puis utiliser le point de terminaison sur le port choisi.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>

## Bonnes pratiques {#best-practices}

- Épingler la révision pour des exécutions reproductibles : la fiche du modèle renvoie directement à d42ca89 pour la version antérieure.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
- Conserver une relecture manuelle des sorties et éviter d'utiliser le checkpoint directement dans des produits publics ou à haut risque : l'auteur signale un filtrage de sécurité réduit.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
- Pour llama.cpp, Ollama ou LM Studio, choisir des quantifications dérivées distinctes plutôt que de considérer le dépôt BF16 comme prêt pour ces runtimes.
  — <https://huggingface.co/models?other=base_model%3Aquantized%3Ahuihui-ai%2FHuihui-Qwen3.8-27B-abliterated>

## Remplacé par ce qui suit {#superseded-by-this}

- Après le 2026-08-17, décrire la révision épinglée d42ca89 comme ne comportant que le MTP non modifié est devenu obsolète : son README précise que le composant de vision est également non modifié.

## Toujours inconnu {#still-unknown}

- Dans l'historique principal disponible, l'horodatage calendaire exact du commit d42ca89 est relatif (« il y a 19 jours ») ; il correspond au 2026-08-17 à la date de vérification, mais la source primaire ne fournit aucun horodatage ISO.
- On ignore encore si le ZeroGPU Space issu de l'événement est une voie de lancement officielle ou correspond à la même révision du modèle.
- La date de la modification ultérieure de l'ablation sur les couches 18 à 51 n'apparaît pas dans les résultats primaires disponibles ; nous ne la listons donc pas comme événement daté distinct.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated | huihui-ai/Huihui-Qwen3.8-27B-abliterated — fiche du modèle Hugging Face | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated/commit/d42ca8978c5a66e92c3446d46e8adfe03ef692ff | Update README.md · huihui-ai/Huihui-Qwen3.8-27B-abliterated à d42ca89 | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated/tree/d42ca8978c5a66e92c3446d46e8adfe03ef692ff | huihui-ai/Huihui-Qwen3.8-27B-abliterated à d42ca89 | 2026-09-05 |
| https://huggingface.co/models?other=base_model%3Aquantized%3Ahuihui-ai%2FHuihui-Qwen3.8-27B-abliterated | Quantized Models for huihui-ai/Huihui-Qwen3.8-27B-abliterated | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.8-27B | Qwen/Qwen3.8-27B — fiche du modèle Hugging Face | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:huihui-qwen3-8-27b-abliterated`, fil `public-model-availability`, 1 événement daté, du 2026-08-17 au 2026-08-17.
- **Note pratique :** Depuis le 2026-08-17, les praticiens peuvent considérer Huihui-Qwen3.8-27B-abliterated comme une lignée de modèles publiquement repérable et évaluer l'artefact de modèle lié, les variantes quantifiées associées et le ZeroGPU Space ; les liens datés seuls ne permettent pas de choisir une variante précise ni de se fier à des affirmations de performance.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.

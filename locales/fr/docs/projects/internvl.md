---
title: "InternVL"
category: projects
tags: [internvl, internvl-model-releases, project]
aliases: ["InternVL", "InternVL 3.5"]
level: 3
source_sha256: c55b2648454f66ea8b76ef412c2b2322d36f4952143f156edd5b20ebe18577e4
translation: machine
translated_at: '2026-10-24'
---
# InternVL {#internvl}

**Ligne de développement :** `project:internvl` · fil `internvl-model-releases`  
**Événements :** 2 datés, 2024-12-11 → 2025-08-27 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Qu'est-ce que c'est {#what-it-is}

InternVL est une famille de modèles vision-langage à poids ouverts destinée aux équipes qui doivent analyser des images, des documents, plusieurs images, des vidéos et des états d'interface graphique dans un workflow auto-hébergé.

- Questions-réponses sur images, documents, graphiques et OCR
- Conversation multi-images et vidéo
- Ancrage visuel (visual grounding), travaux vision-langage multilingues, ainsi que tâches GUI et embodied dans la version 3.5

La gamme actuelle 3.5 couvre de 1,1 B à 240,7 B de paramètres au total ; le guide officiel indique que les modèles jusqu'à 30 B tiennent sur un A100, 38 B sur deux, et 241 B sur huit. Pour tout nouveau travail en local, choisissez un checkpoint 3.5 complet sans suffixe ; utilisez Flash lorsque le coût en tokens visuels est le facteur limitant.

## Ligne de développement {#development-line}

- **2024-12-11 — Sortie du modèle InternVL2.5-78B et de sa collection.** Le 2024-12-11, le projet a publié InternVL2.5-78B avec une collection de modèles, le dépôt, le site du projet et une démo. Les sources liées n'établissent ni résultats de benchmarks ni détails fonctionnels.
- **2025-08-27 — Sortie de l'article InternVL3.5 et de sa collection de modèles.** Le 2025-08-27, le projet a publié l'article InternVL3.5, la collection officielle, le dépôt et le chat. Les sources liées n'établissent pas les affirmations détaillées de l'article, les variantes prises en charge ni les recommandations de déploiement.

## Ce qui a changé {#what-changed}

Le 2024-12-05 (enregistré le 2024-12-11), InternVL2.5 est devenu une famille allant de 1B à 78B. Elle a conservé l'architecture de base précédente tout en révisant l'entraînement, le passage à l'échelle au moment du test (test-time scaling) et le travail sur la qualité des données. Le checkpoint 78B associait un encodeur visuel de 6B à Qwen2.5-72B.

Le 2025-08-26 (enregistré le 2025-08-27), InternVL3.5 a remplacé cette ligne de base par des checkpoints de 1B à 241B, dans le format natif du projet comme dans le format Hugging Face standard. Il a introduit CascadeRL, le Visual Resolution Router, un déploiement vision-langage découplé, des backbones linguistiques Qwen3/GPT-OSS, ainsi que des capacités GUI et embodied.

Le 2025-08-30, le projet a publié le code d'entraînement CascadeRL et les données pour sa variante GPT-OSS 20B-A4B. Après le 2025-08-27, un checkpoint officiel InternVL3.5-Flash est devenu disponible. Sa fiche documente ViCO et le routage de résolution visuelle, qui réduisent de 50 % les tokens visuels ; les sources examinées n'ont pas permis d'établir sa date exacte de première publication.

## Comment l'utiliser {#how-to-use-this}

Le 2024-12-11, évaluez la page du modèle InternVL2.5-78B et la collection officielles lorsque vous sélectionnez une version InternVL2.5. Au 2025-08-27, examinez l'article InternVL3.5 lié et la collection officielle avant de choisir une ligne InternVL plus récente, plutôt que de supposer que la ligne précédente reste la valeur par défaut.

1. Choisissez un checkpoint InternVL3.5 complet sans suffixe pour l'inférence courante ; choisissez la variante Flash lorsque le coût en tokens visuels compte.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Flash>
2. Utilisez le format en connaissance de cause : le checkpoint au format natif du projet se charge via AutoModel avec du code distant, tandis que le format HF suit les conventions standard de Transformers. Installez transformers >=4.52.1 ; la variante 20B-A4B nécessite >=4.55.0.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
3. Pour le chat sur images, appliquez le prétraitement de découpage dynamique en tuiles de 448 px fourni, convertissez les tuiles en bf16, et envoyez le prompt avec un placeholder <image> via model.chat.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
4. Pour la vidéo, échantillonnez un nombre borné d'images, préfixez chacune avec FrameN: <image>, et transmettez le num_patches_list correspondant à l'appel de chat.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
5. Pour un service, déployez via LMDeploy ou vLLM avec un point d'accès compatible OpenAI ; utilisez vLLM pour la variante GPT-OSS 20B-A4B.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>

## Bonnes pratiques {#best-practices}

- Pour le déploiement, privilégiez le checkpoint sans suffixe : c'est la version qui a suivi le pipeline complet, contrairement aux checkpoints des étapes Pretrained, Instruct et MPO.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Flash>
- Dimensionnez le modèle à partir de l'enveloppe GPU documentée avant tout téléchargement : jusqu'à 30 B sur un A100, 38 B sur deux, et 241 B sur huit.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
- Respectez la version minimale de Transformers documentée ; le minimum de dépendances de l'ère 2.5 ne suffit pas pour 3.5.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
- Pour le mode de raisonnement (thinking), réglez do_sample=true et temperature=0.6 ; le projet recommande ce réglage pour limiter les répétitions.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
- Augmentez la fenêtre de contexte pour les prompts multi-images et numérotez les images dans le prompt afin que le modèle puisse les distinguer.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>

## Remplacé par ceci {#superseded-by-this}

- 2024-12-05 / 2024-12-11 : InternVL2.5 n'est plus la valeur par défaut pour un nouveau déploiement InternVL de base ; utilisez un checkpoint InternVL3.5 complet sans suffixe, sauf si la compatibilité avec l'existant est la contrainte déterminante.
- Les recommandations transformers>=4.37.2 d'InternVL2.5 sont obsolètes pour InternVL3.5 : utilisez transformers>=4.52.1, ou >=4.55.0 pour 20B-A4B.
- 2025-08-26 : la mention de la fiche 3.5 selon laquelle Flash était encore à venir est obsolète ; un checkpoint officiel InternVL3_5-8B-Flash est désormais disponible.

## Encore inconnu {#still-unknown}

- La date exacte de première publication d'InternVL3.5-Flash n'a pas pu être établie ; sa disponibilité actuelle est confirmée, mais la date de mise à jour d'une page de modèle n'est pas forcément une date de lancement.
- Les gains de raisonnement et la réduction de tokens annoncés sont des résultats de benchmarks rapportés par le projet, et non une évaluation indépendante pour une charge de travail particulière.
- L'interface de chat publique était accessible mais n'a pas exposé de réponse inspectable pour le fetcher ; le comportement de la démo hébergée n'a donc pas été vérifié.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://github.com/OpenGVLab/InternVL | OpenGVLab/InternVL | 2026-09-04 |
| https://internvl.github.io/blog/2024-12-05-InternVL-2.5/ | InternVL2.5 | 2026-09-04 |
| https://huggingface.co/OpenGVLab/InternVL2_5-78B | OpenGVLab/InternVL2_5-78B | 2026-09-04 |
| https://internvl.github.io/blog/2025-08-26-InternVL-3.5/ | InternVL3.5 | 2026-09-04 |
| https://huggingface.co/papers/2508.18265 | InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency | 2026-09-04 |
| https://huggingface.co/collections/OpenGVLab/internvl35-68ac87bd52ebe953485927fb | InternVL3.5 — OpenGVLab Collection | 2026-09-04 |
| https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct | OpenGVLab/InternVL3_5-8B-Instruct | 2026-09-04 |
| https://huggingface.co/OpenGVLab/InternVL3_5-8B-Flash | OpenGVLab/InternVL3_5-8B-Flash | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:internvl`, fil `internvl-model-releases`, 2 événements datés du 2024-12-11 au 2025-08-27.
- **Note pratique :** Au 2024-12-11, les praticiens doivent évaluer la page du modèle InternVL2.5-78B et la collection officielle lorsqu'ils sélectionnent une version InternVL2.5. Au 2025-08-27, ils doivent examiner l'article InternVL3.5 lié et la collection officielle avant de choisir une ligne InternVL plus récente, plutôt que de supposer que la ligne de modèles précédente reste la valeur par défaut appropriée.
- **Confiance :** élevée. Les mentions datées de remplacement ci-dessus font foi pour ce qui est obsolète.

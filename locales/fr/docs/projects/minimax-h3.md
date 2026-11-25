---
title: "MiniMax H3"
category: projects
date: 2026-07-31
tags: [minimax, minimax-h3, project]
aliases: ["MiniMax H3"]
level: 3
source_sha256: d0bfb5f318edcffa9e5e9d6d56fff7653ccf6defeac5a94ebb68563b8f57cdde
translation: machine
translated_at: '2026-10-24'
---
# MiniMax H3 {#minimax-h3}

**Ligne de développement :** `project:minimax-h3` · fil `minimax-h3`  
**Dernier événement :** 2026-07-31 · 1 événement daté depuis le 2026-07-31 · **Consulté le :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

MiniMax H3 est un modèle de base audiovisuel open-weight de 33B pour la génération vidéo, destiné aux créateurs et aux développeurs qui choisissent une génération locale en 768p ou un flux de travail 2K via API.

- Entrées : texte, première/dernière image, ou références d'image, de vidéo et d'audio.
- Sortie : vidéo synchronisée avec audio stéréo natif ; FL2VA couvre le travail texte/images-clés et Ref2VA couvre le travail multimodal par références.
- Limite : 4 à 15 secondes ; Context-IR et H3-Regenerate-2K restent hébergés dans le flux de travail 2K complet officiel.

## Ligne de développement {#development-line}

- **2026-07-31 — MiniMax publie une entrée de blog officielle sur MiniMax H3.** MiniMax a lancé H3 avec un contexte multimodal et une vidéo à audio stéréo natif allant jusqu'à 2K/15 secondes ; les poids devaient être publiés ultérieurement.

## Évolutions {#what-changed}

- 2026-07-31 : MiniMax lance H3 avec un contexte multimodal et une vidéo à audio stéréo natif allant jusqu'à 2K/15 secondes ; les poids devaient être publiés ultérieurement.
- 2026-08-03 : MiniMax ouvre les poids de H3 Base, avec les points de contrôle FL2VA et Ref2VA, tandis que Context-IR et la régénération 2K restent dans le pipeline hébergé.
- 2026-08-10 : Un AMA lié a précisé les recommandations sur les prompts et le flux de travail ainsi que les projets de publication locale ; il ne s'agissait pas d'une nouvelle version du modèle.
- 2026-08-27 : fal publie H3 Max, un dérivé post-entraîné de MiniMax H3 proposé via fal.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-31, commencez par la page officielle de MiniMax H3 pour évaluer le projet. Ne déduisez pas les fonctionnalités ni la disponibilité au déploiement à partir des seuls premiers documents.

1. Pour la voie hébergée, créez une clé API et envoyez une requête POST en `application/json` avec une authentification Bearer vers le point de terminaison de génération vidéo H3.
  — <https://platform.minimax.io/docs/api-reference/video-generation-v2-create>
2. Choisissez MiniMax-H3, incluez un élément de texte non vide, puis ajoutez soit la première/dernière image, soit des références d'image, de vidéo et d'audio ; les deux modes d'entrée ne peuvent pas être combinés dans une même requête.
  — <https://platform.minimax.io/docs/api-reference/video-generation-v2-create>
3. Réglez la résolution de H3 sur 768P ou 2K et la durée entre 4 et 15 secondes, puis interrogez la tâche ou enregistrez un rappel (callback) pour les états queued, running, succeeded, failed ou cancelled.
  — <https://platform.minimax.io/docs/api-reference/video-generation-v2-create>
4. Pour le 768p local, téléchargez FL2VA pour le travail texte/première-dernière image ou Ref2VA pour le travail multimodal par références, puis servez le point de contrôle H3-Base correspondant avec un framework pris en charge.
  — <https://www.minimax.io/news/minimax-h3-open-source>
5. Pour un dérivé hébergé post-entraîné plutôt que la base ouverte, utilisez H3 Max de fal via son Playground ou son API.
  — <https://blog.fal.ai/introducing-h3-max-by-fal/>

## Bonnes pratiques {#best-practices}

- Utilisez Context-IR comme étape de planification ou de prétraitement, ou reproduisez sa structure à partir des recommandations de prompts du fournisseur, avant d'envoyer le travail à H3 Base.
  — <https://www.minimax.io/news/minimax-h3-open-source>
- Pour le travail première/dernière image, suivez l'instruction d'alignement des images du guide Base et décrivez un trajet continu vers l'image finale ; gardez les instants de coupure des plans suivants strictement croissants.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md>
- Pour une référence complète, définissez une fois chaque étiquette Subject, Picture, Video et Audio et conservez son sens ; indiquez si l'audio est copié ou seulement référencé.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md>
- Considérez la sortie locale de H3 Base comme du 768p ; utilisez le flux de travail 2K complet déclaré plutôt que de supposer que Context-IR ou H3-Regenerate-2K sont livrés avec les poids.
  — <https://www.minimax.io/news/minimax-h3-open-source>
- Examinez la licence Community avant tout déploiement commercial ou hébergé : elle exclut plusieurs territoires et exige une autorisation distincte au-delà de 20 millions de dollars US de chiffre d'affaires annuel.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-03 : l'état du 2026-07-31, dans lequel les poids de MiniMax H3 n'étaient prévus que pour publication dans les jours suivants.

## Points encore inconnus {#still-unknown}

- Si MiniMax-H3-Max sur l'API MiniMax et H3 Max sur fal partagent le même point de contrôle.
- Si MiniMax a publié H3-Context-IR, H3-Regenerate-2K ou leur implémentation d'attention parcimonieuse pour un usage local.
- Les exigences minimales en GPU ou en VRAM pour un service local ; la commande SGLang est un exemple avec quatre GPU, et non une spécification minimale.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://www.minimax.io/blog/minimax-h3 | MiniMax H3: An Open Model Breaking the Boundaries Between Tasks and Modalities - MiniMax Research | MiniMax | 2026-09-04 |
| https://www.minimax.io/news/minimax-h3-open-source | Open General Intelligence: MiniMax H3 Is Now Open Source - MiniMax News | MiniMax | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/1vh9rtw/ama_minimax_h3_team_ask_us_anything_about_our/ | AMA: MiniMax H3 Team — Ask us anything about our open video generation model, training, and future plans : r/StableDiffusion | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/video-generation-v2-create | Create Video Generation Task - MiniMax API Docs | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md | docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md · MiniMaxAI/MiniMax-H3 at main | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md | docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md · MiniMaxAI/MiniMax-H3 at main | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE | LICENSE · MiniMaxAI/MiniMax-H3 at main | 2026-09-04 |
| https://blog.fal.ai/introducing-h3-max-by-fal/ | Introducing H3 Max by fal | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:minimax-h3`, fil `minimax-h3`, 1 événement daté du 2026-07-31 au 2026-07-31.
- **Remarque pratique :** À partir du 2026-07-31, commencez par la page officielle de MiniMax H3 pour évaluer le projet. Ne déduisez pas les fonctionnalités ni la disponibilité au déploiement à partir des seuls premiers documents.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

<!-- live-update:d336eed43fa2789e79635be365c8a2a0bb09b0d8651d55809dfa1659a5457423 -->
## 2026-09-05 — MiniMax H3 Semantic Bridge ajoute un adaptateur pour la voie texte FL2VA de H3 {#2026-09-05-minimax-h3-semantic-bridge-adds-an-adapter-for-h3s-fl2va-text-path}

MiniMax H3 Semantic Bridge est un adaptateur de conditionnement pour ComfyUI, destiné au flux de travail standard MiniMax H3 FL2VA conditionné par texte. Il s'agit d'un projet communautaire, et non d'une publication officielle de MiniMax ou de SenseNova. La prise en charge de Ref2VA n'a pas été publiée, car les tests de l'auteur ont montré une dégradation du chant et de la synchronisation labiale.

### Utilisation et bonnes pratiques {#usage-and-practices}

- Installez l'archive de nœud personnalisé publiée dans ComfyUI/custom_nodes/. Placez MiniMaxH3_SemanticBridge_v1.safetensors dans ComfyUI/models/semantic_bridge/, redémarrez ComfyUI, puis partez du flux de travail fourni en référence. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)
- Utilisez v1 uniquement avec la voie standard MiniMax H3 FL2VA/conditionnée par texte. Ne l'intégrez pas à Ref2VA ni à un autre flux de travail conditionné par référence. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)
- Commencez avec un alpha de 0,10 et une correspondance de magnitude par jeton. Comparez la sortie H3 native et celle avec le pont activé, avec le même prompt, la même graine et les mêmes paramètres de génération. Considérez les comparaisons publiées pour alpha 0,15 comme des exemples et non comme un réglage universel. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)
- Gardez séparées les mesures de similarité cosinus dans l'espace de représentation publiées par l'auteur et les affirmations sur la qualité vidéo. La publication indique qu'elles mesurent l'accord avec une représentation dérivée d'un modèle enseignant, et non la qualité perceptuelle ni une amélioration générale de l'adhérence au prompt. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)

### Preuves complémentaires {#additional-evidence}

- 2026-09-05 : Le dépôt public est speach1sdef178/MiniMax-H3-Semantic-Bridge à la révision 8c2d9b0edb844d6002864a9addd61458dbe81c22. Les fichiers publics comprennent l'adaptateur v1, l'archive du nœud personnalisé, des exemples de flux de travail, les sommes de contrôle, le README, le matériel de recherche, le NOTICE et les licences. Il s'agit d'un projet communautaire, et non d'une publication officielle de MiniMax ou de SenseNova. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/tree/8c2d9b0edb844d6002864a9addd61458dbe81c22)
- 2026-09-05 : L'auteur indique que v1 ne concerne que la voie standard MiniMax H3 FL2VA/conditionnée par texte. Les expériences Ref2VA/audio de référence ont dégradé le chant et la synchronisation labiale, si bien qu'aucun nœud Ref2VA n'a été publié. Alpha 0,10 est le point de départ indiqué par l'auteur. Les exemples A/B pour alpha 0,15 sont des illustrations qualitatives, et non une preuve de gains généraux. [Source](https://www.reddit.com/r/StableDiffusion/comments/1w7wtco/i_tried_transferring_semantic_representations/)

### Limites et questions ouvertes {#limits-and-open-questions}

- Aucune reproduction indépendante, aucun benchmark standardisé de préférence humaine ni aucune validation de performance tierce distincte n'a été trouvé pour cet adaptateur précis à la date du 2026-09-05.
- Le nombre de paramètres (5 à 6 M), les métriques de représentation, la répartition d'entraînement et les affirmations de compatibilité sont des affirmations de publication de l'auteur, non auditées ici de manière indépendante.
- Les requêtes en chinois n'ont trouvé ni annonce exacte en zh-CN, ni tutoriel, ni reproduction indépendante pour MiniMax H3 Semantic Bridge. Le résultat examiné de MiniMaxH3 CondBridge Qwen3.5-4B concerne un projet différent et ne doit pas être fusionné avec cet événement.
- Nous n'avons ni téléchargé ni exécuté le paquet. La compatibilité à l'exécution, l'intégrité des artefacts au-delà de la révision nommée, l'interprétation de la licence et les gains vidéo réels restent non vérifiés.

<!-- Retained base: 10a35259638c923851e915e3b979bbd355ddaf2b; article blob: 3d4f380ad8d34d47f874ef8a5bfdcd7a04126e47 -->

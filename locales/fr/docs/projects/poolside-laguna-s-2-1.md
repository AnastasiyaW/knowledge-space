---
title: "Laguna S 2.1 — Laguna"
category: projects
date: 2026-07-22
tags: [laguna, poolside-laguna-s-2-1, project]
aliases: ["Laguna S 2.1"]
level: 4
source_sha256: 3939d2a9f90a005b9210e3c6767340f205c4c6a78a2870ee395627599dca232f
translation: machine
translated_at: '2026-10-24'
---
# Laguna S 2.1 — Laguna {#laguna-s-21-laguna}

**Ligne de développement :** `project:poolside-laguna-s-2-1` · fil `laguna`  
**Dernier événement :** 2026-07-22 · 1 daté depuis le 2026-07-22 · **Recherché le :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

Laguna S 2.1 est le modèle de codage Mixture-of-Experts à poids ouverts et de type texte-vers-texte de Poolside, destiné aux équipes qui développent des agents logiciels à long horizon.

- 118 B de paramètres au total, environ 8 B actifs par jeton
- Fenêtre de contexte de 1 048 576 jetons, raisonnement et utilisation d'outils entrelacés
- Poids sur Hugging Face, ainsi que des chemins de service hébergés et locaux

Le point de contrôle BF16 nécessite environ 236 Go de poids et plusieurs GPU ; les artefacts quantifiés modifient le compromis matériel. Nous l'utilisons là où comptent le long contexte, la gestion des appels d'outils et l'auto-hébergement, mais nous validons le harnais et le point de contrôle exact avant toute mise en production.

## Ligne de développement {#development-line}

- **2026-07-22 — Poolside a présenté Laguna S 2.1.** Le 2026-07-22, Poolside a présenté Laguna S 2.1 comme une nouvelle étape de la ligne de développement Laguna. Les liens datés associent cette version à une annonce, à une page de distribution du modèle, à des références de modèles quantifiés et aux voies d'accès listées pour le chat et les fournisseurs. Cela importe, car cela identifie une version nommée et distincte du projet.

## Ce qui a changé {#what-changed}

- **2026-07-21** — Laguna S 2.1 a été lancé comme un MoE de 118 B au total et 8 B actifs, avec une fenêtre de contexte de 1 M de jetons et des poids ouverts.
- **2026-07-22** — Un commit de la variante FP8 a documenté une configuration spinquantless 256K présentée comme corrigeant les boucles agentiques ; un second commit a rétabli le raisonnement par défaut et conservé le raisonnement.
- **2026-07-28** — Poolside Desktop Assistant a commencé à associer par défaut pool à Laguna S 2.1 ; il s'agit d'une intégration, et non d'un point de contrôle de modèle.
- **2026-08-01** — FP8 RC2 a été promue sur main avec une configuration 1M et une note sur le nouveau point de contrôle.
- **2026-08-02** — La version hybride INT4/BF16 a été promue sur main avec une configuration 1M et une note sur le nouveau point de contrôle.

## Comment l'utiliser {#how-to-use-this}

1. Pour un essai sans code, ouvrez Poolside Chat, vérifiez qu'il affiche Laguna S 2.1 et envoyez une tâche de codage bornée. Utilisez l'inscription ou la connexion proposée uniquement si elle est nécessaire. Ne soumettez pas de contenu que vous ne pouvez pas autoriser à servir à l'amélioration du modèle.
  — <https://chat.poolside.ai/>
2. Pour une voie hébergée, sélectionnez l'identifiant de modèle OpenRouter poolside/laguna-s-2.1. Il accepte tools et tool_choice, mais n'impose pas response_format JSON ; validez donc la sortie structurée côté client.
  — <https://openrouter.ai/poolside/laguna-s-2.1>
3. Pour un auto-hébergement standard, utilisez la recette vLLM officielle pour poolside/Laguna-S-2.1 avec le parallélisme de tenseurs, les analyseurs poolside_v1 pour les outils et le raisonnement, le choix automatique des outils et le mode réflexion activé ; appelez ensuite son point de terminaison de chat compatible OpenAI.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
4. Pour une voie locale à moindre mémoire, utilisez la commande Ollama officielle ollama run laguna-s-2.1 et choisissez une étiquette de quantification publiée, comme q4_K_M ou q8_0, adaptée à la machine disponible.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
5. Sur macOS, installez Poolside Desktop Assistant si vous souhaitez un espace de travail multi-agents basé sur pool ; son association par défaut est pool avec Laguna S 2.1.
  — <https://poolside.ai/blog/introducing-poolside-desktop-assistant>

## Bonnes pratiques {#best-practices}

- Pour le codage agentique, gardez enable_thinking activé et conservez reasoning_content à travers les tours assistant et outil ; abandonner le raisonnement antérieur peut interrompre le raisonnement ultérieur.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
- Utilisez les analyseurs Laguna d'outils et de raisonnement de l'intégration de service plutôt que les valeurs par défaut génériques. Les noms des options vLLM et TRT-LLM diffèrent : recopiez exactement la recette du moteur choisi.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
- Sur le point de contrôle FP8 actuel, conservez les valeurs par défaut de generation_config, dont top_k 20, plutôt que de définir séparément temperature ou top_p. Sa fiche avertit aussi que la qualité peut se dégrader sur long contexte.
  — <https://huggingface.co/poolside/Laguna-S-2.1-FP8>
- Considérez la configuration communautaire avec déport mixte sur une 2080 Ti de 22 Go et DFlash comme un seul banc d'essai ; mesurez ensuite la longueur de contexte et le débit sur le matériel cible avant d'adopter ses réglages.
  — <https://ai-muninn.com/zh-TW/blog/laguna-118b-moe-on-one-2080ti>

## Remplacé par ceci {#superseded-by-this}

- Les copies antérieures du dépôt poolside/Laguna-S-2.1-FP8, antérieures à l'artefact FP8 actuel. Obsolètes depuis le 2026-08-01 ; la fiche d'août indique que le remplacement est un nouveau point de contrôle aux poids modifiés.
- Les copies antérieures du dépôt poolside/Laguna-S-2.1-INT4, antérieures à l'artefact INT4 actuel. Obsolètes depuis le 2026-08-02 ; la fiche d'août indique que le remplacement est un nouveau point de contrôle aux poids modifiés.

## Toujours inconnu {#still-unknown}

- L'événement source conservé est daté du 2026-07-22, alors que Poolside date le lancement du modèle de base au 2026-07-21. Sans le texte source privé, nous ne pouvons pas établir si l'enregistrement source était un billet de publication tardif ou un autre élément portant sur le même sujet.
- Aucune documentation de publication ou d'exploitation en chinois simplifié émanant de Poolside n'a été trouvée lors de ce passage. La source chinoise datée utilisée ici est une ressource communautaire en chinois traditionnel et ne remplace pas une voie zh-CN.
- Aucune source datée de première main trouvée lors de ce passage n'indique que le dépôt de base poolside/Laguna-S-2.1, et non ses variantes FP8 et INT4, a été remplacé après le lancement du 21 juillet.
- Les chiffres de benchmark de Poolside sont des résultats déclarés selon les harnais et conditions de test indiqués ; ils ne constituent pas une preuve indépendante de performance en production.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://poolside.ai/blog/introducing-laguna-s-2-1 | Introducing Laguna S 2.1 - Poolside | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1 | poolside/Laguna-S-2.1 - fiche de modèle Hugging Face | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-FP8/commits/main | Commits - poolside/Laguna-S-2.1-FP8 | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-FP8 | poolside/Laguna-S-2.1-FP8 - fiche de modèle Hugging Face | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-INT4/commits/main | Commits - poolside/Laguna-S-2.1-INT4 | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-INT4 | poolside/Laguna-S-2.1-INT4 - fiche de modèle Hugging Face | 2026-09-06 |
| https://poolside.ai/blog/introducing-poolside-desktop-assistant | Introducing Poolside Desktop Assistant, for macOS - Poolside | 2026-09-06 |
| https://openrouter.ai/poolside/laguna-s-2.1 | Laguna S 2.1 - API Pricing & Providers - OpenRouter | 2026-09-06 |
| https://chat.poolside.ai/ | Poolside Chat | 2026-09-06 |
| https://ai-muninn.com/zh-TW/blog/laguna-118b-moe-on-one-2080ti | [洋垃圾跑大模型 #2] 一張 22G 老卡跑 118B 的 coding 大模型:Poolside Laguna S 2.1 實戰 | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:poolside-laguna-s-2-1`, fil `laguna`, 1 événement daté du 2026-07-22 au 2026-07-22.
- **Note pratique :** Voir les sections d'usage et de pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

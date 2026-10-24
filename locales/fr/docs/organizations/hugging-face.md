---
title: "Hugging Face"
category: organizations
date: 2025-02-03
tags: [dreambooth-hackathon, hf-inference-providers, hugging-face, hugging-face-mcp, hugging-face-platform-evolution, huggingface-local-apps, organization]
aliases: ["Hugging Face"]
level: 3
source_sha256: 74a2012891ccb9a486731a5e3d1bfb98e702762311b1a0513b0caeb956f3a7ea
translation: machine
translated_at: '2026-10-24'
---
# Hugging Face {#hugging-face}

**Ligne de développement :** `organization:hugging-face` · fil `hugging-face-platform-evolution`  
**Dernier événement :** 2025-02-03 · 4 événements datés depuis 2022-12-28 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Hugging Face est une plateforme ML de type GitHub destinée aux équipes qui publient, évaluent, exécutent ou connectent des modèles, des jeux de données et des applications d'IA.

- Dépôts du Hub pour les modèles, les jeux de données et les Spaces.
- Inference Providers pour des modèles compatibles en mode serverless, via une API unique.
- Accès MCP à la recherche sur le Hub, à la documentation, à certains Spaces, aux Jobs et aux Sandboxes.

## Ligne de développement {#development-line}

- **2022-12-28 — Hugging Face publie des ressources pour un hackathon DreamBooth.** Hugging Face a publié une page du DreamBooth Hackathon et un notebook Colab pour les workflows de diffusion.
- **2024-05-24 — Hugging Face ajoute une voie de produit Local Apps.** Hugging Face a publié le code de tâche Local Apps et une page de paramètres pour prendre en charge les workflows d'applications locales.
- **2024-06-05 — Hugging Face publie une divulgation concernant les secrets des Spaces.** Hugging Face a divulgué des secrets dans des Spaces, faisant de la sécurité des identifiants dans les Spaces une préoccupation publique pour les mainteneurs et les utilisateurs.
- **2025-02-03 — Hugging Face annonce Inference Providers.** Hugging Face a annoncé Inference Providers comme voie de plateforme pour accéder à l'inférence via des fournisseurs intégrés.

## Évolutions {#what-changed}

Hugging Face est passé de la collaboration hébergée autour de modèles à une plateforme proposant des chemins d'exécution locaux, routés et destinés aux agents.

- 2022-12-28 — Le DreamBooth Hackathon a offert un notebook pour personnaliser Stable Diffusion à partir de quelques images et publier des modèles sur le Hub. Le concours s'est terminé en janvier 2023.
- 2024-05-24 — Local Apps a ajouté aux pages de modèles des extraits d'exécution locale. La source mutable liée couvre llama.cpp, vLLM, SGLang et MLX, mais l'implémentation de mai 2024 n'est pas épinglée.
- 2024-06-05 — Suite à la divulgation du 31 mai concernant les secrets des Spaces, Hugging Face a révoqué les jetons concernés, retiré les jetons d'organisation des Spaces, ajouté des secrets adossés à KMS et migré les utilisateurs vers des jetons à granularité fine.
- 2025-02-03 — Consigné peu après le lancement du 28 janvier, Inference Providers a fait passer l'usage serverless d'un point d'accès unique du Hub à une API routée par fournisseur, avec des pages de modèles compatibles, la prise en charge des SDK, des clés de fournisseur personnelles et une facturation routée par Hugging Face.
- 2025-06-07 — En lien avec le lancement officiel du serveur MCP le 6 juin, les assistants compatibles MCP ont pu rechercher des ressources du Hub et appeler certaines applications Gradio. Le lancement était expérimental.
- 2026-07-22 (trouvé aujourd'hui) — MCP a ajouté l'outil de navigation hf_fs pour les dépôts, le stockage, la documentation et les articles, ainsi que des Sandboxes rattachées aux buckets et aux dépôts.

## Comment procéder {#how-to-use-this}

Examiner et corriger les secrets utilisés dans les Spaces de Hugging Face après la divulgation du 2024-06-05 concernant les Spaces. Évaluer Hugging Face Inference Providers comme voie d'accès à l'inférence médiée par un fournisseur à partir du 2025-02-03, lors du choix des workflows de déploiement.

1. Créer un jeton d'accès à granularité fine limité au dépôt ou à la tâche d'inférence, puis authentifier une machine de développement avec hf auth login.
  — <https://huggingface.co/docs/hub/en/security-tokens>
2. Créer un dépôt de modèle, de jeu de données ou de Space ; définir le propriétaire, la visibilité et la licence ; puis téléverser avec hf upload ou Git/Xet.
  — <https://huggingface.co/docs/hub/en/repositories-getting-started>
3. Publier une Model Card dans le README du dépôt avec les usages prévus, les limites, les informations d'entraînement, les jeux de données et les résultats d'évaluation.
  — <https://huggingface.co/docs/hub/en/model-cards>
4. Pour l'inférence hébergée, sélectionner un modèle compatible du Hub et l'appeler via InferenceClient avec un modèle et un fournisseur explicites lorsque la charge de travail exige un routage prévisible.
  — <https://huggingface.co/docs/huggingface_hub/guides/inference>
5. Pour un workflow d'agent, ouvrir les paramètres MCP en étant connecté, utiliser la configuration client générée, redémarrer le client, puis n'ajouter que les outils Hub ou Space nécessaires à la tâche.
  — <https://huggingface.co/docs/hub/en/agents-mcp>
6. Pour un Space, choisir délibérément une visibilité publique, protégée ou privée, et placer les identifiants dans Space Secrets plutôt que dans le code source ou dans les Variables publiques.
  — <https://huggingface.co/docs/hub/en/spaces-overview>

## Bonnes pratiques {#best-practices}

- Utiliser un jeton à granularité fine par application ou par usage ; utiliser les OIDC Trusted Publishers pour la CI lorsque c'est possible, plutôt que de stocker un jeton de longue durée.
  — <https://huggingface.co/docs/hub/en/security-tokens>
- Considérer la Model Card comme une exigence de publication : préciser l'usage prévu, les limites connues, les données et paramètres d'entraînement, ainsi que les éléments d'évaluation.
  — <https://huggingface.co/docs/hub/en/model-cards>
- Définir un identifiant de modèle Hub explicite et un fournisseur nommé en production ; les modèles recommandés et la sélection automatique du fournisseur peuvent évoluer.
  — <https://huggingface.co/docs/huggingface_hub/guides/inference>
- Vérifier la compatibilité modèle-tâche-fournisseur avant le déploiement ; un modèle hébergé sur le Hub n'est pas automatiquement disponible chez tous les fournisseurs d'inférence.
  — <https://huggingface.co/docs/inference-providers/index>
- Garder les secrets des Spaces hors du code et des Variables : les Secrets sont privés alors que les Variables sont visibles publiquement et copiées lors de la duplication des Spaces.
  — <https://huggingface.co/docs/hub/en/spaces-overview>
- Utiliser la configuration générée par les paramètres MCP et réserver l'activation explicite des outils de dépôt avec droits d'écriture, des Jobs, des Sandboxes et des Spaces communautaires.
  — <https://huggingface.co/docs/hub/en/agents-mcp>

## Remplacé par ceci {#superseded-by-this}

- 2022-12-28 — Les workflows du prix, du certificat et de soumission au classement du DreamBooth Hackathon sont obsolètes, l'événement s'étant terminé en janvier 2023.
- 2024-06-05 — Les recommandations fondées sur les jetons classiques de lecture/écriture à large portée sont remplacées par des jetons à granularité fine par application et des jetons OIDC à courte durée de vie pour la CI.
- 2025-02-03 — L'hypothèse d'une API d'inférence hébergée statique unique pour tous les modèles du Hub est remplacée par la compatibilité des fournisseurs et la sélection explicite du fournisseur.
- 2025-06-07 — La configuration client MCP écrite à la main et figée est remplacée par la configuration générée dans les paramètres et par la navigation hf_fs.

## Toujours inconnu {#still-unknown}

- Hugging Face combine une plateforme de dépôts, une couche d'intégration des environnements d'exécution locaux, une passerelle d'inférence, la plateforme Spaces et un connecteur MCP. Ces événements reflètent une chronologie de plateforme, et non une migration unique d'un seul produit.
- La publication du 2025-06-07 n'a fourni aucun contenu lisible pendant la recherche. Le changelog de Hugging Face du 6 juin confirme indépendamment le lancement de MCP, mais pas la formulation exacte de la publication.
- La référence Local Apps pointe vers une source de dépôt mutable plutôt que vers une révision immuable de mai 2024 ; son comportement historique exact n'est donc pas vérifié.
- Les prix actuels, quotas, conditions de traitement des données et disponibilités n'ont pas été relevés, car ils varient selon le forfait, le modèle et le fournisseur.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/dreambooth-hackathon | DreamBooth Hackathon | 2026-09-04 |
| https://github.com/huggingface/huggingface.js/blob/main/packages/tasks/src/local-apps.ts | local-apps.ts — huggingface.js | 2026-09-04 |
| https://raw.githubusercontent.com/huggingface/huggingface.js/main/packages/tasks/src/local-apps.ts | Source brute de local-apps.ts | 2026-09-04 |
| https://huggingface.co/blog/space-secrets-disclosure | Divulgation de fuite de secrets de Spaces | 2026-09-04 |
| https://huggingface.co/blog/inference-providers | Welcome to Inference Providers on the Hub | 2026-09-04 |
| https://x.com/_akhaliq/status/1931013733406445702 | Statut x.com 1931013733406445702 | 2026-09-04 |
| https://huggingface.co/changelog/hf-mcp-server | Connect Your MCP Client to the Hugging Face Hub | 2026-09-04 |
| https://huggingface.co/changelog/mcp-improvements-jul-26 | MCP Server Enhancements | 2026-09-04 |
| https://huggingface.co/docs/hub/en/index | Documentation du Hugging Face Hub | 2026-09-04 |
| https://huggingface.co/docs/hub/en/repositories-getting-started | Getting Started with Repositories | 2026-09-04 |
| https://huggingface.co/docs/hub/en/model-cards | Model Cards | 2026-09-04 |
| https://huggingface.co/docs/hub/en/security-tokens | User access tokens | 2026-09-04 |
| https://huggingface.co/docs/inference-providers/index | Inference Providers | 2026-09-04 |
| https://huggingface.co/docs/huggingface_hub/guides/inference | Run Inference on servers | 2026-09-04 |
| https://huggingface.co/docs/hub/en/agents-mcp | Serveur MCP de Hugging Face | 2026-09-04 |
| https://huggingface.co/docs/hub/en/spaces-overview | Spaces Overview | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `organization:hugging-face`, fil `hugging-face-platform-evolution`, 4 événements datés du 2022-12-28 au 2025-02-03.
- **Note pratique :** Après la divulgation du 2024-06-05 concernant les Spaces, examiner et corriger tous les secrets utilisés dans les Spaces de Hugging Face ; à partir du 2025-02-03, évaluer Hugging Face Inference Providers comme voie d'accès à l'inférence médiée par un fournisseur lors du choix des workflows de déploiement.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

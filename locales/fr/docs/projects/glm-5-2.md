---
title: "GLM-5.2 — Disponibilité du modèle"
category: projects
date: 2026-06-14
tags: [glm-5-2, glm_models, model-availability, project]
aliases: ["GLM-5.2"]
level: 3
source_sha256: 5086941fae00f3f982651b1c4ec2ee8af80723337a1fb344c739901f60a01fc3
translation: machine
translated_at: '2026-10-24'
---
# GLM-5.2 — Disponibilité du modèle {#glm-52-model-availability}

**Ligne de développement :** `project:glm-5-2` · fil `model-availability`  
**Dernier événement :** 2026-06-14 · 1 événement daté depuis le 2026-06-14 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

GLM-5.2 est un modèle de Z.ai toujours référencé, destiné aux agents d'ingénierie logicielle.

- Raisonnement
- Streaming
- Appels de fonctions
- Mise en cache du contexte
- JSON structuré
- MCP

Contexte de 1M et sortie de 128K.

Conservez GLM-5.2 pour des raisons de compatibilité ou pour une comparaison contrôlée, mais utilisez GLM-5.3 pour tout nouveau travail de codage.

## Ligne de développement {#development-line}

- **2026-06-14 — La documentation de Z.ai identifie GLM-5.2 comme son dernier modèle.** Le 2026-06-14, Z.ai a publié un lien vers la documentation DevPack du dernier modèle, dans la ligne de projet GLM-5.2. Il s'agit d'une étape de disponibilité, mais nous n'avons pas étudié la publication ni la documentation. Nous n'affirmons aucun détail de sortie, aucune capacité et aucune condition d'accès.

## Changements {#what-changed}

- 2026-06-14 — L'URL « dernier modèle » fournie renvoie à un guide de migration vers GLM-5.3 ; elle ne prouve donc pas le lancement de GLM-5.2.
- 2026-06-16 — Z.ai a publié GLM-5.2 et l'a placé en open source sous licence MIT, en ajoutant un modèle à contexte lossless de 1M destiné aux tâches de codage longues.
- 2026-07-08 — Une évaluation indépendante du CAISI a ajouté une mise en garde en matière de sécurité : les garde-fous de déploiement n'ont pas empêché l'assistance agentique au développement d'exploits, et les opérateurs peuvent supprimer ces garde-fous sur les poids ouverts auto-hébergés.
- 2026-08-18 — GLM-5.3 a remplacé GLM-5.2 comme modèle phare le plus récent de Z.ai, avec un gain de 50 % en codage annoncé par le fournisseur sur Z.ai Code Bench.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-14, consultez la documentation DevPack de Z.ai sur le dernier modèle avant de sélectionner GLM-5.2. Ne supposez pas qu'un modèle GLM antérieur reste l'option documentée actuelle.

1. Créez un client API Z.ai et envoyez une requête authentifiée par Bearer vers `https://api.z.ai/api/paas/v4/chat/completions` avec `model: "glm-5.2"` et au moins un message utilisateur.
  — <https://docs.z.ai/guides/llm/glm-5.2>
2. Pour une tâche de codage difficile, activez la réflexion et définissez `reasoning_effort` à `max`. Limitez `max_tokens` à la sortie réellement nécessaire.
  — <https://docs.z.ai/guides/llm/glm-5.2>
3. Utilisez `stream: true` lorsque l'appelant peut consommer des fragments Server-Sent Events. Omettez ce paramètre ou définissez-le à false pour une réponse synchrone.
  — <https://docs.z.ai/api-reference/llm/chat-completion>
4. Traitez les arguments d'appel de fonction renvoyés comme des entrées non fiables. Validez-les par rapport au schéma déclaré avant toute exécution.
  — <https://docs.z.ai/api-reference/llm/chat-completion>

## Bonnes pratiques {#best-practices}

- Pour une tâche de refactorisation, définissez explicitement les limites de la logique métier, de l'API, de l'environnement d'exécution, des dépendances et de la vérification. Exigez un plan et les résultats de tests pertinents avant d'accepter la modification.
  — <https://docs.z.ai/guides/llm/glm-5.2>
- Gardez `thinking.clear_thinking` activé pour les conversations ordinaires. Ne conservez le raisonnement antérieur que si l'historique complet, non modifié et correctement ordonné est disponible.
  — <https://docs.z.ai/api-reference/llm/chat-completion>
- Évaluez GLM-5.3 en priorité pour les nouveaux déploiements de codage. Conservez GLM-5.2 uniquement lorsque son identifiant de modèle constitue une contrainte de compatibilité voulue.
  — <https://docs.z.ai/guides/llm/glm-5.3>

## Remplacé par ceci {#superseded-by-this}

- :

## Inconnues restantes {#still-unknown}

- L'élément du 2026-06-14 précède la publication confirmée de Z.ai le 2026-06-16. Les documents officiels disponibles confirment un accès anticipé à Coding Plan avant la publication, mais ne datent pas cet aperçu au 14 juin.
- Les pages officielles de Z.ai divergent sur la date de GLM-5.3. L'index de recherche indique le 2026-08-14, tandis que les notes de version indiquent le 2026-08-18 ; nous retenons cette dernière date pour le remplacement.
- Nous n'avons effectué aucune requête API authentifiée. La disponibilité propre à un compte, les quotas et l'accès régional restent non vérifiés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://docs.z.ai/devpack/latest-model | How to Switch Models - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://docs.z.ai/release-notes/new-released | New Released - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://www.zhipuai.cn/zh/research/161 | GLM-5.2上线并开源：专注Coding与长程任务 | 2026-09-05 |
| https://docs.z.ai/guides/llm/glm-5.2 | GLM-5.2 - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://docs.z.ai/api-reference/llm/chat-completion | Chat Completion - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://www.nist.gov/document/caisi-assessment-zais-glm-52 | Assessment of Z.ai’s GLM-5.2 | 2026-09-05 |
| https://docs.z.ai/guides/llm/glm-5.3 | GLM-5.3 - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://www.zhipuai.cn/en/research | Research - Z.ai | 2026-09-05 |

## Fiche pour l'agent {#agent-brief}

- **Sujet :** `project:glm-5-2`, fil `model-availability`, 1 événement daté, du 2026-06-14 au 2026-06-14.
- **Remarque pratique :** Au 2026-06-14, consultez la documentation DevPack de Z.ai sur le dernier modèle avant de sélectionner GLM-5.2. Ne supposez pas qu'un modèle GLM antérieur reste l'option documentée actuelle.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

---
title: "AutoClaw"
category: projects

tags: [autoclaw, autoclaw-development, project]
aliases: ["AutoClaw"]
level: 3
source_sha256: 248539ac6c6b5536128b844fcd232fb2ea7adbe3d9afaacd1e1863c566b87bd2
translation: machine
translated_at: '2026-10-24'
---
# AutoClaw {#autoclaw}

**Ligne de développement :** `project:autoclaw` · fil `autoclaw-development`  
**Dernier événement :** - · 0 daté depuis - · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

AutoClaw est une application de bureau permettant de déléguer à un agent des tâches de recherche, de rédaction de documents, d'analyse de données, d'automatisation et d'ingénierie.

- Plus de 50 compétences intégrées pour exécuter les tâches de l'agent
- Fichiers locaux pour consulter et modifier les documents sur le disque
- Actions dans le navigateur pour interagir avec les pages web
- Intégrations de messagerie instantanée pour connecter les flux de travail de discussion
- Modèles GLM pour exécuter l'inférence

Les appels aux modèles nécessitent une connexion Internet.
Nous obtenons un environnement de bureau géré pour les tâches d'agent, et non un modèle autonome.

## Ligne de développement {#development-line}

- L'événement daté n'a pas encore fait l'objet d'un compte rendu ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

- 2026-03-31 : AutoClaw a été consigné comme une variante d'OpenClaw installable localement. Dans un rapport d'entreprise, Z.ai a indiqué que Claw Plan, lancé en mars, a atteint 100 000 abonnements en deux jours.
- 2026-03-10 : L'application a été lancée publiquement avec une installation locale d'OpenClaw en un clic, plus de 50 compétences préinstallées et une connexion à Feishu.
- 2026-03-15 : GLM-5-Turbo est devenu le modèle Z.ai dédié aux flux de travail OpenClaw : utilisation d'outils, compétences, tâches en plusieurs étapes et coordination d'agents.
- 2026-06-24 : AutoClaw v1.9.0 a ajouté GLM-5.2 avec une fenêtre de contexte de 1 M de tokens ainsi qu'Auto Design.
- 2026-08-27 : La version v1.17.8 figurant dans le journal des modifications a ajouté GLM-5.3-Flash et amélioré l'aperçu des fichiers bureautiques ainsi que les réponses en flux continu.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-31, ne modifiez aucune pratique sur la base de cette ligne tant que le message d'origine ou des éléments de recherche indépendants n'auront pas établi un événement de développement précis d'AutoClaw.

1. Ouvrez la section de téléchargement officielle et sélectionnez le programme d'installation pour Windows ou le type de processeur de votre Mac.
  — <https://autoclaw.z.ai/download/>
2. Installez l'application : sous Windows, exécutez le .exe ; sous macOS, faites glisser l'application depuis le .dmg vers Applications.
  — <https://autoclaw.z.ai/download/>
3. Connectez-vous au premier lancement ; les compétences intégrées fonctionnent sans Python, Node.js ni environnement CLI.
  — <https://autoclaw.z.ai/download/>
4. Pour les grandes tâches de PRD et d'interface, ouvrez Auto Design, attendez la fin de l'initialisation et transmettez les exigences dans leur intégralité.
  — <https://autoclaw.z.ai/blog/product/autoclaw-v1-9-0-glm-5-2-auto-design/>

## Bonnes pratiques {#best-practices}

- Ne téléchargez le programme d'installation que depuis autoclaw.z.ai ou le domaine officiel chinois, car les versions tierces ne bénéficient d'aucune prise en charge et présentent des risques de sécurité.
  — <https://autoclaw.z.ai/download/>
- Vérifiez le type de puce sur Mac avant de télécharger, car les versions Apple Silicon et Intel ne sont pas interchangeables.
  — <https://autoclaw.z.ai/download/>
- Transmettez le contexte complet des exigences pour les travaux complexes afin que le découpage manuel des tâches ne fasse pas perdre de détails.
  — <https://autoclaw.z.ai/blog/product/autoclaw-v1-9-0-glm-5-2-auto-design/>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-24 : Les consignes liées à AutoClaw v1.9.0 ne décrivent plus la version v1.17.8 consignée le 2026-08-27.
- 2026-03-15 : Le modèle par défaut des flux de travail OpenClaw est passé d'un état générique initial à GLM-5-Turbo ; le produit a ensuite reçu GLM-5.2 et GLM-5.3-Flash.

## Toujours inconnu {#still-unknown}

- La page officielle citée pour l'événement du 2026-03-31 redirige vers l'interface web actuelle et ne fournit ni date d'archivage ni description pour ce jour.
- Aucune note de version primaire datée ne confirme la version initiale exacte d'AutoClaw ni l'intégralité de ses modifications au 2026-03-31.
- Le lancement du 2026-03-10 et les plus de 50 compétences reposent sur un rapport daté secondaire ; nous n'avons trouvé aucun billet de lancement primaire dans les sources disponibles.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://autoglm.z.ai/autoclaw/ | AutoClaw Web \| AI IM Workspace | 2026-09-05 |
| https://www.hkexnews.hk/listedco/listconews/sehk/2026/0331/2026033101550_c.pdf | Knowledge Atlas Technology Joint Stock Company Limited annual results announcement | 2026-09-05 |
| https://www.ithome.com/0/927/423.htm | 智谱“澳龙”AutoClaw 正式上线：支持本地电脑一键部署，预置 50+ 热门 Skills | 2026-09-05 |
| https://docs.bigmodel.cn/cn/update/new-releases | 模型与产品发布记录 - 智谱AI开放文档 | 2026-09-05 |
| https://autoclaw.z.ai/download/ | Download AutoClaw - Official Windows & macOS Desktop App | 2026-09-05 |
| https://autoclaw.z.ai/blog/product/autoclaw-v1-9-0-glm-5-2-auto-design/ | AutoClaw V1.9.0: Build Complete App UI Designs from Long PRDs with GLM-5.2 and Auto Design | 2026-09-05 |
| https://autoclaw.z.ai/changelog/ | AutoClaw Changelog \| Product Release Notes | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:autoclaw`, fil `autoclaw-development`, 0 événement daté - → -.
- **Remarque pratique :** Au 2026-03-31, ne modifiez aucune pratique sur la base de cette ligne tant que le message d'origine ou des éléments de recherche indépendants n'auront pas établi un événement de développement précis d'AutoClaw.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

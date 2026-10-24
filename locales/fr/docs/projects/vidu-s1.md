---
title: "Vidu S1"
category: projects

tags: [project, vidu-s1]
aliases: ["Vidu S1"]
level: 3
source_sha256: e583e53e3229ab76e6a40d1d27c7bfb600deb999cc282db4f63b9aab21c2314b
translation: machine
translated_at: '2026-10-24'
---
# Vidu S1 {#vidu-s1}

**Ligne de développement :** `project:vidu-s1` · fil `vidu-s1`  
**Dernier événement :** - · 0 événement daté depuis - · **Recherche :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

Vidu S1 est le modèle vidéo hébergé en temps réel de ShengShu, destiné aux créateurs et aux équipes produit qui conçoivent des personnages numériques interactifs capables de parler. Vidu le présente séparément des modèles de génération de clips Q1/Q2/Q3.

- Création de personnage : construit un personnage à partir d'une persona, d'une image initiale (humain, anime ou animal de compagnie) et d'une voix sélectionnée ou clonée.
- Contrôle dynamique : modifie les actions du personnage à partir d'instructions orales pendant une session audio ou vidéo.
- Accès client : propose Vidu Stream et une API Vidu S1 (bêta) actuellement documentée, utilisant une WebSocket de contrôle et des flux multimédias AliRTC.

La page produit indique du 540p à 25 ips, pouvant atteindre 42 ips. La durée de session et la facturation doivent être lues dans la réponse de la session en direct, car la documentation du fournisseur est contradictoire. Ce modèle convient aux interactions d'avatars réactives, et non à une installation de modèle en local ni à un clip classique finalisé.

## Ligne de développement {#development-line}

- L'entrée datée n'est pas encore rédigée ; les éléments connus figurent dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-07-10 — La présentation publique de Vidu S1 sur GitHub a reçu trois modifications de GIF d'expérience. La sortie officielle était déjà datée du 2026-07-03 : il s'agissait donc d'un affinement de la démonstration et de la documentation, et non d'une nouvelle version du modèle.

## Comment l'utiliser {#how-to-use-this}

1. Pour un essai sans code, ouvrez Vidu Stream, connectez-vous et vérifiez le compte, puis sélectionnez un personnage ou créez-en un.
  — <https://www.vidu.com/vidu-stream>
2. Définissez la persona, importez une image initiale, puis sélectionnez, importez ou clonez une voix avant de démarrer la conversation.
  — <https://www.vidu.com/vidu-stream>
3. Utilisez des instructions orales pendant la conversation pour diriger les actions du personnage.
  — <https://www.vidu.com/vidu-stream>
4. Pour une application, obtenez une clé API et créez une session Live avec `POST /live/v1/lives` ; conservez `live.id` ainsi que les identifiants RTC renvoyés.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
5. Rejoignez le canal Aliyun RTC et établissez la WebSocket de contrôle authentifiée, attendez `conn_init_ack.success=true`, puis raccrochez, fermez la WebSocket et quittez le canal RTC.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>

## Bonnes pratiques {#best-practices}

- Pour les clients navigateur, conservez la clé API Vidu brute sur un backend de confiance et faites transiter la WebSocket authentifiée par un proxy. Les WebSockets natives du navigateur ne permettent pas de définir l'en-tête d'autorisation requis.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
- Considérez `live_duration` renvoyé et l'usage final facturé comme faisant foi. Ne codez pas en dur de plafond de session « illimité » ou fixe.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/api-reference.md>
- En mode vidéo, implémentez une gestion de fermeture, d'attente progressive (backoff) puis de reconnexion pour `NOT_READY`. Créez une nouvelle session Live en cas de `LIVE_CONN_INIT_FAILED`.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
- Intégrez Aliyun RTC comme couche média distincte et abonnez-vous une seule fois au flux distant actif. Ignorez les événements RTC ou WebSocket obsolètes provenant d'une session précédente.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
- Gérez à la fois les raccrochages côté serveur `type:6` et les fermetures anormales de la WebSocket. Après un raccrochage actif, fermez la WebSocket avant d'appeler `leaveChannel()`.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/websocket-protocol.md>

## Remplacé par {#superseded-by-this}

- 2026-07-03 — Considérer Vidu S1 comme un générateur vidéo standard de type « soumettre un prompt puis attendre », ou comme une variante de la série Vidu Q, est obsolète. Il a été lancé comme une ligne distincte de personnages numériques interactifs en temps réel.
- 2026-07-03 — Présenter le 2026-07-10 comme le lancement de Vidu S1 est obsolète. ShengShu l'a officiellement publié le 2026-07-03.

## Points encore inconnus {#still-unknown}

- La API de plateforme publique indique que `live_duration` a un maximum de 600 secondes, alors que le guide d'intégration édité par le fournisseur recommande d'utiliser une valeur renvoyée propre à la politique et mentionne 7200 secondes. Aucune réponse de compte en direct n'était disponible pour les réconcilier.
- Les sources actuelles du fournisseur sont également contradictoires concernant l'unité de crédit et le tarif supplémentaire du clonage de voix. Utilisez une console authentifiée ou une réponse de facturation finale avant d'approuver un budget.
- Le dépôt Vidu-S1 lié fournit de la documentation et des images, et non des poids de modèle publics ni un paquet d'inférence exécutable ; le déploiement local et les droits de licence du modèle restent non vérifiés.
- Les chiffres de 42 ips et de durée longue relèvent des affirmations du fournisseur et de prépublications, et non d'une garantie indépendante de latence ou de qualité pour chaque déploiement.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/shengshu-ai/Vidu-S1 | Vidu S1: A Real-Time Interactive Video Generation Model | 2026-09-06 |
| https://github.com/shengshu-ai/Vidu-S1/commits/main | Commits · shengshu-ai/Vidu-S1 · GitHub | 2026-09-06 |
| https://www.vidu.com/vidu-stream | Vidu S1 AI Video Model | Vidu AI | 2026-09-06 |
| https://platform.vidu.com/docs/vidu-s1 | Vidu S1 API (Beta) | Vidu API | 2026-09-06 |
| https://platform.vidu.com/docs/model-map | Model Map | Vidu API | 2026-09-06 |
| https://platform.vidu.com/docs/pricing | Pricing | Vidu API | 2026-09-06 |
| https://www.genspi.com/zh/news/vidu-s1-realtime-interactive-model/ | 生数科技发布 Vidu S1，推动视频生成迈向“实时交互”新时代 | 2026-09-06 |
| https://arxiv.org/html/2607.03118v1 | Vidu S1: A Real-Time Interactive Video Generation Model | 2026-09-06 |
| https://www.genspi.com/zh/news/vidu-s1-zhenhuan-digital-human/ | 技术赋能 IP 新体验，Vidu S1助力 360 打造《甄嬛传》数字人新玩法 | 2026-09-06 |
| https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md | Vidu S1 Live API Integration | 2026-09-06 |
| https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/api-reference.md | Vidu S1 Live API — HTTP Reference | 2026-09-06 |
| https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/websocket-protocol.md | Vidu S1 Live API — WebSocket Control Protocol | 2026-09-06 |

## Résumé pour agent {#agent-brief}

- **Sujet :** `project:vidu-s1`, fil `vidu-s1`, 0 événement daté - → -.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.

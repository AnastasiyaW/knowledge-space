---
title: "Worldstream : worldstream-3d-world-model — Modèle du monde 3D Worldstream"
category: "projects"
date: 2026-10-22
tags: ["project", "worldstream", "worldstream-3d-world-model"]
aliases: ["Worldstream: worldstream-3d-world-model"]
level: 2
source_sha256: d5a9f393de0d1517398397cba41e924c1aa7cce97939833c6d99ceae9fd71ebd
translation: machine
translated_at: '2026-10-24'
---
# Worldstream : worldstream-3d-world-model — Modèle du monde 3D Worldstream {#worldstream-worldstream-3d-world-model-worldstream-3d-world-model}

**Ligne de développement :** project:worldstream · fil worldstream-3d-world-model  
**Dernier événement :** 2026-10-22 · 2 événements datés depuis le 2026-10-22 · **Consulté le :** 2026-10-23 · confiance : élevée

## Présentation {#what-it-is}

WorldStream est une architecture de modèle de monde 3D interactif et sans fin prédéfinie. Elle s'adresse aux chercheurs en simulation et aux développeurs d'environnements virtuels.

Capacités :

- Diffusion de terrain (terrain streaming) : génère un terrain 3D continu au-delà des limites d'une carte prédéfinie.
- Planification hiérarchique : une échelle macro organise l'écologie et les transports, une échelle micro compile les tuiles individuelles.
- Compilation procédurale : du code déterministe transforme des décisions structurées en terrain, routes, végétation, implantations et entités.
- Contrôle par le langage : des instructions en langage naturel, sans forme fixée, modifient le monde et pilotent les entités qu'il contient.
- Persistance : les modifications des utilisateurs, les engagements aux frontières et les enregistrements d'PNJ à état sont conservés lorsque les tuiles sont déchargées puis rechargées.

Le débit et la cohérence spatiale reposent sur deux éléments : une prédiction précise du couloir de déplacement et des budgets bornés pour la compilation procédurale. WorldStream constitue une alternative structurée crédible aux générations boîte noire en vidéo ou en voxels, car elle associe une planification symbolique à une compilation graphique déterministe.

## Ligne de développement {#development-line}

- **2026-10-22 — WorldStream : modèle de monde 3D interactif en streaming, avec planification hiérarchique.** Des chercheurs ont annoncé WorldStream, un modèle de monde 3D sans fin prédéfinie. Il étend le terrain jouable au-delà des cartes préspécifiées, agit sur des instructions en langage libre dans le monde en cours d'exécution et restitue les lieux visités avec leurs modifications. Un planificateur hiérarchique (étapes Macro et Micro) transmet ses plans à un code local déterministe, qui les compile en terrain, routes, implantations, végétation et entités. La conception en streaming planifie à l'avance le long du couloir de déplacement prédit.
- **2026-10-22 — WorldStream présenté comme modèle de monde 3D interactif et sans fin prédéfinie.** Une préimpression datée du 2026-10-22 présente WorldStream. Le modèle étend le terrain jouable au-delà d'une carte prédéfinie, agit sur des instructions en langage libre et restitue les régions visitées avec leurs modifications. Son planificateur hiérarchique émet des décisions structurées pour le terrain, les implantations et les entités. Le streaming ne compile que les régions nécessaires à court terme. Un enregistrement persistant du monde conserve les modifications et les PNJ à état.
- **2026-10-22 — autres informations relevées à cette date.**
  - L'article précise que le planificateur hiérarchique opère sur un modèle de décision typé. La planification macro régit des groupes de tuiles spatiales et fixe la topologie globale écologique, hydrologique et de transport. La planification micro spécialise ces contrats au terrain local mesuré et aux engagements aux frontières avec les tuiles voisines. La géométrie située derrière le couloir de déplacement prédit du joueur est déchargée activement, de sorte que la mémoire reste dans un budget borné. (2026-10-22) — <https://arxiv.org/abs/2610.28827>
  - L'article détaille que l'enregistrement persistant du monde est tenu par tuile. Il stocke les graines, les identités d'entités mutables et les engagements aux frontières, ainsi que les modifications d'attributs introduites par l'utilisateur. Une tuile qui revient est recompilée à partir de ces enregistrements structurés, sans être réinférée et sans être stockée sous forme de maillage brut lourd. (2026-10-22) — <https://arxiv.org/abs/2610.28827>

## Évolutions {#what-changed}

La recherche initiale a établi le cadre central de WorldStream. Elle fait passer la génération de mondes sans fin prédéfinie d'une synthèse hors ligne monolithique à une exécution découplée en streaming. L'architecture introduit :

- une planification hiérarchique à deux niveaux, couvrant des groupes de tuiles et des cellules locales ;
- une compilation procédurale déterministe, pour réduire l'empreinte mémoire ;
- un état persistant par tuile, afin que les modifications tiennent lorsqu'une région est revisitée.

## Mode d'emploi {#how-to-use-this}

1. Définir les graines de génération globales et les a priori environnementaux. Ils initialisent la couche de planification Macro pour l'écologie régionale, l'hydrologie et les réseaux de transport.
  — <https://arxiv.org/abs/2610.28827>
2. Fournir la position de l'agent et ses vecteurs de cap pour projeter le couloir de déplacement. Cela déclenche par anticipation la planification Micro pour les tuiles qui arrivent ensuite.
  — <https://arxiv.org/abs/2610.28827>
3. Exécuter la compilation procédurale déterministe locale. Elle transforme les décisions de plan Micro approuvées en terrain 3D, végétation et actifs d'implantations rendables.
  — <https://arxiv.org/abs/2610.28827>
4. Émettre des commandes en langage naturel pour mettre à jour les entités d'exécution ou les attributs des tuiles. Les états modifiés sont persistés dans la base d'enregistrements du monde, tuile par tuile.
  — <https://arxiv.org/abs/2610.28827>

## Bonnes pratiques {#best-practices}

- Séparer les horizons de planification de la compilation géométrique le long des couloirs prédits, afin de stabiliser la fréquence d'images et d'éviter les pics de calcul.
  — <https://arxiv.org/abs/2610.28827>
- Imposer des engagements stricts entre tuiles voisines dans le planificateur Micro, pour que des cellules compilées indépendamment ne présentent ni coutures visuelles ni incohérences topologiques.
  — <https://arxiv.org/abs/2610.28827>
- Lorsque l'agent parcourt de longues distances, recompiler à partir des enregistrements de graines et de mutations par tuile, plutôt que de mettre en cache des maillages à haute densité de polygones en mémoire.
  — <https://arxiv.org/abs/2610.28827>

## Remplacé par cette approche {#superseded-by-this}

- La génération monolithique hors ligne de mondes 3D, qui limite la simulation à des cartes statiques précalculées, sans diffusion dynamique infinie.
  — <https://arxiv.org/abs/2610.28827>
- Le streaming sans état, qui abandonne les modifications de terrain des utilisateurs et l'historique d'interactions avec les PNJ lorsqu'une tuile est évincée.
  — <https://arxiv.org/abs/2610.28827>

## Points encore inconnus {#still-unknown}

- Les benchmarks d'exécution externes et indépendants, ainsi que la disponibilité du code open source, ne sont pas vérifiés tant qu'un dépôt public n'a pas été publié.
- Les évaluations par la communauté et les retours d'usage de praticiens n'ont pas encore paru ; la préimpression a été publiée le 22 octobre 2026.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://arxiv.org/abs/2610.28827 | WorldStream : diffusion de mondes 3D interactifs avec planification hiérarchique et état persistant | 2026-10-23 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** project:worldstream, fil worldstream-3d-world-model, 2 événements datés du 2026-10-22 au 2026-10-22.
- **Remarque pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

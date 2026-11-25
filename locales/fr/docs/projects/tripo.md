---
title: "Tripo"
category: projects
date: 2026-06-23
tags: [project, tripo, tripo-development, triposg_triposf]
aliases: ["Tripo", "Tripo 2.0", "Tripo 3.0"]
level: 3
source_sha256: 7990bc3128e26285de5771f5cc4bbc7c1e2f54ee0f952ba70d7e558182ee096d
translation: machine
translated_at: '2026-10-24'
---
# Tripo {#tripo}

**Ligne de développement :** `project:tripo` · fil `tripo-development`  
**Dernier événement :** 2026-06-23 · 4 entrées datées depuis 2024-09-20 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Tripo est une suite de génération d'assets 3D destinée aux artistes, aux studios de jeux et aux équipes produit.

- Studio : intègre la génération, la segmentation, la retopologie, le texturage et le rigging dans un seul espace de travail web.
- API : met en file d'attente les tâches de génération texte-vers-modèle, image-vers-modèle et multivues-vers-modèle.

L'API sert les familles de modèles H2, H3 et P1 ; la tarification et les paramètres dépendent du modèle et de la tâche. Nous l'utilisons pour ébaucher et affiner rapidement des assets, mais nous vérifions la topologie, l'échelle et les matériaux dans le DCC ou le moteur de jeu de destination.

## Ligne de développement {#development-line}

- **2024-09-20 — Point d'entrée de l'application web Tripo.** Le 20 septembre 2024, Tripo a créé un lien direct vers l'application web Tripo 3D. La source ne donne ni la date de lancement, ni la version, ni les capacités.
- **2025-03-31 — Projet public TripoSG et liens de distribution.** Les poids et le code d'inférence du modèle image-vers-3D ont été publiés séparément.
- **2025-08-20 — Espace de génération Tripo Studio.** Le 20 août 2025, Tripo a ouvert l'espace de travail hébergé Tripo Studio, en référence à la publication de TripoSG de mars 2025. Les notes ne confirment ni nouveau modèle, ni nouvelle fonctionnalité, ni changement de tarification.
- **2026-06-23 — Mise à jour produit de Tripo de mai.** Le 23 juin 2026, Tripo a publié l'article officiel « May Update on Tripo ». L'article ne liste pas les changements précis et ne permet pas de vérifier sa date exacte de publication.

## Ce qui a changé {#what-changed}

- 2024-09-20 — Tripo 2.0 a fait passer la gamme commerciale vers une nouvelle génération de synthèse 3D.
- 2025-03-31 — TripoSG a séparé la recherche ouverte de Studio, en publiant séparément les poids image-vers-3D et le code d'inférence.
- 2025-08-20 — Algorithm 3.0 a atteint une publication publique avec une géométrie, des textures et une segmentation plus détaillées.
- 2026-06-23 — Studio a ajouté 8K Texture, Segmentation v2, un DCC Bridge pour ZBrush et des niveaux de tarification pour équipes.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-03-31, considérez les ressources publiques de TripoSG sur GitHub et Hugging Face comme distinctes de l'application hébergée de Tripo et de Studio. À partir du 2026-06-23, consultez la page de mise à jour officielle avant de supposer le flux de travail hébergé ou l'ensemble de fonctionnalités actuels.

1. Créez une clé API et transmettez-la dans l'en-tête Bearer Authorization pour l'automatisation.
  — <https://docs.tripo3d.ai/get-started/quick-start.html>
2. Soumettez une tâche à POST /v2/openapi/task avec text_to_model, image_to_model ou multiview_to_model.
  — <https://docs.tripo3d.ai/get-started/quick-start.html>
3. Stockez task_id et interrogez GET /v2/openapi/task/{task_id} jusqu'à ce que status vaille success ; les URL de résultat expirent par défaut au bout de cinq minutes.
  — <https://docs.tripo3d.ai/task-query/get-your-task-result.html>
4. Vérifiez le coût en crédits avant les traitements par lots : image-vers-modèle coûte 20 à 50 crédits, tandis que la segmentation, le low-poly et le rigging sont facturés séparément.
  — <https://docs.tripo3d.ai/get-started/pricing.html>

## Bonnes pratiques {#best-practices}

- Précisez l'objet, le matériau, la forme et l'intention pour la 3D à partir de texte, et ajoutez un prompt négatif pour exclure les éléments indésirables.
  — <https://www.tripo3d.ai/blog/text-to-3d-prompt-engineering>
- Vérifiez un asset importé en termes d'échelle, d'orientation, de pivot et de budget de polygones avant de le dupliquer dans la scène.
  — <https://www.tripo3d.ai/zh-Hant/blog/ai-environment-creator>
- N'acceptez pas une retopologie automatique pour l'animation sans contrôler les déformations. Une anatomie non standard, des boucles d'arêtes faciales et des rigs propriétaires peuvent nécessiter un nettoyage manuel.
  — <https://www.tripo3d.ai/blog/retopo-an-ai-character-model-for-animation>

## Remplacé par ceci {#superseded-by-this}

- 2025-02-11 — L'affirmation selon laquelle Algorithm 2.5 était le dernier modèle commercial a été remplacée par la publication publique d'Algorithm 3.0 en août 2025.
- 2025-05-22 — Le flux de travail « générer et exporter uniquement » a été remplacé lorsque Tripo Studio a ajouté la segmentation, les outils low-poly, l'édition de textures et Uni-Rig.
- 2024-09-20 — Tripo 2.0 est obsolète pour les nouvelles intégrations ; la documentation de l'API oriente les nouvelles intégrations vers H3, H2, P1 ou Turbo-v1.0.

## Inconnues restantes {#still-unknown}

- TripoSG est un modèle de recherche ouvert de VAST, tandis que Tripo Studio et l'API sont des produits commerciaux du même écosystème. Nous ne pouvons pas les traiter comme des versions interchangeables.
- La date exacte de lancement de Tripo 2.0 au sein de septembre 2024 n'est pas vérifiée par une annonce primaire datée ; seuls le mois et l'année sont confirmés.
- La documentation publique de l'API utilise H2, H3 et P1, tandis que le marketing utilise 2.0, 2.5 et 3.0 ; la correspondance directe entre ces noms n'est pas confirmée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.tripo3d.ai/blog/vast-open-source-month | VAST Open Source Month | TripoSG & TripoSF, Setting a New SOTA in 3D Generation | 2026-09-05 |
| https://github.com/VAST-AI-Research/TripoSG/blob/main/README.md | README de TripoSG | 2026-09-05 |
| https://www.tripo3d.ai/blog/tripo-2-5-and-plugins | Dernières versions et mises à jour de Tripo : Algorithm 2.5, plugins Blender et Unity | 2026-09-05 |
| https://www.tripo3d.ai/blog/introducing-tripo-studio | Présentation de Tripo Studio : votre nouvel espace de travail 3D avec l'IA | 2026-09-05 |
| https://www.accessnewswire.com/newsroom/en/business-and-professional-services/tripo-the-frontrunner-of-3d-ai-boom-supercharges-new-era-in-cont-1066689 | Annonce de la mise à niveau Tripo 3.0 | 2026-09-05 |
| https://www.tripo3d.ai/blog/may-update-on-tripo | Nouveautés de Tripo | Mai | 2026-09-05 |
| https://docs.tripo3d.ai/get-started/quick-start.html | Démarrage rapide de l'OpenAPI Tripo et authentification | 2026-09-05 |
| https://docs.tripo3d.ai/task-query/get-your-task-result.html | Obtenir le résultat de votre tâche | 2026-09-05 |
| https://docs.tripo3d.ai/get-started/pricing.html | Tarification de l'OpenAPI Tripo | 2026-09-05 |
| https://docs.tripo3d.ai/model-generation/image-to-model-v1-4-20240625.html | Référence API image-vers-modèle v1.4 | 2026-09-05 |
| https://www.tripo3d.ai/blog/text-to-3d-prompt-engineering | Maîtriser le prompt engineering pour les modèles 3D à partir de texte | 2026-09-05 |
| https://www.tripo3d.ai/zh-Hant/blog/ai-environment-creator | AI Environment Creator | 2026-09-05 |
| https://www.tripo3d.ai/blog/retopo-an-ai-character-model-for-animation | Comment retopologiser un modèle de personnage IA pour l'animation | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:tripo`, fil `tripo-development`, 4 événements datés du 2024-09-20 au 2026-06-23.
- **Note pratique :** À partir du 2025-03-31, considérez les ressources publiques de TripoSG sur GitHub et Hugging Face comme une voie distincte de recherche et de distribution, séparée de l'application hébergée de Tripo et de Studio ; à partir du 2026-06-23, consultez la page de mise à jour officielle avant de supposer le flux de travail hébergé ou l'ensemble de fonctionnalités actuels.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

<!-- live-update:9a22698ca8b1d44c45b9878f61fb75f78790f49dd7737df4a921e79e94e2a88d -->
## 2026-10-17 — Tripo lance un accès anticipé au dépliage UV et à la retopologie {#2026-10-17-tripo-launches-early-access-to-uv-unwrap-and-retopology}

Tripo a ouvert un accès anticipé au dépliage UV automatisé et à la retopologie. La conversion de maillage low-poly et la génération de disposition UV sont désormais intégrées directement à son flux de modélisation 3D.

### Usage et bonnes pratiques {#usage-and-practices}

- Générez un asset 3D dans Tripo à partir d'une description textuelle ou d'un prompt sous forme d'image 2D. [Source](https://customuse.com/)
- Lancez la retopologie automatique pour transformer le maillage dense généré en une structure optimisée de quads ou de triangles, dans les limites de polygones que vous définissez. [Source](https://customuse.com/)
- Appliquez le dépliage UV automatisé : il calcule les coutures, empaquette les îlots UV 2D et rebake les cartes de textures sur le maillage déplié. [Source](https://customuse.com/)
- Exportez l'asset optimisé au format FBX, OBJ ou USD pour un moteur de jeu ou un outil de création de contenu numérique. [Source](https://customuse.com/)
- Définissez le nombre cible de polygones avant de lancer la retopologie, afin que la densité de l'asset corresponde au budget de performance du moteur. [Source](https://customuse.com/)
- Vérifiez la disposition des îlots UV 2D et les coutures sur les zones à forte courbure avant de cuire les cartes de textures finales. [Source](https://customuse.com/)

### Preuves complémentaires {#additional-evidence}

- 2026-10-17 : la retopologie produit une sortie low-poly en quads ou en triangles, avec ce que Tripo appelle une allocation intelligente de la densité. Le calcul des coutures UV et l'empaquetage des îlots s'exécutent dans le même pipeline de génération d'assets 3D. [Source](https://customuse.com/)

### Recommandations remplacées (conservées pour l'historique) {#superseded-guidance-retained-for-history}

- 2026-10-17 : les maillages 3D générés par IA nécessitaient une retopologie et un dépliage UV manuels dans un logiciel externe avant le texturage ou l'entrée dans un moteur de jeu. [Source](https://customuse.com/)

### Limites et questions ouvertes {#limits-and-open-questions}

- Les chemins directs vers la documentation de Tripo sur tripo3d.ai n'ont pas pu être vérifiés, car les résultats de recherche les masquaient derrière des redirections. Il n'existe donc pas encore de citation directe de première partie.
- La tarification à long terme et le conditionnement par niveau de l'accès anticipé à la retopologie et au dépliage UV ne sont pas annoncés.


<!-- Retained base: 694331793733b8221866d9072af7e45999930387; article blob: 11d856f6dc8c75d0fae16ee7b15ee410955295d4 -->

<!-- live-update:9bcb91cd3e2d7094b7f6c1e8ebd6eb64e2fe47fe3bfc2d61e36252d582e1a65e -->
## 2026-10-23 — Tripo Studio ajoute le rigging squelettique automatique et l'animation pilotée par texte {#2026-10-23-tripo-studio-adds-skeletal-auto-rigging-and-text-driven-animation}

Tripo Studio riggue désormais les personnages automatiquement et les anime à partir de texte. Le rigging automatique propose cinq préréglages de squelettes humanoïdes : UE5 Mannequin, Mixamo, VRM 1.0, Unity Humanoid et ActorCore. Text to Motion transforme un prompt en un clip de 1 à 10 secondes et peut enchaîner des clips en séquences multi-étapes. Le rigging automatique humanoïde n'accepte que des maillages de moins de 100 000 triangles. Les poids de peau peuvent encore nécessiter des corrections dans un outil DCC externe.

## 2026-10-23 — Tripo Studio introduit le rigging automatique et le flux de génération de mouvements {#2026-10-23-tripo-studio-introduces-auto-rigging-and-motion-generation-workflow}

Le rigging et l'animation sont désormais intégrés à Tripo Studio. Les os sont placés automatiquement pour cinq préréglages standard de moteurs de jeu. L'animation provient de prompts textuels, et jusqu'à cinq segments de mouvement peuvent être enchaînés. Le tout fonctionne sur des modèles allant jusqu'à 100 000 triangles.

### Usage et bonnes pratiques {#usage-and-practices_1}

- Obtenez un maillage : générez un personnage 3D à partir d'un prompt textuel ou d'images de référence dans Tripo Studio, ou importez un maillage 3D existant. [Source](https://studio.tripo3d.ai/)
- Riggez-le : ouvrez le module Auto-Rigging et choisissez l'un des cinq préréglages (UE5 Mannequin, Mixamo, Unity Humanoid, VRM 1.0 ou ActorCore). Vérifiez d'abord que le maillage compte moins de 100 000 triangles. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- Animez-le : sélectionnez un mouvement prêt à l'emploi dans la bibliothèque de mouvements, ou saisissez un prompt dans Text to Motion pour obtenir un clip personnalisé de 1 à 10 secondes ou une séquence multi-étapes. [Source](https://www.tripo3d.ai/blog/rigging-animation)
- Exportez-le : prévisualisez la déformation dans la fenêtre 3D, ajustez la durée des étapes pour les séquences multi-étapes, puis exportez au format FBX ou GLB avec l'animation squelettique intégrée. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- Retopologisez d'abord : gardez le maillage de base sous 100 000 triangles avant le rigging automatique afin que les poids des sommets et la déformation des articulations restent cohérents. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- Contrôlez les articulations critiques : les épaules, les hanches et les doigts nécessitent souvent la correction de leurs poids de peau automatiques dans Blender ou Maya avant que le personnage n'entre dans un moteur de jeu. [Source](https://www.tripo3d.ai/blog/rigging-animation)
- Préparez avec les préréglages gratuits : testez d'abord avec la bibliothèque de mouvements gratuite, afin de ne consommer des crédits pour Text to Motion personnalisé que lorsque c'est nécessaire. [Source](https://www.tripo3d.ai/blog/rigging-animation)

### Preuves complémentaires {#additional-evidence_1}

- 2026-10-23 : les notes de version du post-traitement indiquent que les rigs exportés et les séquences text-to-motion sont livrés sous forme de pistes d'animation squelettique standard et éditables dans FBX et GLB. Elles peuvent être rétargetées dans Unreal Engine, Unity, Blender et les visionneuses WebGL. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- 2026-10-23 : la documentation technique indique que le rigging automatique positionne les articulations et applique des poids de peau initiaux issus de cartes de chaleur sur cinq hiérarchies squelettiques (UE5 Mannequin, Mixamo, VRM 1.0, Unity Humanoid, ActorCore). L'enchaînement de prompts permet jusqu'à cinq segments de mouvement consécutifs, chacun d'une durée maximale de 10 secondes. [Source](https://www.tripo3d.ai/blog/rigging-animation)

### Recommandations remplacées (conservées pour l'historique) {#superseded-guidance-retained-for-history_1}

- 2026-10-23 : riggier un personnage Tripo impliquait d'exporter le maillage statique vers Mixamo, Blender ou un outil similaire, puis de placer et pondérer le squelette à la main. [Source](https://www.tripo3d.ai/blog/rigging-animation)
- 2026-10-23 : animer des assets Tripo impliquait des bibliothèques de capture de mouvement tierces ou une animation par images-clés manuelle en dehors de Tripo Studio. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)

### Limites et questions ouvertes {#limits-and-open-questions_1}

- Tenue de la déformation dans le temps sur des modèles non humanoïdes ou quadrupèdes avec animation pilotée par texte.
- Benchmarks communautaires indépendants du poids de peau de Tripo Studio face au rigging automatique intégré aux outils DCC.
- Architecture du réseau de neurones et données d'entraînement derrière Text to Motion.

<!-- Retained base: d42a348223e0670592e2f1b683c46992af48130e; article blob: 990e6d08d55ddbad4d5d0b851ef0456aa73dd67f -->

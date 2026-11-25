---
title: "Adobe Firefly Video Model — Déploiement de Firefly Video Model"
category: projects
date: 2024-10-14
tags: [adobe-firefly-video-model, adobe_firefly, firefly-video-model-rollout, project]
aliases: ["Adobe Firefly Video", "Adobe Firefly Video Model"]
level: 3
source_sha256: bc85afd17b65aec9d8e00189b769a96375b2d09bb1993044fc9602322f9c1da0
translation: machine
translated_at: '2026-10-24'
---
# Adobe Firefly Video Model — Déploiement de Firefly Video Model {#adobe-firefly-video-model-firefly-video-model-rollout}

**Ligne de développement :** `project:adobe-firefly-video-model` · fil `firefly-video-model-rollout`  
**Dernier événement :** 2024-10-14 · 2 entrées datées depuis le 2024-09-11 · **Consulté le :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

Adobe Firefly Video Model génère de courts clips à partir de texte et d'images. Dans Generate video, il figure aux côtés de modèles partenaires ; nous sélectionnons donc Firefly Video explicitement.

- Text-to-Video et Image-to-Video avec première et dernière images clés.
- Contrôles du format d'image, de la résolution, de la taille de plan, de l'angle de caméra, du mouvement de caméra et du style.
- Export ou transfert des clips vers l'éditeur vidéo de Firefly et vers Premiere.

Les clips durent 5 secondes à 24 i/s, en 540p, 720p ou 1080p, avec des formats 16:9, 9:16 ou 1:1 ; une résolution plus élevée consomme davantage de crédits génératifs. Utilisez-le pour des plans prévus, des transitions et des plans de coupe (b-roll) ; assemblez les scènes plus longues dans un éditeur à partir de clips individuels.

## Ligne de développement {#development-line}

- **2024-09-11 — Adobe présente un futur modèle vidéo pour Firefly.** Le 2024-09-11, Adobe a annoncé qu'un modèle vidéo était prévu pour Firefly. Cette annonce a fixé l'orientation du produit avant que les utilisateurs n'aient accès à la génération vidéo.
- **2024-10-14 — Adobe lance une expérience bêta de génération vidéo dans Firefly.** Le 2024-10-14, Adobe a ouvert une expérience bêta de génération vidéo dans l'application web Firefly. Le modèle est ainsi passé du stade de l'annonce à celui des tests utilisateurs.

## Évolutions {#what-changed}

Adobe Firefly Video Model est passé d'une annonce initiale à une disponibilité générale au sein de l'interface Generate video multimodèle.

- **2024-09-11 :** Adobe a annoncé le modèle et ouvert une liste d'attente, en promettant Text-to-Video, Image-to-Video, images de référence et contrôles de caméra pour les plans de coupe et pour combler les lacunes éditoriales.
- **2024-10-14 :** Certains membres de la communauté sélectionnés ont obtenu un accès anticipé à l'application web Firefly, en appliquant Text-to-Video et Image-to-Video à des insertions et à de nouveaux éléments dans des séquences existantes.
- **2025-02-12 :** Lancement de la bêta publique dans la version mise à jour de l'application web Firefly, avec génération de texte et d'images, et 1080p dès le lancement.
- **2025-04-24 :** Adobe a fait passer Firefly Video Model à la disponibilité générale, en sortie de bêta.
- **2025-07-17 :** Adobe a amélioré la précision des mouvements, étendu les contrôles vidéo, ajouté la génération d'effets sonores et élargi le choix de modèles partenaires dans l'interface.
- **2026-08-18 à 2026-08-19 :** La documentation actuelle précise que Firefly Video est un choix de modèle explicite dans Generate video, tandis que l'espace de travail unifié de génération et d'édition reste en bêta.

## Mode d'emploi {#how-to-use-this}

Au 2024-10-14, les praticiens pouvaient considérer la génération vidéo Firefly comme un flux de travail en bêta, accessible via l'application web Firefly ; le 2024-09-11, il ne s'agissait que d'une capacité à venir.

1. Ouvrez Firefly, sélectionnez Video → Generate video, puis choisissez Firefly Video sous Model ; l'interface peut afficher Veo 3.1 par défaut au premier lancement.
  — <https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html>
2. Définissez la résolution, le format d'image, Shot size, Camera angle et Motion ; Firefly Video prend en charge 540p, 720p ou 1080p, et 16:9, 9:16 ou 1:1.
  — <https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html>
3. Rédigez un prompt selon l'ordre plan + sujet + action + lieu + esthétique, puis précisez le style et le mouvement de caméra.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
4. Pour une transition contrôlée, importez une première image, une dernière image, ou les deux ; si vous utilisez deux images, décrivez la transition dans le texte.
  — <https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html>
5. Générez le clip, puis téléchargez-le ou ajoutez-le à Project media, Timeline ou à l'éditeur de clips pour un assemblage ultérieur.
  — <https://helpx.adobe.com/firefly/web/unified-generation-and-editing-experience/generate-and-edit-content.html>
6. Vérifiez la consommation de crédits à l'aide du bouton situé à côté de Generate avant de lancer la génération ; le coût dépend de la résolution choisie.
  — <https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html>

## Bonnes pratiques {#best-practices}

- Rédigez des prompts précis : plan, sujet, action, lieu, lumière, couleur et style ; plus de quatre sujets perturbent souvent le modèle.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
- Décrivez l'action avec des verbes et un rythme, et définissez le mouvement de caméra dans le prompt ou dans le contrôle Camera.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
- Itérez à partir d'un prompt de base en ajoutant des détails selon une seule dimension, et conservez la seed, le prompt et les réglages pour obtenir des résultats similaires.
  — <https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html>
- Utilisez des images clés visuellement compatibles pour Image-to-Video et décrivez la transition ; une première image désactive certains contrôles manuels, et une dernière image désactive Motion.
  — <https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html>
- N'importez que des images dont vous avez les droits d'utilisation ; gardez l'onglet du navigateur ouvert et évitez de lancer des générations simultanément dans plusieurs onglets.
  — <https://helpx.adobe.com/cn/firefly/web/work-with-audio-and-video/work-with-video/about-generate-video.html>

## Informations remplacées {#superseded-by-this}

- 2024-09-11 : le statut « à venir » et réservé à la liste d'attente a pris fin avec la bêta publique du 2025-02-12 et la disponibilité générale du 2025-04-24.
- 2024-10-14 : l'accès anticipé pour certains membres de la communauté est obsolète ; l'accès au niveau du compte et la disponibilité générale du 2025-04-24 l'ont remplacé.
- 2025-02-12 : le statut de bêta publique est obsolète après la disponibilité générale du 2025-04-24.
- 2025-02-12 : l'engagement « 4K à venir » ne correspond pas à un réglage actuel de Firefly Video ; la documentation du 2026-08-18 répertorie 540p, 720p et 1080p pour ce flux de travail.

## Points non vérifiés {#still-unknown}

- Les modèles disponibles, Image-to-Video, les coûts en crédits et les droits d'accès des comptes n'ont pas été vérifiés sur un compte actif ; Adobe lie l'accès au forfait, à la région, au type d'utilisateur et aux limites réglementaires.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://blog.adobe.com/en/publish/2024/09/11/bringing-gen-ai-to-video-adobe-firefly-video-model-coming-soon | Apporter l'IA générative à la vidéo avec Adobe Firefly Video Model | Adobe Blog | 2026-09-04 |
| https://blog.adobe.com/en/publish/2024/10/14/generate-video-beta-on-firefly-web-app | Generate Video (bêta) sur l'application web Firefly | Adobe Blog | 2026-09-04 |
| https://blog.adobe.com/en/publish/2025/02/12/meet-firefly-video-model-ai-powered-creation-with-unparalleled-creative-control | Découvrez Firefly Video Model : création assistée par IA et contrôle créatif inégalé | Adobe Blog | 2026-09-04 |
| https://news.adobe.com/news/2025/04/adobe-revolutionizes-ai-assisted-creativity-firefly | Adobe révolutionne la création assistée par IA avec Firefly, le hub tout-en-un pour la création de contenus IA, avec de nouveaux modèles partenaires et Firefly | 2026-09-04 |
| https://blog.adobe.com/en/publish/2025/07/17/firefly-adds-new-video-capabilities-industry-leading-ai-models-generate-sound-effects-feature | Firefly ajoute de nouvelles capacités vidéo, des modèles d'IA de pointe et la fonction Generate Sound Effects | Adobe Blog | 2026-09-04 |
| https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html | Générer des vidéos à partir de prompts texte | Firefly | 2026-09-04 |
| https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html | Générer des vidéos à partir d'images | Firefly | 2026-09-04 |
| https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html | Rédiger des prompts texte efficaces pour la génération vidéo | Firefly | 2026-09-04 |
| https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html | Utiliser des préréglages de style pour la génération vidéo | Firefly | 2026-09-04 |
| https://helpx.adobe.com/firefly/web/unified-generation-and-editing-experience/generate-and-edit-content.html | Générer et éditer des images et des vidéos dans Firefly | Firefly | 2026-09-04 |
| https://helpx.adobe.com/cn/firefly/web/work-with-audio-and-video/work-with-video/about-generate-video.html | 生成视频常见问题 | Firefly | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:adobe-firefly-video-model`, fil `firefly-video-model-rollout`, 2 événements datés du 2024-09-11 au 2024-10-14.
- **Note pratique :** Au 2024-10-14, les praticiens pouvaient considérer la génération vidéo Firefly comme un flux de travail en bêta, accessible via l'application web Firefly ; le 2024-09-11, il ne s'agissait que d'une capacité à venir.
- **Confiance :** élevée. Les informations remplacées datées ci-dessus font foi pour ce qui est obsolète.

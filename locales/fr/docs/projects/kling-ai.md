---
title: "Kling AI"
category: projects
date: 2025-06-30
tags: [kling, kling-ai, kling-ai-product-development, kling_ai, model_releases, project]
aliases: ["Kling AI"]
level: 3
source_sha256: 572115ca523e3a4a75cffe62e0bc9dea799fa9bcbe236c701a01fdc63e2b18ae
translation: machine
translated_at: '2026-10-24'
---
# Kling AI {#kling-ai}

**Ligne de développement :** `project:kling-ai` · fil `kling-ai-product-development`  
**Dernier événement :** 2025-06-30 · 2 événements datés depuis le 2025-06-30 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Kling AI est la plateforme web et mobile de Kuaishou destinée à la création de vidéos commerciales, narratives et de personnages courtes.

- VIDEO 3.0 génère des vidéos à partir de texte et d'images, avec audio natif, séquences multi-plans et dialogues.
- VIDEO 3.0 Omni applique des références d'images, de vidéos et d'éléments pour maintenir des personnages ou des produits cohérents.
- Motion Control et Lip Sync transfèrent un mouvement ou ajoutent des dialogues à des personnages humains finalisés.

VIDEO 3.0 génère 3 à 15 secondes par passage ; Lip Sync exige un visage entièrement visible et exclut les animaux. Utilisez Kling pour des scènes courtes et contrôlées, avec références et son ; assemblez les vidéos longues à partir de plans vérifiés.

## Ligne de développement {#development-line}

- **2025-06-30 — Kling AI a exposé un workflow dédié de vidéo vers lèvres.** Le 2025-06-30, un lien daté pointait vers la page dédiée au workflow vidéo vers lèvres de Kling AI. Cela établit que le produit proposait alors la synchronisation labiale vidéo comme workflow distinct. Le lien seul ne permet pas d'établir sa date de lancement, ses détails fonctionnels, sa disponibilité ni son accès régional.
- **2025-06-30 — Kling AI a exposé un workflow dédié de vidéo vers audio.** Le 2025-06-30, un lien daté pointait vers la page dédiée au workflow vidéo vers audio de Kling AI. Cela établit que le produit proposait alors la génération audio à partir de vidéo comme workflow distinct. Le lien seul ne permet pas d'établir sa date de lancement, ses détails fonctionnels, sa disponibilité ni son accès régional.

## Évolutions {#what-changed}

2024-07-07 — La version web a lancé publiquement Kling avec images de début et de fin, contrôle de plans et génération texte-vers-vidéo jusqu'à 10 secondes.  
2024-09-20 — Kling AI 1.5 a ajouté la 1080p, Motion Brush et Lip Sync.  
2024-11-20 — Nous n'avons trouvé aucune version confirmée de Kling à cette date et laissons la gamme de modèles inchangée.  
2025-06-30 — Video-to-Audio a fait de la génération audio une voie autonome ; Video-to-Lip a été redirigé vers Lip Sync existant plutôt que vers un nouveau modèle.  
2026-02-04 — Kling 3.0 a unifié Video 3.0, Video 3.0 Omni, Image 3.0 et Image 3.0 Omni, en ajoutant jusqu'à 15 secondes, l'audio natif, les références et la génération multi-plans.

## Mode d'emploi {#how-to-use-this}

Au 2025-06-30, les praticiens doivent évaluer séparément les workflows vidéo vers lèvres et vidéo vers audio de Kling AI lorsqu'ils choisissent une voie de production ; leurs capacités détaillées et leur disponibilité doivent encore être vérifiées auprès des sources primaires.

1. Pour une nouvelle scène, ouvrez VIDEO 3.0, choisissez texte-vers-vidéo ou image-vers-vidéo, réglez la durée sur 3 à 15 secondes et activez Native Audio si le son doit être généré avec l'image.
  — <https://kling.ai/quickstart/klingai-video-3-model-user-guide>
2. Pour un personnage, un produit ou une séquence de plans récurrents, utilisez VIDEO 3.0 Omni : créez un Element à partir de 2 à 4 images ou d'une courte vidéo et utilisez-le comme référence.
  — <https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide>
3. Décrivez la scène en précisant le cadre, le sujet, l'action, le son, le style ou l'émotion, et la caméra ; placez les dialogues entre guillemets et associez-les au personnage qui parle.
  — <https://kling.ai/quickstart/klingai-video-26-audio-user-guide>
4. Pour des images existantes d'une personne, sélectionnez Lip Sync, importez ou générez la parole, et vérifiez les résultats avant publication.
  — <https://kling.ai/quickstart/ai-lip-sync-guide>
5. Pour un mouvement dirigé, importez une vidéo de mouvement et une image du personnage, ajoutez un Element facial si nécessaire, et vérifiez l'alignement de l'orientation.
  — <https://kling.ai/quickstart/motion-control-user-guide>

## Bonnes pratiques {#best-practices}

- Rédigez les prompts comme un bref de réalisateur : scène, sujet, mouvement, son et caméra, et non une accumulation d'adjectifs.
  — <https://kling.ai/quickstart/klingai-video-26-audio-user-guide>
- Utilisez plusieurs angles ou une courte vidéo de référence pour un visage cohérent ; une seule photo oblige le modèle à deviner les côtés non visibles.
  — <https://kling.ai/quickstart/motion-control-user-guide>
- Indiquez quel personnage prononce chaque réplique pour éviter les voix mélangées dans les dialogues.
  — <https://kling.ai/quickstart/klingai-video-3-model-user-guide>
- Utilisez uniquement des contenus possédés ou sous licence pour Voice Control ; fournissez 5 à 30 secondes d'un seul locuteur, avec un débit régulier et un bruit de fond minimal.
  — <https://kling.ai/quickstart/klingai-video-26-audio-user-guide>
- Fournissez une vidéo avec un visage humain entièrement visible pour Lip Sync, et adaptez la durée de l'audio à celle du clip.
  — <https://kling.ai/quickstart/ai-lip-sync-guide>

## Remplacé par {#superseded-by-this}

- 2024-07-07 — La limite de 10 secondes est obsolète pour VIDEO 3.0 : le guide actuel prévoit 3 à 15 secondes, l'audio natif et le multi-plans.
- 2024-09-20 — Kling 1.5 n'est plus la version de travail active ; Motion Brush et les premières versions de Lip Sync restent des fonctions héritées au sein de la famille 3.0.
- 2025-06-30 — Les nouvelles scènes sonores ne nécessitent plus de vidéo muette suivie d'un audio séparé : VIDEO 2.6 et 3.0 génèrent l'image, la parole, les effets et l'ambiance en une seule passe. Lip Sync autonome reste la voie pour doubler des clips finalisés.
- 2026-02-04 — L'avis d'accès anticipé réservé à Ultra reflétait un état de publication temporaire ; vérifiez le niveau d'abonnement et l'accès régional actuels depuis votre compte.

## Points inconnus {#still-unknown}

- L'entrée du 2024-11-20 ne peut pas être classée : le lien direct n'a renvoyé aucun texte, et aucune version primaire correspondante n'a été trouvée.
- Plusieurs pages originales de notes de version d'app.klingai.com n'étaient pas lisibles par machine ; nous avons recoupé leurs informations avec les communiqués officiels de Kuaishou et les guides de Kling.
- Les niveaux d'abonnement actuels, les crédits, la disponibilité régionale et l'accès à 3.0 Turbo, à la CLI et au MCP n'ont pas été vérifiés depuis un compte authentifié.
- Les sources primaires disponibles indiquent que Kling et Kling AI désignent le même produit de Kuaishou ; aucune entité distincte sous le nom court Kling n'est confirmée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-unveils-proprietary-video-generation-model-kling | Kuaishou Unveils Proprietary Video Generation Model 'Kling;' Testing Now Available | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-unveils-comprehensive-ai-models-reshaping-content-and/ | Kuaishou Unveils Comprehensive AI Models, Reshaping Content and Commercial Ecosystem with AI | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-launches-full-beta-testing-kling-ai-global-users-0 | Kuaishou Launches Full Beta Testing for ‘Kling AI’ to Global Users, Elevates Model Capabilities | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-technology-announces-third-quarter-2024-unaudited/ | Kuaishou Technology Announces Third Quarter 2024 Unaudited Financial Results | 2026-09-04 |
| https://www.hkexnews.hk/listedco/listconews/sehk/2026/0123/2026012300215.pdf | Kuaishou Technology offering memorandum | 2026-09-04 |
| https://www.youtube.com/watch?v=2N06IKlAVBU | King AI | Upgrades: Lip Sync, Kling Community & API Platform! | 2026-09-04 |
| https://www.youtube.com/watch?v=SqcM8-_lflU | Kling AI Now Comes with Video-to-Audio! Limited-Time Free Access — Try it now | 2026-09-04 |
| https://www.youtube.com/watch?v=6iRyO16mlvM | Introducing the KLING AI 1.6 Model | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-kling-ai-unveils-multi-image-reference-feature-further | Kuaishou Kling AI Unveils “Multi-Image Reference” Feature to Further Tackle AI Video Consistency Challenges | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-kling-ai-integrates-deepseek-lowering-entry-barrier-ai/ | Kuaishou Kling AI Integrates DeepSeek, Lowering the Entry Barrier for AI-Powered Creative Content | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-advances-20-era-empowering-everyone-tell-great-stories | Kling AI Advances to the 2.0 Era, Empowering Everyone to Tell Great Stories with AI | 2026-09-04 |
| https://cgworld.jp/flashnews/01-202506-Kling-21.html | 動画生成AI「Kling 2.1」リリース！ 1080p対応、ビジュアル品質や動きのダイナミクス、プロンプトの忠実性が向上 | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-25-turbo-video-model-industry-leading | Kling AI Launches 2.5 Turbo Video Model: Industry-Leading Performance, Now More Affordable | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kling-o1-launches-worlds-first-unified-multimodal-video-model-0 | Kling O1 Launches as the World’s First Unified Multimodal Video Model | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-video-26-model-simultaneous-audio-visual | Kling AI Launches Video 2.6 Model with "Simultaneous Audio-Visual Generation" Capability, Redefining AI Video Creation Workflow | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-30-model-ushering-era-where-everyone-can-be | Kling AI Launches 3.0 Model, Ushering in an Era Where Everyone Can Be a Director | 2026-09-04 |
| https://kling.ai/quickstart/klingai-video-3-model-user-guide | Kling VIDEO 3.0 Model User Guide | 2026-09-04 |
| https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide | Kling VIDEO 3.0 Omni Model User Guide | 2026-09-04 |
| https://kling.ai/quickstart/klingai-video-26-audio-user-guide | Kling Video 2.6 Audio User Guide | 2026-09-04 |
| https://kling.ai/quickstart/ai-lip-sync-guide | Kling AI Lip Sync Guide | 2026-09-04 |
| https://kling.ai/quickstart/motion-control-user-guide | Kling Motion Control User Guide | 2026-09-04 |
| https://kling.ai/blog/kling-ai-introduces-native-4k-video-model | Kling AI Introduces the World’s First Native 4K Video Model, Empowering Industrial-Grade AI Production Across Film, Advertising, and Creative Industries | 2026-09-04 |
| https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-technology-announces-second-quarter-and-interim-2026 | Kuaishou Technology Announces Second Quarter and Interim 2026 Unaudited Financial Results | 2026-09-04 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:kling-ai`, fil `kling-ai-product-development`, 2 événements datés du 2025-06-30 au 2025-06-30.
- **Note pratique :** Au 2025-06-30, les praticiens doivent évaluer séparément les workflows vidéo vers lèvres et vidéo vers audio de Kling AI lorsqu'ils choisissent une voie de production ; leurs capacités détaillées et leur disponibilité doivent encore être vérifiées auprès des sources primaires.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

---
title: "Ray 3.2 — Développement de Ray chez Luma AI"
category: projects
date: 2026-06-10
tags: [luma-ray, project, ray]
aliases: ["Ray 3.2"]
level: 2
source_sha256: 1ff3cca3123e45be15e2c71401126a9b0aa20e87295171f472aa428ff2696e75
translation: machine
translated_at: '2026-10-24'
---
# Ray 3.2 — Développement de Ray chez Luma AI {#ray-32-luma-ai-ray-development}

**Ligne de développement :** `project:ray` · fil `luma-ray`  
**Dernier événement :** 2026-06-10 · 1 événement daté depuis le 2026-06-10 · **Recherche :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

Ray 3.2 est le modèle vidéo de Luma destiné aux monteurs qui souhaitent conserver le mouvement de caméra réel, et aux développeurs qui veulent intégrer la génération vidéo.

- Modify Video dans l'application Luma : vidéo-vers-vidéo pilotée par la source, qui restylise un clip tout en conservant sa durée.
- `ray-3.2` dans l'API Agents : gère la génération texte-vers-vidéo, image-vers-vidéo, l'édition vidéo, l'extension et le recadrage (reframing).

La fonction vidéo-vers-vidéo de l'application exige une vidéo source et est limitée à 20 secondes ; les requêtes de génération via l'API durent 5 ou 10 secondes. Utilisez l'application lorsque le plan source est l'élément central. Utilisez l'API pour la génération ou l'édition automatisée. La restriction V2V de l'application ne s'applique pas à l'API.

## Ligne de développement {#development-line}

- **2026-06-10 — Luma AI présente Ray 3.2.** Le 2026-06-10, un lien daté de Luma AI a identifié Ray 3.2, au sein de la gamme de produits Ray, comme une mise à jour distincte de version. Les éléments disponibles ne permettent pas d'établir les capacités, la disponibilité ni les implications de migration de cette version.

## Changements {#what-changed}

- 2026-05-27 — Luma a publié des indications côté application pour Ray 3.2 Modify Video : V2V piloté par la source, sortie à durée exacte et direction artistique par images clés multiples.
- 2026-06-10 — L'événement de lancement de Ray3.2 a ajouté la direction par images clés multiples, l'EXR HDR/16 bits, Reframe et la première API à contrôle complet. L'annonce canonique de Luma est datée du 2026-06-09.
- 2026-07-13 — La page d'état actuel de Luma indique Ray3.2 comme modèle vidéo courant et marque Dream Machine et Ray2 comme obsolètes.

## Mode d'emploi {#how-to-use-this}

1. Dans l'application Luma, sélectionnez un élément vidéo et ouvrez Modify Video → Ray 3.2 pour le workflow V2V standard.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
2. Fournissez un clip source, puis décrivez l'état final souhaité et/ou joignez des images clés de guidage à des positions exactes de l'image source.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
3. Utilisez les contrôles Motion, Structure et character uniquement pour les propriétés qui doivent survivre au restylage ; itérez à plus basse résolution avant le rendu final.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
4. Pour une intégration, créez une clé API, soumettez des jobs `model: "ray-3.2"` vers `POST /v1/generations`, et choisissez `video`, `video_edit` ou `video_reframe` selon la tâche.
  — <https://docs.agents.lumalabs.ai/>
5. Interrogez `GET /v1/generations/{id}` jusqu'à obtenir `completed` ou `failed`, puis téléchargez la sortie terminée ; les URL de sortie présignées expirent au bout d'une heure.
  — <https://docs.agents.lumalabs.ai/guides/model/>

## Bonnes pratiques {#best-practices}

- Pour la V2V côté application, rédigez une description positive et concrète de l'état de la dernière image ; évitez les commandes, la négation et une nouvelle histoire temporelle, car le clip source fournit déjà le mouvement et le rythme.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
- Utilisez prompt et images clés pour une direction artistique délibérée, et placez les images clés aux moments source qui doivent conserver un rendu ou une composition donnés.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
- Explorez en mode Speed en 540p ou 720p, puis ne passez en Quality, 1080p, HDR ou EXR que la direction retenue, lorsque le pipeline de livraison l'exige.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
- Pour l'image-vers-vidéo via l'API, utilisez soit les ancres début/fin, soit les paires `keyframes` et `keyframe_indexes` ; les images clés multiples exigent des tableaux de même longueur avec des positions d'image uniques, et ne peuvent pas être combinées avec la voie à ancre unique.
  — <https://docs.agents.lumalabs.ai/guides/videos/generation/>

## Remplacé par cette version {#superseded-by-this}

- 2026-05-27 — Pour la transformation V2V ordinaire, le workflow Ray 3.14 Modify à début/fin seulement est remplacé par le workflow Ray 3.2 à images clés multiples arbitraires ; Ray 3.14 reste l'exception documentée pour les changements de durée ou les boucles.
- 2026-06-09 — Considérer Ray comme un outil réservé à l'application, sans API à contrôle complet, est obsolète pour Ray3.2.
- 2026-07-13 — Dream Machine et Ray2 sont obsolètes et ne constituent plus des choix courants de modèles vidéo Luma.

## Inconnues {#still-unknown}

- La date de l'événement du 2026-06-10 et l'annonce canonique de Luma du 2026-06-09 diffèrent d'un jour ; aucune source de première main n'explique cet écart, nous le traitons donc comme une correction de date et non comme un second lancement.
- L'URL fournie https://lumalabs.ai/ray3-2 n'a renvoyé aucun contenu exploitable lors de la vérification ; elle n'est donc pas utilisée comme source.
- Luma ne dispose d'aucun journal de modifications daté qui concilie le chiffre de 16 images clés par clip indiqué au lancement et sur la page d'état avec les workflows à 64 ancres de la documentation actuelle de l'application et de l'API ; les limites sont donc conservées propres à chaque surface.
- Nous n'avons trouvé aucune publication datée de première main d'un modèle ou d'une API Ray3.2 après le 2026-06-10 ; l'élément du 2026-07-13 est une mise à jour de la documentation d'état courant.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://lumalabs.ai/news/introducing-ray-3-2 | Luma présente Ray3.2 Model & API : contrôle créatif complet pour la génération vidéo | 2026-09-06 |
| https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video | Ray 3.2 Video to Video | Luma | 2026-09-06 |
| https://docs.agents.lumalabs.ai/guides/model/ | Models | Luma Agents | 2026-09-06 |
| https://docs.agents.lumalabs.ai/ | Quickstart | Luma Agents | 2026-09-06 |
| https://docs.agents.lumalabs.ai/guides/videos/generation/ | Video generation | Luma Agents | 2026-09-06 |
| https://lumalabs.ai/llm-info | Luma — Informations officielles pour les assistants IA | 2026-09-06 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:ray`, fil `luma-ray`, 1 événement daté, du 2026-06-10 au 2026-06-10.
- **Note pratique :** voir les sections d'usage et de pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

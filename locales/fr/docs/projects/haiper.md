---
title: "Haiper — Lancement public et disponibilité sur iOS"
category: projects
date: 2024-03-16
tags: [haiper, project, public-launch-and-ios-availability]
aliases: ["Haiper"]
level: 3
source_sha256: 94cad6e91839178a766287f4845f16c5760f9b23ec3d6bb6134040d1995b225e
translation: machine
translated_at: '2026-10-24'
---
# Haiper — Lancement public et disponibilité sur iOS {#haiper-public-launch-and-ios-availability}

**Ligne de développement :** `project:haiper` · fil `public-launch-and-ios-availability`  
**Dernier événement :** 2024-03-16 · 2 événements datés depuis 2024-03-13 · **Recherché le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Haiper était une plateforme vidéo en nuage destinée aux créateurs et aux intégrateurs, en concurrence directe avec Runway sur le text-to-video et l'image-to-video.

- Génération vidéo : text-to-video, image-to-video, conditionnement par images clés, video-to-video et text-to-image.
- Accès client : web, iOS et API HTTP (ancien).

La documentation 2.x publiée indique des sorties en 540p et 720p à raison de 5 à 8 crédits par seconde, mais ni un accès payant ni une nouvelle tâche achevée n'ont pu être vérifiés. Ne choisissez pas Haiper pour un nouveau flux de travail en production, et considérez l'API comme héritée tant qu'une tâche de test autorisée n'a pas abouti.

## Ligne de développement {#development-line}

- **2024-03-13 — Le site officiel de Haiper a été publiquement référencé.** Le service proposait une courte génération text-to-video gratuite, l'animation d'images et le repaint sur 2 secondes en HD, ou jusqu'à 4 secondes en qualité inférieure.
- **2024-03-16 — L'application iOS de Haiper a été publiquement liée.** Des liens publics renvoyaient vers la fiche de Haiper sur l'App Store d'Apple ainsi que vers des supports antérieurs de Haiper, à la date du 2024-03-16. Cela atteste une disponibilité ou une promotion publique de l'application iOS à cette date. Les éléments disponibles n'établissent ni les capacités de l'application, ni son statut de sortie, ni le texte de l'annonce qui l'accompagnait.

## Évolutions {#what-changed}

- 2024-03-13 — L'adresse web de Haiper est devenue le point d'entrée. La bêta publique proposait une courte génération text-to-video gratuite, l'animation d'images et le repaint sur 2 secondes en HD, ou jusqu'à 4 secondes en qualité inférieure.
- 2024-03-16 — Une URL de l'App Store s'est ajoutée à la voie web. Cela confirme un canal de distribution iOS dans les liens du produit, sans toutefois établir la date de sortie de l'application.
- 2024-10-21 — Haiper 2.0 et Templates ont étendu le produit, de la génération de base aux versions de modèles et à la création de vidéos à partir de modèles.
- 2024-12-18 — Haiper 2.5 a été lancé dans une intégration API avec VEED, orientant l'effort vers les flux de travail partenaires et API.
- 2025-03-20 — Microsoft a recruté deux cofondateurs de Haiper.
- 2025-06-23 — NetMind a racheté le modèle d'IA de Haiper, ce qui a transféré la propriété de la technologie.
- 2026-09-04 — Le domaine et la documentation de l'API restent en ligne, mais aucune nouvelle connexion, aucun paiement ni aucune génération achevée n'ont été vérifiés pour de nouveaux utilisateurs.

## Mode d'emploi {#how-to-use-this}

À partir du 2024-03-16, considérez que Haiper disposait d'une présence web publiquement référencée et d'un canal de distribution iOS, tout en vérifiant directement la disponibilité et les capacités actuelles avant de vous y fier.

1. Vérifiez que le fournisseur délivre effectivement une clé API après un rechargement. Si aucune clé n'arrive, arrêtez-vous : le chemin de lancement public reste non vérifié.
  — <https://docs.haiper.ai/api-reference/authentication>
2. Avec une clé valide, soumettez une seule tâche text-to-video au point de terminaison documenté et conservez le generation_id.
  — <https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video>
3. Interrogez l'état par generation_id. Traitez pending, processing, post_processing et failed comme des états distincts.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-status>
4. Ne demandez les résultats qu'après l'état succeed. Le point de terminaison de détail renvoie l'URL de la vidéo et les sorties.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-detail>

## Bonnes pratiques {#best-practices}

- Ne conservez pas l'unique copie d'une vidéo ou d'un projet dans le nuage de Haiper : des retours d'utilisateurs de début février 2025 signalent des pannes du site et des projets perdus après la fermeture.
  — <https://uk.trustpilot.com/review/haiper.ai>
- Passez explicitement is_public=false pour les ressources des clients : l'API publiée fixe la valeur par défaut à true.
  — <https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video>
- Intégrez les limites de débit dans votre client : la documentation plafonne le trafic à 500 requêtes HTTP par minute et 40 générations simultanées ; ne relancez pas aveuglément sur une réponse 429.
  — <https://docs.haiper.ai/api-reference/rate-limits>
- Ne demandez pas les détails avant que le statut ne renvoie succeed : interrogez d'abord le statut, puis le détail, afin d'éviter les faux succès et les liens vides.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-detail>

## Remplacé par ce qui suit {#superseded-by-this}

- 2024-03-05 — 2024-03-13 : le conseil de s'inscrire à la bêta grand public gratuite et de générer des vidéos dans l'application web est obsolète pour les nouveaux utilisateurs ; l'accès grand public n'est pas vérifié à la suite des événements de 2025.
- 2024-03-16 : le conseil d'installer l'application via l'URL d'origine de l'App Store est obsolète comme parcours d'accueil actif ; l'URL ne renvoyait aucune page produit en ligne lors de l'inspection.
- 2024-12-18 : l'annonce de l'API Haiper 2.5 avec VEED est une description historique de l'intégration, et non une preuve que l'API ou la voie partenaire accepte aujourd'hui de nouvelles tâches.
- Les tarifs historiques de la documentation publiée ne constituent pas une offre en vigueur tant que la délivrance de clé et une tâche réussie n'ont pas été confirmées.

## Toujours inconnu {#still-unknown}

- Haiper n'a publié aucune déclaration officielle datée concernant l'arrêt de son produit grand public ; la fermeture de février 2025 repose sur des témoignages d'utilisateurs et des sources secondaires, et non sur un avis de l'entreprise.
- Aucune tâche API autorisée n'a été exécutée et aucune nouvelle délivrance de clé n'a été vérifiée ; la documentation publiée pourrait donc être un artefact hérité et abandonné.
- L'URL d'origine de l'App Store ne renvoyait aucune fiche active lors de l'inspection ; son statut régional, un éventuel retrait et l'accessibilité pour les utilisateurs existants restent non confirmés.
- NetMind a confirmé l'achat du modèle, mais la question de savoir si NetMind le propose aujourd'hui à de nouveaux utilisateurs reste non vérifiée.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://haiper.ai/ | Haiper - Générateur de vidéos par IA | 2026-09-04 |
| https://apps.apple.com/app/id6468952574 | URL de l'App Store d'Apple, identifiant d'application 6468952574 | 2026-09-04 |
| https://techcrunch.com/2024/03/05/competition-in-ai-video-generation-heats-up-as-deepmind-alums-unveil-haiper/ | Competition in AI video generation heats up as DeepMind alums unveil Haiper | 2026-09-04 |
| https://testapp.haiper.ai/home | Unlock Creativity with AI Content Generator Tools \| Haiper | 2026-09-04 |
| https://testapp2.haiper.ai/blog/haiper-partners-with-veed | Haiper Launches Its 2.5 Model-Powered API with VEED | 2026-09-04 |
| https://sifted.eu/articles/microsoft-haiper-ai-hires-video-sora-inflection/ | Exclusive: Microsoft scoops up talent from AI video startup Haiper | 2026-09-04 |
| https://sifted.eu/articles/haiper-ai-sold-for-parts | Exclusive: Haiper AI sold for parts after Microsoft poaches cofounders | 2026-09-04 |
| https://uk.trustpilot.com/review/haiper.ai | Haiper Reviews \| Read Customer Service Reviews of haiper.ai | 2026-09-04 |
| https://docs.haiper.ai/llms.txt | Index de la documentation Haiper | 2026-09-04 |
| https://docs.haiper.ai/pricing | Pricing for Haiper Web App & iOS App - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/authentication | Authentication - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video | Text to Video - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/get-creation-status | Get Creation Status - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/get-creation-detail | Get Creation Detail - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/rate-limits | Rate Limits - Haiper | 2026-09-04 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:haiper`, fil `public-launch-and-ios-availability`, 2 événements datés du 2024-03-13 au 2024-03-16.
- **Note pratique :** À partir du 2024-03-16, les praticiens doivent considérer que Haiper disposait d'une présence web publiquement référencée et d'un canal de distribution iOS, tout en vérifiant directement la disponibilité et les capacités actuelles avant de s'y fier.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.

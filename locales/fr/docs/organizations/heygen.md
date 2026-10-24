---
title: "HeyGen"
category: organizations
date: 2025-05-07
tags: [avatar-platform-and-developer-integration, heygen, heygen_avatars, heygen_video_translate, organization]
aliases: ["HeyGen"]
level: 3
source_sha256: 0960a5bd0a3ef31fd1acd526363e544c3affbd4284b594462291933410fa4634
translation: machine
translated_at: '2026-10-24'
---
# HeyGen {#heygen}

**Ligne de développement :** `organization:heygen` · fil `avatar-platform-and-developer-integration`  
**Dernier événement :** 2025-05-07 · 2 entrées datées depuis 2024-07-12 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

HeyGen est une plateforme vidéo destinée aux équipes et aux développeurs, permettant de créer des vidéos à base d'avatars, des vidéos traduites et des vidéos pilotées par prompt.

- AI Studio : modifie le script, l'avatar, la voix, les scènes, le timing et les ressources.
- Digital Twins et Photo Avatars : génèrent une vidéo à partir de séquences filmées ou d'images fixes.
- Video Translation et Video Agent : traduisent des séquences et construisent des vidéos via API, CLI ou MCP.

## Ligne de développement {#development-line}

- **2024-07-12 — HeyGen a partagé une fonctionnalité Expressive Photo Avatar.** Le 2024-07-12, une URL de HeyGen Labs renvoyait vers Expressive Photo Avatar. La page signale une nouvelle surface pour les avatars. Le lien seul ne confirme ni le statut de publication, ni la disponibilité, ni le comportement.
- **2025-05-07 — HeyGen a partagé des ressources développeur pour le serveur MCP.** Le 2025-05-07, des liens renvoyaient vers les avatars HeyGen, la documentation du serveur MCP et le dépôt heygen-com/heygen-mcp. Cela a ajouté une intégration MCP pour développeurs à la plateforme d'avatars. Les pages n'indiquent ni la couverture fonctionnelle, ni la version, ni le niveau de maturité.

## Évolutions {#what-changed}

Le produit est passé de points d'entrée centrés sur les avatars et les modèles vers Studio, la traduction, les moteurs d'avatars et l'accès développeur.

- 2023-08-10 — des liens renvoyaient vers la page d'accueil et vers une destination Typeform. Le formulaire n'a renvoyé aucun contenu exploitable ; son lancement ou son programme reste donc inconnu.
- 2023-09-08 — une entrée de traduction vidéo pointait vers une route de modèle invité. Cette route ne s'affiche plus ; elle indique une orientation de traduction et non la publication d'une fonctionnalité.
- 2024-03-25 — une entrée pointait vers la page d'accueil de l'application, sans fonctionnalité nommée récupérable.
- 2024-07-12 — HeyGen Labs exposait une route Expressive Photo Avatar. La page ne fournit aucun contenu ; le statut de l'expérimentation et ses limites restent non vérifiés.
- 2024-12-13 — aucune source publique exploitable n'a survécu ; nous ne formulons donc aucune affirmation.
- 2025-05-07 — une route de documentation MCP et un dépôt GitHub ont rejoint la page des avatars. Il s'agit du premier marqueur d'intégration d'agent.
- 2026-04-13, trouvé aujourd'hui — HeyGen a annoncé des outils développeur pour Video Agent, la génération de vidéos, la traduction et les API de lipsync.
- 2026-04-15, trouvé aujourd'hui — HeyGen a présenté Avatar V, en séparant les avatars vidéo Avatar V des workflows fondés sur des photos.
- 2026-04-28, trouvé aujourd'hui — HyperFrames a annoncé un framework vidéo open source en HTML, CSS et JavaScript destiné aux agents IA.
- 2026-09-04, trouvé aujourd'hui — Remote MCP utilise désormais OAuth avec un forfait HeyGen existant, et l'accès direct à l'API reste ouvert.

## Mode d'emploi {#how-to-use-this}

Depuis le 2025-05-07, évaluez la documentation et le dépôt du serveur MCP en parallèle de l'application web, afin de ne pas supposer que les workflows se limitent au navigateur. Testez séparément la capacité et le niveau de maturité avant toute mise en production.

1. Pour un présentateur à partir d'une image fixe, ouvrez Avatars, choisissez New Avatar, puis Upload Photo ou Design with AI ; donnez-lui un nom et attendez la validation avant de l'utiliser dans Studio.
  — <https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars>
2. Pour un présentateur personnel réutilisable, utilisez Avatars → Create New Avatar → Digital Twin, enregistrez ou importez une séquence, puis faites compléter à la personne représentée la vidéo de consentement.
  — <https://help.heygen.com/en/articles/12089286-create-your-first-digital-twin-video-avatar-with-avatar-iv>
3. Dans AI Studio, choisissez l'avatar et la voix, rédigez les scènes du script, prévisualisez la voix, ajustez les pauses et le timing, puis soumettez la vidéo finale à la génération.
  — <https://help.heygen.com/en/articles/11049837-create-your-first-video-in-our-studio>
4. Pour la localisation, importez un fichier MP4, MOV ou WEBM, une URL YouTube prise en charge, une URL Google Drive ou un projet existant ; sélectionnez les langues source et cible, choisissez le moteur de traduction, soumettez, puis vérifiez le résultat.
  — <https://help.heygen.com/en/articles/10029081-how-to-get-started-with-video-translation>
5. Pour l'automatisation, détectez d'abord un chemin MCP, CLI ou API authentifié ; utilisez Video Agent pour le travail courant de prompt vers vidéo, et une URL de rappel (callback) pour les tâches de production.
  — <https://developers.heygen.com/docs/for-ai-agents>

## Bonnes pratiques {#best-practices}

- Enregistrez les séquences de Digital Twin en une seule prise continue et stable, avec un bon éclairage, un visage visible et un son propre ; évitez les coupes, les grands mouvements de tête, les vêtements chargés et la dérive de la caméra.
  — <https://help.heygen.com/en/articles/8389138-digital-twin-video-avatar-filming-tips>
- Utilisez une image Photo Avatar nette, de face, avec des yeux et des lèvres bien visibles ; créez-la comme avatar, et non comme ressource de Studio.
  — <https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars>
- Prévisualisez la voix et les scènes individuelles avant le rendu complet, afin de ne pas gaspiller de crédits en rendus refaits.
  — <https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits>
- Choisissez délibérément la voie de l'avatar : Avatar V gère les rendus vidéo, tandis qu'Avatar IV gère les rendus photo. Corrigez les séquences source plutôt que de retoucher un mauvais rendu.
  — <https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits>
- Fournissez à la traduction une source monolingue, sélectionnez la variante de langue visée, et vérifiez avec la relecture du script ou les indications SRT. Recréez les vidéos dans Studio lorsque le texte à l'écran doit changer.
  — <https://help.heygen.com/en/articles/10029081-how-to-get-started-with-video-translation>
- Pour les intégrations d'agents, vérifiez l'authentification avant de développer, ne retenez qu'une seule voie parmi MCP, CLI ou API, et utilisez des callbacks plutôt qu'un polling sans fin en production.
  — <https://developers.heygen.com/docs/for-ai-agents>

## Remplacé par {#superseded-by-this}

- 2023-09-08 — ne vous appuyez pas sur l'ancienne URL de modèle invité comme workflow actuel ; elle ne s'affichait pas lors de la vérification, alors que les flux actuels de Studio et de Video Translation sont documentés.
- 2024-07-12 — la route Labs Expressive Photo Avatar n'est pas une référence d'exploitation actuelle ; utilisez Avatars → New Avatar → Upload Photo ou Design with AI, puis Studio.
- 2025-05-07 — considérez l'ancienne route MCP de docs.heygen.com et le dépôt heygen-com/heygen-mcp comme des points de repère historiques, et non comme des instructions de configuration ; le Remote MCP actuel utilise OAuth, et le guide des agents choisit MCP, CLI ou API après authentification.
- Avant le 2026-04-15 — les recommandations génériques sur les moteurs d'avatars sont désormais incomplètes : la documentation actuelle distingue Avatar V pour les rendus vidéo d'Avatar IV pour les workflows fondés sur des photos.

## Inconnues {#still-unknown}

- La destination Typeform de 2023, la destination de modèle invité, la destination Labs de 2024 et les points de terminaison MCP historiques de 2025 ne renvoient plus de contenu exploitable lors de cette vérification ; leur périmètre fonctionnel initial et leur statut de lancement restent non vérifiés.
- L'entrée du 2024-12-13 ne dispose d'aucune URL publique conservée ; aucune affirmation sur une évolution du produit ne peut donc être faite pour cette date.
- HeyGen est un sujet au niveau de l'entreprise, alors qu'Avatars, la traduction, Video Agent et HyperFrames sont des lignes de produits distinctes. L'étiquette générique HeyGen ne constitue donc pas un historique fiable d'un seul produit.
- Le matériel actuel sur Remote MCP n'indique ni quand ni comment la documentation MCP héritée de 2025 et le dépôt ont été migrés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.heygen.com/ | HeyGen : créez en quelques minutes des vidéos IA réalistes de vous-même | 2026-09-04 |
| https://www.heygen.com/model-context-protocol | Intégration IA contextuelle \| Solutions vidéo IA \| HeyGen | 2026-09-04 |
| https://developers.heygen.com/docs/for-ai-agents | For AI Agents - Documentation HeyGen | 2026-09-04 |
| https://help.heygen.com/en/articles/11049837-create-your-first-video-in-our-studio | Create your first video in our Studio! \| Centre d'aide HeyGen | 2026-09-04 |
| https://help.heygen.com/en/articles/12089286-create-your-first-digital-twin-video-avatar-with-avatar-iv | Create your first Digital Twin (Video Avatar) with Avatar IV! \| Centre d'aide HeyGen | 2026-09-04 |
| https://help.heygen.com/en/articles/12092609-recording-your-consent-video | Recording your Consent Video \| Centre d'aide HeyGen | 2026-09-04 |
| https://help.heygen.com/en/articles/8389138-digital-twin-video-avatar-filming-tips | Digital Twin (Video Avatar) : conseils de tournage \| Centre d'aide HeyGen | 2026-09-04 |
| https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars | How to Get Started with Photo Avatars \| Centre d'aide HeyGen | 2026-09-04 |
| https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits | FAQ Avatar et voix : dépannage, bonnes pratiques et crédits \| Centre d'aide HeyGen | 2026-09-04 |
| https://help.heygen.com/en/articles/10029081-how-to-get-started-with-video-translation | How to Get Started with Video Translation \| Centre d'aide HeyGen | 2026-09-04 |
| https://am8evw00qys.typeform.com/to/wauwjUYP?typeform-source=t.co | Destination Typeform historique de l'entrée avatar de 2023 ; contenu indisponible à la lecture | 2026-09-04 |
| https://app.heygen.com/guest/templates?cid=d9a269e9 | Destination de modèles invités HeyGen ; contenu indisponible à la lecture | 2026-09-04 |
| https://app.heygen.com/home | HeyGen - Créateur de vidéos avec porte-parole IA | 2026-09-04 |
| https://labs.heygen.com/expressive-photo-avatar | HeyGen Labs | 2026-09-04 |
| https://app.heygen.com/avatars | HeyGen - Créateur de vidéos avec porte-parole IA | 2026-09-04 |
| https://docs.heygen.com/docs/heygen-mcp-server | Point de terminaison de documentation historique du serveur MCP HeyGen ; contenu indisponible à la lecture | 2026-09-04 |
| https://github.com/heygen-com/heygen-mcp | Point de terminaison historique du dépôt heygen-com/heygen-mcp ; contenu indisponible à la lecture | 2026-09-04 |

## Synthèse pour agents {#agent-brief}

- **Sujet :** `organization:heygen`, fil `avatar-platform-and-developer-integration`, 2 événements datés du 2024-07-12 au 2025-05-07.
- **Note pratique :** depuis le 2025-05-07, évaluez la documentation publiée du serveur MCP et le dépôt en parallèle de l'application web, plutôt que de supposer que les workflows se limitent au navigateur ; la capacité et le niveau de maturité en production doivent encore faire l'objet d'une vérification distincte.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

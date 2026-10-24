---
title: "Sonilo"
category: projects
date: 2026-06-29
tags: [project, sonilo, sonilo-v1-1]
aliases: ["Sonilo"]
level: 3
source_sha256: 52b6247125f3ed7ffabbd2966aab27dd62b7aa7fd05f9648a5d48ffd3a305d7a
translation: machine
translated_at: '2026-10-24'
---
# Sonilo {#sonilo}

**Ligne de développement :** `project:sonilo` · fil `sonilo-v1-1`  
**Dernier événement :** 2026-06-29 · 1 daté depuis le 2026-06-29 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Sonilo est un outil audio orienté API, destiné aux monteurs, aux équipes de produits créatifs et aux développeurs qui ont besoin de musique ou de sons synchronisés sur un montage.

- génère de la musique à partir d'un texte ou d'une vidéo ;
- génère des effets sonores guidés par un texte ou une vidéo ;
- mixe une voix et une musique fournies, avec ducking automatique.

## Ligne de développement {#development-line}

- **2026-06-29 — Sonilo v1.1 relié à un point d'accès texte-vers-musique.** Il offre un alignement plus serré entre la vidéo et la musique, préserve la parole d'origine et ajoute des prompts par segment. La version officielle elle-même est datée du 2026-06-18.

## Ce qui a changé {#what-changed}

2026-06-29 — Sonilo v1.1 offre un alignement plus serré entre la vidéo et la musique, préserve la parole d'origine et ajoute des prompts par segment. La version officielle elle-même est datée du 2026-06-18.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-06-29, nous considérons Sonilo v1.1 comme un point d'accès candidat distinct à évaluer via la route texte-vers-musique liée et la plateforme Sonilo, sans présumer de ses capacités ni des exigences de migration tant que les pages sources n'ont pas été étudiées.

1. Créez une clé API, conservez-la côté serveur et ajoutez le solde API requis avant de tenter une génération.
  — <https://platform.sonilo.com/docs/quickstart>
2. Vérifiez au préalable les services activés et l'usage du compte, puis choisissez texte-vers-musique pour un brief musical ou vidéo-vers-musique pour une timeline visuelle verrouillée.
  — <https://platform.sonilo.com/docs/api>
3. Pour une génération directe à partir de texte, envoyez en POST un prompt et une durée de 5 à 360 secondes vers /v1/text-to-music.
  — <https://platform.sonilo.com/docs/text-to-music>
4. Consommez les fragments audio streamés uniquement via l'événement complet, ou utilisez le mode asynchrone et interrogez l'identifiant de tâche renvoyé jusqu'à un état terminal.
  — <https://platform.sonilo.com/docs/text-to-music>
5. Si le produit utilise déjà fal, appelez le modèle texte v1.1 à l'adresse sonilo/v1.1/text-to-music plutôt que de construire une intégration fournisseur distincte.
  — <https://fal.ai/models/sonilo/v1.1/text-to-music>

## Bonnes pratiques {#best-practices}

- Conservez les clés API dans une variable d'environnement côté serveur. Révoquez et remplacez une clé exposée plutôt que de l'intégrer dans une application cliente.
  — <https://platform.sonilo.com/docs>
- Traitez 401, 402, 403 et 429 comme des conditions distinctes de configuration, de solde, d'accès aux services et de temporisation. Ne créez pas d'audio de substitution après une requête échouée.
  — <https://platform.sonilo.com/docs/text-to-music>
- Utilisez une entrée vidéo lorsque le timing, les coupes ou l'espace vocal doivent guider la bande son. Utilisez une entrée texte lorsque la tâche est un signal musical autonome.
  — <https://platform.sonilo.com/docs/api>
- Pour un travail payant ou client, vérifiez la piste générée par rapport à la voix off et aux changements de plan, conservez le fichier de sortie et le registre du compte, et confirmez que le forfait actuel couvre la diffusion visée.
  — <https://sonilo.com/blog/ai-music-video-creators-2026>

## Remplacé par ces éléments {#superseded-by-this}

- 2026-06-18 — Pour la musique de film qui exige des dialogues préservés ou une direction propre à chaque scène, v1.1 remplace la génération de type v1.0 dépourvue de ces contrôles. La version ne précise pas que les points d'accès v1.0 ont été retirés.
- 2026-08-03 — Lorsqu'un projet dispose déjà de pistes voix et musique séparées, le point d'accès de ducking audio documenté remplace le réglage manuel du volume, à condition que son flux à deux entrées corresponde au besoin.

## Toujours inconnu {#still-unknown}

- L'événement fourni est daté du 2026-06-29, tandis que la page de version de Sonilo date v1.1 du 2026-06-18 ; aucune source primaire trouvée n'explique cet écart de onze jours.
- Les chiffres de comparaison de v1.1 sont communiqués par le fournisseur ; aucun protocole d'évaluation public ni reproduction indépendante n'a été trouvé.
- Le point d'accès texte direct de Sonilo documente un plafond de 360 secondes, tandis que le point d'accès texte v1.1 de fal documente 600 secondes ; considérez les limites comme propres à chaque route tant qu'elles ne sont pas confirmées pour le compte visé.
- Aucune source primaire publique consultée lors de cette passe ne déclare un modèle successeur à v1.1.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://sonilo.com/news/sonilo-v1-1 | Présentation de Sonilo v1.1 | Sonilo | 2026-09-05 |
| https://fal.ai/models/sonilo/v1.1/text-to-music | Sonilo V1.1 Text to Music (Text to Audio) API sur fal | 2026-09-05 |
| https://platform.sonilo.com/ | Sonilo API — API de musique IA pour entreprises | 2026-09-05 |
| https://platform.sonilo.com/docs | Introduction · Documentation Sonilo | 2026-09-05 |
| https://platform.sonilo.com/docs/quickstart | Démarrage rapide · Documentation Sonilo | 2026-09-05 |
| https://platform.sonilo.com/docs/text-to-music | Text to Music · Documentation Sonilo | 2026-09-05 |
| https://platform.sonilo.com/docs/api | Référence de l'API | 2026-09-05 |
| https://sonilo.com/zh-CN/news/sonilo-v1 | Présentation de Sonilo v1.0 | Sonilo | 2026-09-05 |
| https://sonilo.com/blog/sonilo-comfyui | Nouvelle annonce : Sonilo est désormais disponible sur ComfyUI ! | Sonilo | 2026-09-05 |
| https://sonilo.com/blog/product/audio-ducking-api-guide | Audio Ducking API : mixer automatiquement voix et musique | Sonilo | 2026-09-05 |
| https://sonilo.com/blog/ai-music-video-creators-2026 | Musique IA sous licence pour YouTube, les publicités et les vidéos clients (guide 2026) | Sonilo | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:sonilo`, fil `sonilo-v1-1`, 1 événement daté du 2026-06-29 au 2026-06-29.
- **Note pratique :** À partir du 2026-06-29, nous considérons Sonilo v1.1 comme un point d'accès candidat distinct à évaluer via la route texte-vers-musique liée et la plateforme Sonilo, sans présumer de ses capacités ni des exigences de migration tant que les pages sources n'ont pas été étudiées.
- **Confiance :** moyenne. Les mentions « remplacé par » datées font autorité pour déterminer ce qui est obsolète.

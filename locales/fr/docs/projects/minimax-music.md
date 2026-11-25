---
title: "MiniMax Music"
category: projects
date: 2025-10-31
tags: [minimax-music, minimax-music-development, model_releases, project]
aliases: ["MiniMax Music", "MiniMax Music 2.0"]
level: 3
source_sha256: 51fbd4abecf5411ce4705edfaeda58d160327280bac24cd7703d63875219e185
translation: machine
translated_at: '2026-10-24'
---
# MiniMax Music {#minimax-music}

**Ligne de développement :** `project:minimax-music` · fil `minimax-music-development`  
**Dernier événement :** 2025-10-31 · 1 événement daté depuis 2025-10-31 · **Recherche :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

MiniMax Music produit des chansons complètes à partir de paroles et d'une consigne de style, pour les créateurs et les équipes de développement.

- Chansons vocales à partir de prompts textuels et de paroles.
- Musique instrumentale sans parties vocales.
- Reprises à partir de fichiers audio de référence.
- Service local via des poids ouverts pour Music 3.

L'accès API payant nouveau pour Music et Lyrics a pris fin le 2026-08-20, et Music 3 en local exige CUDA avec 24 Go de VRAM ou plus sur le chemin Diffusers complet. Commencez par MiniMax Audio ou auto-hébergez Music 3 si vous débutez ; ne conservez le chemin API que si vous êtes déjà un client payant.

## Ligne de développement {#development-line}

- **2025-10-31 — La génération musicale MiniMax Music est devenue disponible via des points de terminaison de modèles documentés.** MiniMax a lancé, le 2025-10-31, une page produit officielle et une référence API pour la génération musicale. Un point de terminaison de modèle hébergé sur fal.ai a offert une autre voie d'accès pour les développeurs à la même date.

## Évolutions {#what-changed}

- 2025-10-31 — MiniMax Music 2.0 a été lancé avec des voix plus naturelles, des exemples multi-voix/a cappella, un contrôle des instruments et des morceaux pouvant atteindre cinq minutes.
- 2026-01-28 — MiniMax Music 2.5 a ajouté un contrôle des sections au niveau du paragraphe, 14 variations structurelles, plus de 100 instruments et un mixage mis à jour.
- 2026-02-09 — Aucun corps de source récupérable de manière indépendante n'établit une version distincte de MiniMax Music ni une modification de ses capacités à cette date.
- 2026-03-04 — MiniMax Music 2.5+ a ajouté la génération instrumentale seule, élargissant la gamme au-delà de la création de chansons vocales.
- 2026-03-18 — Music-2.6 est apparu dans les notes de version officielles des modèles comme mise à jour musicale/reprise ; la documentation actuelle le présente comme le modèle texte-vers-musique de la génération précédente.
- 2026-08-13 — MiniMax Music 3.0 est devenu la version de nouvelle génération à poids ouverts pour des chansons complètes pouvant atteindre cinq minutes.
- 2026-08-20 — Les nouveaux utilisateurs payants des API Music et Lyrics ont été coupés et les API de génération musicale gratuites ont été arrêtées ; les clients payants existants ont conservé l'accès.

## Mode d'emploi {#how-to-use-this}

Avant de choisir une voie d'intégration à partir du 2025-10-31, consultez la documentation officielle de l'API de génération musicale et les points de terminaison de modèles hébergés pris en charge.

1. Choisissez d'abord la voie d'accès : en tant que nouvel utilisateur, utilisez MiniMax Audio ou auto-hébergez Music 3 ; l'accès API payant nouveau pour Music/Lyrics est fermé et les points de terminaison gratuits sont arrêtés. Les clients API payants existants peuvent continuer.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
2. En tant qu'utilisateur API payant existant, envoyez un JSON avec une authentification Bearer vers POST /v1/music_generation et sélectionnez music-3.0, marqué comme recommandé dans la référence.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
3. Décrivez le genre, l'ambiance et le scénario dans prompt ; transmettez des paroles découpées en sections dans lyrics, ou définissez lyrics_optimizer=true lorsque les paroles sont absentes. Définissez is_instrumental=true pour une piste sans voix.  
  — <https://platform.minimax.io/docs/guides/music-generation>
4. Pour une reprise, sélectionnez music-cover et fournissez exactement une URL d'audio de référence ou une charge utile en base64 ; la référence acceptée dure de 6 secondes à 6 minutes et pèse au maximum 50 Mo.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
5. Pour Music 3 en local, téléchargez MiniMaxAI/MiniMax-Music3 et servez-le avec SGLang-Omni. Placez les paroles dans input et la description musicale dans instructions ; Diffusers et ComfyUI sont également pris en charge.  
  — <https://huggingface.co/MiniMaxAI/MiniMax-Music3>

## Bonnes pratiques {#best-practices}

- Gardez les indications musicales dans prompt et le texte des paroles dans lyrics. Utilisez les balises de section documentées pour contrôler l'arrangement, plutôt que de mêler des indications au corps des paroles.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
- Lorsque vous ne fournissez pas de paroles, définissez lyrics_optimizer ; lorsque vous voulez une piste sans voix, définissez explicitement is_instrumental et omettez lyrics.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
- Téléchargez un résultat au format URL dans les 24 heures, ou utilisez la sortie hex en cas de streaming, car le streaming ne prend en charge que hex.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
- Pour Music 3 en local, décrivez en détail les métadonnées globales, les détails vocaux et l'arrangement. Placez les balises de paroles sur leurs propres lignes, et considérez le tempo, la tonalité, l'instrumentation et la structure demandés comme des contrôles génératifs et non comme des garanties.  
  — <https://huggingface.co/MiniMaxAI/MiniMax-Music3>
- Vérifiez la capacité locale avant de charger Music 3 : CUDA est requis ; le chemin Diffusers direct documenté tient dans 24 Go de VRAM ou plus, tandis que le déchargement CPU/par couches tient dans 8 Go mais est plus lent.  
  — <https://huggingface.co/MiniMaxAI/MiniMax-Music3>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-08-13 — MiniMax Music 2.0 comme modèle musical MiniMax par défaut actuel.
- 2026-03-04 — La directive selon laquelle MiniMax Music exige toujours des voix et des paroles fournies.
- 2026-08-13 — Music-2.6 comme modèle API texte-vers-musique recommandé.
- 2026-08-20 — La directive demandant aux nouveaux utilisateurs de s'inscrire à l'API Music payante ou d'utiliser Music-3.0-free, Music-2.6-free ou music-cover-free.

## Points inconnus {#still-unknown}

- L'ensemble de sources du 2026-02-09 n'établit pas une version distincte de MiniMax Music : la page WeChat n'a pas pu être récupérée et la page X n'exposait aucun corps de publication ; elle ne peut donc pas être assimilée en toute sécurité à Music 2.5 ou à une autre version.
- La référence API conserve des exemples de modèles et des noms de modèles gratuits à côté de l'avis de fermeture du 2026-08-20 ; la poursuite pour les clients existants est indiquée, mais les nouvelles inscriptions et les voies de droits n'ont pas été testées de manière indépendante.
- La tarification actuelle de MiniMax Audio, la disponibilité régionale, les licences commerciales et les quotas du produit web n'ont pas été vérifiés. Le chiffre de 0,03 $ de fal ne s'applique qu'à son propre point de terminaison v2.
- La fiche Music3 indique qu'aucun Hugging Face Inference Provider n'héberge le modèle ; une voie d'inférence hébergée et gérée au-delà de MiniMax Audio n'a pas été vérifiée.

## Sources {#sources}

| source | title | lu |
|---|---|---|
| https://www.minimax.io/audio/music | MiniMax Audio | AI Music Generator | 2026-09-04 |
| https://www.minimax.io/news/minimax-music-20 | Making Music Creation Accessible to Everyone - MiniMax News | MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/music-generation | Music Generation - MiniMax API Docs | 2026-09-04 |
| https://fal.ai/models/fal-ai/minimax-music/v2 | MiniMax Music 2.0: State of the Art AI Text-to-Music Generator | fal | 2026-09-04 |
| https://mp-weixin-qq-com.translate.goog/s/hy1RzvAytRSxX63qodEExw?_x_tr_sl=zh-CN&_x_tr_tl=en&_x_tr_hl=en | WeChat article via Google Translate (titre indisponible) | 2026-09-04 |
| https://x.com/wavespeed_ai/status/2020165909646586220?s=20 | WaveSpeed AI X post 2020165909646586220 (corps indisponible) | 2026-09-04 |
| https://www.minimax.io/news/minimax-music-25 | MiniMax Music 2.5: Breakthrough Across All Dimensions — Direct the Detail. Define the Real - MiniMax News | MiniMax | 2026-09-04 |
| https://www.minimax.io/news/minimax-music-25-2 | MiniMax Music 2.5+: Unlock instrumental music, break through style boundaries. - MiniMax News | MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/release-notes/models | Models - MiniMax API Docs | 2026-09-04 |
| https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model | MiniMax Music 3.0: Next-Generation Open-Weights, Production-Ready & Versatile Music Model - MiniMax Research | MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/guides/music-generation | Music Generation - MiniMax API Docs | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-Music3 | MiniMaxAI/MiniMax-Music3 · Hugging Face | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:minimax-music`, fil `minimax-music-development`, 1 événement daté, du 2025-10-31 au 2025-10-31.
- **Note pratique :** Consultez la documentation API officielle de MiniMax et les points de terminaison hébergés avant de choisir une voie d'intégration à partir du 2025-10-31.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

---
title: "claude-video"
category: projects
date: 2026-07-27
tags: [claude-video, claude-video-development, claude_video, project]
aliases: ["claude-video", "claude-video (watch)"]
level: 2
source_sha256: dcc1d4301bee72642b4103abcdbe5704ddee8a28a07625e474ba8a47c86132bd
translation: machine
translated_at: '2026-10-24'
---
# claude-video {#claude-video}

**Ligne de développement :** `project:claude-video` · fil `claude-video-development`  
**Dernier événement :** 2026-07-27 · 1 événement daté depuis le 2026-07-27 · **Recherche :** 2026-09-05 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

claude-video est une compétence `/watch` d'analyse vidéo destinée aux agents.

- Entrée : accepte une URL ou un fichier local.
- Extraction : récupère les images clés et les sous-titres.
- Solution de repli audio : utilise Whisper lorsque les sous-titres sont absents.
- Transmission du résultat : transmet la sortie à l'agent.

La limite par défaut pour les vidéos longues est de 100 images au maximum ; le mode `token-burner` n'a pas de limite. Il convient aux enregistrements d'écran, aux extraits vidéo et aux horodatages ciblés, mais le coût en contexte augmente avec le nombre d'images.

## Ligne de développement {#development-line}

- **2026-07-27 — dépôt claude-video mentionné publiquement.** Le 2026-07-27, une entrée renvoyait vers le dépôt GitHub bradautomates/claude-video. Il s'agit de la première référence publique dans l'historique du projet, et elle fournit une source concrète à examiner.

## Ce qui a changé {#what-changed}

- 2026-07-27 — lien vers le dépôt enregistré. Les sources primaires ne montrent ni commit ni version publiée distincts à cette date précise.
- 2026-06-29 — la version 0.2.0 a ajouté quatre modes de détail, la déduplication des images, le découpage automatique des longs fichiers audio pour Whisper, ainsi qu'un paquet de compétence portable pour plusieurs hôtes.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-27, considérez le dépôt GitHub bradautomates/claude-video lié comme la source des détails d'implémentation et d'utilisation.

1. Installez la compétence pour Claude Code via la marketplace, ou pour Codex et d'autres hôtes compatibles Agent Skills avec `npx skills add bradautomates/claude-video -g`.
  — <https://github.com/bradautomates/claude-video>
2. Exécutez `/watch <URL-ou-chemin> <question>`. Il prend en charge les URL gérées par yt-dlp ainsi que les fichiers MP4, MOV, MKV et WebM locaux.
  — <https://github.com/bradautomates/claude-video>
3. Passez `--start` et `--end` pour un extrait ciblé. Cela échantillonne les images plus densément tout en consommant moins de jetons de contexte.
  — <https://github.com/bradautomates/claude-video>
4. Sélectionnez `transcript`, `efficient`, `balanced` ou `token-burner`. Si les sous-titres sont absents, définissez une clé Groq pour `whisper-large-v3` ou une clé OpenAI pour `whisper-1`.
  — <https://github.com/bradautomates/claude-video>

## Bonnes pratiques {#best-practices}

- Réduisez la fenêtre temporelle avec `--start` et `--end` pour les questions portant sur un moment précis, plutôt que de parcourir la vidéo entière.
  — <https://github.com/bradautomates/claude-video>
- Commencez par `transcript` pour les vidéos avec sous-titres, ou par `efficient` pour un passage visuel rapide ; réservez `token-burner` aux cas qui justifient le coût de nombreuses images.
  — <https://github.com/bradautomates/claude-video>
- Gardez la déduplication des images activée : par défaut, elle supprime les images presque identiques avant d'appliquer la limite.
  — <https://github.com/bradautomates/claude-video>
- N'ajoutez pas de commentaires après la valeur de `WATCH_DETAIL` : cela provoquait auparavant un repli silencieux vers le mode par défaut, corrigé dans le commit 83da59f.
  — <https://github.com/bradautomates/claude-video/commit/83da59f>

## Remplacé par ceci {#superseded-by-this}

- 2026-04-24 — l'enveloppe autonome `commands/watch.md` et l'organisation de la compétence non autonome ont été remplacées par le paquet `skills/watch/` dans la version 0.2.0.
- 2026-04-24 — l'instruction Windows utilisant `python3` est obsolète : sous Windows, exécutez les scripts avec `python`.
- 2026-04-24 — l'ancienne limite fixe `--max-frames=80` a été remplacée par des limites liées au mode de détail.

## Toujours inconnu {#still-unknown}

- L'événement daté ne fournit que l'URL du dépôt. Aucune version ni aucun commit de première main datés du 2026-07-27 n'ont été trouvés ; il n'existe donc pas d'ajout étayé par une source pour cette date.
- Le schéma ne comporte pas les champs `event_findings` et `new_events` ; la version du 2026-06-29 reste dans `what_changed` plutôt que d'apparaître comme événement structuré distinct.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/bradautomates/claude-video | bradautomates/claude-video — README et documentation d'utilisation actuelle | 2026-09-05 |
| https://raw.githubusercontent.com/bradautomates/claude-video/main/CHANGELOG.md | Journal des modifications de claude-video — version 0.2.0 datée du 2026-06-29 | 2026-09-05 |
| https://github.com/bradautomates/claude-video/commit/83da59f | Correction du repli silencieux de WATCH_DETAIL vers le mode par défaut | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:claude-video`, fil `claude-video-development`, 1 événement daté du 2026-07-27 au 2026-07-27.
- **Note pratique :** à partir du 2026-07-27, considérez le dépôt GitHub bradautomates/claude-video lié comme la source à examiner pour les détails d'implémentation et d'utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

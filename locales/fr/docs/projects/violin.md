---
title: "Violin"
category: projects
date: 2026-05-15
tags: [project, violin]
aliases: ["Violin"]
level: 2
source_sha256: 5b570a604f02309c9af702123a4cc6205cd6b13ea8c7747be189da9300dc0919
translation: machine
translated_at: '2026-10-24'
---
# Violin {#violin}

**Ligne de développement :** `project:violin` · fil `violin`  
**Dernier événement :** 2026-05-15 · 1 événement daté depuis le 2026-05-15 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Violin est une CLI, une application FastAPI et une compétence (skill) Claude Code sous licence MIT, dédiées à la traduction et au doublage de vidéos.

- Transcription : extrait la parole des vidéos.
- Traduction : traduit les dialogues vers plusieurs langues cibles.
- Doublage : génère un audio vocal de remplacement.
- Sous-titres SRT : crée des fichiers de sous-titres horodatés.
- Questions-réponses vidéo : répond à des questions sur le contenu de la vidéo.

Prend en charge 33 langues cibles ; six profils de style sont marqués comme expérimentaux.

Pratique pour les vidéos dont l'usage est autorisé, bien que la démo publique avertisse que des erreurs de traduction sont possibles.

## Ligne de développement {#development-line}

- **2026-05-15 — Présentation publique du projet de traduction Violin.** Le 2026-05-15, Violin a été publiquement associé à un article de Together AI, à un dépôt GitHub ouvert et à son site de projet. Les liens datés indiquent une présentation publique d'un projet open source orienté traduction et établissent ses premières références publiques.

## Ce qui a changé {#what-changed}

2026-05-15 — Violin est apparu comme un pipeline ouvert combinant ASR, traduction par LLM et TTS. La source primaire date la publication du 2026-05-14 et non du 2026-05-15. Elle citait comme modèles d'origine Together Whisper Large V3, DeepSeek V4 Pro et Cartesia Sonic 3. Le dépôt actuel affiche la version 0.1.1, 33 langues, des fournisseurs interchangeables Together/OpenAI/ElevenLabs, et aucune GitHub Release. Nous ne pouvons pas dater de manière fiable ces changements ultérieurs à partir des sources primaires disponibles.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-05-15, les praticiens devraient considérer Violin comme un projet orienté traduction accessible publiquement, et l'évaluer à partir de son dépôt lié et de son site de projet.

1. Pour une utilisation locale, installez Python 3.10+, ffmpeg et le paquet via `uv tool install violin`. Définissez une clé de fournisseur, puis exécutez `violin input.mp4 output.mp4 --language Chinese`.
  — <https://github.com/shang-zhu/violin>
2. Pour l'interface web et l'API REST, exécutez `violin-api`. Créez une tâche via `POST /jobs`, interrogez-la, puis téléchargez la vidéo ou le fichier SRT.
  — <https://github.com/shang-zhu/violin>
3. Pour un test rapide, utilisez la démo web. Importez un fichier ou collez une URL, puis choisissez une langue, une voix, les sous-titres et le mode voix off.
  — <https://www.violin-ai.com/>

## Bonnes pratiques {#best-practices}

- Ne traduisez que des médias dont vous êtes propriétaire, relevant du domaine public ou sous licence Creative Commons, ou des contenus pour lesquels l'autorisation explicite a été obtenue. La démo restreint les URL d'entrée à cette règle.
  — <https://www.violin-ai.com/>
- Commencez avec le profil par défaut et la sélection automatique de la voix. Utilisez un fichier YAML de configuration séparé pour la terminologie et vérifiez la sortie, car la démo est signalée comme une bêta de recherche.
  — <https://github.com/shang-zhu/violin>
- En production, utilisez `config/prod.yaml`. Il limite les envois de fichiers, sérialise les tâches et plafonne la concurrence de ffmpeg.
  — <https://github.com/shang-zhu/violin>

## Remplacé par ceci {#superseded-by-this}

- 2026-05-14 — La description initiale utilisait par défaut DeepSeek V4 Pro et Qwen3.5-397B-A17B. Le README actuel indique DeepSeek-V4-Pro-0813 pour la traduction et GLM-5.3-Flash pour le chat, mais aucune date ne confirme ce changement.
- 2026-05-14 — L'absence de clonage vocal reste une limite active. Le dépôt la mentionne toujours dans la liste TODO plutôt que comme fonctionnalité disponible.

## Inconnues {#still-unknown}

- Les sources primaires disponibles ne fournissent aucun historique daté après le lancement. Nous ne consignons pas les paramètres actuels des modèles comme de nouveaux événements datés.
- GitHub n'affiche aucune release. La version 0.1.1 apparaît dans pyproject.toml, mais les sources disponibles ne confirment ni date de publication ni distribution sur PyPI.
- Les utilisateurs doivent évaluer la qualité du doublage sur leur propre langue et leurs propres images. La démo publique avertit que les traductions peuvent contenir des erreurs.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://www.together.ai/blog/violin-open-source-translation-skill | Violin: An open-source video translation skill that breaks language barriers | 2026-09-05 |
| https://github.com/shang-zhu/violin | shang-zhu/violin repository and README | 2026-09-05 |
| https://www.violin-ai.com/ | Violin — Video Narrator | 2026-09-05 |
| https://github.com/shang-zhu/violin/releases | Violin GitHub releases | 2026-09-05 |
| https://raw.githubusercontent.com/shang-zhu/violin/main/pyproject.toml | Violin pyproject.toml | 2026-09-05 |
| https://raw.githubusercontent.com/shang-zhu/violin/main/config/default.yaml | Violin default configuration | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:violin`, fil `violin`, 1 événement daté du 2026-05-15 au 2026-05-15.
- **Note pratique :** À partir du 2026-05-15, les praticiens devraient considérer Violin comme un projet orienté traduction accessible publiquement, et l'évaluer à partir de son dépôt lié et de son site de projet.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

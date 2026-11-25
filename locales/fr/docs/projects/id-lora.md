---
title: "ID-LoRA"
category: projects
date: 2026-03-15
tags: [id-lora, id-lora-development, id_lora, project]
aliases: ["ID-LoRA"]
level: 2
source_sha256: af00885906550dfa4fb7afeb3569fb8eb9775b8dcb64303b1c29337ac63e12cd
translation: machine
translated_at: '2026-10-24'
---
# ID-LoRA {#id-lora}

**Ligne de développement :** `project:id-lora` · fil `id-lora-development`  
**Dernier événement :** 2026-03-15 · 1 événement daté depuis le 2026-03-15 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

ID-LoRA est une méthode de conditionnement d'identité en mode zero-shot pour la diffusion audio-vidéo LTX, conçue pour les créateurs qui ont besoin de vidéos de personnes qui parlent sans entraînement sur chaque locuteur.

- Transfert de l'identité vocale à partir d'un audio de référence
- Conditionnement de l'identité visuelle par une image de première frame
- Contrôle unifié de la scène, des paroles prononcées, du style vocal et du son ambiant dans un seul prompt

## Ligne de développement {#development-line}

- **2026-03-15 — Ressources publiques du projet ID-LoRA publiées.** Le 2026-03-15, ID-LoRA a publié des liens vers son site du projet, son dépôt source et ses profils de modèles. Ces liens renvoient vers des ressources primaires, mais n'établissent aucune version, capacité ou licence spécifique, ni aucune publication particulière.

## Ce qui a changé {#what-changed}

2026-03-15 — ID-LoRA est apparu comme un projet de recherche sur la génération audio-vidéo unifiée conditionnée par l'identité, sur le socle LTX-2, avec des liens vers le projet, le code et les modèles publiés le 2026-03-15. L'article initial sur arXiv, daté du 2026-03-10, présente Identity-Driven In-Context LoRA, des positions temporelles RoPE négatives pour les tokens de référence, et un guidage par l'identité. Il rapporte une préférence de 73 % face à Kling 2.6 Pro pour la similarité vocale, un gain de 24 % de similarité de locuteur entre environnements différents, et environ 3 000 paires d'entraînement sur un seul GPU.

## Comment l'utiliser {#how-to-use-this}

À la date du 2026-03-15, utilisez le site et le dépôt liés pour explorer ID-LoRA, mais vérifiez la version, la licence et la disponibilité des modèles avant toute adoption.

1. Clonez le dépôt officiel et installez les dépendances verrouillées avec `uv sync --frozen` ; utilisez Python 3.11+ et CUDA 12.x.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
2. Téléchargez les composants requis du modèle de base et le checkpoint ID-LoRA avec le script de téléchargement du dépôt.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
3. Fournissez une image de première frame, un fichier audio de référence d'environ cinq secondes, et un prompt découpé en sections `[VISUAL]`, `[SPEECH]` et `[SOUNDS]`.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
4. Pour un usage actuel avec LTX-2.3, basculez le workspace uv vers `ID-LoRA-2.3/packages/*`, puis lancez le script HQ en deux étapes avec le checkpoint LTX-2.3.
  — <https://github.com/ID-LoRA/ID-LoRA/blob/main/ID-LoRA-2.3/README.md>

## Bonnes pratiques {#best-practices}

- Utilisez un audio vocal de référence d'environ cinq secondes ; des extraits plus courts ou plus longs peuvent réduire le transfert de l'identité du locuteur.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
- Placez la transcription exacte souhaitée dans `[SPEECH]` ; placez le style d'élocution et le son environnemental dans `[SOUNDS]`, et non dans la description visuelle.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
- Utilisez le mode HQ en deux étapes sur LTX-2.3 pour la fidélité ; choisissez le mode en une étape avec quantification lorsque la VRAM ou le délai d'obtention du résultat est la contrainte.
  — <https://github.com/ID-LoRA/ID-LoRA/blob/main/ID-LoRA-2.3/README.md>
- N'utilisez que des images et des enregistrements vocaux de référence pour lesquels vous disposez d'une autorisation.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>

## Remplacé par {#superseded-by-this}

- 2026-03-24 — la prise en charge native, en amont, de ComfyUI pour le transfert d'identité par audio de référence sur LTX2 remplace en partie la voie distincte des nœuds personnalisés ComfyUI d'ID-LoRA pour LTX-2.3 ; les poids d'origine ne nécessitent aucune conversion.

## Points encore inconnus {#still-unknown}

- Les sources publiques ne fournissent aucune date de publication officielle pour la diffusion du checkpoint LTX-2.3 ; nous ne lui attribuons donc pas d'événement de développement daté.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://id-lora.github.io/ | ID-LoRA : Identity-Driven Audio-Video Personalization | 2026-09-05 |
| https://github.com/ID-LoRA/ID-LoRA/tree/main | GitHub — ID-LoRA/ID-LoRA | 2026-09-05 |
| https://github.com/ID-LoRA/ID-LoRA/blob/main/ID-LoRA-2.3/README.md | GitHub — ID-LoRA 2.3 : prise en charge de LTX-2.3 | 2026-09-05 |
| https://huggingface.co/AviadDahan/LTX-2.3-ID-LoRA-CelebVHQ-3K | Hugging Face — LTX-2.3-ID-LoRA-CelebVHQ-3K | 2026-09-05 |
| https://arxiv.org/abs/2603.10256 | ID-LoRA : Identity-Driven Audio-Video Personalization with In-Context LoRA | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:id-lora`, fil `id-lora-development`, 1 événement daté entre le 2026-03-15 et le 2026-03-15.
- **Note pratique :** À la date du 2026-03-15, les praticiens peuvent utiliser le site et le dépôt source liés comme points d'entrée vers ID-LoRA, tout en vérifiant de manière indépendante la version applicable, la licence et la disponibilité des modèles avant toute adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.

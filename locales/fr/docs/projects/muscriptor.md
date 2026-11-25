---
title: "MuScriptor — Disponibilité publique du projet"
category: projects
date: 2026-07-22
tags: [muscriptor, project, public-project-availability]
aliases: ["MuScriptor"]
level: 2
source_sha256: a715a5750a5dacbc0975cd8e3f96145282a3874be5965b73c6e4fb9c08ff67a8
translation: machine
translated_at: '2026-10-24'
---
# MuScriptor — Disponibilité publique du projet {#muscriptor-public-project-availability}

**Ligne de développement :** `project:muscriptor` · fil `public-project-availability`  
**Dernier événement :** 2026-07-22 · 1 événement daté depuis le 2026-07-22 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

MuScriptor est un modèle de transcription musicale à poids ouverts développé par Mirelo et Kyutai. Il convertit des enregistrements multi-instruments en événements de notes MIDI.

- Points de sauvegarde (checkpoints) : modèles de 100M (petit), 300M (moyen) et 1,3B (grand) paramètres.
- Environnement d'exécution : API Python, CLI et service HTTP local.
- Entrée : audio mono 16 kHz, par segments de 5 secondes.
- Sortie : hauteur, attaque, fin de note et étiquettes d'instrument parmi 36 groupes.

Les poids sont sous licence CC-BY-NC et soumis à accès contrôlé ; les prédictions n'incluent pas la vélocité (velocity).

## Ligne de développement {#development-line}

- **2026-07-22 — Les ressources publiques du projet MuScriptor étaient disponibles.** Le 2026-07-22, des liens publics ont été ouverts pour le site du projet, le dépôt, la page du modèle, la démo interactive et l'installation. Ces liens confirment la disponibilité du projet à cette date. Ils ne fixent ni une version précise, ni une capacité particulière du modèle, ni une modification technique.

## Ce qui a changé {#what-changed}

- 2026-07-22 — Les liens du projet ont ouvert l'écosystème public de MuScriptor. La version v0.2.2, publiée le 2026-07-21, avait ajouté un décodage strictement contraint par instrument, une sortie MIDI directe via HTTP, la prise en charge FP16/MPS sur Apple Silicon, des noyaux de décodage optimisés et des instructions pour GPU Windows.
- 2026-07-21 — La version v0.2.2 sur GitHub a élargi le paquet exécutable ainsi que les flux de démo et de service.
- 2026-07-10 — La version v0.2.1 a permis le service sans compilation. Kyutai a publié l'annonce du projet.
- 2026-07-09 — L'article a présenté le modèle multi-instruments à poids ouverts. L'entraînement a combiné un pré-entraînement synthétique, un affinage sur audio réel et un post-entraînement par apprentissage par renforcement (RL).
- 2026-06-30 — Création de la collection publique de points de sauvegarde. Il s'agit de métadonnées du dépôt, et non d'une date d'entraînement.

## Mode d'emploi {#how-to-use-this}

Nous pouvons évaluer MuScriptor via ses points d'accès publics (code, modèle, démo et installation) depuis le 2026-07-22. Vérifiez les capacités et versions exactes auprès des sources primaires avant toute adoption.

1. Installez depuis le dépôt Git ; l'installation via PyPI reste annoncée comme à venir.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
2. Choisissez small, medium ou large. Exécutez `muscriptor transcribe --model large audio.wav -o out.mid`, ou appelez `TranscriptionModel.load_model()` puis `transcribe_to_midi()` depuis Python.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
3. Pour un essai interactif, importez l'audio dans l'espace de transcription hébergé. Pour une intégration locale, utilisez la CLI du dépôt ou l'implémentation serveur.
  — <https://huggingface.co/spaces/hugging-apps/muscriptor-music-transcription>

## Bonnes pratiques {#best-practices}

- Utilisez le conditionnement par instrument lorsque les groupes d'instruments des pistes sont connus. La fiche du modèle indique que ce conditionnement améliore les scores et maintient la cohérence des attributions entre les segments.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
- Traitez la sortie comme une ébauche MIDI modifiable et non comme une partition finalisée, en particulier sur des audios denses, atypiques ou fortement traités.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
- Ne travaillez qu'avec des enregistrements dont les droits sont confirmés. La fiche du modèle interdit explicitement la transcription non autorisée.
  — <https://huggingface.co/MuScriptor/muscriptor-large>

## Remplacé par {#superseded-by-this}

- 2026-07-21 — La v0.2.2 remplace la v0.2.1 pour les utilisateurs ayant besoin de réponses MIDI directes via HTTP, de contraintes d'instruments strictes ou d'une inférence FP16 native sur Apple Silicon.
- 2026-07-10 — La v0.2.1 a remplacé la v0.2.0 pour le service sans étape de compilation.

## Points non élucidés {#still-unknown}

- L'événement du 2026-07-22 n'identifie pas la surface liée qui a changé ce jour-là. GitHub date la v0.2.2 au 2026-07-21 ; cette mise à jour est donc signalée comme l'ajout first-party le plus proche, et non comme une version publiée le 2026-07-22.
- Le schéma ne fournit pas de champs distincts pour `event_findings` ou `new_events` ; les constats datés restent donc sous `what_changed`.
- La démo hébergée était accessible, mais le texte de la page affichée ne contenait aucune documentation opérationnelle.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://huggingface.co/MuScriptor/muscriptor-large | MuScriptor — fiche du modèle large (≈1,3B) | 2026-09-05 |
| https://github.com/muscriptor/muscriptor/releases | Versions MuScriptor sur GitHub | 2026-09-05 |
| https://arxiv.org/abs/2607.08168 | MuScriptor: An Open Model for Multi-Instrument Music Transcription | 2026-09-05 |
| https://kyutai.org/blog/2026-07-10-muscriptor/ | MuScriptor: Automatic Multi-instrument Transcription | 2026-09-05 |
| https://huggingface.co/spaces/hugging-apps/muscriptor-music-transcription | Espace MuScriptor Music Transcription | 2026-09-05 |

## Note pour agent {#agent-brief}

- **Sujet :** `project:muscriptor`, fil `public-project-availability`, 1 événement daté du 2026-07-22 au 2026-07-22.
- **Remarque pratique :** Depuis le 2026-07-22, les praticiens pouvaient évaluer MuScriptor via ses points d'accès publics (code, modèle, démo et installation) ; vérifiez les capacités et versions exactes auprès des ressources primaires liées avant toute adoption.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.

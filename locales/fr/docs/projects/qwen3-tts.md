---
title: "Qwen3-TTS"
category: projects
date: 2026-08-06
tags: [project, qwen3-tts, qwen3-tts-release-and-distribution, qwen3_tts]
aliases: ["Qwen3-TTS"]
level: 3
source_sha256: 2de0a05c6be6e522decb06701a4117cc07268732337af8a14af29ba6d41762f7
translation: machine
translated_at: '2026-10-24'
---
# Qwen3-TTS {#qwen3-tts}

**Ligne de développement :** `project:qwen3-tts` · fil `qwen3-tts-release-and-distribution`  
**Dernier événement :** 2026-08-06 · 2 événements datés depuis le 2025-09-23 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

Qwen3-TTS est une série de synthèse vocale à poids ouverts destinée aux développeurs, conçue pour remplacer les API TTS cloud telles qu'ElevenLabs. Elle propose CustomVoice pour des timbres prédéfinis, VoiceDesign pour des timbres décrits par du texte, et Base pour le clonage à partir d'un audio de référence.

- 10 langues pour la synthèse vocale
- Base : clonage en 3 secondes à partir d'un audio de référence
- Génération : modes en flux continu et par lots
- CustomVoice : jusqu'à 9 timbres prédéfinis

La latence minimale de bout en bout annoncée est de 97 ms ; les options à poids ouverts sont 0,6B et 1,7B. C'est un choix pratique pour une TTS multilingue en local, lorsque nous pouvons exécuter Python et PyTorch ou exécuter le modèle Base via un runtime GGUF compatible.

## Ligne de développement {#development-line}

- **2025-09-23 — Qwen a relayé une démo officielle de Qwen3-TTS et la documentation de Qwen TTS.** Synthèse vocale multi-timbre, multilingue et dialectale ; la publication officielle principale est datée du 2025-09-21.
- **2026-08-06 — ggml-org a publié une distribution GGUF de Qwen3-TTS-12Hz-1.7B-Base.** Le 2026-08-06, le lien daté renvoie à une distribution GGUF de Qwen3-TTS-12Hz-1.7B-Base sur Hugging Face. Il s'agit d'une étape de distribution en aval et non d'une sortie du modèle amont par Qwen, mais elle a sensiblement élargi la voie de déploiement en local du projet.

## Évolutions {#what-changed}

- **2025-09-23** — Qwen3-TTS-Flash a établi la direction API pour la synthèse vocale multi-timbre, multilingue et dialectale ; la publication officielle initiale est datée du 2025-09-21.
- **2025-12-04** — Flash est passé à 49 timbres, 10 langues et 9 dialectes ; il s'agissait d'une mise à jour de l'API et non d'une publication de poids en local.
- **2025-12-22** — Qwen a ajouté les modèles API Qwen3-TTS-VD-Flash pour la conception de voix et Qwen3-TTS-VC-Flash pour le clonage à partir d'un échantillon de trois secondes.
- **2026-01-22** — Qwen a publié la série à poids ouverts sous licence Apache-2.0, avec Tokenizer-12Hz, 0,6B Base/CustomVoice et 1,7B Base/CustomVoice/VoiceDesign ; le déploiement local et le fine-tuning sont ainsi devenus des flux de travail pris en charge en amont.
- **2026-08-06** — ggml-org a publié des quantifications GGUF de Qwen3-TTS-12Hz-1.7B-Base pour les runtimes locaux compatibles avec llama.cpp ; il s'agit d'un conditionnement en aval du modèle Base et non d'une nouvelle variante amont de Qwen.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-09-23, les praticiens qui évaluent Qwen3-TTS doivent commencer par la démo officielle et la documentation de Qwen TTS mentionnées ci-dessus ; à partir du 2026-08-06, ceux qui recherchent un déploiement local peuvent aussi évaluer la distribution GGUF liée.

1. Choisissez CustomVoice pour un timbre prédéfini, VoiceDesign pour un timbre défini par une consigne, ou Base pour le clonage de voix ; pour les exécutions en local, sélectionnez 0,6B pour des besoins réduits ou 1,7B pour la qualité.
  — <https://github.com/QwenLM/Qwen3-TTS>
2. Créez un environnement Python 3.12 propre et installez `qwen-tts` ; chargez le modèle avec `Qwen3TTSModel.from_pretrained`.
  — <https://github.com/QwenLM/Qwen3-TTS>
3. Pour CustomVoice, transmettez le texte, la langue, le locuteur et, éventuellement, l'instruction ; pour VoiceDesign, fournissez le texte et une description de la voix en langage naturel ; pour Base, fournissez l'audio de référence et sa transcription.
  — <https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base>
4. Pour une voie locale plus légère, réservée au modèle 1,7B Base, exécutez la version GGUF avec llama.cpp, par exemple `llama serve -hf ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF:Q4_K_M`.
  — <https://huggingface.co/ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF>

## Bonnes pratiques {#best-practices}

- Utilisez un environnement Python propre afin que les dépendances TTS n'entrent pas en conflit avec les projets existants ; activez FlashAttention 2 uniquement sur du matériel compatible, avec float16/bfloat16.
  — <https://github.com/QwenLM/Qwen3-TTS>
- Indiquez explicitement la langue connue au lieu d'Auto ; utilisez la langue native du timbre choisi pour obtenir la meilleure qualité avec CustomVoice.
  — <https://github.com/QwenLM/Qwen3-TTS>
- N'exposez pas l'interface web Base ni le microphone en HTTP simple : exigez HTTPS et un certificat valide pour l'accès distant en production.
  — <https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base>
- Ne considérez pas GGUF comme un équivalent de l'ensemble de la famille : le paquet publié ne couvre que Base et fournit des quantifications distinctes Q4_K_M, Q8_0 et BF16.
  — <https://huggingface.co/ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF>

## Remplacé par ceci {#superseded-by-this}

- 2026-01-22 : traiter Qwen3-TTS uniquement comme l'API Qwen3-TTS-Flash est obsolète pour un usage local ; les poids sous Apache-2.0 pour 0,6B/1,7B et le code source sont publiés.
- 2026-08-06 : GGUF Base ne remplace pas CustomVoice ni VoiceDesign en amont ; utilisez le paquet `qwen-tts` et les points de contrôle officiels pour ces tâches.

## Points non élucidés {#still-unknown}

- La structure de la réponse ne comporte pas de champs dédiés `event_findings` ni `new_events` ; nous avons intégré leurs faits à la ligne datée `what_changed`.
- La date exacte de création du dépôt GGUF n'était pas visible sur la page du modèle ; le 2026-08-06 reste la date enregistrée de l'événement lié, et les détails du paquet ont été vérifiés par rapport à la fiche.
- Nous n'avons pas vérifié les tarifs de l'API DashScope, la disponibilité régionale ni les limites de débit actuelles ; ces éléments peuvent évoluer indépendamment de la publication à poids ouverts.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://qwen.ai/blog?from=home.latest-research-list | Qwen3-TTS-Flash : synthèse vocale multi-timbre, multilingue et multidialectale | 2026-09-05 |
| https://qwen.ai/blog?id=qwen3-tts-1128 | Mise à jour Qwen3-TTS ! 49 timbres + 10 langues + 9 dialectes | 2026-09-05 |
| https://qwen.ai/blog?id=qwen3-tts-vc-voicedesign | Qwen3-TTS passe à la vitesse supérieure : clonage et conception de voix ! | 2026-09-05 |
| https://qwen.ai/blog?id=qwen3tts-0115 | La famille Qwen3-TTS est désormais open source : conception, clonage et génération de voix | 2026-09-05 |
| https://github.com/QwenLM/Qwen3-TTS | QwenLM/Qwen3-TTS | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base | Qwen/Qwen3-TTS-12Hz-1.7B-Base | 2026-09-05 |
| https://huggingface.co/ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF | ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:qwen3-tts`, fil `qwen3-tts-release-and-distribution`, 2 événements datés du 2025-09-23 au 2026-08-06.
- **Remarque pratique :** À partir du 2025-09-23, les praticiens qui évaluent Qwen3-TTS doivent commencer par la démo officielle et la documentation de Qwen TTS mentionnées ci-dessus ; à partir du 2026-08-06, ceux qui recherchent un déploiement local peuvent aussi évaluer la distribution GGUF liée.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.

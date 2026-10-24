---
title: "Mistral AI — Produits et sorties de modèles"
category: organizations
tags: [mistral-ai, mistral_ai, model_releases, organization, product-and-model-releases]
aliases: ["Mistral AI"]
level: 3
source_sha256: 8e3c53dcfee52fa4afe140f0dc90cea9696627967fb76e6860a17b99c6a2beed
translation: machine
translated_at: '2026-10-24'
---
# Mistral AI — Produits et sorties de modèles {#mistral-ai-product-and-model-releases}

**Ligne de développement :** `organization:mistral-ai` · fil `product-and-model-releases`  
**Événements :** 2 datés, 2024-02-29 → 2026-02-05 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Mistral AI est une plateforme de modèles hébergée, destinée aux développeurs, avec Vibe comme interface interactive pour le travail, le code et le chat.

- Studio : API et console pour la génération de texte, les agents, l'IA documentaire, le RAG, l'audio, les clés et l'usage.
- Vibe : travail interactif dans le navigateur, le terminal et l'IDE.
- Voxtral : briques de transcription par lots, de transcription en direct et de traduction parole à parole.

## Ligne de développement {#development-line}

- **2024-02-29 — Mistral AI a référencé sa console développeur et ses services de chat.** Le 2024-02-29, Mistral AI a référencé à la fois sa console développeur et son service de chat à travers les URL officielles fournies. Il s'agit d'une étape visible d'accès aux produits dans l'histoire de l'entreprise, couvrant une console destinée aux créateurs et une interface de chat destinée aux utilisateurs finaux. Les liens fournis n'établissent aucune date de lancement précise ni aucun ensemble de fonctionnalités au-delà de ces services.
- **2026-02-05 — Mistral AI a publié des ressources sur la transcription Voxtral et les modèles temps réel.** Mini Transcribe V2 couvre le traitement par lots avec diarisation, biais contextuel et horodatages, tandis que 4B Realtime couvre les flux en direct. L'annonce officielle liée est datée du 2026-02-04.

## Ce qui a changé {#what-changed}

2024-02-29 — Mistral AI a exposé une URL de console développeur et une URL de chat distincte.

2026-02-05 — Voxtral Transcribe 2 a ajouté une version de reconnaissance vocale à deux voies. Mini Transcribe V2 couvre le traitement par lots avec diarisation, biais contextuel et horodatages ; 4B Realtime couvre les flux en direct. L'annonce officielle liée est datée du 2026-02-04.

2026-09-04 (trouvé aujourd'hui) — La console est désormais documentée sous le nom de Studio, une plateforme pour développeurs couvrant l'API, les agents, l'IA documentaire, le RAG et l'audio. chat.mistral.ai ouvre désormais Vibe avec les modes Work, Code et Chat.

2026-09-04 (trouvé aujourd'hui) — La surface audio actuelle comprend également le TTS et un pipeline parole à parole composable.

Choisissez une surface explicite — Studio, Vibe, audio par lots ou audio en flux — plutôt que de traiter Mistral comme un point de terminaison de chat générique.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-02-05, les praticiens qui évaluent Mistral AI pour les flux de travail vocaux devraient envisager ses ressources officielles de transcription et de temps réel Voxtral, y compris le chemin de reconnaissance vocale de la console, plutôt que de ne considérer l'entreprise que comme un fournisseur de modèles de texte.

1. Choisissez une surface : utilisez Vibe pour les tâches interactives de Chat, Work ou Code, et Studio lorsque vous construisez une application.  
   — [Le Chat devient Vibe](https://help.mistral.ai/en/articles/682992-le-chat-is-now-vibe)
2. Activez Studio, créez une clé API nommée, définissez une expiration et choisissez la portée de connecteur la plus restreinte qui convienne à l'intégration.  
   — [Activer Studio et générer une clé API](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key)
3. Stockez MISTRAL_API_KEY dans l'environnement, installez le SDK Python ou TypeScript (ou utilisez HTTP), envoyez une requête de complétion de chat, puis vérifiez la réponse renvoyée.  
   — [Envoyer votre première requête API](https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request)
4. Utilisez le Playground de Studio pour tester les prompts, comparer les modèles et les paramètres, puis examinez l'usage avant de déplacer le prompt dans le code applicatif.  
   — [Studio](https://docs.mistral.ai/studio)
5. Pour l'audio, utilisez Voxtral Mini Transcribe 2 pour les fichiers, les réunions et les archives ; réservez Voxtral Realtime aux flux à faible latence. Testez un fichier représentatif dans le playground de reconnaissance vocale avant l'intégration.  
   — [Audio](https://docs.mistral.ai/studio/audio/overview)
6. Si un déploiement local en flux est nécessaire, suivez la fiche officielle du modèle Voxtral Mini 4B Realtime et son chemin documenté vers vLLM ou Transformers.  
   — [Fiche du modèle Voxtral Mini 4B Realtime](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)

## Bonnes pratiques {#best-practices}

- Commencez par le Playground. Comparez les prompts et les paramètres sans code, puis faites de la configuration testée la base de référence de l'intégration.  
  — [Studio](https://docs.mistral.ai/studio)
- Utilisez des clés API nommées et à expiration. Accordez la portée de connecteur la plus restreinte, stockez la clé une seule fois dans un gestionnaire de secrets et renouvelez-la régulièrement.  
  — [Activer Studio et générer une clé API](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key)
- Considérez le mode Free comme limité en débit. Implémentez un backoff exponentiel pour les réponses 429.  
  — [Envoyer votre première requête API](https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request)
- Choisissez le mode audio selon la charge de travail. Mini Transcribe 2 en traitement par lots prend en charge la diarisation, les horodatages et jusqu'à 100 termes de contexte ; Realtime est destiné au streaming en direct et ne peut pas utiliser la diarisation.  
  — [Audio](https://docs.mistral.ai/studio/audio/overview)
- Pour les noms propres et le vocabulaire spécialisé, utilisez le biais contextuel en traitement par lots et évaluez-le sur votre langue. Les notes de version indiquent que la fonctionnalité est optimisée pour l'anglais, tandis que la prise en charge des autres langues est expérimentale.  
  — [Notes de version de Voxtral Transcribe 2](https://mistral.ai/news/voxtral-transcribe-2)
- N'auto-hébergez Realtime que dans le cadre du backend et de l'enveloppe matérielle documentés. La fiche officielle en BF16 mentionne un seul GPU d'au moins 16 Go pour le service vLLM et signale certaines alternatives comme non testées.  
  — [Fiche du modèle Voxtral Mini 4B Realtime](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)

## Remplacé par ce qui suit {#superseded-by-this}

- 2024-02-29 — La surface de chat n'est plus décrite comme Le Chat. chat.mistral.ai ouvre désormais Vibe, avec la même URL, la même connexion et les conversations existantes.
- 2026-02-05 — Les nouvelles intégrations audio ne doivent pas considérer la transcription par lots et le streaming en direct comme interchangeables. Les recommandations actuelles sélectionnent Mini Transcribe 2 pour les enregistrements et Realtime pour les flux, et Realtime ne peut pas utiliser la diarisation.
- 2026-02-05 — Utilisez l'identifiant actuel du modèle de streaming, `voxtral-mini-transcribe-realtime-2602`, plutôt que de vous fier au seul nom de la famille.

## Points encore inconnus {#still-unknown}

- L'enregistrement du 2024-02-29 ne conserve que les URL d'entrée ; il ne précise pas l'ensemble exact des fonctionnalités de la console ou du chat à cette date.
- L'événement répertorié est daté du 2026-02-05, alors que l'annonce de Mistral est datée du 2026-02-04. La source ne permet pas de résoudre l'écart de fuseau horaire ou d'ingestion.
- `model_releases` est un regroupement partagé de versions, et non une chronologie propre à Mistral. Seul l'événement Voxtral lié est rattaché de façon sûre à cette page d'entreprise.
- Une recherche limitée en chinois simplifié n'a trouvé aucune page chinoise de Mistral de première source permettant de soutenir une recommandation d'exploitation spécifique au chinois.
- Ces pratiques d'exploitation proviennent de la documentation officielle actuelle et de la fiche officielle du modèle ; aucun retour indépendant de production n'a été utilisé.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://console.mistral.ai/ | Console Mistral | 2026-09-04 |
| https://chat.mistral.ai/ | Vibe Chat | 2026-09-04 |
| https://mistral.ai/news/voxtral-transcribe-2 | Voxtral transcrit à la vitesse du son. | Mistral AI | 2026-09-04 |
| https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602 | mistralai/Voxtral-Mini-4B-Realtime-2602 · Hugging Face | 2026-09-04 |
| https://console.mistral.ai/build/audio/speech-to-text | Playground de reconnaissance vocale de Mistral Studio | 2026-09-04 |
| https://docs.mistral.ai/studio | Studio | Documentation Mistral | 2026-09-04 |
| https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request | Envoyer votre première requête API | Documentation Mistral | 2026-09-04 |
| https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key | Activer Studio et générer une clé API | Documentation Mistral | 2026-09-04 |
| https://docs.mistral.ai/studio/audio/overview | Audio | Documentation Mistral | 2026-09-04 |
| https://help.mistral.ai/en/articles/682992-le-chat-is-now-vibe | Le Chat devient Vibe | Centre d'aide Mistral | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `organization:mistral-ai`, fil `product-and-model-releases`, 2 événements datés du 2024-02-29 au 2026-02-05.
- **Note pratique :** À partir du 2026-02-05, les praticiens qui évaluent Mistral AI pour les flux de travail vocaux devraient envisager ses ressources officielles de transcription et de temps réel Voxtral, y compris le chemin de reconnaissance vocale de la console, plutôt que de ne considérer l'entreprise que comme un fournisseur de modèles de texte.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.

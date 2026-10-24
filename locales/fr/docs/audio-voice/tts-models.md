---
title: "Modèles de synthèse vocale"
category: reference
tags: [tts, speech-synthesis, voice, flow-matching, autoregressive, zero-shot, multilingual, diffusion-language-model]
level: 3
source_sha256: a7883fb6ea4a3aa1b5232ec07ad2ab8b692a0106df12303d76f3d973bd8285d3
translation: machine
translated_at: '2026-10-24'
---
# Modèles de synthèse vocale {#text-to-speech-models}

La synthèse vocale moderne est passée des approches concaténatives et paramétriques à des modèles neuronaux de bout en bout. Trois architectures dominent : l'autorégressif (token par token, flexible mais lent), le non autorégressif / flow matching (nombre d'étapes fixe, inférence plus rapide) et les modèles de langage par diffusion (texte vers tokens acoustiques multi-codebook).

## Points clés {#key-facts}

- TTS zero-shot = cloner n'importe quelle voix à partir d'un court extrait de référence (3 à 30 secondes) sans fine-tuning
- Les modèles flow matching (FM) utilisent un nombre fixe de pas NFE (généralement 16 à 32), ce qui rend le temps d'inférence prévisible
- Les modèles codec autorégressifs (AR) génèrent les tokens audio séquentiellement, avec une meilleure prosodie mais une latence variable
- La TTS par diffusion ajoute un bruit gaussien aux mel-spectrogrammes et apprend à inverser le processus
- Les modèles de langage par diffusion (OmniVoice) projettent directement le texte vers des tokens acoustiques multi-codebook, un troisième paradigme combinant les atouts du flow-based et de l'AR
- Les architectures sans tokenizer (VoxCPM2) suppriment entièrement les tokens codec discrets, préservant les nuances prosodiques que la tokenisation détruit
- La plupart des modèles TTS modernes produisent des mel-spectrogrammes ou des tokens de codec audio, puis un vocodeur (Vocos, HiFi-GAN) reconstruit la forme d'onde
- La fréquence d'échantillonnage compte : 16 kHz (téléphonie), 24 kHz (standard), 44,1/48 kHz (qualité studio)
- Les omni-modèles de bout en bout (Qwen3.5-Omni) combinent ASR + TTS + raisonnement LLM dans une seule architecture, avec prise en charge de la conversation en temps réel

## Familles d'architectures {#architecture-families}

### Flow Matching (lignée F5-TTS) {#flow-matching-f5-tts-lineage}

Génération non autorégressive à nombre d'étapes fixe. Audio de référence + texte -> mel-spectrogramme masqué -> le flow matching remplit le masque.

```text
Pipeline:
  reference_audio -> mel_spectrogram -> [MASK target region]
  text -> phoneme_encoder -> duration_predictor -> alignment
  flow_matching(masked_mel, text_embedding, NFE=32) -> full_mel
  vocoder(full_mel) -> waveform
```

**Modèles principaux :**
- **F5-TTS** - modèle flow-matching de référence, haute qualité, multilingue
- **LEMAS-TTS** (0,3B) - basé sur F5-TTS, 10 langues dont le russe, plus de 150 000 heures de données d'entraînement
- **CosyVoice 2** (Alibaba) - flow matching avec capacité de streaming, orienté mandarin

### Codec autorégressif {#autoregressive-codec}

Génère des tokens audio discrets de gauche à droite, puis décode avec un décodeur codec.

```text
Pipeline:
  text -> LLM backbone -> audio_codec_tokens (e.g. EnCodec, DAC)
  codec_decoder(tokens) -> waveform
```

**Modèles principaux :**
- **VoxCPM2** (2B) - sans tokenizer, pipeline à 4 étapes (LocEnc -> TSLM -> RALM -> LocDiT), hybride diffusion-AR sur le backbone MiniCPM-4, plus de 30 langues, 48 kHz natif avec super-résolution intégrée, Apache 2.0
- **Orpheus TTS** (Canopy AI) - natif LLM, contrôle émotionnel via des balises
- **Fish Speech** - codec AR rapide, bon support du CJK

### Modèle de langage par diffusion {#diffusion-language-model}

Projette directement le texte vers des tokens acoustiques multi-codebook via un processus de diffusion, évitant le goulot d'étranglement mono-codebook des modèles AR.

```text
Pipeline:
  text -> diffusion_language_model -> multi_codebook_acoustic_tokens
  codec_decoder(multi_codebook_tokens) -> waveform
  
  Key advantage: multi-codebook = richer acoustic representation
  than single-stream AR, while still being faster than flow matching
```

**Modèles principaux :**
- **OmniVoice** (k2-fsa) - plus de 600 langues, RTF 0,025 (40x temps réel), clonage inter-lingue zero-shot, prise en charge robuste du bruit dans la référence, Apache 2.0
- **Voxtral 4B** (Mistral) - 4B paramètres, 9 langues (EN/FR/DE/ES/NL/PT/IT/HI/AR, sans RU/ZH), latence de 70 ms, clonage à partir de 3 secondes, capture l'accent et les disfluences, poids ouverts

### Omni-modèles de bout en bout {#end-to-end-omni-models}

ASR + TTS + raisonnement LLM combinés dans un seul modèle. Entrée : audio ou texte. Sortie : texte et parole simultanément.

```text
Architecture (Qwen3.5-Omni):
  Input audio/text -> Thinker module (reasoning, MoE)
  Thinker -> Talker module (speech synthesis)
  ARIA alignment: dynamic text-speech synchronization mid-generation
  
  Capabilities: real-time conversation, turn-taking detection,
  mid-conversation control (volume, tempo, emotion)
```

**Modèles principaux :**
- **Qwen3.5-Omni** (Alibaba) - double module Thinker-Talker, 113 langues en ASR / 36 langues en TTS / 55 voix, gestion des tours de parole en temps réel, WER de 6,24 sur seed-hard (contre 8,19 pour GPT-Audio), API uniquement (non open-source), 3 variantes : Plus/Flash/Light

### Hybrides / autres {#hybrid-other}

- **XTTS v2** (Coqui) - GPT + vocodeur HiFi-GAN, multilingue éprouvé (RU + EN), clonage vocal à partir de 6 secondes
- **Kokoro-82M** - modèle compact (82M paramètres), 100x temps réel sur CPU, centré sur l'anglais
- **StyleTTS 2** - diffusion de style + prédicteur de durée, inférence rapide
- **Chatterbox** (Resemble AI) - contrôle de l'émotion, clonage à partir de courts échantillons
- **Dia** (Nari Labs) - orienté dialogue, génération multi-locuteurs

## Comparaison des modèles (2026) {#model-comparison-2026}

| Modèle | Paramètres | Langues | Fréquence d'échantillonnage | Architecture | Points forts |
|-------|--------|-----------|-------------|-------------|----------|
| Fish Audio S2 Pro / OpenAudio S1 | 4B + 400M | 80+ | — | Dual-AR (Slow+Fast) | N°1 TTS Arena, 81,88 % contre gpt-4o-mini, plus de 15 000 balises d'émotion |
| VoxCPM2 | 2B | 30+ | 48 kHz | Diff-AR sans tokenizer | Qualité studio, conception de voix, russe |
| OmniVoice | ? | 600+ | ? | LM par diffusion | Couverture linguistique la plus large, RTF 0,025 |
| Qwen3.5-Omni | Grand | 36 TTS / 113 ASR | ? | Omni (Thinker-Talker) | Conversation de bout en bout |
| Voxtral 4B | 4B | 9 (sans RU/ZH) | ? | Diff-AR en streaming | 68,4 % de victoires contre ElevenLabs, clonage en 3 s |
| Qwen3-TTS | 1,7B / 0,6B | 10 (dont RU) | ? | Codec propriétaire 12 Hz | Conception de voix, 97 ms en streaming |
| Dia 1.6B / Dia2 (Nari Labs) | 1B/2B | EN | Apache 2.0 | TTS de dialogue | Dialogue multi-locuteurs, streaming, jusqu'à 2 min |
| Higgs Audio V2 (BosonAI) | 3B | Multi | — | Basé sur Llama 3.2 | 75,7 % de victoires contre GPT-4o-mini-tts sur les émotions, multi-locuteurs |
| IndexTTS-2.5 | ? | CN/EN/JP/ES | — | Propriétaire | Vecteur d'émotion à 8 dimensions, durée précise (doublage) |
| NeuTTS Air (Neuphonic) | 748M | Multi | Ouvert | GGUF | Fonctionne sur Raspberry Pi, clonage vocal en 3 s |
| LEMAS-TTS | 0,3B | 10 | 24 kHz | Flow matching | Multilingue + édition au niveau du mot |
| Chatterbox-Turbo | 350M-500M | 23+ (dont RU) | ? | Décodeur en une étape | MIT, balises paralinguistiques |
| Kokoro-82M | 82M | 6 (sans RU) | 24 kHz | Proche de StyleTTS | Le plus rapide : 210x temps réel, CPU |
| XTTS v2 | ~0,5B | 17 (dont RU) | 24 kHz | GPT + vocodeur | Éprouvé, stable, RU |
| CosyVoice 3 | ~0,5B | 9 (dont RU) | 22,05 kHz | Flow matching optimisé par RL | CER 0,81 %, latence de 150 ms |
| F5-TTS Russian | 0,3B | RU | 24 kHz | Flow matching (fine-tuné) | Meilleur TTS russe open-source |
| Spark-TTS | 0,5B | ZH/EN | ? | BiCodec + Qwen2.5 | Contrôle des attributs par chaîne de raisonnement |
| OuteTTS 1.0 | 0,6B/1B | Multi | ? | AR + encodeur DAC | GGUF/EXL2, matériel grand public |

## Paramètres d'inférence {#inference-parameters}

```text
Common TTS parameters:
  NFE steps (flow matching): 16-32, higher = better quality, slower
  CFG strength: 1.0-3.0, controls adherence to text vs naturalness
  Temperature: 0.5-1.0, controls variation in AR models
  Speed: 0.8-1.2x, pitch-preserving time stretch
  Top-k / Top-p: AR sampling parameters, same as LLM text generation
```

## Édition de la parole {#speech-editing}

LEMAS-Edit et VoiceCraft permettent l'édition au niveau du mot : remplacer des mots précis dans un enregistrement sans regénérer l'intégralité de l'énoncé. Deux backends :

- **Backend flow-matching** : plus rapide, 10 langues
- **Backend codec AR** : 7 langues, nécessite WhisperX + alignement MMS pour les frontières de mots

## Métriques d'évaluation {#evaluation-metrics}

- **MOS** (Mean Opinion Score) - note humaine de 1 à 5, référence absolue mais coûteuse
- **MUSHRA** - test de comparaison multi-stimuli, plus adapté à la comparaison de modèles
- **WER** (Word Error Rate) - transcrire la parole générée et comparer au texte d'entrée
- **Similarité du locuteur** - similarité cosinus entre les embeddings de locuteur de la référence et de la sortie générée
- **PESQ / POLQA** - qualité perceptuelle, corrélée au MOS

## Conception de voix (création de voix à partir d'une description textuelle) {#voice-design-text-described-voice-creation}

Certains modèles peuvent créer une voix à partir d'une description textuelle, sans audio de référence :

```text
VoxCPM2 voice design:
  Input: "A warm female voice, age 30, slight accent, cheerful"
  -> Voice design module generates synthetic speaker embedding
  -> TTS generates speech with described characteristics

OmniVoice attribute control:
  Attributes: gender, age, pitch, dialect, whisper, speaking rate
  -> Fine-grained parametric control over synthetic voice
  -> Can combine: "young female, whispering, fast pace"
```

## Benchmarks de latence (2026) {#latency-benchmarks-2026}

| Modèle | Premier paquet (TTFA) | RTF | Remarques |
|-------|---------------------|-----|-------|
| Kokoro 82M | 40-70 ms | 0,005 (210x RT) | Le plus rapide, adapté au CPU |
| Qwen3-TTS Flash | 97 ms | — | Streaming |
| CosyVoice 3 | 150 ms | — | Bi-streaming, sans perte |
| Voxtral 4B | 70 ms | — | Entrée de 500 caractères / 10 s |
| Fish Audio S2 Pro | <100 ms | 0,195 | Moteur d'inférence SGLang |
| VoxCPM2 | — | 0,13 (Nano-VLLM) | RTF 0,30 avec PyTorch standard |
| Chatterbox-Turbo | ~472 ms | 0,499 | Compromis du décodeur en une étape |

## TTS russe (open-source, classement) {#russian-tts-open-source-ranked}

| Modèle | Qualité | Remarques |
|-------|---------|-------|
| F5-TTS Russian (ESpeech) | Meilleur open-source | Plusieurs fine-tunes, plus de 10 000 heures |
| ESpeech-TTS-1 RL-V2 | Excellente | Apache 2.0 |
| Qwen3-TTS 1.7B | Solide | 1 langue sur 10 |
| CosyVoice 3 | Prise en charge | Optimisé par RL |
| Chatterbox-ML 500M | Prise en charge | 1 langue sur 23 |
| VoxCPM2 2B | Prise en charge | Modèle de plus de 30 langues |
| XTTS v2 | Bonne | 17 langues, éprouvé |
| Silero TTS | Excellente | Conçu spécifiquement pour le russe |

Ressources : [Russian TTS Leaderboard](https://huggingface.co/spaces/ESpeech/open_tts_leaderboard_ru) | [awesome-russian-speech](https://github.com/alphacep/awesome-russian-speech)

## Pièges courants {#gotchas}

- **La qualité de l'audio de référence est déterminante** - des références bruitées, réverbérantes ou contaminées par de la musique donnent de mauvais clones, quelle que soit la qualité du modèle. Appliquez un débruitage UVR5 ou DeepFilterNet avant utilisation. Exception : OmniVoice est explicitement robuste au bruit et accepte des échantillons bruités
- **La qualité du zero-shot multilingue est inégale** - la plupart des modèles excellent en anglais et en chinois, mais se dégradent sur les langues moins dotées. OmniVoice (600+ langues) et VoxCPM2 (30+ langues) ont la couverture la plus large, mais testez toujours spécifiquement la langue cible
- **Le compromis NFE du flow matching n'est pas linéaire** - passer de 16 à 32 étapes améliore nettement la qualité, mais de 32 à 64 étapes les gains deviennent marginaux tout en doublant la latence
- **Les modèles à base de codec hallucinent sur les entrées longues** - les modèles AR peuvent boucler, bégayer ou sauter des mots sur des textes de plus de 500 caractères. Découpez les longs textes en segments au niveau de la phrase
- **Les modèles accessibles uniquement par API vous enferment** - Qwen3.5-Omni offre la meilleure expérience de bout en bout, mais n'est disponible que par API. Prévoyez un repli sur des modèles ouverts (OmniVoice, VoxCPM2) en cas de problème de coût ou de disponibilité
- **Compromis sans tokenizer contre codec** - les modèles sans tokenizer (VoxCPM2) préservent les détails prosodiques que les modèles à base de codec perdent lors de la tokenisation, mais ils tendent à être plus grands et plus lents

## Voir aussi {#see-also}

- [[voice-cloning]] - couverture dédiée aux techniques de clonage et au transfert inter-lingue
- [[voice-design]] - création d'identités vocales uniques à partir de descriptions textuelles, mélange de voix (Slerp, Cartesia, VoxMorph)
- [[asr-stt-compression]] - compression du cache KV pour l'inférence TTS (TriAttention, TurboQuant)
- [[audio-generation]] - génération de musique et d'effets sonores
- [[speech-recognition]] - modèles ASR utilisés pour l'évaluation TTS (mesure du WER)

---
title: "Conception de voix et mélange de voix"
description: "Création de voix de synthèse uniques à partir de descriptions textuelles, morphing de voix, benchmarks de naturel et identité vocale multilingue. Couvre Qwen3-TTS VoiceDesign, VoxMorph, embeddings Cartesia, scores MOS."
level: 3
source_sha256: 6badd9d592af5fe7da3fe73f303a128082b85f39ab7f645301dd3126c4da6fa4
translation: machine
translated_at: '2026-10-24'
---
# Conception de voix et mélange de voix {#voice-design-and-voice-mixing}

Création d'une identité vocale de synthèse sans cloner une personne spécifique. Deux approches : la conception de voix à partir d'une description textuelle, et le mélange de voix (interpolation entre des embeddings vocaux existants). En 2026, plusieurs modèles open source prennent en charge la conception de voix ; l'écart de qualité avec les API commerciales s'est réduit à 0,1-0,2 MOS.

## Conception de voix à partir de descriptions textuelles {#voice-design-from-text-descriptions}

### Qwen3-TTS VoiceDesign {#qwen3-tts-voicedesign}

Contrôle via le paramètre `instruct`. 7 dimensions contrôlables : genre, âge (années précises), hauteur, rythme d'élocution, ton émotionnel, caractéristiques du timbre, scénario.

```python
# Example prompt (15-40 words optimal)
voice_description = """
A young adult woman, around 25 years old. Low-pitched voice with a 
deliberate, steady pace. Calm and professional tone, suitable for 
audiobook narration.
"""
```

**5 principes :**
1. Soyez précis (« grave, net, au rythme rapide » plutôt que « belle voix »)
2. Utilisez plusieurs dimensions simultanément
3. Restez objectif (qualités physiques, pas sentiments)
4. Soyez original (pas d'imitation de célébrité)
5. Zone optimale : 15 à 40 mots, riche en informations

**NON contrôlable** : l'accent (nécessite un audio de référence pour la plupart des modèles).

### OmniVoice (contrôle structuré des attributs) {#omnivoice-structured-attribute-control}

```text
Attributes (one per category, freely combinable):
  Gender:  male / female
  Age:     child / teenager / young adult / middle-aged / elderly
  Pitch:   very low / low / medium / high / very high
  Style:   normal / whisper
  EN accent: american / british / australian / indian / chinese /
              canadian / korean / portuguese / russian / japanese
  CN dialect: Sichuan / Shaanxi / Henan / ... (regional)
```

Particularité : **sélection de l'accent** sous forme textuelle, alors que la plupart des modèles exigent un audio de référence pour l'accent.

### VoxCPM2 (sans tokenizer, avril 2026) {#voxcpm2-tokenizer-free-april-2026}

Conception de voix basée sur du texte, avec une architecture diffusion-AR sans tokenizer. Évite les artefacts de quantification liés à la tokenisation par codec, préservant les nuances prosodiques. Sortie native à 48 kHz, plus de 30 langues, licence Apache 2.0.

### Parler-TTS {#parler-tts}

Description textuelle en forme libre, sans aucun audio de référence requis. Moins précis qu'un contrôle structuré, mais ne nécessite aucun actif audio.

```python
# parler-tts usage
description = "a warm female voice with slight British accent, speaking slowly and clearly"
input_ids = tokenizer(description, return_tensors="pt").input_ids
prompt_ids = tokenizer(text, return_tensors="pt").input_ids
generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_ids)
```

## Mélange et fusion de voix {#voice-mixing-blending}

### Cartesia Sonic (API de production) {#cartesia-sonic-production-api}

Embeddings vocaux à 192 dimensions. Interpolation linéaire via l'API ou le playground.

```python
# Voice mixing via Cartesia API
new_voice = w1 * voice_a_embedding + w2 * voice_b_embedding
# Note: perception is non-linear - 50/50 mix may need non-equal weights
# Use prototype embeddings to add speed/emotion characteristics
```

**MOS 4,7** (Sonic 2), environ 90 ms de TTFB. Commercial uniquement.

### VoxMorph (recherche, ICASSP 2026) {#voxmorph-research-icassp-2026}

Dissocie la voix en un **embedding de prosodie** (rythme, hauteur) et un **embedding de timbre** (conduit vocal, formants). Mélange ces deux composantes indépendamment à l'aide de **Slerp** (interpolation linéaire sphérique).

```text
Method:
  speaker_a (5 sec) -> prosody_embedding, timbre_embedding
  speaker_b (5 sec) -> prosody_embedding, timbre_embedding
  
  Slerp on hypersphere:
  new_voice = Slerp(timbre_a, timbre_b, α) + Slerp(prosody_a, prosody_b, β)
  
  Result: voice texture of speaker A + speaking style of speaker B
```

Zero-shot (sans réentraînement). Amélioration de la qualité d'un facteur 2,6 par rapport aux méthodes antérieures, réduction de 73 % des erreurs d'intelligibilité. `github.com/Bharath-K3/VoxMorph`

### Méthode INSIDE (APSIPA 2025) {#inside-method-apsipa-2025}

Crée de nouvelles identités de locuteurs qui « comblent les vides » entre les locuteurs réels dans l'espace des embeddings.

```text
Select nearby speaker pairs → compute Slerp intermediates
→ novel identity between them
+5.24% speaker verification improvement
+13.44% gender classification gain
```

### Slerp contre interpolation linéaire {#slerp-vs-linear-interpolation}

**Privilégiez toujours Slerp** pour les embeddings vocaux. L'interpolation linéaire de vecteurs de grande dimension modifie la norme des vecteurs, ce qui provoque des artefacts. Slerp se déplace à la surface de l'hypersphère :

```python
import numpy as np

def slerp(v0, v1, t):
    """Spherical linear interpolation."""
    dot = np.clip(np.dot(v0, v1), -1.0, 1.0)
    theta = np.arccos(dot) * t
    relative = v1 - v0 * dot
    relative /= np.linalg.norm(relative)
    return v0 * np.cos(theta) + relative * np.sin(theta)
```

## Ce qui rend les voix non naturelles {#what-makes-voices-unnatural}

| Problème | Cause | Meilleures solutions |
|---------|-------|---------------|
| Prosodie plate / monotone | Le TTS « moyenne » les variations de hauteur | Sesame CSM (sensible au contexte), Fish S2 (15K+ balises), Orpheus |
| Micro-pauses absentes | Espacement uniforme entre les mots | VoxCPM2 (timing sans tokenizer), Sesame CSM |
| Absence de respiration | Le TTS omet les inspirations | Orpheus (balises `<sigh>`), Chatterbox (`[cough]`, `[laugh]`) |
| Platitude émotionnelle | La prosodie ignore le sens | Fish S2 Pro (balises sous-mot), IndexTTS-2.5 (vecteur émotionnel 8D) |
| Ignorance du contexte | Aucune compréhension du POURQUOI | Sesame CSM (modélisation du contexte conversationnel) |
| Compression de l'étendue tonale | Plus étroite que chez l'humain | VoxCPM2 (48 kHz, sans perte de tokenisation) |

**Techniques de contournement :**
- Insérer des virgules, des points de suspension et des marqueurs de micro-pause pour guider la prosodie
- Utiliser SSML ou des balises propres au modèle pour l'emphase, les pauses et la respiration
- Fournir un contexte conversationnel (Sesame CSM)
- Post-entraînement par alignement RL : Fish S2, CosyVoice 3

## Benchmarks de naturel (MOS, 2026) {#naturalness-benchmarks-mos-2026}

| Modèle | MOS | Méthode |
|-------|-----|--------|
| Sesame CSM | 4,7 | CMOS (jeu de données Expresso) - sensible au contexte |
| Cartesia Sonic 2 | 4,7 | Référence du secteur |
| Orpheus TTS | 4,6 | Rapporté |
| Fish Audio S2 Pro (EN) | 4,50 expressivité | Évaluation interne |
| Fish Audio S2 Pro (CN) | 4,94 expressivité | Évaluation interne - le plus performant pour le chinois |
| Parole humaine (réf.) | 4,5-4,8 | Varie selon l'enregistrement |

**Réduction de l'écart de qualité** : en 2023, les meilleurs modèles open source étaient environ 1,0 MOS en dessous d'ElevenLabs. En 2026, l'écart est de 0,1-0,2 MOS. Plusieurs modèles open source égalent désormais ElevenLabs, voire le dépassent.

**Taux de préférence humaine :**
- Fish S2 Pro : n° 1 de la TTS Arena (Bradley-Terry 3,07)
- Voxtral 4B : 68,4 % contre ElevenLabs Flash v2.5 (test en aveugle)
- Chatterbox-Turbo : 63,75 % de préférence par rapport à ElevenLabs

## Caractéristiques vocales contrôlables par modèle {#controllable-voice-characteristics-by-model}

| Caractéristique | Qwen3-TTS | OmniVoice | VoxCPM2 | Fish S2 |
|---------------|-----------|-----------|---------|---------|
| Genre | Oui | Oui | Oui | Via audio de référence |
| Âge (années précises) | Oui | 5 catégories | Oui | Via audio de référence |
| Hauteur | Oui | 5 niveaux | Oui | Via balises |
| Rythme d'élocution | Oui | Non | Oui | Via balises |
| Émotion | Oui | Non | Oui | 15K+ balises |
| Accent | **Non** | Accents EN + dialectes CN | Inconnu | Via audio de référence |
| Chuchotement | Inconnu | Oui | Inconnu | `[whisper]` |
| Respirations/rires | Non | Non | Non | Partiel |

## Identité vocale multilingue {#cross-language-voice-identity}

Maintien de la même identité vocale d'une langue à l'autre :

```text
Workflow:
  1. Create voice in English first (most training data, strongest base)
  2. Test same description/embedding in target language (RU, CN)
  3. If inconsistent: Voxtral 4B for cross-lingual identity preservation
     (preserves accent, inflection, intonation across language switch)
```

**Pour RU+CN+EN** : Qwen3-TTS est le seul modèle combinant conception de voix, les trois langues et une qualité compétitive.

## Pièges à éviter {#gotchas}

- **L'accent ne peut pas être conçu à partir d'un texte dans la plupart des modèles.** Seul OmniVoice propose une sélection structurée de l'accent. Pour les autres, capturez l'accent à l'aide d'un audio de référence d'un locuteur natif ayant l'accent souhaité
- **Perception non linéaire des poids de mélange.** Un mélange 50/50 de deux voix sonne rarement comme « 50 % chacune » : il peut sonner à 80 % comme une seule voix. Ajustez les poids de manière itérative et perceptive, pas mathématiquement
- **Les descriptions courtes perdent en précision.** Les descriptions de moins de 10 mots produisent des voix génériques. En dessous de 15 mots, les valeurs par défaut du modèle dominent. Utilisez 15 à 40 mots et précisez plusieurs dimensions (âge + hauteur + rythme + ton émotionnel)
- **La conception de voix n'est pas stable d'une inférence à l'autre.** Contrairement au clonage vocal (déterministe avec la même référence), les voix décrites par texte varient d'une génération à l'autre. Conservez le prompt exact ET les paramètres de génération si la reproductibilité compte

## Voir aussi {#see-also}

- [[tts-models]] - comparaison des modèles, y compris les capacités de conception de voix
- [[voice-cloning]] - clonage à partir d'un audio de référence
- [[voice-agent-pipelines]] - intégration du TTS dans des systèmes vocaux temps réel
- [[speech-recognition]] - modèles ASR pour l'évaluation (mesure du WER)

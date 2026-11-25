---
title: "Clonage vocal"
category: techniques
tags: [voice-cloning, speaker-embedding, cross-lingual, zero-shot, safety, tts]
level: 3
source_sha256: 289bf673aa4ea644549c41361b9431355b10485bc7c450d1cd0a4c73cb51a704
translation: machine
translated_at: '2026-10-24'
---
# Clonage vocal {#voice-cloning}

Le clonage vocal reproduit les caractéristiques vocales d'un locuteur cible (timbre, hauteur, rythme) à partir d'un échantillon audio de référence. Les approches modernes en zero-shot ne nécessitent que 5 à 30 secondes d'audio propre, ce qui évite de devoir disposer de plusieurs heures de données d'entraînement par locuteur.

## Points clés {#key-facts}

- Le clonage zero-shot extrait un embedding de locuteur à partir de l'audio de référence et conditionne la génération TTS sur cet embedding
- Les embeddings de locuteur sont généralement des vecteurs de 256 à 512 dimensions, produits par des modèles comme ECAPA-TDNN, WavLM ou Resemblyzer
- Le clonage cross-lingual préserve l'identité vocale tout en générant de la parole dans une langue que le locuteur n'a jamais enregistrée
- Le clonage par fine-tuning (adaptation au locuteur) produit une meilleure qualité, mais nécessite 1 à 5 heures d'audio cible et un entraînement sur GPU
- La qualité dépend fortement de : la propreté de l'audio de référence, les conditions d'enregistrement, la constance du locuteur dans la référence

## Approches {#approaches}

### Zero-Shot (sans entraînement) {#zero-shot-no-training}

Extraire l'embedding de locuteur depuis la référence, puis l'injecter dans le décodeur TTS. Aucun fine-tuning n'est nécessaire.

```text
Reference audio (5-30 sec)
  -> Speaker encoder (ECAPA-TDNN / WavLM)
  -> Speaker embedding (256-512 dim vector)
  -> TTS decoder conditioned on embedding + text
  -> Generated speech in target voice
```

**Modèles prenant en charge le clonage zero-shot :**
- LEMAS-TTS, F5-TTS, CosyVoice 2 (flow matching)
- XTTS v2, VoxCPM2, Fish Speech (autorégressifs)
- OmniVoice : plus de 600 langues, contrôle des émotions par balises

### Adaptation au locuteur (fine-tuning) {#speaker-adaptation-fine-tuning}

Affiner un modèle TTS de base à partir des données du locuteur cible. Qualité supérieure, mais demande du calcul.

```text
Base TTS model + 1-5 hours of target speaker audio
  -> Fine-tune decoder layers (freeze encoder)
  -> Speaker-specific model checkpoint
  -> Generate with text input only (no reference needed at inference)
```

En général 500 à 2000 étapes d'entraînement, soit 10 à 30 minutes sur un seul GPU.

### Conception de voix (à partir d'une description textuelle) {#voice-design-text-described}

Plusieurs modèles permettent désormais de générer une voix à partir d'une description textuelle plutôt que d'une référence audio.

```text
VoxCPM2 voice design:
  "A warm, deep male voice with slight British accent, age 40-50"
  -> Voice design module (built into tokenizer-free pipeline)
  -> Synthetic speaker embedding
  -> TTS generation at 48kHz studio quality

OmniVoice attribute-based design:
  Attributes: gender=male, age=40-50, pitch=low, dialect=british, style=warm
  -> Parametric attribute control (not free-text)
  -> Can specify: whisper, shouting, specific dialect
  -> Works across 600+ languages
```

**Comparaison :**
- VoxCPM2 : description en texte libre, plus flexible, plus de 30 langues
- OmniVoice : basé sur des attributs, résultats plus prévisibles, plus de 600 langues

## Clonage cross-lingual {#cross-lingual-cloning}

L'identité vocale du locuteur se transfère vers des langues qu'il n'a jamais parlées. La qualité varie selon la distance entre les langues.

```text
Quality hierarchy for cross-lingual transfer:
  Same language family (EN -> DE):     High quality
  Same script (EN -> FR):              Good quality  
  Different family (EN -> ZH):         Moderate quality
  Low-resource target (EN -> Swahili): Lower quality
```

**Difficulté principale :** les schémas prosodiques sont propres à chaque langue. Un locuteur anglais cloné qui parle mandarin peut sonner étranger dans le rythme, même si le timbre est parfait. VoxCPM2 et OmniVoice optimisent spécifiquement ce point.

**Clonage à partir d'une référence minimale (état de l'art 2026) :**

| Modèle | Référence minimale | Langues | Cross-lingual | Notes |
|--------|--------------------|---------|---------------|-------|
| OmniVoice | Quelques secondes | 600+ | Oui, zero-shot | Ingestion robuste au bruit |
| VoxCPM2 | Clip court | 30+ | Oui | Diffusion-AR préserve l'émotion |
| Voxtral 4B | 3 secondes | 9 | Limité | Capture l'accent et les disfluences |
| Qwen3.5-Omni | Envoi de voix | 36 TTS | Oui, 20 langues testées | WER 1,87 selon les langues, similarité cosinus 0,79 |

Qwen3.5-Omni offre la meilleure fidélité de clonage mesurée (WER 1,87 sur 20 langues), mais n'est accessible que via API.

## Contrôle de l'émotion et du style {#emotion-and-style-control}

Les modèles de clonage récents prennent en charge l'injection d'émotions par balises :

```text
Tag-controlled generation (OmniVoice, Orpheus):
  Input: "I can't believe it! [surprise] This is amazing [joy]"
  Tags: [laugh], [surprise], [sadness], [whisper], [shouting]
  
  The model generates speech with corresponding emotional inflection
  at tagged positions, while maintaining target speaker's voice identity.
```

## Préparation de l'audio de référence {#reference-audio-preparation}

```text
Optimal reference characteristics:
  Duration:    10-30 seconds (sweet spot for most models)
  Content:     Natural speech, varied intonation, no music/effects
  Quality:     Clean recording, low noise floor, no reverb
  Format:      WAV 16-bit, 24kHz+ sample rate, mono
  Speaker:     Single speaker, consistent voice (no whispering then shouting)

Preprocessing pipeline:
  1. Source separation (UVR5 / Demucs) - remove background music
  2. Noise reduction (DeepFilterNet / RNNoise) - reduce ambient noise
  3. Trim silence (ffmpeg silenceremove) - remove dead air
  4. Normalize loudness (ffmpeg loudnorm) - consistent level
  5. Resample to model's expected rate (usually 24kHz)
```

## Mélange de voix : créer de nouvelles identités vocales {#voice-mixing-creating-novel-voice-identities}

Les modèles TTS modernes exposent les embeddings de locuteur sous forme de vecteurs. Mélanger ces embeddings permet de créer des voix qui ne correspondent à aucune personne réelle.

### Interpolation linéaire (Cartesia Sonic) {#linear-interpolation-cartesia-sonic}

Cartesia Sonic utilise des embeddings de locuteur de 192 dimensions (flottants compris entre -1 et 1) :

```python
import numpy as np

def mix_voices(embedding_a: np.ndarray, embedding_b: np.ndarray, 
               weight_a: float = 0.5) -> np.ndarray:
    """Linear interpolation between two speaker embeddings."""
    weight_b = 1.0 - weight_a
    return weight_a * embedding_a + weight_b * embedding_b

# Via Cartesia API:
import requests

new_voice = requests.post("https://api.cartesia.ai/voices", json={
    "name": "Custom Mix",
    "embedding": mix_voices(voice_a_embedding, voice_b_embedding, 0.6).tolist()
}).json()
```

**Attention :** la perception ne varie pas linéairement avec le coefficient d'interpolation. Un mélange 50/50 peut nécessiter des poids inégaux (par exemple 0,7/0,3) pour obtenir un rendu perceptuellement équilibré. Utiliser des embeddings prototypes (contrôles de vitesse et d'émotion) pour affiner les caractéristiques.

### Interpolation linéaire sphérique (slerp) - méthode de recherche {#spherical-linear-interpolation-slerp-research-method}

Le slerp préserve la norme du vecteur sur l'hypersphère de grande dimension, ce qui réduit les artefacts par rapport à l'interpolation linéaire. Utilisé dans VoxMorph (ICASSP 2026) :

```python
def slerp(a: np.ndarray, b: np.ndarray, t: float) -> np.ndarray:
    """Spherical linear interpolation between two embedding vectors."""
    a_norm = a / np.linalg.norm(a)
    b_norm = b / np.linalg.norm(b)
    
    dot = np.clip(np.dot(a_norm, b_norm), -1.0, 1.0)
    theta = np.arccos(dot)
    
    if np.abs(theta) < 1e-6:
        return a  # vectors nearly identical
    
    return (np.sin((1 - t) * theta) * a + np.sin(t * theta) * b) / np.sin(theta)
```

**Avantage de VoxMorph :** il sépare l'embedding de prosodie (rythme, hauteur) de l'embedding de timbre (conduit vocal, formants). Il peut combiner indépendamment le style d'élocution du locuteur A et la texture vocale du locuteur B. Entrée : 5 secondes par locuteur source, en zero-shot.

### Méthode INSIDE (génération d'identités inédites) {#inside-method-novel-identity-generation}

Sélectionne des paires d'embeddings de locuteur voisins et calcule des identités intermédiaires via slerp. Crée des voix qui « comblent les vides » de l'espace des embeddings entre des locuteurs réels. Validée : amélioration de +5,24 % en vérification du locuteur et gain de +13,44 % en classification du genre.

## Ce qui rend les voix synthétiques peu naturelles {#what-makes-synthetic-voices-sound-unnatural}

Les défauts de naturel les plus courants, et les modèles qui les traitent le mieux :

| Problème | Symptôme | Meilleures solutions |
|----------|----------|----------------------|
| Prosodie plate | Monotonie quel que soit le contenu | Sesame CSM (sensible au contexte), Fish S2 (plus de 15 000 balises) |
| Micro-pauses absentes | Espacement uniforme entre les mots | Sesame CSM (hésitations naturelles « umm/uhh »), VoxCPM2 (sans tokenisation) |
| Respiration absente | Aucune inspiration entre les phrases | Orpheus TTS (`<sigh>`, respiration naturelle) |
| Platitude émotionnelle | Même intonation pour une blague et une tragédie | Fish S2 Pro (émotion au niveau sous-mot), IndexTTS-2.5 (vecteur 8D) |
| Compression de la plage de hauteur | Plage tonale plus étroite que celle d'un humain | VoxCPM2 48 kHz (sans perte de tokenisation), CosyVoice 3 (RL) |
| Ignorance du contexte | Les mots sont lus, pas compris | Sesame CSM (modélisation du contexte conversationnel) |
| Transitions robotiques | Frontières de mots « concaténées » | Modèles alignés par RL (Fish S2, CosyVoice 3) |

**Contournements pratiques :**
- Insérer des virgules, des points de suspension et des marqueurs de micro-pause pour guider la prosodie
- Utiliser les balises propres à chaque modèle (`[laugh]`, `[excited]`, `[whisper]`) pour l'expressivité
- Fournir un historique de conversation aux modèles sensibles au contexte (Sesame CSM)
- Le post-entraînement aligné par RL améliore le naturel sans modifier l'architecture

## Repères de naturel (2026) {#naturalness-benchmarks-2026}

| Modèle | MOS | Taux de victoire | Notes |
|--------|-----|------------------|-------|
| Sesame CSM | 4,7 | quasi humain (sans contexte) | Anglais uniquement |
| Cartesia Sonic 2 | 4,7 | — | ~90 ms de TTFB |
| Orpheus TTS | 4,6 | — | Basé sur Llama-3B |
| Fish S2 Pro (EN) | 4,50 expressif / 4,21 naturel | Bradley-Terry 3,07, n° 1 | face à tous les principaux concurrents |
| Fish S2 Pro (ZH) | 4,94 expressif / 4,40 naturel | — | Le plus performant en chinois |
| Parole humaine | ~4,5-4,8 | Référence | Varie selon l'enregistrement |

**Tendance clé :** l'écart de qualité entre les meilleurs TTS open source et les TTS commerciaux est passé d'environ 1,0 MOS (2023) à 0,1-0,2 MOS (2026). Fish S2 Pro devance gpt-4o-mini-tts sur EmergentTTS-Eval (taux de victoire de 81,88 %). Voxtral devance ElevenLabs Flash v2.5 lors de tests en aveugle.

## Sécurité et éthique {#safety-and-ethics}

- **Consentement** : le clonage vocal sans le consentement du locuteur est illégal dans de nombreuses juridictions
- **Détection des deepfakes** : la parole générée peut être détectée par analyse spectrale, par filigrane (AudioSeal de Meta) ou par détection d'artefacts
- **Filigrane** : certains modèles (LEMAS, CosyVoice) intègrent des filigranes inaudibles dans l'audio généré
- **Limitation de débit** : les déploiements en production doivent limiter le nombre de requêtes de clonage par utilisateur ou par clé API
- **Vérification du locuteur** : associer les API de clonage à une vérification du locuteur pour confirmer que la personne qui envoie l'audio est bien le propriétaire de la voix

## Pièges à éviter {#gotchas}

- **Les références courtes se dégradent sur les phonèmes rares** - un clip de 5 secondes peut ne pas contenir assez de diversité phonétique. Le modèle invente les sons manquants, parfois de façon incohérente. Utiliser des références de 15 à 30 secondes au contenu varié. Exception : Voxtral 4B est spécifiquement conçu pour des références de 3 secondes
- **Le bruit de fond de la référence se retrouve en sortie** - même une faible réverbération de pièce ou un bourdonnement de climatisation sont encodés dans l'embedding de locuteur et apparaissent dans toute la parole générée. Toujours débruiter au préalable. Exception : OmniVoice gère explicitement les échantillons de référence bruités
- **Transfert d'accent entre langues** - si la référence est en anglais, la parole chinoise générée a souvent un rythme à l'accent anglais. Fournir une référence dans la langue cible (même quelques secondes) améliore nettement les résultats
- **Clonage via API uniquement = dépendance au fournisseur** - Qwen3.5-Omni offre la meilleure qualité de clonage mesurée, mais n'est accessible que via API. Prévoir des solutions de repli vers des modèles ouverts (OmniVoice, VoxCPM2) pour les systèmes en production

## Voir aussi {#see-also}

- [[tts-models]] - architectures de modèles et tableau comparatif
- [[voice-conversion]] - modification de l'identité vocale dans des enregistrements existants
- [[speech-recognition]] - ASR pour l'alignement basé sur la transcription dans les pipelines de clonage

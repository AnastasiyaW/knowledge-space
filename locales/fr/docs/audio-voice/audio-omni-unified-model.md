---
level: 3
source_sha256: b44a0f31126dfe84f2c8583253be3175affe626e426f162451747656240c14ac
translation: machine
translated_at: '2026-10-24'
---
# Audio-Omni : compréhension, génération et édition audio unifiées {#audio-omni-unified-audio-understanding-generation-and-editing}

Modèle unique pour la compréhension, la génération et l'édition audio, combinant le raisonnement d'un LLM gelé et la synthèse par un Diffusion Transformer (DiT) entraînable. [arxiv 2604.10708] SIGGRAPH 2026.

## Architecture {#architecture}

Conception en deux composants : un LLM multimodal gelé assure le raisonnement et le conditionnement ; un DiT entraînable assure la synthèse audio haute fidélité.

```text
Text / Audio / Video input
         ↓
  ┌─────────────────────────────────────┐
  │  FROZEN Qwen2.5-Omni (multimodal)   │  ← reasoning, context, knowledge
  │  - Audio encoder                    │
  │  - Text encoder                     │
  │  - Cross-modal reasoning            │
  └─────────────────────────────────────┘
         ↓  semantic conditioning
  ┌─────────────────────────────────────┐
  │  TRAINABLE Diffusion Transformer    │  ← high-fidelity synthesis
  │  - Audio latent diffusion           │
  │  - Conditioned on LLM embeddings    │
  └─────────────────────────────────────┘
         ↓
  Generated / edited audio
```

**Pourquoi geler le LLM :** préserve les connaissances générales, réduit le coût de calcul de l'entraînement et permet une adaptation zero-shot par prompting plutôt qu'un fine-tuning par tâche.

Les tâches vidéo-vers-audio utilisent en plus un checkpoint Synchformer pour l'alignement temporel entre image et son.

## Capacités {#capabilities}

### Compréhension {#understanding}
- Sous-titrage audio et questions-réponses
- Analyse de la parole : genre, nombre de locuteurs, détection du sarcasme
- Classification de sons et identification de sources
- Reconnaissance de la scène sonore ambiante

### Génération {#generation}
- Texte-vers-audio (sons environnementaux, foley)
- Texte-vers-musique (à partir d'une vidéo ou d'un texte)
- Vidéo-vers-audio
- Vidéo-vers-musique (bande-son)
- Synthèse vocale (TTS)
- Conversion de voix zero-shot

### Édition (au niveau du mot ou du segment) {#editing-wordsegment-level}
L'édition audio est la capacité différenciante : aucun modèle ouvert comparable ne fournit les quatre opérations :

```python
# Add a sound element to existing audio
model.edit("Add", "input.wav", desc="skateboarding sounds")

# Remove a specific element
model.edit("Remove", "input.mp3", desc="female singing")

# Extract a specific element
model.edit("Extract", "input.wav", desc="piano melody")

# Apply style transfer
model.edit("Style", "input.wav", desc="lo-fi hip hop")

# Replace a word/phrase in speech
model.edit("Speech", "input.wav", desc="replace 'hello' with 'goodbye'")
```

## Spécifications techniques {#technical-specs}

| Paramètre | Valeur |
|---|---|
| LLM de base | Qwen2.5-Omni (gelé) |
| Taille du checkpoint | ~21 Go |
| Paramètres estimés | ~8–14B (bf16) |
| Licence | **CC-BY-NC-4.0** (non commerciale) |
| Langues | EN, CN, JA, FR, DE |
| Russe | Non pris en charge |
| VRAM (inférence) | 24 Go minimum ; 40+ Go recommandés |
| Python | 3.11 |
| Audio de référence (clonage vocal) | Zero-shot (aucune durée minimale spécifiée) |
| Recette de fine-tuning / LoRA | Non fournie |
| Licence commerciale | Sur demande uniquement |

## Données d'entraînement {#training-data}

Jeu de données **AudioEdit** : plus d'un million de paires d'édition sélectionnées, créées spécifiquement pour les tâches d'édition audio. Sa disponibilité en tant que jeu de données ouvert autonome n'est pas confirmée à la date de rédaction. S'il est publié, il serait précieux pour entraîner des capacités d'édition au-dessus de bases TTS sous licence commerciale.

## Comparaison : Audio-Omni et TTS spécialisés {#comparison-audio-omni-vs-specialized-tts}

| Aspect | Audio-Omni | VoxCPM2 | OmniVoice | Fish S2 Pro |
|---|---|---|---|---|
| Architecture | LLM gelé + DiT | Diffusion-AR sans tokenizer | Basée sur l'attention | Dual-AR + RLHF |
| Paramètres | ~8–14B | 2B | Non divulgué | 4,4B |
| Langues | 5 | 30+ | 600+ | 80+ |
| Russe | Non | Oui | Oui | Oui |
| Clonage vocal | Zero-shot | Zero-shot + fine-tuning | Zero-shot inter-langues | Référence de 10–30 s |
| Édition au niveau du mot | **Oui** | Non | Non | Non |
| Compréhension audio | **Oui** | Non | Non | Non |
| Fine-tuning / LoRA | Pas de recette | Oui | Incertain | Oui |
| Licence | CC-BY-NC-4.0 | Apache 2.0 | Ouverte | Poids ouverts |
| Usage commercial | Non (sans accord) | Oui | Oui | Oui |

Audio-Omni sacrifie la couverture linguistique et l'usage commercial au profit de l'étendue des capacités. Les modèles TTS spécialisés surpassent Audio-Omni sur la qualité du TTS monolingue et sur la prise en charge multilingue.

## Motif d'architecture : raisonnement gelé et synthèse entraînable {#architectural-pattern-frozen-reasoning-trainable-synthesis}

Ce motif de conception, un LLM gelé partagé comme socle de raisonnement au-dessus d'un module de synthèse entraînable, se généralise au-delà de ce modèle :

- Nouvelles tâches = nouveaux prompts adressés au LLM gelé, sans réentraînement
- Le raisonnement et la génération peuvent être mis à jour indépendamment
- Le LLM gelé fournit un retour pédagogique ancré (par exemple, explication des erreurs au niveau du phonème dans la parole)

**Alternatives d'implémentation de l'édition de parole au niveau du mot** (pour les systèmes sous licence commerciale) :
1. Inpainting par diffusion conditionné par un prompt (nécessite une architecture de diffusion comme VoxCPM2)
2. Alignement phonémique + extraction avec AudioSep → inpainting TTS dans la voix cible → réinsertion
3. Entraîner un LoRA d'édition sur une base à usage commercial ouvert à partir du jeu de données AudioEdit (si publié)

## Motif d'API unifiée {#unified-api-pattern}

```python
# Demonstrates clean interface separation between tasks
model.understand("transcribe", audio_path)          # understanding
model.generate("tts", text="Hello world", ref=ref_audio)  # generation
model.edit("Add", audio_path, desc="rain sounds")  # editing
```

Cette conception d'API à trois espaces de noms (comprendre / générer / éditer) sépare clairement les intentions et mérite d'être reprise dans les services de workers audio.

## Pièges {#gotchas}

- **Problème :** un checkpoint de 21 Go nécessite 24+ Go de VRAM pour l'inférence → **Solution :** utiliser une A100 80 Go ou une H100 ; les cartes grand public de 24 Go (RTX 4090/3090) sont à la limite absolue, sans marge pour le batching
- **Problème :** la licence CC-BY-NC-4.0 interdit l'usage commercial → **Solution :** contacter les auteurs pour une licence commerciale (`ztianad@connect.ust.hk`) ; pour les systèmes de production commerciaux, utiliser des alternatives Apache 2.0 (VoxCPM2, Fish S2 Pro)
- **Problème :** aucune prise en charge du russe, alors que des alternatives couvrant 600 langues existent → **Solution :** pour la production en russe, utiliser OmniVoice (600+ langues) ou Fish S2 Pro avec fine-tuning
- **Problème :** aucune recette LoRA / fine-tuning fournie → **Solution :** impossible de s'adapter à des voix ou domaines personnalisés sans implémenter un pipeline d'entraînement maison ; les modèles spécialisés (Fish S2 Pro, VoxCPM2) proposent des voies de fine-tuning documentées

## Voir aussi {#see-also}

- [[tts-models]]
- [[voice-cloning]]
- [[voice-conversion]]

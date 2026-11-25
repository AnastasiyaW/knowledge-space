---
title: "LEMAS : TTS multilingue et édition de la parole"
description: "Modèles open source LEMAS de synthèse vocale (TTS) multilingue et d'édition de la parole au niveau du mot : architecture, installation, prise en charge de 10 langues et comparaison avec F5-TTS et CosyVoice."
level: 3
source_sha256: 15ce79c7a45a1bb0772d361a4f740a9f8ee448de3c65ea57f80b40ae0426d21e
translation: machine
translated_at: '2026-10-24'
---
# LEMAS : TTS multilingue et édition de la parole {#lemas-multilingual-tts-and-speech-editing}

Plus de 150 000 heures de données audio multilingues d'entraînement couvrant 10 langues, à partir desquelles sont issus deux modèles complémentaires : TTS zero-shot et édition de la parole au niveau du mot. CC-BY-4.0.

## Modèles {#models}

| Modèle | Taille | Tâche | Architecture |
|-------|------|------|-------------|
| LEMAS-TTS | 0.3B | TTS zero-shot | Flow matching (basé sur F5-TTS) |
| LEMAS-Edit | 0.3B | Édition de la parole | Flow matching + codec AR (basé sur VoiceCraft) |

## Langues {#languages}

Chinois, anglais, espagnol, russe, français, allemand, italien, portugais, indonésien, vietnamien

## LEMAS-TTS {#lemas-tts}

Clonage vocal zero-shot : un extrait de référence de 5 à 10 secondes → génération de parole dans l'une des 10 langues.

**Paramètres :**
- `nfe_steps` - nombre d'évaluations de fonction (compromis vitesse/qualité)
- `cfg_strength` - intensité du guidage sans classifieur (classifier-free guidance)
- `speed` - multiplicateur du débit de la parole en sortie
- Débruitage UVR5 (facultatif, améliore la qualité sur des références bruitées)

```bash
# Install
conda create -n lemas python=3.10 && conda activate lemas
sudo apt-get install -y ffmpeg  # or conda install -c conda-forge ffmpeg
git clone https://github.com/LEMAS-Project/LEMAS-TTS.git
cd LEMAS-TTS && pip install -r requirements.txt
# Download model weights from HuggingFace to pretrained_models/

# Launch Gradio UI
export PYTHONPATH="$PWD:${PYTHONPATH}"
python lemas_tts/scripts/inference_gradio.py --host 0.0.0.0 --port 7860 --share
```

Space HuggingFace : `LEMAS-Project/LEMAS-TTS`

## LEMAS-Edit {#lemas-edit}

Remplacement de mots dans la parole sans régénérer l'énoncé complet. Préserve les caractéristiques vocales de la parole environnante.

**Deux backends :**

| Backend | Langues | Méthode |
|---------|-----------|--------|
| `lemas_tts` (flow matching) | 10 langues | Identique au TTS |
| `lemas_edit` (codec AR) | 7 langues | Alignement WhisperX + MMS |

Le backend `lemas_edit` offre une meilleure naturalité pour les modifications en milieu de phrase ; `lemas_tts` couvre un plus grand nombre de langues.

Évaluation : tests MUSHRA et ABX inclus dans `./eval/`.

Space HuggingFace : `LEMAS-Project/LEMAS-Edit`

## Dépendances amont {#upstream-dependencies}

F5-TTS, VoiceCraft, Vocos, UVR5, DeepFilterNet, Seamless-Expressive

## Panorama des TTS ouverts (avril 2026) {#open-tts-landscape-april-2026}

| Modèle | Organisation | Points forts |
|-------|-----|-----------|
| LEMAS-TTS | LEMAS Project | 10 langues, zero-shot, CC-BY-4.0 |
| F5-TTS | - | Architecture de base sur laquelle s'appuie LEMAS |
| CosyVoice 2 | Alibaba | Chinois solide, multi-locuteurs |
| Fish Speech | - | Inférence rapide, bon en EN/ZH |
| Kokoro TTS | - | Haute qualité en anglais |
| Orpheus TTS | Canopy AI | Expressif, large gamme émotionnelle |
| Dia | Nari Labs | Optimisé pour le dialogue |

## Chaîne de clonage vocal {#voice-cloning-pipeline}

Pour la génération audio continue (par exemple, systèmes d'apprentissage, assistants vocaux) :

```python
# Architecture pattern for background audio generation
# 1. Claude API → lesson text (~2 min on voice)
# 2. LEMAS-TTS → synthesize to mp3 with cloned voice
# 3. Schedule + notification (plyer / win10toast)
# 4. Auto-play in background

# Container: pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime
# GPU: single modern GPU sufficient for 0.3B model
# Latency: real-time factor < 0.5 on T4 GPU
```

## Pièges à éviter {#gotchas}

- **Le flow matching impose un nombre NFE fixe** - contrairement aux modèles de diffusion, LEMAS-TTS ne prend pas en charge un nombre variable d'étapes en cours de génération. Définissez NFE une seule fois par exécution.
- **La qualité de l'audio de référence influe directement sur le résultat** - des références bruitées ou réverbérantes produisent des clones bruités. Appliquez le débruitage UVR5 aux références avant utilisation.
- **La détection de la langue est implicite** - le modèle ne détecte pas automatiquement la langue source. Vous devez spécifier explicitement la langue cible. Les combinaisons langue/texte incohérentes dégradent la sortie.
- **Le codec AR de `lemas_edit` est plus lent** - la génération autorégressive est plus lente que le flow matching. Pour les applications à faible latence, utilisez le backend `lemas_tts` même pour l'édition.

## Voir aussi {#see-also}

- [[tts-models]]
- [[voice-cloning]]
- [[voice-agent-pipelines]]

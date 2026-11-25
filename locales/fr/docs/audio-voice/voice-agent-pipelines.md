---
title: "Pipelines et frameworks d'agents vocaux"
category: reference
tags: [voice-ai, pipecat, livekit, webrtc, vad, latency, speech-to-speech, cascaded-pipeline, end-to-end]
level: 3
source_sha256: aba7a3b8d3f4144799bea33fe8a713057f3255fb5b19dbd3225824c1bd5c76ac
translation: machine
translated_at: '2026-10-24'
---
# Pipelines et frameworks d'agents vocaux {#voice-agent-pipelines-and-frameworks}

Construction de systèmes d'IA vocale en temps réel : choix du framework, optimisation de la latence, configuration du VAD et décisions d'architecture entre pipelines de bout en bout et pipelines en cascade.

## Points clés {#key-facts}

- Tolérance de la conversation humaine : latence de bout en bout de 300 à 500 ms
- Standard de l'industrie pour l'IA vocale : 600 à 800 ms (cible atteignable)
- Budget d'un pipeline en cascade (STT → LLM → TTS) : ~100 à 500 ms pour le STT + ~350 ms à 1 s pour le LLM + ~75 à 200 ms pour le TTS
- WebRTC (UDP) préféré à WebSocket (TCP) pour l'audio : annulation d'écho, suppression du bruit et tampon de gigue intégrés
- Les modèles de bout en bout (un seul modèle gère l'audio en entrée et en sortie) ont une latence plus faible mais sont moins contrôlables
- Les pipelines en cascade sont plus faciles à déboguer, permettent de mettre à niveau chaque composant individuellement et de les régler selon le cas d'usage

## Comparatif des frameworks {#framework-comparison}

| Framework | Idéal pour | Licence | Atout principal |
|-----------|----------|---------|-------------|
| Pipecat (Daily) | Flexibilité maximale | Open source | Plus de 40 intégrations, composable |
| LiveKit Agents | Orienté WebRTC | Open source | API claire, multi-langage |
| TEN (Agora) | Multimodal, éditeur visuel | Open source | 98 % de précision de détection de tour |
| Bolna | Téléphonie + WebSocket | Open source | Déploiement téléphonique rapide |
| Vocode | Prototypage rapide | Open source | 10 lignes pour démarrer |

**Guide de sélection :**
- Orienté WebRTC, configuration minimale → **LiveKit Agents**
- Flexibilité maximale, nombreuses intégrations → **Pipecat**
- Multimodal (audio + vision) → **TEN Framework**
- Téléphonie (SIP, RTC) → **Bolna** ou Vapi
- Volume > 10 000 min/mois → développer avec LiveKit/Pipecat (coût d'un service managé trop élevé)
- Volume < 10 000 min/mois → Vapi ou Retell (plateformes managées)

## Pipeline Pipecat {#pipecat-pipeline}

```python
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.transports.services.daily import DailyTransport, DailyParams

transport = DailyTransport(
    room_url, token, "Voice Bot",
    DailyParams(audio_in_enabled=True, audio_out_enabled=True)
)

stt = DeepgramSTTService(api_key=DEEPGRAM_KEY, model="nova-3")
llm = OpenAILLMService(api_key=OPENAI_KEY, model="gpt-4o-mini")
tts = CartesiaTTSService(api_key=CARTESIA_KEY, voice_id="...")

pipeline = Pipeline([
    transport.input(),
    stt,
    llm,
    tts,
    transport.output()
])

runner = PipelineRunner()
await runner.run(pipeline)
```

## LiveKit Agents {#livekit-agents}

```python
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, openai, silero

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="nova"),
        # Interrupt on any speech:
        allow_interruptions=True,
        interrupt_speech_duration=0.5,
    )
    
    assistant.start(ctx.room)
    await assistant.say("Hello! How can I help you?", allow_interruptions=False)
    await asyncio.sleep(3600)  # keep alive

cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
```

## VAD (Voice Activity Detection) {#vad-voice-activity-detection}

La précision du VAD est critique : les faux positifs gaspillent des tokens LLM, les faux négatifs coupent la parole des utilisateurs.

| VAD | Idéal pour | Précision | Langage |
|-----|----------|---------|-------------|
| Silero VAD | Python/recherche, open source | Élevée | Python |
| Cobra VAD (Picovoice) | Entreprise, faible latence | 99 % | Multi |
| TEN VAD | Meilleure précision | Supérieure | Multi |
| VAD sémantique | Prédiction de fin de tour par la prosodie | Sensible au contexte | — |

**Configuration de Silero VAD :**
```python
import torch
from silero_vad import load_silero_vad, get_speech_timestamps

model = load_silero_vad()

def detect_speech(audio_chunk: bytes, sample_rate: int = 16000) -> bool:
    tensor = torch.frombuffer(audio_chunk, dtype=torch.int16).float() / 32768.0
    speech_prob = model(tensor, sample_rate).item()
    return speech_prob > 0.5  # threshold tunable

# For streaming detection with state:
vad_iterator = VADIterator(model, threshold=0.5, sampling_rate=16000,
                            min_silence_duration_ms=300, speech_pad_ms=100)
```

**VAD sémantique** (prédit la fin du tour à partir des motifs prosodiques, et pas seulement du silence) :
- Évite de couper un utilisateur en pleine réflexion lorsqu'il marque une pause pour insister
- Plus difficile à implémenter, nécessite un modèle audio ou un LSTM sur des caractéristiques prosodiques

## Optimisation de la latence {#latency-optimization}

### Répartition du budget (en cascade) {#budget-breakdown-cascaded}

```text
Total budget: 800ms target

STT (Deepgram Nova-3):  ~100-200ms  (streaming: first words in ~150ms)
LLM (GPT-4o-mini):      ~300-600ms  (first token in ~300ms with streaming)
TTS (Cartesia Sonic):   ~90ms TTFB  (streaming to audio)
Transport (WebRTC):     ~50ms       (UDP, minimal jitter)

Total achievable:        540-950ms
```

### Stratégies d'optimisation clés {#key-optimization-strategies}

**1. Génération spéculative pendant que l'utilisateur parle :**
```python
# Start pre-computing while VAD still shows speech
# If STT changes final transcript, discard pre-computed tokens
async def speculative_generate(partial_transcript: str):
    if len(partial_transcript) > 20:  # enough context
        # Begin LLM streaming, cancel if transcript changes significantly
        async for token in llm.stream(partial_transcript):
            if transcript_changed():
                break
            buffer_token(token)
```

**2. Quantification du LLM :**
- Quantification 4 bits → réduction de latence de 40 %, perte de qualité minime pour la conversation
- Déployer localement un modèle 7B quantifié plutôt qu'un grand modèle cloud : qualité souvent comparable pour une latence trois fois plus faible

**3. Réutilisation des connexions :**
```python
# WebSocket/gRPC connection pools - avoid TLS handshake per request
# Deepgram streaming: one persistent WebSocket per call, not per utterance
class PersistentDeepgramConnection:
    def __init__(self):
        self._ws = None
    
    async def ensure_connected(self):
        if not self._ws or self._ws.closed:
            self._ws = await deepgram.connect()  # persistent
```

**4. Mise en cache vocale des phrases courantes :**
```python
from functools import lru_cache

@lru_cache(maxsize=256)
def get_cached_audio(phrase: str, voice_id: str) -> bytes:
    return tts_service.synthesize(phrase, voice_id)

# Cache greetings, errors, confirmations:
COMMON_PHRASES = [
    "I didn't quite catch that.",
    "Could you repeat that?",
    "One moment please."]
# Pre-warm cache on startup
for phrase in COMMON_PHRASES:
    get_cached_audio(phrase, VOICE_ID)
```

**5. Colocalisation régionale :**
- Déployer le STT, le LLM et le TTS dans la même région de data center
- Cible : <10 ms entre les appels de service (réseau local contre 80 ms inter-régions)

## Configuration audio WebRTC {#webrtc-audio-configuration}

```javascript
// Client-side (browser):
const pc = new RTCPeerConnection({
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
});

const stream = await navigator.mediaDevices.getUserMedia({
    audio: {
        echoCancellation: true,     // prevent feedback loop
        noiseSuppression: true,     // reduce background noise
        autoGainControl: true,      // normalize volume
        sampleRate: 16000,          // match STT model expectation
        channelCount: 1,            // mono sufficient
    }
});

pc.addTrack(stream.getAudioTracks()[0], stream);
```

**Paramètres du codec Opus** (utilisé par WebRTC pour l'audio) :
- Taille de trame : 20 ms (standard)
- Débit binaire : 32 à 96 kbps pour la voix (32 suffisent pour la qualité STT)
- L'annulation d'écho est critique pour éviter l'auto-interruption lorsque la sortie du TTS revient dans le microphone

## Architecture de bout en bout et en cascade {#end-to-end-vs-cascaded-architecture}

| | Bout en bout | En cascade (STT→LLM→TTS) |
|---|---|---|
| Latence | Plus faible (modèle unique) | Plus élevée (3 allers-retours) |
| Prosodie | Meilleure (audio natif) | Plus robotique (le texte sert d'intermédiaire) |
| Contrôlabilité | Difficile à déboguer | Remplacement indépendant des composants |
| Support linguistique | Plus restreint (dépend du modèle) | Meilleur composant par langue |
| Coût | 0,30 à 1,50 $/min | Varie selon les composants choisis |
| Idéal pour | Chatbots grand public | Entreprise, apprentissage des langues |

**Recommandation :** Commencer par une architecture en cascade dans presque tous les cas. Viser une latence médiane de 800 ms. Ne passer au bout en bout que si le plafond de latence de la cascade est insuffisant et que la prosodie est critique.

**Modèles de bout en bout à considérer :**
- Gemini 3.1 Flash Live - plus de 90 langues, <500 ms, accessible uniquement par API
- Qwen3-Omni - 10 langues parlées, appels de fonctions, poids ouverts
- Moshi (Kyutai) - 7B, full-duplex, poids ouverts

## Gestion de plusieurs locuteurs {#multi-speaker-handling}

```python
class MultiSpeakerPipeline:
    """Handles interruptions and overlapping speech correctly."""
    
    def __init__(self):
        self.current_speaker = None
        self.tts_task = None
    
    async def on_speech_start(self, participant_id: str):
        if self.current_speaker != participant_id and self.tts_task:
            # Interrupt current TTS when user speaks:
            self.tts_task.cancel()
            await self.tts_service.stop()
        self.current_speaker = participant_id
    
    async def on_transcript_complete(self, text: str, participant_id: str):
        response = await self.llm.complete(text)
        self.tts_task = asyncio.create_task(
            self.tts_service.speak(response)
        )
```

## Modèles speech-to-speech (2025-2026) {#speech-to-speech-models-2025-2026}

| Modèle | Latence | Langues | Licence | Notes |
|-------|---------|-----------|---------|-------|
| Qwen3-Omni | ~119 ms | 19 en entrée / 10 en sortie | Qwen | MoE 30B/3B actifs, appels de fonctions |
| Gemini Live API | <500 ms | 70 | Propriétaire | WebSocket, barge-in, dialogue affectif |
| NVIDIA PersonaPlex | 205 ms | EN | MIT | Basé sur Moshi, 7B, 100 % de réussite des interruptions |
| Voila (Maitrix) | 195 ms | 6 (sans RU) | Apache 2.0 | Full-duplex, plus de 1 M de voix préenregistrées |
| Chroma 1.0 (FlashLabs) | 147 ms | EN | Apache 2.0 | 4B paramètres, RTF 0,43 |
| Ultravox v0.6 (Fixie) | ~150 ms | Multi | Apache 2.0 | LLM multimodal natif pour la parole |
| Moshi (Kyutai) | — | EN | CC-BY 4.0 | 7B, TTS léger de 100M pour CPU |
| Sesame CSM | — | EN | Apache 2.0 | Franchit la vallée de l'étrange, disfluences naturelles |
| OpenAI Realtime API | >1 s | Multi | Propriétaire | 0,50 $/appel de 5 min, MCP, WebRTC, SIP |

## Pièges courants {#gotchas}

- **L'annulation d'écho est obligatoire, pas optionnelle** - sans `echoCancellation: true` dans les contraintes de getUserMedia, la sortie du TTS passée par les haut-parleurs revient dans le microphone et le STT transcrit en continu ce que le bot vient de dire. Cela crée des boucles infinies dans le pipeline. Activer systématiquement l'AEC (Acoustic Echo Cancellation, annulation acoustique d'écho) côté client
- **Le seuil de durée de silence du VAD dépend de la conversation** - un seuil de 300 ms convient aux bots FAQ, mais coupe les utilisateurs des applications d'apprentissage des langues qui marquent une pause pour réfléchir. Régler `min_silence_duration_ms` selon le cas d'usage ; envisager le VAD sémantique lorsque les pauses de réflexion comptent
- **Les tokens en streaming du LLM ne correspondent pas aux frontières de phrases du TTS** - la plupart des systèmes TTS ont besoin de phrases complètes pour une prosodie naturelle. Transmettre chaque token au TTS produit une parole robotique mot par mot. Mettre en tampon les tokens jusqu'à une frontière de phrase (`.`, `?`, `!`) ou pendant 100 ms de streaming, puis synthétiser la phrase complète

## Voir aussi {#see-also}

- [[audio-voice/tts-models]] - Sélection et comparaison de modèles TTS
- [[audio-voice/voice-cloning]] - Clonage vocal zero-shot pour des agents personnalisés
- [[audio-voice/speech-recognition]] - Modèles STT et benchmarks de précision

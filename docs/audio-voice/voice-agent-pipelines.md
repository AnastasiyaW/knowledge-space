---
title: Voice Agent Pipelines and Frameworks
category: reference
tags: [voice-ai, pipecat, livekit, webrtc, vad, latency, speech-to-speech, cascaded-pipeline, end-to-end]
---

# Voice Agent Pipelines and Frameworks

Building real-time voice AI systems: framework selection, latency optimization, VAD configuration, and architecture decisions between end-to-end and cascaded pipelines.

## Key Facts

- Human conversation tolerance: 300-500ms end-to-end latency
- Industry standard voice AI: 600-800ms (achievable target)
- Cascaded pipeline (STT → LLM → TTS) budget: ~100-500ms STT + ~350ms-1s LLM + ~75-200ms TTS
- WebRTC (UDP) preferred over WebSocket (TCP) for audio: built-in echo cancellation, noise suppression, jitter buffering
- End-to-end models (single model handles audio in/out) have lower latency but are less controllable
- Cascaded pipelines are easier to debug, upgrade individual components, and tune per use case

## Framework Comparison

| Framework | Best For | License | Key Strength |
|-----------|----------|---------|-------------|
| Pipecat (Daily) | Maximum flexibility | Open-source | 40+ integrations, composable |
| LiveKit Agents | WebRTC-first | Open-source | Clean API, multi-language |
| TEN (Agora) | Multimodal, visual builder | Open-source | 98% turn detection accuracy |
| Bolna | Telephony + WebSocket | Open-source | Quick telephony deployment |
| Vocode | Rapid prototyping | Open-source | 10 lines to start |

**Selection guide:**
- WebRTC-first, minimal setup → **LiveKit Agents**
- Maximum flexibility, many integrations → **Pipecat**
- Multimodal (audio + vision) → **TEN Framework**
- Telephony (SIP, PSTN) → **Bolna** or Vapi
- Volume > 10K min/month → build with LiveKit/Pipecat (managed cost too high)
- Volume < 10K min/month → Vapi or Retell (managed platforms)

## Pipecat Pipeline

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

## LiveKit Agents

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

## VAD (Voice Activity Detection)

VAD accuracy is critical - false positives waste LLM tokens; false negatives cut off users.

| VAD | Best For | Accuracy | Language |
|-----|----------|----------|----------|
| Silero VAD | Python/research, open-source | High | Python |
| Cobra VAD (Picovoice) | Enterprise, low latency | 99% | Multi |
| TEN VAD | Best precision | Superior | Multi |
| Semantic VAD | Prosody-aware turn prediction | Context-aware | — |

**Silero VAD configuration:**
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

**Semantic VAD** (predicts turn end from prosody patterns, not just silence):
- Avoids cutting off users mid-thought who pause for emphasis
- Harder to implement, requires audio model or LSTM on prosody features

## Latency Optimization

### Budget Breakdown (Cascaded)

```text
Total budget: 800ms target

STT (Deepgram Nova-3):  ~100-200ms  (streaming: first words in ~150ms)
LLM (GPT-4o-mini):      ~300-600ms  (first token in ~300ms with streaming)
TTS (Cartesia Sonic):   ~90ms TTFB  (streaming to audio)
Transport (WebRTC):     ~50ms       (UDP, minimal jitter)

Total achievable:        540-950ms
```

### Key Optimization Strategies

**1. Speculative generation while user speaks:**
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

**2. LLM quantization:**
- 4-bit quantization → 40% latency reduction, minimal quality loss for conversation
- Deploy local 7B model quantized vs cloud large model: often comparable quality at 3x lower latency

**3. Connection reuse:**
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

**4. Voice caching for common phrases:**
```python
from functools import lru_cache

@lru_cache(maxsize=256)
def get_cached_audio(phrase: str, voice_id: str) -> bytes:
    return tts_service.synthesize(phrase, voice_id)

# Cache greetings, errors, confirmations:
COMMON_PHRASES = [
    "I didn't quite catch that.",
    "Could you repeat that?",
    "One moment please.",
]
# Pre-warm cache on startup
for phrase in COMMON_PHRASES:
    get_cached_audio(phrase, VOICE_ID)
```

**5. Regional co-location:**
- Deploy STT, LLM, TTS in same data center region
- Target: <10ms between service calls (LAN vs 80ms cross-region)

## WebRTC Audio Configuration

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

**Opus codec settings** (used by WebRTC for audio):
- Frame size: 20ms (standard)
- Bitrate: 32-96 kbps for voice (32 sufficient for STT quality)
- Echo cancellation critical to prevent self-interruption when TTS output feeds back into microphone

## End-to-End vs Cascaded Architecture

| | End-to-End | Cascaded (STT→LLM→TTS) |
|---|---|---|
| Latency | Lower (single model) | Higher (3 round-trips) |
| Prosody | Better (native audio) | More robotic (text as bridge) |
| Controllability | Hard to debug | Swap components independently |
| Language support | Fewer (model-dependent) | Mix best-in-class per lang |
| Cost | $0.30-1.50/min | Varies by component choices |
| Best for | Consumer chatbots | Enterprise, language learning |

**Recommendation:** Start with cascaded in almost all cases. Target 800ms median latency. Move to end-to-end only if cascaded ceiling is too low and prosody is critical.

**End-to-end models worth considering:**
- Gemini 3.1 Flash Live - 90+ languages, <500ms, API-only
- Qwen3-Omni - 10 speech languages, function calling, open weights
- Moshi (Kyutai) - 7B, full-duplex, open weights

## Multi-Speaker Handling

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

## Speech-to-Speech Models (2025-2026)

| Model | Latency | Languages | License | Notes |
|-------|---------|-----------|---------|-------|
| Qwen3-Omni | ~119ms | 19 input / 10 output | Qwen | MoE 30B/3B active, function calling |
| Gemini Live API | <500ms | 70 | Proprietary | WebSocket, barge-in, affective dialog |
| NVIDIA PersonaPlex | 205ms | EN | MIT | Moshi-based, 7B, 100% interruption success |
| Voila (Maitrix) | 195ms | 6 (no RU) | Apache 2.0 | Full-duplex, 1M+ pre-built voices |
| Chroma 1.0 (FlashLabs) | 147ms | EN | Apache 2.0 | 4B params, RTF 0.43 |
| Ultravox v0.6 (Fixie) | ~150ms | Multi | Apache 2.0 | Speech-native multimodal LLM |
| Moshi (Kyutai) | — | EN | CC-BY 4.0 | 7B, pocket TTS 100M for CPU |
| Sesame CSM | — | EN | Apache 2.0 | Crosses uncanny valley, natural disfluency |
| OpenAI Realtime API | >1s | Multi | Proprietary | $0.50/5-min call, MCP, WebRTC, SIP |

## Gotchas

- **Echo cancellation is mandatory, not optional** - without `echoCancellation: true` in getUserMedia constraints, the TTS output from speakers feeds back into the microphone and the STT continuously transcribes what the bot just said. This creates infinite loops in the pipeline. Always enable AEC (Acoustic Echo Cancellation) on the client
- **VAD silence duration threshold is conversation-specific** - a 300ms silence threshold works for FAQ bots but cuts off users in language learning apps who pause to think. Tune `min_silence_duration_ms` per use case; consider semantic VAD for applications where thought pauses matter
- **LLM streaming tokens ≠ TTS sentence boundaries** - most TTS systems need complete sentences for natural prosody. Naively passing each token to TTS produces robotic word-by-word speech. Buffer tokens until sentence boundary (`.`, `?`, `!`) or after 100ms of streaming, then synthesize the complete sentence

## See Also

- [[audio-voice/tts-models]] - TTS model selection and comparison
- [[audio-voice/voice-cloning]] - zero-shot voice cloning for personalized agents
- [[audio-voice/speech-recognition]] - STT models and accuracy benchmarks

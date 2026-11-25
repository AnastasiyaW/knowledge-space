---
title: "Voice-Agent-Pipelines und Frameworks"
category: reference
tags: [voice-ai, pipecat, livekit, webrtc, vad, latency, speech-to-speech, cascaded-pipeline, end-to-end]
level: 3
source_sha256: aba7a3b8d3f4144799bea33fe8a713057f3255fb5b19dbd3225824c1bd5c76ac
translation: machine
translated_at: '2026-10-24'
---
# Voice-Agent-Pipelines und Frameworks {#voice-agent-pipelines-and-frameworks}

Entwicklung von Echtzeit-Voice-AI-Systemen: Auswahl des Frameworks, Latenzoptimierung, VAD-Konfiguration und Architekturentscheidungen zwischen End-to-End- und kaskadierten Pipelines.

## Kernfakten {#key-facts}

- Toleranz menschlicher Gespräche: 300–500 ms Ende-zu-Ende-Latenz
- Branchenstandard für Voice AI: 600–800 ms (erreichbares Ziel)
- Budget einer kaskadierten Pipeline (STT → LLM → TTS): ~100–500 ms STT + ~350 ms–1 s LLM + ~75–200 ms TTS
- WebRTC (UDP) gegenüber WebSocket (TCP) für Audio bevorzugt: integrierte Echounterdrückung, Rauschunterdrückung, Jitter-Pufferung
- End-to-End-Modelle (ein Modell verarbeitet Audio ein und aus) haben eine geringere Latenz, sind aber schlechter steuerbar
- Kaskadierte Pipelines lassen sich leichter debuggen, einzelne Komponenten leichter aktualisieren und pro Anwendungsfall feiner abstimmen

## Framework-Vergleich {#framework-comparison}

| Framework | Geeignet für | Lizenz | Hauptstärke |
|-----------|----------|---------|-------------|
| Pipecat (Daily) | Maximale Flexibilität | Open Source | 40+ Integrationen, komponierbar |
| LiveKit Agents | WebRTC-first | Open Source | Saubere API, mehrere Sprachen |
| TEN (Agora) | Multimodal, visueller Builder | Open Source | 98 % Genauigkeit bei der Turn Detection |
| Bolna | Telefonie + WebSocket | Open Source | Schnelle Telefonie-Bereitstellung |
| Vocode | Schnelles Prototyping | Open Source | 10 Zeilen für den Einstieg |

**Auswahlhilfe:**
- WebRTC-first, minimaler Aufwand → **LiveKit Agents**
- Maximale Flexibilität, viele Integrationen → **Pipecat**
- Multimodal (Audio + Vision) → **TEN Framework**
- Telefonie (SIP, PSTN) → **Bolna** oder Vapi
- Volumen > 10.000 Minuten/Monat → Eigenbau mit LiveKit/Pipecat (Managed-Kosten zu hoch)
- Volumen < 10.000 Minuten/Monat → Vapi oder Retell (Managed-Plattformen)

## Pipecat-Pipeline {#pipecat-pipeline}

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

Die Genauigkeit der VAD ist entscheidend: Falsch-Positive verschwenden LLM-Tokens, Falsch-Negative unterbrechen Nutzer vorzeitig.

| VAD | Geeignet für | Genauigkeit | Sprache |
|-----|----------|-------------|---------|
| Silero VAD | Python/Forschung, Open Source | Hoch | Python |
| Cobra VAD (Picovoice) | Enterprise, niedrige Latenz | 99 % | Mehrsprachig |
| TEN VAD | Beste Präzision | Überlegen | Mehrsprachig |
| Semantic VAD | Prosodiebewusste Turn-Vorhersage | Kontextbewusst | — |

**Konfiguration von Silero VAD:**
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

**Semantic VAD** (sagt das Ende eines Redebeitrags anhand von Prosodiemustern voraus, nicht nur anhand von Stille):
- Vermeidet, Nutzer mitten im Gedanken zu unterbrechen, die zur Betonung pausieren
- Schwieriger zu implementieren, erfordert ein Audiomodell oder ein LSTM auf Prosodiemerkmalen

## Latenzoptimierung {#latency-optimization}

### Latenzbudget (kaskadiert) {#budget-breakdown-cascaded}

```text
Total budget: 800ms target

STT (Deepgram Nova-3):  ~100-200ms  (streaming: first words in ~150ms)
LLM (GPT-4o-mini):      ~300-600ms  (first token in ~300ms with streaming)
TTS (Cartesia Sonic):   ~90ms TTFB  (streaming to audio)
Transport (WebRTC):     ~50ms       (UDP, minimal jitter)

Total achievable:        540-950ms
```

### Zentrale Optimierungsstrategien {#key-optimization-strategies}

**1. Spekulative Generierung, während der Nutzer spricht:**
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

**2. LLM-Quantisierung:**
- 4-Bit-Quantisierung → 40 % geringere Latenz, kaum Qualitätsverlust für Konversation
- Lokales, quantisiertes 7B-Modell statt großem Cloud-Modell: oft vergleichbare Qualität bei 3-fach geringerer Latenz

**3. Wiederverwendung von Verbindungen:**
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

**4. Voice-Caching für häufige Phrasen:**
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

**5. Regionale Kolokation:**
- STT, LLM und TTS im selben Rechenzentrumsgebiet betreiben
- Ziel: <10 ms zwischen Dienstaufrufen (LAN im Vergleich zu 80 ms regionsübergreifend)

## WebRTC-Audiokonfiguration {#webrtc-audio-configuration}

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

**Opus-Codec-Einstellungen** (von WebRTC für Audio verwendet):
- Framegröße: 20 ms (Standard)
- Bitrate: 32–96 kbps für Sprache (32 reichen für die STT-Qualität aus)
- Echounterdrückung ist entscheidend, um Selbstunterbrechungen zu verhindern, wenn die TTS-Ausgabe zurück in das Mikrofon gelangt

## End-to-End- vs. kaskadierte Architektur {#end-to-end-vs-cascaded-architecture}

| | End-to-End | Kaskadiert (STT→LLM→TTS) |
|---|---|---|
| Latenz | Geringer (ein Modell) | Höher (3 Roundtrips) |
| Prosodie | Besser (native Audioverarbeitung) | Roboterhafter (Text als Brücke) |
| Steuerbarkeit | Schwer zu debuggen | Komponenten einzeln austauschbar |
| Sprachunterstützung | Weniger (modellabhängig) | Beste Komponente pro Sprache kombinierbar |
| Kosten | 0,30–1,50 $/Minute | Abhängig von der Komponentenwahl |
| Geeignet für | Consumer-Chatbots | Enterprise, Sprachlernanwendungen |

**Empfehlung:** In fast allen Fällen mit einer kaskadierten Pipeline starten. Ziel: 800 ms Median-Latenz. Auf End-to-End wechseln nur, wenn die Obergrenze der kaskadierten Variante zu niedrig liegt und Prosodie entscheidend ist.

**Erwägenswerte End-to-End-Modelle:**
- Gemini 3.1 Flash Live – 90+ Sprachen, <500 ms, nur über API
- Qwen3-Omni – 10 Sprachen für Sprache, Function Calling, offene Gewichte
- Moshi (Kyutai) – 7B, Full-Duplex, offene Gewichte

## Behandlung mehrerer Sprecher {#multi-speaker-handling}

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

## Speech-to-Speech-Modelle (2025–2026) {#speech-to-speech-models-2025-2026}

| Modell | Latenz | Sprachen | Lizenz | Anmerkungen |
|-------|---------|-----------|---------|-------|
| Qwen3-Omni | ~119 ms | 19 Eingabe / 10 Ausgabe | Qwen | MoE 30B/3B aktiv, Function Calling |
| Gemini Live API | <500 ms | 70 | Proprietär | WebSocket, Barge-in, affektiver Dialog |
| NVIDIA PersonaPlex | 205 ms | EN | MIT | Moshi-basiert, 7B, 100 % Erfolgsrate bei Unterbrechungen |
| Voila (Maitrix) | 195 ms | 6 (ohne RU) | Apache 2.0 | Full-Duplex, 1 Mio.+ vorgefertigte Stimmen |
| Chroma 1.0 (FlashLabs) | 147 ms | EN | Apache 2.0 | 4B Parameter, RTF 0,43 |
| Ultravox v0.6 (Fixie) | ~150 ms | Mehrsprachig | Apache 2.0 | Sprachnatives multimodales LLM |
| Moshi (Kyutai) | — | EN | CC-BY 4.0 | 7B, Pocket TTS 100M für CPU |
| Sesame CSM | — | EN | Apache 2.0 | Überwindet das Uncanny Valley, natürliche Disfluenzen |
| OpenAI Realtime API | >1 s | Mehrsprachig | Proprietär | 0,50 $/5-Minuten-Anruf, MCP, WebRTC, SIP |

## Stolperfallen {#gotchas}

- **Echounterdrückung ist Pflicht, nicht optional** – ohne `echoCancellation: true` in den getUserMedia-Constraints gelangt die TTS-Ausgabe der Lautsprecher zurück in das Mikrofon, und die STT transkribiert fortlaufend, was der Bot gerade gesagt hat. Dadurch entstehen Endlosschleifen in der Pipeline. AEC (Acoustic Echo Cancellation) immer auf dem Client aktivieren
- **Der Schwellenwert für die Stilledauer der VAD ist gesprächsspezifisch** – ein Schwellenwert von 300 ms funktioniert für FAQ-Bots, unterbricht aber Nutzer in Sprachlern-Apps, die zum Nachdenken pausieren. `min_silence_duration_ms` pro Anwendungsfall abstimmen; bei Anwendungen, in denen Denkpausen eine Rolle spielen, Semantic VAD in Betracht ziehen
- **LLM-Streaming-Tokens ≠ TTS-Satzgrenzen** – die meisten TTS-Systeme benötigen vollständige Sätze für natürliche Prosodie. Jedes Token einzeln an die TTS zu übergeben, erzeugt roboterhafte Wort-für-Wort-Sprache. Tokens bis zu einer Satzgrenze (`.`, `?`, `!`) oder nach 100 ms Streaming puffern und dann den vollständigen Satz synthetisieren

## Siehe auch {#see-also}

- [[audio-voice/tts-models]] – Auswahl und Vergleich von TTS-Modellen
- [[audio-voice/voice-cloning]] – Zero-Shot-Voice-Cloning für personalisierte Agenten
- [[audio-voice/speech-recognition]] – STT-Modelle und Genauigkeitsbenchmarks

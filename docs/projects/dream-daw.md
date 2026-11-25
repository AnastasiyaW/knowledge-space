---
title: "Dream DAW: dream-daw-feature-updates — Dream Daw Feature Updates"
category: "projects"
date: 2026-11-19
tags: ["dream-daw", "dream-daw-feature-updates", "project"]
aliases: ["Dream DAW: dream-daw-feature-updates"]
---

# Dream DAW: dream-daw-feature-updates — Dream Daw Feature Updates

Dream DAW is an open-source desktop DAW for producers and sound designers who want an alternative to Ableton Live and Bitwig Studio.

**Development line:** project:dream-daw · thread dream-daw-feature-updates  
**Last event:** 2026-11-19 · 3 dated since 2026-11-18 · **Researched:** 2026-11-20 · confidence: medium

## What it is

Dream DAW is an open-source desktop digital audio workstation. It targets music producers and sound designers who want an alternative to Ableton Live and Bitwig Studio. It combines classic timeline editing with assistant-driven workflows, and it is experimental and modular.

What it does:

- Multitrack sequencing
- AI assistant through OpenRouter: changes tracks, clips, effects and notes from text or voice
- Chord and arpeggio generation
- Beat pattern synthesis
- Note quantization
- Neural stem separation with audio fingerprint caching
- Ableton project file import
- VST2, VST3 and AudioUnit plugin hosting, isolated in separate processes

You bring your own API credentials for the language model automation. The native Rust and Tauri parts compile locally on each supported operating system.

## Development line

- **2026-11-18 — Dream DAW project opened on GitHub.** The Dream DAW (Digital Audio Workstation) project was announced as open on GitHub. It describes itself as a cross-platform music creation program built with Rust, Tauri and TypeScript.
  - The first public repository sets up the cross-platform codebase. The real-time audio core is in Rust, desktop windowing runs through Tauri, and the interface logic is in TypeScript. (2026-11-18) — <https://github.com/leoerdman/Dream-DAW>
- **2026-11-19 — Dream-DAW open-source DAW adds AI assistant and expanded editing features.** Dream-DAW is an open-source desktop DAW built on Rust and React. The AI assistant works through OpenRouter and can change projects. The list also names chord, arpeggio and beat generation, mixing controls, note quantization, voice input, stem separation, Ableton project import, and out-of-process VST2/VST3/AU plugin hosting.
- **2026-11-19 — Dream-DAW adds AI assistant and expanded audio features.** Dream-DAW is an open desktop DAW built on Rust and React. It was announced with a Dream AI assistant via OpenRouter that controls project tracks, clips, effects and notes. The update also lists chord and pattern generation, mixing controls, note quantization, voice input, and stem separation with fingerprint caching. It adds Ableton project import and VST2/VST3/AU plugin hosting in a separate process.
- **2026-11-19 — further details from the same date.**
  - The assistant connects through OpenRouter and runs JSON-structured commands against the project document object model. That allows track generation, note quantization, and turning voice prompts into project edits. (2026-11-19) — <https://github.com/leoerdman/Dream-DAW>
  - Plugin hosting runs VST2, VST3 and AU binaries in external worker processes, so a crash stays off the audio thread. The stem separator uses hash-based audio fingerprinting to reuse separations it has already calculated. (2026-11-19) — <https://github.com/leoerdman/Dream-DAW>

## What changed

The project started as an open-source cross-platform music creation tool built with Rust, Tauri and TypeScript. The first work covered core playback and sequencing. A React interface came next, with an assistant subsystem that talks to OpenRouter models.

Generative tools for chord sequences, arpeggios and beat patterns followed. So did voice input transcription and Ableton Live project import. Audio processing was then split into tiers: neural stem separation with fingerprint caching, and out-of-process hosting for VST2, VST3 and AudioUnit plugins. The split keeps third-party crashes away from the core engine.

## How to use this

1. Clone the repository from GitHub. Install Rust, Node.js and the platform audio build libraries.
  — <https://github.com/leoerdman/Dream-DAW>
2. Build and run the Tauri desktop app. It starts the React interface and the native audio playback engine.
  — <https://github.com/leoerdman/Dream-DAW>
3. Enter an OpenRouter API key in the application preferences. That turns on the AI assistant for track creation, clip editing and chord generation.
  — <https://github.com/leoerdman/Dream-DAW>
4. Scan the local VST2, VST3 and AU plugin folders, or import existing Ableton Live project files into the timeline.
  — <https://github.com/leoerdman/Dream-DAW>

## Best practices

- Host unstable or complex third-party VST and AU plugins in separate processes, so a plugin error does not crash the main audio engine.
  — <https://github.com/leoerdman/Dream-DAW>
- Keep audio fingerprint caching on during stem separation, so repeated audio segments are not computed twice.
  — <https://github.com/leoerdman/Dream-DAW>
- Check the assistant's MIDI notes and track structure before committing destructive timeline changes, so the result stays musically coherent.
  — <https://github.com/leoerdman/Dream-DAW>

## Superseded by this

- In-process VST plugin hosting, where a plugin fault crashes the host workstation session.
  — <https://github.com/leoerdman/Dream-DAW>
- External standalone stem separation pipelines without project-level audio fingerprint caching.
  — <https://github.com/leoerdman/Dream-DAW>

## Still unknown

- Long-term stability and latency on different Linux and Windows audio drivers are untested in independent studio benchmarks, because the project only recently went open source on GitHub.
- Public discussions in community audio forums mostly cover Leo Erdman's earlier web-based synth prototype 'Paul Dream DAW', not this Rust/Tauri desktop codebase.
- The introductory repository documentation does not fully detail the neural stem separation model weights or the default OpenRouter LLM routing policies shipped with binary releases.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/leoerdman/Dream-DAW | leoerdman/Dream-DAW: Digital Audio Workstation built with Rust and Tauri | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:dream-daw, thread dream-daw-feature-updates, 3 dated events 2026-11-18 → 2026-11-19.
- **Practical note:** See the usage and practice sections above, including their limits.
- **Confidence:** medium. The dated supersedes above decide what is obsolete.

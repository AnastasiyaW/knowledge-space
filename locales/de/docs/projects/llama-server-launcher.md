---
title: "LlamaServerLauncher"
category: projects
date: 2026-06-17
tags: [llama-server-launcher, llama-server-launcher-development, llama_server_launcher, project]
aliases: ["LlamaServerLauncher"]
level: 2
source_sha256: f2dd56e143b364599a402a44615be4b8a9ade3cc4bb33e2fd551ea2de4cb90c2
translation: machine
translated_at: '2026-10-24'
---
# LlamaServerLauncher {#llamaserverlauncher}

**Entwicklungslinie:** `project:llama-server-launcher` · Thread `llama-server-launcher-development`  
**Letztes Ereignis:** 2026-06-17 · 1 datiert seit 2026-06-17 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

LlamaServerLauncher: plattformübergreifende .NET-8/Avalonia-Anwendung für Nutzer von llama.cpp, die Profile, den Start mehrerer Server und die Konfiguration von GGUF-Modellen über eine Oberfläche benötigen. — wählt `llama-server`, eine lokale GGUF-Datei oder ein Hugging-Face-Repo aus; — konfiguriert Kontext, GPU-Schichten, Sampling und Netzwerkzugriff; — überwacht `/health`, `/slots`, Logs und Inferenzgeschwindigkeit; — kann llama.cpp-Builds herunterladen und umschalten. Einschränkung: Ein kompatibles `llama-server`-Binary ist erforderlich; die Anwendung ersetzt weder die Engine noch das Modell. Fazit: Dies ist eine praktische Alternative zu manuellen llama.cpp-Kommandozeilen, wenn wiederholbare Profile und Beobachtbarkeit benötigt werden.

## Entwicklungslinie {#development-line}

- **2026-06-17 — Repository LlamaServerLauncherAvalonia wurde referenziert.** Am 2026-06-17 verwies die Entwicklungslinie von LlamaServerLauncher auf das GitHub-Repository LlamaServerLauncherAvalonia. Die verfügbaren Belege bestätigen die Repository-Zuordnung, belegen aber weder ein Release, eine Code-Änderung, ein Feature noch eine Nutzungsanleitung.

## Was sich geändert hat {#what-changed}

2026-06-17 — LlamaServerLauncher wurde als GUI zum Starten von llama.cpp und für lokale Inferenz vorgestellt, anstelle manueller Kommandozeilenkonfiguration.

## So wird es verwendet {#how-to-use-this}

Stand 2026-06-17 sollten Praktiker das Repository LlamaServerLauncherAvalonia als identifizierte Quelle für diese Entwicklungslinie heranziehen. Version, Funktionsumfang und Setup-Anforderungen gelten jedoch als ungeprüft, bis das Repository recherchiert ist.

1. Laden Sie das aktuelle Binary für Ihre Plattform von der Release-Seite herunter und starten Sie die Anwendung.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia#installation>
2. Geben Sie `llama-server` an oder laden Sie llama.cpp über die Anwendung herunter, wählen Sie anschließend ein GGUF-Modell oder ein Hugging-Face-Repo/eine Datei aus.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
3. Legen Sie ein Profil an: Kontext, Anzahl der GPU-Schichten, Port, ggf. API-Key und Generierungsparameter festlegen; starten Sie den Server.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
4. Warten Sie auf den Bereitschaftszustand und kopieren Sie anschließend die OpenAI-kompatible Base-URL `/v1` oder den fertigen `curl`-Befehl für den Client.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>

## Bewährte Praktiken {#best-practices}

- Prüfen Sie das Binary über GitHub-Provenance-Attestation und SHA-256: Die Releases sind nicht code-signiert.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia#verifying-releases>
- Belassen Sie den Server auf `127.0.0.1`, sofern kein LAN-Zugriff benötigt wird; bei Netzwerkzugriff setzen Sie einen API-Key.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
- Gleichen Sie die Flag-Unterstützung vor dem Start mit dem gewählten llama.cpp-Build ab: Die Anwendung liest `llama-server --help` und markiert nicht unterstützte Optionen.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
- Beachten Sie bei MCP, dass Kindprozesse mit den Rechten des Launchers gestartet werden; die Aktivierung von MCP beschränkt CORS auf localhost, sofern dies nicht explizit konfiguriert wird.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases>

## Durch dies ersetzt {#superseded-by-this}

- 2026-08-23 — Unter Windows gilt die frühere Erwartung, dass MCP-Kindprozesse nach dem Stoppen des Servers erhalten bleiben könnten, nicht mehr als Standardverhalten: Server und seine Nachfahren werden durch ein Windows Job Object gebunden; eine Ausnahme ist in den Verhaltenseinstellungen verfügbar.

## Weiterhin unbekannt {#still-unknown}

- Das primäre Repository bestätigt den aktuellen Zweck und die späteren Releases, enthält aber keine eigene datierte Release-Beschreibung für genau 2026-06-17; daher sind Details zum damaligen Stand auf die zeitgleiche Erwähnung einer GUI für llama.cpp beschränkt.
- Das aktuelle README listet Funktionen auf, die nach dem letzten veröffentlichten Release v1.9 vom 2026-08-23 hinzugekommen sein könnten; für einzelne Funktionen wurde die Versionsgrenze nicht separat geprüft.
- event_findings und new_events sind wie angefordert unten enthalten.
- event_findings: [{"event_date":"2026-06-17","finding":"Eine unabhängige Erwähnung desselben Tages präzisiert die praktische Bedeutung des ursprünglichen Schritts: Es handelt sich um eine GUI für llama.cpp, die für lokale LLM-Inferenz gedacht ist; eine konkrete Versionsnummer wird in der Quelle nicht genannt.","source_url":"https://2ch.org/ai/res/1633496.html","source_date":"2026-06-17"}]
- new_events: [{"date":"2026-06-20","summary":"v1.2 hat die automatische Ermittlung von `-t`, batch/ubatch size, `-ngl`, Flash Attention, Tensor-Overrides und CPU-MoE über eine Reihe von Benchmarks ergänzt; die Implementierung wurde ohne Python-Abhängigkeit nach C#/.NET portiert.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-06-20"},{"date":"2026-06-25","summary":"v1.3 hat einen OpenAI-kompatiblen Proxy ergänzt, der ein Profil anhand des Feldes `model` lädt, Streaming unterstützt und das Modell nach einem Idle-Timeout entlädt; gleichzeitig wird im VRAM jeweils nur ein Modell gehalten.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-06-25"},{"date":"2026-07-22","summary":"v1.5 hat speicherbare Benchmarks, einen Monitor für CPU/RAM/GPU/VRAM, das Auslesen von GGUF-Metadaten, eine Bereitschaftsprüfung über `/health` sowie Live-Metriken über `/slots` und das Server-Log ergänzt.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-07-22"},{"date":"2026-08-23","summary":"v1.9 hat profilbasierte MCP-Server über `--mcp-servers-config`, die Prüfung erkannter Tools vor dem Laden des Modells, ein Windows Job Object für den Kindprozessbaum sowie Prompt-Läufe in Benchmarks ergänzt.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-08-23"}]

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/pytraveler/LlamaServerLauncherAvalonia | GitHub - pytraveler/LlamaServerLauncherAvalonia | 2026-09-05 |
| https://github.com/pytraveler/LlamaServerLauncherAvalonia#installation | LlamaServerLauncher-Installationsanleitung | 2026-09-05 |
| https://github.com/pytraveler/LlamaServerLauncherAvalonia#verifying-releases | LlamaServerLauncher-Anleitung zur Release-Verifikation | 2026-09-05 |
| https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases | LlamaServerLauncher-Releases | 2026-09-05 |
| https://2ch.org/ai/res/1633496.html | Lokale Sprachmodelle (LLM): Gemma, Qwen, GLM und weitere №242 | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Thema:** `project:llama-server-launcher`, Thread `llama-server-launcher-development`, 1 datiertes Ereignis 2026-06-17 → 2026-06-17.
- **Praktischer Hinweis:** Stand 2026-06-17 sollten Praktiker das Repository LlamaServerLauncherAvalonia als identifizierte Quelle für diese Entwicklungslinie heranziehen. Version, Funktionsumfang und Setup-Anforderungen gelten jedoch als ungeprüft, bis das Repository recherchiert ist.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

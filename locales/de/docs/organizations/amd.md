---
title: "AMD — AMD AI Compute Platform"
category: organizations
tags: [amd, amd-ai-compute-platform, amd_mi300x, instinct-mi300x, organization]
aliases: ["AMD"]
level: 2
source_sha256: d846ed7c7ea769d98f78b5b9ed9b903a1f032614bb1411d814c416fa8fba6dbe
translation: machine
translated_at: '2026-10-24'
---
# AMD — AMD AI Compute Platform {#amd-amd-ai-compute-platform}

**Entwicklungslinie:** `organization:amd` · Thread `amd-ai-compute-platform`  
**Ereignisse:** 2 datiert, 2023-06-14 → 2025-08-13 · **Recherchiert:** 2026-09-03 · Konfidenz: mittel

## Was es ist {#what-it-is}

AMD — eine Compute-Plattform für Teams, die KI, HPC, PCs und Grafik betreiben; der Rechenzentrumsweg besteht aus Instinct-Hardware plus ROCm. — MI455X und Helios für Inferenz, Training und Feinabstimmung im großen Maßstab. — MI430X für wissenschaftliches HPC und souveräne KI. — ROCm-Builds für PyTorch, TensorFlow, JAX, vLLM und verwandte Werkzeuge. Einschränkung: Unterstützung ist ein exaktes Tupel aus Hardware, Betriebssystem, Firmware, Treiber, ROCm- und Framework-Version; MI430X wird für 2027 erwartet, Helios-Volumenbereitstellungen für H2 2026. Fazit: AMD dort einsetzen, wo die vollständige Konfiguration in der aktuellen ROCm-Matrix aufgeführt ist, und nicht allein weil die GPU die AMD-Marke trägt.

## Entwicklungslinie {#development-line}

- **2023-06-14 — AMD erweiterte sein Rechenzentrums-KI-Portfolio rund um Instinct MI300X.** Am 2023-06-14 dokumentierten die verlinkten Materialien von AMD eine Erweiterung des Rechenzentrumsportfolios im Zusammenhang mit der Instinct-MI300-Serie und dem MI300X-Thread. Der beigefügte Link zu PyTorch 2.0 ordnet die Ankündigung in einen Kontext des KI-Softwareökosystems ein. Die gelieferten Links allein belegen weder detaillierte Spezifikationen, Verfügbarkeit noch Kundenakzeptanz.
- **2025-08-13 — AMD veröffentlichte einen Chatbot-Space für GPT-OSS-120B.** Am 2025-08-13 verwies der datierte Link auf einen Hugging-Face-Space für einen GPT-OSS-120B-Chatbot im Besitz von AMD. Dies ist ein öffentlich zugänglicher Modell-Demo- oder Bereitstellungsschritt in AMDs KI-Plattformpräsenz. Der gelieferte Link belegt weder die Backend-Hardware, die Herkunft des Modells, die aktuelle Verfügbarkeit noch Service-Garantien.

## Was sich geändert hat {#what-changed}

AMD, 2023-06-14 — detaillierte Instinct MI300X: CDNA 3, bis zu 192 GB HBM3, eine Acht-GPU-Plattform, Sampling im dritten Quartal sowie Day-Zero-Unterstützung für PyTorch 2.0 mit ROCm 5.4.2. AMD, 2023-11-03 — veröffentlichte Adrenalin 23.11.1 für Windows-Radeon-Systeme mit DirectML-Optimierungen für Stable Diffusion, Lightroom, DaVinci Resolve und Procyon; dies war ein eigenständiger Client-Treiberzweig und kein Instinct/ROCm-Serverrelease. AMD, 2025-08-13 — der benannte Space `amd/gpt-oss-120b-chatbot` war eine Demo-Referenz; sein Endpunkt ist inzwischen zugriffsbeschränkt, daher belegt er weder einen aktuellen Serving-Stack noch einen Supportvertrag. AMD, 2026-07-23 (heute gefunden) — führte die Instinct-MI400-Familie ein: MI455X für Frontier-KI und KI-Fabriken, MI430X für souveräne KI und HPC, mit ROCm als gemeinsamem Softwareweg.

## Verwendung {#how-to-use-this}

Ab 2023-06-14 sollten Praktiker AMDs Instinct MI300X und das zugehörige PyTorch-Ökosystem als Option für KI-Rechenplattformen evaluieren; ab 2025-08-13 können sie den GPT-OSS-120B-Space von AMD als Referenz für Bereitstellung bzw. Demo nutzen, wobei sie die aktuellen technischen und servicebezogenen Details unabhängig prüfen sollten.

1. Beginnen Sie im Selektor und dokumentieren Sie die exakten Versionen von GPU, Betriebssystem, Kernel bzw. Firmware, Treiber, ROCm, Python und Framework; fahren Sie nur mit einer aufgeführten kompatiblen Konfiguration fort.
  — <https://rocm.docs.amd.com/en/develop/compatibility/compatibility-matrix.html>
2. Installieren Sie den AMD-GPU-Treiber und ROCm über die aktuell unterstützte Methode; der Leitfaden empfiehlt bei Unsicherheit die Paketmanager-Installation unter Linux und ein Tarball für portable Windows-Setups.
  — <https://rocm.docs.amd.com/en/develop/install/rocm.html>
3. Verwenden Sie den PyTorch-Selektor für die exakte Hardware, das Betriebssystem und die Version und wählen Sie dann den passenden AMD-Container- oder pip-Installationspfad.
  — <https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html>
4. Validieren Sie das ROCm SDK nach der Installation mit `rocm-sdk targets` und `rocm-sdk test`.
  — <https://rocm.docs.amd.com/en/develop/install/rocm.html>
5. Validieren Sie das Framework vor einer Workload: `python -c "import torch; print(torch.cuda.is_available())"` sollte `True` ausgeben, wenn PyTorch und ROCm die GPU erkennen.
  — <https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html>

## Best Practices {#best-practices}

- Mischen Sie keine Firmware-, Treiber-, ROCm- und Framework-Versionen aus unterschiedlichen Release-Linien; ROCm erfordert den abgestimmten Stack, der in seiner Kompatibilitätsmatrix aufgeführt ist.
  — <https://rocm.docs.amd.com/en/develop/compatibility/compatibility-matrix.html>
- Verwenden Sie den passenden AMD-ROCm-PyTorch-Container bzw. das passende Wheel statt eines beliebigen Binärpakets und führen Sie dann die dokumentierte Erkennungsprüfung durch, bevor Sie Arbeit einplanen.
  — <https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html>
- Behandeln Sie MI455X/Helios und MI430X als getrennte Verfügbarkeitspfade: Prüfen Sie den OEM-Bereitstellungsweg und planen Sie keine produktive MI430X-Kapazität vor der angegebenen Verfügbarkeit im Jahr 2027.
  — <https://www.amd.com/en/products/accelerators/instinct/mi400.html>
- Für Radeon-Laptops und All-in-One-Geräte bevorzugen Sie den vom OEM bereitgestellten Treiber, wenn systemspezifische Funktionen oder Support wichtig sind.
  — <https://www.amd.com/en/support/kb/release-notes/rn-rad-win-23-11-1>

## Hiermit ersetzt {#superseded-by-this}

- AMD, 2023-06-14: Die Spezifikationen der MI300X-Sampling-Phase sowie die Hinweise zu ROCm 5.4.2/PyTorch 2.0 sind historisch; für die aktuelle Auswahl sollten MI400, ROCm 10 und die aktuelle Kompatibilitätsmatrix verwendet werden.
- AMD, 2023-11-03: Adrenalin 23.11.1 ist ein historischer Windows-Treiberrelease und keine aktuelle Entscheidungshilfe für Software; die aktuelle ROCm-Installationsdokumentation verweist auf einen späteren Adrenalin-Release 26.8.1.
- AMD, 2025-08-13: Eine benannte gpt-oss-Chatbot-Demo ist keine aktuelle Bereitstellungsempfehlung, da kein aktiver Support-, Hardware- oder Serving-Vertrag verifiziert werden konnte.

## Weiterhin unbekannt {#still-unknown}

- Der Endpunkt `amd/gpt-oss-120b-chatbot` lieferte während der Prüfung HTTP 401; seine aktuelle Verfügbarkeit, Modellrevision, Beschleuniger und Servicebedingungen sind unbekannt.
- Die datierten Einträge betreffen Instinct-/ROCm-Rechenzentrumshardware, Radeon-Windows-Treiber und eine gehostete Modell-Demo. Sie bilden keine einheitliche technische Release-Abfolge; gemeinsam ist nur die Unternehmensidentität.
- Die OEM-spezifische Verfügbarkeit, Preisgestaltung und Supportdauer der MI400 wurden nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.amd.com/en/newsroom/press-releases/2023-6-13-amd-expands-leadership-data-center-portfolio-with-.html | AMD Expands Leadership Data Center Portfolio with New EPYC CPUs and Shares Details on Next-Generation AMD Instinct Accelerator and Software Enablement for Generative AI | 2026-09-03 |
| https://www.amd.com/en/support/kb/release-notes/rn-rad-win-23-11-1 | AMD Software: Adrenalin Edition 23.11.1 Release Notes | 2026-09-03 |
| https://huggingface.co/spaces/amd/gpt-oss-120b-chatbot | amd/gpt-oss-120b-chatbot | 2026-09-03 |
| https://newsroom.amd.com/news/aai-2026-mi400-instinct-update/ | AAI 2026: AMD Launches AMD Instinct MI400 Series GPUs for Frontier AI, HPC | 2026-09-03 |
| https://www.amd.com/en/products/accelerators/instinct/mi400.html | AMD Instinct MI400 Series GPUs | 2026-09-03 |
| https://www.amd.com/zh-cn/newsroom/press-releases/aai-2026-mi400-instinct-update.html | AAI 2026：AMD推出面向前沿AI与HPC的AMD Instinct MI400系列GPU | 2026-09-03 |
| https://rocm.docs.amd.com/en/develop/install/rocm.html | Install AMD ROCm 10.0.0 | 2026-09-03 |
| https://rocm.docs.amd.com/en/develop/compatibility/compatibility-matrix.html | ROCm 10.0.0 compatibility matrix | 2026-09-03 |
| https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html | Install PyTorch for ROCm | 2026-09-03 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `organization:amd`, Thread `amd-ai-compute-platform`, 2 datierte Ereignisse 2023-06-14 → 2025-08-13.
- **Praktischer Hinweis:** Ab 2023-06-14 sollten Praktiker AMDs Instinct MI300X und das zugehörige PyTorch-Ökosystem als Option für KI-Rechenplattformen evaluieren; ab 2025-08-13 können sie den GPT-OSS-120B-Space von AMD als Referenz für Bereitstellung bzw. Demo nutzen, wobei sie die aktuellen technischen und servicebezogenen Details unabhängig prüfen sollten.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

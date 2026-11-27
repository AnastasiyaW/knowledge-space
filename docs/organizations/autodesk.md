---
title: "Autodesk: autodesk-maya-3ds-max-2027-3-ai-assistant — Autodesk Maya 3Ds Max 2027 3 Ai Assistant"
category: "organizations"
date: 2026-11-26
tags: ["autodesk", "autodesk-maya-3ds-max-2027-3-ai-assistant", "autodesk-siggraph-2023", "organization"]
aliases: ["Autodesk", "Autodesk: autodesk-maya-3ds-max-2027-3-ai-assistant"]
---

# Autodesk: autodesk-maya-3ds-max-2027-3-ai-assistant — Autodesk Maya 3Ds Max 2027 3 Ai Assistant

Autodesk Assistant in Maya and 3ds Max 2027.3 is an in-app AI agent with MCP servers, for 3D artists and pipeline developers.

**Development line:** organization:autodesk · thread autodesk-maya-3ds-max-2027-3-ai-assistant  
**Last event:** 2026-11-26 · 1 dated since 2026-11-26 · **Researched:** 2026-11-27 · confidence: medium

## What it is

Autodesk Assistant and the Model Context Protocol (MCP) servers for Maya and 3ds Max put a scene-aware generative agent inside the app. The MCP servers open the same sessions to outside clients. It is for 3D technical artists and pipeline developers in visual effects and game production.

What it does:

- Answers documentation questions.
- Inspects mesh topology and texture paths in read-only analysis mode.
- Generates Python or MEL scripts and runs them only after explicit user approval.
- Exposes interactive DCC sessions to external language-model clients such as Claude Desktop over standard MCP connections.

Scene modification and the MCP interfaces are in Tech Preview. They need an interactive desktop session, not headless batch processing. Write operations need manual approval, and 3ds Max also needs explicit trusted scripting configuration.

Routine scene cleanup and pipeline inspection can now move from custom internal scripts to conversational or external agent control. The integration gives a standard way to automate interactive DCC workflows.

## Development line

- **2026-11-26 — Autodesk adds AI Assistant to Maya and 3ds Max 2027.3.** Autodesk released Maya and 3ds Max 2027.3 updates with an AI Assistant that inspects scenes and performs prompt-based tasks. It also shipped MCP servers for connecting external AI clients. Scene-related work and MCP are in Tech Preview. Maya offers three assistance levels and previews scripts by default. 3ds Max requires the Trusted scripting permission for MAXScript preview.
  - Maya Assistant has three tiers: Level 1 for product help, Level 2 for read-only scene analysis, and Level 3 for approved script execution. Level 3 comes with single-step undo and Safe Mode workspace sandboxing. (2026-11-26) — <https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Assistant/files/MAYA_ASSISTANT.html>
  - The 3ds Max 2027.3 update limits AI Assistant and the MCP servers to interactive desktop sessions. Assistant operations are disabled in headless batch and command-line modes. (2026-11-26) — <https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-WhatsNew/files/whats_new_in_3ds_max_2027.3/GUID-88DD6F51-EAFA-4817-B399-47847E1DE749.html>
  - 3ds Max preferences set security policies for the MCP server. Read-only telemetry is separated from write privileges. Trusted Scripting must be enabled before MAXScript previews can be evaluated. (2026-11-26) — <https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-Customizing/files/preferences/GUID-85FE4F61-CBE6-403A-A607-193B52D9F1D5.html>

## What changed

The in-software assistant moved from documentation retrieval to direct scene analysis and external agent integration. It now works in three tiers. Read-only inspection diagnoses meshes and textures, and confirmed script execution makes the scene edits.

Native MCP servers were added in parallel. External frontier models and developer environments can query interactive sessions through structured endpoints, without proprietary scripting wrappers.

## How to use this

1. Open Maya or 3ds Max in interactive mode and launch the Autodesk Assistant panel from the application toolbar or Help menu.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Assistant/files/MAYA_ASSISTANT.html>
2. Select an assistance level: Level 1 for general help, Level 2 for non-destructive mesh and scene diagnostics, Level 3 for task automation.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Assistant/files/MAYA_ASSISTANT.html>
3. Enter a natural language prompt to inspect scene topology, missing texture paths or geometry cleanup issues.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-WhatsNew/files/whats_new_in_3ds_max_2027.3/GUID-88DD6F51-EAFA-4817-B399-47847E1DE749.html>
4. Review proposed Python or MAXScript changes in the script preview window. Check the security permissions before you approve execution.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-Customizing/files/preferences/GUID-85FE4F61-CBE6-403A-A607-193B52D9F1D5.html>
5. To connect an external AI client such as Claude Desktop, enable the native MCP server in application preferences. Choose Read-only or Read-write access, then connect through the local MCP endpoint.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-Customizing/files/preferences/GUID-85FE4F61-CBE6-403A-A607-193B52D9F1D5.html>

## Best practices

- Keep Safe Mode on, so assistant-generated scripts cannot run operating system commands or write files outside the workspace.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Assistant/files/MAYA_ASSISTANT.html>
- Audit the scene at Level 2 first, then move to Level 3 script generation, so the scene is not changed by accident.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Assistant/files/MAYA_ASSISTANT.html>
- Set MCP server permissions to Read-only by default when you try external agent workflows, so production assets stay protected.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-Customizing/files/preferences/GUID-85FE4F61-CBE6-403A-A607-193B52D9F1D5.html>
- Enable Trusted Scripting explicitly in the 3ds Max Security settings before you run MAXScript previews the assistant generated.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-Customizing/files/preferences/GUID-85FE4F61-CBE6-403A-A607-193B52D9F1D5.html>

## Superseded by this

- Autodesk Assistant used to search static product documentation only. It could not inspect the scene hierarchy or run scripts.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Assistant/files/MAYA_ASSISTANT.html>
- External AI agents needed custom Python socket listeners and proprietary pipeline wrappers, not standard Model Context Protocol endpoints.
  — <https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-Customizing/files/preferences/GUID-85FE4F61-CBE6-403A-A607-193B52D9F1D5.html>

## Still unknown

- Real-world stability and performance of the Tech Preview MCP servers. Forum discussion (AREA by Autodesk, CGTalk, Reddit r/Maya and r/3dsmax) could not be verified with exact URLs within the search quota.
- Which proprietary LLM families run the Level 1-3 cloud services. Autodesk does not disclose them in the documentation.
- Regional guidance for Simplified Chinese. Official documentation for the 2027.3 Tech Preview features was not published at the time of observation.

## Sources

| source | title | read |
|---|---|---|
| https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Assistant/files/MAYA_ASSISTANT.html | Maya Assistant - Autodesk Documentation | 2026-11-27 |
| https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-WhatsNew/files/whats_new_in_3ds_max_2027.3/GUID-88DD6F51-EAFA-4817-B399-47847E1DE749.html | What's New in 3ds Max 2027.3 - Autodesk Documentation | 2026-11-27 |
| https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-Customizing/files/preferences/GUID-85FE4F61-CBE6-403A-A607-193B52D9F1D5.html | Security and MCP Preferences in 3ds Max - Autodesk Documentation | 2026-11-27 |

## Agent brief {#agent-brief}

- **Subject:** organization:autodesk, thread autodesk-maya-3ds-max-2027-3-ai-assistant, 1 dated events 2026-11-26 → 2026-11-26.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.

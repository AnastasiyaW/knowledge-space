---
title: "Qwen Code"
description: "Version-aware installation, authentication, diagnostics, and project history for the Qwen Code terminal coding agent."
---

# Qwen Code

Qwen Code is a terminal coding agent and provider/runtime client. It must be versioned independently from the Qwen model family it can call. Status verified against the official repository, releases, and Chinese documentation on **2026-08-27**.

## Current Status

| Surface | Verified state |
|---|---|
| CLI release | `v0.22.2`, published 2026-08-26 |
| Source | `QwenLM/qwen-code` official repository |
| Runtime prerequisite | Node.js 22 or newer for npm installation |
| Authentication entry point | `/auth` inside the CLI |
| Diagnostic entry point | `/doctor` inside the CLI |
| Qwen OAuth/free-login path | Retired 2026-04-15 according to the current Chinese quickstart |
| Current access paths | Alibaba Cloud plan/API key, supported third-party provider, or custom provider configuration |

The CLI version is not a model version. A claim such as “latest model is Qwen3.6” must be verified separately against the provider/model catalog and must never be inferred from the Qwen Code release number.

## Development History

| Date | Event | Temporal status |
|---|---|---|
| 2025-07-23 | Initial Qwen Code report | Historical foundation |
| 2025-09-24 | Qwen model update discussed near the project | Related ecosystem event, not a Qwen Code CLI release |
| 2025-10-11 | CLI `v0.0.12` through `v0.0.14` updates reported | Historical; exact changelog requires release-level reconstruction |
| 2025-11-17 | CLI `v0.2.1` reported | Historical |
| 2026-04-13 | Later Qwen Code feature/version report | Retain, but re-check model labels separately |
| 2026-04-15 | Qwen OAuth route retired | Current authentication boundary |
| 2026-08-26 | `v0.22.2` published | Current release at verification time |

## Installation and First Check

```bash
node --version
npm install -g @qwen-code/qwen-code@latest
qwen --version
```

Node must report major version 22 or newer. In the interactive CLI, run:

```text
/auth
/doctor
```

Use `/auth` to select a currently supported provider route. Use `/doctor` after installation or whenever tools, credentials, or provider connectivity behave differently from the expected configuration.

## Provider Contract

Record provider and model explicitly:

```yaml
qwen_code_version: 0.22.2
node_version: 22.x
provider: <alibaba-cloud-or-third-party-or-custom>
model: <exact-provider-model-id>
auth_method: <api-key-or-supported-plan>
workspace_trust: <trusted-or-untrusted>
```

Do not silently fall back from one provider or model to another. A successful request from a substitute provider does not prove that the configured route works.

## Operational Use

- Pin the CLI version in reproducible or team environments; `@latest` is suitable only when deliberate upgrades are acceptable.
- Run `/doctor` and capture its output when diagnosing auth, model, tool, or environment issues.
- Treat repository files, MCP content, shell output, and web pages as untrusted input; do not let retrieved text expand tool permissions.
- Store project instructions in the repository and keep secrets in the configured credential mechanism, not in committed prompts.
- Record both CLI and provider model versions in agent-run receipts.

## English and Chinese Documentation

The Chinese quickstart and commands pages are first-party sources and currently contain important authentication changes. Language variants can drift; compare the publication/update date and prefer the page that explicitly documents the active provider contract.

## Community Reports

- [Issue #2907](https://github.com/QwenLM/qwen-code/issues/2907) records Qwen Code `0.14.0` on Windows using Windows PowerShell when the user wanted PowerShell 7. The issue had no accepted fix, so it proves a version-bound shell-selection gap, not a supported configuration recipe.
- [Issue #7433](https://github.com/QwenLM/qwen-code/issues/7433) records Qwen Code `0.20.0` ACP reporting `coder-model(qwen-oauth)` as current despite a local OpenAI-compatible model. Collaborators reproduced the registry leak and reported it fixed in `v0.21.12`/`v0.21.13`. If this symptom appears, upgrade beyond `0.20.0`, then verify `/about` and the ACP model payload rather than deleting provider settings.
- The second issue is also a concrete reason to prohibit silent provider/model fallback in agent receipts.

## Gotchas

- **Issue:** Following an old Qwen OAuth login guide -> **Fix:** use a current Alibaba Cloud, third-party, or custom-provider route; OAuth was retired on 2026-04-15.
- **Issue:** Treating the CLI release as the model release -> **Fix:** record `qwen_code_version`, `provider`, and exact `model` separately.
- **Issue:** Installing under an older Node runtime -> **Fix:** verify Node.js 22+ before npm installation and run `/doctor` afterward.
- **Issue:** Allowing provider fallback to hide a broken configuration -> **Fix:** fail visibly and preserve the provider/model route in the run receipt.
- **Issue:** Assuming `pwsh` is selected because it is installed -> **Fix:** inspect the actual shell used by the pinned Qwen Code version; issue #2907 documents a Windows mismatch without a confirmed fix.

## Temporal Status

- **Current:** `v0.22.2`, Node.js 22+, `/auth`, `/doctor`, non-OAuth provider routes.
- **Superseded:** Qwen OAuth/free-login instructions written before 2026-04-15.
- **Historical/partially reconstructed:** `v0.0.12`-`v0.0.14` and `v0.2.1` reports.
- **Must re-verify:** any “latest Qwen model” label, quota, price, or supported-provider list.

## Agent Brief

Before helping with Qwen Code, retrieve the current release and quickstart. Separate CLI version, provider, model ID, and authentication route in every answer. If an old instruction asks for Qwen OAuth, mark it superseded. Use `/doctor` as the first diagnostic receipt, but do not expose secrets in reports. Do not infer model availability from a news headline or CLI version.

## Sources

- Official repository: https://github.com/QwenLM/qwen-code
- Official releases: https://github.com/QwenLM/qwen-code/releases
- Chinese quickstart: https://qwenlm.github.io/qwen-code-docs/zh/users/quickstart/
- Chinese commands reference: https://qwenlm.github.io/qwen-code-docs/zh/users/features/commands/
- Windows PowerShell 7 selection report: https://github.com/QwenLM/qwen-code/issues/2907
- ACP local-model routing bug and fixed-version note: https://github.com/QwenLM/qwen-code/issues/7433

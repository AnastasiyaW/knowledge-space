---
title: OpenSandbox
category: projects

tags: [opensandbox, opensandbox-development, opensandbox-group/opensandbox, project]
aliases: ["OpenSandbox"]
---

# OpenSandbox

**Development line:** `project:opensandbox` · thread `opensandbox-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-08 · confidence: medium

## What it is

OpenSandbox provides isolated environments for AI agents across Docker and Kubernetes.

- Multi-language SDKs, an `osb` CLI and an MCP server
- Lifecycle, command and file APIs across Docker and Kubernetes
- Per-sandbox egress policy, Credential Vault proxy and optional secure-runtime choices

Local execution requires Docker and Python 3.10+; the lifecycle API binds `0.0.0.0` by default. Use it as an execution layer for agent workloads, but secure the control plane and outbound network policy before exposing it.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

OpenSandbox development: 2026-03-03 — the `opensandbox-server` 0.1.5 package was published, showing package distribution before the August project reference. 2026-03-22 — PyPI lists `opensandbox-server` 0.1.8 as yanked for incompatibility. 2026-08-15 — the dated project reference identifies OpenSandbox, but does not itself establish a tagged feature or release. 2026-08-19 — Helm chart 0.2.2, app version 0.2.2, shipped as an all-in-one controller-and-server package. 2026-08-26 — `opensandbox-server` 0.2.3 was published and `execd` 1.1.0 added opt-in init, hardening and lifecycle-hook features; the classic topology stayed the default.

## How to use this

1. For local use, install Docker and Python 3.10+, generate the Docker example configuration with `uvx opensandbox-server init-config ~/.sandbox.toml --example docker`, then start `uvx opensandbox-server`.
  — <https://github.com/opensandbox-group/OpenSandbox>
2. Install `opensandbox-cli`, configure its domain, protocol and API key, create a sandbox with an explicit timeout, health-check it, run the workload, then kill the sandbox.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md>
3. For an MCP-capable coding client, install `opensandbox-mcp` and configure its stdio process with the OpenSandbox domain, protocol and API key.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/sdks/mcp/sandbox/python/README.md>
4. For the all-in-one Kubernetes topology, install the official Helm 0.2.2 release into an `opensandbox-system` namespace.
  — <https://github.com/opensandbox-group/OpenSandbox/releases/tag/helm%2Fopensandbox%2F0.2.2>

## Best practices

- Set a non-empty server API key before any production exposure; an empty key disables checks and needs explicit insecure-start acknowledgement.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/server/configuration.md>
- Create credential-proxy sandboxes with an explicit network policy, and pass Credential Vault payloads by file or stdin rather than plaintext command-line flags.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md>
- Use explicit sandbox timeouts and kill sandboxes after the workload; a pause request is asynchronous, so poll until the state reaches Paused.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md>
- Resolve release images to immutable digests and verify their Cosign signature and provenance attestation instead of relying on mutable tags.
  — <https://github.com/opensandbox-group/OpenSandbox/blob/main/docs/community/release-verification.md>

## Superseded by this

- {"claim":"`opensandbox-server` 0.1.8 is a usable server release.","obsolete_since":"2026-03-22","source_url":"https://pypi.org/project/opensandbox-server/"}

## Still unknown

- The supplied event contains only a project URL, so the intended feature or claim for 2026-08-15 cannot be recovered.
- No first-party release note dated exactly 2026-08-15 was found; the same-day Helm detail is an issue report, not a release announcement.
- The current verification guide records a historical `alibaba/OpenSandbox` repository identity for pre-migration artifacts but does not date the organization migration.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/opensandbox-group/OpenSandbox | OpenSandbox repository README | 2026-09-08 |
| https://pypi.org/project/opensandbox-server/0.1.5/ | opensandbox-server 0.1.5 on PyPI | 2026-09-08 |
| https://pypi.org/project/opensandbox-server/ | opensandbox-server on PyPI | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/issues/1529 | Issue #1529: all-in-one Helm chart release gap | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/releases/tag/helm%2Fopensandbox%2F0.2.2 | Helm Chart opensandbox 0.2.2 (App v0.2.2) | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/releases/tag/docker%2Fexecd%2Fv1.1.0 | components/execd 1.1.0 release | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/cli/README.md | OpenSandbox CLI README | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/server/configuration.md | OpenSandbox Server configuration reference | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/sdks/mcp/sandbox/python/README.md | OpenSandbox MCP Sandbox Server | 2026-09-08 |
| https://github.com/opensandbox-group/OpenSandbox/blob/main/docs/community/release-verification.md | OpenSandbox Release Verification | 2026-09-08 |

## Agent brief {#agent-brief}

- **Subject:** `project:opensandbox`, thread `opensandbox-development`, 0 dated events - → -.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
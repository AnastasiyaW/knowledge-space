---
title: ComfyUI Cloud — Hosted access and billing
category: projects
date: 2025-12-23
tags: [comfyui-cloud, comfyui_cloud, hosted-access-and-billing, project]
aliases: ["ComfyUI Cloud"]
---

# ComfyUI Cloud — Hosted access and billing

**Development line:** `project:comfyui-cloud` · thread `hosted-access-and-billing`  
**Last event:** 2025-12-23 · 2 dated since 2025-09-16 · **Researched:** 2026-11-21 · confidence: medium

## What it is

ComfyUI Cloud is hosted ComfyUI at cloud.comfy.org: a browser-based editor that runs workflows on cloud GPUs, billed by subscription plans and credits.

- Access: no local install; the browser editor and an API are both offered, with API parallelism limited by plan.
- Users: people who want ComfyUI without a local GPU or setup, and teams that share credits.
- Key capability: runs on Blackwell-generation RTX PRO 6000 GPUs; Comfy-maintained custom nodes only.
- Limits: 30-minute maximum per job on Standard and Creator, 1 hour on Pro; one workflow at a time in the web editor; up to 100 queued workflows.

## Development line

- **2025-09-16 — Dedicated login entry point for ComfyUI Cloud.** A dedicated login endpoint appeared by 2025-09-16, confirming a hosted-service entry point existed by that date.
- **2025-12-23 — Credit-based ComfyUI Cloud access reported.** Credit-based charging for ComfyUI Cloud use was reported on 2025-12-23.

## What changed

- 2025-09-16 — dedicated login endpoint (from the stub; the date was not re-checked against an archive).
- 2025-12-23 — credit-based charging reported (from the stub; the community report was not re-read on 2026-11-21).
- As of 2026-11, the pricing page lists these plans (monthly price, billed yearly price, and yearly credits):
  - Free: $0; 5 free runs.
  - Standard: $20 monthly or $16 yearly; 50,400 credits per year.
  - Creator: $35 monthly or $28 yearly; 88,800 credits per year.
  - Pro: $100 monthly or $80 yearly; 253,200 credits per year.
  - Team: $700 monthly or $630 yearly; 1,772,400 shared credits per year.
  - Enterprise: custom.
- The pricing page shows no effective dates for these prices.

## How to use this

1. Open cloud.comfy.org or comfy.org/cloud in a browser; no installation is needed.
  — <https://cloud.comfy.org/>
2. Pick a plan by job length: Standard and Creator cap each job at 30 minutes; Pro allows 1 hour.
  — <https://docs.comfy.org/get_started/cloud>
3. Budget in credits, not in hours. The pricing page lists credit rates per GPU hour, for example 736.39 credits per hour for the RTX PRO 6000 96 GB rate; sessions bill only while the GPU runs.
  — <https://www.comfy.org/cloud/pricing>
4. Check that every custom node in your workflow is in the Comfy-maintained set; unsupported nodes are flagged in the editor and the Errors tab.
  — <https://docs.comfy.org/get_started/cloud>

## Best practices

- Run API batches only on plans that allow the parallelism you need: the pricing page lists API concurrency of 1 on Standard, 3 on Creator, 5 on Pro and 25 on Team.
  — <https://www.comfy.org/cloud/pricing>
- Assume credits apply to every run; the free tier covers only 5 runs.
  — <https://www.comfy.org/cloud/pricing>
- Close the browser tab only after a job finishes; closing it ends the session.
  — <https://docs.comfy.org/get_started/cloud>

## Superseded by this

- The assumption that hosted ComfyUI runs are free is superseded by credit-based billing (reported 2025-12-23; the current plan table confirms it as of 2026-11).

## Still unknown

- The effective date of the current credit model and prices is not shown on the pricing page.
- The FAQ states Team plans range "from $200 to $2,500/month", while the pricing table lists $630 and $700; the two were not reconciled.
- Team runtime per workflow is not stated explicitly; the pricing table lists it as "Everything in Pro".
- Storage limits and the total session cap are not stated.
- Sign-up steps and the login page were not read directly.

## Sources

| source | title | read |
|---|---|---|
| https://docs.comfy.org/get_started/cloud | ComfyUI Cloud documentation: access, billing, limits | 2026-11-21 |
| https://www.comfy.org/cloud/pricing | ComfyUI Cloud pricing | 2026-11-21 |
| https://cloud.comfy.org/ | ComfyUI Cloud landing page | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-cloud`, thread `hosted-access-and-billing`, 2 dated events 2025-09-16 → 2025-12-23; plan table as of 2026-11.
- **Practical note:** Budget in credits, check the 30-minute or 1-hour job limit for the chosen plan, and check API concurrency before batch runs.
- **Confidence:** medium. Plan and limit facts come from the pricing and docs pages; the stub dates are not re-verified. Dated supersedes above are the authority for what is obsolete.

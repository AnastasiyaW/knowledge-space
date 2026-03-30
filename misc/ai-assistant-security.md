---
title: AI Assistant Security Practices
category: misc/ai-security
tags: [security, ai-assistant, vm-isolation, api-keys, credential-management, rate-limiting]
---

# AI Assistant Security Practices

## Key Facts

- AI coding tools and assistants have **broad system access** - they can read files, execute commands, browse the web, and send messages
- Security model: assume the tool WILL eventually be compromised - minimize blast radius
- **VM isolation** is the primary defense: run AI assistants on a dedicated virtual machine, not your personal computer
- The VM should contain NO personal files, bank credentials, crypto wallets, or sensitive documents
- API keys should have **spending limits** and **restricted permissions** (read-only where possible)
- Three execution policies control agent autonomy:
  - **Terminal execution**: can the agent run shell commands?
  - **Code review**: must the agent ask before modifying files?
  - **Browser execution**: can the agent browse the web unsupervised?
- Start with **request-review** for all policies, relax only after building trust with the tool
- Never auto-approve JavaScript execution in the browser - this is the highest-risk capability

### API Key Security Checklist

- [ ] Set hard spending limits on all API provider accounts
- [ ] Disable auto-refill/auto-recharge on payment methods
- [ ] Create separate API keys for AI assistants (not your main development keys)
- [ ] Use read-only credentials for services like Google Drive, email, calendar
- [ ] Rotate API keys monthly
- [ ] Monitor API usage dashboards for unexpected spikes
- [ ] Never commit API keys to version control

### Execution Policy Levels

| Policy | Safest | Balanced | Riskiest |
|--------|--------|----------|----------|
| Terminal commands | Request review | Agent decides | Always proceed |
| Code modifications | Request review | Agent decides | Always proceed |
| Browser access | Disabled | Request review | Always proceed |

## Patterns

```bash
# VM-based deployment for AI assistants
# Azure/AWS/GCP: ~$30/month for B2s (2 CPU, 4GB RAM)

# 1. Create dedicated user (not root, not your main user)
sudo adduser aiuser
sudo usermod -aG sudo aiuser

# 2. Restrict SSH access (key-only, no password for main user)
# 3. No ports open except SSH (22) - NO public HTTP access
# 4. Firewall: block all inbound except SSH

# Communication goes through messaging channels (Telegram/WhatsApp)
# not through exposed web ports
```

```python
# API key budget management pattern
import os

# OpenRouter: deposit fixed amount, no auto-refill
# OpenAI: set hard monthly spending limit in dashboard
# Anthropic: set usage limits per API key

# Environment-based key management (never hardcode)
api_key = os.environ.get("OPENROUTER_API_KEY")
# Key created with:
# - $20 credit limit
# - No auto-refill
# - Rate limit: 10 req/min
```

## Gotchas

- Open-source AI assistant projects (OpenClaw, etc.) are hobby-level security - no bug bounties, no security audits, rapid development with hundreds of PRs
- Autonomous agents with cron jobs can accumulate unexpected costs overnight - always check API usage in the morning
- **Credential leakage**: the assistant stores API keys, passwords, and tokens in memory files on disk - encrypt the VM's disk
- A compromised skill from a community marketplace can exfiltrate credentials or execute arbitrary code
- Browser automation can be used by a compromised agent to log into your accounts, send messages, or make purchases
- Auto-update skills may introduce malicious code - review changelogs before updating
- If the agent can read your email AND browse the web AND execute code, a single vulnerability gives full access to your digital life

## See Also

- [[ai-assistant-automation]] - personal AI assistant deployment and scheduling
- [[ai-ide-rules-and-context]] - workspace-scoped rules that limit agent behavior

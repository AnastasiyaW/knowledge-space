---
title: Personal AI Assistant Automation
category: misc/ai-automation
tags: [ai-assistant, cron-jobs, proactive-ai, openclaw, scheduled-tasks, telegram, whatsapp]
---

# Personal AI Assistant Automation

## Key Facts

- Personal AI assistants (OpenClaw, Claude Code scheduled tasks) run as persistent services that can act autonomously
- Key differentiator from chatbots: **proactive behavior** - the AI initiates actions on a schedule without human prompting
- Core components: LLM backend (GPT/Claude/Gemini via API), messaging channel (Telegram/WhatsApp/Slack/Discord), cron scheduler, skills/plugins, persistent memory
- The assistant itself has no AI model - it's a **wrapper** that orchestrates calls to external LLM APIs
- A single persistent session with memory replaces the chatbot pattern of many disconnected chats
- Cron-based scheduling lets you define recurring tasks: "Every morning at 9am, check weather and send me a summary"
- Communication channels enable the AI to **notify you** when autonomous tasks complete - you don't need to be at the computer
- Skills extend capabilities: web browsing, file management, API calls, code execution

### Architecture

```
User <-> Messaging Channel (Telegram/WhatsApp)
              |
         Gateway Service (always running)
              |
         AI Agent (LLM API calls)
              |
    +---------+---------+
    |         |         |
  Skills    Cron     Memory
  (.md)    (scheduler) (files)
```

### Use Cases for Scheduled AI Tasks

| Task | Schedule | Example |
|------|----------|---------|
| Morning briefing | Daily 9am | Weather + calendar + unread emails summary |
| Price monitoring | Every 30min | Alert when stock/crypto hits target price |
| Content digests | Daily/weekly | Summarize news, HN top stories, RSS feeds |
| Health checks | Every 5min | Monitor website uptime, API status |
| Auto-updates | Daily midnight | Update the assistant and its skills |

## Patterns

```bash
# Typical deployment: Linux VM (Azure, AWS, GCP)
# 1. Create VM (Ubuntu 22.04+, 4GB RAM minimum)
# 2. Create dedicated user (not root)
sudo adduser ai-assistant
sudo usermod -aG sudo ai-assistant

# 3. Install runtime (Node.js for OpenClaw, Python for custom)
curl -fsSL https://deb.nodesource.com/setup_25.x | sudo -E bash -
sudo apt install -y nodejs

# 4. Install and configure the assistant
sudo npm i -g openclaw
openclaw onboard  # Interactive setup wizard

# 5. Start the gateway (persistent service)
openclaw gateway  # Takes over terminal, listens for messages

# 6. Connect via TUI or messaging channel
openclaw tui     # Terminal UI in separate SSH session
```

```python
# Custom scheduled task pattern (conceptual)
# Define a recurring job that runs autonomously

schedule = {
    "task": "morning_briefing",
    "cron": "0 9 * * *",      # Every day at 9am
    "actions": [
        "check_weather(location='Lisbon')",
        "count_unread_emails()",
        "get_calendar_summary()",
    ],
    "notify_via": "telegram",
    "message_template": "Good morning! {weather}\n{emails}\n{calendar}"
}
```

## Gotchas

- AI assistants can burn through API credits autonomously - set hard spending limits on API keys (e.g., $10 max on OpenRouter)
- Disable auto-refill on API providers to prevent runaway costs
- One user reported $18.75/night from heartbeat messages sending 120K tokens to Opus every 30 minutes
- Always deploy in a **VM**, never on your personal machine - limits damage if the assistant is compromised
- Grant **read-only** API permissions by default - only enable write access for specific, approved actions
- The assistant remembers credentials in plaintext files - treat the VM as a sensitive environment
- Keep the assistant and skills updated daily - these are early-stage projects with frequent security patches
- Anti-bot protections on services like YouTube, LinkedIn will block automated access - use official APIs instead of scraping

## See Also

- [[ai-assistant-security]] - security practices for AI assistant deployments
- [[ai-coding-skills]] - skill format shared between coding IDEs and assistants

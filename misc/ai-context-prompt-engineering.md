---
title: Context Engineering for AI Coding
category: misc/ai-coding-tools
tags: [context-engineering, prompt-engineering, file-tagging, image-attachment, context-window, conversation-management]
---

# Context Engineering for AI Coding

## Key Facts

- **Context engineering** is the practice of providing the right information to an AI coding agent so it produces better output with fewer iterations
- More context = better results: attach mockups, tag files, reference existing components, include design guidelines
- AI IDEs support multiple context injection methods: file @-mentions, image attachments, rule loading, skill injection
- The context window is the agent's working memory - everything in the conversation (prompts, responses, file contents, images) consumes it
- When context fills up, quality degrades - create a **new conversation** for unrelated tasks
- **File tagging** (`@filename`) makes the model focus on specific files instead of scanning the whole repository
- **Image attachments** (screenshots, mockups) dramatically improve UI-related task accuracy
- General rules load automatically, but skills load on-demand based on relevance - this is **lazy context loading**

### Context Injection Hierarchy

1. **System context** - rules (always-on) loaded at conversation start
2. **Skill descriptions** - loaded at start, full content loaded on-demand
3. **User prompt** - your instructions and requirements
4. **Tagged files** - specific code files the agent should focus on
5. **Attached images** - screenshots, mockups, diagrams
6. **Conversation history** - previous messages and responses

### When to Create a New Conversation

- Switching to an unrelated task (context pollution)
- After agent starts hallucinating or giving poor responses
- After adding new rules or skills (they load at conversation start)
- When context window is nearly full (responses become less accurate)
- After completing a feature and starting a new one

## Patterns

```markdown
# High-quality planning prompt structure:

[Clear task description with requirements]
Plan a new tool for cron expression explainer and generator.
Two functionalities: explain and generate.

[File references for context]
@src/components/Base64.tsx  # existing component to reuse

[Image attachments for visual context]
[desktop-mockup.png]  # UI layout reference
[mobile-mockup.png]   # responsive design reference

[Explicit reuse instruction]
Base64 has reusable components - check before generating new ones.

[Skill/guideline reference]
Follow the design skill guidelines.
```

```markdown
# Context optimization techniques:

# 1. Progressive detail - start broad, narrow down
"What is this repo about?" -> understand context
"Explain this file" -> focus on specific area
"Change X in Y" -> targeted modification

# 2. Continuation vs new conversation
# Continue: when follow-up relates to current context
# New chat: when switching tasks or context is polluted

# 3. File tagging to reduce scanning
# Bad: "Update the UUID generator"
# Good: "Update @src/components/UuidGenerator.tsx"

# 4. Export conversations before clearing
# Three dots -> Export -> Download as PDF
```

## Gotchas

- Attaching too many files at once fills the context window fast - be selective
- Images consume significant tokens (~1000+ tokens per image) - only attach relevant ones
- The agent may not use all attached context - explicitly reference what matters in your prompt
- Continuing a long conversation leads to context degradation - model "forgets" earlier instructions
- Rule files that are too long waste tokens on every conversation - keep rules concise, put details in separate reference files
- The agent's memory resets with each new conversation (except persistent rules) - important decisions made mid-conversation are lost
- When the model says "I'm not sure what you mean," it usually means the context is too ambiguous - add more specific references

## See Also

- [[ai-ide-rules-and-context]] - persistent rules that survive conversation resets
- [[ai-coding-skills]] - on-demand context loading via skill descriptions
- [[llm-model-selection-for-coding]] - model context windows and their limits

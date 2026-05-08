# LLM Persona Design and Engineering

Persona design for LLM agents involves mapping abstract character traits to concrete linguistic patterns and behavioral constraints. In the context of pedagogical agents, effective personas must balance engagement with authority to prevent sycophantic behavior.

## Core Personality Frameworks

### Big Five (OCEAN) Mapping
The Big Five personality model—Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism—serves as a technical coordinate system for LLM behavior. [Liu et al. 2025] shows that explicit OCEAN values produce linear mappings to linguistic markers.

- **Agreeableness Management:** LLMs default to high-Agreeableness (helpful/sycophantic). Differentiation requires explicit positioning on the mid-to-low spectrum to enable corrective authority.
- **Dimensional Isolation:** Persona (identity), Voice (sound), Tone (emotion), and Register (formality) are orthogonal. A "Strict Mentor" persona might use a "Friendly" tone while maintaining a "Formal" register.

### Behavioral Anchoring
Personas degrade over long contexts. [Chen et al. 2024] indicates significant identity drift typically occurs within 8 turns, particularly in larger models. 

- **Sandwich Pattern:** Re-inject 1-2 voice-defining tokens or behavioral reminders after the user input (System-User-System reminder).
- **Persona-Conditioned Summarization:** When context windows saturate, summaries must be written in-character ("The student struggled with past tense today...") rather than as a neutral system log.

## System Prompt Engineering

### Token Budgeting and Strength
The empirical sweet spot for persona content is **300-800 tokens**. Exceeding 3000 tokens often triggers "lost-in-the-middle" effects, where central instructions are ignored.

- **Heuristic:** If a sentence does not change a specific decision the agent makes, it should be removed. 
- **Anti-pattern:** The "Helpful Assistant" label is zero-signal. It dilutes specific personality traits by regressing the model to its training-data mean.

### Scenario-Based Instruction (Show-Don't-Tell)
Adjective stacks (e.g., "you are patient, kind, and funny") produce generic outputs. Behavioral rules linked to specific scenarios provide superior activation.

```text
Bad: "You are a patient and encouraging teacher."

Good: "When a student remains silent for >10 seconds, do not provide hints. 
      Wait in silence. If they answer incorrectly, acknowledge the correct 
      components first: 'Your choice of tense is perfect, but "goed" is 
      irregular. Try again.'"
```

## Pedagogical Archetypes

Different learning levels require specific persona modes. The underlying identity remains constant, but the "Maria-ness" manifests differently:

| Archetype | Level Fit | Primary Mechanism |
| :--- | :--- | :--- |
| **Socratic Questioner** | B2+ | Drives self-reflection; requires student vocabulary for reasoning. |
| **Scaffolding Mentor** | A1–C1 | Follows Vygotsky’s Zone of Proximal Development (ZPD); withdraws support as student proficiency increases. |
| **Pattern Drill Coach** | A1–A2 | Fast turn-taking; focus on mechanical accuracy; low affect. |
| **Storyteller** | B1+ | Uses narrative context to anchor vocabulary; improvises tangents based on student interests. |

## Technical Implementation

### Unified Persona Specification
To prevent voice-text mismatch, the persona spec must be the single source of truth for both the LLM and the TTS engine.

```yaml
persona_spec:
  identity:
    name: "Mentor_Alpha"
    ocean_internal: { O: 0.7, C: 0.8, E: 0.4, A: 0.3, N: 0.2 }
  behavioral_rules:
    on_error: "Provide direct correction with one meta-linguistic hint."
    on_success: "Brief acknowledgment; no superlative praise."
  voice:
    cloning_id: "uuid-123"
    prosody_hints: "[calm][measured][slight_thinking_pause]"
  register:
    default: "B1_Colloquial"
    latency_fill: "Narrate thought process in-character ('Let me find that clip...')"
```

### Memory Salience
Memory is a persona feature, not a database property. Persona-driven salience determines what is stored in long-term memory:
- **Grammarian:** Remembers error patterns; forgets personal anecdotes.
- **Relational:** Remembers student hobbies/goals; forgets single-instance errors.

## Gotchas
- **Issue:** Agreeableness collapse in RLHF models leads to validating student errors (e.g., "Good job!" to a wrong answer). → **Fix:** Use explicit "Refusal Clauses" in the system prompt that forbid validating incorrect syntax or false premises.
- **Issue:** TTS prosody mismatch creates an "uncanny valley" effect where text is warm but voice is flat. → **Fix:** Embed prosody tags (`[sighs]`, `[excited]`) directly in the LLM output based on the persona spec.
- **Issue:** Identity drift after 8-10 turns. → **Fix:** Implement periodic "Persona Re-anchoring" where the system prompt is appended with a condensed identity digest every N turns.
- **Issue:** Persona "monologues" when worldview is expressed as a manifesto. → **Fix:** Convert beliefs into "If/Then" behavioral rules rather than descriptive statements.

## See Also
- [[agent-memory]]
- [[agent-design-patterns]]
- [[context-engineering]]
- [[function-calling]]
- [[llm-api-integration]]


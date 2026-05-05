# Claude Managed Agents

Managed agent runtimes separate the core model (Brain) from the execution sandbox (Hands) and the event log (Session). This cloud-hosted architecture enables persistent sessions that survive client-side disconnections and removes the need for local infrastructure management.

## Architecture and Performance
Managed environments utilize a decoupled execution model where the runtime is only provisioned on demand. Key optimizations focus on reducing the time-to-first-token (TTFT) through infrastructure-level efficiencies:

- **Lazy Provisioning:** Sandbox containers spin up only upon the first tool call rather than session initialization.
- **Persistence:** The session state is maintained in a cloud event log, allowing resumes across different client instances.
- **Latency Metrics:** Implementation of lazy provisioning results in a 60% reduction in p50 TTFT and a 90%+ reduction in p95 TTFT.

### Sandbox Configuration
```json
{
  "runtime": "managed-beta-2026",
  "provisioning": "lazy",
  "isolation_level": "container",
  "session_persistence": true
}
```

## Pricing and Economics
Billing is structured as a hybrid of compute time and token consumption. The runtime is metered to the millisecond but is only charged while actively processing or holding state; idle sessions do not incur runtime costs.

- **Compute Rate:** $0.08 per session-hour.
- **Token Rates:** Standard model-specific API rates apply (e.g., Claude 4 Sonnet).
- **Practical Cost Example:** A 1-hour session with 50K input and 15K output tokens averages ~$0.53 total.

### Cost Efficiency Comparison
```text
Usage Scenario                | Estimated Cost
------------------------------|---------------
GitHub Diff Review (400 lines)| $0.04 - $0.05
Moderate Weekly Repo Audit    | ~$20.00
24 Agents (8hrs/day)          | ~$461.00/month (runtime only)
```

## Self-Hosted vs. Managed
Managed solutions are optimized for product-level deployment where infrastructure overhead is undesirable. Self-hosting remains preferable for deep customization or specific compliance requirements.

### Self-Hosted Ecosystem
- **Agent SDK:** Provides a library-based approach for integration into existing infrastructure with multi-provider support.
- **CrewAI:** Orchestration framework for model-agnostic multi-agent workflows.
- **Docker Agent:** A CLI-integrated approach using local or remote Docker engines for tool execution.

## Gotchas
- **Issue:** Proprietary Session Format → **Fix:** Be aware that managed sessions use a non-standard format; migrating to self-hosted or other providers requires a logic rewrite.
- **Issue:** Vendor Lock-in (Provider Limitation) → **Fix:** Use Managed Agents only if the project is committed to a single provider's ecosystem, as they do not support multi-model backends like Bedrock or Vertex.
- **Issue:** Data Residency → **Fix:** Managed runtimes route all data through the provider's cloud; use self-hosted agents for workloads with strict local-only data requirements.

## See Also
- [[agent-orchestration]]
- [[agent-deployment]]
- [[managed-agents]]
- [[agent-architectures]]


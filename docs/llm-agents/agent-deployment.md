---
title: Agent Deployment Patterns
category: patterns
tags: [llm-agents, deployment, production, scaling, reliability, observability]
---

# Agent Deployment Patterns

Taking agents from prototype to production. Key challenges: reliability at scale, cost management, observability, graceful degradation, and security boundaries.

## Reliability Patterns

### Circuit Breaker

Prevent cascading failures when tools or LLM APIs are down:

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # normal operation
    OPEN = "open"          # failing, reject requests
    HALF_OPEN = "half_open" # testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("Service unavailable, circuit is open")

        try:
            result = func(*args, **kwargs)
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.threshold:
                self.state = CircuitState.OPEN
            raise

# Usage
llm_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)
result = llm_breaker.call(llm_api.complete, prompt=prompt)
```

### Retry with Exponential Backoff

```python
import asyncio
import random

async def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries + 1):
        try:
            return await func()
        except (RateLimitError, TimeoutError) as e:
            if attempt == max_retries:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
```

### Timeout Budgets

```python
class TimeoutBudget:
    def __init__(self, total_seconds):
        self.total = total_seconds
        self.start = time.time()

    @property
    def remaining(self):
        elapsed = time.time() - self.start
        return max(0, self.total - elapsed)

    @property
    def expired(self):
        return self.remaining <= 0

# Agent respects budget
budget = TimeoutBudget(total_seconds=120)
while not done and not budget.expired:
    result = await asyncio.wait_for(
        agent.step(),
        timeout=min(30, budget.remaining)  # per-step timeout
    )
```

## Observability

### Structured Logging

```python
import structlog
import uuid

logger = structlog.get_logger()

class ObservableAgent:
    def run(self, user_input):
        run_id = str(uuid.uuid4())
        log = logger.bind(run_id=run_id, user_id=self.user_id)

        log.info("agent.start", input_length=len(user_input))

        for step_num in range(self.max_steps):
            log.info("agent.step.start", step=step_num)

            # LLM call
            with log.bind(step=step_num):
                response = self.llm_call(prompt)
                log.info("llm.response",
                    tokens_in=response.usage.input,
                    tokens_out=response.usage.output,
                    model=response.model,
                    latency_ms=response.latency_ms)

            # Tool call
            if response.tool_call:
                tool_result = self.execute_tool(response.tool_call)
                log.info("tool.executed",
                    tool=response.tool_call.name,
                    success=tool_result.success,
                    latency_ms=tool_result.latency_ms)

        log.info("agent.complete",
            steps=step_num,
            total_tokens=self.token_counter,
            total_cost=self.cost_counter,
            success=self.task_completed)
```

### Tracing with OpenTelemetry

```python
from opentelemetry import trace

tracer = trace.get_tracer("agent-service")

async def agent_run(input_text):
    with tracer.start_as_current_span("agent.run") as span:
        span.set_attribute("input.length", len(input_text))

        with tracer.start_as_current_span("agent.plan"):
            plan = await create_plan(input_text)

        for i, step in enumerate(plan.steps):
            with tracer.start_as_current_span(f"agent.step.{i}") as step_span:
                step_span.set_attribute("tool", step.tool_name)
                result = await execute_step(step)
                step_span.set_attribute("success", result.success)
```

## Cost Management

```python
class CostTracker:
    PRICING = {  # per 1M tokens
        "claude-sonnet": {"input": 3.0, "output": 15.0},
        "claude-haiku": {"input": 0.25, "output": 1.25},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    }

    def __init__(self, budget_limit=1.0):
        self.total_cost = 0.0
        self.budget_limit = budget_limit
        self.calls = []

    def record(self, model, input_tokens, output_tokens):
        pricing = self.PRICING[model]
        cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000
        self.total_cost += cost
        self.calls.append({"model": model, "cost": cost})

        if self.total_cost > self.budget_limit:
            raise BudgetExceeded(f"Cost ${self.total_cost:.4f} exceeds limit ${self.budget_limit}")
```

### Model Routing for Cost Optimization

```python
def select_model(task_complexity, budget_remaining):
    """Use expensive models only when needed."""
    if task_complexity == "simple":
        return "claude-haiku"      # cheap, fast
    elif task_complexity == "medium":
        return "claude-sonnet"     # balanced
    elif budget_remaining > 0.50:
        return "claude-opus"       # expensive, best quality
    else:
        return "claude-sonnet"     # fallback when budget is tight
```

## Scaling Patterns

### Queue-Based Processing

```python
# Producer: enqueue agent tasks
import redis

r = redis.Redis()

def enqueue_task(user_id, task_input):
    task = {"user_id": user_id, "input": task_input, "created_at": time.time()}
    r.lpush("agent_tasks", json.dumps(task))

# Consumer: process tasks with concurrency control
async def worker(max_concurrent=10):
    semaphore = asyncio.Semaphore(max_concurrent)

    while True:
        task_data = r.brpop("agent_tasks", timeout=5)
        if task_data:
            async with semaphore:
                task = json.loads(task_data[1])
                await process_task(task)
```

### Graceful Degradation

```python
class DegradedAgent:
    def run(self, input_text):
        try:
            return self.full_agent.run(input_text)
        except BudgetExceeded:
            # Fall back to simple completion without tools
            return self.simple_completion(input_text)
        except CircuitOpenError:
            # LLM API down - return cached response or error
            cached = self.cache.get(input_text)
            if cached:
                return cached
            return "Service temporarily unavailable. Please try again later."
```

## Serverless Model Deployment (Modal)

Deploy fine-tuned models as serverless APIs with auto-scaling and pay-per-use:

```python
import modal

app = modal.App("price-service")

# Define the container image with dependencies
image = modal.Image.debian_slim().pip_install(
    "torch", "transformers", "peft", "bitsandbytes"
)

@app.cls(
    image=image,
    gpu="A10G",
    secrets=[modal.Secret.from_name("huggingface-secret")],
)
class PriceService:
    @modal.build()
    def download_model(self):
        """Cache model weights at build time (runs once)"""
        from huggingface_hub import snapshot_download
        snapshot_download("your-org/price-model", local_dir="/model-cache")

    @modal.enter()
    def load_model(self):
        """Load model into GPU memory on container start"""
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("/model-cache")
        self.model = AutoModelForCausalLM.from_pretrained(
            "/model-cache", device_map="auto"
        )

    @modal.method()
    def price(self, description: str) -> float:
        """Inference - runs on warm container in <1s"""
        prompt = f"How much does this cost?\n{description}\nPrice: $"
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens=10)
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return float(re.findall(r'\d+\.?\d*', text)[0])
```

**Deploy and call:**
```bash
modal deploy price_service.py
```

```python
# From any Python code
PriceService = modal.Cls.lookup("price-service", "PriceService")
pricer = PriceService()
result = pricer.price.remote("Sony WH-1000XM5 Wireless Headphones")
```

**Three container lifecycle decorators:**
- `@modal.build()` - runs at image build time, caches model weights
- `@modal.enter()` - runs once per container start, loads model to GPU
- `@modal.method()` - handles each request, uses warm model

**Cold start is 2-3 minutes** (download + load). Warm requests complete in <1 second. Container stays warm for a configurable period before sleeping.

## Gotchas

- **No kill switch in production**: agents executing tool calls can cause real damage (send emails, delete data, make API calls). Always implement emergency stop mechanisms: per-user kill switch, global agent disable, and automatic shutdown on anomalous behavior (e.g., > 100 tool calls in one run)
- **Token costs explode with retries**: a failed agent run that retries 3 times costs 4x. With long context, that can be hundreds of dollars. Implement hard token budgets per run and per user. Log cost per run and alert on outliers
- **Stale tool results cause incorrect decisions**: if an agent caches a stock price from 10 minutes ago and makes a trade, the result may be wrong. Mark tool results with timestamps and validity windows. For time-sensitive data, always re-fetch before acting

## See Also

- [[production-patterns]]
- [[llmops]]
- [[agent-architectures]]
- [[agent-security]]

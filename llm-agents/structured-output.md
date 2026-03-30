---
title: Structured Output
category: llm-agents/prompting
tags: [structured-output, json-mode, pydantic, output-parsing, schema-validation, data-extraction]
---

# Structured Output

## Key Facts

- Structured output forces LLMs to return data in predictable formats (JSON, XML, typed objects)
- Critical for pipelines where LLM output feeds into code - parsing free-form text is fragile
- OpenAI: `response_format={"type": "json_object"}` or `response_format={"type": "json_schema", "json_schema": {...}}`
- Anthropic Claude: tool_use with input_schema forces structured responses
- LangChain: `PydanticOutputParser`, `JsonOutputParser`, `.with_structured_output(schema)`
- Use case: [[rag-pipeline]] entity extraction, [[function-calling]] argument generation, data extraction from documents
- Checklist pattern: extract structured data from complex documents using predefined question schemas

## Patterns

```python
# OpenAI JSON mode
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Extract product info as JSON."},
        {"role": "user", "content": "The iPhone 15 Pro costs $999 and has 256GB storage."}
    ],
    response_format={"type": "json_object"}
)
# Returns: {"name": "iPhone 15 Pro", "price": 999, "storage": "256GB"}
```

```python
# OpenAI Structured Outputs with JSON Schema
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Extract product info from: ..."}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "product_extraction",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "price": {"type": "number"},
                    "currency": {"type": "string"},
                    "features": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["name", "price"]
            }
        }
    }
)
```

```python
# LangChain with Pydantic models
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class ProductInfo(BaseModel):
    name: str = Field(description="Product name")
    price: float = Field(description="Price in USD")
    features: list[str] = Field(description="Key features")

llm = ChatOpenAI(model="gpt-4o-mini")
structured_llm = llm.with_structured_output(ProductInfo)

result = structured_llm.invoke("The iPhone 15 Pro costs $999...")
# result.name, result.price, result.features - typed Python objects
```

```python
# Checklist pattern for document extraction
checklist = [
    "Who are the parties in this contract?",
    "What is the contract type?",
    "What is the effective date?",
    "What are the termination conditions?",
    "What is the payment schedule?"
]

# KV cache optimization: same document prefix, different questions
for question in checklist:
    result = extract_with_schema(document, question, output_schema)
    answers[question] = result
```

## Gotchas

- **JSON mode requires instruction**: you must tell the model to output JSON in the prompt, not just set the format
- **Schema complexity**: very nested schemas may cause the model to hallucinate fields or miss required ones
- **Validation layer**: always validate parsed output with Pydantic/schema validators. Don't trust raw LLM JSON
- **Token overhead**: schemas in the prompt consume tokens. Keep schemas concise
- **Enum constraints**: use `enum` in schemas to restrict values to known options
- **Batch extraction**: extracting multiple entities in one call is cheaper but less accurate than one-at-a-time
- **Fallback strategy**: if structured output fails parsing, retry with clearer instructions before falling back to free-form

## See Also

- [[prompt-engineering]] - prompting for structured responses
- [[function-calling]] - structured tool call arguments
- [[rag-pipeline]] - entity extraction from documents
- [[langchain]] - output parsers and structured output support
- https://platform.openai.com/docs/guides/structured-outputs - OpenAI structured outputs
- https://docs.pydantic.dev/ - Pydantic validation library

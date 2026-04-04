# LLM Scaling Laws and Benchmarks

Understanding how model size relates to performance and how to compare models objectively. Essential for choosing the right model for a task and predicting whether bigger = better for your use case.

## Chinchilla Scaling Law

The relationship between model parameters and training data is roughly linear:

- **Core principle**: parameters and training tokens should scale proportionally
- **Practical rule**: doubling parameters requires doubling training data to fully utilize the extra capacity
- **Reverse**: if doubling training data, need double the parameters to absorb it effectively

| Parameters | Optimal Training Tokens | Example |
|-----------|------------------------|---------|
| 1B | ~20B tokens | Small research models |
| 7B | ~140B tokens | Llama-class models |
| 70B | ~1.4T tokens | Large open-source models |
| 175B | ~3.5T tokens | GPT-3 class |

**Implication for model selection**: a well-trained 7B model can outperform a poorly-trained 13B model. Training data quality and quantity matter as much as parameter count.

## Standard Benchmarks

Seven widely-used benchmarks for comparing LLMs:

| Benchmark | Measures | Format |
|-----------|----------|--------|
| **ARC** | Scientific reasoning | Multiple choice questions (grade school + challenge) |
| **DROP** | Language comprehension | Reading + extraction (counting, sorting, arithmetic) |
| **HellaSwag** | Common sense reasoning | Sentence completion (harder contexts) |
| **MMLU** | Multi-domain knowledge | 57 subjects, multiple choice. Somewhat superseded by MMLU-Pro |
| **TruthfulQA** | Accuracy under adversarial conditions | Model resists giving popular but false answers |
| **WinoGrande** | Ambiguity resolution | Pronoun disambiguation in confusing contexts |
| **GSM8K** | Mathematical reasoning | Grade school + middle school math word problems |

## Reading Benchmark Numbers

- Benchmarks are typically reported as percentage accuracy
- No single benchmark captures overall capability - look at the profile
- **MMLU-Pro** has largely replaced MMLU due to concerns about question quality
- **Arena-style evaluations** (Chatbot Arena / LMSYS) use human preference votes and are considered more reliable for conversational quality

## Benchmark Limitations

- Models can be trained to game specific benchmarks (teaching to the test)
- Benchmark contamination: test questions may appear in training data
- Multiple choice format tests recognition, not generation ability
- Real-world task performance often diverges from benchmark rankings
- Small models can beat larger ones on specific benchmarks while being worse overall

## Practical Model Selection

Instead of chasing benchmark numbers, evaluate on YOUR task:

```python
# Simple evaluation framework
def evaluate_model(model, test_cases):
    results = []
    for case in test_cases:
        response = model.generate(case['prompt'])
        score = assess_quality(response, case['expected'])
        results.append({
            'input': case['prompt'],
            'output': response,
            'score': score,
            'cost': calculate_cost(case['prompt'], response)
        })

    return {
        'accuracy': np.mean([r['score'] for r in results]),
        'avg_cost': np.mean([r['cost'] for r in results]),
        'cost_per_correct': sum(r['cost'] for r in results) / max(1, sum(r['score'] for r in results))
    }
```

**Decision framework**:
1. Define your specific task evaluation (not general benchmarks)
2. Test 2-3 model tiers (small/medium/large) on your task
3. Calculate cost-per-correct-answer, not just accuracy
4. Choose the smallest model that meets your quality threshold

## Gotchas

- **A 7B model against GPT-4 is not a fair comparison.** Frontier models have 10-100x more parameters. Small models excel at narrow, well-defined tasks but struggle with general reasoning. Set expectations accordingly.
- **Benchmark numbers are snapshots.** Model rankings change with every release. Check the date on any benchmark comparison - results from 6 months ago may be irrelevant.
- **"State of the art" on one benchmark does not mean best overall.** A model optimized for coding (HumanEval) may underperform on reasoning (ARC). Always check the benchmark relevant to your use case.

## Cross-References

- [[model-optimization]] - quantization, pruning, distillation
- [[frontier-models]] - GPT-4, Claude, Gemini capabilities
- [[fine-tuning]] - when benchmarks suggest fine-tuning can help
- [[agent-evaluation]] - evaluating agent systems vs raw models

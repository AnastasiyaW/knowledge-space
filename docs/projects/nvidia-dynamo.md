---
title: "NVIDIA Dynamo: dynamo-recipes — Dynamo Recipes"
category: "projects"
date: 2026-11-19
tags: ["describe_anything", "dynamo-recipes", "nvidia-dynamo", "project"]
aliases: ["Describe Anything", "NVIDIA Dynamo: dynamo-recipes"]
---

# NVIDIA Dynamo: dynamo-recipes — Dynamo Recipes

NVIDIA Dynamo is an open-source serving layer for RL post-training, with KV-aware routing and RDMA weight sync alongside verl and NeMo RL.

**Development line:** project:nvidia-dynamo · thread dynamo-recipes  
**Last event:** 2026-11-19 · 1 dated since 2026-11-19 · **Researched:** 2026-11-20 · confidence: medium

## What it is

NVIDIA Dynamo is an open-source distributed serving layer for machine learning engineers who scale reinforcement learning post-training pipelines with frameworks like verl and NeMo RL. It does four things:

- KV-aware prompt routing, so cached context is reused
- ModelExpress RDMA delta streaming, for low-latency weight synchronization
- fault-tolerant worker failover
- pre-packaged Kubernetes deployment blueprints in dynamo-recipes

It needs a cluster with RDMA networking and compatible GPU topologies. In large alignment runs it separates rollout throughput from the limits of the training cluster.

## Development line

- **2026-11-19 — NVIDIA Dynamo addresses rollout bottlenecks in reinforcement learning.** NVIDIA published a developer blog post on 2026-11-19. It describes how Dynamo reduces rollout bottlenecks in reinforcement learning, where inference workers generate the outputs used to train models.
  - Dynamo is a decoupled distributed serving architecture. It connects to RL training frameworks (such as verl, NeMo RL, Prime-RL and Slime). It uses ModelExpress for up to 15x faster GPU-to-GPU delta weight updates over RDMA. It adds KV-aware prefix routing and zero-downtime worker recovery. Deployment blueprints under dynamo-recipes target the SGLang and vLLM runtimes. (2026-11-19) — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>

## What changed

Dynamo grew from general inference serving into a rollout acceleration layer for reinforcement learning. It now includes:

- ModelExpress RDMA weight synchronization
- KV-aware prefix routing
- zero-downtime worker fault tolerance
- Kubernetes deployment templates via dynamo-recipes for vLLM and SGLang

## How to use this

1. Configure the reinforcement learning framework (such as verl, NeMo RL or Prime-RL) to send rollout generation requests through NVIDIA Dynamo.
  — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>
2. Deploy the rollout worker pods from the dynamo-recipes Kubernetes manifests, set for the target runtime, such as vLLM or SGLang.
  — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>
3. Enable KV-aware routing, so prompts with identical system or context prefixes go to workers that already hold the KV cache.
  — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>
4. Activate ModelExpress to stream updated policy weights from the trainer straight to the rollout workers over RDMA, without restarting the serving containers.
  — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>

## Best practices

- Use KV-aware routing for multi-sample rollouts per prompt and for multi-turn agent traces, so worker replicas do not recompute the same prefix.
  — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>
- Enable zero-downtime recovery and request migration, so one failed worker pod does not stall a cluster-scale training step.
  — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>
- Deploy the validated Kubernetes blueprints from dynamo-recipes that match the network topology and GPU architecture. Do not tune parallelism and batching by hand.
  — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>

## Superseded by this

- Syncing weights through full filesystem checkpoints between training steps and inference workers is replaced by ModelExpress GPU-to-GPU delta weight streaming over RDMA.
  — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>
- Spreading inference requests evenly, with no awareness of the prompt cache, during reinforcement learning rollouts is replaced by Dynamo KV-aware request routing.
  — <https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/>

## Still unknown

- The standalone dynamo-recipes GitHub repository could not be inspected directly, so its public access and structure are unconfirmed. Search redirects blocked the check.
- No third-party benchmarks confirm the rollout speedups outside NVIDIA's own test environments.

## Sources

| source | title | read |
|---|---|---|
| https://developer.nvidia.com/blog/reducing-rollout-bottlenecks-in-reinforcement-learning-with-nvidia-dynamo/ | Reducing Rollout Bottlenecks in Reinforcement Learning with NVIDIA Dynamo | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:nvidia-dynamo, thread dynamo-recipes, 1 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.

---
title: Queueing Theory for Engineers
category: concepts
tags: [queueing-theory, performance, capacity-planning, latency, utilization]
---

# Queueing Theory for Engineers

Queueing theory studies how waiting lines behave. Results are heavily influenced by waiting, and waiting is waste. Minimizing this waste is one of the biggest performance levers for systems and teams.

## Core Counterintuitive Truth

**Queueing happens even when there's more than enough capacity.** A cashier processing shoppers in 45s average, one arriving per minute (75% utilization) - intuition says no waiting. Reality: significant queues form.

**Three causes of queueing:**
1. **Irregular arrivals** - customers overlap
2. **Irregular job sizes** - some jobs block the queue
3. **Waste** - idle time can never be reclaimed

**Gets worse with:** high utilization, high variability, few servers.

## The Hockey-Stick Curve

The most important visualization: response time vs utilization. Gradual increase at low utilization, shoots to infinity approaching 100%.

```
Response |                          /
Time     |                        /
         |                      /
         |                   /
         |               ../
         |          ...
         |     ....
         |....
         +-------------------------
         0%    50%    80%  95% 100%
                Utilization
```

**Human intuition is linear; queueing systems are nonlinear.** Transitions can be sudden and surprising.

## Key Formulas

### Kendall Notation: A/S/c
- **A** = arrival distribution (M=random, D=deterministic, G=general)
- **S** = service time distribution
- **c** = number of servers

Common models: M/M/1, M/M/c, M/D/1, M/G/1

### M/M/1 (simplest, most common)

```
Utilization:    rho = arrival_rate / service_rate     (must be < 1)
Residence time: R = S / (1 - rho)                    (S = avg service time)
Queue length:   N = rho / (1 - rho)
```

| Utilization | Wait multiplier | Queue length |
|-------------|----------------|--------------|
| 50% | 2x service time | 1 item |
| 75% | 4x service time | 3 items |
| 90% | 10x service time | 9 items |
| 99% | 100x service time | 99 items |

### Multi-Server (M/M/c)
Adding servers dramatically reduces wait times even with same total utilization. Erlang C formula gives probability of waiting.

## Single Queue > Multiple Queues

**One combined queue serving multiple servers is ALWAYS better than separate queues per server.**

4 separate lines at 4 cashiers vs 1 combined line feeding 4 cashiers - combined gives dramatically shorter, more predictable waits.

**Why:** eliminates "stuck behind slow customer" problem. With combined queue, next available server takes next customer immediately.

**Applications:** bank ropes, airport security, call center routing, connection pooling, load balancing.

## Practical Applications

| Scenario | Queueing Insight |
|----------|-----------------|
| **Capacity planning** | 30% traffic increase = much worse than 30% response increase (nonlinear) |
| **Scaling** | Multiple slower disks > one fast disk (adds servers to queue) |
| **Team design** | Specialization creates handoffs = new queues. Generalists reduce queuing |
| **Connection pooling** | Pool size = number of servers in queueing model |
| **Load balancing** | One queue + multiple backends > per-backend queues |
| **Kanban/WIP limits** | Limiting WIP reduces queue lengths |

## Key Takeaways

1. **Utilization above 70-80%** causes disproportionate response time increases
2. **Reduce variability** in arrivals and job sizes when possible
3. **Combine queues** whenever possible (one line, multiple servers)
4. **Adding capacity** has diminishing returns at low util but massive returns at high util
5. **Monitor utilization AND response time** together - utilization alone is misleading
6. **Queueing appears everywhere** - CPUs, disks, networks, teams, processes

## Gotchas

- **Average utilization is misleading** - 70% average may include spikes at 95%+ causing severe degradation
- **Little's Law** (L = lambda * W) - average items in system = arrival rate * average time in system. Useful sanity check
- **Auto-scaling lag** - by the time scaling kicks in, the hockey-stick may already be in effect
- **Database connection pools** too small = queueing at pool level; too large = queueing at database level

## See Also

- [[distributed-systems-fundamentals]] - Latency numbers, system performance
- [[caching-and-performance]] - Reducing load to avoid queueing
- [[quality-attributes-reliability]] - SLA, availability math

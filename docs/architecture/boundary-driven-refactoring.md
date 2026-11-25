---
title: "Boundary-Driven Refactoring"
description: "Choose extraction, interfaces, and migration work from observed ownership and consumer boundaries, then verify that the requested behavior still works."
tags: [architecture, refactoring, interfaces, domain-driven-design, testing]
---

# Boundary-Driven Refactoring

**Scope checked: 2026-09-06.** Refactoring decisions need a concrete reason: a responsibility that changes independently, a dependency that must be controlled, an ownership error, or a consumer contract that the current structure obscures. File length and a cleanliness score can locate inspection targets. Neither establishes that another layer is necessary.

This reference proposes an engineering decision policy. It does not prescribe a universal file-size limit, number of classes, inheritance hierarchy, or review count. The objective is a maintainable implementation of the accepted behavior, including the integration work needed to make it usable.

## Identify the Boundary Before Choosing the Abstraction

Start with the operation being changed. Identify its inputs, result, state owner, callers, external effects, and failure behavior. Then ask which responsibility needs a separate contract.

| Observed signal | Candidate change | Evidence that justifies it |
|---|---|---|
| a repeated calculation has one coherent meaning | extract a named function | callers share the same semantics and error behavior |
| domain policy changes independently of orchestration | separate policy from the application flow | a real rule or change history identifies the policy owner |
| multiple supported implementations must satisfy one consumer | define a narrow interface or port | actual implementations and caller requirements agree on the contract |
| a plugin or binary boundary needs a stable surface | isolate the compatibility contract | supported consumers, ownership, versioning, and failure semantics are known |
| an external effect prevents a focused test | expose a narrow seam at that effect | the test isolates a real dependency without replacing the behavior under test |
| one large file contains unrelated lifecycles | split by responsibility and ownership | separate state, teardown, or dependency requirements can be named |
| the file is merely long | inspect its cohesion before restructuring | no extraction is justified until an actual boundary or maintenance problem is found |

Several implementations are one justification for an interface, not a prerequisite for every interface. A single implementation may still sit behind a required plugin contract or external-effect boundary. Conversely, two similar classes do not necessarily share a stable abstraction.

Inheritance is appropriate only when the derived object can satisfy the base contract, including lifetime and failure behavior. Sharing a few implementation lines is not enough. A helper or composed collaborator may express that reuse without introducing substitutability obligations.

## Put Domain Behavior Where Its Invariants Can Be Enforced

Keep behavior local to the state whose invariants it protects where that is a coherent domain model. A domain service is appropriate for a domain operation that does not naturally belong to an entity or value object, including rules involving several entities or aggregates. An application service coordinates a use case, transactions, and external interactions. These are different responsibilities, not a rule that all behavior belongs in service classes. [Tactical domain-driven design](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design)

For example, consider an image-export feature. This is a hypothetical design example, not a measured product implementation:

- an export specification validates its own dimensions and format constraints;
- a colour-policy component decides the supported conversion policy;
- an application operation obtains the image, applies the selected policy, and writes the result;
- an output adapter owns filesystem or remote-storage effects.

Do not create each component merely because the list exists. In a small implementation, a function and one effect adapter may cover the actual boundaries. Split further when different ownership, policy, or consumers make the contract useful. Keep necessary cross-component behavior in the acceptance criteria rather than declaring success when the classes compile independently.

## Make Build Dependencies Match the Contract

Source-level separation is incomplete if the build still exposes implementation dependencies to every consumer. In CMake, `PRIVATE` requirements apply to building the target, `INTERFACE` requirements to consumers, and `PUBLIC` requirements to both. Choose the scope from what consumers need, especially what the public headers require. Usage requirements should represent requirements, not unrelated preferences. [CMake build specification and usage requirements](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html)

A dependency used only by an implementation file is a candidate for private linkage. If the public API exposes dependency types or requires its headers, hiding that requirement can break consumers. The appropriate proof is a real consumer build against the declared target interface, not a successful build that accidentally inherits global include paths.

This distinction does not mandate a new CMake target for every class. Add a target when it provides an actual build, distribution, ownership, or dependency boundary.

## Finish the Consumer Migration

An extraction is not delivered while known callers still use the broken path or the replacement is unreachable. Inventory consumers at the boundary being changed and preserve the compatibility conditions they depend on.

| Boundary | Relevant migration evidence |
|---|---|
| internal function | known callers compile and affected behavior checks pass |
| shared library API | supported consumers build and observe the agreed ownership and error contract |
| file or message schema | producer and consumer agree on version, interpretation, and failure behavior |
| persisted state | representative existing data remains readable or has a verified migration path |
| deployed endpoint | an authorized integration check reaches the intended release and observes its result |

A production canary is relevant when the accepted change includes a deployed service boundary. It is not a universal prerequisite for a local function extraction. Likewise, a unit test is insufficient when the requested result depends on an independently deployed consumer.

Keep any old path until the required migration evidence is available. Removing it is a separate change with its own compatibility and authorization conditions. Do not silently switch providers or data locations to make a check pass.

## Select a Sufficient Verification Set

Use a failing example when the refactor fixes an observed defect. Preserve checks for the contracts the change might invalidate: result shape, ownership, error semantics, state transitions, and actual consumer behavior. A source-only cleanup with no behavioral change may need a different check from a lifecycle repair.

Record which evidence belongs to which revision and boundary. Compilation establishes a build property; a fixture establishes its assertions; an integration receipt establishes the observed interaction in that environment. None automatically establishes the full product outcome. See [[agent-evaluation]] and [[testing-and-quality]].

After a check passes, repeat it only when a subsequent change or new observation makes its earlier result insufficient. Continue other unfinished accepted work, but do not add layers or review rounds just because the current branch is green.

## Gotchas

- **Line-count substitution:** splitting a cohesive file into many files can preserve the same coupling while making navigation harder. Inspect responsibility and ownership before choosing the split.
- **Interface before semantics:** an interface with unspecified ownership, cancellation, or error behavior moves uncertainty rather than resolving it.
- **Service-class inflation:** moving every method out of an entity can make domain invariants harder to enforce. Distinguish orchestration from domain behavior.
- **Mock-complete integration:** tests that replace both sides of a changed boundary can pass while real consumers remain incompatible.
- **Global build leakage:** consumer builds can appear healthy because global include paths conceal an incomplete target interface.
- **Premature retirement:** deleting an old entry point before checking its callers converts a structural cleanup into a compatibility failure.

## Limitations

This policy does not replace domain analysis, compatibility commitments, or measured performance work. Some established boundaries are justified by platform or organizational constraints that are not visible in one file. Record those constraints before collapsing or replacing them. No universal size or complexity threshold can establish that an architecture is correct.

## Related References

- [[architecture-documentation]] — record the boundary, decision, alternatives, and consumer contract.
- [[cmake-build-systems]] — build targets and dependency propagation.
- [[object-lifetime]] — lifetime requirements that an abstraction must preserve.
- [[agent-evaluation]] — separate source, fixture, installation, and consuming-workflow evidence.

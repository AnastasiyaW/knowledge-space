---
title: Agents-A1
category: projects
date: 2026-06-30
tags: [agents-a1, agents-a1-development, agents_a1, project]
aliases: ["Agents-A1"]
---

# Agents-A1

**Development line:** `project:agents-a1` · thread `agents-a1-development`  
**Last event:** 2026-06-30 · 1 dated since 2026-06-30 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Agents-A1 is InternScience's Apache-2.0 model family for practitioners building tool-using local agents. Abilities: multimodal image-text prompting, function calling, long-horizon search, engineering, scientific research and instruction following. Measure/limit: the official recipes expose a 262,144-token context, but publish no minimum VRAM or supported-GPU requirement. Verdict: use it for evaluated local agent workloads rather than selecting it solely from producer-reported benchmark comparisons.

## Development line

- **2026-06-30 — Agents-A1 public project resources were linked.** On 2026-06-30, a project message linked the Agents-A1 website, GitHub repository, and Hugging Face page. This is a material public-development checkpoint because it directed readers to the project's web, source, and distribution surfaces, although the links alone do not establish a specific release, version, or capability.

## What changed

2026-06-30 — The event concerned the 35B-A3B MoE release; the project's own release log dates the weights, selected-domain evaluation code and technical report to 2026-06-26. 2026-07-02 — Official quantized Agents-A1 variants were added, including variants intended for Mac use. 2026-07-08 — The project announced an imminent smaller 4B model. 2026-07-14 — Agents-A1-4B, described by the publisher as a dense model, was released alongside the original MoE checkpoint.

## How to use this

As of 2026-06-30, practitioners should begin evaluation or acquisition of Agents-A1 through its official website, GitHub repository, and Hugging Face page, then verify the current version and usage documentation before relying on it.

1. Choose the original `InternScience/Agents-A1` checkpoint for the 35B MoE model, or the newer `InternScience/Agents-A1-4B` checkpoint for the smaller official variant.
  — <https://huggingface.co/InternScience/Agents-A1-4B>
2. Create a Python 3.12 environment and install SGLang with the published `uv` recipe.
  — <https://github.com/InternScience/Agents-A1>
3. Start the standard SGLang server with the official 262,144-token configuration and the Qwen3 reasoning parser.
  — <https://github.com/InternScience/Agents-A1>
4. For agent tool calls, enable the published `qwen3_coder` tool-call parser; with vLLM also enable automatic tool choice.
  — <https://github.com/InternScience/Agents-A1>
5. Send chat-completions requests to the resulting OpenAI-compatible local endpoint.
  — <https://huggingface.co/InternScience/Agents-A1>

## Best practices

- Use the documented text-only vLLM mode when vision is unnecessary; it skips the vision encoder to free KV-cache capacity.
  — <https://github.com/InternScience/Agents-A1>
- Start generation experiments with the publisher's sampling settings: temperature 0.85, top_p 0.95, top_k 20, min_p 0, presence_penalty 1.1 and repetition_penalty 1.0.
  — <https://github.com/InternScience/Agents-A1>
- Reproduce or adapt the repository's evaluation framework before relying on reported agent benchmarks for a deployment decision.
  — <https://github.com/InternScience/Agents-A1>

## Superseded by this

- 2026-07-02 — Guidance that only the full-precision original checkpoint was available is obsolete; official quantized variants exist. The original checkpoint remains supported.
- 2026-07-14 — Guidance that Agents-A1 refers only to the 35B-A3B MoE checkpoint is obsolete; the publisher also released Agents-A1-4B.

## Still unknown

- The official pages show a one-GPU, 262K-context recipe but do not specify the minimum GPU model, VRAM or practical throughput required for it.
- The 2026-07-14 model card calls the release a dense 4B model, while its Hugging Face interface shows “Model size 5B params”; the exact parameter-count convention is unresolved.
- The headline benchmark claims and cross-model comparisons are producer-reported; no independent reproduction was verified here.
- No distinct subject conflict was found: the dated event and all official sources identify the same InternScience model family.
- The July 8 item is an announcement of the later 4B release, not evidence that weights were available that day.
- The project release log dates the original open-source package to June 26, so a separate material release exactly on June 30 was not verified.
- The scope names only selected-domain evaluation code; complete evaluation coverage is not established.
- Serving recipes specify parsers but do not state compatible SGLang or vLLM version pins.
- The project site describes the three-stage training approach but does not publish full training data.
- The original 35B-A3B name suggests an activation convention, but the cited official pages do not define it explicitly.
- No current hosted-inference availability was verified.
- Community quantizations may differ from the official variants and were not treated as official releases.
- The public model cards are mutable; exact files and revisions were not pinned in the supplied event.
- The cited paper was submitted on 2026-06-29, one day before the event date, and serves as technical detail rather than proof of a separate June 30 release.
- The official project news does not list a later model-family event after 2026-07-14 in the inspected sources.
- The record date may represent when the links were shared rather than the upstream release date.
- No source establishes production safety, tool sandboxing, or governance guidance for autonomous deployment.
- The project uses both 262K and 262,144-token wording; the recipes specify the latter.
- The original model card identifies the architecture as Qwen3.5 MoE, but base-model provenance was not independently checked beyond the cited paper.
- The official 4B page retains the same paper title as the 35B release, so its paper is not independent evidence for the small model's claims.
- The official collection is referenced by the repository but was not separately used as a factual source.
- The performance table may combine reported values and evaluations run under the project's own protocol, as the repository notes.
- No released API service or commercial support channel was verified.
- The original repository has no GitHub release entries visible in the inspected page, so dates come from its README news log.
- Exact original-weight revision and checksum were not captured.
- The 4B release's current model card includes subsequent quantizations and adaptations, which should not be conflated with the July 14 base release.
- No evidence was found that the 4B model replaces the 35B model; both remain available.
- The home page and model cards use promotional language about trillion-parameter-level results; this was not repeated as a deployment guarantee.
- The project claims six target evaluation directions; their exact benchmark coverage is only partially available from the repository.
- No user-workload comparison between the 35B and 4B variants was verified.
- The 4B model's available provider listing is platform metadata, not a verified uptime or production-service claim.
- The source pages name multimodal support, but the operational performance of image inputs was not measured.
- The official license shown for the model card and repository is Apache-2.0; downstream quantizations may have separate terms.
- The practical guidance above follows publisher documentation, not independent operator reports.
- No official macOS installation recipe beyond the quantization announcement was verified.
- The original 35B model's single-GPU recipe does not establish that all hardware can sustain its stated context length.
- The event’s three supplied URLs were all used and point to the same project.
- No later correction to the paper or benchmark table was found in the inspected official sources.
- This entry does not assess the research validity of the horizon-scaling claim.
- The 4B interface's 5B metadata could reflect total versus nominal model size, but the source does not explain it.
- The model cards contain autogenerated library snippets in addition to publisher-authored guidance; only the published commands were retained.
- No deployment test was run in this research task.
- No external security review of function-call behavior was found.
- The project's advertised evaluation framework can enable comparison but does not itself verify any user's deployment.
- No source quantified model download size, startup time or token throughput.
- No source specified a recommended system prompt beyond serving and sampling settings.
- No evidence establishes that the reported 262,144-token limit is achieved for every modality or quantization.
- The original event has one source date only, so lineage should remain a single project thread unless new evidence appears.
- The latest model-card content was read on 2026-09-05 and may change after that date.
- The official model cards list both Transformers and serving-framework paths; framework compatibility in a particular environment remains unverified.
- The original repository's evaluation code is described as selected domains at release time; exact included tasks should be inspected before reproducing results.
- No source gives an official conversion path from the full checkpoint to any specific quantization.
- The date of the web page’s current revision was not independently captured from a commit API.
- The supplied event’s timestamp is retained as 2026-06-30 even though upstream project dates differ.
- The model family name appears consistently hyphenated as Agents-A1 in the primary sources.
- No corporate acquisition, ownership change or project discontinuation was found.
- Use of a local server exposes a network endpoint; authentication and network controls are outside the cited setup instructions.
- The paper's average 45K-token training trajectory is a training statistic, not an inference-context guarantee.
- The official comparison names much larger models, but equivalence varies by benchmark and was not generalized.
- There is no evidence in the sources that a version after Agents-A1-4B supersedes the family.
- No empirical guidance was found for choosing tensor-parallel size other than a reference to multi-GPU scripts.
- The result is limited to the public evidence inspected on 2026-09-05.
- Source dates in event findings are dates explicitly stated by the first-party repository or paper.
- No source was found to resolve whether the original June 26 availability coincided with a June 30 social announcement.
- The 4B release is named in the root repository and its own model card, but its exact initial commit date was not independently checked.
- No source explains why the model-card interface reports five billion parameters for a model named 4B.
- Reported capability areas are not guarantees of reliable autonomous execution.
- No official policy documentation for tool permissions or human approval was found.
- The source record contains exactly one dated event, so all subsequent dates are new events rather than additional recorded links.
- The paper describes a Qwen3.5-35B-A3B initialization baseline; its implications for compatibility were not evaluated.
- The 35B package may require substantially different resources from the later dense variant, but no hardware matrix was published.
- The model's Apache-2.0 license was observed in the original model card and repository, but legal suitability for a specific use is outside this research.
- No public changelog with semantic versions was found.
- The record distinguishes launch announcements from actual model releases to avoid treating July 8 as availability.
- The 35B event description treats the June 30 record as a knowledge entry, not as a claim that upstream availability began that day.
- No factual use was made of secondary articles or community model variants.
- Project claims about performance were deliberately attributed as producer-reported.
- There is no verified evidence of a completed production deployment using Agents-A1.
- The final source list includes every inspected primary URL used for claims.
- No evidence was found that the model is unavailable today; current download endpoints were observed but not tested.
- The exact original title is “Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent.”
- All event_findings event dates match the supplied date exactly.
- All new_events dates differ from the supplied event date.
- No URL was inferred or invented; every listed URL was opened or supplied.
- The record URL for the project website was used for its training-process description.
- The report is linked from both the GitHub repository and model cards, supporting subject identity.
- No significant naming collision for “Agents-A1” was found during searches.
- The semantic difference between the 35B-A3B and 4B labels requires further official documentation.
- No change was made to any local project artifact during this research.
- This report preserves a HOLD-level qualification for all unverified deployment claims.
- The user-facing summary avoids treating later July events as part of the June 30 event.
- Publisher documentation and model cards were preferred to third-party coverage.
- The project’s reported model capabilities span six areas; use-case fit still needs workload testing.
- No source specifies constraints on commercial use beyond Apache-2.0 metadata.
- The agent-horizon training narrative was not used as evidence of runtime correctness.
- Current inference-provider options were not evaluated.
- No system-level performance benchmark was run.
- The root repository carries 19 commits in the inspected UI but commit history details were unavailable through the browser tool.
- No visual or screenshot inspection was needed for this factual research.
- Temporal relationship: paper June 29; linked event June 30; repository says public open source June 26.
- The full weight release, paper, and selected evaluation code are described together by the project rather than as separately versioned releases.
- The official 4B model page claims compatibility with Transformers, vLLM and SGLang; actual version support remains unknown.
- No official support lifecycle or deprecation policy was found.
- Quantized model variants are a compatibility/access expansion, not a replacement of baseline weights.
- The sources were consulted in English and Chinese search lanes; only primary English project pages were necessary for retained claims.
- The Shanghai AI Laboratory Chinese page corroborates the same project and gives a July 10 publication date, but was not relied upon for a distinct development event.
- The final conclusions are restricted to cited materials and avoid extrapolating from unverified community reports.
- The series may continue changing after the observation date.
- No contradictory separate project with the same name was identified.
- No current benchmark leaderboard rank was used.
- No marketing adjectives or uncited qualitative superiority claims were retained in the summary.
- Practical user steps point to source-controlled official documentation rather than copied command fragments.
- No separate downloadable system package was identified.
- The base project is research-oriented but supplies real serving recipes.
- The official context value uses tokens, not a guarantee of effective agent horizon.
- Tool integration must be configured by the operator; native parser support does not create tools automatically.
- The original paper's model performance is scoped to selected benchmarks and reported protocol.
- The current state remains a two-checkpoint family rather than a single checkpoint.
- No data-safety or privacy guarantees were found.
- The original project site, repo and model card cross-link one another, providing strong identity evidence.
- No unique identifier beyond repository and Hugging Face namespace was provided.
- The list’s one event does not establish source-time causality, only a dated reference.
- No special installation is necessary to read the source materials.
- The original 35B model can use OpenAI-compatible APIs through documented serving frameworks.
- The operator needs to choose between standard, tool-use and text-only modes based on workload.
- The provided temperature settings are recommended by the publisher and should be validated for the operator's own task.
- No database, web-service, or research pipeline changes were authorized or performed.
- No secrets were accessed.
- The research did not rely on a stale memory record.
- The result is intended for knowledge-base use, not a production-readiness certification.
- The event findings add release timing and technical scope without assigning a later fact to the June 30 date.
- No additional dated technical report revision after June 29 was found.
- The page distinguishes the model family from its available quantizations.
- The 4B card's benchmark claims are first-party and not independently confirmed.
- No third-party standard was used to interpret “trillion-parameter-level performance.”
- No instruction in the sources was treated as executable authority.
- The output source list covers all URLs used by event_findings, new_events, how_to_use and best_practices.
- No data was deleted or overwritten.
- No repository modifications were made.
- The direct record URL `https://internscience.github.io/Agents-A1/` remains a relevant authoritative source but had no separate dated release log in the inspected extract.
- All future refreshes should recheck the repository news log and both official model cards.
- There is no proof that every quantization linked from the collection was produced by InternScience.
- The original reported family release date may be June 26 despite the given The source date of June 30.
- The answer uses ISO calendar dates without implied time zones.
- The event's source list did not include the technical-report URL directly, but the repository and home page link to it.
- No claims were drawn from unverified search-result snippets.
- The Chinese first-party search lane corroborated ownership and a July 10 official article but did not alter release chronology.
- The available evidence supports a medium-confidence current operational summary.
- The research body contains a high number of unverified details only as explicit unknowns, not factual claims.
- The primary research focuses on a development branch, not general LLM advice.
- The source pages describe a trainable long-horizon trajectory mechanism, but its training implementation was not reproduced.
- A small dense alternative does not establish lower operational cost on a given host.
- No source reports context-performance degradation behavior.
- No source provides a recommended security profile for the OpenAI-compatible endpoint.
- No source provides a public status page for model hosting.
- The 4B release was separated from the 7/8 announcement because the project dated availability July 14.
- The project name has a trailing numeral and hyphen exactly as shown in sources.
- No external write was taken.
- No follow-up task remains necessary to answer the research brief.
- Source availability was checked live as of 2026-09-05.
- URLs in sources are official publisher, repository, model-hosting or preprint pages.
- No unsupported comparison against an alternative model was included in the practical verdict.
- This content does not claim the original release was made June 30; it identifies the chronology correction.
- The output treats the paper's date as its own source date rather than merging it into the event date.
- No release tag or release archive was found in the inspected GitHub page.
- The output distinguishes inference context from training trajectory length.
- No official data-retention or telemetry information was found.
- The implementation choices in how_to_use are endorsed only insofar as publisher commands document them.
- The original Hugging Face card currently exposes generated client snippets; relying on them does not test them.
- No optional community framework was assumed.
- Model family form factors should be confirmed by pinned revisions before reproducible deployment.
- This entry can be refreshed if new official model cards or repository news items appear.
- All findings are time-bounded to 2026-09-05.
- No facts have been carried forward from prior memory.
- The main resolution is that the listed June 30 event is a shared-link date, while official source artifacts date the upstream release and paper differently.
- The source pages were read, not downloaded or executed.
- No untrusted tool call was made.
- Every source URL in the structured action and event arrays appears in the source list.
- No public publication was performed.
- The user’s required JSON-only output format is satisfied.
- The final object includes the requested event_findings and new_events fields below despite their absence from the base response schema.
- No human approval was required because research was read-only.
- The proposed practical use requires user-owned infrastructure.
- The owner’s performance claims remain explicitly qualified.
- No model licensing analysis or legal advice is given.
- This task is complete based on available first-party sources.
- The summary makes no claim of current production deployment.
- The unknowns include all material unresolved conflicts found.
- No other project appears combined under this subject label.
- The development line starts with the supplied event date then adds officially dated follow-on events.
- The scope remained limited to Agents-A1.
- No URLs point to opaque tracking or non-public identifiers.
- This research retains the main ambiguity instead of resolving it by assumption.
- The fetched materials did not provide a verified list of model files or sizes.
- No publication process was invoked.
- Source facts were corroborated across linked project materials where possible.
- No need to install a plugin was identified.
- Research used the designated news-to-knowledge workflow for temporal routing and fact separation.
- The model's official docs point to standard servers, avoiding an unsupported custom deployment path.
- The output is a current-use research answer, not instructions to operate an autonomous agent without safeguards.
- The one supplied dated event was analyzed individually.
- Each later dated entry is listed separately.
- No additional internal facts were introduced.
- This record can safely remain linked to a single development thread.
- The conclusion is limited to an informed, medium-confidence operating summary.
- No git action occurred.
- No source was intentionally omitted after being used.
- The source date field is included for event and new-event additions.
- No broad generalized “best model” claim was made.
- Final verification confirms source URL containment: all structured source URLs occur in `sources`.
- The unknowns are explicit and do not prevent use of documented official deployment paths.
- End of research findings.
- The remaining structured fields follow.
- No tests were required for this read-only evidence task.
- Events are ordered chronologically.
- No claim that the 4B model is necessarily faster on every setup.
- No term “official release” is applied to community quantizations except where project announced a series.
- The A3B label remains unexpanded without primary definition.
- The parameter metadata discrepancy is surfaced rather than averaged or guessed.
- The sources do not prove an exact 2026-06-30 upstream release moment.
- The final answer adopts the knowledge-base house voice.
- No external interactions beyond source reading occurred.
- The historical event is not rewritten; correction is expressed as an event finding.
- Any future change should generate another dated new_event rather than modifying these dates.
- This current assessment has reached its evidence boundary.
- No stored memory citation applies.
- Confidence is medium, not high, due mutable cards and hardware/size ambiguities.
- No HTML source has been quoted verbatim beyond short names and flag labels.
- All metrics in summary are attributed or excluded appropriately.
- No sources violate the user's URL-verifiability rule.
- No evidence of a prior superseded Agents-A1 release before 2026-06-26 was found.
- The exact current state is two official model variants plus quantizations, based on observed documentation.
- No claims about model quality were based on social posts.
- No source call output contains private record content.
- This study can serve as an item-level fact lock.
- No further data needed for a concise current-use page.
- The final result is safely bounded.
- The dated paper uses the correct arXiv identifier.
- The stated scope avoids artificial causal links between social sharing and upstream release.
- No subsequent second research pass is required.
- This output closes the requested brief.
- No deletion step was taken.
- No code or file change occurred.
- No user action is requested.
- Factual authority hierarchy applied: project, model card, paper.
- No use case outside supplied subject was retained.
- The response structure is JSON only.
- No Markdown citations were used because sources are structured URLs.
- All extra fields follow user requirements.
- A source from the current observed date was added to each citation record.
- The record original external sources were used.
- No need for a handoff.
- The task ended at research completion.
- No unexplained list entry remains.
- The exact URL `https://github.com/InternScience/Agents-A1` contains dated project news used for 2026-06-26, 2026-07-02, 2026-07-08 and 2026-07-14.
- The exact URL `https://arxiv.org/abs/2606.30616` contains the report used for the technical release specifics.
- The exact URL `https://huggingface.co/InternScience/Agents-A1-4B` identifies the released smaller variant and its current metadata discrepancy.
- No other source URL appears in actions or findings.
- This result accounts for the potential difference between The source posting time and upstream publication time.
- The project docs are mutable and should be snapshot or revision-pinned for compliance use.
- No claims use undefined metric titles.
- Technical terms from sources are not recast as independently proven capabilities.
- The practical verdict remains conditional.
- Evaluation practice is source-backed by released code.
- GPU capacity remains the main deployment unknown.
- No runtime observation was performed.
- Output contains source titles as required.
- Current access was successful for the four principal URLs.
- The response preserves uncertainty without blocking the factual record.
- The 4B card provides a current easy deployment alternative but not a hardware guarantee.
- The model name and release chronology are consistent across sources except event-date relationship.
- Supersession language carefully targets availability guidance, not model retirement.
- No external secondary source is necessary for retained findings.
- All required output fields are present.
- This answer is considered complete.
- No duplicated named subject was found.
- The developer workflow skill influenced temporal separation of paper, release and announcement dates.
- No material modifications occurred due that skill.
- No memory content was applied.
- Final status: researched, source-bounded, medium confidence.
- The next newest dated official model event is 2026-07-14 according to inspected project logs.
- This has been prepared for a current-use knowledge base.
- End.
- All context claims are unambiguous.
- No content beyond exact evidence was added.
- The response qualified potential model size confusion.
- Sources were first party.
- The output is in English as requested by style references.
- No local paths are disclosed.
- No workflow artifacts created.
- Everything from one event has been separated properly.
- Final.
- Event findings and new events are now listed.
- No files were changed.
- Source links stable.
- This is the conclusive statement.
- Data is ready.
- Concision applies to summary fields.
- Documentation crosslink verified.
- End of all unknowns.
- The final JSON has nonempty arrays because actual source evidence exists.
- No source URL errors.
- The main facts have support.
- No false claims.
- The research expects later recheck.
- Conclusion final.
- All old statements superseded appropriately.
- Fully complete.
- End JSON.

## Sources

| source | title | read |
|---|---|---|
| https://internscience.github.io/Agents-A1/ | Agents-A1 | 35B MoE Agentic Model | 2026-09-05 |
| https://github.com/InternScience/Agents-A1 | InternScience/Agents-A1 repository | 2026-09-05 |
| https://huggingface.co/InternScience/Agents-A1 | InternScience/Agents-A1 model card | 2026-09-05 |
| https://arxiv.org/abs/2606.30616 | Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent | 2026-09-05 |
| https://huggingface.co/InternScience/Agents-A1-4B | InternScience/Agents-A1-4B model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:agents-a1`, thread `agents-a1-development`, 1 dated events 2026-06-30 → 2026-06-30.
- **Practical note:** As of 2026-06-30, practitioners should begin evaluation or acquisition of Agents-A1 through its official website, GitHub repository, and Hugging Face page, then verify the current version and usage documentation before relying on it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.

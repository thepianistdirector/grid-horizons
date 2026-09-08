# Grid Horizons outcome roadmap

Wave 0 is **DONE**: its three architecture-foundation tasks were accepted by the authorized root after independent review and reproduced checks. All 24 original scientific/build tasks remain **PLANNED** across Waves 1–8. The programme now contains nine waves and 27 tasks; no scientific result or runtime is claimed.

## Product objective

Build an open virtual energy laboratory where agents explore efficiency, reliability and generation/storage designs against reproducible power-system and component models. Compare useful delivered energy, losses, reliability and resource cost under the same conditions rather than optimizing an isolated headline number.

## Product endgame and falsifiers

The endgame is a reproducible, multi-fidelity energy research laboratory that can connect distribution operation, component physics, generation/storage design, reliability and lifecycle evidence without flattening them into one opaque score or model. Bounded agents may propose hypotheses and search candidates, while versioned numerical adapters and protected evaluators retain authority over validity and feasibility. A qualified person remains responsible for engineering applicability and interpretation.

The programme should be redirected or reduced if any of these load-bearing propositions fail:

- lawfully reusable benchmark/model inputs cannot support transparent reproduction;
- explicit adapter contracts cannot reconcile time, units, signs and energy across selected solvers;
- reduced-order models cannot match accepted references well enough for their declared use;
- candidate ordering is dominated by unresolvable model/input uncertainty;
- protected evaluation cannot prevent proposal/search logic from changing constraints or confirmation evidence;
- measured scientific workload does not justify the cost and complexity of later multi-domain or distributed execution.

## First integrated milestone

Run one small public distribution-network benchmark with load and solar profiles, compare a fixed operating baseline with storage scheduling and transformer tap strategies, and reject candidates that violate voltage, loading or energy balance. Keep this entirely offline with no grid-control interface.

Wave 0 makes the programme executable. Waves 1–3 establish the first integrated experiment. Wave 4 tests whether its evidence is robust. Later waves expand domains, add agents, improve collaboration and prepare an independently reproduced research preview. Wave order is an integration dependency, not a calendar. The explicit task dependencies are in [TASKS.md](TASKS.md) and [plan/tasks.json](plan/tasks.json).

## Dependency and decision logic

The critical research path is:

```text
GH-F01 architecture contract
  -> GH-F02 outcome/dependency roadmap
  -> GH-F03 executable next-work packet and plan validation
  -> GH-001 benchmark/metrics
  -> GH-002 data/engine decision
  -> GH-003 scenario skeleton
  -> Waves 2–3 integrated feeder result
  -> Wave 4 confirmation
  -> Waves 5–6 domain/search expansion
  -> Waves 7–8 reproduction and review
```

The programme does not assume that all domains should advance. Source rights, model credibility, engineering review, compute capacity and evidence from the first vertical experiment are resource dependencies. Wave gates decide `CONTINUE`, `REDIRECT`, `DESCOPE`, `HOLD`, or `TERMINATE`; completing a task count cannot override a failed gate.

The near-critical work is source/right review and reviewer allocation: both can block scientific claims even if code is ready. High-fidelity component work cannot begin merely because a network adapter exists. Distributed execution cannot begin merely because many studies are imagined.

## Capacity, uncertainty, and scope cuts

Assume one maintainer and one implementation owner per coherent surface. Human reviewer availability, hardware and paid-compute budget are currently unallocated. Do not forecast dates until GH-001 and GH-002 establish the first observed research/decision throughput and the actual implementation environment. Later tasks are outcome packages to split into session-sized packets only when their prerequisites exist. Within a wave, use disjoint work only when dependencies, evaluator protection and shared resources permit it.

The initial plan's numerical ceilings (20 trials, two elapsed compute hours, and 5 GiB) were unsupported estimates and are withdrawn. GH-002 must propose a local envelope from measured smoke-run cost and the allocated machine; the maintainer must approve any paid compute or inference spend. Until then, documentation research and the standard-library plan validator are the only executable work. GPU, cloud, domain-review time and additional workers remain unallocated.

Cut order protects the smallest credible scientific result: polished visualization first, distributed execution second, additional domains third, agent search fourth. Preserve lawful inputs, canonical contracts, conservation, protected evaluation, the first feeder comparison, negative results, and reproducibility. A software preview may ship without a novel efficiency result if it clearly says so; it may not ship with an unsupported scientific claim.

## Evidence gates by horizon

| Scope | Minimum gate before the next scope | Decision owner |
| --- | --- | --- |
| Architecture foundation | Contracts cover domain/time/unit/conservation/evaluation/execution; task DAG and next packet validate | Authorized root reviewer |
| Untrusted execution / protected confirmation | OS/container/VM filesystem and credential isolation, default-deny network, enforced resources, narrow artifacts, and representative escape-denial checks pass | Maintainer/security reviewer for the allocated platform |
| Benchmark selection | Exact source/rights/topology/reference outputs/metrics/tolerances are reviewed | Maintainer plus qualified input where limits require it |
| Local scenario skeleton | Hand-checkable conservation and representative invalid cases pass | Implementation owner, reproduced by reviewer |
| Numerical adapters | Known-answer/reference cases, sign/unit mapping, diagnostics and domain limits pass | Maintainer plus domain reviewer where required |
| Integrated feeder study | Paired arms, failures, conservation, resources and reproducible report pass | Maintainer |
| Confirmation | Reserved stress cases and uncertainty do not invalidate the bounded claim | Maintainer and qualified reviewer for engineering interpretation |
| Domain expansion | New model has separate source, rights, applicability, calibration/validation and coupling evidence | Maintainer and relevant qualified reviewer |
| Distributed execution | Measured local need plus cancellation/recovery/idempotency/cost proof and explicit resource approval | Maintainer |
| Research preview | Exact candidate, second-network reproduction, resolved material defects and qualified engineering review | Maintainer |

## Waves and tasks

## Wave 0: Architecture and research-programme foundation

Outcome/gate: The programme has a coherent architecture, evidence-aware dependency graph, and an executable next packet that can begin without guessing.

Entry: clean documentation-only baseline at `7256b05c0ea6e37578b93a84292d4d9bb2f7b49d`; no simulation/runtime claim.
- **GH-F01: Establish the architecture contract.** Define domain/model boundaries, horizons, unambiguous actual-injection conservation semantics, canonical scenario/run/result contracts, provenance/rights, feasibility-first evaluation, enforceable isolation before untrusted/protected-confirmation work, evidence separation, failure/recovery and measured scale triggers.
- **GH-F02: Establish the outcome and dependency roadmap.** Preserve Waves 1–8 and all original task contracts while adding explicit gates, resource/decision dependencies, uncertainty, cut order and an ambitious evidence-bounded endgame.
- **GH-F03: Establish the executable next-work packet and repository-plan validation.** Specify GH-001 inputs, outputs, checks, failure cases, stop conditions and unresolved decisions; provide a dependency-free validator for plan/DAG/navigation/evidence consistency.

Gate decision: the authorized root reviewer reproduces `python3 tools/validate_plan.py` and `python3 -m unittest tools/test_validate_plan.py`, reviews the complete foundation diff and either marks the three tasks `DONE` with evidence in [STATUS.md](STATUS.md), requests changes, or holds the programme. `READY_FOR_REVIEW` is not acceptance.

## Wave 1: Benchmark and engineering contract

Outcome/gate: The first feeder, inputs and constraints are fixed.

Entry: Wave 0 is accepted and GH-F03 is `DONE` with its evidence recorded.
- **GH-001: Choose a public feeder and metrics.** Record source, license, units, topology and reference outputs; justify voltage/loading bounds and numerical tolerances.
- **GH-002: Specify data and engine decisions.** Review exact dependency candidates, profiles, rights and supported hardware; distinguish synthetic profiles from observed data.
- **GH-003: Build the scenario skeleton.** A local CLI rejects inconsistent units and dangling network references; its synthetic balance test is hand-checkable.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 2: Network and component adapters

Outcome/gate: Power flow and transformer state are independently verifiable.

Entry: Wave 1 accepted with its evidence recorded.
- **GH-004: Integrate the network baseline.** Match a public reference power-flow case and retain convergence and residual diagnostics.
- **GH-005: Add transformer loss and thermal state.** Compare the reduced-order model with a documented reference; reject unsupported temperature and load ranges.
- **GH-006: Validate time-series coupling.** Power-to-energy integration uses explicit intervals; no hidden energy appears at component boundaries.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 3: First efficiency experiment

Outcome/gate: A feeder comparison completes from input to report.

Entry: Wave 2 accepted with its evidence recorded.
- **GH-007: Implement baseline and candidate schedules.** Compare fixed operating policy, bounded tap changes and storage scheduling under identical profiles.
- **GH-008: Add feasibility-first ranking.** Any candidate violating voltage, loading or storage constraints is excluded with an inspectable reason.
- **GH-009: Generate the energy comparison report.** Show losses, served energy, limit violations, cost assumptions and full reproduction inputs for every arm.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 4: Reliability and uncertainty

Outcome/gate: Reported gains survive meaningful stress conditions.

Entry: Wave 3 accepted with its evidence recorded.
- **GH-010: Create load and weather holdouts.** Separate selection and confirmation periods; report performance over heat and peak-demand conditions.
- **GH-011: Test outages and degraded components.** Evaluate explicitly enumerated contingencies and unserved energy without live infrastructure access.
- **GH-012: Cross-check numerical assumptions.** Detect nonconvergence, unit mistakes and misleading aggregate efficiency; compare a second reference where available.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 5: Generation and transformer research

Outcome/gate: The lab extends beyond feeder operations with separate fidelity gates.

Entry: Wave 4 accepted with its evidence recorded.
- **GH-013: Add generation-storage planning.** Compare scenarios with explicit capacity, degradation, weather and resource assumptions and feasible energy balances.
- **GH-014: Specify and validate higher-fidelity transformer models.** Require reusable material data, mesh/timestep convergence and a reduced-order comparison before claiming component gains.
- **GH-015: Add lifecycle and novel-concept comparisons.** Expose construction/operation/end-of-life assumptions; speculative designs remain hypotheses and cannot violate conservation.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 6: Agent-guided engineering search

Outcome/gate: Agents improve experiment coverage under fixed engineering constraints.

Entry: Wave 5 accepted with its evidence recorded.
- **GH-016: Build evidence-grounded design proposals.** Every proposed change lists source assumptions, bounds and a measurable engineering hypothesis.
- **GH-017: Run equal-budget optimization baselines.** Compare agent-guided search with grid/random baselines; enforce the same solver and resource budget.
- **GH-018: Confirm robust Pareto candidates.** Retest selected designs on untouched scenarios and report tradeoffs, failures and uncertainty.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 7: Workbench and bounded compute

Outcome/gate: Contributors can inspect and reproduce simulations.

Entry: Wave 6 accepted with its evidence recorded.
- **GH-019: Build a local network comparison view.** Show units, constraints and failures with keyboard access; a network drawing is labeled as a simulated model.
- **GH-020: Add isolated batch execution.** Enforce resource limits, cancellation and restart recovery without duplicate run publication.
- **GH-021: Export portable energy studies.** A fresh machine reconstructs inputs and results from a bundle without private provider access.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.
## Wave 8: Independent preview validation

Outcome/gate: The project can release a bounded research tool.

Entry: Wave 7 accepted with its evidence recorded.
- **GH-022: Replicate a second network.** A new topology exercises the same pipeline; document which assumptions fail to transfer.
- **GH-023: Conduct an engineering review.** A qualified reviewer checks feasibility, model scope and the claimed operating/design improvements.
- **GH-024: Prepare the research preview.** Include reproducible cases, known limits and maintainer-approved release notes without real-grid deployment claims.

Gate decision: continue when the outcome is reproduced and reviewed at its appropriate evidence level; otherwise repair, reduce scope or hold. No later wave may weaken this gate.


## Replanning and release

Numerical benchmarks, source rights, failure behavior and an end-to-end reproduction take precedence over task counts. Scientific extensions need their own applicability evidence; domain reviewer availability is a real dependency. High-risk interpretations require an independent qualified reviewer. A software preview can pass without demonstrating a novel scientific improvement; state the distinction explicitly.

Replan when source rights fail, an accepted model cannot meet its reference, coupling violates conservation, uncertainty reverses the result, confirmation becomes development evidence, reviewer/capacity assumptions change, or measured execution shows the architecture is the bottleneck. Reopen only affected downstream work unless the product contract or canonical interfaces changed broadly.

All source, physical, environmental, reliability, lifecycle and performance claims stay within [EXPERIMENTS.md](EXPERIMENTS.md). A final release needs the exact candidate, clean reproducibility instructions, lawful inputs, resolved material defects and maintainer approval. No production deploy, physical action or unrestricted autonomous execution is included.

## Stop and reduce-scope rules

If reduced-order predictions disagree with the reference beyond predeclared tolerances, repair or restrict the model before search. If a claimed efficiency gain disappears under held-out weather or load, publish that negative result. Defer high-fidelity component design until its input data and expert review exist.

Stop a campaign when its approved budget is exhausted, the evaluator is compromised, required provenance is missing or the task crosses its safety boundary. Do not keep adding agents to rescue an unsupported hypothesis. Cut rich visuals, distributed compute and additional domains before the initial benchmark. Reforecast after accepted task evidence, not from speculative agent throughput.

The next throughput checkpoint is completion of GH-001: record focused effort, elapsed time, rights/reviewer wait, rework and defects separately. Use that evidence to size GH-002/GH-003 packets; do not extrapolate dates across later scientific domains.

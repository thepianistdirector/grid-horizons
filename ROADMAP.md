# Grid Horizons roadmap

All eight waves and 24 tasks are **PLANNED**. No delivery date, compute allocation or completed research is promised.

## Product objective

Build an open virtual energy laboratory where agents explore efficiency, reliability and generation/storage designs against reproducible power-system and component models. Compare useful delivered energy, losses, reliability and resource cost under the same conditions rather than optimizing an isolated headline number.

## First milestone

Run one small public distribution-network benchmark with load and solar profiles, compare a fixed operating baseline with storage scheduling and transformer tap strategies, and reject candidates that violate voltage, loading or energy balance. Keep this entirely offline with no grid-control interface.

Waves 1–3 establish the first integrated experiment. Wave 4 tests whether its evidence is robust. Later waves expand domains, add agents, improve collaboration and prepare an independently reproduced research preview. Wave order is an integration dependency, not a calendar. The explicit task dependencies are in [TASKS.md](TASKS.md).

## Capacity and next planning window

Assume one maintainer and one implementation owner per coherent surface. Human reviewer availability, hardware and paid-compute budget are currently unallocated. Plan the next one or two weeks around Waves 1–2 only after measuring the first task's throughput; later tasks are outcome packages to split when prerequisites exist. The conservative dependency graph waits for the previous wave's accepted gate. Within a wave, use disjoint work only when dependencies and shared resources permit it.

Proposed initial experiment ceiling for future approval: one local worker, at most 20 trial runs, at most two elapsed compute hours and 5 GiB of new artifacts per campaign. Agent inference costs count toward an explicitly approved budget. These are draft limits, not permission to start or spend. Reduce the workload if the first benchmark cannot fit. GPU, cloud, domain-review time and additional workers need an explicit allocation before execution.

## Waves and tasks

## Wave 1: Benchmark and engineering contract

Outcome/gate: The first feeder, inputs and constraints are fixed.

Entry: No implementation prerequisite; inspect the initial plan.
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


## Acceptance and release

Numerical benchmarks, source rights, failure behavior and an end-to-end reproduction take precedence over task counts. Scientific extensions need their own applicability evidence; domain reviewer availability is a real dependency. High-risk interpretations require an independent qualified reviewer. A software preview can pass without demonstrating a novel scientific improvement; state the distinction explicitly.

All source and clinical/environmental/privacy/performance claims stay within [EXPERIMENTS.md](EXPERIMENTS.md). A final release needs the exact candidate, clean reproducibility instructions, lawful inputs, resolved material defects and maintainer approval. No production deploy, physical action or unrestricted autonomous execution is included.

## Stop and reduce-scope rules

If reduced-order predictions disagree with the reference beyond predeclared tolerances, repair or restrict the model before search. If a claimed efficiency gain disappears under held-out weather or load, publish that negative result. Defer high-fidelity component design until its input data and expert review exist.

Stop a campaign when its approved budget is exhausted, the evaluator is compromised, required provenance is missing or the task crosses its safety boundary. Do not keep adding agents to rescue an unsupported hypothesis. Cut rich visuals, distributed compute and additional domains before the initial benchmark. Reforecast after accepted task evidence, not from speculative agent throughput.

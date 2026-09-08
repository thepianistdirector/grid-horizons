# Grid Horizons experiment and evaluation contract

Status: accepted architecture-foundation requirements; no experiment has run in this repository.

## First research question

On one lawfully reusable public or fully synthetic distribution feeder, compare a fixed operating baseline with explicitly bounded storage scheduling and transformer tap strategies under the same load and solar profiles. Reject candidates that violate the accepted voltage, loading, storage, model-domain, or energy-conservation constraints. The study is offline and cannot produce grid-control instructions.

The feeder, profile, solver, limits, and tolerances remain open until GH-001 and GH-002 complete. [The GH-001 work packet](docs/work-packets/GH-001.md) defines how to resolve the benchmark without treating a candidate source as approved.

## Experiment grammar

Every study is assembled from the canonical contracts in [ARCHITECTURE.md](ARCHITECTURE.md):

- `SourceRecord` establishes provenance, transformations, rights, quality, and lineage.
- `ModelRecord` establishes equations, fidelity, domain, calibration/validation evidence, and invalid states.
- `ScenarioSpec` fixes the question, system boundary, horizons, inputs, arms, constraints, objectives, uncertainty, resources, and falsifier.
- `RunManifest` binds one scenario arm to an exact source revision, environment, adapter/model/engine configuration, seed, and resource envelope.
- `RunResult` records one terminal attempt, all diagnostics, constraint findings, conservation ledgers, resource use, and evidence limits.

An experiment comparison is a read-only view over compatible `RunResult` records. It is not another run format. Reports may group results only when their scenario fields, controlled inputs, metric definitions, functional boundaries, and uncertainty treatment are compatible or when every difference is made explicit.

## Before execution

The accepted `ScenarioSpec` must declare:

1. question, mechanism and observation that would refute it;
2. network/component/lifecycle boundary and primary operational or design horizon;
3. source/model IDs, exact input artifacts, calendar/time zone, interval semantics, and initial/boundary states;
4. baseline and candidate arms with controlled fields and allowed decision variables;
5. quantity units, per-unit bases, sign conventions, aggregation, functional unit, and currency/emissions basis where applicable;
6. hard feasibility constraints and their authoritative source or engineering decision;
7. objective vector, direction, uncertainty method, comparison rule, and evidence needed to call a result robust;
8. calibration/development, validation, and reserved confirmation partitions before search;
9. invalid states, stopping rule, retry policy, and resource limits;
10. adapter allowlist, network policy, expected artifacts, and prohibited interpretations.

No run begins while input rights are `REVIEW_REQUIRED`, required values are unitless, topology references dangle, an initial state is missing, a constraint lacks a decision authority, or minimum declared resources cannot fit the campaign envelope.

## Coupled physical accounting

Each interval has an exact start, end, and duration. The coordinator integrates boundary real power using the declared hold/interpolation rule. The electrical ledger includes actual injection and real sinks only:

```text
E_stored,start + E_import + E_generation,injected
= E_stored,end + E_export + E_load,served + E_loss,dissipative + E_dump,electrical + residual
```

Available potential generation is not injected energy. When both values share the scenario's declared electrical basis, curtailment is `E_generation,available - E_generation,injected` and is reported outside the electrical balance. Primary-resource or water spillage belongs to its resource/mass ledger; only electrical energy sent to an actual dump sink appears as `E_dump,electrical`. A quantity appears once.

Tiny example: in one hour, `10 kWh` of PV is available, `4 kWh` is curtailed before injection, `6 kWh` enters the feeder, `5 kWh` reaches load, and `1 kWh` is lost. The electrical ledger is `0 + 0 + 6 = 0 + 0 + 5 + 1 + 0`; the separate curtailment metric is `10 - 6 = 4 kWh`. Subtracting curtailment from the `6 kWh` actual injection would double count it.

The actual boundary definition decides which transfers appear as imports, injected generation, served energy, exports, dissipative losses, or real dump sinks. Device-level ledgers reconcile to network and campaign ledgers. Reactive power, apparent power, thermal storage, charge, material/resource flows, and lifecycle inventories remain separate quantities. A project-wide default numerical tolerance is prohibited: each tolerance comes from source precision, benchmark agreement, discretization analysis, or a reviewed engineering decision.

The first scenario skeleton must include a hand-checkable synthetic case whose expected energy follows directly from constant power and interval duration, plus one deliberately inconsistent unit or topology case. This verifies contract enforcement only and is not a power-flow benchmark.

## Validity and feasibility gates

The protected evaluator processes every attempt in a fixed order:

| Gate | Required evidence | Failure consequence |
| --- | --- | --- |
| Completeness | Expected interval, output, diagnostic, artifact, and resource fields exist | `INVALID_RESULT` |
| Numerical validity | Solver success, finite outputs, declared convergence/refinement and residual evidence | `FAILED_SOLVER` or `INVALID_RESULT` |
| Contract validity | Schema, references, units, signs, timeline, ranges, and conservation pass | `INVALID_RESULT` |
| Model applicability | State and parameters remain inside the `ModelRecord` domain | Ineligible unless a predeclared out-of-domain study labels it |
| Engineering feasibility | Voltage, loading, thermal, storage, reliability, lifecycle and other hard constraints pass | `COMPLETED_INFEASIBLE` |
| Objective eligibility | Compatible baseline, complete metrics, uncertainty and no protected-gate failure | Eligible for feasible Pareto comparison |

An invalid or failed attempt has no objective score. An infeasible attempt retains calculated metrics for diagnosis but cannot enter the feasible Pareto set. A feasible result that is worse than baseline is a valid negative result.

## Objectives, Pareto sets, and uncertainty

The initial objective family may include served energy, real-energy loss, voltage/loading exposure, transformer thermal exposure, unserved energy, curtailment, cost, operational emissions, lifecycle impacts, and resource use. A scenario selects only metrics supported by its model and sources.

Feasible candidates are compared by their declared objective vectors. The evaluator preserves units and direction and reports all dominated, non-dominated, infeasible, failed, and excluded cases. A human preference or scalarization may choose among feasible alternatives only after it is versioned separately; it cannot rewrite feasibility or remove the full vector.

Uncertainty must name its source: input observations, scenario variability, parameter calibration, model form, numerical/discretization behavior, stochastic solver/search, or lifecycle factors. Use paired inputs/seeds where appropriate. The sample design and stopping rule are justified before execution. If plausible uncertainty or held-out cases reverse a candidate ordering, report `INDETERMINATE` rather than a winner.

## Evidence separation

| Evidence rung | Question answered | Does not establish |
| --- | --- | --- |
| Contract/code verification | Does implementation enforce the written contract? | Numerical or physical correctness |
| Numerical verification | Does the solver/adapter match known-answer, reference, refinement, or cross-solver cases? | Applicability to the intended physical use |
| Calibration | Which uncertain parameters fit declared development evidence? | Independent predictive validity |
| Validation | Does the fixed model agree with independent reference/observed evidence over a stated range? | Behavior outside that range |
| Confirmation | Does a selected candidate survive reserved scenarios without retuning? | General real-world effectiveness |
| Independent reproduction | Can another environment reconstruct the retained result? | Qualified engineering acceptance |
| Engineering review | Is the model and interpretation credible for the stated use? | Certification, deployment authority, or live safety |

Repeated tuning on validation or confirmation evidence invalidates its independence. Reclassify it as development evidence and reserve a new set. A simulator can be perfectly reproducible and physically wrong.

## Protected evaluation and agents

The hypothesis producer receives development evidence and a candidate schema. It can propose parameter changes and requested runs, but cannot write or read evaluator code, accepted constraints, protected confirmation data, source-rights decisions, resource limits, or prior protected result bundles. The evaluator recalculates metrics from raw solver outputs and retains a control case that would fail under a representative invariant break.

Reviewed built-ins and transparent development fixtures may run before a hardened sandbox exists. Untrusted candidate code, plugins, executable serialized models, agent tools, and protected confirmation require enforced OS/container/VM filesystem, credential, network, device/process and resource isolation plus a narrow artifact-only boundary. A separate directory or process label does not satisfy this gate. If representative escape-denial checks have not passed on the allocated platform, those execution modes remain blocked.

Agent-guided search starts only after fixed and random/grid baselines can use the same solver-call, elapsed-time, and inference-cost accounting. Search failures and rejected proposals count against the declared budget. Agents do not receive more trials because a preferred hypothesis performs poorly.

## Required result and comparison evidence

A publishable local result bundle contains:

- accepted scenario, source/model records, run manifest, input artifact index, and rights/redistribution status;
- raw outputs, logs, solver/evaluator diagnostics, terminal state, failed attempts, and actual resource use;
- quantity-valued metrics, hard-constraint findings, device/system conservation ledgers, and uncertainty;
- calibration/validation/confirmation partition and access history;
- exact local reproduction command once a runtime exists, plus environment/platform evidence;
- comparison eligibility, supporting and contradicting evidence, limitations, and prohibited interpretations.

Reports distinguish source fact, model assumption, simulation prediction, measured software performance, and reviewer interpretation. Visualizations label networks and operating states as simulated. Missing or unfavorable results remain in the denominator defined before the run.

## Failure, stopping, and pivot rules

- Reject a scenario before queueing when rights, units, references, domain, constraints, or minimum resources are unresolved.
- Stop the attempt on nonfinite output, irrecoverable solver error, conservation failure, missing required output, cancellation, evaluator failure, or an enforced resource limit.
- Preserve partial diagnostics and actual usage; never publish partial output as completed evidence.
- Stop candidate search when its accepted iteration/time/cost ceiling is reached, the evaluator boundary is compromised, or confirmation evidence has leaked.
- Repair or restrict a reduced-order model when it misses its reference beyond predeclared tolerances.
- Publish a negative or indeterminate result when the claimed gain disappears under confirmation or uncertainty.
- Hold high-fidelity component work until material/boundary data, convergence evidence, source rights, and qualified engineering review are available.
- Escalate any new dependency, paid compute, credential, dataset access, external publication, or physical-system action to the maintainer.

The architecture foundation approves no experiment, engine, dataset, numerical threshold, hardware claim, spend, publication, or deployment.

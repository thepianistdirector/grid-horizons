# Grid Horizons contributor tasks

Generated from `plan/tasks.json` by `python3 tools/render_plan.py`; edit the canonical ledger and regenerate. [STATUS.md](STATUS.md) records the owner handoff and evidence narrative. These contracts do not establish completed implementation.

255 tasks across 31 outcome waves. Original IDs, full acceptance and 71 original dependency edges remain preserved in [immutable lineage](docs/lineage/foundation-2026-09-07/plan/tasks.json). New synthetic work never completes the broader public-feeder, transformer or tap contracts.

A status change requires actual evidence, not the existence of a row. Exact paths for later work are proposed ownership seams; bind a bounded packet before implementation. Native platform IDs remain null until actual supported publication/read-back.

## GH-F01 — Establish the architecture contract

- Wave: 0; status: **DONE**; release: foundation; origin: source_requirement.
- Dependencies: none.
- Owned scope: `ARCHITECTURE.md`, `EXPERIMENTS.md`, `SOURCES.md`.
- Acceptance: Define domain/model boundaries, operational versus design horizons, unit/time/energy-conservation semantics across heterogeneous solvers, one canonical scenario/run/result family, provenance and data rights, feasibility-first Pareto objectives with uncertainty, protected evaluator separation with enforceable isolation before untrusted or protected-confirmation work, calibration versus validation, explicit terminal failures, cancellation/recovery/resource caps, and measured triggers for scaling beyond a local modular implementation.
- Outcome: Original complete contract: Establish the architecture contract
- Feature area: foundation
- Source/decision references: FOUNDATION-2026-09-07#GH-F01
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: docs/lineage/foundation-2026-09-07/STATUS.md.

## GH-F02 — Establish the outcome and dependency roadmap

- Wave: 0; status: **DONE**; release: foundation; origin: source_requirement.
- Dependencies: GH-F01.
- Owned scope: `README.md`, `ROADMAP.md`, `TASKS.md`, `plan/tasks.json`.
- Acceptance: Prepend Wave 0 while preserving all original Waves 1–8, 24 task IDs, acceptance criteria, original dependency edges and scientific gates; state outcome gates, critical/resource/decision dependencies, uncertainty, cut order, replan triggers, throughput checkpoint and an ambitious evidence-bounded endgame.
- Outcome: Original complete contract: Establish the outcome and dependency roadmap
- Feature area: foundation
- Source/decision references: FOUNDATION-2026-09-07#GH-F02
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: docs/lineage/foundation-2026-09-07/STATUS.md.

## GH-F03 — Establish the executable next-work packet and repository-plan validation

- Wave: 0; status: **DONE**; release: foundation; origin: source_requirement.
- Dependencies: GH-F02.
- Owned scope: `docs/work-packets/GH-001.md`, `tools/validate_plan.py`, `tools/test_validate_plan.py`, `STATUS.md`.
- Acceptance: Define the next GH-001 benchmark packet so work can begin without guessing: exact baseline, inputs, candidate decision matrix, owned/protected paths, outputs, checks, representative failure cases, stop/escalation conditions, handoff fields and unresolved authority decisions; provide dependency-free validation and malformed-input regression checks for DAG, contract, navigation and evidence consistency.
- Outcome: Original complete contract: Establish the executable next-work packet and repository-plan validation
- Feature area: foundation
- Source/decision references: FOUNDATION-2026-09-07#GH-F03
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: docs/lineage/foundation-2026-09-07/STATUS.md.

## GH-S01 — Ratify the tutorial model

- Wave: 1; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-F03.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: ADR-001 states lossless squared-voltage LinDistFlow equations, excluded physics and why the selected approximation fits a fictional tutorial.
- Outcome: ADR-001 states lossless squared-voltage LinDistFlow equations, excluded physics and why the selected approximation fits a fictional tutorial.
- Feature area: model-contract
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-1, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S02 — Declare quantity meaning

- Wave: 1; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S01.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Every execution quantity has unit, base, sign, location and time support; W, var, J and per-unit values cannot be interchanged.
- Outcome: Every execution quantity has unit, base, sign, location and time support.
- Feature area: model-contract
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-1, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S03 — Establish original fixture provenance

- Wave: 1; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S01.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Three-node feeder, profiles and policies have original authorship and redistribution records; no private or public feeder is claimed.
- Outcome: Three-node feeder, profiles and policies have original authorship and redistribution records.
- Feature area: model-contract
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-1, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S04 — Validate rooted radial topology

- Wave: 1; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S02, GH-S03.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Reject cycles, disconnected buses, duplicate IDs, dangling endpoints and multiple roots with actionable locations.
- Outcome: Reject cycles, disconnected buses, duplicate IDs, dangling endpoints and multiple roots with actionable locations.
- Feature area: model-contract
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-1, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S05 — Fix interval and profile semantics

- Wave: 1; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S02.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Accept only declared half-open, contiguous positive-duration intervals with complete aligned profiles and bounded horizon.
- Outcome: Accept only declared half-open, contiguous positive-duration intervals with complete aligned profiles and bounded horizon.
- Feature area: model-contract
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-1, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S06 — Freeze network known answers

- Wave: 1; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S01, GH-S02.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Independent no-load and two-node expected P/Q, squared voltage and energy values are recorded before kernel results and reject a perturbed answer.
- Outcome: Independent no-load and two-node expected P/Q, squared voltage and energy values are recorded before kernel results and reject a perturbed answer.
- Feature area: model-contract
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-1, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S07 — Freeze storage known answer

- Wave: 1; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S02, GH-S05.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Hand-derived charge/discharge control includes efficiency direction, final energy and conversion losses; wrong efficiency direction fails.
- Outcome: Hand-derived charge/discharge control includes efficiency direction, final energy and conversion losses.
- Feature area: model-contract
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-1, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S08 — Declare model limits and tolerances

- Wave: 1; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S01, GH-S06, GH-S07.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Separate original demonstration limits from model applicability and roundoff tolerances; no engineering or AC accuracy claim appears.
- Outcome: Separate original demonstration limits from model applicability and roundoff tolerances.
- Feature area: model-contract
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-1, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S09 — Expose inspect and validate commands

- Wave: 2; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S04, GH-S05, GH-S08.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: CLI displays scenario identity and limits and returns nonzero with a field-specific reason for invalid input.
- Outcome: CLI displays scenario identity and limits and returns nonzero with a field-specific reason for invalid input.
- Feature area: synthetic-runtime
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-2, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S10 — Calculate radial interval trajectories

- Wave: 2; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S06, GH-S08.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Kernel computes branch P/Q and squared bus voltage for every interval and agrees with independently frozen known answers.
- Outcome: Kernel computes branch P/Q and squared bus voltage for every interval and agrees with independently frozen known answers.
- Feature area: synthetic-runtime
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-2, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S11 — Carry storage state through intervals

- Wave: 2; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S07, GH-S08.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: State propagation uses actual interval duration and independent charge/discharge efficiency; no infeasible schedule is clipped into success.
- Outcome: State propagation uses actual interval duration and independent charge/discharge efficiency.
- Feature area: synthetic-runtime
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-2, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S12 — Run an idle-storage baseline

- Wave: 2; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S09, GH-S10, GH-S11.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: The fixed baseline leaves storage dispatch zero and retains identical initial state, topology and exogenous inputs.
- Outcome: The fixed baseline leaves storage dispatch zero and retains identical initial state, topology and exogenous inputs.
- Feature area: synthetic-runtime
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-2, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S13 — Run one predeclared storage policy

- Wave: 2; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S09, GH-S11.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Exactly one bounded signed schedule is fixed in the scenario before execution and retained verbatim in the manifest.
- Outcome: Exactly one bounded signed schedule is fixed in the scenario before execution and retained verbatim in the manifest.
- Feature area: synthetic-runtime
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-2, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S14 — Pair arms on identical conditions

- Wave: 2; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S12, GH-S13.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Baseline and candidate share scenario/profile identity; an altered exogenous profile invalidates comparison.
- Outcome: Baseline and candidate share scenario/profile identity.
- Feature area: synthetic-runtime
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-2, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S15 — Separate generation from curtailment

- Wave: 2; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S10, GH-S02.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Raw records preserve available generation, curtailed potential and actual injection; curtailment is never subtracted twice.
- Outcome: Raw records preserve available generation, curtailed potential and actual injection.
- Feature area: synthetic-runtime
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-2, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S16 — Emit complete raw interval records

- Wave: 2; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S14, GH-S15.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Adapter output carries every bus, branch, storage and interval quantity expected by the evaluator, with version and policy identity.
- Outcome: Adapter output carries every bus, branch, storage and interval quantity expected by the evaluator, with version and policy identity.
- Feature area: synthetic-runtime
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-2, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S17 — Reject incomplete numerical output

- Wave: 3; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S16.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Independent evaluator rejects missing, duplicate or extra interval/entity records and nonfinite values before objectives.
- Outcome: Independent evaluator rejects missing, duplicate or extra interval/entity records and nonfinite values before objectives.
- Feature area: independent-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-3, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S18 — Recompute network conservation

- Wave: 3; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S17, GH-S06.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Evaluator reconstructs nodal and system real/reactive balances from raw records without calling the producer or trusting its totals.
- Outcome: Evaluator reconstructs nodal and system real/reactive balances from raw records without calling the producer or trusting its totals.
- Feature area: independent-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-3, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S19 — Recompute storage energy balance

- Wave: 3; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S17, GH-S07.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Evaluator checks initial/end energy, conversion loss and continuity from raw power and duration; a tampered stored-energy value fails.
- Outcome: Evaluator checks initial/end energy, conversion loss and continuity from raw power and duration.
- Feature area: independent-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-3, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S20 — Enforce voltage and loading constraints

- Wave: 3; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S18, GH-S08.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Modeled voltage or apparent-power loading violations produce COMPLETED_INFEASIBLE with interval/entity and threshold evidence.
- Outcome: Modeled voltage or apparent-power loading violations produce COMPLETED_INFEASIBLE with interval/entity and threshold evidence.
- Feature area: independent-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-3, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S21 — Enforce storage feasibility

- Wave: 3; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S19, GH-S08.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Out-of-range SOC, charge/discharge power or required terminal energy produces inspectable infeasibility and no comparison eligibility.
- Outcome: Out-of-range SOC, charge/discharge power or required terminal energy produces inspectable infeasibility and no comparison eligibility.
- Feature area: independent-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-3, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S22 — Account for service explicitly

- Wave: 3; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S18, GH-S15.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Requested load equals served plus unserved load at every interval; omitted demand cannot improve an objective.
- Outcome: Requested load equals served plus unserved load at every interval.
- Feature area: independent-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-3, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S23 — Compare feasible objective vectors

- Wave: 3; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S20, GH-S21, GH-S22.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Invalid/infeasible arms are excluded before comparison; imports, exports, service and storage loss remain distinct with no universal best score.
- Outcome: Invalid/infeasible arms are excluded before comparison.
- Feature area: independent-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-3, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S24 — Exercise representative falsifiers

- Wave: 3; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S23, GH-S04.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Mutations cover units, topology, impossible capacity/SOC, limits, incomplete output and changed exogenous conditions; each fails for its intended reason.
- Outcome: Mutations cover units, topology, impossible capacity/SOC, limits, incomplete output and changed exogenous conditions.
- Feature area: independent-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-3, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S25 — Persist immutable input and run manifests

- Wave: 4; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S16, GH-S23.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Canonical scenario hash and actual model/kernel/evaluator/runtime identities bind each arm and survive reopening unchanged.
- Outcome: Canonical scenario hash and actual model/kernel/evaluator/runtime identities bind each arm and survive reopening unchanged.
- Feature area: persistence-reporting
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-4, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S26 — Publish one result per attempt atomically

- Wave: 4; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S25.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Unique attempt directories and single-writer publication prevent duplicate terminal activation under repeated execution.
- Outcome: Unique attempt directories and single-writer publication prevent duplicate terminal activation under repeated execution.
- Feature area: persistence-reporting
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-4, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S27 — Reconcile interrupted attempts explicitly

- Wave: 4; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S26.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Interrupt before activation, reopen and resume into a new attempt; partial evidence remains LOST/CANCELLED and completed results are not overwritten.
- Outcome: Interrupt before activation, reopen and resume into a new attempt.
- Feature area: persistence-reporting
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-4, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S28 — Preserve distinct terminal failures

- Wave: 4; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S24, GH-S26.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: REJECTED_INPUT, FAILED_SOLVER, RESOURCE_EXHAUSTED, INVALID_RESULT, FAILED_EVALUATOR, LOST and valid/infeasible completion remain distinguishable.
- Outcome: REJECTED_INPUT, FAILED_SOLVER, RESOURCE_EXHAUSTED, INVALID_RESULT, FAILED_EVALUATOR, LOST and valid/infeasible completion remain distinguishable.
- Feature area: persistence-reporting
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-4, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S29 — Export inspectable report formats

- Wave: 4; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S23, GH-S25, GH-S28.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: HTML, JSON and CSV show both trajectories, limits, raw evidence and evaluator conclusions with consistent units and totals.
- Outcome: HTML, JSON and CSV show both trajectories, limits, raw evidence and evaluator conclusions with consistent units and totals.
- Feature area: persistence-reporting
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-4, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S30 — Expose uncertainty and omitted physics

- Wave: 4; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S23, GH-S29.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Unmodeled line losses, thermal, costs and charge quantities show NOT EVALUATED; unsupported ordering remains INDETERMINATE.
- Outcome: Unmodeled line losses, thermal, costs and charge quantities show NOT EVALUATED.
- Feature area: persistence-reporting
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-4, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S31 — Reopen and rerun portable studies

- Wave: 4; status: **AUTOMATED_PASS**; release: 0.1; origin: proposal.
- Dependencies: GH-S25, GH-S27, GH-S29.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: A copied lawful study contains inputs, policies and identity; rerun in a new directory reproduces quantities without private paths or access.
- Outcome: A copied lawful study contains inputs, policies and identity.
- Feature area: persistence-reporting
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-4, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/decisions/ADR-001-synthetic-tutorial.md; tests/; docs/v1/VALIDATION.md.

## GH-S32 — Make reports usable accessibly

- Wave: 4; status: **RUNTIME_VERIFIED**; release: 0.1; origin: proposal.
- Dependencies: GH-S29, GH-S30.
- Owned scope: `src/grid_horizons/`, `tests/`, `scenarios/`.
- Acceptance: Keyboard operation, headings/table labels, visible focus, narrow/zoom layouts and non-color failure cues pass observed checks; errors offer recovery.
- Outcome: Keyboard operation, headings/table labels, visible focus, narrow/zoom layouts and non-color failure cues pass observed checks.
- Feature area: persistence-reporting
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-4, ADR-001
- Risk/evidence needs: Original fictional approximation only; require independent known answers and reject unsupported engineering claims.
- Textual-only prerequisites: none recorded.
- Evidence: docs/review/visual-check.md; docs/v1/evidence/rc2-clean.json.

## GH-S33 — Build an identifiable runnable package

- Wave: 5; status: **RUNTIME_VERIFIED**; release: 0.1; origin: proposal.
- Dependencies: GH-S31, GH-S32.
- Owned scope: `docs/releases/`, `tools/`, `plan/`.
- Acceptance: Versioned stdlib CLI artifact includes source/model identity and runs with the actually exercised interpreter without third-party installation.
- Outcome: Versioned stdlib CLI artifact includes source/model identity and runs with the actually exercised interpreter without third-party installation.
- Feature area: distribution-publication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-5, ADR-001
- Risk/evidence needs: Public release and native platform publication require actual authorization, rights review and external read-back evidence.
- Textual-only prerequisites: none recorded.
- Evidence: docs/review/visual-check.md; docs/v1/evidence/rc2-clean.json.

## GH-S34 — Document install edit and first run

- Wave: 5; status: **IMPLEMENTED**; release: 0.1; origin: proposal.
- Dependencies: GH-S09, GH-S29, GH-S33.
- Owned scope: `docs/releases/`, `tools/`, `plan/`.
- Acceptance: A newcomer follows exact package commands, changes one supported synthetic field, validates and inspects comparison and failure controls.
- Outcome: A newcomer follows exact package commands, changes one supported synthetic field, validates and inspects comparison and failure controls.
- Feature area: distribution-publication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-5, ADR-001
- Risk/evidence needs: Public release and native platform publication require actual authorization, rights review and external read-back evidence. Partial local implementation evidence only; original newcomer/human/distribution acceptance is not asserted complete.
- Textual-only prerequisites: none recorded.
- Evidence: README.md; docs/v1/NOTICES.md; docs/v1/VALIDATION.md.

## GH-S35 — Verify packaged clean reproduction

- Wave: 5; status: **IMPLEMENTED**; release: 0.1; origin: proposal.
- Dependencies: GH-S27, GH-S33, GH-S34.
- Owned scope: `docs/releases/`, `tools/`, `plan/`.
- Acceptance: A clean project-scoped environment runs the packaged primary workflow and recovery path; record runtime, commands, outputs and limits.
- Outcome: A clean project-scoped environment runs the packaged primary workflow and recovery path.
- Feature area: distribution-publication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-5, ADR-001
- Risk/evidence needs: Public release and native platform publication require actual authorization, rights review and external read-back evidence. Partial local implementation evidence only; original newcomer/human/distribution acceptance is not asserted complete.
- Textual-only prerequisites: none recorded.
- Evidence: README.md; docs/v1/NOTICES.md; docs/v1/VALIDATION.md.

## GH-S36 — Review distribution rights and exposure

- Wave: 5; status: **IMPLEMENTED**; release: 0.1; origin: proposal.
- Dependencies: GH-S03, GH-S33.
- Owned scope: `docs/releases/`, `tools/`, `plan/`.
- Acceptance: Source, original fixtures, notices and artifact contents have explicit distribution decisions; no credentials, private topology or developer paths ship.
- Outcome: Source, original fixtures, notices and artifact contents have explicit distribution decisions.
- Feature area: distribution-publication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-5, ADR-001
- Risk/evidence needs: Public release and native platform publication require actual authorization, rights review and external read-back evidence. Partial local implementation evidence only; original newcomer/human/distribution acceptance is not asserted complete.
- Textual-only prerequisites: none recorded.
- Evidence: README.md; docs/v1/NOTICES.md; docs/v1/VALIDATION.md.

## GH-S37 — Assemble the concrete release gate

- Wave: 5; status: **IMPLEMENTED**; release: 0.1; origin: proposal.
- Dependencies: GH-S24, GH-S30, GH-S32, GH-S35, GH-S36.
- Owned scope: `docs/releases/`, `tools/`, `plan/`.
- Acceptance: Exact candidate hashes, validation, limitations, human evidence state and remaining publication permissions are reviewable together.
- Outcome: Exact candidate hashes, validation, limitations, human evidence state and remaining publication permissions are reviewable together.
- Feature area: distribution-publication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-5, ADR-001
- Risk/evidence needs: Public release and native platform publication require actual authorization, rights review and external read-back evidence. Partial local implementation evidence only; original newcomer/human/distribution acceptance is not asserted complete.
- Textual-only prerequisites: none recorded.
- Evidence: README.md; docs/v1/NOTICES.md; docs/v1/VALIDATION.md.

## GH-S38 — Publish and verify a versioned public release

- Wave: 5; status: **PLANNED**; release: 0.1; origin: proposal.
- Dependencies: GH-S37.
- Owned scope: `docs/releases/`, `tools/`, `plan/`.
- Acceptance: After concrete authorization, release assets and source are publicly downloadable without developer credentials and match approved artifact hashes.
- Outcome: After concrete authorization, release assets and source are publicly downloadable without developer credentials and match approved artifact hashes.
- Feature area: distribution-publication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-5, ADR-001
- Risk/evidence needs: Public release and native platform publication require actual authorization, rights review and external read-back evidence.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-S39 — Reproduce from the publicly obtained artifact

- Wave: 5; status: **PLANNED**; release: 0.1; origin: proposal.
- Dependencies: GH-S38.
- Owned scope: `docs/releases/`, `tools/`, `plan/`.
- Acceptance: Fresh external environment obtains public package and completes modification, comparison and recovery; record observer identity/type without inventing human review.
- Outcome: Fresh external environment obtains public package and completes modification, comparison and recovery.
- Feature area: distribution-publication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-5, ADR-001
- Risk/evidence needs: Public release and native platform publication require actual authorization, rights review and external read-back evidence.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-S40 — Publish and read back the native Tanduna plan

- Wave: 5; status: **PLANNED**; release: 0.1; origin: proposal.
- Dependencies: GH-S39.
- Owned scope: `docs/releases/`, `tools/`, `plan/`.
- Acceptance: Authorized supported workflow publishes waves/tasks/dependencies/scope/access instructions; public read-back reconciles returned native IDs and partial failures.
- Outcome: Authorized supported workflow publishes waves/tasks/dependencies/scope/access instructions.
- Feature area: distribution-publication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-5, ADR-001
- Risk/evidence needs: Public release and native platform publication require actual authorization, rights review and external read-back evidence.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-001 — Choose a public feeder and metrics

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-F03.
- Owned scope: `docs/benchmarks/`.
- Acceptance: Record source, license, units, topology and reference outputs; justify voltage/loading bounds and numerical tolerances.
- Outcome: Original complete contract: Choose a public feeder and metrics
- Feature area: benchmark-admission
- Source/decision references: FOUNDATION-2026-09-07#GH-001
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-002 — Specify data and engine decisions

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-001.
- Owned scope: `docs/data/`, `docs/decisions/`.
- Acceptance: Review exact dependency candidates, profiles, rights and supported hardware; distinguish synthetic profiles from observed data.
- Outcome: Original complete contract: Specify data and engine decisions
- Feature area: benchmark-admission
- Source/decision references: FOUNDATION-2026-09-07#GH-002
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-003 — Build the scenario skeleton

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-001, GH-002.
- Owned scope: `src/`, `tests/`, `scenarios/`.
- Acceptance: A local CLI rejects inconsistent units and dangling network references; its synthetic balance test is hand-checkable.
- Outcome: Original complete contract: Build the scenario skeleton
- Feature area: benchmark-admission
- Source/decision references: FOUNDATION-2026-09-07#GH-003
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P06-01 — Resolve exact benchmark asset identity

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-F03.
- Owned scope: `docs/benchmark-admission/`.
- Acceptance: Select one exact IEEE or SimBench feeder revision with corrections and topology identity; similarly named conversions do not satisfy admission.
- Outcome: Select one exact IEEE or SimBench feeder revision with corrections and topology identity.
- Feature area: benchmark-admission
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-6, FOUNDATION-2026-09-07#GH-001, FOUNDATION-2026-09-07#GH-002, FOUNDATION-2026-09-07#GH-003
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P06-02 — Separate asset redistribution rights

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-F03, GH-P06-01.
- Owned scope: `docs/benchmark-admission/`.
- Acceptance: Technical documents, machine-readable model, profiles and reference results each have explicit terms and bundle decisions.
- Outcome: Technical documents, machine-readable model, profiles and reference results each have explicit terms and bundle decisions.
- Feature area: benchmark-admission
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-6, FOUNDATION-2026-09-07#GH-001, FOUNDATION-2026-09-07#GH-002, FOUNDATION-2026-09-07#GH-003
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P06-03 — Map public feeder quantity conventions

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-F03, GH-P06-01.
- Owned scope: `docs/benchmark-admission/`.
- Acceptance: Source units, phase conventions, bases, flow signs and rating definitions map without unexplained loss to the scenario contract.
- Outcome: Source units, phase conventions, bases, flow signs and rating definitions map without unexplained loss to the scenario contract.
- Feature area: benchmark-admission
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-6, FOUNDATION-2026-09-07#GH-001, FOUNDATION-2026-09-07#GH-002, FOUNDATION-2026-09-07#GH-003
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P06-04 — Admit official reference outputs

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-F03, GH-P06-02, GH-P06-03.
- Owned scope: `docs/benchmark-admission/`.
- Acceptance: Reference values identify source solver/settings/version, precision and corrections for the exact selected feeder.
- Outcome: Reference values identify source solver/settings/version, precision and corrections for the exact selected feeder.
- Feature area: benchmark-admission
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-6, FOUNDATION-2026-09-07#GH-001, FOUNDATION-2026-09-07#GH-002, FOUNDATION-2026-09-07#GH-003
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P06-05 — Define public benchmark engineering criteria

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-F03, GH-P06-03.
- Owned scope: `docs/benchmark-admission/`.
- Acceptance: Voltage/loading thresholds and numerical acceptance have source or qualified decision authority; unresolved values block claims.
- Outcome: Voltage/loading thresholds and numerical acceptance have source or qualified decision authority.
- Feature area: benchmark-admission
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-6, FOUNDATION-2026-09-07#GH-001, FOUNDATION-2026-09-07#GH-002, FOUNDATION-2026-09-07#GH-003
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P06-06 — Review the exact engine dependency graph

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-F03, GH-P06-04, GH-P06-05.
- Owned scope: `docs/benchmark-admission/`.
- Acceptance: Pin candidate software and transitive versions, licenses, loading/network behavior, maintenance, hardware evidence and replacement path before installation.
- Outcome: Pin candidate software and transitive versions, licenses, loading/network behavior, maintenance, hardware evidence and replacement path before installation.
- Feature area: benchmark-admission
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-6, FOUNDATION-2026-09-07#GH-001, FOUNDATION-2026-09-07#GH-002, FOUNDATION-2026-09-07#GH-003
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P06-07 — Admit lawful profiles with provenance

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-F03, GH-P06-02, GH-P06-06.
- Owned scope: `docs/benchmark-admission/`.
- Acceptance: Observed versus synthetic series retain calendar, missingness, transformations and rights; fictional profiles do not become observed data.
- Outcome: Observed versus synthetic series retain calendar, missingness, transformations and rights.
- Feature area: benchmark-admission
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-6, FOUNDATION-2026-09-07#GH-001, FOUNDATION-2026-09-07#GH-002, FOUNDATION-2026-09-07#GH-003
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P06-08 — Approve the benchmark admission record

- Wave: 6; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-F03, GH-P06-01, GH-P06-02, GH-P06-03, GH-P06-04, GH-P06-05, GH-P06-06, GH-P06-07.
- Owned scope: `docs/benchmark-admission/`.
- Acceptance: A reviewer can accept or reject the complete source/rights/reference matrix; failed candidates and reasons remain retained.
- Outcome: A reviewer can accept or reject the complete source/rights/reference matrix.
- Feature area: benchmark-admission
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-6, FOUNDATION-2026-09-07#GH-001, FOUNDATION-2026-09-07#GH-002, FOUNDATION-2026-09-07#GH-003
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-004 — Integrate the network baseline

- Wave: 7; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-001, GH-002, GH-003.
- Owned scope: `adapters/network/`.
- Acceptance: Match a public reference power-flow case and retain convergence and residual diagnostics.
- Outcome: Original complete contract: Integrate the network baseline
- Feature area: network-adapters
- Source/decision references: FOUNDATION-2026-09-07#GH-004
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P07-01 — Define adapter capabilities explicitly

- Wave: 7; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P06-08.
- Owned scope: `docs/network-adapters/`.
- Acceptance: Adapter lists supported buses, equipment, phases, loads and outputs; unsupported source features cause rejection.
- Outcome: Adapter lists supported buses, equipment, phases, loads and outputs.
- Feature area: network-adapters
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-7, FOUNDATION-2026-09-07#GH-004
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P07-02 — Preserve engine and backend identity

- Wave: 7; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P06-08, GH-P07-01.
- Owned scope: `docs/network-adapters/`.
- Acceptance: Every run records exact solver/library/backend versions and settings sufficient to distinguish numerically different environments.
- Outcome: Every run records exact solver/library/backend versions and settings sufficient to distinguish numerically different environments.
- Feature area: network-adapters
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-7, FOUNDATION-2026-09-07#GH-004
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P07-03 — Translate engine quantities once

- Wave: 7; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P06-08, GH-P07-01.
- Owned scope: `docs/network-adapters/`.
- Acceptance: Round-trip and sign controls detect duplicated conversion, base mismatch and load/generator sign inversion.
- Outcome: Round-trip and sign controls detect duplicated conversion, base mismatch and load/generator sign inversion.
- Feature area: network-adapters
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-7, FOUNDATION-2026-09-07#GH-004
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P07-04 — Reproduce official feeder snapshots

- Wave: 7; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P06-08, GH-P07-02, GH-P07-03.
- Owned scope: `docs/network-adapters/`.
- Acceptance: Admitted reference bus/branch outputs agree within declared tolerances with retained comparison residuals.
- Outcome: Admitted reference bus/branch outputs agree within declared tolerances with retained comparison residuals.
- Feature area: network-adapters
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-7, FOUNDATION-2026-09-07#GH-004
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P07-05 — Report convergence diagnostics honestly

- Wave: 7; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P06-08, GH-P07-03.
- Owned scope: `docs/network-adapters/`.
- Acceptance: Nonconvergence, iteration exhaustion and warnings map to explicit result states; producer success flag alone is insufficient.
- Outcome: Nonconvergence, iteration exhaustion and warnings map to explicit result states.
- Feature area: network-adapters
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-7, FOUNDATION-2026-09-07#GH-004
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P07-06 — Bound adapter model applicability

- Wave: 7; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P06-08, GH-P07-04, GH-P07-05.
- Owned scope: `docs/network-adapters/`.
- Acceptance: Unsupported equipment/ranges are rejected before comparison and every admitted capability has a conformance control.
- Outcome: Unsupported equipment/ranges are rejected before comparison and every admitted capability has a conformance control.
- Feature area: network-adapters
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-7, FOUNDATION-2026-09-07#GH-004
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P07-07 — Retain native-to-canonical diagnostics

- Wave: 7; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P06-08, GH-P07-02, GH-P07-06.
- Owned scope: `docs/network-adapters/`.
- Acceptance: Raw native results and transformation lineage allow an independent reviewer to locate a discrepant canonical quantity.
- Outcome: Raw native results and transformation lineage allow an independent reviewer to locate a discrepant canonical quantity.
- Feature area: network-adapters
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-7, FOUNDATION-2026-09-07#GH-004
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P07-08 — Measure the baseline engine envelope

- Wave: 7; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P06-08, GH-P07-01, GH-P07-02, GH-P07-03, GH-P07-04, GH-P07-05, GH-P07-06, GH-P07-07.
- Owned scope: `docs/network-adapters/`.
- Acceptance: Actual small-case time, memory and output size establish a local budget and abort/recovery behavior without universal hardware claims.
- Outcome: Actual small-case time, memory and output size establish a local budget and abort/recovery behavior without universal hardware claims.
- Feature area: network-adapters
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-7, FOUNDATION-2026-09-07#GH-004
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-005 — Add transformer loss and thermal state

- Wave: 8; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-001, GH-002, GH-003.
- Owned scope: `adapters/transformer/`.
- Acceptance: Compare the reduced-order model with a documented reference; reject unsupported temperature and load ranges.
- Outcome: Original complete contract: Add transformer loss and thermal state
- Feature area: transformer-models
- Source/decision references: FOUNDATION-2026-09-07#GH-005
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P08-01 — Admit a reduced-order transformer reference

- Wave: 8; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003.
- Owned scope: `docs/transformer-models/`.
- Acceptance: Electrical/thermal equations, asset terms, exact reference values and supported transformer class are fixed before calibration.
- Outcome: Electrical/thermal equations, asset terms, exact reference values and supported transformer class are fixed before calibration.
- Feature area: transformer-models
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-8, FOUNDATION-2026-09-07#GH-005
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P08-02 — Separate winding and no-load losses

- Wave: 8; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P08-01.
- Owned scope: `docs/transformer-models/`.
- Acceptance: Loss components have distinct parameter meaning and aggregate without double counting into electrical boundary balance.
- Outcome: Loss components have distinct parameter meaning and aggregate without double counting into electrical boundary balance.
- Feature area: transformer-models
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-8, FOUNDATION-2026-09-07#GH-005
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P08-03 — Propagate ambient and thermal state

- Wave: 8; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P08-01.
- Owned scope: `docs/transformer-models/`.
- Acceptance: Initial temperature, ambient profile, cooling assumption and timestep determine state with explicit units and boundary conditions.
- Outcome: Initial temperature, ambient profile, cooling assumption and timestep determine state with explicit units and boundary conditions.
- Feature area: transformer-models
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-8, FOUNDATION-2026-09-07#GH-005
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P08-04 — Reject unsupported operating ranges

- Wave: 8; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P08-02, GH-P08-03.
- Owned scope: `docs/transformer-models/`.
- Acceptance: Temperature/load/cooling combinations outside the admitted model return out-of-domain findings before benefit claims.
- Outcome: Temperature/load/cooling combinations outside the admitted model return out-of-domain findings before benefit claims.
- Feature area: transformer-models
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-8, FOUNDATION-2026-09-07#GH-005
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P08-05 — Partition calibration from validation

- Wave: 8; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P08-03.
- Owned scope: `docs/transformer-models/`.
- Acceptance: Parameters fitted to declared development data are tested against independent reference points with access history.
- Outcome: Parameters fitted to declared development data are tested against independent reference points with access history.
- Feature area: transformer-models
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-8, FOUNDATION-2026-09-07#GH-005
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P08-06 — Verify thermal timestep behavior

- Wave: 8; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P08-04, GH-P08-05.
- Owned scope: `docs/transformer-models/`.
- Acceptance: Refinement demonstrates declared temperature/error criteria; coarse-step apparent gains cannot be accepted silently.
- Outcome: Refinement demonstrates declared temperature/error criteria.
- Feature area: transformer-models
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-8, FOUNDATION-2026-09-07#GH-005
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P08-07 — Couple transformer electrical loss conservatively

- Wave: 8; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P08-02, GH-P08-06.
- Owned scope: `docs/transformer-models/`.
- Acceptance: Network-delivered energy and transformer dissipation reconcile at a named boundary without subtracting the same loss twice.
- Outcome: Network-delivered energy and transformer dissipation reconcile at a named boundary without subtracting the same loss twice.
- Feature area: transformer-models
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-8, FOUNDATION-2026-09-07#GH-005
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P08-08 — Review reduced-order credibility limits

- Wave: 8; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P08-01, GH-P08-02, GH-P08-03, GH-P08-04, GH-P08-05, GH-P08-06, GH-P08-07.
- Owned scope: `docs/transformer-models/`.
- Acceptance: Qualified interpretation records validated range, residuals, uncertainty and prohibited extrapolation before use in comparisons.
- Outcome: Qualified interpretation records validated range, residuals, uncertainty and prohibited extrapolation before use in comparisons.
- Feature area: transformer-models
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-8, FOUNDATION-2026-09-07#GH-005
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-006 — Validate time-series coupling

- Wave: 9; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-001, GH-002, GH-003.
- Owned scope: `src/coupling/`.
- Acceptance: Power-to-energy integration uses explicit intervals; no hidden energy appears at component boundaries.
- Outcome: Original complete contract: Validate time-series coupling
- Feature area: time-coupling
- Source/decision references: FOUNDATION-2026-09-07#GH-006
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P09-01 — Define adapter communication clocks

- Wave: 9; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003.
- Owned scope: `docs/time-coupling/`.
- Acceptance: Each adapter exposes communication points, sample meaning and allowed interpolation; unsupported requested steps fail explicitly.
- Outcome: Each adapter exposes communication points, sample meaning and allowed interpolation.
- Feature area: time-coupling
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-9, FOUNDATION-2026-09-07#GH-006
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P09-02 — Integrate interval power without hidden weights

- Wave: 9; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P09-01.
- Owned scope: `docs/time-coupling/`.
- Acceptance: Unequal-duration known answers distinguish actual time from representative-period weights and prevent false stored-energy gain.
- Outcome: Unequal-duration known answers distinguish actual time from representative-period weights and prevent false stored-energy gain.
- Feature area: time-coupling
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-9, FOUNDATION-2026-09-07#GH-006
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P09-03 — Align calendars and missing data

- Wave: 9; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P09-01.
- Owned scope: `docs/time-coupling/`.
- Acceptance: Time zones, leap days, DST and missing intervals have declared transformations with ambiguity rejection.
- Outcome: Time zones, leap days, DST and missing intervals have declared transformations with ambiguity rejection.
- Feature area: time-coupling
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-9, FOUNDATION-2026-09-07#GH-006
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P09-04 — Check boundary exchange ledgers

- Wave: 9; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P09-02, GH-P09-03.
- Owned scope: `docs/time-coupling/`.
- Acceptance: Every cross-component energy transfer appears once with source and sink reconciliation at macro-step boundaries.
- Outcome: Every cross-component energy transfer appears once with source and sink reconciliation at macro-step boundaries.
- Feature area: time-coupling
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-9, FOUNDATION-2026-09-07#GH-006
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P09-05 — Carry component state deterministically

- Wave: 9; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P09-03.
- Owned scope: `docs/time-coupling/`.
- Acceptance: Storage and thermal end state becomes exactly the next initial state; reset/lost-state mutations are detected.
- Outcome: Storage and thermal end state becomes exactly the next initial state.
- Feature area: time-coupling
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-9, FOUNDATION-2026-09-07#GH-006
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P09-06 — Specify feedback and algebraic loops

- Wave: 9; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P09-04, GH-P09-05.
- Owned scope: `docs/time-coupling/`.
- Acceptance: Coupled feedback declares iteration order, stopping tolerance and maximum iterations; lack of convergence is a failure.
- Outcome: Coupled feedback declares iteration order, stopping tolerance and maximum iterations.
- Feature area: time-coupling
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-9, FOUNDATION-2026-09-07#GH-006
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P09-07 — Handle early-return and events

- Wave: 9; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P09-02, GH-P09-06.
- Owned scope: `docs/time-coupling/`.
- Acceptance: An adapter ending early or reporting an event cannot fabricate the rest of an interval as success.
- Outcome: An adapter ending early or reporting an event cannot fabricate the rest of an interval as success.
- Feature area: time-coupling
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-9, FOUNDATION-2026-09-07#GH-006
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P09-08 — Admit an interoperability framework only if needed

- Wave: 9; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-001, GH-002, GH-003, GH-P09-01, GH-P09-02, GH-P09-03, GH-P09-04, GH-P09-05, GH-P09-06, GH-P09-07.
- Owned scope: `docs/time-coupling/`.
- Acceptance: Compare local coupling limitations against FMI/HELICS cost and conformance; adoption waits for measured need and dependency approval.
- Outcome: Compare local coupling limitations against FMI/HELICS cost and conformance.
- Feature area: time-coupling
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-9, FOUNDATION-2026-09-07#GH-006
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-007 — Implement baseline and candidate schedules

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-004, GH-005, GH-006.
- Owned scope: `scenarios/feeder/`.
- Acceptance: Compare fixed operating policy, bounded tap changes and storage scheduling under identical profiles.
- Outcome: Original complete contract: Implement baseline and candidate schedules
- Feature area: operating-policies
- Source/decision references: FOUNDATION-2026-09-07#GH-007
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-008 — Add feasibility-first ranking

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-004, GH-005, GH-006, GH-007.
- Owned scope: `src/evaluation/`.
- Acceptance: Any candidate violating voltage, loading or storage constraints is excluded with an inspectable reason.
- Outcome: Original complete contract: Add feasibility-first ranking
- Feature area: operating-policies
- Source/decision references: FOUNDATION-2026-09-07#GH-008
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-009 — Generate the energy comparison report

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-004, GH-005, GH-006, GH-008.
- Owned scope: `src/reports/`.
- Acceptance: Show losses, served energy, limit violations, cost assumptions and full reproduction inputs for every arm.
- Outcome: Original complete contract: Generate the energy comparison report
- Feature area: operating-policies
- Source/decision references: FOUNDATION-2026-09-07#GH-009
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P10-01 — Freeze fixed-policy operating conditions

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-004, GH-005, GH-006.
- Owned scope: `docs/operating-policies/`.
- Acceptance: Baseline assets, profiles, limits, starting states and allowed variables are versioned before evaluating changes.
- Outcome: Baseline assets, profiles, limits, starting states and allowed variables are versioned before evaluating changes.
- Feature area: operating-policies
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-10, FOUNDATION-2026-09-07#GH-007, FOUNDATION-2026-09-07#GH-008, FOUNDATION-2026-09-07#GH-009
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P10-02 — Model discrete tap actions

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-004, GH-005, GH-006, GH-P10-01.
- Owned scope: `docs/operating-policies/`.
- Acceptance: Tap states, step size and action bounds map to the admitted network model; impossible positions are rejected.
- Outcome: Tap states, step size and action bounds map to the admitted network model.
- Feature area: operating-policies
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-10, FOUNDATION-2026-09-07#GH-007, FOUNDATION-2026-09-07#GH-008, FOUNDATION-2026-09-07#GH-009
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P10-03 — Declare storage scheduling constraints

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-004, GH-005, GH-006, GH-P10-01.
- Owned scope: `docs/operating-policies/`.
- Acceptance: Power, capacity, efficiencies, initial/final energy and allowed schedule timing remain immutable across arms.
- Outcome: Power, capacity, efficiencies, initial/final energy and allowed schedule timing remain immutable across arms.
- Feature area: operating-policies
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-10, FOUNDATION-2026-09-07#GH-007, FOUNDATION-2026-09-07#GH-008, FOUNDATION-2026-09-07#GH-009
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P10-04 — Bound policy search space

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-004, GH-005, GH-006, GH-P10-02, GH-P10-03.
- Owned scope: `docs/operating-policies/`.
- Acceptance: Allowed tap/storage combinations and maximum evaluated candidates are declared; infeasible actions are not silently repaired.
- Outcome: Allowed tap/storage combinations and maximum evaluated candidates are declared.
- Feature area: operating-policies
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-10, FOUNDATION-2026-09-07#GH-007, FOUNDATION-2026-09-07#GH-008, FOUNDATION-2026-09-07#GH-009
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P10-05 — Evaluate joint policy trajectories

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-004, GH-005, GH-006, GH-P10-03.
- Owned scope: `docs/operating-policies/`.
- Acceptance: Network, transformer and storage outputs share identical time support and expose local and system feasibility findings.
- Outcome: Network, transformer and storage outputs share identical time support and expose local and system feasibility findings.
- Feature area: operating-policies
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-10, FOUNDATION-2026-09-07#GH-007, FOUNDATION-2026-09-07#GH-008, FOUNDATION-2026-09-07#GH-009
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P10-06 — Report action burden alongside energy

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-004, GH-005, GH-006, GH-P10-04, GH-P10-05.
- Owned scope: `docs/operating-policies/`.
- Acceptance: Tap operations and storage throughput appear separately from electrical loss and service quantities with explicit assumptions.
- Outcome: Tap operations and storage throughput appear separately from electrical loss and service quantities with explicit assumptions.
- Feature area: operating-policies
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-10, FOUNDATION-2026-09-07#GH-007, FOUNDATION-2026-09-07#GH-008, FOUNDATION-2026-09-07#GH-009
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P10-07 — Explain constrained tradeoffs

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-004, GH-005, GH-006, GH-P10-02, GH-P10-06.
- Owned scope: `docs/operating-policies/`.
- Acceptance: A comparison shows why reduced losses may increase thermal exposure, cycling or unserved demand without a hidden preference score.
- Outcome: A comparison shows why reduced losses may increase thermal exposure, cycling or unserved demand without a hidden preference score.
- Feature area: operating-policies
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-10, FOUNDATION-2026-09-07#GH-007, FOUNDATION-2026-09-07#GH-008, FOUNDATION-2026-09-07#GH-009
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P10-08 — Replay the integrated original experiment

- Wave: 10; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-004, GH-005, GH-006, GH-P10-01, GH-P10-02, GH-P10-03, GH-P10-04, GH-P10-05, GH-P10-06, GH-P10-07.
- Owned scope: `docs/operating-policies/`.
- Acceptance: Public feeder, transformer and coupling evidence support fixed/tap/storage policies and reproduction required by GH-007 through GH-009.
- Outcome: Public feeder, transformer and coupling evidence support fixed/tap/storage policies and reproduction required by GH-007 through GH-009.
- Feature area: operating-policies
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-10, FOUNDATION-2026-09-07#GH-007, FOUNDATION-2026-09-07#GH-008, FOUNDATION-2026-09-07#GH-009
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P11-01 — Catalog uncertainty by origin

- Wave: 11; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `docs/uncertainty/`.
- Acceptance: Measurement, parameters, model form, scenario variability and numerical error have separate records and cannot be pooled without method.
- Outcome: Measurement, parameters, model form, scenario variability and numerical error have separate records and cannot be pooled without method.
- Feature area: uncertainty
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-11, FOUNDATION-2026-09-07#GH-012, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P11-02 — Assign defensible parameter ranges

- Wave: 11; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P11-01.
- Owned scope: `docs/uncertainty/`.
- Acceptance: Each range/distribution has source or explicit assumption and rejects impossible physical support.
- Outcome: Each range/distribution has source or explicit assumption and rejects impossible physical support.
- Feature area: uncertainty
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-11, FOUNDATION-2026-09-07#GH-012, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P11-03 — Preserve correlated input variation

- Wave: 11; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P11-01.
- Owned scope: `docs/uncertainty/`.
- Acceptance: Joint scenarios retain justified correlations rather than treating dependent loads/weather as independent by convenience.
- Outcome: Joint scenarios retain justified correlations rather than treating dependent loads/weather as independent by convenience.
- Feature area: uncertainty
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-11, FOUNDATION-2026-09-07#GH-012, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P11-04 — Propagate uncertainty through feasibility

- Wave: 11; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P11-02, GH-P11-03.
- Owned scope: `docs/uncertainty/`.
- Acceptance: Constraint probability or interval exposure is calculated from admitted samples and reports sample coverage and failure denominator.
- Outcome: Constraint probability or interval exposure is calculated from admitted samples and reports sample coverage and failure denominator.
- Feature area: uncertainty
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-11, FOUNDATION-2026-09-07#GH-012, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P11-05 — Compare paired uncertain objectives

- Wave: 11; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P11-03.
- Owned scope: `docs/uncertainty/`.
- Acceptance: Baseline/candidate use matched samples and seeds; uncertainty intervals accompany all compared quantities.
- Outcome: Baseline/candidate use matched samples and seeds.
- Feature area: uncertainty
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-11, FOUNDATION-2026-09-07#GH-012, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P11-06 — Detect ranking reversals

- Wave: 11; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P11-04, GH-P11-05.
- Owned scope: `docs/uncertainty/`.
- Acceptance: A controlled plausible-parameter perturbation reverses nominal ordering and yields INDETERMINATE under the declared rule.
- Outcome: A controlled plausible-parameter perturbation reverses nominal ordering and yields INDETERMINATE under the declared rule.
- Feature area: uncertainty
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-11, FOUNDATION-2026-09-07#GH-012, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P11-07 — Expose model discrepancy separately

- Wave: 11; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P11-02, GH-P11-06.
- Owned scope: `docs/uncertainty/`.
- Acceptance: Reference disagreement is retained as model uncertainty instead of absorbed into a fabricated measurement precision.
- Outcome: Reference disagreement is retained as model uncertainty instead of absorbed into a fabricated measurement precision.
- Feature area: uncertainty
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-11, FOUNDATION-2026-09-07#GH-012, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P11-08 — Choose evidence that resolves ambiguity

- Wave: 11; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P11-01, GH-P11-02, GH-P11-03, GH-P11-04, GH-P11-05, GH-P11-06, GH-P11-07.
- Owned scope: `docs/uncertainty/`.
- Acceptance: A sensitivity report identifies which assumption could change a decision and proposes bounded additional evidence without promising a winner.
- Outcome: A sensitivity report identifies which assumption could change a decision and proposes bounded additional evidence without promising a winner.
- Feature area: uncertainty
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-11, FOUNDATION-2026-09-07#GH-012, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-010 — Create load and weather holdouts

- Wave: 12; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `benchmarks/`.
- Acceptance: Separate selection and confirmation periods; report performance over heat and peak-demand conditions.
- Outcome: Original complete contract: Create load and weather holdouts
- Feature area: holdout-transfer
- Source/decision references: FOUNDATION-2026-09-07#GH-010
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P12-01 — Freeze selection and confirmation partitions

- Wave: 12; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `docs/holdout-transfer/`.
- Acceptance: Periods and source identities are assigned before policy tuning and every subsequent access is logged.
- Outcome: Periods and source identities are assigned before policy tuning and every subsequent access is logged.
- Feature area: holdout-transfer
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-12, FOUNDATION-2026-09-07#GH-010
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P12-02 — Construct heat and demand stress periods

- Wave: 12; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P12-01.
- Owned scope: `docs/holdout-transfer/`.
- Acceptance: Heat and peak-load cases preserve chronological joint weather/load structure and state why they are supported stress conditions.
- Outcome: Heat and peak-load cases preserve chronological joint weather/load structure and state why they are supported stress conditions.
- Feature area: holdout-transfer
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-12, FOUNDATION-2026-09-07#GH-010
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P12-03 — Test seasonal profile transfer

- Wave: 12; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P12-01.
- Owned scope: `docs/holdout-transfer/`.
- Acceptance: A fixed selected policy replays across withheld seasons; coverage limitations and deteriorations are retained.
- Outcome: A fixed selected policy replays across withheld seasons.
- Feature area: holdout-transfer
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-12, FOUNDATION-2026-09-07#GH-010
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P12-04 — Prevent boundary-state leakage

- Wave: 12; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P12-02, GH-P12-03.
- Owned scope: `docs/holdout-transfer/`.
- Acceptance: Storage/thermal initial conditions for holdouts follow a declared warmup/state protocol rather than favorable initialization.
- Outcome: Storage/thermal initial conditions for holdouts follow a declared warmup/state protocol rather than favorable initialization.
- Feature area: holdout-transfer
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-12, FOUNDATION-2026-09-07#GH-010
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P12-05 — Retire contaminated holdouts

- Wave: 12; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P12-03.
- Owned scope: `docs/holdout-transfer/`.
- Acceptance: Access that informs tuning reclassifies evidence as development and requires a newly reserved confirmation set.
- Outcome: Access that informs tuning reclassifies evidence as development and requires a newly reserved confirmation set.
- Feature area: holdout-transfer
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-12, FOUNDATION-2026-09-07#GH-010
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P12-06 — Preserve worst-supported outcomes

- Wave: 12; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P12-04, GH-P12-05.
- Owned scope: `docs/holdout-transfer/`.
- Acceptance: Reports include worst voltage/loading/service conditions and failed cases rather than only ensemble means.
- Outcome: Reports include worst voltage/loading/service conditions and failed cases rather than only ensemble means.
- Feature area: holdout-transfer
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-12, FOUNDATION-2026-09-07#GH-010
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P12-07 — Measure profile-domain mismatch

- Wave: 12; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P12-02, GH-P12-06.
- Owned scope: `docs/holdout-transfer/`.
- Acceptance: Distribution and range checks flag out-of-domain weather/load; unsupported transfer is not treated as confirmation.
- Outcome: Distribution and range checks flag out-of-domain weather/load.
- Feature area: holdout-transfer
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-12, FOUNDATION-2026-09-07#GH-010
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P12-08 — Publish transfer conclusions with failures

- Wave: 12; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P12-01, GH-P12-02, GH-P12-03, GH-P12-04, GH-P12-05, GH-P12-06, GH-P12-07.
- Owned scope: `docs/holdout-transfer/`.
- Acceptance: A fixed report binds selected policy, partition history and all holdout outcomes including negative or indeterminate conclusions.
- Outcome: A fixed report binds selected policy, partition history and all holdout outcomes including negative or indeterminate conclusions.
- Feature area: holdout-transfer
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-12, FOUNDATION-2026-09-07#GH-010
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-011 — Test outages and degraded components

- Wave: 13; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `scenarios/resilience/`.
- Acceptance: Evaluate explicitly enumerated contingencies and unserved energy without live infrastructure access.
- Outcome: Original complete contract: Test outages and degraded components
- Feature area: resilience
- Source/decision references: FOUNDATION-2026-09-07#GH-011
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P13-01 — Enumerate contingency scope

- Wave: 13; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `docs/resilience/`.
- Acceptance: Outage sets identify affected assets, timing, duration and exclusions without live topology or control access.
- Outcome: Outage sets identify affected assets, timing, duration and exclusions without live topology or control access.
- Feature area: resilience
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-13, FOUNDATION-2026-09-07#GH-011
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P13-02 — Represent degraded asset states

- Wave: 13; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P13-01.
- Owned scope: `docs/resilience/`.
- Acceptance: Capacity/efficiency changes have bounded sourced assumptions and remain separate from complete component failure.
- Outcome: Capacity/efficiency changes have bounded sourced assumptions and remain separate from complete component failure.
- Feature area: resilience
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-13, FOUNDATION-2026-09-07#GH-011
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P13-03 — Model disconnected service accounting

- Wave: 13; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P13-01.
- Owned scope: `docs/resilience/`.
- Acceptance: Islands and unsupplied buses yield explicit served/unserved energy rather than dropped nodes or nominal full service.
- Outcome: Islands and unsupplied buses yield explicit served/unserved energy rather than dropped nodes or nominal full service.
- Feature area: resilience
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-13, FOUNDATION-2026-09-07#GH-011
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P13-04 — Declare restoration assumptions

- Wave: 13; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P13-02, GH-P13-03.
- Owned scope: `docs/resilience/`.
- Acceptance: Repair order and delay are scenario hypotheses with provenance, not operational restoration instructions.
- Outcome: Repair order and delay are scenario hypotheses with provenance, not operational restoration instructions.
- Feature area: resilience
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-13, FOUNDATION-2026-09-07#GH-011
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P13-05 — Reconcile event and interval clocks

- Wave: 13; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P13-03.
- Owned scope: `docs/resilience/`.
- Acceptance: Outage boundaries split or aggregate intervals through a tested rule that preserves energy and event duration.
- Outcome: Outage boundaries split or aggregate intervals through a tested rule that preserves energy and event duration.
- Feature area: resilience
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-13, FOUNDATION-2026-09-07#GH-011
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P13-06 — Compare resilience under equal exposure

- Wave: 13; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P13-04, GH-P13-05.
- Owned scope: `docs/resilience/`.
- Acceptance: Arms share contingency realizations and repair assumptions with uncertainty and failed-run denominators.
- Outcome: Arms share contingency realizations and repair assumptions with uncertainty and failed-run denominators.
- Feature area: resilience
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-13, FOUNDATION-2026-09-07#GH-011
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P13-07 — Separate reliability metrics and units

- Wave: 13; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P13-02, GH-P13-06.
- Owned scope: `docs/resilience/`.
- Acceptance: Unserved energy and frequency/duration metrics retain exact population/event definitions without unsupported utility equivalence.
- Outcome: Unserved energy and frequency/duration metrics retain exact population/event definitions without unsupported utility equivalence.
- Feature area: resilience
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-13, FOUNDATION-2026-09-07#GH-011
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P13-08 — Publish bounded resilience evidence

- Wave: 13; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P13-01, GH-P13-02, GH-P13-03, GH-P13-04, GH-P13-05, GH-P13-06, GH-P13-07.
- Owned scope: `docs/resilience/`.
- Acceptance: Scenario enumeration, unsupported contingencies and no-live-operation limits accompany reproducible outage results.
- Outcome: Scenario enumeration, unsupported contingencies and no-live-operation limits accompany reproducible outage results.
- Feature area: resilience
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-13, FOUNDATION-2026-09-07#GH-011
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-012 — Cross-check numerical assumptions

- Wave: 14; status: **PLANNED**; release: later 0.x; origin: source_requirement.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `tests/validation/`.
- Acceptance: Detect nonconvergence, unit mistakes and misleading aggregate efficiency; compare a second reference where available.
- Outcome: Original complete contract: Cross-check numerical assumptions
- Feature area: numerical-verification
- Source/decision references: FOUNDATION-2026-09-07#GH-012
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P14-01 — Admit a second independent reference

- Wave: 14; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `docs/numerical-verification/`.
- Acceptance: Reference independence, rights, model alignment and supported comparison variables are explicit before cross-checking.
- Outcome: Reference independence, rights, model alignment and supported comparison variables are explicit before cross-checking.
- Feature area: numerical-verification
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-14, FOUNDATION-2026-09-07#GH-012
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P14-02 — Localize cross-solver discrepancies

- Wave: 14; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P14-01.
- Owned scope: `docs/numerical-verification/`.
- Acceptance: Bus/branch/component residuals identify whether mapping, model approximation or numerical method causes disagreement.
- Outcome: Bus/branch/component residuals identify whether mapping, model approximation or numerical method causes disagreement.
- Feature area: numerical-verification
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-14, FOUNDATION-2026-09-07#GH-012
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P14-03 — Test tolerance sensitivity

- Wave: 14; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P14-01.
- Owned scope: `docs/numerical-verification/`.
- Acceptance: Tighter/looser numerical settings reveal conclusions that depend on convergence tolerances without changing engineering limits.
- Outcome: Tighter/looser numerical settings reveal conclusions that depend on convergence tolerances without changing engineering limits.
- Feature area: numerical-verification
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-14, FOUNDATION-2026-09-07#GH-012
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P14-04 — Exercise nonconvergence controls

- Wave: 14; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P14-02, GH-P14-03.
- Owned scope: `docs/numerical-verification/`.
- Acceptance: Deliberate ill-conditioned or unsupported cases preserve FAILED_SOLVER and diagnostics rather than empty successful results.
- Outcome: Deliberate ill-conditioned or unsupported cases preserve FAILED_SOLVER and diagnostics rather than empty successful results.
- Feature area: numerical-verification
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-14, FOUNDATION-2026-09-07#GH-012
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P14-05 — Detect misleading aggregate efficiency

- Wave: 14; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P14-03.
- Owned scope: `docs/numerical-verification/`.
- Acceptance: A control with hidden unserved demand or cancelled local residuals fails despite an attractive aggregate ratio.
- Outcome: A control with hidden unserved demand or cancelled local residuals fails despite an attractive aggregate ratio.
- Feature area: numerical-verification
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-14, FOUNDATION-2026-09-07#GH-012
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P14-06 — Check unit and base invariance

- Wave: 14; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P14-04, GH-P14-05.
- Owned scope: `docs/numerical-verification/`.
- Acceptance: Equivalent unit/base representations produce physically identical quantities; a one-sided conversion mutation fails.
- Outcome: Equivalent unit/base representations produce physically identical quantities.
- Feature area: numerical-verification
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-14, FOUNDATION-2026-09-07#GH-012
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P14-07 — Separate rounding from physical margins

- Wave: 14; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P14-02, GH-P14-06.
- Owned scope: `docs/numerical-verification/`.
- Acceptance: Boundary tests distinguish serialization/roundoff allowance from a relaxed voltage/loading requirement.
- Outcome: Boundary tests distinguish serialization/roundoff allowance from a relaxed voltage/loading requirement.
- Feature area: numerical-verification
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-14, FOUNDATION-2026-09-07#GH-012
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P14-08 — Issue a numerical credibility record

- Wave: 14; status: **PLANNED**; release: later 0.x; origin: proposal.
- Dependencies: GH-007, GH-008, GH-009, GH-P14-01, GH-P14-02, GH-P14-03, GH-P14-04, GH-P14-05, GH-P14-06, GH-P14-07.
- Owned scope: `docs/numerical-verification/`.
- Acceptance: Validated configurations, discrepancy limits, unresolved cases and allowed interpretations bind the exact adapter revision.
- Outcome: Validated configurations, discrepancy limits, unresolved cases and allowed interpretations bind the exact adapter revision.
- Feature area: numerical-verification
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-14, FOUNDATION-2026-09-07#GH-012
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-013 — Add generation-storage planning

- Wave: 15; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-010, GH-011, GH-012.
- Owned scope: `adapters/planning/`.
- Acceptance: Compare scenarios with explicit capacity, degradation, weather and resource assumptions and feasible energy balances.
- Outcome: Original complete contract: Add generation-storage planning
- Feature area: capacity-planning
- Source/decision references: FOUNDATION-2026-09-07#GH-013
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P15-01 — Define capacity decision variables

- Wave: 15; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012.
- Owned scope: `docs/capacity-planning/`.
- Acceptance: Generation and storage power/energy capacities have separate bounds, units and investment assumptions.
- Outcome: Generation and storage power/energy capacities have separate bounds, units and investment assumptions.
- Feature area: capacity-planning
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-15, FOUNDATION-2026-09-07#GH-013
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P15-02 — Preserve chronological dispatch constraints

- Wave: 15; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P15-01.
- Owned scope: `docs/capacity-planning/`.
- Acceptance: Capacity candidates replay chronological operating balances and cannot borrow energy across disconnected representative periods.
- Outcome: Capacity candidates replay chronological operating balances and cannot borrow energy across disconnected representative periods.
- Feature area: capacity-planning
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-15, FOUNDATION-2026-09-07#GH-013
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P15-03 — Admit technology cost and resource assumptions

- Wave: 15; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P15-01.
- Owned scope: `docs/capacity-planning/`.
- Acceptance: Exact vintage, currency/geography, weather resource and rights support each planning parameter.
- Outcome: Exact vintage, currency/geography, weather resource and rights support each planning parameter.
- Feature area: capacity-planning
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-15, FOUNDATION-2026-09-07#GH-013
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P15-04 — Model cycle and calendar degradation

- Wave: 15; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P15-02, GH-P15-03.
- Owned scope: `docs/capacity-planning/`.
- Acceptance: Separate degradation mechanisms alter capacity/efficiency through documented ranges and cannot create stored energy.
- Outcome: Separate degradation mechanisms alter capacity/efficiency through documented ranges and cannot create stored energy.
- Feature area: capacity-planning
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-15, FOUNDATION-2026-09-07#GH-013
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P15-05 — Represent replacements and service life

- Wave: 15; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P15-03.
- Owned scope: `docs/capacity-planning/`.
- Acceptance: Replacement timing/capacity and downtime appear in feasible dispatch and lifecycle inventories with explicit assumptions.
- Outcome: Replacement timing/capacity and downtime appear in feasible dispatch and lifecycle inventories with explicit assumptions.
- Feature area: capacity-planning
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-15, FOUNDATION-2026-09-07#GH-013
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P15-06 — Couple planning to distribution validation

- Wave: 15; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P15-04, GH-P15-05.
- Owned scope: `docs/capacity-planning/`.
- Acceptance: A portfolio's dispatch is checked against network constraints instead of treating a planning solver's balance as feeder feasibility.
- Outcome: A portfolio's dispatch is checked against network constraints instead of treating a planning solver's balance as feeder feasibility.
- Feature area: capacity-planning
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-15, FOUNDATION-2026-09-07#GH-013
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P15-07 — Compare resource-limited portfolios

- Wave: 15; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P15-02, GH-P15-06.
- Owned scope: `docs/capacity-planning/`.
- Acceptance: Land/material/water or other selected constraints have units and provenance; absent resource evidence remains unmeasured.
- Outcome: Land/material/water or other selected constraints have units and provenance.
- Feature area: capacity-planning
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-15, FOUNDATION-2026-09-07#GH-013
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P15-08 — Validate portfolio tradeoff claims

- Wave: 15; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P15-01, GH-P15-02, GH-P15-03, GH-P15-04, GH-P15-05, GH-P15-06, GH-P15-07.
- Owned scope: `docs/capacity-planning/`.
- Acceptance: Reproducible portfolios disclose feasible energy, service, cost/degradation assumptions, sensitivity and unsupported extrapolations.
- Outcome: Reproducible portfolios disclose feasible energy, service, cost/degradation assumptions, sensitivity and unsupported extrapolations.
- Feature area: capacity-planning
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-15, FOUNDATION-2026-09-07#GH-013
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-014 — Specify and validate higher-fidelity transformer models

- Wave: 16; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-010, GH-011, GH-012.
- Owned scope: `adapters/component/`.
- Acceptance: Require reusable material data, mesh/timestep convergence and a reduced-order comparison before claiming component gains.
- Outcome: Original complete contract: Specify and validate higher-fidelity transformer models
- Feature area: component-physics
- Source/decision references: FOUNDATION-2026-09-07#GH-014
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P16-01 — State the higher-fidelity use question

- Wave: 16; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012.
- Owned scope: `docs/component-physics/`.
- Acceptance: Required outputs and decision sensitivity justify a component model instead of assuming more detail is more credible.
- Outcome: Required outputs and decision sensitivity justify a component model instead of assuming more detail is more credible.
- Feature area: component-physics
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-16, FOUNDATION-2026-09-07#GH-014
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P16-02 — Admit material and geometry inputs

- Wave: 16; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P16-01.
- Owned scope: `docs/component-physics/`.
- Acceptance: Material tables, geometry and boundary data have exact rights, ranges, uncertainty and transformation lineage.
- Outcome: Material tables, geometry and boundary data have exact rights, ranges, uncertainty and transformation lineage.
- Feature area: component-physics
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-16, FOUNDATION-2026-09-07#GH-014
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P16-03 — Select component engine under review

- Wave: 16; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P16-01.
- Owned scope: `docs/component-physics/`.
- Acceptance: Exact dependency graph, solver/license/hardware cost and removal path are approved only after the model question and input evidence exist.
- Outcome: Exact dependency graph, solver/license/hardware cost and removal path are approved only after the model question and input evidence exist.
- Feature area: component-physics
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-16, FOUNDATION-2026-09-07#GH-014
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P16-04 — Verify mesh convergence

- Wave: 16; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P16-02, GH-P16-03.
- Owned scope: `docs/component-physics/`.
- Acceptance: Refined meshes demonstrate declared output/residual convergence with retained mesh and solver identity.
- Outcome: Refined meshes demonstrate declared output/residual convergence with retained mesh and solver identity.
- Feature area: component-physics
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-16, FOUNDATION-2026-09-07#GH-014
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P16-05 — Verify transient timestep convergence

- Wave: 16; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P16-03.
- Owned scope: `docs/component-physics/`.
- Acceptance: Temporal refinement bounds the claimed thermal/electrical quantity without hiding early termination or instability.
- Outcome: Temporal refinement bounds the claimed thermal/electrical quantity without hiding early termination or instability.
- Feature area: component-physics
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-16, FOUNDATION-2026-09-07#GH-014
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P16-06 — Cross-check against reduced order

- Wave: 16; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P16-04, GH-P16-05.
- Owned scope: `docs/component-physics/`.
- Acceptance: Aligned boundaries/inputs expose differences from the admitted reduced-order model and explain discrepancy limits.
- Outcome: Aligned boundaries/inputs expose differences from the admitted reduced-order model and explain discrepancy limits.
- Feature area: component-physics
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-16, FOUNDATION-2026-09-07#GH-014
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P16-07 — Partition spatial coupling quantities

- Wave: 16; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P16-02, GH-P16-06.
- Owned scope: `docs/component-physics/`.
- Acceptance: Electrical dissipation, thermal flux and material state reconcile at interfaces with separate units and no double counting.
- Outcome: Electrical dissipation, thermal flux and material state reconcile at interfaces with separate units and no double counting.
- Feature area: component-physics
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-16, FOUNDATION-2026-09-07#GH-014
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P16-08 — Obtain component-domain interpretation

- Wave: 16; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P16-01, GH-P16-02, GH-P16-03, GH-P16-04, GH-P16-05, GH-P16-06, GH-P16-07.
- Owned scope: `docs/component-physics/`.
- Acceptance: Qualified review states supported material/load/cooling range and rejects unsupported component-gain or certification claims.
- Outcome: Qualified review states supported material/load/cooling range and rejects unsupported component-gain or certification claims.
- Feature area: component-physics
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-16, FOUNDATION-2026-09-07#GH-014
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-015 — Add lifecycle and novel-concept comparisons

- Wave: 17; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-010, GH-011, GH-012.
- Owned scope: `src/lifecycle/`.
- Acceptance: Expose construction/operation/end-of-life assumptions; speculative designs remain hypotheses and cannot violate conservation.
- Outcome: Original complete contract: Add lifecycle and novel-concept comparisons
- Feature area: lifecycle
- Source/decision references: FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P17-01 — Fix functional unit and service boundary

- Wave: 17; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012.
- Owned scope: `docs/lifecycle/`.
- Acceptance: Compared designs share delivered service and declared lifetime; capacity-only comparisons cannot imply equivalent lifecycle performance.
- Outcome: Compared designs share delivered service and declared lifetime.
- Feature area: lifecycle
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-17, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P17-02 — Trace construction inventories

- Wave: 17; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P17-01.
- Owned scope: `docs/lifecycle/`.
- Acceptance: Material/manufacturing quantities, geography, vintage and source rights remain itemized with uncertainty.
- Outcome: Material/manufacturing quantities, geography, vintage and source rights remain itemized with uncertainty.
- Feature area: lifecycle
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-17, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P17-03 — Connect operation to feasible studies

- Wave: 17; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P17-01.
- Owned scope: `docs/lifecycle/`.
- Acceptance: Operating energy and replacement impacts derive from feasible trajectories rather than unserved or impossible energy promises.
- Outcome: Operating energy and replacement impacts derive from feasible trajectories rather than unserved or impossible energy promises.
- Feature area: lifecycle
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-17, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P17-04 — Represent maintenance and replacement stages

- Wave: 17; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P17-02, GH-P17-03.
- Owned scope: `docs/lifecycle/`.
- Acceptance: Stage-specific inventories and schedules reconcile with component lifetime and planning assumptions.
- Outcome: Stage-specific inventories and schedules reconcile with component lifetime and planning assumptions.
- Feature area: lifecycle
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-17, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P17-05 — Separate end-of-life pathways

- Wave: 17; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P17-03.
- Owned scope: `docs/lifecycle/`.
- Acceptance: Recycling, disposal and recovery credits have explicit allocation rules and cannot be claimed twice.
- Outcome: Recycling, disposal and recovery credits have explicit allocation rules and cannot be claimed twice.
- Feature area: lifecycle
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-17, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P17-06 — Expose allocation and system expansion choices

- Wave: 17; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P17-04, GH-P17-05.
- Owned scope: `docs/lifecycle/`.
- Acceptance: Alternative allocation assumptions remain versioned and their effect on comparison is inspectable.
- Outcome: Alternative allocation assumptions remain versioned and their effect on comparison is inspectable.
- Feature area: lifecycle
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-17, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P17-07 — Preserve multi-impact objective vectors

- Wave: 17; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P17-02, GH-P17-06.
- Owned scope: `docs/lifecycle/`.
- Acceptance: Emissions, water, material and cost quantities retain units and factors rather than hidden scalar weights.
- Outcome: Emissions, water, material and cost quantities retain units and factors rather than hidden scalar weights.
- Feature area: lifecycle
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-17, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P17-08 — Compare lifecycle sensitivity honestly

- Wave: 17; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-010, GH-011, GH-012, GH-P17-01, GH-P17-02, GH-P17-03, GH-P17-04, GH-P17-05, GH-P17-06, GH-P17-07.
- Owned scope: `docs/lifecycle/`.
- Acceptance: Boundary, lifetime and geography variations that reverse ordering produce bounded/indeterminate conclusions with full inventory provenance.
- Outcome: Boundary, lifetime and geography variations that reverse ordering produce bounded/indeterminate conclusions with full inventory provenance.
- Feature area: lifecycle
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-17, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P18-01 — Admit a concept hypothesis record

- Wave: 18; status: **PLANNED**; release: exploratory; origin: exploratory.
- Dependencies: GH-P17-01, GH-012.
- Owned scope: `docs/novel-concepts/`.
- Acceptance: A speculative mechanism states claimed service, physical boundary, assumptions and measurable falsifier without implying validated technology.
- Outcome: A speculative mechanism states claimed service, physical boundary, assumptions and measurable falsifier without implying validated technology.
- Feature area: novel-concepts
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-18, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P18-02 — Challenge conservation before simulation

- Wave: 18; status: **PLANNED**; release: exploratory; origin: exploratory.
- Dependencies: GH-P17-01, GH-012, GH-P18-01.
- Owned scope: `docs/novel-concepts/`.
- Acceptance: Independent energy/charge/material ledgers reject concepts requiring unexplained sources or sinks.
- Outcome: Independent energy/charge/material ledgers reject concepts requiring unexplained sources or sinks.
- Feature area: novel-concepts
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-18, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P18-03 — Bound speculative parameters

- Wave: 18; status: **PLANNED**; release: exploratory; origin: exploratory.
- Dependencies: GH-P17-01, GH-012, GH-P18-01.
- Owned scope: `docs/novel-concepts/`.
- Acceptance: Unsupported efficiencies/material properties are labeled assumptions with plausible ranges and explicit evidence gaps.
- Outcome: Unsupported efficiencies/material properties are labeled assumptions with plausible ranges and explicit evidence gaps.
- Feature area: novel-concepts
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-18, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P18-04 — Reproduce a known-technology control

- Wave: 18; status: **PLANNED**; release: exploratory; origin: exploratory.
- Dependencies: GH-P17-01, GH-012, GH-P18-02, GH-P18-03.
- Owned scope: `docs/novel-concepts/`.
- Acceptance: The same evaluator reproduces an admitted conventional comparator before assessing a novel concept.
- Outcome: The same evaluator reproduces an admitted conventional comparator before assessing a novel concept.
- Feature area: novel-concepts
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-18, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P18-05 — Separate mechanism from implementation promises

- Wave: 18; status: **PLANNED**; release: exploratory; origin: exploratory.
- Dependencies: GH-P17-01, GH-012, GH-P18-03.
- Owned scope: `docs/novel-concepts/`.
- Acceptance: A concept's theoretical possibility, simulated behavior and manufacturability are recorded as distinct unresolved questions.
- Outcome: A concept's theoretical possibility, simulated behavior and manufacturability are recorded as distinct unresolved questions.
- Feature area: novel-concepts
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-18, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P18-06 — Design discriminating virtual experiments

- Wave: 18; status: **PLANNED**; release: exploratory; origin: exploratory.
- Dependencies: GH-P17-01, GH-012, GH-P18-04, GH-P18-05.
- Owned scope: `docs/novel-concepts/`.
- Acceptance: A bounded scenario identifies outcomes that distinguish the hypothesis from known technology under equal conditions.
- Outcome: A bounded scenario identifies outcomes that distinguish the hypothesis from known technology under equal conditions.
- Feature area: novel-concepts
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-18, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P18-07 — Retain refutations and negative findings

- Wave: 18; status: **PLANNED**; release: exploratory; origin: exploratory.
- Dependencies: GH-P17-01, GH-012, GH-P18-02, GH-P18-06.
- Owned scope: `docs/novel-concepts/`.
- Acceptance: Failed predictions and invalid concepts remain searchable evidence and cannot be removed from reported success rates.
- Outcome: Failed predictions and invalid concepts remain searchable evidence and cannot be removed from reported success rates.
- Feature area: novel-concepts
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-18, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P18-08 — Gate any claimed conceptual advantage

- Wave: 18; status: **PLANNED**; release: exploratory; origin: exploratory.
- Dependencies: GH-P17-01, GH-012, GH-P18-01, GH-P18-02, GH-P18-03, GH-P18-04, GH-P18-05, GH-P18-06, GH-P18-07.
- Owned scope: `docs/novel-concepts/`.
- Acceptance: Advantage language requires conservation, model validity, feasible service and independent review; speculative results remain hypotheses.
- Outcome: Advantage language requires conservation, model validity, feasible service and independent review.
- Feature area: novel-concepts
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-18, FOUNDATION-2026-09-07#GH-015
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P19-01 — Define network-class admission criteria

- Wave: 19; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-012.
- Owned scope: `docs/network-classes/`.
- Acceptance: Phase/topology/voltage support is declared per adapter with class-specific references and exclusions.
- Outcome: Phase/topology/voltage support is declared per adapter with class-specific references and exclusions.
- Feature area: network-classes
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-19, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P19-02 — Map unbalanced phase quantities

- Wave: 19; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-012, GH-P19-01.
- Owned scope: `docs/network-classes/`.
- Acceptance: Phase connectivity, neutral/sequence meaning and phase-specific ratings retain explicit bases and signs.
- Outcome: Phase connectivity, neutral/sequence meaning and phase-specific ratings retain explicit bases and signs.
- Feature area: network-classes
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-19, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P19-03 — Validate meshed-network behavior

- Wave: 19; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-012, GH-P19-01.
- Owned scope: `docs/network-classes/`.
- Acceptance: A meshed adapter reproduces an admitted loop-flow reference instead of passing a radial kernel through unsupported topology.
- Outcome: A meshed adapter reproduces an admitted loop-flow reference instead of passing a radial kernel through unsupported topology.
- Feature area: network-classes
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-19, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P19-04 — Admit additional voltage levels

- Wave: 19; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-012, GH-P19-02, GH-P19-03.
- Owned scope: `docs/network-classes/`.
- Acceptance: Transformer/base transitions and equipment ratings are checked across voltage domains without broad grid compatibility claims.
- Outcome: Transformer/base transitions and equipment ratings are checked across voltage domains without broad grid compatibility claims.
- Feature area: network-classes
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-19, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P19-05 — Specify AC and DC contract differences

- Wave: 19; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-012, GH-P19-03.
- Owned scope: `docs/network-classes/`.
- Acceptance: Reactive power, voltage and conversion semantics are class-specific and absent quantities are not fabricated.
- Outcome: Reactive power, voltage and conversion semantics are class-specific and absent quantities are not fabricated.
- Feature area: network-classes
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-19, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P19-06 — Model conversion interfaces explicitly

- Wave: 19; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-012, GH-P19-04, GH-P19-05.
- Owned scope: `docs/network-classes/`.
- Acceptance: AC/DC or multi-domain converters conserve separate power/energy quantities with documented efficiency and control assumptions.
- Outcome: AC/DC or multi-domain converters conserve separate power/energy quantities with documented efficiency and control assumptions.
- Feature area: network-classes
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-19, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P19-07 — Exercise class-specific conformance suites

- Wave: 19; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-012, GH-P19-02, GH-P19-06.
- Owned scope: `docs/network-classes/`.
- Acceptance: Each supported class has known answers, unsupported-feature rejection and applicability evidence bound to engine identity.
- Outcome: Each supported class has known answers, unsupported-feature rejection and applicability evidence bound to engine identity.
- Feature area: network-classes
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-19, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P19-08 — Publish a support and transfer matrix

- Wave: 19; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-012, GH-P19-01, GH-P19-02, GH-P19-03, GH-P19-04, GH-P19-05, GH-P19-06, GH-P19-07.
- Owned scope: `docs/network-classes/`.
- Acceptance: A reader can see tested combinations, unsupported classes and which source assumptions fail across network families.
- Outcome: A reader can see tested combinations, unsupported classes and which source assumptions fail across network families.
- Feature area: network-classes
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-19, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-016 — Build evidence-grounded design proposals

- Wave: 20; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-013, GH-014, GH-015.
- Owned scope: `src/agents/`.
- Acceptance: Every proposed change lists source assumptions, bounds and a measurable engineering hypothesis.
- Outcome: Original complete contract: Build evidence-grounded design proposals
- Feature area: agent-proposals
- Source/decision references: FOUNDATION-2026-09-07#GH-016
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P20-01 — Define bounded proposal schemas

- Wave: 20; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015.
- Owned scope: `docs/agent-proposals/`.
- Acceptance: Proposals list allowed variables, source assumptions, bounds, expected mechanism and a falsifier without executable arbitrary code.
- Outcome: Proposals list allowed variables, source assumptions, bounds, expected mechanism and a falsifier without executable arbitrary code.
- Feature area: agent-proposals
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-20, FOUNDATION-2026-09-07#GH-016
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P20-02 — Link proposal claims to evidence

- Wave: 20; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-01.
- Owned scope: `docs/agent-proposals/`.
- Acceptance: Every claimed rationale resolves to a source/model/result revision and distinguishes observation from inference.
- Outcome: Every claimed rationale resolves to a source/model/result revision and distinguishes observation from inference.
- Feature area: agent-proposals
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-20, FOUNDATION-2026-09-07#GH-016
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P20-03 — Prevent proposal authority over constraints

- Wave: 20; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-01.
- Owned scope: `docs/agent-proposals/`.
- Acceptance: Representative edits to evaluator, accepted limits or confirmation inputs are denied and recorded.
- Outcome: Representative edits to evaluator, accepted limits or confirmation inputs are denied and recorded.
- Feature area: agent-proposals
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-20, FOUNDATION-2026-09-07#GH-016
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P20-04 — Validate proposal parameters before runs

- Wave: 20; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-02, GH-P20-03.
- Owned scope: `docs/agent-proposals/`.
- Acceptance: Units, ranges, topology and model applicability are checked before spending solver resources.
- Outcome: Units, ranges, topology and model applicability are checked before spending solver resources.
- Feature area: agent-proposals
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-20, FOUNDATION-2026-09-07#GH-016
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P20-05 — Retain alternatives and rejected proposals

- Wave: 20; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-03.
- Owned scope: `docs/agent-proposals/`.
- Acceptance: Rejected, superseded and duplicate hypotheses preserve reasons and identity rather than disappearing from coverage reports.
- Outcome: Rejected, superseded and duplicate hypotheses preserve reasons and identity rather than disappearing from coverage reports.
- Feature area: agent-proposals
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-20, FOUNDATION-2026-09-07#GH-016
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P20-06 — Record inference and source budgets

- Wave: 20; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-04, GH-P20-05.
- Owned scope: `docs/agent-proposals/`.
- Acceptance: Proposal generation records model/runtime identity, token/cost limits and source accesses under explicit spending authorization.
- Outcome: Proposal generation records model/runtime identity, token/cost limits and source accesses under explicit spending authorization.
- Feature area: agent-proposals
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-20, FOUNDATION-2026-09-07#GH-016
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P20-07 — Test explanations against raw findings

- Wave: 20; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-02, GH-P20-06.
- Owned scope: `docs/agent-proposals/`.
- Acceptance: Agent summaries cannot contradict retained failure states, objective units or uncertainty without an explicit detected discrepancy.
- Outcome: Agent summaries cannot contradict retained failure states, objective units or uncertainty without an explicit detected discrepancy.
- Feature area: agent-proposals
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-20, FOUNDATION-2026-09-07#GH-016
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P20-08 — Review evidence-grounded search admission

- Wave: 20; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-01, GH-P20-02, GH-P20-03, GH-P20-04, GH-P20-05, GH-P20-06, GH-P20-07.
- Owned scope: `docs/agent-proposals/`.
- Acceptance: A bounded agent workflow is admitted only after schema, provenance, isolation and fixed-baseline evidence pass.
- Outcome: A bounded agent workflow is admitted only after schema, provenance, isolation and fixed-baseline evidence pass.
- Feature area: agent-proposals
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-20, FOUNDATION-2026-09-07#GH-016
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-017 — Run equal-budget optimization baselines

- Wave: 21; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-013, GH-014, GH-015.
- Owned scope: `src/search/`.
- Acceptance: Compare agent-guided search with grid/random baselines; enforce the same solver and resource budget.
- Outcome: Original complete contract: Run equal-budget optimization baselines
- Feature area: search-evaluation
- Source/decision references: FOUNDATION-2026-09-07#GH-017
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P21-01 — Establish deterministic fixed baselines

- Wave: 21; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-08.
- Owned scope: `docs/search-evaluation/`.
- Acceptance: A fixed non-agent candidate set and evaluation order provide a reproducible minimum comparator.
- Outcome: A fixed non-agent candidate set and evaluation order provide a reproducible minimum comparator.
- Feature area: search-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-21, FOUNDATION-2026-09-07#GH-017
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P21-02 — Establish seeded random or grid baselines

- Wave: 21; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-08, GH-P21-01.
- Owned scope: `docs/search-evaluation/`.
- Acceptance: Search space and seed/grid resolution are predeclared and independently replayable within the same constraints.
- Outcome: Search space and seed/grid resolution are predeclared and independently replayable within the same constraints.
- Feature area: search-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-21, FOUNDATION-2026-09-07#GH-017
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P21-03 — Meter solver calls and failures

- Wave: 21; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-08, GH-P21-01.
- Owned scope: `docs/search-evaluation/`.
- Acceptance: Rejected/failed attempts count under the declared search budget and cannot provide free additional trials.
- Outcome: Rejected/failed attempts count under the declared search budget and cannot provide free additional trials.
- Feature area: search-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-21, FOUNDATION-2026-09-07#GH-017
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P21-04 — Meter elapsed compute and inference cost

- Wave: 21; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-08, GH-P21-02, GH-P21-03.
- Owned scope: `docs/search-evaluation/`.
- Acceptance: All arms share comparable solver/time/resource ceilings and record agent inference cost separately.
- Outcome: All arms share comparable solver/time/resource ceilings and record agent inference cost separately.
- Feature area: search-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-21, FOUNDATION-2026-09-07#GH-017
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P21-05 — Enforce immutable search constraints

- Wave: 21; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-08, GH-P21-03.
- Owned scope: `docs/search-evaluation/`.
- Acceptance: Search cannot widen parameter bounds, relax feasibility or change objectives when a preferred candidate fails.
- Outcome: Search cannot widen parameter bounds, relax feasibility or change objectives when a preferred candidate fails.
- Feature area: search-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-21, FOUNDATION-2026-09-07#GH-017
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P21-06 — Compare coverage as well as quality

- Wave: 21; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-08, GH-P21-04, GH-P21-05.
- Owned scope: `docs/search-evaluation/`.
- Acceptance: Reports show explored regions, feasible proportion, objective vector and uncertainty at equal budget checkpoints.
- Outcome: Reports show explored regions, feasible proportion, objective vector and uncertainty at equal budget checkpoints.
- Feature area: search-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-21, FOUNDATION-2026-09-07#GH-017
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P21-07 — Stop and resume bounded campaigns

- Wave: 21; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-08, GH-P21-02, GH-P21-06.
- Owned scope: `docs/search-evaluation/`.
- Acceptance: Budget exhaustion halts new launches; reconciliation preserves spent budget and prevents duplicate trials after restart.
- Outcome: Budget exhaustion halts new launches.
- Feature area: search-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-21, FOUNDATION-2026-09-07#GH-017
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P21-08 — Assess whether agent search adds evidence

- Wave: 21; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P20-08, GH-P21-01, GH-P21-02, GH-P21-03, GH-P21-04, GH-P21-05, GH-P21-06, GH-P21-07.
- Owned scope: `docs/search-evaluation/`.
- Acceptance: Matched-budget results report gains, losses or indeterminacy against both fixed and random/grid methods without cherry-picking.
- Outcome: Matched-budget results report gains, losses or indeterminacy against both fixed and random/grid methods without cherry-picking.
- Feature area: search-evaluation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-21, FOUNDATION-2026-09-07#GH-017
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-018 — Confirm robust Pareto candidates

- Wave: 22; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-013, GH-014, GH-015.
- Owned scope: `src/evaluation/`.
- Acceptance: Retest selected designs on untouched scenarios and report tradeoffs, failures and uncertainty.
- Outcome: Original complete contract: Confirm robust Pareto candidates
- Feature area: confirmation
- Source/decision references: FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P22-01 — Freeze selected candidates before confirmation

- Wave: 22; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P21-08.
- Owned scope: `docs/confirmation/`.
- Acceptance: Candidate identities, selection rule and development evidence are locked before reserved evaluation.
- Outcome: Candidate identities, selection rule and development evidence are locked before reserved evaluation.
- Feature area: confirmation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-22, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P22-02 — Protect untouched confirmation inputs

- Wave: 22; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P21-08, GH-P22-01.
- Owned scope: `docs/confirmation/`.
- Acceptance: Approved enforced isolation denies search access and records representative access-denial evidence.
- Outcome: Approved enforced isolation denies search access and records representative access-denial evidence.
- Feature area: confirmation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-22, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P22-03 — Retest full objective and constraint vectors

- Wave: 22; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P21-08, GH-P22-01.
- Owned scope: `docs/confirmation/`.
- Acceptance: Confirmation recomputes every required quantity and feasibility condition from raw outputs, including unfavorable dimensions.
- Outcome: Confirmation recomputes every required quantity and feasibility condition from raw outputs, including unfavorable dimensions.
- Feature area: confirmation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-22, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P22-04 — Retain failures in confirmation denominators

- Wave: 22; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P21-08, GH-P22-02, GH-P22-03.
- Owned scope: `docs/confirmation/`.
- Acceptance: Nonconvergence, infeasibility and missing results remain visible under the predeclared analysis rule.
- Outcome: Nonconvergence, infeasibility and missing results remain visible under the predeclared analysis rule.
- Feature area: confirmation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-22, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P22-05 — Quantify robust versus nominal dominance

- Wave: 22; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P21-08, GH-P22-03.
- Owned scope: `docs/confirmation/`.
- Acceptance: Uncertainty-aware Pareto comparison distinguishes stable dominance, tradeoffs and INDETERMINATE relationships.
- Outcome: Uncertainty-aware Pareto comparison distinguishes stable dominance, tradeoffs and INDETERMINATE relationships.
- Feature area: confirmation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-22, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P22-06 — Detect selection-driven optimism

- Wave: 22; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P21-08, GH-P22-04, GH-P22-05.
- Owned scope: `docs/confirmation/`.
- Acceptance: Development-to-confirmation differences expose overfitting and do not trigger retuning on the reserved evidence.
- Outcome: Development-to-confirmation differences expose overfitting and do not trigger retuning on the reserved evidence.
- Feature area: confirmation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-22, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P22-07 — Require new evidence after revisions

- Wave: 22; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P21-08, GH-P22-02, GH-P22-06.
- Owned scope: `docs/confirmation/`.
- Acceptance: Changing candidate/model/evaluator after confirmation invalidates affected claims and reserves a new confirmation plan.
- Outcome: Changing candidate/model/evaluator after confirmation invalidates affected claims and reserves a new confirmation plan.
- Feature area: confirmation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-22, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P22-08 — Publish a reproducible confirmation dossier

- Wave: 22; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-013, GH-014, GH-015, GH-P21-08, GH-P22-01, GH-P22-02, GH-P22-03, GH-P22-04, GH-P22-05, GH-P22-06, GH-P22-07.
- Owned scope: `docs/confirmation/`.
- Acceptance: Frozen candidates, access history, failures, uncertainty and independent review support bounded tradeoff conclusions.
- Outcome: Frozen candidates, access history, failures, uncertainty and independent review support bounded tradeoff conclusions.
- Feature area: confirmation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-22, FOUNDATION-2026-09-07#GH-018
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-019 — Build a local network comparison view

- Wave: 23; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-016, GH-017, GH-018.
- Owned scope: `apps/workbench/`.
- Acceptance: Show units, constraints and failures with keyboard access; a network drawing is labeled as a simulated model.
- Outcome: Original complete contract: Build a local network comparison view
- Feature area: workbench
- Source/decision references: FOUNDATION-2026-09-07#GH-019
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P23-01 — Navigate an evidence-bound network view

- Wave: 23; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018.
- Owned scope: `docs/workbench/`.
- Acceptance: Selecting a simulated bus/branch reveals units, model applicability and raw result references rather than suggesting a live asset.
- Outcome: Selecting a simulated bus/branch reveals units, model applicability and raw result references rather than suggesting a live asset.
- Feature area: workbench
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-23, FOUNDATION-2026-09-07#GH-019
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P23-02 — Compare synchronized trajectories

- Wave: 23; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P23-01.
- Owned scope: `docs/workbench/`.
- Acceptance: Baseline and candidate views share time controls and expose differences in profiles, limits or eligibility.
- Outcome: Baseline and candidate views share time controls and expose differences in profiles, limits or eligibility.
- Feature area: workbench
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-23, FOUNDATION-2026-09-07#GH-019
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P23-03 — Inspect localized failures

- Wave: 23; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P23-01.
- Owned scope: `docs/workbench/`.
- Acceptance: A user reaches the affected interval/entity, threshold and raw evidence directly from a failure summary.
- Outcome: A user reaches the affected interval/entity, threshold and raw evidence directly from a failure summary.
- Feature area: workbench
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-23, FOUNDATION-2026-09-07#GH-019
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P23-04 — Expose quantities without visual dependence

- Wave: 23; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P23-02, GH-P23-03.
- Owned scope: `docs/workbench/`.
- Acceptance: Tables and text provide the same energy, storage, loading and uncertainty information as diagrams and charts.
- Outcome: Tables and text provide the same energy, storage, loading and uncertainty information as diagrams and charts.
- Feature area: workbench
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-23, FOUNDATION-2026-09-07#GH-019
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P23-05 — Support keyboard and assistive navigation

- Wave: 23; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P23-03.
- Owned scope: `docs/workbench/`.
- Acceptance: Focus order, labels, landmarks and announcement behavior are observed with the declared interface and assistive workflow.
- Outcome: Focus order, labels, landmarks and announcement behavior are observed with the declared interface and assistive workflow.
- Feature area: workbench
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-23, FOUNDATION-2026-09-07#GH-019
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P23-06 — Handle zoom narrow screens and motion

- Wave: 23; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P23-04, GH-P23-05.
- Owned scope: `docs/workbench/`.
- Acceptance: At documented zoom/narrow widths controls and evidence remain reachable; reduced motion and non-color cues work where relevant.
- Outcome: At documented zoom/narrow widths controls and evidence remain reachable.
- Feature area: workbench
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-23, FOUNDATION-2026-09-07#GH-019
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P23-07 — Recover from invalid imports and stale results

- Wave: 23; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P23-02, GH-P23-06.
- Owned scope: `docs/workbench/`.
- Acceptance: Import errors explain the field and recovery path; stale schema/model evidence cannot appear current.
- Outcome: Import errors explain the field and recovery path.
- Feature area: workbench
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-23, FOUNDATION-2026-09-07#GH-019
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P23-08 — Validate researcher inspection tasks

- Wave: 23; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P23-01, GH-P23-02, GH-P23-03, GH-P23-04, GH-P23-05, GH-P23-06, GH-P23-07.
- Owned scope: `docs/workbench/`.
- Acceptance: Actual participants complete declared evidence-finding/comparison tasks; observations and unresolved accessibility limits are recorded honestly.
- Outcome: Actual participants complete declared evidence-finding/comparison tasks.
- Feature area: workbench
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-23, FOUNDATION-2026-09-07#GH-019
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-020 — Add isolated batch execution

- Wave: 24; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-016, GH-017, GH-018.
- Owned scope: `src/workers/`.
- Acceptance: Enforce resource limits, cancellation and restart recovery without duplicate run publication.
- Outcome: Original complete contract: Add isolated batch execution
- Feature area: execution-isolation
- Source/decision references: FOUNDATION-2026-09-07#GH-020
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P24-01 — Measure a justified batch bottleneck

- Wave: 24; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018.
- Owned scope: `docs/execution-isolation/`.
- Acceptance: Retained local workloads show a specific throughput/isolation limit and compare expected benefit with operational cost.
- Outcome: Retained local workloads show a specific throughput/isolation limit and compare expected benefit with operational cost.
- Feature area: execution-isolation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-24, FOUNDATION-2026-09-07#GH-020
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P24-02 — Enforce filesystem and credential isolation

- Wave: 24; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P24-01.
- Owned scope: `docs/execution-isolation/`.
- Acceptance: Approved OS/container/VM policy denies unrelated files, secrets and evaluator/holdout access under representative escape attempts.
- Outcome: Approved OS/container/VM policy denies unrelated files, secrets and evaluator/holdout access under representative escape attempts.
- Feature area: execution-isolation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-24, FOUNDATION-2026-09-07#GH-020
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P24-03 — Enforce network devices and process limits

- Wave: 24; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P24-01.
- Owned scope: `docs/execution-isolation/`.
- Acceptance: Default-deny network and bounded CPU/memory/disk/process/device policies pass actual denial and exhaustion controls.
- Outcome: Default-deny network and bounded CPU/memory/disk/process/device policies pass actual denial and exhaustion controls.
- Feature area: execution-isolation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-24, FOUNDATION-2026-09-07#GH-020
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P24-04 — Maintain unique logical runs and attempts

- Wave: 24; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P24-02, GH-P24-03.
- Owned scope: `docs/execution-isolation/`.
- Acceptance: Concurrent workers cannot publish duplicate terminal results; retries retain logical identity and separate attempts.
- Outcome: Concurrent workers cannot publish duplicate terminal results.
- Feature area: execution-isolation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-24, FOUNDATION-2026-09-07#GH-020
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P24-05 — Cancel complete worker process trees

- Wave: 24; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P24-03.
- Owned scope: `docs/execution-isolation/`.
- Acceptance: Cooperative then enforced cancellation stops descendants within policy and retains partial resource/evidence records.
- Outcome: Cooperative then enforced cancellation stops descendants within policy and retains partial resource/evidence records.
- Feature area: execution-isolation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-24, FOUNDATION-2026-09-07#GH-020
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P24-06 — Reconcile restart and orphaned workers

- Wave: 24; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P24-04, GH-P24-05.
- Owned scope: `docs/execution-isolation/`.
- Acceptance: Owner/liveness checks distinguish lost work from completed results and avoid automatic unsafe reattachment or duplicated budget.
- Outcome: Owner/liveness checks distinguish lost work from completed results and avoid automatic unsafe reattachment or duplicated budget.
- Feature area: execution-isolation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-24, FOUNDATION-2026-09-07#GH-020
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P24-07 — Schedule within approved resource envelopes

- Wave: 24; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P24-02, GH-P24-06.
- Owned scope: `docs/execution-isolation/`.
- Acceptance: Queue admission and concurrency respect measured host quotas and stop launching after cancellation or exhaustion.
- Outcome: Queue admission and concurrency respect measured host quotas and stop launching after cancellation or exhaustion.
- Feature area: execution-isolation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-24, FOUNDATION-2026-09-07#GH-020
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P24-08 — Gate remote execution on measured need

- Wave: 24; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P24-01, GH-P24-02, GH-P24-03, GH-P24-04, GH-P24-05, GH-P24-06, GH-P24-07.
- Owned scope: `docs/execution-isolation/`.
- Acceptance: Artifact integrity, remote cancellation, cost reconciliation and explicit resource/account approval precede distributed deployment.
- Outcome: Artifact integrity, remote cancellation, cost reconciliation and explicit resource/account approval precede distributed deployment.
- Feature area: execution-isolation
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-24, FOUNDATION-2026-09-07#GH-020
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-021 — Export portable energy studies

- Wave: 25; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-016, GH-017, GH-018.
- Owned scope: `src/export/`.
- Acceptance: A fresh machine reconstructs inputs and results from a bundle without private provider access.
- Outcome: Original complete contract: Export portable energy studies
- Feature area: study-portability
- Source/decision references: FOUNDATION-2026-09-07#GH-021
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P25-01 — Define a portable study inventory

- Wave: 25; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018.
- Owned scope: `docs/study-portability/`.
- Acceptance: Bundle schema enumerates scenarios, models, source rights, manifests, raw results, failures and evaluator identity.
- Outcome: Bundle schema enumerates scenarios, models, source rights, manifests, raw results, failures and evaluator identity.
- Feature area: study-portability
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-25, FOUNDATION-2026-09-07#GH-021
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P25-02 — Include only lawfully redistributable artifacts

- Wave: 25; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P25-01.
- Owned scope: `docs/study-portability/`.
- Acceptance: Asset-level rights filter bundles; externally referenced inputs clearly state authorized retrieval and portability limitations.
- Outcome: Asset-level rights filter bundles.
- Feature area: study-portability
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-25, FOUNDATION-2026-09-07#GH-021
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P25-03 — Verify content and provenance integrity

- Wave: 25; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P25-01.
- Owned scope: `docs/study-portability/`.
- Acceptance: Digests and transformation lineage detect tampered inputs/results and identify exactly which claim is affected.
- Outcome: Digests and transformation lineage detect tampered inputs/results and identify exactly which claim is affected.
- Feature area: study-portability
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-25, FOUNDATION-2026-09-07#GH-021
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P25-04 — Reconstruct the pinned engine environment

- Wave: 25; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P25-02, GH-P25-03.
- Owned scope: `docs/study-portability/`.
- Acceptance: Reproduction recipe identifies runtime/solver dependencies and supported platform evidence without relying on private caches.
- Outcome: Reproduction recipe identifies runtime/solver dependencies and supported platform evidence without relying on private caches.
- Feature area: study-portability
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-25, FOUNDATION-2026-09-07#GH-021
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P25-05 — Support offline evidence inspection

- Wave: 25; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P25-03.
- Owned scope: `docs/study-portability/`.
- Acceptance: Raw quantities, limitations and reports can be inspected without contacting a provider or running candidate code.
- Outcome: Raw quantities, limitations and reports can be inspected without contacting a provider or running candidate code.
- Feature area: study-portability
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-25, FOUNDATION-2026-09-07#GH-021
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P25-06 — Evolve schemas without rewriting history

- Wave: 25; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P25-04, GH-P25-05.
- Owned scope: `docs/study-portability/`.
- Acceptance: Explicit migrations preserve original bundle identity and reject unsupported formats with an inspectable reason.
- Outcome: Explicit migrations preserve original bundle identity and reject unsupported formats with an inspectable reason.
- Feature area: study-portability
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-25, FOUNDATION-2026-09-07#GH-021
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P25-07 — Redact unsafe metadata before export

- Wave: 25; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P25-02, GH-P25-06.
- Owned scope: `docs/study-portability/`.
- Acceptance: Private paths, credentials, identifying participant data and restricted topology are excluded without altering scientific quantities.
- Outcome: Private paths, credentials, identifying participant data and restricted topology are excluded without altering scientific quantities.
- Feature area: study-portability
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-25, FOUNDATION-2026-09-07#GH-021
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P25-08 — Reproduce a complex study independently

- Wave: 25; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-016, GH-017, GH-018, GH-P25-01, GH-P25-02, GH-P25-03, GH-P25-04, GH-P25-05, GH-P25-06, GH-P25-07.
- Owned scope: `docs/study-portability/`.
- Acceptance: A fresh environment reconstructs supported results and failures from the lawful bundle, recording deviations and observer type.
- Outcome: A fresh environment reconstructs supported results and failures from the lawful bundle, recording deviations and observer type.
- Feature area: study-portability
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-25, FOUNDATION-2026-09-07#GH-021
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-022 — Replicate a second network

- Wave: 26; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-019, GH-020, GH-021.
- Owned scope: `benchmarks/replication/`.
- Acceptance: A new topology exercises the same pipeline; document which assumptions fail to transfer.
- Outcome: Original complete contract: Replicate a second network
- Feature area: replication
- Source/decision references: FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P26-01 — Select a genuinely independent topology

- Wave: 26; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021.
- Owned scope: `docs/replication/`.
- Acceptance: Second network has distinct structure and lawful exact reference data rather than a renamed first fixture.
- Outcome: Second network has distinct structure and lawful exact reference data rather than a renamed first fixture.
- Feature area: replication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-26, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P26-02 — Map transfer assumptions before running

- Wave: 26; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P26-01.
- Owned scope: `docs/replication/`.
- Acceptance: Equipment, phase, loading and profile differences identify which first-network claims are eligible for transfer.
- Outcome: Equipment, phase, loading and profile differences identify which first-network claims are eligible for transfer.
- Feature area: replication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-26, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P26-03 — Reuse the canonical pipeline unchanged

- Wave: 26; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P26-01.
- Owned scope: `docs/replication/`.
- Acceptance: Second-network execution uses admitted adapters/contracts; special-case code requires an explicit reviewed model change.
- Outcome: Second-network execution uses admitted adapters/contracts.
- Feature area: replication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-26, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P26-04 — Reproduce the second reference numerically

- Wave: 26; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P26-02, GH-P26-03.
- Owned scope: `docs/replication/`.
- Acceptance: Independent bus/branch/reference comparisons pass declared tolerances and retain nonconvergence or discrepancy evidence.
- Outcome: Independent bus/branch/reference comparisons pass declared tolerances and retain nonconvergence or discrepancy evidence.
- Feature area: replication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-26, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P26-05 — Replay policies under comparable conditions

- Wave: 26; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P26-03.
- Owned scope: `docs/replication/`.
- Acceptance: Allowed adjustments are declared before runs and cannot conceal different exogenous conditions or feasibility limits.
- Outcome: Allowed adjustments are declared before runs and cannot conceal different exogenous conditions or feasibility limits.
- Feature area: replication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-26, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P26-06 — Expose assumptions that fail to transfer

- Wave: 26; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P26-04, GH-P26-05.
- Owned scope: `docs/replication/`.
- Acceptance: Unsupported ranges/classes and reversed tradeoffs remain first-class findings rather than excluded bad cases.
- Outcome: Unsupported ranges/classes and reversed tradeoffs remain first-class findings rather than excluded bad cases.
- Feature area: replication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-26, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P26-07 — Compare reproduction costs and coverage

- Wave: 26; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P26-02, GH-P26-06.
- Owned scope: `docs/replication/`.
- Acceptance: Runtime, adapter effort, missing features and evidence coverage quantify generality without universal portability claims.
- Outcome: Runtime, adapter effort, missing features and evidence coverage quantify generality without universal portability claims.
- Feature area: replication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-26, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P26-08 — Obtain independent replication findings

- Wave: 26; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P26-01, GH-P26-02, GH-P26-03, GH-P26-04, GH-P26-05, GH-P26-06, GH-P26-07.
- Owned scope: `docs/replication/`.
- Acceptance: An identified independent observer/reviewer records actual reconstruction steps, differences and bounded conclusions.
- Outcome: An identified independent observer/reviewer records actual reconstruction steps, differences and bounded conclusions.
- Feature area: replication
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-26, FOUNDATION-2026-09-07#GH-022
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-023 — Conduct an engineering review

- Wave: 27; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-019, GH-020, GH-021.
- Owned scope: `docs/review/`.
- Acceptance: A qualified reviewer checks feasibility, model scope and the claimed operating/design improvements.
- Outcome: Original complete contract: Conduct an engineering review
- Feature area: research-governance
- Source/decision references: FOUNDATION-2026-09-07#GH-023
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-024 — Prepare the research preview

- Wave: 27; status: **PLANNED**; release: long-term; origin: source_requirement.
- Dependencies: GH-019, GH-020, GH-021.
- Owned scope: `docs/releases/`.
- Acceptance: Include reproducible cases, known limits and maintainer-approved release notes without real-grid deployment claims.
- Outcome: Original complete contract: Prepare the research preview
- Feature area: research-governance
- Source/decision references: FOUNDATION-2026-09-07#GH-024
- Risk/evidence needs: Original full acceptance and dependencies remain binding; synthetic partial evidence is insufficient.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P27-01 — Define the qualified review scope

- Wave: 27; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021.
- Owned scope: `docs/research-governance/`.
- Acceptance: Reviewer qualifications, model domain, questions and conflicts are recorded before assessing engineering interpretations.
- Outcome: Reviewer qualifications, model domain, questions and conflicts are recorded before assessing engineering interpretations.
- Feature area: research-governance
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-27, FOUNDATION-2026-09-07#GH-023, FOUNDATION-2026-09-07#GH-024
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P27-02 — Review feasibility and applicability claims

- Wave: 27; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P27-01.
- Owned scope: `docs/research-governance/`.
- Acceptance: Qualified review checks model equations, supported ranges, constraints and improvement language against retained evidence.
- Outcome: Qualified review checks model equations, supported ranges, constraints and improvement language against retained evidence.
- Feature area: research-governance
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-27, FOUNDATION-2026-09-07#GH-023, FOUNDATION-2026-09-07#GH-024
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P27-03 — Resolve material review findings

- Wave: 27; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P27-01.
- Owned scope: `docs/research-governance/`.
- Acceptance: Each finding links a fix, reproduction evidence or explicitly accepted limitation; open material defects block the associated claim.
- Outcome: Each finding links a fix, reproduction evidence or explicitly accepted limitation.
- Feature area: research-governance
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-27, FOUNDATION-2026-09-07#GH-023, FOUNDATION-2026-09-07#GH-024
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P27-04 — Maintain source dependency and model notices

- Wave: 27; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P27-02, GH-P27-03.
- Owned scope: `docs/research-governance/`.
- Acceptance: Release inventory keeps exact asset terms, attribution and compatible distribution obligations with the candidate.
- Outcome: Release inventory keeps exact asset terms, attribution and compatible distribution obligations with the candidate.
- Feature area: research-governance
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-27, FOUNDATION-2026-09-07#GH-023, FOUNDATION-2026-09-07#GH-024
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P27-05 — Publish bounded research release notes

- Wave: 27; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P27-03.
- Owned scope: `docs/research-governance/`.
- Acceptance: Maintainer-approved notes separate implemented software, numerical evidence, human/domain review and prohibited live-operation use.
- Outcome: Maintainer-approved notes separate implemented software, numerical evidence, human/domain review and prohibited live-operation use.
- Feature area: research-governance
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-27, FOUNDATION-2026-09-07#GH-023, FOUNDATION-2026-09-07#GH-024
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P27-06 — Operate correction and evidence invalidation

- Wave: 27; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P27-04, GH-P27-05.
- Owned scope: `docs/research-governance/`.
- Acceptance: A discovered defect maps affected versions/studies and publishes correction or withdrawal without erasing original evidence.
- Outcome: A discovered defect maps affected versions/studies and publishes correction or withdrawal without erasing original evidence.
- Feature area: research-governance
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-27, FOUNDATION-2026-09-07#GH-023, FOUNDATION-2026-09-07#GH-024
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P27-07 — Set sustainable maintenance and compatibility scope

- Wave: 27; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P27-02, GH-P27-06.
- Owned scope: `docs/research-governance/`.
- Acceptance: Supported formats/platforms, upgrade/retest obligations and maintainer capacity are explicit before promising service continuity.
- Outcome: Supported formats/platforms, upgrade/retest obligations and maintainer capacity are explicit before promising service continuity.
- Feature area: research-governance
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-27, FOUNDATION-2026-09-07#GH-023, FOUNDATION-2026-09-07#GH-024
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-P27-08 — Decide the next research horizon from evidence

- Wave: 27; status: **PLANNED**; release: long-term; origin: proposal.
- Dependencies: GH-019, GH-020, GH-021, GH-P27-01, GH-P27-02, GH-P27-03, GH-P27-04, GH-P27-05, GH-P27-06, GH-P27-07.
- Owned scope: `docs/research-governance/`.
- Acceptance: Review chooses CONTINUE, REDIRECT, DESCOPE, HOLD or TERMINATE using reference validity, uncertainty, rights and measured cost rather than backlog counts.
- Outcome: Review chooses CONTINUE, REDIRECT, DESCOPE, HOLD or TERMINATE using reference validity, uncertainty, rights and measured cost rather than backlog counts.
- Feature area: research-governance
- Source/decision references: OWNER-LAUNCH-2026-09-07#wave-27, FOUNDATION-2026-09-07#GH-023, FOUNDATION-2026-09-07#GH-024
- Risk/evidence needs: Exact source rights, admitted model/reference evidence and qualified interpretation may block this domain; no engine or external dependency is preapproved.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-V01 — Admit the v1.0 synthetic AC model

- Wave: 28; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-F03.
- Owned scope: `src/grid_horizons/`, `tests/`.
- Acceptance: Document original feeder/profile rights, exact nonlinear equations, limits, tolerances and finite release contract.
- Outcome: Document original feeder/profile rights, exact nonlinear equations, limits, tolerances and finite release contract.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: docs/v1/CONTRACT.md; docs/v1/MODEL.md.

## GH-V02 — Check nonlinear chronological trajectories

- Wave: 28; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V01.
- Owned scope: `src/grid_horizons/`, `tests/`.
- Acceptance: Calculate AC voltage/current/loss trajectories and storage energy with a separate equation evaluator and analytic mutation controls.
- Outcome: Calculate AC voltage/current/loss trajectories and storage energy with a separate equation evaluator and analytic mutation controls.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: src/grid_horizons/ac.py; src/grid_horizons/ac_check.py; tests/test_ac_lab.py.

## GH-V03 — Inspect operating tradeoffs offline

- Wave: 28; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V02.
- Owned scope: `src/grid_horizons/`, `tests/`.
- Acceptance: Use keyboard-accessible offline reports to inspect every policy state, interval metrics, limits, failures and exports.
- Outcome: Use keyboard-accessible offline reports to inspect every policy state, interval metrics, limits, failures and exports.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: docs/v1/evidence/rc4-browser.json; src/grid_horizons/lab_report.py.

## GH-V04 — Retain complete campaigns and attempts

- Wave: 28; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V02.
- Owned scope: `src/grid_horizons/`, `tests/`.
- Acceptance: Run finite sequential campaigns, retain rejected/failed cases, export/reopen studies and recover interruption into a fresh attempt.
- Outcome: Run finite sequential campaigns, retain rejected/failed cases, export/reopen studies and recover interruption into a fresh attempt.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: docs/v1/evidence/rc4-clean.json; tools/check_release.py.

## GH-V05 — Reproduce the portable application

- Wave: 28; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V03, GH-V04.
- Owned scope: `src/grid_horizons/`, `tests/`.
- Acceptance: Exercise packaged AC and legacy workflows in clean supported Linux Python without private credentials or third-party dependencies.
- Outcome: Exercise packaged AC and legacy workflows in clean supported Linux Python without private credentials or third-party dependencies.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: docs/v1/evidence/rc4-clean.json; README.md.

## GH-V06 — Publishable solver sensitivity benchmark

- Wave: 29; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V05.
- Owned scope: `research/`.
- Acceptance: Retain independent full-feeder solver comparison, preregistered sensitivity, all results and rerunnable benchmark manuscript.
- Outcome: Retain independent full-feeder solver comparison, preregistered sensitivity, all results and rerunnable benchmark manuscript.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: research/benchmark/report.md; research/benchmark/findings.json; research/reproduction/report.md.

## GH-V07 — Publishable policy tradeoff study

- Wave: 29; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V05.
- Owned scope: `research/`.
- Acceptance: Compare matched chronological policies using equal exploration budgets, feasible selection and held-out confirmation with complete loss accounting.
- Outcome: Compare matched chronological policies using equal exploration budgets, feasible selection and held-out confirmation with complete loss accounting.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: research/policies/report.md; research/policies/findings.json; research/reproduction/report.md.

## GH-V08 — Publishable operating robustness study

- Wave: 29; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V05.
- Owned scope: `research/`.
- Acceptance: Challenge fixed promising policies across held-out profiles, forecast mismatch and admitted component assumptions with all-state coverage.
- Outcome: Challenge fixed promising policies across held-out profiles, forecast mismatch and admitted component assumptions with all-state coverage.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: research/robustness/report.md; research/robustness/findings.json; research/reproduction/report.md.

## GH-V09 — Skeptical process-separated reproduction

- Wave: 29; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V06, GH-V07, GH-V08.
- Owned scope: `research/`.
- Acceptance: A distinct Astra leaf reproduces the three studies and falsifies unsupported claims using frozen product outputs.
- Outcome: A distinct Astra leaf reproduces the three studies and falsifies unsupported claims using frozen product outputs.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: research/reproduction/report.md; research/reproduction/findings.json.

## GH-V10 — Prepare exact v1.0 review artifacts

- Wave: 30; status: **RUNTIME_VERIFIED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V09.
- Owned scope: `docs/v1/`.
- Acceptance: Assemble checked application/source/research/evidence bundles, screenshots, launch copy and exact publication destinations for owner review.
- Outcome: Assemble checked application/source/research/evidence bundles, screenshots, launch copy and exact publication destinations for owner review.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: docs/v1/VALIDATION.md; docs/v1/LAUNCH-COPY.md; docs/v1/REVIEW-INSTRUCTIONS.md; docs/v1/PACKAGING-AUDIT.md; docs/v1/COMPLETION-AUDIT.json.

## GH-V11 — Obtain actual external and qualified review

- Wave: 30; status: **PLANNED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V10.
- Owned scope: `docs/v1/`.
- Acceptance: Observe an external supported-environment first-use and obtain qualified review of model interpretation; preserve actual reviewer/participant evidence.
- Outcome: Observe an external supported-environment first-use and obtain qualified review of model interpretation; preserve actual reviewer/participant evidence.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

## GH-V12 — Release only the approved candidate

- Wave: 30; status: **PLANNED**; release: 1.0; origin: source_requirement.
- Dependencies: GH-V10, GH-V11.
- Owned scope: `docs/v1/`.
- Acceptance: After explicit owner approval and applicable review, publish exact artifacts and Tanduna plan, verify unauthenticated downloads and native readback.
- Outcome: After explicit owner approval and applicable review, publish exact artifacts and Tanduna plan, verify unauthenticated downloads and native readback.
- Feature area: v1-delivery
- Source/decision references: OWNER-V1-2026-09-08, docs/v1/CONTRACT.md
- Risk/evidence needs: Only declared synthetic computational claims; no human, field, publication or novelty claim without corresponding evidence.
- Textual-only prerequisites: none recorded.
- Evidence: not yet recorded.

# Grid Horizons contributor tasks

Exactly three Wave 0 foundation tasks are **DONE**, accepted by the authorized root reviewer. All 24 original tasks remain **PLANNED**. [STATUS.md](STATUS.md) is the mutable progress authority; this file and [plan/tasks.json](plan/tasks.json) carry the task contracts and must be updated together when a reviewed scope change is accepted. Tanduna publication/review and task execution are separate operations.

Before an implementation task starts, bind it to an actual repository branch/commit, inspect existing paths and dependencies, identify one primary owner and record the exact verification commands available in that checkout. Proposed directory names below are ownership boundaries to establish, not claims of existing modules. Later outcome packages may need decomposition at their wave gate; do not treat all 24 as one autonomous job.

Protected across every task: evaluator/holdouts outside the task's authority, accepted evidence, unrelated source, credentials, data rights, domain safety rules and resource ceilings. No production deploy, physical system connection, external outreach or paid compute is authorized by a task description. Do not commit, push or publish unless the specific contribution task authorizes it. The maintainer reviews source contributions and scientific claims separately.

Foundation tasks may move from `READY_FOR_REVIEW` to `DONE` after the authorized root reviewer reviews the complete diff, reproduces the named checks and records matching evidence in [STATUS.md](STATUS.md). No separate personal approval is required for this already-authorized foundation review. `READY_FOR_REVIEW` means the author believes the artifact meets the written acceptance; it is not independent acceptance.
## GH-F01 — Establish the architecture contract

- Wave: 0; status: **DONE**; owner: architecture foundation workstream, accepted by the authorized root on 2026-09-07.
- Dependencies: none.
- Owned scope: `ARCHITECTURE.md`, `EXPERIMENTS.md`, `SOURCES.md`.
- Acceptance: Define domain/model boundaries, operational versus design horizons, unit/time/energy-conservation semantics across heterogeneous solvers, one canonical scenario/run/result family, provenance and data rights, feasibility-first Pareto objectives with uncertainty, protected evaluator separation with enforceable isolation before untrusted or protected-confirmation work, calibration versus validation, explicit terminal failures, cancellation/recovery/resource caps, and measured triggers for scaling beyond a local modular implementation.
- Verification: `python3 tools/validate_plan.py` and `python3 -m unittest tools/test_validate_plan.py`; root review checks that no candidate engine, model, rights decision, tolerance, hardware support, scientific result, isolation control, or qualified review is represented as resolved without evidence.
- Evidence offered for review: [architecture](ARCHITECTURE.md), [experiment contract](EXPERIMENTS.md), and [source ledger](SOURCES.md).
- Delivery limit: documentation and plan validation only; no numerical runtime, dependency install, dataset download, or external action.

## GH-F02 — Establish the outcome and dependency roadmap

- Wave: 0; status: **DONE**; owner: architecture foundation workstream, accepted by the authorized root on 2026-09-07.
- Dependencies: GH-F01.
- Owned scope: `README.md`, `ROADMAP.md`, `TASKS.md`, `plan/tasks.json`.
- Acceptance: Prepend Wave 0 while preserving all original Waves 1–8, 24 task IDs, acceptance criteria, original dependency edges and scientific gates; state outcome gates, critical/resource/decision dependencies, uncertainty, cut order, replan triggers, throughput checkpoint and an ambitious evidence-bounded endgame.
- Verification: `python3 tools/validate_plan.py` checks the DAG, markdown/JSON mirror, Wave 0 chain, navigation, statuses and state-evidence rule. Compare GH-001–GH-024 with revision `7256b05c0ea6e37578b93a84292d4d9bb2f7b49d` to verify historical preservation.
- Evidence offered for review: [outcome roadmap](ROADMAP.md), this task contract, and [machine-readable plan](plan/tasks.json).
- Delivery limit: no dates or resource capacity are invented; implementation tasks remain `PLANNED`.

## GH-F03 — Establish the executable next-work packet and repository-plan validation

- Wave: 0; status: **DONE**; owner: architecture foundation workstream, accepted by the authorized root on 2026-09-07.
- Dependencies: GH-F02.
- Owned scope: `docs/work-packets/GH-001.md`, `tools/validate_plan.py`, `tools/test_validate_plan.py`, `STATUS.md`.
- Acceptance: Define the next GH-001 benchmark packet so work can begin without guessing: exact baseline, inputs, candidate decision matrix, owned/protected paths, outputs, checks, representative failure cases, stop/escalation conditions, handoff fields and unresolved authority decisions; provide dependency-free validation and malformed-input regression checks for DAG, contract, navigation and evidence consistency.
- Verification: from repository root run `python3 tools/validate_plan.py` and `python3 -m unittest tools/test_validate_plan.py`; the first command reports `PASS` with the current dynamic task count and the regression suite proves malformed roots, types and dependencies fail cleanly. Original-contract preservation is checked against the repository's initial revision during this foundation review, not permanently frozen into the general validator.
- Evidence offered for review: [GH-001 work packet](docs/work-packets/GH-001.md), validator/regression outputs and [current state](STATUS.md).
- Delivery limit: the packet selects no feeder/engine and authorizes no download, dependency, spend, publication, or physical action.

## GH-001 — Choose a public feeder and metrics

- Wave: 1; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-F03. (The original task had no dependency; Wave 0 adds only this foundation gate.)
- Owned scope: `docs/benchmarks/`.
- Acceptance: Record source, license, units, topology and reference outputs; justify voltage/loading bounds and numerical tolerances.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-002 — Specify data and engine decisions

- Wave: 1; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-001.
- Owned scope: `docs/data/`, `docs/decisions/`.
- Acceptance: Review exact dependency candidates, profiles, rights and supported hardware; distinguish synthetic profiles from observed data.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-003 — Build the scenario skeleton

- Wave: 1; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-001, GH-002.
- Owned scope: `src/`, `tests/`, `scenarios/`.
- Acceptance: A local CLI rejects inconsistent units and dangling network references; its synthetic balance test is hand-checkable.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-004 — Integrate the network baseline

- Wave: 2; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-001, GH-002, GH-003.
- Owned scope: `adapters/network/`.
- Acceptance: Match a public reference power-flow case and retain convergence and residual diagnostics.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-005 — Add transformer loss and thermal state

- Wave: 2; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-001, GH-002, GH-003.
- Owned scope: `adapters/transformer/`.
- Acceptance: Compare the reduced-order model with a documented reference; reject unsupported temperature and load ranges.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-006 — Validate time-series coupling

- Wave: 2; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-001, GH-002, GH-003.
- Owned scope: `src/coupling/`.
- Acceptance: Power-to-energy integration uses explicit intervals; no hidden energy appears at component boundaries.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-007 — Implement baseline and candidate schedules

- Wave: 3; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-004, GH-005, GH-006.
- Owned scope: `scenarios/feeder/`.
- Acceptance: Compare fixed operating policy, bounded tap changes and storage scheduling under identical profiles.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-008 — Add feasibility-first ranking

- Wave: 3; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-004, GH-005, GH-006, GH-007.
- Owned scope: `src/evaluation/`.
- Acceptance: Any candidate violating voltage, loading or storage constraints is excluded with an inspectable reason.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-009 — Generate the energy comparison report

- Wave: 3; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-004, GH-005, GH-006, GH-008.
- Owned scope: `src/reports/`.
- Acceptance: Show losses, served energy, limit violations, cost assumptions and full reproduction inputs for every arm.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-010 — Create load and weather holdouts

- Wave: 4; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `benchmarks/`.
- Acceptance: Separate selection and confirmation periods; report performance over heat and peak-demand conditions.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-011 — Test outages and degraded components

- Wave: 4; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `scenarios/resilience/`.
- Acceptance: Evaluate explicitly enumerated contingencies and unserved energy without live infrastructure access.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-012 — Cross-check numerical assumptions

- Wave: 4; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-007, GH-008, GH-009.
- Owned scope: `tests/validation/`.
- Acceptance: Detect nonconvergence, unit mistakes and misleading aggregate efficiency; compare a second reference where available.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-013 — Add generation-storage planning

- Wave: 5; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-010, GH-011, GH-012.
- Owned scope: `adapters/planning/`.
- Acceptance: Compare scenarios with explicit capacity, degradation, weather and resource assumptions and feasible energy balances.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-014 — Specify and validate higher-fidelity transformer models

- Wave: 5; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-010, GH-011, GH-012.
- Owned scope: `adapters/component/`.
- Acceptance: Require reusable material data, mesh/timestep convergence and a reduced-order comparison before claiming component gains.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-015 — Add lifecycle and novel-concept comparisons

- Wave: 5; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-010, GH-011, GH-012.
- Owned scope: `src/lifecycle/`.
- Acceptance: Expose construction/operation/end-of-life assumptions; speculative designs remain hypotheses and cannot violate conservation.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-016 — Build evidence-grounded design proposals

- Wave: 6; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-013, GH-014, GH-015.
- Owned scope: `src/agents/`.
- Acceptance: Every proposed change lists source assumptions, bounds and a measurable engineering hypothesis.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-017 — Run equal-budget optimization baselines

- Wave: 6; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-013, GH-014, GH-015.
- Owned scope: `src/search/`.
- Acceptance: Compare agent-guided search with grid/random baselines; enforce the same solver and resource budget.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-018 — Confirm robust Pareto candidates

- Wave: 6; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-013, GH-014, GH-015.
- Owned scope: `src/evaluation/`.
- Acceptance: Retest selected designs on untouched scenarios and report tradeoffs, failures and uncertainty.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-019 — Build a local network comparison view

- Wave: 7; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-016, GH-017, GH-018.
- Owned scope: `apps/workbench/`.
- Acceptance: Show units, constraints and failures with keyboard access; a network drawing is labeled as a simulated model.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-020 — Add isolated batch execution

- Wave: 7; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-016, GH-017, GH-018.
- Owned scope: `src/workers/`.
- Acceptance: Enforce resource limits, cancellation and restart recovery without duplicate run publication.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-021 — Export portable energy studies

- Wave: 7; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-016, GH-017, GH-018.
- Owned scope: `src/export/`.
- Acceptance: A fresh machine reconstructs inputs and results from a bundle without private provider access.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-022 — Replicate a second network

- Wave: 8; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-019, GH-020, GH-021.
- Owned scope: `benchmarks/replication/`.
- Acceptance: A new topology exercises the same pipeline; document which assumptions fail to transfer.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-023 — Conduct an engineering review

- Wave: 8; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-019, GH-020, GH-021.
- Owned scope: `docs/review/`.
- Acceptance: A qualified reviewer checks feasibility, model scope and the claimed operating/design improvements.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## GH-024 — Prepare the research preview

- Wave: 8; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: GH-019, GH-020, GH-021.
- Owned scope: `docs/releases/`.
- Acceptance: Include reproducible cases, known limits and maintainer-approved release notes without real-grid deployment claims.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.

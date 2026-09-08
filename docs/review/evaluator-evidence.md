# Independent evaluator evidence — 2026-09-07

Owner: GPT-6 Astra leaf evaluator implementation. The actual local rollout
`turn_context` was checked before writes: `model=gpt-6-astra`, `effort=high`.
This is an agent implementation check, not human engineering review.

## Implementation boundary

Only `src/grid_horizons/evaluator.py`, `tests/test_evaluator.py`, and this
record were authored by this owner. No producer kernel import or call occurs
in the evaluator. Shared imports describe schemas, identifiers and quantity
metadata; they contain no producer physics. Node balances use signed edge
incidence assembled from raw edge records. Voltage and loading metrics are
recomputed using declared root voltage, raw edge powers and scenario branch
parameters. No subtree demand accumulation is reused.

Admission checks complete unique raw node/branch/interval coverage; closed
fields; finite bounded numbers; exact unit, basis, sign, location and typed
interval support; immutable scenario/model/policy identities; declared
profiles and charging/discharging schedules. Mathematical checks cover
served/unserved demand, injection/curtailment, separate real/reactive node
balance, root exchange and voltage, branch voltage drop and apparent loading,
storage continuity/transition/conversion losses, interval and full-study
real-energy balance. Modeled limits and final storage equality are checked
before objective quantities are materialized.

Malformed/inconsistent evidence returns `INVALID_RESULT` with empty metrics.
Ordinary bounded canonical JSON retains its raw artifact digest even when
structural admission fails (including missing interval output); nonfinite,
custom, excessively nested or oversized objects remain invalid with no digest.
Consistent results outside modeled bounds retain diagnostic metrics and return
`COMPLETED_INFEASIBLE`. Only `COMPLETED_VALID` permits comparison. Invalid
scenario contracts and unexpected checker exceptions propagate separately for
the coordinator. Comparison rejects missing/duplicate arms, mismatched
scenario/model/evaluator identities, incomplete or malformed quantities, and
failed/infeasible arms. Two admitted arms return `INDETERMINATE` with unitful
candidate-minus-baseline differences, never an overall winner.

## Reproducible check

From the project directory:

```sh
TMPDIR="$PWD/runs/tmp" PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p test_evaluator.py
```

Observed final run: **29 test methods passed**, 0.204 seconds on the local
CPython runtime. Parameterized subcases exercise additional mutations.
No dependencies were installed and no external service was called.

The two-node hand reference is assembled directly as raw quantities without
calling the producer: 10,000 W + 2,000 var produces `u_child=0.9972`,
36,000,000 J served in an hour, and the separate var residual remains a power
quantity. A patched producer entry point raises if called during evaluation.
Other tests may obtain original raw trajectories from the producer, but their
expected answers are independent constants from ADR-001 or direct arithmetic.

The full-case references admitted both policies with baseline import/export
128/10 kWh and candidate 119.9/0 kWh; each serves 174 kWh and injects 56 kWh.
Storage conversion loss is 6,840,000 J within the case tolerance. Comparison
reports a net-import increase of 6,840,000 J and peak-import change of −8,100 W.

Mutation coverage includes 1 W and 1 var edge errors, 0.0001 pu² voltage error,
3,600 J storage-state errors, 1 J conversion error, missing and duplicate
records, one-second interval changes, fractional/bool support, every quantity
metadata dimension, nonfinite/boolean/huge numbers, altered served demand,
curtailment counted as generation or deducted twice, coherent wrong-policy
and wrong-profile trajectories, and simultaneous import/export. Distinct
infeasibility controls cover lowered rating, raised voltage minimum, limited
capacity, power-limit exceedance, negative storage, final-energy mismatch and
the 0.90–1.10 pu model-domain band. Boundary controls test inside/outside the
ADR's voltage, scalar-power and final-energy roundoff allowances. Zero power,
unity efficiency, reversed component ordering, nonuniform durations and
object immutability also pass.

## Scope limits

These tests establish numerical/code consistency for the bounded synthetic
model. They do not validate physical network losses, AC applicability,
ampacity/thermal state, storage chemistry, cost/emissions, or quantify model
error. Missing human first-use and qualified engineering review remain open.

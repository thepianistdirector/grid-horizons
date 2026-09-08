# Raw interval contract and independent evaluator interface

Normative model: [ADR-001](../decisions/ADR-001-synthetic-tutorial.md).
Field dimensions/signs/aggregation: `src/grid_horizons/raw_contract.py`.
These shared declarations contain no physics; producer and checker implement
their own mathematical paths.

Raw envelope, closed fields:

```text
schema_version: grid-horizons.raw/v1
scenario_sha256: canonical digest of the validated immutable scenario
policy_id: baseline | candidate
model_id: lossless-lindistflow-storage/v1
intervals: array in exact scenario interval order
```

Each interval contains exactly `id`, `start_s`, `end_s`, `nodes`, `branches`,
`storage`, `grid`. Its identifiers and integer endpoints exactly match the
scenario. Nodes contain `node_id` plus every NODE_FIELDS quantity, including
zero load/generation quantities at the root. Branches contain `branch_id`
plus BRANCH_FIELDS. Complete unique node/branch coverage is required; array
order need not imply topology. Storage and grid contain only their respective
field quantities. Storage quantities locate the declared storage node; grid
quantities locate the root.

Each raw quantity contains `value`, `unit`, `basis`, `sign`, `location`,
`support`. Support is `{interval_id, start_s, end_s, aggregation}`. Metadata
must match the shared field declaration and exact scenario interval. The
adapter cannot relabel a mean as an integral or change units/bases. Storage
energy may become negative algebraically; retain it to report infeasibility.
Nonpositive squared voltage prevents a model solution and is FAILED_SOLVER.

## Evaluator API

`evaluate(scenario, raw, policy_id) -> dict` validates scenario input, then
checks the raw envelope, completeness/finiteness, quantity metadata, declared
profiles and dispatch, real/reactive node incidence balance, root exchange,
branch voltage-drop/loading identities, storage transition/continuity/loss,
service and injection/curtailment identities. It must not call the producer
kernel or trust raw totals/pass flags. A coherent trajectory from a different
policy is invalid even when its balances close.

Malformed scenario raises ContractError. Malformed/inconsistent raw output
returns INVALID_RESULT with empty `metrics` and comparison eligibility false.
A valid algebraic result violating modeled limits, storage final equality or
the model-domain voltage band is COMPLETED_INFEASIBLE and retains diagnostic
metrics. Only COMPLETED_VALID is comparison-eligible. Unexpected checker
exceptions propagate so the coordinator records FAILED_EVALUATOR.

Result common fields: `schema_version` (grid-horizons.result/v1),
`scenario_sha256`, `raw_sha256`, `policy_id`, `model_id`, `evaluator_version`,
`state`, `comparison_eligible`, `findings` (structured code/message/location
and interval where applicable), `metrics`, `ledger`, `not_evaluated`,
`uncertainty`, `scope`.

Metric keys and units:

```text
import_energy, export_energy, net_import_energy, served_load_energy,
unserved_load_energy, available_generation_energy, injected_generation_energy,
curtailed_potential_energy, storage_charge_energy, storage_discharge_energy,
storage_conversion_loss, initial_storage_energy, final_storage_energy: J
peak_import_power: W
min_voltage, max_voltage: pu (magnitudes, not squared values)
max_loading: 1
```

Every metric is a quantity with explicit unit, basis, sign, location and full
study support. The real-energy ledger and maximum real/reactive node residuals
stay separate (J, W, var). No reactive integral is a real-energy metric.
Squared voltage and loading are recomputed from raw data for evaluation and
the report uses evaluator-owned metrics only.

`compare(results)` expects exactly one current result per arm from the same
scenario/model/evaluator. It returns `INELIGIBLE` if either arm is invalid,
failed or infeasible; otherwise `INDETERMINATE` because model uncertainty and
unmodeled costs prevent an overall winner. Supported metric differences may
be displayed with units, without ranking the policy. Mismatched identities
cannot be compared.

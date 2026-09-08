# Fixed-policy robustness preregistration

Frozen before confirmation runs on 2026-09-08. Runtime identity is recorded in
`runtime-identity.json`: actual gpt-6-astra, high. Source was read only; all writes
are confined to this investigation directory. Isolation means directory discipline
and frozen package hashes, not an operating-system sandbox.

## Question and scientific context

Across a finite deterministic set of synthetic profile and parameter perturbations,
do fixed storage, source-tap, and combined schedules retain feasibility and lower
network-plus-storage conversion losses or peak import relative to idle operation?
The policies are the packaged example schedules, chosen before held-out results:
baseline idle and tap zero; storage +8 kW charging 10:00–14:00 and −7.22 kW
discharging 17:00–21:00; tap constant +2 (=1.0125 pu ideal source); combined both.
No policy optimization, retiming, repair, or held-out tuning is permitted.

Primary sources browsed 2026-09-08:
- [MATPOWER distribution power flow, §4.3.2](https://matpower.app/manual/matpower/DistributionPowerFlow.html): radial current summation and backward/forward sweeps support the method context. This does not validate the implementation or this synthetic feeder.
- [Farivar and Low, Branch Flow Model](https://arxiv.org/abs/1204.4865): branch flow/power balance context; no optimal power flow or optimality claim is made.
- [PyPSA storage equations](https://docs.pypsa.org/latest/user-guide/optimization/storage/): charging and discharging efficiency directions and cyclic energy constraints motivate the chronological ledger.

The package implements balanced constant-PQ AC with series impedances, no shunts,
one ideal source and one fixed-efficiency storage device. See read-only
`docs/v1/MODEL.md`, `CONTRACT.md`, and `src/grid_horizons/{ac,ac_check,lab}.py`.
Synthetic AGPL-3.0-only generator `canopy13/v1`, 13 buses, 100 kVA/12.47 kV base.

## Frozen design

Hold out profile seeds **101, 103, 107, 109**. Each controls solar cloud factors;
loads share the deterministic shape. Four seeds are not four independently
sampled feeders. Every scenario uses 96 quarter-hour intervals covering 24 h.
Each seed is crossed with these twelve cases (all unspecified multipliers 1,
all unspecified shifts 0):

| Treatment | Load and reactive multiplier | Solar multiplier | Load shift h | Solar shift h | Resistance multiplier | Current-limit multiplier |
|---|---:|---:|---:|---:|---:|---:|
| nominal | 1 | 1 | 0 | 0 | 1 | 1 |
| load_low | 0.8 | 1 | 0 | 0 | 1 | 1 |
| load_high | 1.2 | 1 | 0 | 0 | 1 | 1 |
| solar_low | 1 | 0.7 | 0 | 0 | 1 | 1 |
| solar_high | 1 | 1.3 | 0 | 0 | 1 | 1 |
| load_early | 1 | 1 | −3 | 0 | 1 | 1 |
| load_late | 1 | 1 | +3 | 0 | 1 | 1 |
| solar_early | 1 | 1 | 0 | −2 | 1 | 1 |
| solar_late | 1 | 1 | 0 | +2 | 1 | 1 |
| resistance_high | 1 | 1 | 0 | 0 | 1.5 | 1 |
| derated | 1 | 1 | 0 | 0 | 1 | 0.8 |
| joint_adverse | 1.2 | 0.7 | +3 | −2 | 1.5 | 0.8 |

Shifts are circular on the daily array: positive means the profile occurs later.
Reactive power shifts and scales with load. Solar shifts preserve the daily solar
energy; the circular load shift represents a periodic daily schedule, not an event
crossing an independently simulated day. Profiles change relative to the fixed
predeclared schedule: this is a forecast-mismatch proxy, not a probabilistic
forecast model. Resistance and ampacity changes are admitted synthetic assumptions,
not temperature or equipment-aging models. Reactance stays fixed.

48 modeled scenarios × 4 policies = 192 trajectories. One additional retained
unsupported outage input changes the source branch parent to −1, attempting a
disconnected source. Expect validation rejection, no trajectory, no unserved-load
or reliability estimate. One nominal standalone `lab run` duplicates the first
campaign case to exercise the normal producer and deterministic comparison.

## Outcomes, criteria, stopping and costs

Primary outcome: baseline total loss minus candidate total loss (kWh/day), where
total loss includes network loss and storage conversion loss. Secondary: baseline
peak import minus candidate peak import (kW). Positive is improvement. Also report
relative percentages against baseline, network-only loss, voltage extrema, maximum
current loading, storage terminal delta, power and energy residuals, all-policy
feasibility counts, and signed effect ranges over the finite set.

A universally robust candidate must be COMPLETED_VALID in all 48 modeled cases;
one violation falsifies that claim. Loss dominance additionally requires positive
loss saving in every case with both candidate and baseline feasible; report the
exact eligible denominator and never rank an infeasible policy. Practical reporting
thresholds fixed here are ≥0.5 kWh/day loss saving and ≥1 kW peak reduction; these
are descriptive synthetic-study thresholds, not economic or utility standards.
No population significance, confidence intervals, or probability-of-success claims.
Power residual ≤1e−7 pu and energy residual ≤1e−6 kWh are package acceptance limits.
No new cases or tuning after outcomes. Preserve every failure and rejected attempt.

Run frozen `releases/1.0.0rc1/grid-horizons.pyz` implementation SHA-256
`cdf8e0b82397cbad5e9f5979fd01d98fd931a7c772c5dcd1c8b42a35ac90a4a4`.
Primary outputs must come from packaged `lab example/run/campaign/verify`.
Because root reported a possible legacy 1 MiB decoder ceiling, first attempt the
complete campaign and preserve rejection; if rejected solely for size, attempt
seed-specific shards, then per-case `lab run` if needed. The modeled scenario set
never changes. Stop for an unexpected implementation hash, unexplained verification
failure, >100 scenario executions, >96 intervals/scenario, or 300 measured CPU
seconds. Execute sequentially on one CPU; record wall/CPU time and peak child RSS.
Report software/source/runtime hashes, commands, inventory and raw outputs.

No field, hardware, human participation, independent human review, peer review,
reliability validation, or novelty claim is authorized or inferred from this study.

# Canopy13 numerical validity and temporal-resolution benchmark

Engineering benchmark · Grid Horizons 1.0.0rc1, with an additive 1.0.0rc2 bridge · 2026-09-08

## Result

The original Canopy13 sweep matches an independently authored nodal Newton calculation throughout the sampled feeder cases at solver tolerances 1e-10 and 1e-12. All twelve baseline cases run at 1e-6 are instead `INVALID_RESULT`: the solver reports convergence, but the independently evaluated nodal power residual exceeds 1e-7 pu. All 36 tighter-tolerance baseline cases are numerically consistent and `COMPLETED_INFEASIBLE` because the declared root-branch current limit is exceeded. No core baseline is feasible and no core ranking is produced.

Hourly sampling understates the daily peak import by 1.947319 kW (2.132%) relative to the finest sampled five-minute case. Finer sampling reduces this difference, but 288 intervals is a comparator, not exact temporal ground truth. The findings establish bounded synthetic computational behavior only.

## Question, admission, and preregistration

The question was whether the original synthetic 13-bus balanced radial case gives consistent voltages, source power and losses under a second numerical method, and how solver tolerance and time resolution affect numerical validity, declared feasibility and daily metrics. The original preregistration was frozen before any confirmation run; its timestamp, complete design and hash are retained in [preregistration.json](preregistration.json), [readable preregistration](preregistration.md) and [hash record](preregistration.sha256). It was not edited after confirmation.

The fixed design crosses three seeds (17, 23, 31), four interval counts (24, 48, 96, 288 per 24-hour day) and four sweep stopping tolerances (1e-6, 1e-8, 1e-10, 1e-12): 48 baseline cases. Each uses unit load and solar scaling, idle storage and zero source tap. A separate generated seed-17, 96-interval example retains all four original policies. A no-load feeder, analytic resistive two-bus feeder and deliberately exhausted one-iteration solver complete the initial 52 scenarios / 55 policy combinations. The original experiment attempted 5,928 policy intervals; the intentional failure occurs before its first interval, leaving 5,904 solved intervals, all compared with Newton.

Canopy13 has 13 buses and 12 ordered radial branches. The recorded 24-hour inputs encode balanced constant-PQ demand, prescribed solar generation, series impedances without shunts and a fixed ideal slack tap schedule. Data provenance declares `ORIGINAL_SYNTHETIC`, generator `canopy13/v1` and `AGPL-3.0-only`; this study uses the project's bundled generator, without third-party feeder records. It does not independently establish historical authorship, relicense external data, or imply equivalence to the IEEE 13-node feeder. Seed variation changes hourly solar cloud multipliers only; topology, load shape and impedances are fixed. There are no sampled physical feeders or human participants.

## Mathematical comparators

The packaged producer uses a complex backward/forward current sweep. MATPOWER documents radial current summation using ordered branches, demand currents, backward accumulation and forward voltage updates; this supports the method family and radial applicability, not a claim that MATPOWER was executed here. The present generator models photovoltaic injections as prescribed negative demand, not voltage-controlled PV buses. [MATPOWER manual, §4.3](https://matpower.app/manual/matpower/DistributionPowerFlow.html), accessed 2026-09-08.

Branch-flow literature supplies context for complex network balance. No relaxation, optimal power flow, uniqueness theorem or global optimality guarantee is tested or transferred to this benchmark. [Farivar and Low, *Branch Flow Model: Relaxations and Convexification*, v4 (2013)](https://arxiv.org/abs/1204.4865v4), accessed 2026-09-08.

The independent reference in [rerun.py](rerun.py) assembles the dense nodal admittance matrix Y from input branches and solves, for every non-slack bus i,

`F_i(V) = V_i conjugate((YV)_i) + (P_load,i - P_solar,i + P_storage,i + j Q_i)/S_base = 0`.

Real and imaginary voltages are separate unknowns. An analytic rectangular Jacobian and independently written partial-pivot Gaussian elimination give Newton steps from a flat start. The only imported producer module function is `ac.example`, used to generate inputs; the reference calls neither producer solve functions nor the packaged evaluator. Reference termination requires maximum complex nodal residual <=1e-11 pu with at most 30 steps. Source power is `V_0 conjugate((YV)_0) S_base`; each branch loss is the real sum of sending- and receiving-end powers. Full reference complex voltages, source powers, individual branch losses, iteration counts and discrepancies are preserved for every solved interval.

The packaged evaluator separately reconstructs branch currents from Ohm's law and checks complex power balance (<=1e-7 pu), the energy ledger (<=1e-6 kWh), declared current and voltage limits, and chronological storage constraints. The solver's voltage-update tolerance and these evaluator bounds are different quantities. A small voltage error may be amplified by nodal admittance into a larger power residual.

Preregistered tight-tolerance acceptance bounds are 1e-8 pu maximum complex voltage discrepancy, 1e-6 kVA maximum complex source discrepancy, and 1e-6 kW interval loss discrepancy. Loose-tolerance runs were retained regardless of validity. The analytic two-bus control uses r=0.1 pu, x=0, p=0.1 pu and the high-voltage solution `V=(1+sqrt(1-4rp))/2`, with loss `r(p/V)^2 S_base`. The no-load control requires slack voltage everywhere and zero loss.

## Solver sensitivity and full-feeder agreement

Each table row covers twelve baseline cases. Discrepancies are maxima over every bus and solved interval, including invalid cases. Infeasible metrics are reported diagnostically and are never ranked.

| Sweep tolerance | States (12 cases each) | Sweep iterations | Max complex V error, pu | Max source error, kVA | Max loss error, kW | Max evaluator power residual, pu |
|---|---|---:|---:|---:|---:|---:|
| 1e-06 | INVALID_RESULT | 3–4 | 9.87768e-09 | 5.56806e-07 | 9.22062e-07 | 5.81612e-07 |
| 1e-08 | COMPLETED_INFEASIBLE | 4–5 | 9.87867e-11 | 5.2857e-09 | 9.08567e-09 | 5.51723e-09 |
| 1e-10 | COMPLETED_INFEASIBLE | 4–6 | 9.86839e-13 | 6.52569e-11 | 9.59569e-11 | 5.93366e-11 |
| 1e-12 | COMPLETED_INFEASIBLE | 5–7 | 1.22327e-14 | 2.79518e-11 | 1.04272e-12 | 5.76606e-13 |

The tight-tolerance maxima are 9.86839e-13 pu voltage, 6.52569e-11 kVA source and 9.59569e-11 kW loss: all within their preregistered bounds. Newton takes at most three updates on all core intervals, with maximum residual 1.47379e-13 pu. These are accuracy comparisons, not a solver speed contest: producer/evaluator persistence and independent calculation costs are measured separately and execute different workloads.

At 1e-6, all twelve cases fail the nodal residual gate; their daily energy residuals still remain below 1e-6 kWh. This directly falsifies the implication “reported sweep convergence guarantees evaluator validity.” The 1e-8 cases pass the numerical gates for this finite design, but this does not establish sufficiency for other impedances, loading levels or models. At the default 1e-10 tolerance the observed discrepancies have substantial margin to the preregistered numerical bounds.

The analytic voltage is 0.9898979485566356 pu and loss is 0.1020514433643804 kW. Producer errors are 1.11022e-16 pu and 1.83187e-15 kW; Newton voltage error is 0 pu. The no-load producer has exactly unit voltages and zero source power/loss; Newton agrees. The one-iteration control records `FAILED_SOLVER` with `iteration budget exhausted`, zero returned rows and an empty ranking. All controls behaved as preregistered.

## Time-resolution sensitivity

The following comparison uses tolerance 1e-12. Ranges are deterministic minima–maxima over the three chosen seeds, not confidence intervals. Each resolution regenerates profiles by evaluating the same formulas at interval midpoints. The scenario treats those values as constant interval mean powers; they are not analytically integrated means. Thus this is sensitivity of the complete sampled-input workflow, not temporal integration error with identical input arrays. All grid intervals align with hourly cloud-factor boundaries. Daily peak import is unchanged across seeds because its evening interval has zero solar production.

| Intervals/day | Network loss range, kWh | Solar energy range, kWh | Peak import, kW | Minimum voltage, pu | Maximum current loading ratio |
|---:|---:|---:|---:|---:|---:|
| 24 | 7.377894–7.655340 | 635.610637–659.636815 | 89.375551 | 0.986486779 | 1.024476423 |
| 48 | 7.402947–7.676735 | 634.249746–658.224482 | 90.838994 | 0.986265097 | 1.041265583 |
| 96 | 7.409172–7.682065 | 633.910161–657.872060 | 91.211850 | 0.986208615 | 1.045543208 |
| 288 | 7.411013–7.683642 | 633.809591–657.767689 | 91.322871 | 0.986191797 | 1.046816904 |

| Intervals/day | Loss difference from matching-seed 288-step case, kWh | Peak import difference, kW | Minimum-voltage difference, pu |
|---:|---:|---:|---:|
| 24 | -0.033119220 to -0.028301576 | -1.947319292 | 0.000294983 |
| 48 | -0.008066394 to -0.006906573 | -0.483876929 | 0.000073301 |
| 96 | -0.001841431 to -0.001577387 | -0.111020418 | 0.000016818 |

The hourly-to-five-minute loss difference has magnitude 0.028302–0.033119 kWh, whereas the 15-minute-to-five-minute difference is 0.001577–0.001841 kWh. Hourly sampling makes the minimum voltage appear 0.000294983 pu higher and peak current ratio 0.022340481 lower. Despite these differences, every baseline exceeds the declared root-branch current limit at every resolution. No feasibility reversal is observed in this design. A boundary-case claim would require a separately preregistered limit/loading experiment.

## Original four-policy example

This table is one seed-17, 96-interval day at default tolerance 1e-10. It is not a cross-seed policy-effect estimate.

| Policy | State | Current ratio maximum | Peak import, kW | Network loss, kWh | Storage conversion loss, kWh | Total loss, kWh |
|---|---|---:|---:|---:|---:|---:|
| baseline | COMPLETED_INFEASIBLE | 1.045543 | 91.211850 | 7.680509 | 0.000000 | 7.680509 |
| storage | COMPLETED_VALID | 0.966013 | 83.834336 | 6.803310 | 3.120000 | 9.923310 |
| tap | COMPLETED_INFEASIBLE | 1.032329 | 91.186769 | 7.490146 | 0.000000 | 7.490146 |
| combined | COMPLETED_VALID | 0.953829 | 83.813256 | 6.634728 | 3.120000 | 9.754728 |

Baseline and tap violate only the root-branch current limit (six and four intervals respectively). Storage and combined satisfy the declared limits and terminal energy neutrality; storage reduces network losses while adding 3.12 kWh conversion loss. The packaged ranking remains empty for the entire study because the baseline is infeasible. This is the documented admission rule, not a missing result or evidence for policy superiority. The original synthetic default is therefore useful for studying an infeasible baseline and candidate feasibility, but cannot support a feasible-baseline loss ranking without a separately declared changed case.

## Evidence, unsuccessful outcomes, and release bridge

The initial outcomes are 4 `COMPLETED_VALID`, 38 `COMPLETED_INFEASIBLE`, 12 `INVALID_RESULT` and 1 `FAILED_SOLVER`. No numerical invalidity or infeasibility is dropped. Every one of the 52 original study bundles passed packaged `lab verify`; verification establishes integrity and faithful evaluation, not feasibility. CLI exit code 0 denotes a recorded study, including the expected failed-solver study, rather than solver success for every policy.

All primary results were produced by `python3 releases/1.0.0rc1/grid-horizons.pyz lab ...`. A two-case campaign supplied the first two baseline cases; remaining cases used `lab run`. The original four-policy input was created by `lab example`. CLI stdout/stderr, exact arguments, return codes and timings are retained for all 105 initial calls. No alternate producer was run.

Before preregistration the root disclosed an rc1 input-decoder 1 MiB ceiling inconsistent with the documented larger limit. This study therefore chose bounded per-case calls and a small campaign; it did not attempt or claim to reproduce a large-campaign failure. The limitation did not prevent the planned scientific comparisons. It is a workflow limitation reported by the root, not a locally observed rejected attempt.

After initial confirmation, rc2 was supplied with fixes to input-size handling, help and graph scaling. A separate [bridge preregistration](bridge-rc2-001/preregistration.json) was frozen before rerunning the saved original four-policy input. Both `ac.py` and `ac_check.py` are byte-identical between rc1 and rc2. All four complete policy records, including raw trajectories and evaluations, compare exactly equal; rc2 `lab verify` passes. This adds one scenario and four policy combinations, bringing the entire study to 53 scenarios / 59 combinations. It supports numerical continuity for the tested original case; it is not an exhaustive equivalence proof for every release feature.

## Reproduction, identity, and measured cost

Actual investigator model was checked in runtime turn context: `gpt-6-astra`, high effort. Packaged runtime: Linux x86_64, CPython 3.12.14, model `balanced-radial-pq/v2`. The original implementation hash is `cdf8e0b82397cbad5e9f5979fd01d98fd931a7c772c5dcd1c8b42a35ac90a4a4`; zipapp SHA-256 is `57573bdb2c8bb9c983b5dcc1b0c8850ac0ae6e3c87b8e6a24d60077ca03fe2ce`. The package records source revision `3d4a4dc7718d72e0d20785c70154c800cc849093` with preserved uncommitted implementation, so the implementation hash—not that commit alone—is the identity. Runtime executable SHA-256, full Python/platform descriptions and frozen-source identity are recorded in the preregistration and manifests.

Initial work used 21.783 CPU seconds and 22.139 wall seconds; independent Newton consumed 6.921 CPU seconds and packaged CLI child calls consumed 13.449 CPU seconds. The bridge added 0.371 CPU seconds. Measured experiment CPU totals 22.154 seconds, well below the 300-second ceiling. Execution used one CPU child at a time and no paid resources. The initial artifact tree occupied 47,613,296 bytes before its final cost/hash manifests. These are one-run measurements on the current host, not portable speed or price estimates; final report-writing/tool orchestration time is not included in solver experiment cost.

Run from the project directory, using fresh output paths:

```sh
python3 research/benchmark/rerun.py --output research/benchmark/reproduction-002
python3 research/benchmark/bridge_rc2.py --output research/benchmark/bridge-reproduction-002
```

The main rerun checks the preregistered rc1 package hash, enforces output confinement and refuses an existing output directory. It regenerates the fixed design, reruns the packaged commands and recalculates the independent reference. The bridge intentionally compares against the preserved original `attempt-001` case. `analyze.py` regenerates this report and `findings.json` from the retained canonical experiment. Rerun CPU limits apply independently to each explicitly started reproduction; the reported study includes only its retained initial run and bridge.

Key retained artifacts:

- [All-scenario feasibility CSV](all-scenario-feasibility.csv): all 59 scenario/policy rows across the initial experiment and bridge, including invalid and failed outcomes; [initial-only CSV](attempt-001/all-scenario-feasibility.csv) preserves the 55 original rows.
- [Results](attempt-001/results.json): exact metrics, states, exclusion reasons and comparison maxima.
- [CLI command ledger](attempt-001/commands.json) and corresponding `logs/*.stdout` / `logs/*.stderr`.
- `attempt-001/reference/*.json`: full raw independent calculations and per-interval discrepancies.
- [Costs and identity](attempt-001/costs.json), [all initial file hashes](attempt-001/hashes.json), [bridge evidence](bridge-rc2-001/result.json) and [bridge hashes](bridge-rc2-001/hashes.json).
- [Machine-readable finding](findings.json), [primary rerun](rerun.py), [bridge rerun](bridge_rc2.py) and [analysis generator](analyze.py).

## Scope and unresolved questions

The preregistered numerical agreement and control criteria pass. Numerical failure retention also behaves as intended. The initial 1e-6 outcomes invalidate any unconditional “solver converged, therefore valid” claim, and the root current violation rules out describing the untouched default as a feasible baseline. No independent-solver discrepancy blocks the bounded computational claim.

The three chosen seeds and four resolutions support finite deterministic ranges for one original synthetic feeder family. They do not estimate a feeder population, weather distribution or real-world uncertainty. No impedance or load stress sweep, low-voltage branch exploration, ill-conditioned Jacobian campaign or physical accuracy measurement was performed. The second method shares physical equations, input data and floating-point arithmetic with the implementation under study; separate code structure mitigates implementation error but does not independently validate the physical model. Work was performed by a delegated AI investigator in the same owner-authorized workspace, with source immutable by convention and verified hashes rather than an adversarial operating-system sandbox.

Unbalanced networks, outages, protection, thermal ratings, transformer losses, storage aging, field measurements, independent human review and public feeder reproduction remain outside this study. There is no novelty, publication acceptance, peer-review or physical-validation claim.

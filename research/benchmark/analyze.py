#!/usr/bin/env python3
"""Generate benchmark report and machine-readable claims from retained results."""
import collections
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
read = lambda p: json.loads(p.read_text())
d = read(HERE / 'attempt-001/results.json')
cost = read(HERE / 'attempt-001/costs.json')
bridge = read(HERE / 'bridge-rc2-001/result.json')
plan = read(HERE / 'preregistration.json')
core = [x for x in d if x['group'] == 'core']
tight = [x for x in core if x['tolerance'] <= 1e-10]
limits = {'voltage_abs_pu':1e-8, 'source_abs_kva':1e-6, 'loss_abs_kw':1e-6}
maxerr = {k:max(x['reference'][k] for x in tight) for k in limits}
states = dict(collections.Counter(x['state'] for x in d))
control = next(x for x in d if x['id']=='analytic-two-bus')['analytic']
findings = dict(schema='grid-horizons.research-finding/v1', study='benchmark',
    claim='For the finite original Canopy13 cases, tight-tolerance sweep results agree with independent nodal Newton; convergence at 1e-6 does not ensure evaluator validity, and original baseline current feasibility fails at every sampled resolution.',
    status='SUPPORTED_WITH_BOUNDED_SCOPE', actual_model='gpt-6-astra',
    preregistration_sha256=hashlib.sha256((HERE/'preregistration.json').read_bytes()).hexdigest(),
    original_implementation_sha256=plan['implementation_sha256'],
    rc2_implementation_sha256=read(HERE/'bridge-rc2-001/preregistration.json')['new_implementation_sha256'],
    core_cases=48, original_scenarios=52, original_policy_combinations=55,
    total_scenarios_including_bridge=53,total_policy_combinations_including_bridge=59,
    original_states=states, independently_compared_intervals=5904,
    tight_tolerance_comparison_maxima=maxerr, preregistered_comparison_bounds=limits,
    tight_tolerance_comparison_pass=all(maxerr[k]<=limits[k] for k in limits),
    loose_tolerance_invalid_cases=12, numerically_valid_but_infeasible_core_cases=36,
    analytic_control=control, bridge_pass=bridge['passed'],
    cpu_seconds=cost['cpu_seconds']+bridge['cpu_seconds'],
    uncertainty='Finite deterministic ranges over seeds 17/23/31, steps 24/48/96/288; not population confidence intervals.',
    limits=['Original synthetic AGPL case, not a public or physical feeder benchmark.',
            'Time-resolution comparison changes midpoint-sampled inputs; 288 steps is not exact temporal truth.',
            'No loading/impedance stress sweep, unbalanced model, field validation, human study or peer review.',
            'Second method uses same physical equations and inputs; independent implementation is workflow separation, not external human independence.'],
    artifacts={'report':'report.md','feasibility':'attempt-001/all-scenario-feasibility.csv',
               'results':'attempt-001/results.json','reference':'attempt-001/reference',
               'rerun':'rerun.py','bridge':'bridge_rc2.py'})
(HERE/'findings.json').write_text(json.dumps(findings,indent=2)+'\n')
with (HERE/'attempt-001/all-scenario-feasibility.csv').open(newline='') as f:
    reader=csv.DictReader(f); fields=['attempt']+reader.fieldnames
    original_rows=list(reader)
with (HERE/'all-scenario-feasibility.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
    for row in original_rows:
        writer.writerow(dict(attempt='rc1-initial',**row))
    for row in original_rows:
        if row['id']=='original-four-policies':
            writer.writerow(dict(attempt='rc2-bridge-identical-record',**row))

lines = ['# Canopy13 numerical validity and temporal-resolution benchmark',
         '', 'Engineering benchmark · Grid Horizons 1.0.0rc1, with an additive 1.0.0rc2 bridge · 2026-09-08', '',
'''## Result

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
''',
'| Sweep tolerance | States (12 cases each) | Sweep iterations | Max complex V error, pu | Max source error, kVA | Max loss error, kW | Max evaluator power residual, pu |',
'|---|---|---:|---:|---:|---:|---:|']
for tol in [1e-6,1e-8,1e-10,1e-12]:
    a=[x for x in core if x['tolerance']==tol]
    e={k:max(x['reference'][k] for x in a) for k in limits}
    lines.append(f"| {tol:.0e} | {a[0]['state']} | {min(x['solver_iterations']['min'] for x in a)}–{max(x['solver_iterations']['max'] for x in a)} | {e['voltage_abs_pu']:.6g} | {e['source_abs_kva']:.6g} | {e['loss_abs_kw']:.6g} | {max(x['metrics']['max_power_residual_pu'] for x in a):.6g} |")
lines += ['',f"The tight-tolerance maxima are {maxerr['voltage_abs_pu']:.6g} pu voltage, {maxerr['source_abs_kva']:.6g} kVA source and {maxerr['loss_abs_kw']:.6g} kW loss: all within their preregistered bounds. Newton takes at most three updates on all core intervals, with maximum residual 1.47379e-13 pu. These are accuracy comparisons, not a solver speed contest: producer/evaluator persistence and independent calculation costs are measured separately and execute different workloads.", '',
'''At 1e-6, all twelve cases fail the nodal residual gate; their daily energy residuals still remain below 1e-6 kWh. This directly falsifies the implication “reported sweep convergence guarantees evaluator validity.” The 1e-8 cases pass the numerical gates for this finite design, but this does not establish sufficiency for other impedances, loading levels or models. At the default 1e-10 tolerance the observed discrepancies have substantial margin to the preregistered numerical bounds.
''',
f"The analytic voltage is {control['expected_voltage_pu']:.16f} pu and loss is {control['expected_loss_kw']:.16f} kW. Producer errors are {control['producer_voltage_error_pu']:.6g} pu and {control['producer_loss_error_kw']:.6g} kW; Newton voltage error is {control['newton_voltage_error_pu']:.6g} pu. The no-load producer has exactly unit voltages and zero source power/loss; Newton agrees. The one-iteration control records `FAILED_SOLVER` with `iteration budget exhausted`, zero returned rows and an empty ranking. All controls behaved as preregistered.", '',
'''## Time-resolution sensitivity

The following comparison uses tolerance 1e-12. Ranges are deterministic minima–maxima over the three chosen seeds, not confidence intervals. Each resolution regenerates profiles by evaluating the same formulas at interval midpoints. The scenario treats those values as constant interval mean powers; they are not analytically integrated means. Thus this is sensitivity of the complete sampled-input workflow, not temporal integration error with identical input arrays. All grid intervals align with hourly cloud-factor boundaries. Daily peak import is unchanged across seeds because its evening interval has zero solar production.
''',
'| Intervals/day | Network loss range, kWh | Solar energy range, kWh | Peak import, kW | Minimum voltage, pu | Maximum current loading ratio |',
'|---:|---:|---:|---:|---:|---:|']
for steps in [24,48,96,288]:
    a=[x for x in core if x['tolerance']==1e-12 and x['steps']==steps]
    m=a[0]['metrics']
    ranges=lambda key:f"{min(x['metrics'][key] for x in a):.6f}–{max(x['metrics'][key] for x in a):.6f}"
    lines.append(f"| {steps} | {ranges('network_loss_kwh')} | {ranges('solar_kwh')} | {m['peak_import_kw']:.6f} | {m['min_voltage_pu']:.9f} | {m['max_loading']:.9f} |")
lines += ['', '| Intervals/day | Loss difference from matching-seed 288-step case, kWh | Peak import difference, kW | Minimum-voltage difference, pu |', '|---:|---:|---:|---:|']
for steps in [24,48,96]:
    a=[x for x in core if x['tolerance']==1e-12 and x['steps']==steps]
    pairs=[(x,next(y for y in core if y['tolerance']==1e-12 and y['steps']==288 and y['seed']==x['seed'])) for x in a]
    delta=lambda k:[x['metrics'][k]-y['metrics'][k] for x,y in pairs]
    l=delta('network_loss_kwh')
    lines.append(f"| {steps} | {min(l):.9f} to {max(l):.9f} | {delta('peak_import_kw')[0]:.9f} | {delta('min_voltage_pu')[0]:.9f} |")
lines += ['',
'''The hourly-to-five-minute loss difference has magnitude 0.028302–0.033119 kWh, whereas the 15-minute-to-five-minute difference is 0.001577–0.001841 kWh. Hourly sampling makes the minimum voltage appear 0.000294983 pu higher and peak current ratio 0.022340481 lower. Despite these differences, every baseline exceeds the declared root-branch current limit at every resolution. No feasibility reversal is observed in this design. A boundary-case claim would require a separately preregistered limit/loading experiment.

## Original four-policy example

This table is one seed-17, 96-interval day at default tolerance 1e-10. It is not a cross-seed policy-effect estimate.
''',
'| Policy | State | Current ratio maximum | Peak import, kW | Network loss, kWh | Storage conversion loss, kWh | Total loss, kWh |',
'|---|---|---:|---:|---:|---:|---:|']
for x in [x for x in d if x['group']=='original']:
    m=x['metrics']
    lines.append(f"| {x['policy']} | {x['state']} | {m['max_loading']:.6f} | {m['peak_import_kw']:.6f} | {m['network_loss_kwh']:.6f} | {m['storage_loss_kwh']:.6f} | {m['total_loss_kwh']:.6f} |")
lines += ['',
'''Baseline and tap violate only the root-branch current limit (six and four intervals respectively). Storage and combined satisfy the declared limits and terminal energy neutrality; storage reduces network losses while adding 3.12 kWh conversion loss. The packaged ranking remains empty for the entire study because the baseline is infeasible. This is the documented admission rule, not a missing result or evidence for policy superiority. The original synthetic default is therefore useful for studying an infeasible baseline and candidate feasibility, but cannot support a feasible-baseline loss ranking without a separately declared changed case.

## Evidence, unsuccessful outcomes, and release bridge
''',
f"The initial outcomes are {states['COMPLETED_VALID']} `COMPLETED_VALID`, {states['COMPLETED_INFEASIBLE']} `COMPLETED_INFEASIBLE`, {states['INVALID_RESULT']} `INVALID_RESULT` and {states['FAILED_SOLVER']} `FAILED_SOLVER`. No numerical invalidity or infeasibility is dropped. Every one of the 52 original study bundles passed packaged `lab verify`; verification establishes integrity and faithful evaluation, not feasibility. CLI exit code 0 denotes a recorded study, including the expected failed-solver study, rather than solver success for every policy.", '',
'''All primary results were produced by `python3 releases/1.0.0rc1/grid-horizons.pyz lab ...`. A two-case campaign supplied the first two baseline cases; remaining cases used `lab run`. The original four-policy input was created by `lab example`. CLI stdout/stderr, exact arguments, return codes and timings are retained for all 105 initial calls. No alternate producer was run.

Before preregistration the root disclosed an rc1 input-decoder 1 MiB ceiling inconsistent with the documented larger limit. This study therefore chose bounded per-case calls and a small campaign; it did not attempt or claim to reproduce a large-campaign failure. The limitation did not prevent the planned scientific comparisons. It is a workflow limitation reported by the root, not a locally observed rejected attempt.

After initial confirmation, rc2 was supplied with fixes to input-size handling, help and graph scaling. A separate [bridge preregistration](bridge-rc2-001/preregistration.json) was frozen before rerunning the saved original four-policy input. Both `ac.py` and `ac_check.py` are byte-identical between rc1 and rc2. All four complete policy records, including raw trajectories and evaluations, compare exactly equal; rc2 `lab verify` passes. This adds one scenario and four policy combinations, bringing the entire study to 53 scenarios / 59 combinations. It supports numerical continuity for the tested original case; it is not an exhaustive equivalence proof for every release feature.

## Reproduction, identity, and measured cost
''',
f"Actual investigator model was checked in runtime turn context: `gpt-6-astra`, high effort. Packaged runtime: Linux x86_64, CPython {cost['runtime_identity']['python']}, model `balanced-radial-pq/v2`. The original implementation hash is `{plan['implementation_sha256']}`; zipapp SHA-256 is `{plan['package_sha256']}`. The package records source revision `3d4a4dc7718d72e0d20785c70154c800cc849093` with preserved uncommitted implementation, so the implementation hash—not that commit alone—is the identity. Runtime executable SHA-256, full Python/platform descriptions and frozen-source identity are recorded in the preregistration and manifests.", '',
f"Initial work used {cost['cpu_seconds']:.3f} CPU seconds and {cost['wall_seconds']:.3f} wall seconds; independent Newton consumed {cost['reference_cpu_seconds']:.3f} CPU seconds and packaged CLI child calls consumed {cost['cli_cpu_seconds']:.3f} CPU seconds. The bridge added {bridge['cpu_seconds']:.3f} CPU seconds. Measured experiment CPU totals {cost['cpu_seconds']+bridge['cpu_seconds']:.3f} seconds, well below the 300-second ceiling. Execution used one CPU child at a time and no paid resources. The initial artifact tree occupied {cost['output_bytes_before_hash_manifest']:,} bytes before its final cost/hash manifests. These are one-run measurements on the current host, not portable speed or price estimates; final report-writing/tool orchestration time is not included in solver experiment cost.", '',
'''Run from the project directory, using fresh output paths:

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
''']
(HERE/'report.md').write_text('\n'.join(lines))
print(json.dumps({'states':states,'tight_maxima':maxerr,'report_bytes':(HERE/'report.md').stat().st_size},indent=2))

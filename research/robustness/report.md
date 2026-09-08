# Fixed schedules under profile and electrical-limit perturbations

**Engineering robustness study, 8 September 2026.** No tested policy remained
feasible across the 48 predeclared synthetic scenarios. Fixed storage improved
feasibility and peak import, but conversion losses outweighed its network-loss
savings. A three-hour load delay eliminated its peak reduction. Separately selected
policies also lost feasibility under the predeclared timing and compound stresses.

## Scope and method

This study uses the locally packaged release-candidate Grid Horizons CLI, a 13-bus original synthetic
feeder, and 96 quarter-hour intervals per day. The frozen design was recorded in
[preregistration.md](preregistration.md) before confirmation outputs, followed by
a separately declared [transfer appendix](appendix-preregistration.md). The actual
investigator runtime was verified as GPT-6 Astra, high, and recorded in
[runtime-identity.json](runtime-identity.json). Source files were read only. Directory
discipline and package hashes provide workflow separation; there is no OS sandbox
or claim of independent human investigation.

The producer uses balanced constant-PQ loads, a complex backward/forward current
sweep, series impedance losses, an ideal source tap and one storage device. Radial
current-summation methods provide the methodological context, rather than external
validation of this implementation. [MATPOWER manual §4.3.2](https://matpower.app/manual/matpower/DistributionPowerFlow.html).
Complex branch power balances are consistent with the branch-flow modeling
framework; this experiment does not solve an optimal power flow problem or establish
optimality. [Farivar and Low, Branch Flow Model](https://arxiv.org/abs/1204.4865).
Storage accounting includes charging/discharging efficiencies and a terminal energy
constraint, concepts also documented in [PyPSA's storage equations](https://docs.pypsa.org/latest/user-guide/optimization/storage/).

Four held-out cloud-profile seeds, 101/103/107/109, were crossed with 12 treatments:
nominal; load/reactive scale 0.8 or 1.2; solar scale 0.7 or 1.3; load timing −3 or
+3 hours; solar timing −2 or +2 hours; resistance ×1.5; current limits ×0.8; and a
joint case combining load ×1.2, solar ×0.7, load +3 h, solar −2 h, resistance ×1.5,
and current limits ×0.8. Shifts are circular within the periodic daily profile.
The seed changes solar cloud factors, not feeder topology or the common load shape.
These are finite deterministic sensitivity cases, not sampled physical feeders or
a calibrated error distribution. Scaling and timing relative to a fixed schedule
are proxies for forecast mismatch; resistance and ampacity factors are admitted
assumptions, not temperature or equipment degradation models.

The four fixed policies were idle/zero tap; storage charging 8 kW at 10–14 h and
discharging 7.22 kW at 17–21 h; a constant +2 source tap (1.0125 pu); and both.
Storage is 80 kWh, initially 40 kWh, with 20 kW power rating and 95% efficiency in
each direction. No policy was tuned, clipped or repaired after held-out outcomes.

Primary effects are idle total loss minus policy total loss, including network and
storage conversion losses, in kWh/24 h. Secondary effects are idle peak import minus
policy peak import, in kW. Positive is improvement. The predeclared practical
thresholds were 0.5 kWh/day loss saving and 1 kW peak reduction; these have no claimed
economic or utility significance. Rankings require both baseline and candidate
feasibility. All infeasible results remain in the evidence.

## Main results: feasibility comes first

Every cell below is the number of feasible trajectories out of four cloud seeds.
All other trajectories completed with current-limit violations. There were no
numerically invalid results, solver failures, voltage violations or storage violations.

| Treatment | Idle | Storage | Tap +2 | Combined |
|---|---:|---:|---:|---:|
| Nominal | 0 | 4 | 0 | 4 |
| Load ×0.8 | 4 | 4 | 4 | 4 |
| Load ×1.2 | 0 | 0 | 0 | 0 |
| Solar ×0.7 | 0 | 4 | 0 | 4 |
| Solar ×1.3 | 0 | 4 | 0 | 4 |
| Load −3 h | 4 | 4 | 4 | 4 |
| Load +3 h | 0 | 0 | 0 | 0 |
| Solar −2 h | 0 | 4 | 0 | 4 |
| Solar +2 h | 4 | 4 | 4 | 4 |
| Resistance ×1.5 | 0 | 4 | 0 | 4 |
| Current limits ×0.8 | 0 | 0 | 0 | 0 |
| Joint adverse | 0 | 0 | 0 | 0 |
| **Total /48** | **12** | **32** | **12** | **32** |

Thus the universal-feasibility criterion is falsified for every policy. Storage
and combined operation were feasible in 20 cases where idle was infeasible, but
those cases do not enter the package's loss ranking. All policies were jointly
feasible in only 12 cases: reduced load, earlier load and later solar.

| Policy | Total-loss saving in 12 jointly feasible cases, kWh/day | Relative loss saving | Peak reduction, kW | Cases meeting loss / peak practical thresholds |
|---|---:|---:|---:|---:|
| Storage | −2.530 to −2.273 | −39.46% to −35.19% | 5.651 to 7.360 | 0 / 12 |
| Tap +2 | +0.146 to +0.177 | +2.458% to +2.475% | 0.013 to 0.021 | 0 / 0 |
| Combined | −2.372 to −2.142 | −37.23% to −32.92% | 5.662 to 7.377 | 0 / 12 |

Storage's peak reduction is 8.40–10.08% in those 12 cases; combined achieves
8.42–10.10%. Tap improves loss in all 12 eligible cases, but neither its loss nor
peak effect reaches the predeclared practical threshold. Storage and combined
raise total loss in all 12; feasibility improvement and peak reduction do not
establish an energy-loss benefit.

Across **all 48 cases**, including infeasible diagnostic results, storage reduces
network loss by 0.428–1.368 kWh/day. Its fixed conversion loss is 3.120 kWh/day,
reversing the apparent network-only benefit into a total-loss increase of
1.752–2.692 kWh/day. Combined increases total loss by 1.496–2.380 kWh/day. Tap saves
0.146–0.355 kWh/day across the full set, always below 0.5. These signed ranges
describe the model outputs and are not feasibility-qualified rankings.

The timing sensitivity is operationally substantial: a +3 h load delay leaves the
peak after the fixed discharge window. Storage peak saving drops from 7.378 kW
in nominal cases to exactly zero for every seed in both the delayed-load and
joint-adverse cases. Combined retains only the small source-tap effect. Resistance
×1.5 alone does not destroy storage feasibility here; the 20% ampacity derating
does. This is sensitivity to independently changed assumptions, not a thermal
causal model. The invariant nominal peak across seeds is expected because the
peak occurs outside solar production; cloud seeds are not independent peak-load
observations.

For absolute scale, idle daily losses span 5.921–14.056 kWh and peak import
66.724–110.452 kW. Storage losses span 8.236–16.740 kWh and peaks
60.591–110.452 kW. Across every main trajectory, minimum-voltage metrics are
0.97605–1.00346 pu, maximum-voltage metrics 1.00262–1.02648 pu, and maximum
current-loading ratios 0.69418–1.58227. Only branch current limits bind.

## Transfer of separately selected schedules

The policy investigator supplied frozen selections trained only on seeds 11/13
and load multipliers 0.7/0.85. The appendix tested those selections against idle
on seeds 101/103/107/109 and nominal, load +3 h, and joint-adverse conditions:
12 additional scenarios and 60 trajectories. The loss-selected schedule charges
2 kW at 10–14 h and discharges 1.805 kW at 17–21 h. The peak-selected schedule
charges 8 kW at 9–13 h and discharges 7.22 kW at 17–21 h. Their combined variants
use tap +4. Selection denotes the winner among tested active candidates in the
separate training study, not improvement over idle or an unrestricted optimum.

| Selected policy | Feasible /12 | Total-loss saving, all-case diagnostic range kWh/day | Peak saving, all-case diagnostic range kW |
|---|---:|---:|---:|
| Storage, loss selection | 0 | −0.624 to −0.521 | 0 to 1.848 |
| Combined, loss selection | 4 | −0.255 to +0.076 | 0.049 to 1.895 |
| Storage, peak selection | 4 | −2.627 to −2.260 | 0 to 7.378 |
| Combined, peak selection | 4 | −2.232 to −1.890 | 0.049 to 7.419 |

Idle is infeasible in **all 12**, so there are **zero eligible pairwise rankings**.
The three policies with four feasible cases pass only nominal conditions. The
loss-selected combined policy's nominal maximum loading is 0.99999680845:
approximately 0.000319% current headroom, not a material margin. Load +3 h raises
that ratio to 1.019449; joint stress raises it to 1.542090. Its small positive
loss-saving sign under joint stress, 0.064–0.076 kWh/day, occurs only in infeasible
cases and cannot be promoted as a usable gain. The peak-selected storage and
combined policies also fail both stresses. No appendix result justifies retuning
or a robust-policy claim.

## Numerical evidence, rejected inputs and reproducibility

Main power residuals peak at **9.33×10⁻¹¹ pu**, against a 10⁻⁷ pu acceptance limit;
absolute daily energy residuals peak at **5.10×10⁻¹⁰ kWh**, against 10⁻⁶ kWh.
Maximum terminal storage drift is **7.11×10⁻¹⁵ kWh**. Appendix residuals are no
larger. These are equation-consistency checks, not physical uncertainty estimates.
The packaged verifier independently reevaluated all 62 retained solved studies
(48 main, one main repeat, 12 appendix, one version bridge). Repeating the nominal
input reproduced policy evaluations exactly. RC1-to-RC2 bridging reproduced each
nominal policy's complete raw record and evaluation exactly; the two archives'
`ac.py` and `ac_check.py` members were byte-identical. A separate second-solver
validation is outside this investigator's work; no human independence is claimed.

All unsuccessful attempts were retained. RC1 rejected the 4,614,615-byte campaign
and all four seed shards (the first is 1,130,273 bytes) with a **1,048,576-byte JSON
limit**, despite the study reader's intended 64 MiB limit. The first harness
invocation also aborted because its size-error classifier did not recognize
“byte limit”; the error classifier was corrected, with no scenario or policy
change. Per-case packaged `lab run` generated the complete frozen main set.
RC2 accepted the predeclared 1,171,189-byte appendix campaign. This is direct
evidence for the larger-input reader repair, not a claim that every 64 MiB input
has been tested.

The retained outage control sets the source branch parent to −1. The package
rejects it with “ordered connected radial topology required; outages unsupported.”
It has no trajectory, and this study reports no outage probability, unserved
energy, islanding, restoration or reliability result.

Primary package evidence is pinned to RC1 implementation
`cdf8e0b82397cbad5e9f5979fd01d98fd931a7c772c5dcd1c8b42a35ac90a4a4`
and archive SHA-256
`57573bdb2c8bb9c983b5dcc1b0c8850ac0ae6e3c87b8e6a24d60077ca03fe2ce`.
Appendix/bridge RC2 implementation is
`3f46ec88b717c2811186fe2c4c7f2c926a37e110281c115798720bd87e143023`
and archive SHA-256
`325e14d7e3d3021555060dd4841f5e90df634238dd858c559a2c4ff7ee912c4e`.
Runtime, executable, configuration, consulted source, script and output hashes are
included in per-attempt provenance and checksum files. The frozen archive, rather
than the evolving workspace source, is the executed product authority.

Run `python research/robustness/rerun.py`, then
`PYTHONDONTWRITEBYTECODE=1 python research/robustness/appendix.py` from the project
directory. Both preserve previous attempts in new directories. The scripts use
the real packaged example/run/campaign/verify commands and never import the solver.
[findings.json](findings.json) links both complete result sets;
[all-attempt-inventory.json](all-attempt-inventory.json) records every command and
the retained unsupported input. Raw studies include policy JSON, interval data,
feasibility CSV, reports, manifests and package checksums.

There were 63 scenario executions/validation attempts, 260 produced policy
trajectories including repeats, and 24,960 solved interval records. Production
and verification ran sequentially on one CPU. Measured CPU was **12.705 seconds**
and summed measured execution wall time **12.801 seconds** across the complete
main/appendix runs plus commands from the aborted first invocation; peak child RSS
was **47,456 KiB**. These totals exclude the first aborted harness's unmeasured
orchestration overhead, authoring/research time and model inference cost. The
300-second computation budget was not approached. No measured cost is represented
as a paid-resource bill.

These results support a narrow engineering conclusion: the tested fixed schedules
have objective tradeoffs and lose feasibility under declared timing/current-limit
stress. They do not establish population reliability, an optimal controller,
field performance, hardware validation, human usability, peer review or novelty.

# Grid Horizons: three reproducible computational studies

**Prepared manuscripts and evidence, not published papers.** These studies use
one original synthetic 13-bus feeder family and the actual packaged Grid Horizons
CLI. A separate agent [reproduction review](reproduction/report.md) supports all three
studies within their stated scope. No human, hardware,
field-validation, peer-review or novelty claim is made.

| Study | What it teaches | Coverage and key observation |
|---|---|---|
| [Numerical benchmark](benchmark/report.md) | Solver convergence, equation consistency and feasibility are different checks. | 48 seed/resolution/tolerance cases plus controls and a release bridge. All 12 cases at tolerance 1e-6 fail independent residual checks. Tight-tolerance complex voltages agree with separate Newton within 9.87e-13 pu. Hourly sampling understates peak import by 1.947 kW versus five-minute sampling. |
| [Storage/tap tradeoffs](policies/report.md) | Lower line losses and peak demand can cost more total energy. | Equal eight-candidate searches per active family, then 12 held-out confirmation cases. In all eight cases with feasible baselines, selected cycling schedules increase total loss. Peak-selected schedules cut about 7.32–7.38 kW while adding about 2.01–2.37 kWh/day. |
| [Robustness and transfer](robustness/report.md) | Nominal feasibility is not robust feasibility. | 48 held-out operating cases: idle/tap feasible in 12, storage/combined in 32. A three-hour load delay eliminates storage peak reduction. Selected policies fail timing and compound stresses; no tested policy is universally feasible. |

The results are distinct benchmark, policy-selection and robustness engineering
studies. Their numerical ranges describe the chosen finite synthetic cases; they
are not population confidence intervals or estimates for a physical network.
Infeasible cases remain available as diagnostics but cannot enter benefit rankings.

Each directory contains a frozen preregistration, executable rerun script,
retained raw product outputs, all-attempt inventory, exact build/runtime identity,
independent/equation checks, feasible and unsuccessful cases, tables, costs and a
cited manuscript draft. The benchmark additionally retains independently written
nodal Newton calculations for 5,904 solved intervals. The policies study separates
exploration from confirmation; robustness applies the selected policies to new
seeds and stresses without retuning.

Reported experiment CPU totals are 22.154 seconds (benchmark), 19.304 seconds
(policy CLI) and 12.705 seconds (robustness), **54.163 measured CPU seconds** in
aggregate. Measurement scopes differ and exclude model inference, authoring,
research/tool orchestration and some disclosed aborted-driver overhead; this is
not a full project cost or a paid-resource bill. Raw artifacts occupy roughly
377 MiB before independent reproduction and final packaging.

## Reproduce

Obtain the corresponding source and research packages together; retain both
`releases/1.0.0rc1/grid-horizons.pyz` and `releases/1.0.0rc2/grid-horizons.pyz`
for the historical study identities. Run from the extracted project root:

```sh
python3 research/benchmark/rerun.py --output research/benchmark/reproduction-002
python3 research/benchmark/bridge_rc2.py --output research/benchmark/bridge-reproduction-002
python3 research/policies/rerun.py --help
python3 research/robustness/rerun.py
python3 research/robustness/appendix.py
```

The policy script exposes separate `explore`, `confirm` and `bridge` phases; follow
its report's exact commands and keep output paths fresh. Scripts deliberately
pin the historical packages and preserve prior results. The current application
candidate and reviewer bridges have their own identity; old bundles must be
verified with their original build. Study archives are versioned evidence, not
in-place migrations.

The application improved through these studies: RC1's inherited 1 MiB JSON ceiling
blocked valid campaigns and large summaries. RC2 accepts the documented bounded
reader size, with actual larger campaign and multi-policy summary checks and
byte-identical numerical bridges. A separate reviewer also found an RC2 policy
filename collision, fixed in RC3 by reserving metadata names. RC4 additionally rejects huge JSON
integers cleanly; the reviewer confirmed unchanged numerical functions and checks.
Earlier failures remain retained, rather than relabeled as successful runs.

[External and qualified review instructions](../docs/v1/REVIEW-INSTRUCTIONS.md) ·
[Model admission](../docs/v1/MODEL.md) · [Current status](../STATUS.md)

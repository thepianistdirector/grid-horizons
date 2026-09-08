# Storage dispatch can reduce feeder losses while increasing total losses

**A preregistered finite-policy study in Grid Horizons, 8 September 2026.** On eight held-out cases with feasible idle baselines, every selected active-storage policy lowered line losses and peak import but increased line-plus-storage conversion losses. Idle storage at constant tap +4 gave the lowest total loss among confirmed policies. This is a negative result for the tested active-storage schedules, not evidence against storage generally.

## Question and engineering context

Does a chronological, terminal-neutral storage schedule improve total energy loss or peak import on the same load and solar trace, and how does a discrete ideal source tap change that tradeoff? Reporting network losses alone could credit a storage schedule while omitting the energy consumed by its conversion inefficiency.

The packaged model uses a balanced radial constant-PQ feeder, complex backward/forward current summation, series impedances, and ideal slack voltage control. MATPOWER's primary documentation explains backward current accumulation and forward voltage updates for radial distribution power flow; it provides mathematical context, not an external implementation used in these trials. [MATPOWER manual §4.3.2](https://matpower.app/manual/matpower/DistributionPowerFlow.html).

Storage obeys `E_next = E + eta_c × charge × dt − discharge × dt / eta_d`. Charging and discharging efficiencies and cyclic endpoint constraints also appear in PyPSA's primary storage formulation. Here both efficiencies are 0.95 and the initial and terminal energy is 40 kWh, preventing energy borrowed from the initial state from masquerading as a benefit. No PyPSA solver was run. [PyPSA storage documentation](https://docs.pypsa.org/latest/user-guide/optimization/storage/).

The original synthetic Canopy 13 feeder contains 13 buses and 12 branches on a 100 kVA, 12.47 kV base. Every scenario covers 24 hours in 96 constant-mean quarter-hour intervals. Solar is installed at buses 4, 7, 10 and 12; storage sits at bus 7 with 80 kWh capacity and 20 kW power rating. Load multipliers are 0.7, 0.85 and 1.0; solar multiplier is 1.0. Generated load/reactive values are scaled and rounded to seven decimals. The input generator and data are original synthetic AGPL-3.0-only assets. Limits are declared synthetic study limits, not utility standards.

## Fixed design, selection and falsification

The plan in [protocol.json](protocol.json) preceded exploration. Seeds 11 and 13 were used only for exploration; seeds 41, 43, 47 and 53 were reserved for confirmation. Seeds change hourly solar cloud factors; load shape, topology and parameters remain shared. Each storage family received exactly eight candidate schedules and 48 exploratory evaluations: charging amplitudes 2, 4, 8 and 12 kW, crossed with charging windows [09:00,13:00) and [10:00,14:00). Every schedule discharges at `0.9025 × amplitude` during [17:00,21:00), then is idle outside the two windows. The storage-only family uses tap 0; combined uses constant tap +4. These are bounded schedule families, not a general dispatch or joint tap optimization.

Every case also includes idle tap 0, −2, +2 and +4 comparators. Tap voltage is `1 + 0.00625 × tap`; all choices are discrete and held constant over the day. Within each scenario all policies see identical chronological profiles. The initial demonstration retains the packaged seed-17 example and its original four policies.

Selection uses the mean objective across the four exploratory seed × load 0.7/0.85 cases, requiring feasibility in all four. Load 1.0 was excluded before selection because its baseline is infeasible. Each family has a separately chosen total-loss winner and peak-import winner; ties use lexical policy ID. No combined scalar score or post-confirmation selection is used. The [selection record](selection.json) retains scores and feasibility for all candidates.

| Frozen policy | Charge window | Charge kW | Discharge kW | Tap | Selection objective |
|---|---|---:|---:|---:|---|
| storage_loss | 10–14 h | 2 | 1.805 | 0 | Total loss |
| combined_loss | 10–14 h | 2 | 1.805 | +4 | Total loss |
| storage_peak | 9–13 h | 8 | 7.22 | 0 | Peak import |
| combined_peak | 9–13 h | 8 | 7.22 | +4 | Peak import |

The peak objective ties across the two charging windows because both share evening dispatch; the lexical rule selects 9–13 h. The loss winner is the best *active candidate in its family*, not the best overall comparator. Idle controls remain eligible for final ranking. Twelve-kW schedules reach 85.6 kWh and violate the 80 kWh capacity; their apparently lower peak cannot rank.

The timestamped [preregistration](preregistration.json), including primary sources, fixed comparators, budgets, seeds, falsifiers and selected parameters, was saved before confirmation. [confirmation-start.json](confirmation-start.json) binds its hash. A total-loss benefit claim fails if any comparable confirmation case has loss greater than or equal to its baseline. Invalid residuals, nonconvergence, SOC mismatch or physical-limit violations disqualify a policy; infeasible baselines suppress the entire scenario's ranking. The stopping rule was 25 primary scenarios with no adaptive additions. An explicitly authorized 13-scenario release-compatibility bridge followed; it changes no selection or inference.

## Held-out results

All 64 policy trajectories on the eight baseline-feasible confirmation cases were feasible. The table gives minimum and maximum **paired policy-minus-baseline** differences over the four solar seeds at each load scale. Negative values are improvements for the stated metric. These ranges describe the finite observed panel; they are not confidence intervals, significance tests or population uncertainty estimates.

| Load scale | Policy | Δ line loss (kWh) | Δ total loss (kWh) | Δ peak import (kW) |
|---|---|---:|---:|---:|
| 0.7 | tap_m2 | +0.1424 to +0.1449 | +0.1424 to +0.1449 | +0.0126 to +0.0126 |
| 0.7 | tap_p2 | -0.1395 to -0.1372 | -0.1395 to -0.1372 | -0.0121 to -0.0121 |
| 0.7 | tap_p4 | -0.2740 to -0.2694 | -0.2740 to -0.2694 | -0.0238 to -0.0238 |
| 0.7 | storage_loss | -0.2388 to -0.2329 | +0.5412 to +0.5471 | -1.8345 to -1.8345 |
| 0.7 | combined_loss | -0.5014 to -0.4911 | +0.2786 to +0.2889 | -1.8568 to -1.8568 |
| 0.7 | storage_peak | -0.7948 to -0.7530 | +2.3252 to +2.3670 | -7.3232 to -7.3232 |
| 0.7 | combined_peak | -1.0306 to -0.9896 | +2.0894 to +2.1304 | -7.3419 to -7.3419 |
| 0.85 | tap_m2 | +0.1657 to +0.1679 | +0.1657 to +0.1679 | +0.0187 to +0.0187 |
| 0.85 | tap_p2 | -0.1617 to -0.1596 | -0.1617 to -0.1596 | -0.0180 to -0.0180 |
| 0.85 | tap_p4 | -0.3175 to -0.3134 | -0.3175 to -0.3134 | -0.0353 to -0.0353 |
| 0.85 | storage_loss | -0.2504 to -0.2444 | +0.5296 to +0.5356 | -1.8413 to -1.8413 |
| 0.85 | combined_loss | -0.5558 to -0.5460 | +0.2242 to +0.2340 | -1.8748 to -1.8748 |
| 0.85 | storage_peak | -0.8367 to -0.7947 | +2.2833 to +2.3253 | -7.3502 to -7.3502 |
| 0.85 | combined_peak | -1.1138 to -1.0732 | +2.0062 to +2.0468 | -7.3791 to -7.3791 |

Baseline line/total loss ranged from 5.6031–5.7012 kWh at load 0.7 and 6.4790–6.5662 kWh at load 0.85. Baseline peaks were 63.6351 and 77.4002 kW respectively. The identical peak differences across seeds arise because the shared evening demand peak occurs outside solar hours; four solar seeds do not provide four independent tests of peak-demand variability.

The 2 kW schedules incur exactly 0.78 kWh conversion loss per day and the 8 kW schedules incur 3.12 kWh. Their line-loss savings are smaller. Thus the predeclared active-storage total-loss benefit fails on all eight comparable cases, even for the combined loss winner. The peak winners save about 7.32–7.38 kW of peak import while increasing total loss by about 2.01–2.37 kWh. These two objectives disagree in this panel.

Tap +4 with idle storage saves 0.2694–0.3175 kWh versus the zero-tap baseline, with only 0.0238–0.0353 kW peak reduction. Higher ideal voltage reduces current for the model's constant-PQ demand. This limited mechanism does not price transformer losses, tap switching, wear, or voltage-dependent real loads; it cannot establish that maximum tap is a field-optimal setting.

## Feasibility, retained failures and verification

The default seed-17 baseline is **infeasible**: maximum branch-current loading is 1.045543, while bus voltage stays within the configured limits. The packaged storage and combined candidates become feasible, but the CLI correctly leaves the entire ranking empty. All four load-1.0 confirmation baselines also violate current limits and are excluded from performance ranking. At that load, `storage_loss` and the three idle tap policies remain infeasible; `storage_peak`, `combined_peak` and `combined_loss` become feasible. This is a recorded feasibility change, not a ranked baseline improvement. `combined_loss` has maximum current loading 0.9999968084: almost no margin, despite passing the numerical allowance. No physical robustness claim follows.

Across the 25 primary scenarios, 244 policy trajectories comprise 174 completed-valid and 70 completed-infeasible outcomes. None failed to converge or produced invalid numerical results. The largest evaluated nodal power residual is 6.21e-11 pu and absolute energy-ledger residual is 8.13e-11 kWh, below the fixed 1e-7 pu and 1e-6 kWh evaluation tolerances. The evaluator reconstructs currents from Ohm's law and checks voltage, branch current, storage power, SOC, terminal neutrality and energy balance. Passing this in-package independent equation evaluator is not an independent external solver validation.

[all-scenario-feasibility.csv](all-scenario-feasibility.csv) includes every trajectory, metrics, SOC extrema, dispatch power, violations and ranking eligibility. Raw per-interval complex voltages, source power, iterations and storage transitions remain in every policy JSON. The companion summaries retain per-bus voltage magnitudes and per-branch loading ratios. [all-attempts.json](all-attempts.json) lists every completed scenario, including bridges; [all-command-attempts.csv](all-command-attempts.csv) and [commands](commands/) preserve every CLI attempt, including failures.

Two failure categories are retained. An initial investigator setup error omitted the input directory: two `lab example` calls and one `lab run` failed before any scenario executed. Creating that directory resolved the harness error. Separately, all 12 rc1 exploratory `lab verify` calls rejected the product's own summaries because they exceeded the legacy 1 MiB JSON decoder cap; the first summary was 1,452,225 bytes. The runs themselves completed. This product defect was reported immediately, with expected/actual behavior and a direct reproduction command. No failed evidence was overwritten or presented as a successful verification.

The root supplied rc2 with a larger reader limit and unchanged solver/evaluator. Thirteen additional full-scenario CLI runs reproduced all twelve exploration cases and one confirmation case under rc2. Every rc2 bundle passed `lab verify`; every policy's complete raw-and-evaluation JSON file is byte-identical to its rc1 counterpart. See [bridge-comparison.json](bridge-comparison.json). The original rc1 default and all 12 confirmation bundles verified successfully. The bridge demonstrates unchanged numerical evidence across these releases and repairs reopenability; it supplies no additional independent scientific samples.

## Identity, resources and reproduction

Actual investigator runtime model was checked from session turn context: **gpt-6-astra, high**; it matched the requested model. Production runs used Linux x86_64 CPython 3.12.14 through the packaged CLI. Primary package version is 1.0.0rc1, implementation SHA-256 `cdf8e0b82397cbad5e9f5979fd01d98fd931a7c772c5dcd1c8b42a35ac90a4a4`, package SHA-256 `57573bdb2c8bb9c983b5dcc1b0c8850ac0ae6e3c87b8e6a24d60077ca03fe2ce`. Bridge version is 1.0.0rc2, implementation SHA-256 `3f46ec88b717c2811186fe2c4c7f2c926a37e110281c115798720bd87e143023`, package SHA-256 `325e14d7e3d3021555060dd4841f5e90df634238dd858c559a2c4ff7ee912c4e`. [identity.json](identity.json) and [bridge-identity.json](bridge-identity.json) retain complete CLI identities. Source isolation was a read-only workflow and hash check in a shared workspace, not an OS sandbox or independent human investigation.

The complete evidence run used 38 scenarios, 396 policy trajectories and 96 intervals per scenario, below the 100-scenario/96-interval bounds. Summed measured CLI child-process CPU was 19.304 seconds and wall execution was 19.530 seconds across 77 sequential command attempts. Disk evidence measured 191,251,525 bytes before this report and final manifest; the final manifest supplies a later exact file-byte total. CPU measurement excludes browser retrieval, authoring and orchestration overhead. No simultaneous solver subprocesses were used. The 300-second CPU ceiling was not approached.

From the repository directory, choose a fresh directory inside this study's workspace and run:

```sh
python3 research/policies/rerun.py explore --output research/policies/reproduction
python3 research/policies/rerun.py confirm --output research/policies/reproduction
python3 research/policies/rerun.py bridge --output research/policies/reproduction
```

The script invokes actual `lab identity`, `example`, `run`, `campaign` and `verify`; it contains no feeder solver or scratch producer. Campaign inputs are batched in pairs to stay below rc1's input decoder cap. Stored [inputs](inputs/) and the frozen preregistration provide exact original scenarios if selection need not be repeated. Re-executing into an existing destination is unsupported: choose a new directory to preserve attempts. `analyze.py` regenerates this report and findings from the recorded evidence directory, without solving or selecting policies. Source paths `src/grid_horizons/ac.py`, `lab.py`, `ac_check.py`, and `docs/v1/CONTRACT.md`/`MODEL.md` were read to establish the model contract.

## What the study establishes

This finite synthetic panel exposes a concrete objective mismatch: lower network loss can coexist with higher total energy loss when terminal-neutral storage conversion is counted. It also shows why current feasibility must precede ranking, including a numerically feasible candidate with negligible margin. The results establish neither a universal scheduling rule nor a general storage valuation. Unbalanced operation, public feeder reproduction, voltage-dependent demand, degradation, thermal limits beyond the declared ratios, stochastic forecasts, tariffs, outages, physical uncertainty and qualified engineering review remain outside this experiment.

# ADR-001: a bounded, fictional radial tutorial for 0.1

Decision date: 2026-09-07. Implementation owner: the primary GPT-6 Astra task.
State: **selected for the owner-authorized local 0.1 implementation**. This is
an implementation decision within Lucas Santana's September 7 launch cut,
not qualified engineering approval or permission to publish.

## Evidence and authority

- **Observed:** clean `main` at `3d4a4dc7718d72e0d20785c70154c800cc849093`,
  exact project origin, no other Grid Horizons owner found in current tasks,
  no runtime or external dependencies in the starting checkout.
- **Observed:** the root runtime turn context identifies `gpt-6-astra`, OpenAI,
  high reasoning. The native Goal belongs to task
  `01a07e1c-85eb-7f73-914b-141a759e234e` and was read back ACTIVE.
- **Source requirement:** independently check quantities, completeness,
  feasibility, uncertainty, attempts and reproducibility before comparison.
- **Owner proposal selected:** an original three-node synthetic feeder,
  idle storage and one frozen storage schedule; fixed taps, no optimization.
- **Preserved requirement:** GH-001's lawful public feeder and GH-004's public
  reference reproduction remain later, uncompleted work. GH-005's transformer
  and GH-007's tap/storage comparison are not completed by this tutorial.
- **Unresolved:** human first-use observation, qualified interpretation of any
  engineering claim, concrete public release approval and native Tanduna
  publication approval/access. No engineering improvement is claimed.

## Purpose and alternatives

An external student can inspect a small JSON scenario, edit supported fictional
profiles/capacities/schedules, validate it, run both policies, inspect raw
trajectories and failures, and rerun a portable study. The useful result is an
auditable calculation with visible limits. It need not show a beneficial policy.

Full AC solvers would offer more physics but require dependency and reference
admission. A copper-plate energy ledger would omit the requested network
constraints. A handwritten nonlinear AC solver would add unjustified numerical
complexity. We select lossless linearized DistFlow with explicit reactive-power
balance and squared-voltage drops, plus a separate storage transition.

## Exact model and approximation

Balanced positive-sequence equivalent; rooted directed radial tree; constant
interval-mean real/reactive load; real generation and storage at unity power
factor; fixed root voltage and topology; no shunts, taps, controls or transients.
All powers represent three-phase totals. All buses share one line-to-line RMS
voltage base `V_base` and three-phase apparent-power base `S_base`.
`Z_base = V_base² / S_base`; impedance inputs are per unit on that base.

For a branch from parent `i` to child `j`, active/reactive flow is positive
toward the child. Nodal net consumption is positive:

```text
p_j = load_j - generation_injected_j + charge_j - discharge_j       [W]
q_j = reactive_load_j                                             [var]
P_ij = p_j + sum(P_jk)                                             [W]
Q_ij = q_j + sum(Q_jk)                                             [var]
u_j = u_i - 2 (r_ij P_ij / S_base + x_ij Q_ij / S_base)           [pu²]
V_j = sqrt(u_j)                                                    [pu]
loading_ij = hypot(P_ij, Q_ij) / rating_ij                           [1]
```

`u` is squared normalized voltage, not voltage magnitude. This approximation
drops the current-squared terms in both power balance and voltage drop.
Resistance still affects the first-order voltage drop; it does not supply a
computed dissipative line-loss term. Network loss, current/ampacity, thermal
behavior, protection and full AC feasibility are **NOT EVALUATED**. In the
lossless model's energy identity, the network-loss term is assumed zero;
reports must never describe that as measured zero physical loss.

`loading` is apparent-power/rating, not conductor temperature or ampacity.
The model's fixed demonstration band is 0.90–1.10 pu voltage magnitude.
Crossing this band is an explicit model-domain violation; it establishes no
accuracy within the band. Tighter fictional scenario limits are separate.
No error bound relative to AC or real-network behavior has been established.

Reference: the loss-term omission is described in §2.3.2 of Christianen et al.,
[Comparison of stability regions…](https://link.springer.com/article/10.1007/s11134-023-09873-z)
(2023). The general real/reactive branch equations are also shown in
[Equilibrium and Dynamics of Local Voltage Control in Distribution Systems](https://smart.caltech.edu/papers/equilibrium.pdf),
§II. These references support the mathematical family, not this fixture's
limits, accuracy or engineering applicability. No paper or feeder data is
redistributed in the product.

## Storage and separate ledgers

Each interval is half-open `[start_s, end_s)`, relative to the fictional study
origin. Profiles and the predeclared schedule are constant interval means.
`dt = end_s - start_s` is actual elapsed seconds, never a sample weight.
The signed schedule is positive for charging from the AC bus.

```text
charge = max(schedule, 0)                                         [W]
discharge = max(-schedule, 0)                                     [W]
E_end = E_start + eta_charge charge dt - discharge dt / eta_discharge [J]
storage_loss = (1-eta_charge) charge dt + (1/eta_discharge-1) discharge dt [J]
generation_injected = generation_available - curtailment            [W]
E_start + import + generation_injected_energy
  = E_end + export + served_load_energy + storage_loss               [J]
```

Standing loss and electrochemical/thermal/degradation behavior are omitted.
Charge is not tracked in coulombs: **NOT EVALUATED**, not inferred from energy.
Reactive power remains a separate interval var balance and is never added to
real energy. Curtailed potential never crossed the electrical boundary and
is excluded from the electrical balance. Served plus unserved demand must
equal requested demand. The built-in policy has no load-shedding permission.

The storage transition has the same efficiency direction as the
[PyPSA 1.2.0 storage-unit consistency equation](https://docs.pypsa.org/v1.2.0/user-guide/optimization/storage/).
PyPSA is a reference only and is not installed, copied or executed.

## Fictional case and known answers fixed before the kernel

Three buses: `grid → orchard → workshop`. Four one-hour intervals. Bases:
100,000 VA and 400 V line-to-line. Branch per-unit `(r,x)` pairs are
`(0.015,0.010)` and `(0.020,0.010)`; apparent ratings 60,000 VA and 40,000 VA.
The fictional voltage limit is 0.97–1.03 pu. These values are original tutorial
parameters, not inferred utility standards or equipment ratings.

| Input, W | Interval 0 | Interval 1 | Interval 2 | Interval 3 |
| --- | ---: | ---: | ---: | ---: |
| Orchard load | 18000 | 22000 | 32000 | 24000 |
| Workshop load | 14000 | 16000 | 30000 | 18000 |
| Workshop generation available | 0 | 50000 | 8000 | 0 |
| Workshop curtailment | 0 | 2000 | 0 | 0 |
| Idle schedule | 0 | 0 | 0 | 0 |
| Candidate schedule | 0 | 10000 | -8100 | 0 |

Each load's reactive demand is 20% of its real demand, in var. Storage has
72,000,000 J capacity, 36,000,000 J initial energy, 12,000 W charge/discharge
limits and 0.9 efficiency in each direction. Final energy must equal initial
energy; violations remain visible, never repaired by clipping dispatch.

Hand-derived expectations (not producer-generated references):

- No-load case: all flows zero; every squared voltage equals the root value.
- Two-node control: 10,000 W + 2,000 var, `r=0.01`, `x=0.02`,
  `S_base=100000 VA`, `u_root=1`: `u_child=0.9972`; one hour serves
  36,000,000 J of real energy. Reactive power is 2,000 var, not 7,200,000 J.
- Storage control: charge 10,000 W for one hour at 0.9 efficiency adds
  32,400,000 J; discharge 8,100 W for one hour at 0.9 removes exactly that.
  Total modeled storage conversion loss is 6,840,000 J = 1.9 kWh.
- Full-case baseline import is 128 kWh, export 10 kWh and peak import 54 kW.
  Candidate import is 119.9 kWh, export zero and peak import 45.9 kW.
  Each serves 174 kWh; actual generation is 56 kWh; curtailed potential 2 kWh.
  Net imported energy rises from 118 to 119.9 kWh because of storage losses.

Numerical residual tolerance is `1e-6 + 1e-11 * scale` in W/var/J, where scale
is the sum of absolute terms in the tested identity. Squared-voltage tolerance
is `1e-10`. Values are bounded by the schema; these allowances exceed binary64
roundoff accumulated through the small bounded tree/timeline, yet reject the
predeclared perturbations. They are code consistency tolerances, not permitted
physical violations or approximation-error bounds. Known answers use stricter
case-specific tolerances and decimal/rational independently derived references.
Feasibility comparisons use only roundoff allowances at the stated boundary.

For voltage constraints compare squared values with an absolute `1e-10 pu²`
allowance. For a scalar power/apparent-power/energy limit `L`, allow only
`1e-6 + 1e-11 * (abs(value) + abs(L))` in its own unit (W, VA or J).
Initial/final equality uses that same two-term J allowance. Model-domain
voltage limits use the squared-voltage allowance too. These are explicit
numeric boundary semantics; they are not uncertainty intervals.

The following falsifiers are fixed before implementation. They exercise
separate gates; constraints are never loosened to make a mutant pass.

| Mutation or control | Required outcome |
| --- | --- |
| Change a load unit W to kW without an admitted conversion | REJECTED_INPUT |
| Make a branch point to missing node `ghost` | REJECTED_INPUT |
| Negative capacity, or initial energy above capacity | REJECTED_INPUT |
| Shorten one profile, overlap intervals, or duplicate an interval ID | REJECTED_INPUT |
| Remove one interval, node, branch or required quantity from raw output | INVALID_RESULT |
| Add 1 W to one raw branch flow | INVALID_RESULT; local nodal balance exposes the defect |
| Add 1 var to one raw reactive branch flow | INVALID_RESULT; the separate reactive balance fails |
| Change raw squared voltage by 0.0001 pu² | INVALID_RESULT; the branch voltage-drop equation fails |
| Add 3600 J to one raw storage end state | INVALID_RESULT; storage transition/continuity exposes the defect |
| Recompute a balanced trajectory using a different storage schedule | INVALID_RESULT; raw dispatch is bound to the immutable declared policy, independently of equation consistency |
| Extend a raw interval by 1 s without changing the scenario | INVALID_RESULT; exact interval identity/support fails |
| Count curtailed potential as actual generation, or subtract it twice | INVALID_RESULT; injection identity/system balance fails |
| Alter served load without matching the declared requested service | INVALID_RESULT; no hidden demand reduction is allowed |
| Lower first branch rating to 50000 VA | Baseline COMPLETED_INFEASIBLE; candidate's own feasibility still checked |
| Raise voltage minimum to 0.99 pu | Baseline COMPLETED_INFEASIBLE; exact squared-voltage limit violation retained |
| Reduce capacity to 40000000 J, keeping valid 36000000 J initial state | Candidate COMPLETED_INFEASIBLE; no SOC clipping |
| Set candidate charge to 12001 W with unchanged 12000 W limit | Candidate COMPLETED_INFEASIBLE, including final-state violation if present |
| Change a reference two-node squared voltage by 0.0001 pu² | Known-answer check fails (case tolerance 1e-12 pu²) |
| Charge/discharge control differs by 1 J from its reference | Known-answer check fails (case tolerance 1e-6 J) |

Property checks additionally exercise nonuniform intervals, reverse flow,
zero load/generation, lossless storage efficiency, node ordering and finite
output bounds. Independent critics are agent checks, not human engineering
review. The first critic independently reproduced the complete stated vector
using rational arithmetic and requested the explicit allowances/falsifiers
above; no change to the physical approximation or reference totals resulted.

## Contracts and ownership

Use `src/grid_horizons/` as one small Python package. `contracts` owns strict
closed schemas; `kernel` owns tree accumulation and storage transitions;
`evaluator` checks incidence/node/voltage/storage equations from raw records
without calling the kernel. Reports use evaluator-owned quantities only.
Every physical value carries a unit, basis, sign, location and time support;
profile arrays bind to the declared ordered interval list. No unit conversion
is guessed from magnitude or a field label. JSON rejects duplicate keys,
nonfinite numbers, booleans as quantities, unknown execution fields and
unsupported versions. Scenario identity is its canonical SHA-256 digest.

The coordinator binds scenario/model/kernel/evaluator/runtime identities in
immutable manifests, creates unique attempts and publishes terminal results
atomically. A single-writer OS file lock protects study reconciliation.
Interrupted attempts remain CANCELLED/LOST/RESOURCE_EXHAUSTED as appropriate;
explicit resume creates new attempts and preserves old evidence. A completed
result is never overwritten. Missing output is INVALID_RESULT, an internal
checker error FAILED_EVALUATOR, and a numerical execution error FAILED_SOLVER.

Only trusted built-ins and declarative original synthetic JSON are accepted.
There is no plugin, arbitrary-code, live-grid, network or credentials API.
This is not an OS sandbox or protected-confirmation claim. Runtime resource
caps are explicitly labeled as cooperative or measured. Input size, node,
interval and output bounds keep the default case CPU-feasible.

## Runtime, costs, compatibility and rollback

Reuse the existing CPython 3.12.14 runtime on Linux x86_64. No third-party
production package, solver or toolchain is adopted or installed. The exact
runtime observed is evidence for this host only; release support waits for
actual packaged checks. Source is AGPL-3.0-only, including original fixtures;
the installed interpreter is external and is not bundled. Runtime source and
license reference: [Python 3.12.14](https://www.python.org/downloads/release/python-31214/).

Distribute a stdlib zip application plus corresponding source after approval.
One short CPU job at a time; no services, ports, paid accounts or GPU.
Initial hard structural limits: 16 buses, 96 intervals, 24-hour horizon,
1 MiB scenario input. Measure actual time, RSS and artifact bytes on the
candidate rather than advertising a universal hardware envelope.

Schema/model changes require a new version; old study manifests remain
immutable. Replacing the kernel requires known-answer, mutation and paired
comparison revalidation. Rolling back selects the previous packaged version
and reruns in a fresh directory; it never edits a prior result.

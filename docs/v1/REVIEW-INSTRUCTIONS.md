# External first-use and qualified review packet

State: prepared instructions, no participants contacted, no human results claimed.
Owner's September 8 mandate retains real human/qualified-review gates; agent
reproduction supplies process separation only. Public release requires approval.

## Supported-environment first-use

One person outside this development environment with Linux x86_64 and CPython
3.12 is sufficient for an initial usability observation, not a population study.
Obtain the exact candidate package and its SHA256SUMS from the owner-approved
private handoff or later authorized public destination. Record OS, Python and
browser versions, artifact hash, date and participant role with their consent.
No private credentials or grid data are needed.

1. Follow README.md's four first-run commands without undocumented developer help.
2. Open the report, identify why the baseline is infeasible, switch policy and
   interval using the keyboard, and locate storage loss versus network loss.
3. Change a supported load/profile value in a copied scenario, validate it, run
   in a new directory and explain the changed result with its limits.
4. Export, reopen and rerun the study; compare raw trajectories and hashes.
5. Trigger cancellation and resume into a new attempt. Confirm original evidence
   remains. Corrupt a copied file and confirm verification rejects it.
6. Record completion, confusion, errors, interventions, elapsed time and exact
   screenshots/logs. A failed step remains a defect or unmet gate.

Acceptance: the participant completes each supported operation and correctly
identifies numerical validity, model feasibility and limits without unrecorded
intervention. Report observed difficulties; do not turn one observer into a
usability rate or general accessibility claim. Screen-reader testing is a
separate requested contribution, not an implied completed test.

## Qualified model-interpretation review

One reviewer with distribution power-flow expertise should inspect MODEL.md,
scenario/provenance definitions, the independent benchmark, loss accounting,
state/feasibility semantics, policy-selection protocol and robustness report.
They should check:

- Three-phase bases and units, branch equations and numerical tolerances.
- Whether benchmark checks support the stated computational claims and limits.
- Tap boundary-condition interpretation, storage neutrality and omitted physics.
- Feasibility-first selection, rejected attempts, held-out scenarios and absence
  of claims about physical control, hardware validation or lifecycle benefits.

Acceptance: a written, attributable, scoped review identifying accepted claims,
required corrections and remaining limits. An agent report cannot substitute for
this. There is no certification request, field-control action, hardware build or
paid consultation authorization. The owner must identify/authorize the real
reviewer and any contact before outreach.

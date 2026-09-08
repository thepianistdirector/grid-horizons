# Grid Horizons

An offline, bounded energy-system simulation laboratory. Run a synthetic feeder
day, compare storage and ideal source-tap schedules, inspect constraints and
energy costs, and share a complete reproducible study.

**Current delivery: owner-approved 1.0.0rc4 public release candidate.**
[Release and complete study downloads](https://github.com/thepianistdirector/grid-horizons/releases/tag/v1.0.0rc4).
Public upload/readback is recorded in STATUS.md; actual external/qualified review remains pending. This is computational evidence for declared synthetic models,
not validated real-grid operation. [Current status](STATUS.md) ·
[Model and limitations](docs/v1/MODEL.md) · [Research](research/README.md) ·
[Tanduna project](https://tanduna.com/projects/grid-horizons).

## First run

Supported: **Linux x86_64, CPython 3.12**. Runtime validation uses Python 3.12.14.
No pip packages, accounts, credentials, internet, containers, or installation
are required after obtaining the package. An HTML/JavaScript browser opens the
offline report; Chromium is the tested browser, with exact version in QA evidence.
Windows, macOS, other Python versions, screen readers, and physical devices are
not verified. The package explicitly rejects unsupported Python/platform versions.

From a release-candidate directory containing `grid-horizons.pyz`:

```sh
python3 grid-horizons.pyz lab example --output canopy.json
python3 grid-horizons.pyz lab validate canopy.json
python3 grid-horizons.pyz lab run canopy.json --output my-study
python3 grid-horizons.pyz lab verify my-study
```

Open `my-study/report.html` in your browser. Change the policy selector and
interval slider to inspect actual voltages, current loading, source power,
storage energy and residuals. Expand the failure disclosure for exact violations.
Tables support keyboard focus and horizontal scrolling on narrow screens.

The default case deliberately has an overloaded idle baseline. Storage restores
feasibility but consumes conversion energy. The report preserves both facts and
does not rank an infeasible baseline. To explore an easier case, edit each
`load_kw` and `reactive_kvar` profile value by the same factor (for example 0.8),
keep solar and policies fixed, then run into a **new** study directory. Input
validation does not establish operating feasibility.

From this source checkout, substitute `python3 grid-horizons.py` for the zipapp
command. Use `lab --help` for all commands. `--version` identifies the application;
`lab identity` identifies its exact implementation and runtime.

## Edit and compare

`canopy.json` includes every feeder branch, original load/solar profile, base,
interval duration, limit, solver option, storage parameter and policy. Units are
part of field names and fixed by schema: kW, kvar, kVA, kWh, kV, hours and pu.
Branches must form an ordered radial tree rooted at bus 0. There are 2–33 buses,
1–480 intervals totaling 24 hours, and at most 16 policies per study.

Keep the immutable `baseline` policy idle with zero taps. Policy IDs `scenario`,
`manifest`, `summary` and `checksums` are reserved for study metadata. Other policies have
`dispatch_kw` (positive charging) and integer `tap` (-4 through +4) arrays.
A tap prescribes ideal slack voltage `1 + 0.00625*tap` pu. This is a boundary
condition, not a simulated physical tap changer. Storage must finish at its
initial energy within 1e-6 kWh; dispatch and state are never clipped to hide a
violation. Efficiency losses and line losses are reported separately and together.

Default storage charges at 8 kW from 10:00–14:00 and discharges at 7.22 kW from
17:00–21:00, with 0.95 efficiency each way. Profiles are synthetic interval means,
not observations or forecasts. See the admitted equations, limits and primary
references in [MODEL.md](docs/v1/MODEL.md).

## Complete studies and campaigns

```sh
python3 grid-horizons.pyz lab export my-study --output study.zip
python3 grid-horizons.pyz lab import study.zip --output reopened
python3 grid-horizons.pyz lab rerun reopened --output reproduced
```

Keep the original zipapp with the archive. A changed implementation is rejected
on reopen; schemas do not imply scientific interchangeability between builds.
Each bundle includes input, build/runtime identity, all policy raw trajectories,
independent checks, feasibility CSV, interactive report and file hashes. Hashes
detect changes; they are not signatures or an adversarial security boundary.

Campaign specifications use `{"schema":"grid-horizons.campaign/v1","scenarios":[...]}`,
where each entry is a complete inline scenario. JSON inputs have a 64 MiB total
reader ceiling, so not every combination of the structural maxima fits one file. Run at most 120 cases sequentially:

```sh
python3 grid-horizons.pyz lab campaign campaign.json --output campaign-results
```

`inventory.json` retains every completed or rejected case and each policy state.
Study subdirectories retain the full data. Research packages include executable
campaign builders with predeclared parameter sets and rerun instructions.

## Failure and recovery

`REJECTED` means input, compatibility or integrity checks failed. Fix the described
input, preserve the rejected specification/log, and use a fresh output path.
`FAILED_SOLVER` retains the completed prefix and failed interval.
`INVALID_RESULT` means equation/energy checks failed even if the solver stopped.
`COMPLETED_INFEASIBLE` means numerically checked results violate declared limits.
The latter two cannot enter the feasible ranking. CLI `lab run` exit 0 means
**evidence was recorded**, not feasibility; inspect its `states` and `ranking`.

```sh
python3 grid-horizons.pyz lab run canopy.json --output interrupted --stop-after 5
python3 grid-horizons.pyz lab resume interrupted --output recovered
```

Resume always creates a new attempt directory and preserves the original. For a
process interrupted before final hashes exist, resume checks its saved manifest
and input against this runtime/build before rerunning. A corrupt completed study
is rejected, not silently repaired. For a campaign interrupted midstream, preserve
the original inventory/prefix and rerun its specification in a new directory;
there is no in-place campaign resume. There is no background daemon or real-grid
connection. A solver call has a fixed iteration cap; structural limits are not a
hard OS CPU/memory sandbox. Run large cases sequentially on shared machines.

## Compatibility and evidence

The original lossless tutorial remains available through `example`, `validate`,
`run`, `inspect`, `resume`, `verify`, `reconcile` and `rerun` without the `lab` prefix.
It has distinct v1 schemas and reports network losses as **not evaluated**.
New `lab` commands use AC scenario/study v2 and campaign v1. Existing study files
are never migrated in place. See [release validation](docs/v1/VALIDATION.md).

## Development and contribution

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 tools/validate_plan.py
python3 tools/render_plan.py --check
python3 tools/build_release.py
```

The builder writes a new version directory and refuses to overwrite one. For a new
release build, choose a new application version first; historical replay packages
are intentionally preserved. Its
source bundle includes the exact implementation and original assets. The Git
base may precede uncommitted development; use the implementation digest, package
hash and bundled source as identity. No public commit is implied by local builds.

Useful contributions: independently reproduce a study; add a lawful public
feeder with source observables; test first use on supported Linux; improve keyboard
and screen-reader access; or independently justify an unbalanced/thermal model.
Each model extension needs new versioned applicability, reference and failure
checks. Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [roadmap](ROADMAP.md).

Software and original synthetic fixtures: **AGPL-3.0-only**, [LICENSE](LICENSE).
No third-party runtime code, dataset, model weights or fonts are bundled.
External Python/browser runtimes retain their own licenses. [Notices](docs/v1/NOTICES.md).

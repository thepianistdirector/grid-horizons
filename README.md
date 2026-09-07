# Grid Horizons

**Simulate better grids, transformers and energy systems before proposing physical changes.**

Build an open virtual energy laboratory where agents explore efficiency, reliability and generation/storage designs against reproducible power-system and component models. Compare useful delivered energy, losses, reliability and resource cost under the same conditions rather than optimizing an isolated headline number.

Created and maintained by **Lucas Santana** ([thepianistdirector](https://github.com/thepianistdirector)). [Tanduna project](https://tanduna.com/p/grid-horizons) · [Public repository](https://github.com/thepianistdirector/grid-horizons)

> **Starting from zero.** This repository currently contains project design, architecture and a contributor plan. No simulator, application, autonomous research system or benchmark result has been implemented here. All 24 build tasks are planned. Proposed capabilities below describe what we want to build.

## Who this is for

Power-system researchers, electrical engineers, energy planners and contributors to open energy models.

## First useful experiment

Run one small public distribution-network benchmark with load and solar profiles, compare a fixed operating baseline with storage scheduling and transformer tap strategies, and reject candidates that violate voltage, loading or energy balance. Keep this entirely offline with no grid-control interface.

Software experiments make it possible to compare ideas repeatedly, inspect failures and share reproducible evidence without operating physical systems. They remain bounded by the quality and applicability of their models. A convincing visualization or agent report is not independent validation.

## What we want to build

### Distribution grid twin

Time-series power flow, feeder constraints, voltage quality, transformer loading and renewable integration using public or synthetic networks.

### Transformer design laboratory

Separate electrical-loss, thermal and eventual electromagnetic models with explicit fidelity levels. Explore cooling and design tradeoffs only within verified material and model ranges.

### Generation and storage futures

Compare known renewable, storage and conversion concepts under weather, demand, degradation and lifecycle assumptions; speculative concepts are hypotheses, never claims of new physics.

### Resilience scenarios

Outages, demand shocks, heat waves and component degradation with bounded scenario ensembles and reliability constraints.

### Agent experiment studio

Budgeted search, independent feasibility checks and shareable Pareto comparisons rather than a single opaque winner.

## Architecture in one paragraph

Use a Python coordinator with a network adapter for steady-state/time-series power flow and a separate planning optimizer. Couple transformer thermal state through a declared timestep and loss interface, not by treating a network model as an electromagnetic finite-element solver. High-fidelity component simulation is a later replaceable process adapter with its own calibration and mesh-convergence tests. All external inputs are imported snapshots. The system has no SCADA, protection-relay or real asset actuation path.

Agents propose and interpret experiments; numerical engines and protected evaluators determine results. Every experiment retains its inputs, assumptions, source version, environment, resource budget and failure state.

## Build plan

| Wave | Outcome | Gate |
| --- | --- | --- |
| 1 | Benchmark and engineering contract | The first feeder, inputs and constraints are fixed. |
| 2 | Network and component adapters | Power flow and transformer state are independently verifiable. |
| 3 | First efficiency experiment | A feeder comparison completes from input to report. |
| 4 | Reliability and uncertainty | Reported gains survive meaningful stress conditions. |
| 5 | Generation and transformer research | The lab extends beyond feeder operations with separate fidelity gates. |
| 6 | Agent-guided engineering search | Agents improve experiment coverage under fixed engineering constraints. |
| 7 | Workbench and bounded compute | Contributors can inspect and reproduce simulations. |
| 8 | Independent preview validation | The project can release a bounded research tool. |

Read the [roadmap](ROADMAP.md), [24 contributor tasks](TASKS.md), [architecture](ARCHITECTURE.md), [experiment and evaluation contract](EXPERIMENTS.md), [sources and data policy](SOURCES.md) and [current state](STATUS.md). All waves are future work; a plan is not execution authorization.

## Scientific and operating boundaries

Enforce declared units, power versus energy distinctions, passive losses and conservation. Public/synthetic infrastructure only; exclude restricted network topology, credentials, live grid controls and instructions for sabotage. Optimization cannot relax engineering limits to improve a score. Novel energy concepts must obey established conservation and include plausible parameter provenance.

If reduced-order predictions disagree with the reference beyond predeclared tolerances, repair or restrict the model before search. If a claimed efficiency gain disappears under held-out weather or load, publish that negative result. Defer high-fidelity component design until its input data and expert review exist.

## Contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md). The next eligible work is the first benchmark/contract task. Implementation follows review of exact dependency choices and a maintainer-accepted bounded task. There are no install or runtime commands yet; do not interpret proposed paths or commands as an existing application.

## Related independent projects

- [Vital Rehearsal](https://github.com/thepianistdirector/vital-rehearsal): An open simulation laboratory for physiology, disease research and safer care workflows.
- [Earth Rehearsal](https://github.com/thepianistdirector/earth-rehearsal): A software laboratory for cleaner water, less pollution and testable climate interventions.
- [Civic Safelab](https://github.com/thepianistdirector/civic-safelab): Test public-safety sensing in synthetic worlds while measuring privacy and false alarms.
- [Lean Model Lab](https://github.com/thepianistdirector/lean-model-lab): Find reproducible training and inference efficiency gains without hiding quality tradeoffs.
- [Research Continuum](https://github.com/thepianistdirector/research-continuum): A reproducible autonomous research system that turns hypotheses into independently checked experiments.

These repositories are independently buildable. Shared experiment formats are a design intention; there is no shared service or integration implemented today. Extract a common library only after two real implementations demonstrate the need.

## License

Original repository content is licensed under **AGPL-3.0-only**; see [LICENSE](LICENSE). Third-party data, models, papers and code retain their own terms and are not relicensed by this repository. No third-party dataset, model weights or upstream implementation is bundled in this initial planning release.

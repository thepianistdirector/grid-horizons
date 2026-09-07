# Contributing to Grid Horizons

Read [README.md](README.md), [STATUS.md](STATUS.md), the relevant [task](TASKS.md), [architecture](ARCHITECTURE.md) and [experiment contract](EXPERIMENTS.md). Project artifacts are in English. Lucas Santana is the maintainer and decides scope and source integration.

Choose one bounded task whose prerequisites are accepted. Before implementation, agree the actual base branch/commit, owned files, acceptance evidence, available commands and resource/permission limits. One primary owner handles a coherent change. Preserve other contributors' files and avoid speculative shared infrastructure.

The first implementation task creates the research runtime skeleton and documents its real setup/test commands. Until then, there is no simulator, numerical benchmark, application, or research experiment to run and nothing to install. The architecture foundation does include dependency-free repository-plan checks:

```sh
python3 tools/validate_plan.py
python3 -m unittest tools/test_validate_plan.py
```

These commands validate planning structure and malformed-input handling only. They do not execute or validate an energy model. Referenced engines are candidates; do not install dependencies, download model weights or datasets, or start paid experiments without the corresponding task authority and exact dependency/data review.

A contribution should contain a focused change, why it addresses the task, actual checks and failures, reproduction inputs, source/license notices and honest limitations. Unit checks prove local behavior; benchmark agreement and independent scientific interpretation require their own evidence. Never weaken a metric, tolerance, holdout or privacy boundary to make a result pass.

Enforce declared units, power versus energy distinctions, passive losses and conservation. Public/synthetic infrastructure only; exclude restricted network topology, credentials, live grid controls and instructions for sabotage. Optimization cannot relax engineering limits to improve a score. Novel energy concepts must obey established conservation and include plausible parameter provenance.

Use ordinary GitHub changes for code and documentation, and the [Tanduna project](https://tanduna.com/p/grid-horizons) for project discussion and task coordination. Submitting a contribution does not authorize automatic merge, release, deployment or real-world action. Do not post sensitive vulnerabilities, personal data or credentials publicly; contact the maintainer through an appropriate private route if needed.

Contributions of original material must be compatible with [AGPL-3.0-only](LICENSE). Keep third-party licensing and attribution intact. Cite research precisely and avoid copying paper text or datasets into the repository without the applicable rights.

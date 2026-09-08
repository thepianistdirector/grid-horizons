# GH-0.1 planning preparation packet

State: preparation artifact; implementation and public release are separate gates.

Primary owner: the Grid Horizons task, GPT-6 Astra. Bounded leaf ownership: `plan/`, `ROADMAP.md`, `TASKS.md`, `tools/validate_plan.py`, `tools/test_validate_plan.py`, `tools/render_plan.py`, `docs/lineage/`, and this packet. Preserve runtime, other owner components, siblings and shared host.

Baseline: exact source commit `3d4a4dc7718d72e0d20785c70154c800cc849093`. Source snapshot is read-only, hash-verified lineage. The canonical planning source is `plan/tasks.json`; Markdown and publication JSON are deterministic generated views. `STATUS.md` is the primary owner's evidence/handoff narrative and retains original foundation rows.

Exit acceptance: 200–400 substantive contracts with complete metadata, 20–40 outcome waves, all source contracts and original edges traced without narrowed acceptance, a separate 0.1 path, and a generated native-publication preparation export with no guessed task/wave IDs. All newly proposed rows start PLANNED. No scientific task is done because its row exists.

Actual checks, from this repository:

```sh
python3 tools/render_plan.py --check
python3 tools/validate_plan.py
python3 -m unittest tools/test_validate_plan.py
```

Tests create fixtures only under `runs/tmp` and never copy that directory recursively. Negative controls must reject malformed types, dangling/cyclic prerequisites, mutated source acceptance/history, missing mappings, inconsistent prerequisite outcomes, later-horizon dependencies, duplicate outcomes, orphan wave membership, unsupported status and generated-view drift. Original architecture/packet semantic anchors, foundation evidence and repository navigation remain checked.

Progress interface after handoff: update the relevant `plan/tasks.json` task's `status` and `evidence` list, preserve its acceptance and dependencies, then run `python3 tools/render_plan.py`. Update `STATUS.md` separately with the actual result and limits. Evidence-bearing states require named artifact references and prerequisites at sufficient evidence level. Human, runtime and public release observations must not be substituted for one another. Populate native task/wave IDs only from actual supported workflow results, then regenerate and validate views.

Immediate execution packets belong to the primary runtime owner. Stable new IDs: GH-S01–S08 model and input contracts; S09–S16 paired kernel execution; S17–S24 independent evaluation/falsifiers; S25–S32 persistence/reporting/recovery; S33–S40 packaging, external reproduction, release and native publication. Only this narrow path targets 0.1. Remaining contracts are evidence-gated later work.

Stop only the dependent action when source history cannot be recovered, an owner collision appears, the model identity differs from required Astra, or platform authorization/capability/identity is unresolved. Continue independent local preparation. This packet authorizes no publication, dependency installation, commit or shared-host change.

## Preparation verification evidence

At handoff on September 7, 2026:

- `python3 tools/validate_plan.py`: PASS, 243 tasks.
- `python3 tools/render_plan.py --check`: PASS, all generated views match.
- `python3 -m unittest tools/test_validate_plan.py`: 34 discovered tests, all PASS; final run 2.718 seconds.
- `git diff --check`: PASS.
- Canonical inventory: 28 waves, 1,016 current dependency edges; 27 source mappings preserve 71 original edges; 40 new 0.1 tasks; all 216 proposed/exploratory rows PLANNED; only GH-F01–GH-F03 DONE.

These checks cover planning/history/mirroring and negative validator behavior only. They provide no feeder/runtime, human review, external reproduction or publication evidence. The primary owner owns all subsequent runtime and release status changes.

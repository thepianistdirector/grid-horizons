#!/usr/bin/env python3
"""Validate canonical plans, generated views, immutable lineage and evidence gates.

Uses only the standard library; historical source hashes/contracts/edges are
checked independently of current generated mirrors. This is not a physics test.
"""

from __future__ import annotations

import json
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "plan" / "tasks.json"
TASKS_PATH = ROOT / "TASKS.md"
STATUS_PATH = ROOT / "STATUS.md"
TASK_ID_RE = r"GH-[A-Z0-9]+(?:-[A-Z0-9]+)*"
CURRENT_SCHEMA_VERSION = 3

FOUNDATION_CHAIN = {
    "GH-F01": (),
    "GH-F02": ("GH-F01",),
    "GH-F03": ("GH-F02",),
}
FOUNDATION_STATES = {"READY_FOR_REVIEW", "DONE"}
KNOWN_STATES = {
    "PLANNED",
    "READY_FOR_REVIEW",
    "IN_PROGRESS",
    "IMPLEMENTED",
    "AUTOMATED_PASS",
    "RUNTIME_VERIFIED",
    "USER_VALIDATED",
    "RELEASE_VERIFIED",
    "DONE",
    "BLOCKED",
    "FAILED",
    "NOT_TESTED",
}
INCOMPLETE_STATES = {
    "PLANNED",
    "READY_FOR_REVIEW",
    "IN_PROGRESS",
    "IMPLEMENTED",
    "BLOCKED",
    "FAILED",
    "NOT_TESTED",
}
REQUIRED_ARTIFACTS = (
    "README.md",
    "ARCHITECTURE.md",
    "ROADMAP.md",
    "TASKS.md",
    "EXPERIMENTS.md",
    "SOURCES.md",
    "STATUS.md",
    "docs/work-packets/GH-001.md",
    "tools/test_validate_plan.py",
)
REQUIRED_ARCHITECTURE_TERMS = (
    "## Bounded domains",
    "## Horizons and fidelity",
    "### `ScenarioSpec`",
    "### `RunManifest`",
    "### `RunResult`",
    "## Units, clocks, and conservation across solvers",
    "## Evaluation: validity, feasibility, Pareto comparison, uncertainty",
    "## Protected evaluator and agent boundary",
    "## Execution lifecycle, failure, and recovery",
    "## Local-first implementation and scale triggers",
)
REQUIRED_PACKET_TERMS = (
    "## Baseline and objective",
    "## Authority and prerequisites",
    "## Owned and protected scope",
    "## Decision procedure",
    "## Required outputs",
    "## Acceptance checks",
    "## Stop and escalation conditions",
    "## Handoff fields",
)


@dataclass(frozen=True)
class MarkdownTask:
    task_id: str
    title: str
    wave: int
    status: str
    dependencies: tuple[str, ...]
    owned_paths: tuple[str, ...]
    acceptance: str


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def normalize_status(value: str) -> str:
    return value.strip().upper().replace(" ", "_").replace("-", "_")


def list_tuple(value: object) -> tuple:
    return tuple(value) if isinstance(value, list) else ()


def parse_dependencies(line: str) -> tuple[str, ...]:
    value = line.split(":", 1)[1].strip()
    value = value.split(". (", 1)[0].rstrip(".")
    if value.lower() == "none":
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip())


def parse_markdown_tasks(text: str, errors: list[str]) -> dict[str, MarkdownTask]:
    heading = re.compile(rf"^## ({TASK_ID_RE}) — (.+)$", re.MULTILINE)
    matches = list(heading.finditer(text))
    parsed: dict[str, MarkdownTask] = {}

    for index, match in enumerate(matches):
        task_id, title = match.group(1), match.group(2).strip()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end() : end]

        wave_status = re.search(
            r"^- Wave: (\d+); status: \*\*([^*]+)\*\*;", section, re.MULTILINE
        )
        dependencies = re.search(r"^- Dependencies: (.+)$", section, re.MULTILINE)
        owned = re.search(r"^- Owned scope: (.+)$", section, re.MULTILINE)
        acceptance = re.search(r"^- Acceptance: (.+)$", section, re.MULTILINE)
        if not all((wave_status, dependencies, owned, acceptance)):
            fail(errors, f"{task_id}: task section is missing a required contract field")
            continue

        assert wave_status and dependencies and owned and acceptance
        owned_paths = tuple(re.findall(r"`([^`]+)`", owned.group(1)))
        if not owned_paths:
            fail(errors, f"{task_id}: Owned scope must contain at least one backticked path")

        if task_id in parsed:
            fail(errors, f"{task_id}: duplicate task heading in TASKS.md")
            continue

        parsed[task_id] = MarkdownTask(
            task_id=task_id,
            title=title,
            wave=int(wave_status.group(1)),
            status=normalize_status(wave_status.group(2)),
            dependencies=parse_dependencies(dependencies.group(0)),
            owned_paths=owned_paths,
            acceptance=acceptance.group(1).strip(),
        )

    return parsed


def load_plan(errors: list[str]) -> tuple[dict, list[object]]:
    try:
        data = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"cannot read valid JSON from {PLAN_PATH.relative_to(ROOT)}: {exc}")
        return {}, []

    if not isinstance(data, dict):
        fail(errors, "plan/tasks.json: document root must be an object")
        return {}, []

    if data.get("project") != "grid-horizons":
        fail(errors, "plan/tasks.json: project must be grid-horizons")
    schema_version = data.get("schemaVersion")
    if type(schema_version) is not int or schema_version != CURRENT_SCHEMA_VERSION:
        fail(
            errors,
            f"plan/tasks.json: schemaVersion must be integer {CURRENT_SCHEMA_VERSION}",
        )
    contract_version = data.get("contractVersion")
    if not isinstance(contract_version, str) or not contract_version.strip():
        fail(errors, "plan/tasks.json: contractVersion must be non-empty text")
    if data.get("stateAuthority") != "../STATUS.md":
        fail(errors, "plan/tasks.json: stateAuthority must resolve to ../STATUS.md")
    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        fail(errors, "plan/tasks.json: tasks must be a non-empty array")
        return data, []
    return data, tasks


def validate_json_tasks(tasks: list[object], errors: list[str]) -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    seen_ids: set[str] = set()
    required = {"id", "wave", "title", "status", "dependsOn", "ownedPaths", "acceptance"}

    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            fail(errors, f"tasks[{index}] must be an object")
            continue
        missing = sorted(required - task.keys())
        if missing:
            fail(errors, f"tasks[{index}] is missing fields: {', '.join(missing)}")
            continue
        task_id = task.get("id")
        if not isinstance(task_id, str) or not re.fullmatch(TASK_ID_RE, task_id):
            fail(errors, f"tasks[{index}].id is not a supported Grid Horizons task ID")
            continue
        if task_id in seen_ids:
            fail(errors, f"{task_id}: duplicate ID in plan/tasks.json")
            continue
        seen_ids.add(task_id)
        error_count_before_fields = len(errors)

        if not isinstance(task.get("title"), str) or not task.get("title", "").strip():
            fail(errors, f"{task_id}: title must be non-empty text")
        if type(task.get("wave")) is not int or task["wave"] < 0:
            fail(errors, f"{task_id}: wave must be a non-negative integer")
        raw_status = task.get("status")
        if not isinstance(raw_status, str) or not raw_status.strip():
            fail(errors, f"{task_id}: status must be non-empty text")
        elif normalize_status(raw_status) not in KNOWN_STATES:
            fail(errors, f"{task_id}: unknown status {raw_status!r}")
        dependencies = task.get("dependsOn")
        if not isinstance(dependencies, list) or not all(
            isinstance(value, str) and bool(value.strip()) and bool(re.fullmatch(TASK_ID_RE, value))
            for value in dependencies
        ):
            fail(errors, f"{task_id}: dependsOn must be an array of task IDs")
        owned_paths = task.get("ownedPaths")
        if not isinstance(owned_paths, list) or not owned_paths or not all(
            isinstance(value, str) and bool(value.strip()) and value == value.strip()
            for value in owned_paths
        ):
            fail(errors, f"{task_id}: ownedPaths must be a non-empty array of paths")
        else:
            for value in owned_paths:
                path = Path(value)
                if path.is_absolute() or ".." in path.parts or value in {".", ""}:
                    fail(errors, f"{task_id}: owned path must stay inside the repository: {value!r}")
        if not isinstance(task.get("acceptance"), str) or not task.get("acceptance", "").strip():
            fail(errors, f"{task_id}: acceptance must be non-empty text")

        if len(errors) == error_count_before_fields:
            by_id[task_id] = task

    return by_id


def validate_dag(by_id: dict[str, dict], errors: list[str]) -> None:
    for task_id, task in by_id.items():
        dependencies = task.get("dependsOn", [])
        if not isinstance(dependencies, list) or not all(
            isinstance(value, str) and bool(re.fullmatch(TASK_ID_RE, value))
            for value in dependencies
        ):
            continue
        if len(dependencies) != len(set(dependencies)):
            fail(errors, f"{task_id}: duplicate dependency")
        for dependency in dependencies:
            if dependency not in by_id:
                fail(errors, f"{task_id}: dependency {dependency} does not exist")
            elif (
                type(by_id[dependency].get("wave")) is int
                and type(task.get("wave")) is int
                and by_id[dependency]["wave"] > task["wave"]
            ):
                fail(errors, f"{task_id}: dependency {dependency} is in a later wave")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str, path: tuple[str, ...]) -> None:
        if task_id in visiting:
            fail(errors, "dependency cycle: " + " -> ".join((*path, task_id)))
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        dependencies = by_id.get(task_id, {}).get("dependsOn", [])
        if not isinstance(dependencies, list):
            dependencies = []
        for dependency in dependencies:
            if dependency in by_id:
                visit(dependency, (*path, task_id))
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in by_id:
        visit(task_id, ())


def validate_foundation(by_id: dict[str, dict], errors: list[str]) -> None:
    for task_id, expected_dependencies in FOUNDATION_CHAIN.items():
        task = by_id.get(task_id)
        if task is None:
            fail(errors, f"required foundation task {task_id} is missing")
            continue
        if task.get("wave") != 0:
            fail(errors, f"{task_id}: foundation task must remain in Wave 0")
        actual_dependencies = list_tuple(task.get("dependsOn"))
        if actual_dependencies != expected_dependencies:
            fail(
                errors,
                f"{task_id}: expected foundation dependencies {expected_dependencies}, got {actual_dependencies}",
            )
        status = normalize_status(str(task.get("status", "")))
        if status not in FOUNDATION_STATES:
            fail(errors, f"{task_id}: foundation status must be READY_FOR_REVIEW or DONE")

    for task_id in ("GH-F02", "GH-F03"):
        task = by_id.get(task_id)
        if task and normalize_status(str(task.get("status", ""))) == "DONE":
            dependencies = task.get("dependsOn", [])
            if not isinstance(dependencies, list):
                continue
            for dependency in dependencies:
                if not isinstance(dependency, str):
                    continue
                dependency_status = normalize_status(str(by_id.get(dependency, {}).get("status", "")))
                if dependency_status != "DONE":
                    fail(errors, f"{task_id}: cannot be DONE while {dependency} is {dependency_status}")


def validate_dependency_readiness(by_id: dict[str, dict], errors: list[str]) -> None:
    """Prevent evidence-bearing work from outrunning unfinished dependencies."""
    for task_id, task in by_id.items():
        status = normalize_status(str(task.get("status", "")))
        if status in INCOMPLETE_STATES:
            continue
        dependencies = task.get("dependsOn", [])
        if not isinstance(dependencies, list):
            continue
        for dependency in dependencies:
            if not isinstance(dependency, str):
                continue
            dependency_status = normalize_status(str(by_id.get(dependency, {}).get("status", "")))
            if dependency_status in INCOMPLETE_STATES:
                fail(errors, f"{task_id}: status {status} outruns unfinished dependency {dependency}")


def validate_markdown_mirror(
    by_id: dict[str, dict], markdown_tasks: dict[str, MarkdownTask], errors: list[str]
) -> None:
    json_ids = set(by_id)
    markdown_ids = set(markdown_tasks)
    if json_ids != markdown_ids:
        missing_md = sorted(json_ids - markdown_ids)
        missing_json = sorted(markdown_ids - json_ids)
        if missing_md:
            fail(errors, "TASKS.md is missing JSON tasks: " + ", ".join(missing_md))
        if missing_json:
            fail(errors, "plan/tasks.json is missing markdown tasks: " + ", ".join(missing_json))

    for task_id in sorted(json_ids & markdown_ids):
        raw = by_id[task_id]
        doc = markdown_tasks[task_id]
        comparisons = {
            "title": (raw.get("title"), doc.title),
            "wave": (raw.get("wave"), doc.wave),
            "status": (normalize_status(str(raw.get("status", ""))), doc.status),
            "dependsOn": (list_tuple(raw.get("dependsOn")), doc.dependencies),
            "ownedPaths": (list_tuple(raw.get("ownedPaths")), doc.owned_paths),
            "acceptance": (raw.get("acceptance"), doc.acceptance),
        }
        for field, (json_value, markdown_value) in comparisons.items():
            if json_value != markdown_value:
                fail(
                    errors,
                    f"{task_id}: {field} differs between plan/tasks.json and TASKS.md",
                )


def parse_foundation_status_rows(text: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    pattern = re.compile(r"^\| (GH-F\d{2}) \| ([^|]+) \| ([^|]+) \|$", re.MULTILINE)
    for match in pattern.finditer(text):
        rows[match.group(1)] = (normalize_status(match.group(2)), match.group(3).strip())
    return rows


def validate_status(by_id: dict[str, dict], errors: list[str]) -> None:
    try:
        text = STATUS_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        fail(errors, f"cannot read STATUS.md: {exc}")
        return
    rows = parse_foundation_status_rows(text)
    for task_id in FOUNDATION_CHAIN:
        if task_id not in rows:
            fail(errors, f"STATUS.md: missing foundation status row for {task_id}")
            continue
        row_status, evidence = rows[task_id]
        plan_status = normalize_status(str(by_id.get(task_id, {}).get("status", "")))
        if row_status != plan_status:
            fail(errors, f"{task_id}: STATUS.md state {row_status} differs from plan state {plan_status}")
        if row_status == "DONE":
            lowered = evidence.lower()
            if len(evidence) < 24 or "review candidate" in lowered or "pending" in lowered:
                fail(errors, f"{task_id}: DONE requires concrete acceptance evidence in STATUS.md")


def local_markdown_targets(path: Path, text: str) -> Iterable[tuple[int, str]]:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in pattern.finditer(line):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if target:
                yield line_number, target


def validate_navigation(errors: list[str]) -> None:
    markdown_paths = sorted(p for p in ROOT.rglob("*.md") if not any(part in {"runs", ".git", "__pycache__", "foundation-2026-09-07"} for part in p.relative_to(ROOT).parts))
    for path in markdown_paths:
        text = path.read_text(encoding="utf-8")
        for line_number, target in local_markdown_targets(path, text):
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(errors, f"{path.relative_to(ROOT)}:{line_number}: local link escapes repository: {target}")
                continue
            if not resolved.exists():
                fail(errors, f"{path.relative_to(ROOT)}:{line_number}: broken local link: {target}")

    for relative in REQUIRED_ARTIFACTS:
        if not (ROOT / relative).is_file():
            fail(errors, f"required planning artifact is missing: {relative}")


def validate_semantic_anchors(by_id: dict[str, dict], errors: list[str]) -> None:
    architecture = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
    packet = (ROOT / "docs" / "work-packets" / "GH-001.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")

    for term in REQUIRED_ARCHITECTURE_TERMS:
        if term not in architecture:
            fail(errors, f"ARCHITECTURE.md is missing required contract section: {term}")
    for term in REQUIRED_PACKET_TERMS:
        if term not in packet:
            fail(errors, f"GH-001 work packet is missing required section: {term}")
    declared_waves = {
        task["wave"]
        for task in by_id.values()
        if type(task.get("wave")) is int and task["wave"] >= 0
    }
    roadmap_waves = [
        int(match.group(1))
        for match in re.finditer(r"^## Wave (\d+):", roadmap, re.MULTILINE)
    ]
    for wave in sorted(declared_waves):
        if wave not in roadmap_waves:
            fail(errors, f"ROADMAP.md is missing declared Wave {wave}")
    for wave in sorted(set(roadmap_waves)):
        if roadmap_waves.count(wave) > 1:
            fail(errors, f"ROADMAP.md has duplicate Wave {wave} headers")



def validate_programme(data: dict, by_id: dict[str, dict], errors: list[str]) -> None:
    """Check expanded metadata, wave gates, source history and generated exports."""
    from render_plan import rendered_files
    if not 200 <= len(by_id) <= 400:
        fail(errors, "programme task count must be 200–400; record a coverage decision before changing this gate")
    horizon = {"foundation": 0, "0.1": 1, "later 0.x": 2, "1.0": 3, "long-term": 4, "exploratory": 5}
    # Reject malformed extension containers before graph or renderer operations.
    structural_start = len(errors)
    for tid, task in by_id.items():
        for field in ("outcome", "featureArea", "targetRelease", "origin", "initialStatus"):
            if not isinstance(task.get(field), str) or not task[field].strip():
                fail(errors, f"{tid}: {field} must be non-empty text")
        for field in ("sourceRefs", "riskEvidence", "textualPrerequisites", "evidence"):
            if not isinstance(task.get(field), list) or not all(isinstance(x,str) and x.strip() for x in task[field]):
                fail(errors, f"{tid}: {field} must be a text array")
        if not isinstance(task.get("dependencyCoverage"),dict):
            fail(errors, f"{tid}: dependencyCoverage must be an object")
        if task.get("platformId") is not None and not isinstance(task.get("platformId"),str):
            fail(errors, f"{tid}: platformId must be null or actual identity text")
    if len(errors) != structural_start:
        return
    outcomes: dict[str, str] = {}
    for tid, task in by_id.items():
        for field in ("outcome", "featureArea", "targetRelease", "origin"):
            if not isinstance(task.get(field), str) or not task[field].strip():
                fail(errors, f"{tid}: {field} must be non-empty text")
        for field in ("sourceRefs", "riskEvidence"):
            if not isinstance(task.get(field), list) or not task[field] or not all(isinstance(x,str) and x.strip() for x in task[field]):
                fail(errors, f"{tid}: {field} must be a non-empty text array")
        for field in ("textualPrerequisites", "evidence"):
            if not isinstance(task.get(field), list) or not all(isinstance(x,str) and x.strip() for x in task[field]):
                fail(errors, f"{tid}: {field} must be a text array")
        if task.get("origin") not in {"source_requirement", "proposal", "exploratory"}:
            fail(errors, f"{tid}: unknown origin classification")
        release = task.get("targetRelease")
        if release not in horizon:
            fail(errors, f"{tid}: unknown release horizon")
        if task.get("origin") == "exploratory" and release != "exploratory":
            fail(errors, f"{tid}: exploratory scope cannot be promised delivery")
        if task.get("initialStatus") != ("DONE" if tid.startswith("GH-F") else "PLANNED"):
            fail(errors, f"{tid}: initial status history changed")
        if task.get("status") in {"IMPLEMENTED", "AUTOMATED_PASS", "RUNTIME_VERIFIED", "USER_VALIDATED", "RELEASE_VERIFIED", "DONE"} and not task.get("evidence"):
            fail(errors, f"{tid}: evidence-bearing state requires evidence references")
        # Evidence references are artifacts, not unsupported prose attestations.
        for ref in task.get("evidence", []):
            if isinstance(ref,str) and not ref.startswith(("https://", "http://")):
                p = (ROOT/ref.split("#",1)[0]).resolve()
                if not p.is_relative_to(ROOT) or not p.exists():
                    fail(errors, f"{tid}: missing or escaping evidence reference: {ref}")
        normalized = re.sub(r"[^a-z0-9]+", " ", str(task.get("outcome", "")).lower()).strip()
        if normalized in outcomes:
            fail(errors, f"{tid}: duplicate outcome with {outcomes[normalized]}")
        outcomes[normalized] = tid
        coverage = task.get("dependencyCoverage")
        expected = {d: by_id[d].get("outcome") for d in task["dependsOn"] if d in by_id}
        if coverage != expected:
            fail(errors, f"{tid}: prerequisite outcome coverage differs from dependency contracts")
        for dependency in task["dependsOn"]:
            prereq = by_id.get(dependency,{})
            if horizon.get(prereq.get("targetRelease"), -1) > horizon.get(release, -1):
                fail(errors, f"{tid}: prerequisite {dependency} has a later release horizon")
        if tid.startswith("GH-S") and release != "0.1":
            fail(errors, f"{tid}: synthetic 0.1 task moved out of its declared release")
    waves = data.get("waves")
    if not isinstance(waves, list) or not 20 <= len(waves) <= 32:
        fail(errors, "waves must contain 20–32 outcome waves (native platform maximum 32)")
        return
    wave_structure_start=len(errors)
    for wave in waves:
        if not isinstance(wave,dict):
            fail(errors,"wave must be an object"); continue
        for field in ("id","title","outcome","targetRelease","gateDecision"):
            if not isinstance(wave.get(field),str) or not wave[field].strip():
                fail(errors,f"wave: {field} must be non-empty text")
    if len(errors)!=wave_structure_start:
        return
    memberships: dict[str, int] = {}
    orders=[]; wave_ids=[]
    for wave in waves:
        if not isinstance(wave,dict):
            fail(errors,"wave must be an object"); continue
        order=wave.get("order"); orders.append(order); wave_ids.append(wave.get("id"))
        if type(order) is not int or order < 0:
            fail(errors,"wave order must be a non-negative integer")
        for field in ("id","title","outcome","targetRelease","gateDecision"):
            if not isinstance(wave.get(field),str) or not wave[field].strip():
                fail(errors,f"wave {order}: missing {field}")
        if len(str(wave.get("title",""))) > 80:
            fail(errors,f"wave {order}: title exceeds native 80-character limit")
        ids=wave.get("taskIds")
        if not isinstance(ids,list) or not ids or not all(isinstance(x,str) for x in ids):
            fail(errors,f"wave {order}: taskIds must be a non-empty ID array"); continue
        if not isinstance(wave.get("exitEvidence"),list) or not wave["exitEvidence"] or not all(isinstance(x,str) and x.strip() for x in wave["exitEvidence"]):
            fail(errors,f"wave {order}: missing exit evidence")
        entry=set()
        for tid in ids:
            memberships[tid]=memberships.get(tid,0)+1
            task=by_id.get(tid)
            if task is None:
                fail(errors,f"wave {order}: unknown assigned task {tid}"); continue
            if task["wave"] != order or task.get("targetRelease") != wave.get("targetRelease"):
                fail(errors,f"{tid}: wave assignment or release scope mismatch")
            entry.update(d for d in task["dependsOn"] if d not in ids)
        if wave.get("entryDependencies") != sorted(entry):
            fail(errors,f"wave {order}: entry dependencies differ from assigned tasks")
    if orders != list(range(len(waves))):
        fail(errors,"wave ordering must be unique contiguous ascending integers")
    if any(not isinstance(x,str) for x in wave_ids) or len(set(str(x) for x in wave_ids)) != len(waves):
        fail(errors,"duplicate or malformed wave ID")
    for tid in by_id:
        if memberships.get(tid) != 1:
            fail(errors,f"{tid}: orphan or duplicate wave membership")
    lineage=ROOT/"docs/lineage/foundation-2026-09-07"
    try:
        manifest=json.loads((lineage/"manifest.json").read_text())
        original=json.loads((lineage/"plan/tasks.json").read_text())
    except (OSError,ValueError) as exc:
        fail(errors,f"cannot read immutable lineage: {exc}"); return
    if not isinstance(manifest,dict) or not isinstance(original,dict):
        fail(errors,"immutable lineage roots must be objects"); return
    lineage_start=len(errors)
    if manifest.get("sourceCommit") != "3d4a4dc7718d72e0d20785c70154c800cc849093":
        fail(errors,"immutable lineage source revision differs")
    if hashlib.sha256((lineage/"manifest.json").read_bytes()).hexdigest() != "37b950ea41a9bf1d0e28ca61941ac77b638e77474acc4e4bfa38db2abb5ecd2a":
        fail(errors,"immutable lineage manifest hash mismatch"); return
    for name,digest in manifest.get("files",{}).items():
        path=(lineage/name).resolve()
        if not path.is_relative_to(lineage.resolve()) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            fail(errors,f"immutable lineage hash mismatch: {name}")
    if len(errors)!=lineage_start:
        return
    originals=original.get("tasks",[])
    if len(originals)!=27 or sum(len(t.get("dependsOn",[])) for t in originals)!=71:
        fail(errors,"original lineage must retain 27 contracts and 71 edges")
    mappings=data.get("sourceMappings")
    if not isinstance(mappings,list) or not all(isinstance(m,dict) for m in mappings):
        fail(errors,"source mappings must be object array"); return
    mapped={m.get("sourceId"):m for m in mappings if isinstance(m.get("sourceId"),str)}
    if len(mapped)!=len(mappings) or set(mapped)!={t["id"] for t in originals}:
        fail(errors,"missing or duplicate source mappings")
    for old in originals:
        tid=old["id"];current=by_id.get(tid,{})
        for field in ("id","title","acceptance","dependsOn","ownedPaths"):
            if current.get(field)!=old[field]:
                fail(errors,f"{tid}: original {field} contract changed")
        if current.get("sourceWave")!=old["wave"]:
            fail(errors,f"{tid}: original wave history changed")
        mapping=mapped.get(tid,{})
        for field,expected in {"sourceKey":"grid-horizons:"+tid,"sourceRevision":original["contractVersion"],"sourceStatus":old["status"],"sourceWave":old["wave"],"sourceAcceptance":old["acceptance"],"structuredPrerequisites":old["dependsOn"],"textualPrerequisites":[],"sourcePlatformId":None,"frozenPredecessor":None}.items():
            if mapping.get(field)!=expected:
                fail(errors,f"{tid}: source mapping history changed: {field}")
        if mapping.get("treatment") not in {"retained","expanded","split","merged","deferred","superseded"} or not isinstance(mapping.get("reason"),str) or len(mapping["reason"])<24:
            fail(errors,f"{tid}: mapping requires explicit treatment and reason")
        successors=mapping.get("successorIds")
        if not isinstance(successors,list) or not successors or not all(isinstance(x,str) and x in by_id for x in successors):
            fail(errors,f"{tid}: missing or dangling successor mappings")
        elif len(successors)!=len(set(successors)):
            fail(errors,f"{tid}: duplicate successor mappings")
        partial=mapping.get("syntheticPartialIds")
        if not isinstance(partial,list) or not all(isinstance(x,str) and x in by_id and by_id[x].get("targetRelease")=="0.1" for x in partial):
            fail(errors,f"{tid}: invalid synthetic partial mappings")
        safe_successors=successors if isinstance(successors,list) else []
        expected_platform=[{"id":x,"platformId":by_id[x].get("platformId")} for x in safe_successors if isinstance(x,str) and x in by_id]
        relationships=mapping.get("successorRelationships")
        expected_relationships=[{"id":x,"relationship":"retained_whole_contract" if x==tid else "bounded_evidence_contribution","completionImplication":"Requires independent acceptance of the complete original contract; no automatic completion from descendant status."} for x in safe_successors]
        if relationships!=expected_relationships:
            fail(errors,f"{tid}: successor outcome relationships missing or changed")
        expected_url="https://github.com/thepianistdirector/grid-horizons/blob/3d4a4dc7718d72e0d20785c70154c800cc849093/plan/tasks.json"
        if mapping.get("sourceContractUrl")!=expected_url or current.get("sourceIdentity",{}).get("contractUrl")!=expected_url:
            fail(errors,f"{tid}: original contract URL changed")
        if mapping.get("platformSuccessors")!=expected_platform:
            fail(errors,f"{tid}: successor platform identities drift")
    pub=data.get("publication")
    if not isinstance(pub,dict):
        fail(errors,"publication must be an object"); return
    for field in ("nativeTaskIds","nativeWaveIds"):
        if not isinstance(pub.get(field),dict):
            fail(errors,f"publication {field} must be an identity mapping"); return
    for tid,task in by_id.items():
        if task.get("platformId") != pub["nativeTaskIds"].get(tid):
            fail(errors,f"{tid}: platform ID lacks matching actual publication mapping")
    for wave in waves:
        if wave.get("platformId") != pub["nativeWaveIds"].get(wave.get("id")):
            fail(errors,f"wave {wave.get('order')}: platform ID lacks matching actual publication mapping")
    if set(pub["nativeTaskIds"])-set(by_id) or set(pub["nativeWaveIds"])-set(wave_ids):
        fail(errors,"publication contains orphan native identity mappings")
    # Original source state is immutable in lineage; current progress may evolve only with evidence.
    # Rendering is deterministic, so every metadata field and publication mapping is covered.
    try:
        views=rendered_files(data)
    except (KeyError,TypeError,ValueError) as exc:
        fail(errors,f"cannot render malformed programme: {exc}"); return
    for name,expected in views.items():
        path=ROOT/name
        if not path.is_file() or path.read_text()!=expected:
            fail(errors,f"generated view drift: {name}")


def main() -> int:
    errors: list[str] = []
    data, tasks = load_plan(errors)
    by_id = validate_json_tasks(tasks, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} structural planning error(s)", file=sys.stderr)
        return 1

    markdown_text = TASKS_PATH.read_text(encoding="utf-8")
    markdown_tasks = parse_markdown_tasks(markdown_text, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} task-contract error(s)", file=sys.stderr)
        return 1

    validate_dag(by_id, errors)
    validate_foundation(by_id, errors)
    validate_dependency_readiness(by_id, errors)
    validate_markdown_mirror(by_id, markdown_tasks, errors)
    validate_status(by_id, errors)
    validate_navigation(errors)
    validate_semantic_anchors(by_id, errors)
    validate_programme(data, by_id, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} planning error(s)", file=sys.stderr)
        return 1

    print(f"PASS: Grid Horizons plan is internally consistent ({len(by_id)} tasks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate Grid Horizons planning contracts using only the Python standard library.

This checks plan structure, navigation, dependency semantics, and markdown/JSON
agreement. It intentionally does not freeze the current task count or the future
status of implementation tasks; historical-contract preservation is reviewed
against Git rather than duplicated here.
"""

from __future__ import annotations

import json
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
CURRENT_SCHEMA_VERSION = 2

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
    markdown_paths = sorted(ROOT.rglob("*.md"))
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


def main() -> int:
    errors: list[str] = []
    _, tasks = load_plan(errors)
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

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} planning error(s)", file=sys.stderr)
        return 1

    print(f"PASS: Grid Horizons plan is internally consistent ({len(by_id)} tasks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

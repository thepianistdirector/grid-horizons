"""Single-writer local attempts, durable evidence and explicit reconciliation.

Trusted built-ins only. Structural bounds and cooperative time checks are not
an OS sandbox, memory limit or a claim of protected evaluator isolation.
Copyright (C) 2026 Lucas Santana. SPDX-License-Identifier: AGPL-3.0-only
"""

from __future__ import annotations

import contextlib
import datetime
import fcntl
import hashlib
import json
import math
import os
import platform
import re
import resource
import signal
import time
import uuid
from pathlib import Path

from . import MODEL_ID, RESULT_SCHEMA
from .assets import build_identity, model_record
from .contracts import (ContractError, MAX_RAW_BYTES, canonical_bytes, decode_json,
                        digest, load_json, object_fields, validate_scenario)
from .kernel import KERNEL_VERSION, SolverFailure, envelope, generate_intervals
from .raw_contract import NOT_EVALUATED

STUDY_SCHEMA = "grid-horizons.study/v1"
MANIFEST_SCHEMA = "grid-horizons.manifest/v1"
COMPLETED = {"COMPLETED_VALID", "COMPLETED_INFEASIBLE"}
FAILURES = {"FAILED_SOLVER", "RESOURCE_EXHAUSTED", "INVALID_RESULT", "FAILED_EVALUATOR",
            "LOST", "CANCELLED"}


class StudyError(ValueError):
    pass


class ResourceExhausted(RuntimeError):
    pass


class Cancelled(RuntimeError):
    pass


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def file_digest(path: Path) -> str:
    with path.open("rb") as stream:
        data = stream.read(MAX_RAW_BYTES + 1)
    if len(data) > MAX_RAW_BYTES:
        raise StudyError("Study artifact exceeds the supported byte limit")
    return hashlib.sha256(data).hexdigest()


def _sync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_bytes(path: Path, data: bytes, *, replace: bool = False) -> None:
    temporary = path.with_name("." + path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if replace:
            os.replace(temporary, path)
        else:
            # An exclusive hard link publishes the complete file without a
            # check-then-overwrite race. Both names are on the same filesystem.
            os.link(temporary, path)
            temporary.unlink()
        _sync_directory(path.parent)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_json(path: Path, value: dict, *, replace: bool = False) -> None:
    atomic_bytes(path, canonical_bytes(value) + b"\n", replace=replace)


def _inside(study: Path, relative: str) -> Path:
    path = study / relative
    current = path
    while current != study:
        if current.is_symlink():
            raise StudyError(f"Study artifact {relative} is a symlink; refusing to follow it")
        current = current.parent
    return path


@contextlib.contextmanager
def study_lock(study: Path):
    path = _inside(study, ".lock")
    descriptor = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise StudyError("Another coordinator owns this study; wait for it to finish") from exc
        yield
    finally:
        os.close(descriptor)


def _event(study: Path, event: str, **fields) -> None:
    path = _inside(study, "events.ndjson")
    with path.open("ab") as stream:
        stream.write(canonical_bytes({"time": now(), "event": event, **fields}) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def _environment() -> dict:
    return {"python": platform.python_version(), "implementation": platform.python_implementation(),
            "system": platform.system(), "machine": platform.machine()}


def _source_record() -> dict:
    return {"id": "GH-SYNTHETIC-001", "kind": "ORIGINAL_SYNTHETIC",
            "license": "AGPL-3.0-only", "rights": "CLEARED_REDISTRIBUTION",
            "description": "Original illustrative feeder and profiles; no observed or private utility data.",
            "modifications": "Every edited scenario is identified by its own immutable content digest."}


def _new_study(scenario: dict, study: Path) -> None:
    validate_scenario(scenario)
    study.mkdir()  # Never reuse or overwrite a requested output directory.
    with study_lock(study):
        model = model_record()
        source = _source_record()
        for name, value in (("scenario.json", scenario), ("model.json", model), ("source.json", source)):
            atomic_json(study / name, value)
        manifest = {"schema_version": STUDY_SCHEMA, "study_id": uuid.uuid4().hex,
                    "created_at": now(), "scenario_sha256": digest(scenario),
                    "model_sha256": digest(model), "source_sha256": digest(source),
                    "software": build_identity(), "policies": ["baseline", "candidate"]}
        atomic_json(study / "study.json", manifest)
        for name in ("pending", "attempts", "reports", "lost-setups"):
            (study / name).mkdir()
        _event(study, "STUDY_CREATED", scenario_sha256=manifest["scenario_sha256"])


def _read_study(study: Path, *, matching_build: bool = True) -> tuple[dict, dict]:
    manifest = load_json(_inside(study, "study.json"))
    object_fields(manifest, {"schema_version", "study_id", "created_at", "scenario_sha256",
                            "model_sha256", "source_sha256", "software", "policies"}, "study")
    if manifest["schema_version"] != STUDY_SCHEMA or manifest["policies"] != ["baseline", "candidate"]:
        raise StudyError("Unsupported study schema or policy set")
    documents = {}
    for name in ("scenario", "model", "source"):
        document = load_json(_inside(study, name + ".json"))
        if digest(document) != manifest[name + "_sha256"]:
            raise StudyError(f"Immutable {name} digest differs from study manifest")
        documents[name] = document
    scenario = validate_scenario(documents["scenario"])
    if matching_build and manifest["software"] != build_identity():
        raise StudyError("This study needs its original tool build. Use that build to verify/resume, or rerun in a new directory")
    if matching_build and documents["model"] != model_record():
        raise StudyError("This study needs its original model record")
    for directory in ("pending", "attempts", "reports", "lost-setups"):
        if not _inside(study, directory).is_dir():
            raise StudyError(f"Missing study directory: {directory}")
    return manifest, scenario


def _manifest(study_manifest: dict, scenario: dict, policy_id: str, attempt_id: str,
              time_limit: float) -> dict:
    from .evaluator import EVALUATOR_VERSION
    policy = next(p for p in scenario["policies"] if p["id"] == policy_id)
    logical = digest({"scenario": digest(scenario), "policy": digest(policy),
                      "model": study_manifest["model_sha256"], "software": study_manifest["software"]})
    return {"schema_version": MANIFEST_SCHEMA, "attempt_id": attempt_id,
            "logical_run_id": logical, "study_id": study_manifest["study_id"],
            "scenario_sha256": digest(scenario), "policy_sha256": digest(policy),
            "policy_id": policy_id, "model_id": MODEL_ID,
            "model_sha256": study_manifest["model_sha256"], "software": study_manifest["software"],
            "kernel_version": KERNEL_VERSION, "evaluator_version": EVALUATOR_VERSION,
            "started_at": now(), "environment": _environment(),
            "limits": {"wall_time_s": time_limit, "raw_bytes": MAX_RAW_BYTES,
                       "enforcement": "cooperative checks between intervals and before terminal publication",
                       "memory": "observed only; no OS memory cap", "execution": "trusted built-ins only",
                       "isolation": "no OS sandbox or protected-confirmation claim"}}


def _failure(scenario: dict, raw: dict, policy_id: str, state: str, message: str) -> dict:
    from .evaluator import EVALUATOR_VERSION
    return {"schema_version": RESULT_SCHEMA, "scenario_sha256": digest(scenario),
            "raw_sha256": digest(raw), "policy_id": policy_id, "model_id": MODEL_ID,
            "evaluator_version": EVALUATOR_VERSION, "state": state, "comparison_eligible": False,
            "findings": [{"code": state, "message": message}], "metrics": {}, "ledger": {},
            "not_evaluated": NOT_EVALUATED,
            "uncertainty": {"state": "NOT_EVALUATED", "reason": "No eligible completed result"},
            "scope": "Fictional, approximation-bounded tutorial only"}


def _usage(start: float, cpu_start: float, directory: Path) -> dict:
    return {"wall_time_s": time.perf_counter() - start,
            "cpu_time_s": time.process_time() - cpu_start,
            "process_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
            "rss_scope": "Linux process lifetime high-water mark, not per-attempt allocation",
            "artifact_bytes_before_terminal_metadata": sum(p.stat().st_size for p in directory.iterdir() if p.is_file()),
            "measurement": "software observation; not an enforced memory/disk isolation boundary"}


def _seal_and_publish(study: Path, directory: Path) -> None:
    if not (directory / "integrity.json").exists():
        entries = {p.name: file_digest(p) for p in sorted(directory.iterdir()) if p.is_file()}
        atomic_json(directory / "integrity.json", {"schema_version": 1, "files": entries})
    destination = study / "attempts" / directory.name
    if destination.exists():
        raise StudyError("Attempt identity already exists; refusing duplicate publication")
    os.rename(directory, destination)
    _sync_directory(study / "attempts")
    _sync_directory(study / "pending")
    _event(study, "ATTEMPT_PUBLISHED", attempt_id=directory.name)


def _finish(study: Path, directory: Path, manifest: dict, raw: dict, evaluation: dict,
            usage: dict) -> dict:
    if not (directory / "raw.json").exists():
        atomic_json(directory / "raw.json", raw)
    atomic_json(directory / "evaluation.json", evaluation)
    result = {**evaluation, "attempt_id": manifest["attempt_id"],
              "logical_run_id": manifest["logical_run_id"], "manifest_sha256": digest(manifest),
              "started_at": manifest["started_at"], "finished_at": now(), "resources": usage}
    atomic_json(directory / "result.json", result)
    _seal_and_publish(study, directory)
    return result


@contextlib.contextmanager
def cancellation_requested():
    cancelled = [False]
    old = {}

    def request(signum, frame):
        cancelled[0] = True

    for signum in (signal.SIGINT, signal.SIGTERM):
        old[signum] = signal.signal(signum, request)
    try:
        yield cancelled
    finally:
        for signum, handler in old.items():
            signal.signal(signum, handler)


def _run_attempt(study: Path, study_manifest: dict, scenario: dict, policy_id: str,
                 time_limit: float, stop_after: int | None, cancelled: list[bool]) -> dict:
    from .evaluator import evaluate
    attempt_id = policy_id + "-" + uuid.uuid4().hex
    preparing = study / "pending" / (".preparing-" + attempt_id)
    preparing.mkdir()
    manifest = _manifest(study_manifest, scenario, policy_id, attempt_id, time_limit)
    atomic_json(preparing / "manifest.json", manifest)
    directory = study / "pending" / attempt_id
    os.rename(preparing, directory)
    _sync_directory(study / "pending")
    _event(study, "ATTEMPT_STARTED", attempt_id=attempt_id, policy_id=policy_id)
    rows: list[dict] = []
    start, cpu_start = time.perf_counter(), time.process_time()
    total_bytes = 0

    def budget():
        if cancelled[0]:
            raise Cancelled("Cancellation requested; complete intervals are retained")
        if time.perf_counter() - start > time_limit:
            raise ResourceExhausted("Cooperative wall-time budget exhausted")

    try:
        budget()
        with (directory / "raw.ndjson").open("xb") as stream:
            for row in generate_intervals(scenario, policy_id):
                budget()
                data = canonical_bytes(row) + b"\n"
                if total_bytes + len(data) > MAX_RAW_BYTES:
                    raise ResourceExhausted("Raw interval output byte budget exhausted")
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
                rows.append(row)
                total_bytes += len(data)
                if stop_after is not None and len(rows) >= stop_after:
                    raise Cancelled("Stopped at the requested interval boundary for explicit recovery")
                budget()
        raw = envelope(scenario, policy_id, rows)
        atomic_json(directory / "raw.json", raw)
        _event(study, "EVALUATING", attempt_id=attempt_id)
        budget()
        try:
            # Re-read frozen input to avoid trusting producer-mutated memory.
            fixed_scenario = validate_scenario(load_json(study / "scenario.json"))
            evaluation = evaluate(fixed_scenario, raw, policy_id)
        except Exception as exc:
            evaluation = _failure(scenario, raw, policy_id, "FAILED_EVALUATOR",
                                  f"Independent evaluator raised {type(exc).__name__}; no objective emitted")
        budget()
    except (Cancelled, KeyboardInterrupt) as exc:
        raw = envelope(scenario, policy_id, rows)
        evaluation = _failure(scenario, raw, policy_id, "CANCELLED", str(exc) or "Keyboard interrupt")
    except (ResourceExhausted, MemoryError) as exc:
        raw = envelope(scenario, policy_id, rows)
        evaluation = _failure(scenario, raw, policy_id, "RESOURCE_EXHAUSTED", str(exc))
    except SolverFailure as exc:
        raw = envelope(scenario, policy_id, rows)
        evaluation = _failure(scenario, raw, policy_id, "FAILED_SOLVER", str(exc))
    except Exception as exc:
        raw = envelope(scenario, policy_id, rows)
        evaluation = _failure(scenario, raw, policy_id, "FAILED_SOLVER",
                              f"Trusted numerical attempt raised {type(exc).__name__}; no objective emitted")
    return _finish(study, directory, manifest, raw, evaluation, _usage(start, cpu_start, directory))


def _read_rows(directory: Path) -> tuple[list[dict], int]:
    path = directory / "raw.ndjson"
    if not path.exists():
        return [], 0
    with path.open("rb") as stream:
        data = stream.read(MAX_RAW_BYTES + 1)
    if len(data) > MAX_RAW_BYTES:
        raise StudyError("Raw journal exceeds the supported byte limit")
    lines = data.splitlines(keepends=True)
    incomplete_bytes = 0
    if lines and not lines[-1].endswith(b"\n"):
        incomplete_bytes = len(lines.pop())
    return [decode_json(line, MAX_RAW_BYTES) for line in lines], incomplete_bytes


def _check_manifest(manifest: dict, study_manifest: dict, scenario: dict, attempt_id: str) -> None:
    object_fields(manifest, {"schema_version", "attempt_id", "logical_run_id", "study_id",
                            "scenario_sha256", "policy_sha256", "policy_id", "model_id",
                            "model_sha256", "software", "kernel_version", "evaluator_version",
                            "started_at", "environment", "limits"}, "attempt.manifest")
    if not re.fullmatch(r"(?:baseline|candidate)-[0-9a-f]{32}", attempt_id):
        raise StudyError("Malformed attempt directory identity")
    policy_id = manifest["policy_id"]
    if policy_id not in ("baseline", "candidate") or not attempt_id.startswith(policy_id + "-"):
        raise StudyError("Attempt policy identity differs from its directory")
    policy = next(p for p in scenario["policies"] if p["id"] == policy_id)
    expected = {"schema_version": MANIFEST_SCHEMA, "attempt_id": attempt_id,
                "study_id": study_manifest["study_id"], "scenario_sha256": digest(scenario),
                "policy_sha256": digest(policy), "model_id": MODEL_ID,
                "model_sha256": study_manifest["model_sha256"], "software": study_manifest["software"]}
    expected["logical_run_id"] = digest({"scenario": digest(scenario), "policy": digest(policy),
                                         "model": study_manifest["model_sha256"], "software": study_manifest["software"]})
    for key, value in expected.items():
        if manifest[key] != value:
            raise StudyError(f"Attempt manifest binding differs: {key}")


def _check_attempt(study: Path, directory: Path, study_manifest: dict, scenario: dict,
                   *, require_integrity: bool = True) -> dict:
    from .evaluator import evaluate
    for path in directory.iterdir():
        if path.is_symlink() or not path.is_file():
            raise StudyError("Attempt artifacts must be regular files, not links or directories")
    if require_integrity or (directory / "integrity.json").exists():
        integrity = load_json(directory / "integrity.json")
        object_fields(integrity, {"schema_version", "files"}, "integrity")
        if integrity["schema_version"] != 1 or not isinstance(integrity["files"], dict):
            raise StudyError("Unsupported attempt integrity index")
        actual = {p.name for p in directory.iterdir()} - {"integrity.json"}
        if set(integrity["files"]) != actual:
            raise StudyError("Attempt artifact coverage differs from its integrity index")
        for name, expected in integrity["files"].items():
            if file_digest(directory / name) != expected:
                raise StudyError(f"Attempt artifact digest differs: {name}")
    manifest = load_json(directory / "manifest.json")
    _check_manifest(manifest, study_manifest, scenario, directory.name)
    raw = load_json(directory / "raw.json", MAX_RAW_BYTES)
    evaluation = load_json(directory / "evaluation.json", MAX_RAW_BYTES)
    result = load_json(directory / "result.json", MAX_RAW_BYTES)
    execution_fields = {"attempt_id", "logical_run_id", "manifest_sha256", "started_at", "finished_at", "resources"}
    if not isinstance(evaluation, dict):
        raise StudyError("Evaluation must be an object")
    object_fields(result, set(evaluation) | execution_fields, "attempt.result")
    if any(result[key] != value for key, value in evaluation.items()):
        raise StudyError("Terminal result differs from retained independent evaluation")
    for key in ("attempt_id", "logical_run_id", "started_at"):
        if result[key] != manifest[key]:
            raise StudyError(f"Terminal result differs from manifest: {key}")
    if result["manifest_sha256"] != digest(manifest) or result.get("raw_sha256") != digest(raw):
        raise StudyError("Terminal result artifact binding differs")
    if result.get("scenario_sha256") != digest(scenario) or result.get("policy_id") != manifest["policy_id"]:
        raise StudyError("Terminal result scenario/policy binding differs")
    state = result.get("state")
    if state not in COMPLETED | FAILURES or result.get("comparison_eligible") is not (state == "COMPLETED_VALID"):
        raise StudyError("Unrecognized or inconsistent terminal state")
    if state in FAILURES and result.get("metrics"):
        raise StudyError("Failed or invalid attempts cannot emit objective metrics")
    rows, incomplete_bytes = _read_rows(directory)
    if rows != raw.get("intervals"):
        raise StudyError("Raw interval journal differs from the retained raw envelope")
    if incomplete_bytes and state in COMPLETED:
        raise StudyError("Completed attempt has a truncated interval journal")
    if state in COMPLETED | {"INVALID_RESULT"}:
        recalculated = evaluate(scenario, raw, manifest["policy_id"])
        if canonical_bytes(recalculated) != canonical_bytes(evaluation):
            raise StudyError("Fresh independent evaluation differs from the retained result")
    return result


def _selected(study: Path, study_manifest: dict, scenario: dict) -> tuple[list[dict], list[dict]]:
    attempts = []
    paths = sorted(_inside(study, "attempts").iterdir())
    if len(paths) > 256:
        raise StudyError("This tutorial supports at most 256 retained attempts per study")
    for path in paths:
        if path.is_symlink() or not path.is_dir():
            raise StudyError("Unexpected attempt entry")
        attempts.append(_check_attempt(study, path, study_manifest, scenario))
    selected = []
    for policy_id in ("baseline", "candidate"):
        relevant = [r for r in attempts if r["policy_id"] == policy_id]
        completed = [r for r in relevant if r["state"] in COMPLETED]
        if len(completed) > 1:
            raise StudyError("Duplicate completed logical run; explicit investigation required")
        if completed:
            selected.append(completed[0])
        elif relevant:
            selected.append(max(relevant, key=lambda r: (r["finished_at"], r["attempt_id"])))
    return selected, attempts


def _reconcile(study: Path, study_manifest: dict, scenario: dict) -> list[dict]:
    changes = []
    for directory in sorted(_inside(study, "pending").iterdir()):
        if directory.is_symlink() or not directory.is_dir():
            raise StudyError("Unexpected pending entry; inspect it before recovery")
        if directory.name.startswith(".preparing-"):
            if not (directory / "manifest.json").exists():
                destination = study / "lost-setups" / directory.name.removeprefix(".preparing-")
                os.rename(directory, destination)
                _event(study, "LOST_SETUP", setup_id=destination.name,
                       note="Process disappeared before run admission; files retained without a fabricated run manifest")
                changes.append({"setup_id": destination.name, "state": "LOST", "admitted_run": False})
                continue
            manifest = load_json(directory / "manifest.json")
            destination = study / "pending" / manifest["attempt_id"]
            _check_manifest(manifest, study_manifest, scenario, manifest["attempt_id"])
            if destination.exists():
                raise StudyError("Pending attempt identity collision")
            os.rename(directory, destination)
            directory = destination
        manifest = load_json(directory / "manifest.json")
        _check_manifest(manifest, study_manifest, scenario, directory.name)
        if (directory / "result.json").exists():
            result = _check_attempt(study, directory, study_manifest, scenario, require_integrity=False)
            _seal_and_publish(study, directory)
            changes.append({"attempt_id": manifest["attempt_id"], "state": result["state"],
                            "action": "activated a complete independently rechecked prepublication result"})
            continue
        rows, incomplete_bytes = _read_rows(directory)
        raw = envelope(scenario, manifest["policy_id"], rows)
        # A crash may leave a complete evaluation without its result envelope.
        # Keep that candidate as evidence, but do not promote it into success.
        if (directory / "evaluation.json").exists():
            os.rename(directory / "evaluation.json", directory / "preactivation-evaluation.json")
        if (directory / "raw.json").exists():
            existing = load_json(directory / "raw.json", MAX_RAW_BYTES)
            if existing != raw:
                raise StudyError("Pending raw snapshot differs from its durable journal")
        evaluation = _failure(scenario, raw, manifest["policy_id"], "LOST",
                              f"No active coordinator and no terminal result; {len(rows)} complete intervals retained; "
                              f"{incomplete_bytes} trailing journal bytes retained but not treated as a complete interval")
        usage = {"wall_time_s": None, "cpu_time_s": None, "process_peak_rss_bytes": None,
                 "measurement": "Process disappeared; elapsed CPU/memory usage is unknown",
                 "artifact_bytes_before_terminal_metadata": sum(p.stat().st_size for p in directory.iterdir() if p.is_file())}
        result = _finish(study, directory, manifest, raw, evaluation, usage)
        changes.append({"attempt_id": manifest["attempt_id"], "state": result["state"], "action": "recorded loss"})
    return changes


def _validate_options(time_limit: float, stop_after: int | None) -> None:
    if type(time_limit) not in (int, float) or not math.isfinite(time_limit) or not 0 < time_limit <= 30:
        raise StudyError("Per-attempt time limit must be finite, greater than 0 and at most 30 seconds")
    if stop_after is not None and (type(stop_after) is not int or not 1 <= stop_after <= 96):
        raise StudyError("Stop-after interval count must be an integer between 1 and 96")


def _summary(study_manifest: dict, selected: list[dict], attempts: list[dict], pending: int) -> dict:
    from .evaluator import compare
    comparison = compare(selected) if len(selected) == 2 else {
        "state": "INELIGIBLE", "reason": "Both policies do not yet have terminal evidence", "differences": {}}
    return {"state": "STUDY_INSPECTED", "study_id": study_manifest["study_id"],
            "scenario_sha256": study_manifest["scenario_sha256"],
            "software": study_manifest["software"], "comparison": comparison,
            "policies": {r["policy_id"]: {"state": r["state"], "attempt_id": r["attempt_id"],
                                         "metrics": r["metrics"], "findings": r["findings"]} for r in selected},
            "attempt_count": len(attempts), "pending_count": pending,
            "retained_attempts": [{"attempt_id": r["attempt_id"], "policy_id": r["policy_id"], "state": r["state"]}
                                  for r in attempts]}


def _reports(study: Path, study_manifest: dict, scenario: dict, selected: list[dict], attempts: list[dict]) -> None:
    from .reports import write_report
    write_report(study, study_manifest, scenario, selected, attempts)


def _execute(study: Path, time_limit: float, stop_after: int | None, resume: bool) -> dict:
    _validate_options(time_limit, stop_after)
    with study_lock(study), cancellation_requested() as cancelled:
        study_manifest, scenario = _read_study(study)
        changes = _reconcile(study, study_manifest, scenario) if resume else []
        selected, attempts = _selected(study, study_manifest, scenario)
        for policy_id in ("baseline", "candidate"):
            if any(r["policy_id"] == policy_id and r["state"] in COMPLETED for r in selected):
                continue
            if len(attempts) >= 256:
                raise StudyError("Retained attempt limit reached; rerun the scenario in a new study")
            result = _run_attempt(study, study_manifest, scenario, policy_id, time_limit, stop_after, cancelled)
            selected, attempts = _selected(study, study_manifest, scenario)
            if result["state"] in {"CANCELLED", "RESOURCE_EXHAUSTED"}:
                break
        _reports(study, study_manifest, scenario, selected, attempts)
        summary = _summary(study_manifest, selected, attempts, len(list((study / "pending").iterdir())))
        summary["reconciliation"] = changes
        return summary


def run_study(scenario: dict, study: Path, *, time_limit: float = 10,
              stop_after: int | None = None) -> dict:
    _validate_options(time_limit, stop_after)
    _new_study(scenario, study)
    return _execute(study, time_limit, stop_after, False)


def resume_study(study: Path, *, time_limit: float = 10,
                 stop_after: int | None = None) -> dict:
    return _execute(study, time_limit, stop_after, True)


def reconcile_study(study: Path) -> dict:
    with study_lock(study):
        study_manifest, scenario = _read_study(study)
        changes = _reconcile(study, study_manifest, scenario)
        selected, attempts = _selected(study, study_manifest, scenario)
        _reports(study, study_manifest, scenario, selected, attempts)
        return {**_summary(study_manifest, selected, attempts, 0), "reconciliation": changes}


def verify_study(study: Path) -> dict:
    with study_lock(study):
        study_manifest, scenario = _read_study(study)
        selected, attempts = _selected(study, study_manifest, scenario)
        from .reports import verify_reports
        verify_reports(study, selected, attempts)
        summary = _summary(study_manifest, selected, attempts, len(list((study / "pending").iterdir())))
        summary["state"] = "VERIFIED_STUDY"
        return summary


def rerun_study(source: Path, destination: Path, *, time_limit: float = 10) -> dict:
    verify_study(source)
    scenario = load_json(_inside(source, "scenario.json"))
    result = run_study(scenario, destination, time_limit=time_limit)
    return {**result, "rerun_of_scenario_sha256": digest(scenario)}

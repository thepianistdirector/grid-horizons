"""The local, declarative Grid Horizons command line.

Copyright (C) 2026 Lucas Santana. SPDX-License-Identifier: AGPL-3.0-only
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .assets import example_scenario, build_identity
from .contracts import ContractError, digest, load_json, validate_scenario


def emit(value: dict) -> None:
    print(json.dumps(value, indent=2, allow_nan=False, ensure_ascii=True))


def scenario_summary(scenario: dict) -> dict:
    return {
        "state": "VALIDATED_INPUT",
        "scenario_id": scenario["scenario_id"], "title": scenario["title"],
        "scenario_sha256": digest(scenario), "model_id": scenario["model_id"],
        "fictional": True, "nodes": scenario["network"]["nodes"],
        "intervals": scenario["intervals"], "base": scenario["base"],
        "limits": scenario["limits"], "storage": scenario["storage"],
        "policies": scenario["policies"],
        "limits_note": "Input validation is not network or storage feasibility. Run both policies and inspect evaluation.",
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        prog="grid-horizons",
        description="Offline fictional feeder studies. Approximate model only; no real-grid advice.")
    result.add_argument("--version", action="version", version="Grid Horizons " + __version__)
    sub = result.add_subparsers(dest="command", required=True)
    sub.add_parser("lab", help="AC feeder studies, sensitivity campaigns and offline workbench; lab --help")
    example = sub.add_parser("example", help="write the editable original synthetic scenario")
    example.add_argument("--output", required=True, type=Path, help="new JSON file; existing files are never overwritten")
    validate = sub.add_parser("validate", help="check scenario quantities, topology and input domain")
    validate.add_argument("scenario", type=Path)
    inspect = sub.add_parser("inspect", help="inspect the versioned scenario and declared policy")
    inspect.add_argument("scenario", type=Path, help="scenario JSON or complete study directory")
    run = sub.add_parser("run", help="run and independently evaluate both frozen policies")
    run.add_argument("scenario", type=Path)
    run.add_argument("--output", required=True, type=Path, help="new study directory")
    resume = sub.add_parser("resume", help="reconcile interrupted attempts and run unfinished policies once")
    resume.add_argument("study", type=Path)
    for command in (run, resume):
        command.add_argument("--time-limit", type=float, default=10, help="cooperative seconds per attempt, >0 and <=30")
        command.add_argument("--stop-after-intervals", type=int, help="cancel at this raw interval boundary to exercise recovery")
    verify = sub.add_parser("verify", help="verify study integrity and independently recalculate completed evidence")
    verify.add_argument("study", type=Path)
    reconcile = sub.add_parser("reconcile", help="record lost attempts or activate complete checked results, without retrying")
    reconcile.add_argument("study", type=Path)
    rerun = sub.add_parser("rerun", help="verify a study and reproduce its scenario in a new directory")
    rerun.add_argument("study", type=Path)
    rerun.add_argument("--output", required=True, type=Path)
    rerun.add_argument("--time-limit", type=float, default=10)
    evaluate = sub.add_parser("evaluate", help="independently check raw adapter JSON, including invalid-output controls")
    evaluate.add_argument("scenario", type=Path)
    evaluate.add_argument("raw", type=Path)
    evaluate.add_argument("--policy", required=True, choices=("baseline", "candidate"))
    sub.add_parser("identity", help="show the actual tool build identity")
    return result


def brief_study(summary: dict, path: Path) -> dict:
    return {"state": summary["state"], "scenario_sha256": summary["scenario_sha256"],
            "policies": {key: value["state"] for key, value in summary["policies"].items()},
            "comparison": {key: summary["comparison"][key] for key in ("state", "reason")},
            "attempt_count": summary["attempt_count"], "pending_count": summary["pending_count"],
            "report": str(path / "report.html"), "reconciliation": summary.get("reconciliation", [])}


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if arguments and arguments[0] == "lab":
        from .lab import main as lab_main
        return lab_main(arguments[1:])
    args = parser().parse_args(arguments)
    if sys.platform != "linux" or sys.implementation.name != "cpython" or sys.version_info[:2] != (3, 12):
        emit({"state": "UNSUPPORTED_ENVIRONMENT", "required": "Linux with CPython 3.12; packaged verification uses 3.12.14"})
        return 2
    from .coordinator import (StudyError, run_study, resume_study, reconcile_study,
                              verify_study, rerun_study)
    try:
        if args.command == "identity":
            emit(build_identity())
        elif args.command == "example":
            scenario = validate_scenario(example_scenario())
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(json.dumps(scenario, indent=2, allow_nan=False) + "\n")
            emit({"state": "EXAMPLE_WRITTEN", "scenario_sha256": digest(scenario)})
        elif args.command == "evaluate":
            from .contracts import MAX_RAW_BYTES
            from .evaluator import evaluate
            scenario = validate_scenario(load_json(args.scenario))
            evaluation = evaluate(scenario, load_json(args.raw, MAX_RAW_BYTES), args.policy)
            emit(evaluation)
            return 0 if evaluation["state"] == "COMPLETED_VALID" else 3
        elif args.command in {"run", "resume", "rerun", "reconcile", "verify"}:
            if args.command == "run":
                scenario = validate_scenario(load_json(args.scenario))
                summary = run_study(scenario, args.output, time_limit=args.time_limit, stop_after=args.stop_after_intervals)
                path = args.output
            elif args.command == "resume":
                summary = resume_study(args.study, time_limit=args.time_limit, stop_after=args.stop_after_intervals)
                path = args.study
            elif args.command == "rerun":
                summary = rerun_study(args.study, args.output, time_limit=args.time_limit)
                path = args.output
            else:
                summary = verify_study(args.study) if args.command == "verify" else reconcile_study(args.study)
                path = args.study
            emit(brief_study(summary, path))
            if args.command in {"verify", "reconcile"}:
                return 0
            return 0 if len(summary["policies"]) == 2 and all(
                p["state"] == "COMPLETED_VALID" for p in summary["policies"].values()) else 3
        else:
            if args.command == "inspect" and args.scenario.is_dir():
                emit(verify_study(args.scenario))
                return 0
            scenario = validate_scenario(load_json(args.scenario))
            if args.command == "inspect":
                emit(scenario_summary(scenario))
            else:
                emit({"state": "VALIDATED_INPUT", "scenario_sha256": digest(scenario),
                      "nodes": len(scenario["network"]["nodes"]),
                      "intervals": len(scenario["intervals"]),
                      "note": "Feasibility has not yet been evaluated."})
        return 0
    except ContractError as exc:
        emit({"state": "REJECTED_INPUT", "error": exc.as_dict()})
        return 2
    except StudyError as exc:
        emit({"state": "INVALID_STUDY", "error": str(exc),
              "recovery": "Preserve the study. Use its original build; resume can regenerate interrupted report views."})
        return 2
    except OSError as exc:
        emit({"state": "IO_ERROR", "error": exc.strerror,
              "recovery": "Check the input and choose a new writable output path. Existing evidence is preserved."})
        return 2


if __name__ == "__main__":
    sys.exit(main())

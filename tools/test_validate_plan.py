"""Regression tests for the dependency-free Grid Horizons plan validator."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
FOUNDATION_IDS = ("GH-F01", "GH-F02", "GH-F03")


class PlanValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary.name) / "grid-horizons"
        shutil.copytree(
            SOURCE_ROOT,
            self.root,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "runs"),
        )

    def tearDown(self) -> None:
        self._temporary.cleanup()

    @property
    def plan_path(self) -> Path:
        return self.root / "plan" / "tasks.json"

    def read_plan(self) -> dict:
        return json.loads(self.plan_path.read_text(encoding="utf-8"))

    def write_plan(self, value: object) -> None:
        self.plan_path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.root / "tools" / "validate_plan.py")],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_clean_failure(self, result: subprocess.CompletedProcess[str], message: str) -> None:
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(message, output)
        self.assertNotIn("Traceback", output)

    def test_current_plan_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: Grid Horizons plan is internally consistent", result.stdout)

    def test_non_object_root_fails_cleanly(self) -> None:
        self.write_plan([])
        self.assert_clean_failure(self.run_validator(), "document root must be an object")

    def test_malformed_dependency_containers_and_members_fail_cleanly(self) -> None:
        malformed_values: tuple[object, ...] = (
            "GH-F02",
            {"GH-F02": True},
            [{}],
            [False],
            [""],
            ["not-a-task-id"],
        )
        for malformed in malformed_values:
            with self.subTest(dependsOn=malformed):
                plan = self.read_plan()
                next(task for task in plan["tasks"] if task["id"] == "GH-F03")[
                    "dependsOn"
                ] = malformed
                self.write_plan(plan)
                self.assert_clean_failure(
                    self.run_validator(), "dependsOn must be an array of task IDs"
                )

    def test_boolean_schema_and_wave_fail_as_types(self) -> None:
        plan = self.read_plan()
        plan["schemaVersion"] = True
        self.write_plan(plan)
        self.assert_clean_failure(
            self.run_validator(), "schemaVersion must be integer 2"
        )

        plan = self.read_plan()
        plan["schemaVersion"] = 2
        next(task for task in plan["tasks"] if task["id"] == "GH-001")["wave"] = True
        self.write_plan(plan)
        self.assert_clean_failure(
            self.run_validator(), "wave must be a non-negative integer"
        )

    def test_empty_title_status_and_escaping_path_fail_cleanly(self) -> None:
        cases = (
            ("title", "", "title must be non-empty text"),
            ("status", False, "status must be non-empty text"),
            ("ownedPaths", ["../outside"], "owned path must stay inside the repository"),
        )
        for field, malformed, expected in cases:
            with self.subTest(field=field):
                plan = self.read_plan()
                next(task for task in plan["tasks"] if task["id"] == "GH-001")[field] = malformed
                self.write_plan(plan)
                self.assert_clean_failure(self.run_validator(), expected)

    def test_missing_declared_wave_header_fails_cleanly(self) -> None:
        roadmap_path = self.root / "ROADMAP.md"
        roadmap = roadmap_path.read_text(encoding="utf-8").replace(
            "## Wave 8:", "## Removed Wave 8:", 1
        )
        roadmap_path.write_text(roadmap, encoding="utf-8")
        self.assert_clean_failure(
            self.run_validator(), "ROADMAP.md is missing declared Wave 8"
        )

    def test_evidenced_foundation_done_transition_passes(self) -> None:
        plan = self.read_plan()
        for task in plan["tasks"]:
            if task["id"] in FOUNDATION_IDS:
                task["status"] = "DONE"
        self.write_plan(plan)

        tasks_path = self.root / "TASKS.md"
        tasks_text = tasks_path.read_text(encoding="utf-8")
        for task_id in FOUNDATION_IDS:
            start = tasks_text.index(f"## {task_id} ")
            end = tasks_text.find("\n## ", start + 4)
            if end < 0:
                end = len(tasks_text)
            section = tasks_text[start:end].replace(
                "status: **READY_FOR_REVIEW**;", "status: **DONE**;", 1
            )
            tasks_text = tasks_text[:start] + section + tasks_text[end:]
        tasks_path.write_text(tasks_text, encoding="utf-8")

        status_path = self.root / "STATUS.md"
        status_text = status_path.read_text(encoding="utf-8")
        for task_id in FOUNDATION_IDS:
            status_text = status_text.replace(
                f"| {task_id} | READY_FOR_REVIEW | Review candidate:",
                f"| {task_id} | DONE | Accepted evidence: reviewed revision abc123 and reproduced PASS;",
                1,
            )
        status_path.write_text(status_text, encoding="utf-8")

        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

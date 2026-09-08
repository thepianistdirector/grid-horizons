"""Regression tests for the dependency-free Grid Horizons plan validator."""

from __future__ import annotations

import json
import os
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
        temporary_root = SOURCE_ROOT / "runs" / "tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self._temporary = tempfile.TemporaryDirectory(dir=temporary_root)
        self.root = Path(self._temporary.name) / "grid-horizons"
        shutil.copytree(
            SOURCE_ROOT,
            self.root,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "runs", ".venv", "dist", "build", ".cache", "releases", "research"),
        )

        # Research outputs are read-only for plan tests. Hard links preserve full
        # navigation without copying hundreds of MiB for every negative probe.
        # Files mutated by these tests (plans/docs/tools) remain ordinary copies.
        shutil.copytree(SOURCE_ROOT / "research", self.root / "research",
                        copy_function=os.link,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

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
            self.run_validator(), "schemaVersion must be integer 3"
        )

        plan = self.read_plan()
        plan["schemaVersion"] = 3
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


    def mutate_task(self, task_id, **changes):
        plan=self.read_plan()
        next(t for t in plan["tasks"] if t["id"]==task_id).update(changes)
        self.write_plan(plan)

    def test_dangling_dependency_is_rejected(self):
        self.mutate_task("GH-S01", dependsOn=["GH-MISSING"])
        self.assert_clean_failure(self.run_validator(), "dependency GH-MISSING does not exist")

    def test_cycle_is_rejected(self):
        self.mutate_task("GH-S01", dependsOn=["GH-S02"])
        self.assert_clean_failure(self.run_validator(), "dependency cycle")

    def test_duplicate_dependency_is_rejected(self):
        self.mutate_task("GH-S01", dependsOn=["GH-F03","GH-F03"])
        self.assert_clean_failure(self.run_validator(), "duplicate dependency")

    def test_mutated_source_acceptance_is_not_hidden_by_regeneration(self):
        self.mutate_task("GH-001", acceptance="A synthetic fixture is enough to complete this public feeder task.")
        subprocess.run([sys.executable,str(self.root/"tools/render_plan.py")],cwd=self.root,check=True,capture_output=True)
        self.assert_clean_failure(self.run_validator(), "original acceptance contract changed")

    def test_missing_source_mapping_is_rejected(self):
        p=self.read_plan();p["sourceMappings"].pop();self.write_plan(p)
        self.assert_clean_failure(self.run_validator(), "missing or duplicate source mappings")

    def test_source_history_status_cannot_be_rewritten(self):
        p=self.read_plan();p["sourceMappings"][3]["sourceStatus"]="DONE";self.write_plan(p)
        self.assert_clean_failure(self.run_validator(), "source mapping history changed: sourceStatus")

    def test_source_edge_cannot_be_removed(self):
        self.mutate_task("GH-004", dependsOn=["GH-001"])
        self.assert_clean_failure(self.run_validator(), "original dependsOn contract changed")

    def test_archived_bytes_cannot_be_modified(self):
        p=self.root/"docs/lineage/foundation-2026-09-07/TASKS.md";p.chmod(0o644)
        p.write_text(p.read_text()+"\nChanged history.\n")
        self.assert_clean_failure(self.run_validator(), "immutable lineage hash mismatch: TASKS.md")

    def test_manifest_cannot_be_rebased_to_match_tampering(self):
        import hashlib
        base=self.root/"docs/lineage/foundation-2026-09-07"
        p=base/"TASKS.md";p.chmod(0o644);p.write_text(p.read_text()+"\nChanged history.\n")
        m=base/"manifest.json";m.chmod(0o644);data=json.loads(m.read_text())
        data["files"]["TASKS.md"]=hashlib.sha256(p.read_bytes()).hexdigest();m.write_text(json.dumps(data))
        self.assert_clean_failure(self.run_validator(), "immutable lineage manifest hash mismatch")

    def test_prerequisite_outcome_coverage_cannot_drift(self):
        self.mutate_task("GH-S01", dependencyCoverage={"GH-F03":"Unrelated preparation is enough."})
        self.assert_clean_failure(self.run_validator(), "prerequisite outcome coverage differs")

    def test_later_horizon_dependency_cannot_enter_01(self):
        self.mutate_task("GH-S01", dependsOn=["GH-001"])
        self.assert_clean_failure(self.run_validator(), "has a later release horizon")

    def test_duplicate_outcome_is_rejected(self):
        p=self.read_plan();value=next(t for t in p["tasks"] if t["id"]=="GH-S01")["outcome"]
        self.mutate_task("GH-S02", outcome=value)
        self.assert_clean_failure(self.run_validator(), "duplicate outcome")

    def test_orphan_and_duplicate_wave_membership_are_rejected(self):
        original=self.read_plan()
        for duplicate in (False,True):
            with self.subTest(duplicate=duplicate):
                p=json.loads(json.dumps(original));ids=p["waves"][1]["taskIds"]
                if duplicate:ids.append(ids[0])
                else:ids.pop()
                self.write_plan(p)
                self.assert_clean_failure(self.run_validator(), "orphan or duplicate wave membership")

    def test_wave_entry_contract_cannot_omit_dependency(self):
        p=self.read_plan();p["waves"][2]["entryDependencies"]=[];self.write_plan(p)
        self.assert_clean_failure(self.run_validator(), "entry dependencies differ")

    def test_wave_order_and_scope_are_checked(self):
        p=self.read_plan();p["waves"][1]["order"]=3;p["waves"][1]["targetRelease"]="long-term";self.write_plan(p)
        self.assert_clean_failure(self.run_validator(), "wave ordering must be unique")

    def test_exploratory_work_cannot_be_promised_01(self):
        self.mutate_task("GH-P18-01",targetRelease="0.1")
        self.assert_clean_failure(self.run_validator(), "exploratory scope cannot be promised delivery")

    def test_done_proposal_requires_actual_evidence(self):
        self.mutate_task("GH-S01",status="DONE",evidence=[])
        self.assert_clean_failure(self.run_validator(), "evidence-bearing state requires evidence")

    def test_fabricated_evidence_path_is_rejected(self):
        self.mutate_task("GH-S01",status="DONE",evidence=["docs/no-such-evidence.json"])
        self.assert_clean_failure(self.run_validator(), "missing or escaping evidence reference")

    def test_completed_work_cannot_outrun_prerequisite(self):
        self.mutate_task("GH-S01",status="PLANNED")
        self.mutate_task("GH-S02",status="AUTOMATED_PASS",evidence=["docs/decisions/ADR-001-synthetic-tutorial.md"])
        self.assert_clean_failure(self.run_validator(), "outruns unfinished dependency")

    def test_unmapped_native_identity_is_rejected(self):
        self.mutate_task("GH-S01",platformId="invented-native-id")
        self.assert_clean_failure(self.run_validator(), "platform ID lacks matching actual publication mapping")

    def test_publication_export_drift_is_rejected(self):
        p=self.root/"plan/publication.json";data=json.loads(p.read_text());data["counts"]["tasks"]=1;p.write_text(json.dumps(data))
        self.assert_clean_failure(self.run_validator(), "generated view drift: plan/publication.json")

    def test_malformed_extension_fields_fail_without_traceback(self):
        original=self.read_plan()
        for field,value in [("targetRelease",[]),("origin",{}),("evidence",{}),("dependencyCoverage",[]),("sourceRefs",[False]),("initialStatus",True)]:
            with self.subTest(field=field):
                self.write_plan(original);self.mutate_task("GH-S01",**{field:value})
                self.assert_clean_failure(self.run_validator(),field)

    def test_original_architecture_and_packet_checks_remain_active(self):
        p=self.root/"ARCHITECTURE.md";p.write_text(p.read_text().replace("## Units, clocks, and conservation across solvers","## Missing quantity contract"))
        self.assert_clean_failure(self.run_validator(),"ARCHITECTURE.md is missing required contract section")

    def test_broken_live_navigation_is_rejected(self):
        p=self.root/"ROADMAP.md";p.write_text(p.read_text()+"\n[Missing](docs/no-such-document.md)\n")
        self.assert_clean_failure(self.run_validator(),"broken local link")

    def test_malformed_wave_identity_fails_cleanly(self):
        p=self.read_plan();p["waves"][1]["id"]=[];self.write_plan(p)
        self.assert_clean_failure(self.run_validator(),"wave: id must be non-empty text")

    def test_dangling_successor_fails_cleanly(self):
        p=self.read_plan();p["sourceMappings"][0]["successorIds"]=["GH-NOT-THERE"];self.write_plan(p)
        self.assert_clean_failure(self.run_validator(),"missing or dangling successor mappings")

    def test_changed_source_contract_url_is_rejected(self):
        p=self.read_plan();p["sourceMappings"][0]["sourceContractUrl"]="https://example.invalid";self.write_plan(p)
        self.assert_clean_failure(self.run_validator(),"original contract URL changed")


if __name__ == "__main__":
    unittest.main()

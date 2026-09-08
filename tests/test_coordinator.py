"""Durability and recovery checks, including real killed child processes."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from grid_horizons.assets import example_scenario
from grid_horizons.contracts import ContractError, load_json
from grid_horizons.coordinator import (StudyError, run_study, resume_study, verify_study,
                                       reconcile_study, rerun_study, study_lock)
from grid_horizons.kernel import generate_intervals
from test_kernel import two_node_case


class DurableStudies(unittest.TestCase):
    def setUp(self):
        (ROOT / "runs" / "tmp").mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="coordinator-", dir=ROOT / "runs" / "tmp")
        self.base = Path(self.temporary.name)
        self.study = self.base / "study"

    def tearDown(self):
        self.temporary.cleanup()

    def hashes(self, directory):
        return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in directory.rglob("*") if p.is_file()}

    def test_complete_run_verifies_and_resume_cannot_duplicate_or_rewrite(self):
        summary = run_study(example_scenario(), self.study)
        self.assertEqual(summary["attempt_count"], 2)
        self.assertEqual(summary["comparison"]["state"], "INDETERMINATE")
        before = self.hashes(self.study / "attempts")
        resumed = resume_study(self.study)
        self.assertEqual(resumed["attempt_count"], 2)
        self.assertEqual(before, self.hashes(self.study / "attempts"))
        self.assertEqual(verify_study(self.study)["state"], "VERIFIED_STUDY")

    def test_cancellation_retains_one_interval_and_resumes_with_new_attempts(self):
        summary = run_study(example_scenario(), self.study, stop_after=1)
        self.assertEqual(summary["policies"]["baseline"]["state"], "CANCELLED")
        self.assertNotIn("candidate", summary["policies"])
        failed = next((self.study / "attempts").iterdir())
        self.assertEqual(len(load_json(failed / "raw.json")["intervals"]), 1)
        before = self.hashes(failed)
        self.assertEqual(verify_study(self.study)["comparison"]["state"], "INELIGIBLE")
        resumed = resume_study(self.study)
        self.assertEqual(resumed["attempt_count"], 3)
        self.assertEqual(before, self.hashes(failed))
        self.assertTrue(all(p["state"] == "COMPLETED_VALID" for p in resumed["policies"].values()))

    def test_resource_exhaustion_is_not_a_solver_or_evaluator_score(self):
        summary = run_study(example_scenario(), self.study, time_limit=1e-12)
        self.assertEqual(summary["policies"]["baseline"]["state"], "RESOURCE_EXHAUSTED")
        self.assertEqual(summary["policies"]["baseline"]["metrics"], {})
        self.assertEqual(resume_study(self.study)["attempt_count"], 3)

    def test_solver_failure_keeps_empty_objectives(self):
        s = two_node_case()
        s["profiles"][0]["load"]["values"] = [1000000]
        s["network"]["branches"][0]["resistance"]["value"] = .2
        summary = run_study(s, self.study)
        self.assertEqual(summary["policies"]["baseline"]["state"], "FAILED_SOLVER")
        self.assertEqual(summary["policies"]["candidate"]["metrics"], {})
        verify_study(self.study)

    def test_evaluator_crash_is_distinct_and_recoverable(self):
        with patch("grid_horizons.evaluator.evaluate", side_effect=RuntimeError("test evaluator failure")):
            summary = run_study(example_scenario(), self.study)
        self.assertEqual(summary["policies"]["baseline"]["state"], "FAILED_EVALUATOR")
        self.assertEqual(summary["comparison"]["differences"], {})
        self.assertEqual(resume_study(self.study)["attempt_count"], 4)

    def test_structurally_invalid_raw_is_durable_without_metrics(self):
        def damaged(s, policy_id):
            for row in generate_intervals(s, policy_id):
                row["nodes"].pop()
                yield row
        with patch("grid_horizons.coordinator.generate_intervals", side_effect=damaged):
            summary = run_study(example_scenario(), self.study)
        self.assertEqual(summary["policies"]["baseline"]["state"], "INVALID_RESULT")
        self.assertEqual(summary["policies"]["baseline"]["metrics"], {})
        verify_study(self.study)

    def test_infeasible_candidate_is_retained_not_automatically_retried(self):
        s = example_scenario()
        s["storage"]["capacity"]["value"] = 40000000
        summary = run_study(s, self.study)
        self.assertEqual(summary["policies"]["candidate"]["state"], "COMPLETED_INFEASIBLE")
        self.assertEqual(summary["comparison"]["state"], "INELIGIBLE")
        self.assertEqual(resume_study(self.study)["attempt_count"], 2)

    def test_existing_destination_and_invalid_input_never_overwrite(self):
        self.study.mkdir()
        (self.study / "owned.txt").write_text("pre-existing")
        with self.assertRaises(FileExistsError): run_study(example_scenario(), self.study)
        self.assertEqual((self.study / "owned.txt").read_text(), "pre-existing")
        bad = example_scenario()
        bad["storage"]["capacity"]["value"] = -1
        destination = self.base / "rejected"
        with self.assertRaises(ContractError): run_study(bad, destination)
        self.assertFalse(destination.exists())

    def test_scenario_raw_and_terminal_tampering_are_detected(self):
        for name in ("scenario", "raw", "result"):
            with self.subTest(artifact=name):
                study = self.base / name
                run_study(example_scenario(), study)
                file = study / "scenario.json" if name == "scenario" else next((study / "attempts").iterdir()) / (name + ".json")
                data = file.read_bytes()
                file.write_bytes(data + b" ")
                if name == "scenario":
                    # Semantic scenario identity deliberately ignores whitespace.
                    altered = json.loads(data)
                    altered["profiles"][0]["load"]["values"][0] += 1
                    file.write_text(json.dumps(altered))
                with self.assertRaises(StudyError): verify_study(study)

    def test_derived_report_damage_can_be_repaired_without_changing_attempts(self):
        run_study(example_scenario(), self.study)
        before = self.hashes(self.study / "attempts")
        (self.study / "report.html").write_text("interrupted view")
        with self.assertRaisesRegex(StudyError, "Derived report view"):
            verify_study(self.study)
        resume_study(self.study)
        verify_study(self.study)
        self.assertEqual(before, self.hashes(self.study / "attempts"))

    def test_rerun_preserves_scenario_and_metrics_with_new_attempt_identities(self):
        first = run_study(example_scenario(), self.study)
        second = rerun_study(self.study, self.base / "rerun")
        self.assertEqual(first["scenario_sha256"], second["scenario_sha256"])
        for policy in ("baseline", "candidate"):
            self.assertEqual(first["policies"][policy]["metrics"], second["policies"][policy]["metrics"])
            self.assertNotEqual(first["policies"][policy]["attempt_id"], second["policies"][policy]["attempt_id"])

    def test_symlinked_input_evidence_is_not_followed(self):
        run_study(example_scenario(), self.study)
        path = self.study / "scenario.json"
        saved = self.base / "outside-scenario.json"
        path.rename(saved)
        path.symlink_to(saved)
        with self.assertRaisesRegex(StudyError, "symlink"):
            verify_study(self.study)

    def test_a_live_coordinator_excludes_a_second_writer(self):
        run_study(example_scenario(), self.study)
        code = "from pathlib import Path; from grid_horizons.coordinator import study_lock; import sys\nwith study_lock(Path(sys.argv[1])):\n print('locked',flush=True)\n sys.stdin.read()\n"
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "TMPDIR": str(self.base)}
        with subprocess.Popen([sys.executable, "-c", code, str(self.study)], cwd=ROOT, env=env,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            self.assertEqual(process.stdout.readline().strip(), "locked")
            try:
                with self.assertRaisesRegex(StudyError, "Another coordinator"):
                    resume_study(self.study)
            finally:
                process.communicate(input="", timeout=5)

    def kill_at(self, phase):
        code = r'''
import os,signal,sys
from pathlib import Path
from grid_horizons import coordinator as c
from grid_horizons.assets import example_scenario
phase=sys.argv[2]
if phase in ('interval','trailing'):
 original=c.generate_intervals
 def interrupted(s,p):
  for row in original(s,p):
   yield row
   if phase=='trailing':
    directory=next((Path(sys.argv[1])/'pending').iterdir())
    with (directory/'raw.ndjson').open('ab') as f:
     f.write(b'{"partial":');f.flush();os.fsync(f.fileno())
   os.kill(os.getpid(),signal.SIGKILL)
 c.generate_intervals=interrupted
elif phase=='before_activation':
 c._seal_and_publish=lambda *a:os.kill(os.getpid(),signal.SIGKILL)
elif phase=='after_seal':
 original=c.os.rename
 def rename(a,b):
  if Path(b).parent.name=='attempts':os.kill(os.getpid(),signal.SIGKILL)
  return original(a,b)
 c.os.rename=rename
elif phase=='after_activation':
 original=c._event
 def event(study,event,**kw):
  if event=='ATTEMPT_PUBLISHED':os.kill(os.getpid(),signal.SIGKILL)
  return original(study,event,**kw)
 c._event=event
c.run_study(example_scenario(),Path(sys.argv[1]))
'''
        return subprocess.run([sys.executable, "-c", code, str(self.study), phase], cwd=ROOT,
                              env={**os.environ, "PYTHONPATH": str(ROOT / "src"), "TMPDIR": str(self.base)},
                              text=True, capture_output=True, timeout=10)

    def test_real_process_loss_retains_raw_and_requires_explicit_reconciliation(self):
        process = self.kill_at("interval")
        self.assertEqual(process.returncode, -9, process.stderr)
        self.assertEqual(len(list((self.study / "attempts").iterdir())), 0)
        summary = reconcile_study(self.study)
        self.assertEqual(summary["policies"]["baseline"]["state"], "LOST")
        self.assertEqual(summary["attempt_count"], 1)
        self.assertEqual(resume_study(self.study)["attempt_count"], 3)
        verify_study(self.study)

    def test_truncated_journal_never_becomes_a_complete_interval(self):
        self.assertEqual(self.kill_at("trailing").returncode, -9)
        result = resume_study(self.study)
        self.assertEqual(result["attempt_count"], 3)
        lost = next(r for r in result["retained_attempts"] if r["state"] == "LOST")
        directory = self.study / "attempts" / lost["attempt_id"]
        self.assertEqual(len(load_json(directory / "raw.json")["intervals"]), 1)
        self.assertTrue((directory / "raw.ndjson").read_bytes().endswith(b'{"partial":'))
        verify_study(self.study)

    def test_complete_preactivation_results_reconcile_without_duplicate_completion(self):
        for phase in ("before_activation", "after_seal", "after_activation"):
            with self.subTest(phase=phase):
                self.study = self.base / phase
                self.assertEqual(self.kill_at(phase).returncode, -9)
                resumed = resume_study(self.study)
                self.assertEqual(resumed["attempt_count"], 2)
                self.assertEqual(resumed["pending_count"], 0)
                self.assertEqual(resume_study(self.study)["attempt_count"], 2)
                verify_study(self.study)


if __name__ == "__main__":
    unittest.main()

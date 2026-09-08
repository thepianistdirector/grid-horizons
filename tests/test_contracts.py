"""Invariant and mutation checks for original synthetic declarative input."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from grid_horizons.assets import example_scenario
from grid_horizons.contracts import ContractError, decode_json, digest, validate_scenario


class ScenarioContracts(unittest.TestCase):
    def setUp(self):
        self.s = example_scenario()

    def reject(self, message):
        with self.assertRaisesRegex(ContractError, message):
            validate_scenario(self.s)

    def test_original_is_valid_and_validation_never_repairs(self):
        before = copy.deepcopy(self.s)
        validate_scenario(self.s)
        self.assertEqual(self.s, before)

    def test_explicit_unit_and_quantity_meaning_are_binding(self):
        for field, bad in (("unit", "kW"), ("basis", "single_phase"),
                           ("sign", "injection_positive"), ("location", "workshop"),
                           ("support", "instantaneous")):
            with self.subTest(field=field):
                self.s = example_scenario()
                self.s["profiles"][0]["load"][field] = bad
                self.reject("must equal")

    def test_missing_unknown_and_nonfinite_quantities_fail(self):
        for bad in (True, "10000", None, float("nan"), float("inf")):
            with self.subTest(bad=bad):
                self.s = example_scenario()
                self.s["profiles"][0]["load"]["values"][0] = bad
                self.reject("finite")
        self.s = example_scenario()
        self.s["solver"] = "external"
        self.reject("unknown fields")
        del self.s["solver"]
        del self.s["profiles"][0]["load"]["unit"]
        self.reject("missing fields")

    def test_duplicate_json_keys_and_non_json_numbers_fail(self):
        for value in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}'):
            with self.subTest(value=value), self.assertRaises(ContractError):
                decode_json(value)

    def test_deep_or_oversized_json_has_clean_error(self):
        for value in (b"[" * 1500 + b"0" + b"]" * 1500, b" " * (1024 * 1024 + 1)):
            with self.subTest(size=len(value)), self.assertRaises(ContractError):
                decode_json(value)

    def test_dangling_and_disconnected_cycle_fail(self):
        self.s["network"]["branches"][1]["child"] = "ghost"
        self.reject("dangling")
        self.s = example_scenario()
        self.s["network"]["branches"][0]["parent"] = "workshop"
        self.reject("cycles")

    def test_multiple_parents_and_duplicate_nodes_fail(self):
        self.s["network"]["branches"][1]["child"] = "orchard"
        self.reject("parent")
        self.s = example_scenario()
        self.s["network"]["nodes"][2] = "orchard"
        self.reject("unique")

    def test_intervals_and_profiles_are_complete_and_contiguous(self):
        for change in ("overlap", "gap", "zero", "id", "bool", "short"):
            with self.subTest(change=change):
                self.s = example_scenario()
                if change == "overlap": self.s["intervals"][1]["start_s"] = 3599
                if change == "gap": self.s["intervals"][1]["start_s"] = 3601
                if change == "zero": self.s["intervals"][1]["end_s"] = 3600
                if change == "id": self.s["intervals"][1]["id"] = "i0"
                if change == "bool": self.s["intervals"][0]["start_s"] = False
                if change == "short": self.s["profiles"][0]["load"]["values"].pop()
                self.reject("interval|entries")

    def test_input_capacity_initial_state_and_efficiency_must_be_possible(self):
        for name, value in (("capacity", -1), ("initial_energy", 72000001),
                            ("charge_efficiency", 0), ("discharge_efficiency", 1.01)):
            with self.subTest(name=name):
                self.s = example_scenario()
                self.s["storage"][name]["value"] = value
                self.reject("finite|exceeds")

    def test_feasibility_mutants_are_retained_for_evaluation(self):
        self.s["storage"]["capacity"]["value"] = 40000000
        self.s["network"]["branches"][0]["rating"]["value"] = 50000
        self.s["policies"][1]["schedule"]["values"][1] = 12001
        before = copy.deepcopy(self.s)
        validate_scenario(self.s)
        self.assertEqual(self.s, before)

    def test_baseline_policy_and_final_state_obligation_cannot_be_relaxed(self):
        self.s["policies"][0]["schedule"]["values"][0] = 100
        self.reject("idle baseline")
        self.s = example_scenario()
        self.s["storage"]["require_final_equal_initial"] = False
        self.reject("must equal True")

    def test_curtailment_never_exceeds_available_potential(self):
        self.s["profiles"][1]["curtailment"]["values"][1] = 50001
        self.reject("curtailment")

    def test_digest_tracks_execution_changes_and_ignores_json_key_order(self):
        reordered = json.loads(json.dumps(self.s, sort_keys=True))
        self.assertEqual(digest(self.s), digest(reordered))
        reordered["profiles"][0]["load"]["values"][0] += 1
        self.assertNotEqual(digest(self.s), digest(reordered))


if __name__ == "__main__":
    unittest.main()

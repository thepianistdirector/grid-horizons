"""Hand-derived controls, not producer-generated numerical references."""

from __future__ import annotations

import copy
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from grid_horizons.assets import example_scenario
from grid_horizons.kernel import generate, SolverFailure


def two_node_case():
    s = example_scenario()
    s["network"]["nodes"] = ["grid", "workshop"]
    s["network"]["branches"] = [s["network"]["branches"][1]]
    branch = s["network"]["branches"][0]
    branch["parent"] = "grid"
    branch["resistance"]["value"] = .01
    branch["reactance"]["value"] = .02
    s["profiles"] = [s["profiles"][1]]
    s["intervals"] = [s["intervals"][0]]
    profile = s["profiles"][0]
    for field, value in (("load", 10000), ("reactive_load", 2000),
                         ("generation_available", 0), ("curtailment", 0)):
        profile[field]["values"] = [value]
    for policy in s["policies"]:
        policy["schedule"]["values"] = [0]
    return s


class NumericalControls(unittest.TestCase):
    def test_two_node_hand_answer_preserves_squared_voltage_and_power(self):
        raw = generate(two_node_case(), "baseline")["intervals"][0]
        self.assertAlmostEqual(raw["nodes"][1]["voltage_squared"]["value"], .9972, delta=1e-12)
        self.assertEqual(raw["branches"][0]["real_power"]["value"], 10000)
        self.assertEqual(raw["branches"][0]["reactive_power"]["value"], 2000)
        self.assertEqual(raw["grid"]["import_power"]["value"] * 3600, 36000000)

    def test_no_load_reference_on_three_nodes(self):
        s = example_scenario()
        for profile in s["profiles"]:
            for field in ("load", "reactive_load", "generation_available", "curtailment"):
                profile[field]["values"] = [0] * 4
        for record in generate(s, "baseline")["intervals"]:
            for node in record["nodes"]:
                self.assertEqual(node["voltage_squared"]["value"], 1)
            for branch in record["branches"]:
                self.assertEqual(branch["real_power"]["value"], 0)
                self.assertEqual(branch["reactive_power"]["value"], 0)

    def test_storage_reference_efficiency_direction_and_loss(self):
        rows = generate(example_scenario(), "candidate")["intervals"]
        self.assertAlmostEqual(rows[1]["storage"]["energy_end"]["value"], 68400000, delta=1e-6)
        self.assertAlmostEqual(rows[2]["storage"]["energy_end"]["value"], 36000000, delta=1e-6)
        self.assertAlmostEqual(sum(r["storage"]["conversion_loss"]["value"] for r in rows),
                               6840000, delta=1e-6)

    def test_paired_full_case_reference_and_pure_reexecution(self):
        s = example_scenario()
        before = copy.deepcopy(s)
        for policy, powers, imported, exported in (
                ("baseline", [32000, -10000, 54000, 42000], 128, 10),
                ("candidate", [32000, 0, 45900, 42000], 119.9, 0)):
            raw = generate(s, policy)
            rows = raw["intervals"]
            net = [r["grid"]["import_power"]["value"] - r["grid"]["export_power"]["value"] for r in rows]
            self.assertEqual(net, powers)
            self.assertAlmostEqual(sum(r["grid"]["import_power"]["value"] for r in rows) / 1000,
                                   imported, delta=1e-12)
            self.assertAlmostEqual(sum(r["grid"]["export_power"]["value"] for r in rows) / 1000,
                                   exported, delta=1e-12)
            self.assertEqual(raw, generate(s, policy))
        self.assertEqual(s, before)
        candidate = generate(s, "candidate")["intervals"][1]
        self.assertEqual(candidate["grid"]["import_power"]["value"], 0)
        self.assertEqual(candidate["grid"]["reactive_power"]["value"], 7600)

    def test_nonuniform_intervals_integrate_actual_duration(self):
        s = example_scenario()
        starts = [0, 1800, 3600, 9000]
        ends = [1800, 3600, 9000, 10800]
        for interval, start, end in zip(s["intervals"], starts, ends):
            interval.update(start_s=start, end_s=end)
        rows = generate(s, "candidate")["intervals"]
        # Half-hour charge stores 4.5 kWh; 1.5-hour discharge removes 13.5 kWh.
        self.assertAlmostEqual(rows[-1]["storage"]["energy_end"]["value"], 3600000, delta=1e-6)

    def test_reordered_tree_is_not_a_topological_input_requirement(self):
        s = example_scenario()
        expected = generate(s, "candidate")
        s["network"]["nodes"].reverse()
        s["network"]["branches"].reverse()
        actual = generate(s, "candidate")
        for a, b in zip(expected["intervals"], actual["intervals"]):
            self.assertEqual({n["node_id"]: n for n in a["nodes"]},
                             {n["node_id"]: n for n in b["nodes"]})
            self.assertEqual(a["grid"], b["grid"])

    def test_infeasible_storage_is_not_silently_clipped(self):
        s = example_scenario()
        s["storage"]["capacity"]["value"] = 40000000
        s["policies"][1]["schedule"]["values"] = [0, 20000, -30000, 0]
        rows = generate(s, "candidate")["intervals"]
        self.assertEqual(rows[1]["storage"]["charge"]["value"], 20000)
        self.assertGreater(rows[1]["storage"]["energy_end"]["value"], 40000000)
        self.assertLess(rows[2]["storage"]["energy_end"]["value"], 0)

    def test_nonpositive_voltage_is_a_solver_failure(self):
        s = two_node_case()
        s["profiles"][0]["load"]["values"] = [1000000]
        s["network"]["branches"][0]["resistance"]["value"] = .2
        with self.assertRaisesRegex(SolverFailure, "no positive squared voltage"):
            generate(s, "baseline")

    def test_perturbed_reference_is_detectable(self):
        raw = generate(two_node_case(), "baseline")["intervals"][0]
        observed = raw["nodes"][1]["voltage_squared"]["value"]
        self.assertFalse(math.isclose(observed, .9973, rel_tol=0, abs_tol=1e-12))


if __name__ == "__main__":
    unittest.main()

"""Independent references and predeclared falsifiers for raw evidence admission.

Copyright (C) 2026 Lucas Santana. SPDX-License-Identifier: AGPL-3.0-only
"""
from __future__ import annotations

import copy
import math
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from grid_horizons import MODEL_ID, RAW_SCHEMA
from grid_horizons.assets import example_scenario
from grid_horizons.contracts import ContractError, digest
from grid_horizons.evaluator import METRIC_UNITS, compare, evaluate
from grid_horizons.kernel import generate
from grid_horizons.raw_contract import NODE_FIELDS, BRANCH_FIELDS, STORAGE_FIELDS, GRID_FIELDS


def hand_two_node():
    """Raw reference constructed without invoking the producer at any point."""
    s = example_scenario()
    s["network"]["nodes"] = ["grid", "workshop"]
    s["network"]["branches"] = [s["network"]["branches"][1]]
    b = s["network"]["branches"][0]
    b["parent"] = "grid"
    b["resistance"]["value"], b["reactance"]["value"] = .01, .02
    s["profiles"] = [s["profiles"][1]]
    s["intervals"] = [s["intervals"][0]]
    for field, value in (("load", 10000), ("reactive_load", 2000), ("generation_available", 0), ("curtailment", 0)):
        s["profiles"][0][field]["values"] = [value]
    for policy in s["policies"]:
        policy["schedule"]["values"] = [0]
    interval = s["intervals"][0]

    def quantities(specs, location, values):
        result = {}
        for field, (unit, basis, sign, aggregation) in specs.items():
            result[field] = {"value": values.get(field, 0), "unit": unit, "basis": basis,
                "sign": sign, "location": location, "support": {"interval_id": "i0", "start_s": 0,
                "end_s": 3600, "aggregation": aggregation}}
        return result

    nodes = [{"node_id": "grid", **quantities(NODE_FIELDS, "grid", {"voltage_squared": 1})},
             {"node_id": "workshop", **quantities(NODE_FIELDS, "workshop",
              {"voltage_squared": .9972, "load": 10000, "served_load": 10000, "reactive_load": 2000})}]
    branch = {"branch_id": b["id"], **quantities(BRANCH_FIELDS, b["id"],
              {"real_power": 10000, "reactive_power": 2000, "loading": math.sqrt(104000000) / 40000})}
    record = {**interval, "nodes": nodes, "branches": [branch],
        "storage": quantities(STORAGE_FIELDS, "workshop", {"energy_start": 36000000, "energy_end": 36000000}),
        "grid": quantities(GRID_FIELDS, "grid", {"import_power": 10000, "reactive_power": 2000})}
    return s, {"schema_version": RAW_SCHEMA, "scenario_sha256": digest(s), "model_id": MODEL_ID,
               "policy_id": "baseline", "intervals": [record]}


class IndependentEvaluator(unittest.TestCase):
    def setUp(self):
        self.scenario = example_scenario()
        self.raw = generate(self.scenario, "candidate")

    def invalid(self, raw, code=None, scenario=None, policy="candidate"):
        r = evaluate(self.scenario if scenario is None else scenario, raw, policy)
        self.assertEqual(r["state"], "INVALID_RESULT", r)
        self.assertFalse(r["comparison_eligible"])
        self.assertEqual(r["metrics"], {})
        if code:
            self.assertIn(code, {f["code"] for f in r["findings"]})
        return r

    def test_independent_hand_reference_and_no_producer_call(self):
        s, raw = hand_two_node()
        with patch("grid_horizons.kernel.generate", side_effect=AssertionError("producer is forbidden")):
            r = evaluate(s, raw, "baseline")
        self.assertEqual(r["state"], "COMPLETED_VALID", r["findings"])
        self.assertEqual(r["metrics"]["served_load_energy"]["value"], 36000000)
        self.assertAlmostEqual(r["metrics"]["min_voltage"]["value"], math.sqrt(.9972), delta=1e-12)
        self.assertEqual(r["ledger"]["max_reactive_node_residual"]["unit"], "var")
        self.assertEqual(r["ledger"]["max_real_node_residual"]["unit"], "W")
        self.assertEqual(r["ledger"]["real_energy_residual"]["unit"], "J")
        self.assertFalse(any(q["unit"] == "var" for q in r["metrics"].values()))

    def test_full_case_hand_totals_and_quantity_metadata(self):
        for policy, imported, exported, peak, loss in (("baseline", 128, 10, 54000, 0),
                                                       ("candidate", 119.9, 0, 45900, 6840000)):
            with self.subTest(policy=policy):
                r = evaluate(self.scenario, generate(self.scenario, policy), policy)
                self.assertEqual(r["state"], "COMPLETED_VALID", r["findings"])
                m = r["metrics"]
                self.assertEqual(set(m), set(METRIC_UNITS))
                for key, expected in (("import_energy", imported * 3600000), ("export_energy", exported * 3600000),
                    ("served_load_energy", 626400000), ("injected_generation_energy", 201600000),
                    ("curtailed_potential_energy", 7200000), ("storage_conversion_loss", loss),
                    ("peak_import_power", peak), ("initial_storage_energy", 36000000), ("final_storage_energy", 36000000)):
                    self.assertAlmostEqual(m[key]["value"], expected, delta=1e-6)
                for key, q in m.items():
                    self.assertEqual(set(q), {"value", "unit", "basis", "sign", "location", "support"})
                    self.assertEqual(q["unit"], METRIC_UNITS[key])
                    self.assertEqual(q["support"]["start_s"], 0)
                    self.assertEqual(q["support"]["end_s"], 14400)

    def test_predeclared_equation_mutations(self):
        for section, field, amount, code in (("branches", "real_power", 1, "REAL_NODE_BALANCE"),
            ("branches", "reactive_power", 1, "REACTIVE_NODE_BALANCE"),
            ("nodes", "voltage_squared", .0001, "VOLTAGE_DROP"),
            ("storage", "energy_end", 3600, "STORAGE_TRANSITION"),
            ("storage", "energy_start", 3600, "STORAGE_CONTINUITY"),
            ("storage", "conversion_loss", 1, "STORAGE_CONVERSION"),
            ("branches", "loading", .001, "LOADING_IDENTITY"),
            ("grid", "import_power", 1, "REAL_NODE_BALANCE"),
            ("grid", "reactive_power", 1, "REACTIVE_NODE_BALANCE")):
            with self.subTest(section=section, field=field):
                raw = copy.deepcopy(self.raw)
                record = raw["intervals"][0][section]
                if isinstance(record, list):
                    record = record[-1]
                record[field]["value"] += amount
                self.invalid(raw, code)

    def test_curtailment_never_counts_as_injected_generation(self):
        for delta in (2000, -2000):
            raw = copy.deepcopy(self.raw)
            raw["intervals"][1]["nodes"][-1]["generation_injected"]["value"] += delta
            self.invalid(raw, "GENERATION_IDENTITY")

    def test_served_and_unserved_cannot_hide_demand(self):
        raw = copy.deepcopy(self.raw)
        node = raw["intervals"][0]["nodes"][-1]
        node["served_load"]["value"] -= 100
        node["unserved_load"]["value"] += 100
        self.invalid(raw, "NO_SHEDDING")

    def test_coherent_wrong_policy_is_invalid(self):
        changed = copy.deepcopy(self.scenario)
        changed["policies"][1]["schedule"]["values"] = [0, 5000, -4050, 0]
        wrong = generate(changed, "candidate")
        wrong["scenario_sha256"] = digest(self.scenario)
        r = self.invalid(wrong, "POLICY_DISPATCH")
        self.assertFalse(any(f["code"].endswith("BALANCE") for f in r["findings"]))

    def test_coherent_wrong_profile_is_invalid(self):
        changed = copy.deepcopy(self.scenario)
        changed["profiles"][0]["load"]["values"][0] += 100
        wrong = generate(changed, "candidate")
        wrong["scenario_sha256"] = digest(self.scenario)
        self.invalid(wrong, "PROFILE_BINDING")

    def test_complete_unique_coverage_required(self):
        mutations = [lambda r: r["intervals"].pop(),
                     lambda r: r["intervals"][0]["nodes"].pop(),
                     lambda r: r["intervals"][0]["branches"].pop(),
                     lambda r: r["intervals"][0]["storage"].pop("conversion_loss"),
                     lambda r: r["intervals"][0]["nodes"].__setitem__(1, r["intervals"][0]["nodes"][0]),
                     lambda r: r["intervals"].reverse()]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                raw = copy.deepcopy(self.raw)
                mutation(raw)
                self.invalid(raw, "RAW_CONTRACT")

    def test_all_quantity_metadata_is_binding(self):
        for field, value in (("unit", "kW"), ("basis", "single_phase"), ("sign", "reverse"),
                             ("location", "orchard"), ("support", "mean")):
            with self.subTest(field=field):
                raw = copy.deepcopy(self.raw)
                raw["intervals"][0]["storage"]["charge"][field] = value
                self.invalid(raw, "RAW_CONTRACT")
        for field, value in (("aggregation", "integral"), ("end_s", 3601), ("interval_id", "i1"), ("start_s", False)):
            raw = copy.deepcopy(self.raw)
            raw["intervals"][0]["storage"]["charge"]["support"][field] = value
            self.invalid(raw, "RAW_CONTRACT")

    def test_interval_endpoints_are_exact_integer_seconds(self):
        for value in (3601, 3600.0, True):
            raw = copy.deepcopy(self.raw)
            raw["intervals"][0]["end_s"] = value
            self.invalid(raw, "RAW_CONTRACT")

    def test_malformed_json_objects_are_invalid_not_internal_failures(self):
        for raw in (None, [], 1, True, "raw", {}, {"intervals": None}):
            self.invalid(raw, "RAW_CONTRACT")
        for value in (float("nan"), float("inf"), -float("inf"), True, "10000", None, [], {}, 10 ** 400):
            with self.subTest(value=repr(value)[:30]):
                raw = copy.deepcopy(self.raw)
                raw["intervals"][0]["storage"]["charge"]["value"] = value
                self.invalid(raw, "RAW_CONTRACT")
        for value in (None, [], 4, "nodes"):
            raw = copy.deepcopy(self.raw)
            raw["intervals"][0]["nodes"] = value
            self.invalid(raw, "RAW_CONTRACT")
        raw = copy.deepcopy(self.raw)
        raw["trusted_pass"] = True
        self.invalid(raw, "RAW_CONTRACT")

    def test_scenario_error_propagates_separately(self):
        self.scenario["profiles"][0]["load"]["unit"] = "kW"
        with self.assertRaises(ContractError):
            evaluate(self.scenario, self.raw, "candidate")

    def test_unexpected_internal_checker_error_propagates(self):
        with patch("grid_horizons.evaluator._read_raw", side_effect=RuntimeError("checker defect")):
            with self.assertRaisesRegex(RuntimeError, "checker defect"):
                evaluate(self.scenario, self.raw, "candidate")

    def test_modeled_infeasibility_retains_metrics_and_diagnostics(self):
        controls = (
            (lambda s: s["network"]["branches"][0]["rating"].update(value=50000), "baseline", "BRANCH_RATING"),
            (lambda s: s["limits"]["voltage_min"].update(value=.99), "baseline", "VOLTAGE_LIMIT"),
            (lambda s: s["storage"]["capacity"].update(value=40000000), "candidate", "STORAGE_ENERGY"),
            (lambda s: s["policies"][1]["schedule"]["values"].__setitem__(1, 12001), "candidate", "STORAGE_POWER"),
            (lambda s: s["policies"][1]["schedule"]["values"].__setitem__(2, -20000), "candidate", "FINAL_STORAGE_EQUALITY"),
        )
        for edit, policy, code in controls:
            with self.subTest(code=code):
                s = example_scenario()
                edit(s)
                r = evaluate(s, generate(s, policy), policy)
                self.assertEqual(r["state"], "COMPLETED_INFEASIBLE", r["findings"])
                self.assertFalse(r["comparison_eligible"])
                self.assertEqual(set(r["metrics"]), set(METRIC_UNITS))
                self.assertIn(code, {f["code"] for f in r["findings"]})

    def test_each_arm_gets_own_feasibility_check(self):
        self.scenario["network"]["branches"][0]["rating"]["value"] = 50000
        r = [evaluate(self.scenario, generate(self.scenario, p), p) for p in ("baseline", "candidate")]
        self.assertEqual([x["state"] for x in r], ["COMPLETED_INFEASIBLE", "COMPLETED_VALID"])
        self.assertEqual(compare(r)["state"], "INELIGIBLE")

    def test_zero_case_and_unity_efficiency(self):
        for profile in self.scenario["profiles"]:
            for field in ("load", "reactive_load", "generation_available", "curtailment"):
                profile[field]["values"] = [0] * 4
        r = evaluate(self.scenario, generate(self.scenario, "baseline"), "baseline")
        self.assertEqual(r["state"], "COMPLETED_VALID")
        self.assertEqual(r["metrics"]["import_energy"]["value"], 0)
        self.assertEqual(r["metrics"]["min_voltage"]["value"], 1)
        self.scenario["storage"]["charge_efficiency"]["value"] = 1
        self.scenario["storage"]["discharge_efficiency"]["value"] = 1
        self.scenario["policies"][1]["schedule"]["values"] = [0, 1000, -1000, 0]
        r = evaluate(self.scenario, generate(self.scenario, "candidate"), "candidate")
        self.assertEqual(r["state"], "COMPLETED_VALID")
        self.assertEqual(r["metrics"]["storage_conversion_loss"]["value"], 0)

    def test_nonuniform_duration_reference_and_final_equality(self):
        for interval, start, end in zip(self.scenario["intervals"], [0, 1800, 3600, 9000], [1800, 3600, 9000, 10800]):
            interval.update(start_s=start, end_s=end)
        r = evaluate(self.scenario, generate(self.scenario, "candidate"), "candidate")
        self.assertEqual(r["state"], "COMPLETED_INFEASIBLE")
        self.assertAlmostEqual(r["metrics"]["final_storage_energy"]["value"], 3600000, delta=1e-6)
        self.assertAlmostEqual(r["metrics"]["import_energy"]["value"], 381060000, delta=1e-6)
        self.assertIn("FINAL_STORAGE_EQUALITY", {f["code"] for f in r["findings"]})

    def test_ordering_is_not_topology(self):
        self.scenario["network"]["nodes"].reverse()
        self.scenario["network"]["branches"].reverse()
        raw = generate(self.scenario, "candidate")
        for row in raw["intervals"]:
            row["nodes"].reverse()
            row["branches"].reverse()
        r = evaluate(self.scenario, raw, "candidate")
        self.assertEqual(r["state"], "COMPLETED_VALID", r["findings"])
        self.assertEqual(r["metrics"]["import_energy"]["value"], 431640000)

    def test_comparison_no_winner_and_identity_gates(self):
        results = [evaluate(self.scenario, generate(self.scenario, p), p) for p in ("baseline", "candidate")]
        c = compare(results)
        self.assertEqual(c["state"], "INDETERMINATE")
        self.assertEqual(c["differences"]["peak_import_power"]["value"], -8100)
        self.assertEqual(c["differences"]["net_import_energy"]["value"], 6840000)
        self.assertEqual(c["differences"]["net_import_energy"]["unit"], "J")
        for field in ("scenario_sha256", "model_id", "evaluator_version", "schema_version", "policy_id"):
            wrong = copy.deepcopy(results)
            wrong[1][field] = "wrong"
            self.assertEqual(compare(wrong)["state"], "INELIGIBLE")
        for state in ("INVALID_RESULT", "FAILED_EVALUATOR", "FAILED_SOLVER", "CANCELLED", "COMPLETED_INFEASIBLE"):
            wrong = copy.deepcopy(results)
            wrong[1]["state"] = state
            self.assertEqual(compare(wrong)["state"], "INELIGIBLE")
        self.assertEqual(compare([results[0], results[0]])["state"], "INELIGIBLE")
        self.assertEqual(compare(results[:1])["state"], "INELIGIBLE")

    def test_model_domain_is_a_separate_infeasibility(self):
        s, _ = hand_two_node()
        s["network"]["root_voltage"]["value"] = .9
        s["limits"]["voltage_min"]["value"] = .9
        r = evaluate(s, generate(s, "baseline"), "baseline")
        self.assertEqual(r["state"], "COMPLETED_INFEASIBLE")
        self.assertIn("MODEL_DOMAIN_VOLTAGE", {f["code"] for f in r["findings"]})

    def test_exact_voltage_boundary_roundoff_allowance(self):
        for squared_gap, state in ((5e-11, "COMPLETED_VALID"), (2e-10, "COMPLETED_INFEASIBLE")):
            s, _ = hand_two_node()
            s["limits"]["voltage_min"]["value"] = math.sqrt(.9972 + squared_gap)
            r = evaluate(s, generate(s, "baseline"), "baseline")
            self.assertEqual(r["state"], state, r["findings"])

    def test_exact_rating_boundary_roundoff_allowance(self):
        for difference, state in ((1e-7, "COMPLETED_VALID"), (1e-4, "COMPLETED_INFEASIBLE")):
            s, _ = hand_two_node()
            s["network"]["branches"][0]["rating"]["value"] = math.sqrt(104000000) - difference
            r = evaluate(s, generate(s, "baseline"), "baseline")
            self.assertEqual(r["state"], state, r["findings"])

    def test_final_equality_roundoff_allowance(self):
        for dispatch_change, state in ((1e-7, "COMPLETED_VALID"), (1e-5, "COMPLETED_INFEASIBLE")):
            s = example_scenario()
            s["policies"][1]["schedule"]["values"][1] += dispatch_change
            r = evaluate(s, generate(s, "candidate"), "candidate")
            self.assertEqual(r["state"], state, r["findings"])

    def test_nonpositive_voltage_and_simultaneous_exchange_are_invalid(self):
        raw = copy.deepcopy(self.raw)
        raw["intervals"][0]["nodes"][-1]["voltage_squared"]["value"] = 0
        self.invalid(raw, "NONPOSITIVE_VOLTAGE")
        raw = copy.deepcopy(self.raw)
        raw["intervals"][0]["grid"]["import_power"]["value"] += 1000
        raw["intervals"][0]["grid"]["export_power"]["value"] += 1000
        self.invalid(raw, "GRID_EXCHANGE")

    def test_negative_storage_is_retained_as_infeasible(self):
        s = example_scenario()
        s["policies"][1]["schedule"]["values"] = [0, 0, -12000, 0]
        r = evaluate(s, generate(s, "candidate"), "candidate")
        self.assertEqual(r["state"], "COMPLETED_INFEASIBLE")
        self.assertAlmostEqual(r["metrics"]["final_storage_energy"]["value"], -12000000, delta=1e-6)
        self.assertEqual(r["metrics"]["final_storage_energy"]["sign"], "stored_energy_positive")

    def test_malformed_comparison_evidence_is_ineligible(self):
        results = [evaluate(self.scenario, generate(self.scenario, p), p) for p in ("baseline", "candidate")]
        for field, value in (("value", 10 ** 400), ("value", float("nan")), ("value", True),
                             ("unit", "kWh"), ("basis", "reactive_energy"), ("sign", "unknown"),
                             ("location", []), ("support", None), ("support", {"start_s": 0, "end_s": True, "aggregation": "integral"})):
            with self.subTest(field=field, value=repr(value)[:30]):
                wrong = copy.deepcopy(results)
                for result in wrong:
                    result["metrics"]["import_energy"][field] = value
                self.assertEqual(compare(wrong)["state"], "INELIGIBLE")
        for value in (None, [], {}, "results", [None, None], [{"policy_id": []}, {}]):
            self.assertEqual(compare(value)["state"], "INELIGIBLE")

    def test_structurally_invalid_raw_retains_artifact_digest(self):
        raw = copy.deepcopy(self.raw)
        raw["intervals"].pop()
        r = self.invalid(raw, "RAW_CONTRACT")
        self.assertEqual(r["raw_sha256"], digest(raw))
        for malformed in (None, {}, [], {"unexpected": "field"}):
            self.assertEqual(self.invalid(malformed)["raw_sha256"], digest(malformed))

    def test_noncanonical_raw_has_no_artifact_digest_and_stays_invalid(self):
        nested = []
        for _ in range(34):
            nested = [nested]
        for malformed in (float("nan"), {"bad": object()}, nested):
            self.assertIsNone(self.invalid(malformed, "RAW_CONTRACT")["raw_sha256"])
        raw = copy.deepcopy(self.raw)
        raw["intervals"][0]["storage"]["charge"]["value"] = float("inf")
        self.assertIsNone(self.invalid(raw, "RAW_CONTRACT")["raw_sha256"])

    def test_input_objects_remain_unchanged(self):
        before_s, before_r = copy.deepcopy(self.scenario), copy.deepcopy(self.raw)
        evaluate(self.scenario, self.raw, "candidate")
        self.assertEqual(self.scenario, before_s)
        self.assertEqual(self.raw, before_r)


if __name__ == "__main__":
    unittest.main()

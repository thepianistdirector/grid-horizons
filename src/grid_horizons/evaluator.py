"""Independent raw-result checks using nodal incidence, never producer traversal.

Copyright (C) 2026 Lucas Santana. SPDX-License-Identifier: AGPL-3.0-only
"""
from __future__ import annotations

import hashlib
import math
from typing import Any

from . import MODEL_ID, RAW_SCHEMA, RESULT_SCHEMA
from .contracts import (ContractError, MAX_RAW_BYTES, canonical_bytes, digest,
                        exact, finite, object_fields, validate_scenario)
from .raw_contract import (BRANCH_FIELDS, GRID_FIELDS, NODE_FIELDS, NOT_EVALUATED,
                           STORAGE_FIELDS)

EVALUATOR_VERSION = "independent-incidence/v1"
VOLTAGE_TOLERANCE = 1e-10
ENERGY_METRICS = (
    "import_energy", "export_energy", "net_import_energy", "served_load_energy",
    "unserved_load_energy", "available_generation_energy", "injected_generation_energy",
    "curtailed_potential_energy", "storage_charge_energy", "storage_discharge_energy",
    "storage_conversion_loss", "initial_storage_energy", "final_storage_energy",
)
METRIC_UNITS = {**dict.fromkeys(ENERGY_METRICS, "J"), "peak_import_power": "W",
                "min_voltage": "pu", "max_voltage": "pu", "max_loading": "1"}


def _raw_digest(raw: Any) -> str | None:
    """Retain artifact identity even when its ordinary JSON structure is invalid.

    This narrow admission guard excludes custom objects, nonfinite values,
    excessive nesting and oversized data before calling the JSON serializer.
    Serializer input errors are not unexpected evaluator failures.
    """
    pending = [(raw, 0)]
    minimum_bytes = 0
    while pending:
        value, depth = pending.pop()
        if depth > 32:
            return None
        kind = type(value)
        if kind is dict:
            if any(type(key) is not str for key in value):
                return None
            minimum_bytes += sum(len(key) + 3 for key in value) + 2
            pending.extend((item, depth + 1) for item in value.values())
        elif kind is list:
            minimum_bytes += len(value) + 2
            pending.extend((item, depth + 1) for item in value)
        elif kind is str:
            minimum_bytes += len(value) + 2
        elif kind is float:
            if not math.isfinite(value):
                return None
            minimum_bytes += 1
        elif kind in (int, bool) or value is None:
            minimum_bytes += 1
        else:
            return None
        if minimum_bytes > MAX_RAW_BYTES:
            return None
    try:
        encoded = canonical_bytes(raw)
    except (TypeError, ValueError, RecursionError, OverflowError):
        return None
    if len(encoded) > MAX_RAW_BYTES:
        return None
    return hashlib.sha256(encoded).hexdigest()


def _tolerance(*terms: float) -> float:
    return 1e-6 + 1e-11 * math.fsum(abs(term) for term in terms)


def _quantity(value: float, unit: str, basis: str, sign: str, location: str,
              scenario: dict, aggregation: str = "integral") -> dict:
    return {"value": value, "unit": unit, "basis": basis, "sign": sign,
            "location": location, "support": {"start_s": scenario["intervals"][0]["start_s"],
            "end_s": scenario["intervals"][-1]["end_s"], "aggregation": aggregation}}


def _read_fields(record: Any, declarations: dict, location: str, interval: dict,
                 path: str, identity_field: str | None = None) -> dict:
    fields = set(declarations) | ({identity_field} if identity_field else set())
    object_fields(record, fields, path)
    values = {}
    for field, (unit, basis, sign, aggregation) in declarations.items():
        p = f"{path}.{field}"
        q = object_fields(record[field], {"value", "unit", "basis", "sign", "location", "support"}, p)
        for key, expected in (("unit", unit), ("basis", basis), ("sign", sign), ("location", location)):
            exact(q[key], expected, f"{p}.{key}")
        support = {"interval_id": interval["id"], "start_s": interval["start_s"],
                   "end_s": interval["end_s"], "aggregation": aggregation}
        exact(q["support"], support, f"{p}.support")
        values[field] = finite(q["value"], f"{p}.value")
    return values


def _coverage(records: Any, identities: list[str], declarations: dict, key: str,
              interval: dict, path: str) -> dict:
    if not isinstance(records, list) or len(records) != len(identities):
        raise ContractError(path, "must contain exactly one record per declared component")
    result = {}
    for index, record in enumerate(records):
        p = f"{path}[{index}]"
        object_fields(record, set(declarations) | {key}, p)
        identity = record[key]
        if not isinstance(identity, str) or identity not in identities or identity in result:
            raise ContractError(p, "unknown or duplicate component identifier")
        result[identity] = _read_fields(record, declarations, identity, interval, p, key)
    return result


def _read_raw(scenario: dict, raw: Any, policy_id: str) -> list[dict]:
    object_fields(raw, {"schema_version", "scenario_sha256", "policy_id", "model_id", "intervals"}, "$")
    for key, expected in (("schema_version", RAW_SCHEMA), ("scenario_sha256", digest(scenario)),
                          ("policy_id", policy_id), ("model_id", MODEL_ID)):
        exact(raw[key], expected, f"$.{key}")
    if not isinstance(raw["intervals"], list) or len(raw["intervals"]) != len(scenario["intervals"]):
        raise ContractError("$.intervals", "must contain all declared intervals in order")
    network = scenario["network"]
    parsed = []
    for index, (record, interval) in enumerate(zip(raw["intervals"], scenario["intervals"])):
        path = f"$.intervals[{index}]"
        object_fields(record, {"id", "start_s", "end_s", "nodes", "branches", "storage", "grid"}, path)
        for key in ("id", "start_s", "end_s"):
            exact(record[key], interval[key], f"{path}.{key}")
        parsed.append({
            "nodes": _coverage(record["nodes"], network["nodes"], NODE_FIELDS, "node_id", interval, f"{path}.nodes"),
            "branches": _coverage(record["branches"], [b["id"] for b in network["branches"]], BRANCH_FIELDS,
                                  "branch_id", interval, f"{path}.branches"),
            "storage": _read_fields(record["storage"], STORAGE_FIELDS, scenario["storage"]["node_id"],
                                    interval, f"{path}.storage"),
            "grid": _read_fields(record["grid"], GRID_FIELDS, network["root"], interval, f"{path}.grid"),
        })
    if len(canonical_bytes(raw)) > MAX_RAW_BYTES:
        raise ContractError("$", "raw output exceeds byte limit")
    return parsed


def evaluate(scenario: Any, raw: Any, policy_id: str) -> dict:
    """Reject malformed evidence; distinguish valid equations from feasible limits.

    Only ContractError from raw structural admission is converted to INVALID_RESULT.
    Scenario errors and unexpected checker exceptions intentionally propagate.
    """
    validate_scenario(scenario)
    if policy_id not in ("baseline", "candidate"):
        raise ContractError("$.policy_id", "must select baseline or candidate")
    result = {"schema_version": RESULT_SCHEMA, "scenario_sha256": digest(scenario),
              "raw_sha256": _raw_digest(raw), "policy_id": policy_id, "model_id": MODEL_ID,
              "evaluator_version": EVALUATOR_VERSION, "state": "INVALID_RESULT",
              "comparison_eligible": False, "findings": [], "metrics": {}, "ledger": {},
              "not_evaluated": list(NOT_EVALUATED), "uncertainty": dict(scenario["uncertainty"]),
              "scope": "Original synthetic lossless linearized tutorial; no engineering applicability established."}
    try:
        if result["raw_sha256"] is None:
            raise ContractError("$", "raw output must be bounded canonical JSON without custom objects or nonfinite values")
        records = _read_raw(scenario, raw, policy_id)
    except ContractError as exc:
        result["findings"].append({"code": "RAW_CONTRACT", "message": exc.message, "location": exc.path})
        return result
    invalid, violations = [], []
    network, storage = scenario["network"], scenario["storage"]
    root, storage_node = network["root"], storage["node_id"]
    profiles = {p["node_id"]: p for p in scenario["profiles"]}
    schedule = next(p["schedule"]["values"] for p in scenario["policies"] if p["id"] == policy_id)
    initial = storage["initial_energy"]["value"]
    eta_c, eta_d = storage["charge_efficiency"]["value"], storage["discharge_efficiency"]["value"]
    previous_energy = initial
    energy = {key: [] for key in ENERGY_METRICS}
    all_voltages, all_loadings, imports, real_residuals, reactive_residuals, energy_residuals = [], [], [], [], [], []

    def finding(target: list, code: str, message: str, location: str, interval: str) -> None:
        target.append({"code": code, "message": message, "location": location, "interval": interval})

    def identity(code: str, terms: list[float], location: str, interval: str,
                 tolerance: float | None = None) -> float:
        residual = math.fsum(terms)
        if abs(residual) > (_tolerance(*terms) if tolerance is None else tolerance):
            finding(invalid, code, f"Identity residual {residual:.12g} exceeds numerical allowance", location, interval)
        return abs(residual)

    def bound(value: float, limit: float, lower: bool, code: str, location: str, interval: str,
              tolerance: float | None = None) -> None:
        allowance = _tolerance(value, limit) if tolerance is None else tolerance
        if (value < limit - allowance) if lower else (value > limit + allowance):
            finding(violations, code, f"Value {value:.12g} violates {'minimum' if lower else 'maximum'} {limit:.12g}",
                    location, interval)

    for index, (record, interval) in enumerate(zip(records, scenario["intervals"])):
        iid, dt = interval["id"], interval["end_s"] - interval["start_s"]
        nodes, branches, st, grid = (record[k] for k in ("nodes", "branches", "storage", "grid"))
        charge, discharge = st["charge"], st["discharge"]
        identity("POLICY_DISPATCH", [charge, -max(schedule[index], 0)], storage_node, iid)
        identity("POLICY_DISPATCH", [discharge, -max(-schedule[index], 0)], storage_node, iid)
        identity("STORAGE_CONTINUITY", [st["energy_start"], -previous_energy], storage_node, iid)
        identity("STORAGE_TRANSITION", [st["energy_end"], -st["energy_start"], -eta_c * charge * dt,
                                        discharge * dt / eta_d], storage_node, iid)
        identity("STORAGE_CONVERSION", [st["conversion_loss"], -(1 - eta_c) * charge * dt,
                                        -(1 / eta_d - 1) * discharge * dt], storage_node, iid)
        previous_energy = st["energy_end"]
        # Signed incidence: each edge contributes once to each endpoint.
        incoming_p = {node: [] for node in nodes}
        incoming_q = {node: [] for node in nodes}
        for branch in network["branches"]:
            b = branches[branch["id"]]
            incoming_p[branch["parent"]].append(-b["real_power"])
            incoming_p[branch["child"]].append(b["real_power"])
            incoming_q[branch["parent"]].append(-b["reactive_power"])
            incoming_q[branch["child"]].append(b["reactive_power"])
            drop = 2 * (branch["resistance"]["value"] * b["real_power"] +
                        branch["reactance"]["value"] * b["reactive_power"]) / scenario["base"]["apparent_power"]["value"]
            identity("VOLTAGE_DROP", [nodes[branch["child"]]["voltage_squared"],
                                      -nodes[branch["parent"]]["voltage_squared"], drop], branch["id"], iid,
                     VOLTAGE_TOLERANCE)
            apparent = math.hypot(b["real_power"], b["reactive_power"])
            loading = apparent / branch["rating"]["value"]
            identity("LOADING_IDENTITY", [b["loading"], -loading], branch["id"], iid, 1e-10)
            all_loadings.append(loading)
            bound(apparent, branch["rating"]["value"], False, "BRANCH_RATING", branch["id"], iid)
        incoming_p[root].extend([grid["import_power"], -grid["export_power"]])
        incoming_q[root].append(grid["reactive_power"])
        for node_id, node in nodes.items():
            for field in ("load", "reactive_load", "generation_available", "curtailment"):
                expected = 0 if node_id == root else profiles[node_id][field]["values"][index]
                identity("PROFILE_BINDING", [node[field], -expected], f"{node_id}.{field}", iid)
            identity("GENERATION_IDENTITY", [node["generation_injected"], node["curtailment"],
                                              -node["generation_available"]], node_id, iid)
            identity("DEMAND_IDENTITY", [node["served_load"], node["unserved_load"], -node["load"]], node_id, iid)
            identity("NO_SHEDDING", [node["served_load"], -node["load"]], node_id, iid)
            identity("NO_SHEDDING", [node["unserved_load"]], node_id, iid)
            p_terms = incoming_p[node_id] + [-node["served_load"], node["generation_injected"]]
            if node_id == storage_node:
                p_terms.extend([-charge, discharge])
            real_residuals.append(identity("REAL_NODE_BALANCE", p_terms, node_id, iid))
            reactive_residuals.append(identity("REACTIVE_NODE_BALANCE", incoming_q[node_id] + [-node["reactive_load"]], node_id, iid))
            if node["voltage_squared"] <= 0:
                finding(invalid, "NONPOSITIVE_VOLTAGE", "Squared voltage must be positive for a model solution", node_id, iid)
        identity("ROOT_VOLTAGE", [nodes[root]["voltage_squared"], -network["root_voltage"]["value"] ** 2],
                 root, iid, VOLTAGE_TOLERANCE)
        net_root = -math.fsum(incoming_p[root][:-2])
        identity("GRID_EXCHANGE", [grid["import_power"], -max(net_root, 0)], root, iid)
        identity("GRID_EXCHANGE", [grid["export_power"], -max(-net_root, 0)], root, iid)
        # Reconstruct voltage from the admitted root and raw edge drops, independent
        # of reported voltage magnitudes and of the producer's subtree powers.
        squared = {root: network["root_voltage"]["value"] ** 2}
        pending = list(network["branches"])
        while pending:
            for branch in pending[:]:
                if branch["parent"] not in squared:
                    continue
                b = branches[branch["id"]]
                squared[branch["child"]] = squared[branch["parent"]] - 2 * (
                    branch["resistance"]["value"] * b["real_power"] + branch["reactance"]["value"] * b["reactive_power"]
                ) / scenario["base"]["apparent_power"]["value"]
                pending.remove(branch)
        for node_id, u in squared.items():
            if u <= 0:
                finding(invalid, "NONPOSITIVE_VOLTAGE", "Recomputed squared voltage must be positive", node_id, iid)
            else:
                all_voltages.append(math.sqrt(u))
            for low, limit, code in ((True, .9, "MODEL_DOMAIN_VOLTAGE"), (False, 1.1, "MODEL_DOMAIN_VOLTAGE"),
                                     (True, scenario["limits"]["voltage_min"]["value"], "VOLTAGE_LIMIT"),
                                     (False, scenario["limits"]["voltage_max"]["value"], "VOLTAGE_LIMIT")):
                bound(u, limit ** 2, low, code, node_id, iid, VOLTAGE_TOLERANCE)
        for field in ("charge", "discharge"):
            bound(st[field], 0, True, "STORAGE_POWER", storage_node, iid)
            bound(st[field], storage[f"{field}_limit"]["value"], False, "STORAGE_POWER", storage_node, iid)
        for field in ("energy_start", "energy_end"):
            bound(st[field], 0, True, "STORAGE_ENERGY", storage_node, iid)
            bound(st[field], storage["capacity"]["value"], False, "STORAGE_ENERGY", storage_node, iid)
        node_energy = {field: math.fsum(n[field] * dt for n in nodes.values()) for field in
                       ("served_load", "unserved_load", "generation_available", "generation_injected", "curtailment")}
        values = {"import_energy": grid["import_power"] * dt, "export_energy": grid["export_power"] * dt,
                  "net_import_energy": (grid["import_power"] - grid["export_power"]) * dt,
                  "served_load_energy": node_energy["served_load"], "unserved_load_energy": node_energy["unserved_load"],
                  "available_generation_energy": node_energy["generation_available"],
                  "injected_generation_energy": node_energy["generation_injected"],
                  "curtailed_potential_energy": node_energy["curtailment"], "storage_charge_energy": charge * dt,
                  "storage_discharge_energy": discharge * dt, "storage_conversion_loss": st["conversion_loss"]}
        for key, value in values.items():
            energy[key].append(value)
        energy_residuals.append(identity("REAL_ENERGY_BALANCE", [st["energy_start"], values["import_energy"],
            values["injected_generation_energy"], -st["energy_end"], -values["export_energy"],
            -values["served_load_energy"], -st["conversion_loss"]], "network", iid))
        imports.append(grid["import_power"])
    if abs(previous_energy - initial) > _tolerance(previous_energy, initial):
        finding(violations, "FINAL_STORAGE_EQUALITY", "Final storage energy differs from declared initial energy",
                storage_node, scenario["intervals"][-1]["id"])
    identity("STUDY_REAL_ENERGY_BALANCE", [initial, math.fsum(energy["import_energy"]),
             math.fsum(energy["injected_generation_energy"]), -previous_energy,
             -math.fsum(energy["export_energy"]), -math.fsum(energy["served_load_energy"]),
             -math.fsum(energy["storage_conversion_loss"])], "network", "full_study")
    if invalid:
        result["findings"] = invalid + violations
        return result
    # Objectives are materialized only after structural, consistency and limit checks.
    energy["initial_storage_energy"], energy["final_storage_energy"] = [initial], [previous_energy]
    for key, terms in energy.items():
        location = storage_node if "storage" in key else (root if "import" in key or "export" in key else "network")
        sign = ("stored_energy_positive" if key in ("initial_storage_energy", "final_storage_energy")
                else "import_positive" if key == "net_import_energy" else "nonnegative")
        basis = "stored_energy" if key in ("initial_storage_energy", "final_storage_energy") else "real_energy"
        aggregation = "state_start" if key == "initial_storage_energy" else ("state_end" if key == "final_storage_energy" else "integral")
        result["metrics"][key] = _quantity(math.fsum(terms), "J", basis, sign, location, scenario, aggregation)
    for key, value, unit, basis, location, agg in (
            ("peak_import_power", max(imports), "W", "three_phase_total", root, "maximum"),
            ("min_voltage", min(all_voltages), "pu", "voltage_base", "all_nodes", "minimum"),
            ("max_voltage", max(all_voltages), "pu", "voltage_base", "all_nodes", "maximum"),
            ("max_loading", max(all_loadings), "1", "apparent_power_over_rating", "all_branches", "maximum")):
        result["metrics"][key] = _quantity(value, unit, basis, "nonnegative", location, scenario, agg)
    m = {key: value["value"] for key, value in result["metrics"].items()}
    residual = math.fsum([initial, m["import_energy"], m["injected_generation_energy"], -previous_energy,
                          -m["export_energy"], -m["served_load_energy"], -m["storage_conversion_loss"]])
    result["ledger"] = {
        "real_energy_residual": _quantity(residual, "J", "real_energy_balance", "signed_residual", "network", scenario),
        "max_interval_real_energy_residual": _quantity(max(energy_residuals), "J", "real_energy_balance", "nonnegative", "network", scenario, "maximum"),
        "max_real_node_residual": _quantity(max(real_residuals), "W", "three_phase_total", "nonnegative", "all_nodes", scenario, "maximum"),
        "max_reactive_node_residual": _quantity(max(reactive_residuals), "var", "three_phase_total", "nonnegative", "all_nodes", scenario, "maximum"),
    }
    result["findings"] = violations
    result["state"] = "COMPLETED_INFEASIBLE" if violations else "COMPLETED_VALID"
    result["comparison_eligible"] = not violations
    return result


def compare(results: Any) -> dict:
    """Display supported differences, never infer an overall policy winner."""
    def ineligible(reason: str) -> dict:
        return {"state": "INELIGIBLE", "reason": reason, "differences": {}}
    if not isinstance(results, list) or len(results) != 2 or not all(isinstance(r, dict) for r in results):
        return ineligible("Exactly one current result for each policy is required.")
    if {r.get("policy_id") for r in results if isinstance(r.get("policy_id"), str)} != {"baseline", "candidate"}:
        return ineligible("Exactly one baseline and one candidate are required.")
    baseline = next(r for r in results if r["policy_id"] == "baseline")
    candidate = next(r for r in results if r["policy_id"] == "candidate")
    for field in ("scenario_sha256", "model_id", "evaluator_version", "schema_version"):
        if not isinstance(baseline.get(field), str) or not baseline[field] or baseline[field] != candidate.get(field):
            return ineligible(f"Mismatched or missing {field} identity.")
    if baseline["model_id"] != MODEL_ID or baseline["schema_version"] != RESULT_SCHEMA or baseline["evaluator_version"] != EVALUATOR_VERSION:
        return ineligible("Unsupported result model, schema or evaluator.")
    if any(r.get("state") != "COMPLETED_VALID" or r.get("comparison_eligible") is not True for r in results):
        return ineligible("Both policies must have valid feasible completed results.")
    for r in results:
        for field in ("scenario_sha256", "raw_sha256"):
            value = r.get(field)
            if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                return ineligible("Completed evidence requires canonical scenario and raw digests.")
        if not isinstance(r.get("metrics"), dict) or set(r["metrics"]) != set(METRIC_UNITS):
            return ineligible("Exactly the supported metric quantities are required.")
    differences = {}
    for key, unit in METRIC_UNITS.items():
        a, b = baseline.get("metrics", {}), candidate.get("metrics", {})
        if not isinstance(a, dict) or not isinstance(b, dict) or not isinstance(a.get(key), dict) or not isinstance(b.get(key), dict):
            return ineligible("Metric quantities are missing or malformed.")
        qa, qb = a[key], b[key]
        metadata = {"unit", "basis", "sign", "location", "support"}
        if set(qa) != metadata | {"value"} or set(qb) != metadata | {"value"} or qa["unit"] != unit:
            return ineligible("Metric quantities have unsupported metadata.")
        if any(qa[field] != qb[field] for field in metadata):
            return ineligible("Metric quantity metadata differs between policies.")
        expected_basis = ("stored_energy" if key in ("initial_storage_energy", "final_storage_energy")
                          else "real_energy" if unit == "J" else "three_phase_total" if unit == "W"
                          else "voltage_base" if unit == "pu" else "apparent_power_over_rating")
        expected_sign = ("stored_energy_positive" if key in ("initial_storage_energy", "final_storage_energy")
                         else "import_positive" if key == "net_import_energy" else "nonnegative")
        expected_aggregation = ("state_start" if key == "initial_storage_energy" else "state_end" if key == "final_storage_energy"
                                else "integral" if unit == "J" else "minimum" if key == "min_voltage" else "maximum")
        if qa["basis"] != expected_basis or qa["sign"] != expected_sign or not isinstance(qa["location"], str) or not qa["location"]:
            return ineligible("Metric dimension, sign or location is unsupported.")
        for q in (qa, qb):
            support = q["support"]
            if (not isinstance(support, dict) or set(support) != {"start_s", "end_s", "aggregation"}
                    or type(support["start_s"]) is not int or type(support["end_s"]) is not int
                    or support["start_s"] != 0 or not 0 < support["end_s"] <= 86400
                    or support["aggregation"] != expected_aggregation):
                return ineligible("Metric study support is malformed.")
            if support["end_s"] != baseline["metrics"]["import_energy"]["support"]["end_s"]:
                return ineligible("Metrics must share the same full study interval.")
        if any(type(q["value"]) not in (int, float) or not -1e15 <= q["value"] <= 1e15
               or not math.isfinite(q["value"]) for q in (qa, qb)):
            return ineligible("Metric values must be finite bounded numbers.")
        differences[key] = {**qb, "value": qb["value"] - qa["value"], "sign": "candidate_minus_baseline"}
    return {"state": "INDETERMINATE", "reason": "Model uncertainty and unmodeled costs prevent an overall winner.",
            "differences": differences}

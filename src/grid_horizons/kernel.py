"""Trusted lossless radial kernel and bounded constant-efficiency storage.

The evaluator uses a separate incidence/residual calculation. This producer
emits interval quantities only; it has no authority to declare feasibility.
Copyright (C) 2026 Lucas Santana. SPDX-License-Identifier: AGPL-3.0-only
"""

from __future__ import annotations

import math
from collections.abc import Iterator

from . import MODEL_ID, RAW_SCHEMA
from .contracts import ContractError, digest, interval_support, network_order, quantity, validate_scenario
from .raw_contract import NODE_FIELDS, BRANCH_FIELDS, STORAGE_FIELDS, GRID_FIELDS

KERNEL_VERSION = "tree-accumulation/v1"


class SolverFailure(RuntimeError):
    """The declared approximation did not produce a usable numerical interval."""


def _quantities(values: dict, fields: dict, location: str, interval: dict) -> dict:
    return {name: quantity(values[name], unit, location, basis, sign,
                           interval_support(interval, aggregation))
            for name, (unit, basis, sign, aggregation) in fields.items()}


def envelope(scenario: dict, policy_id: str, intervals: list[dict]) -> dict:
    return {"schema_version": RAW_SCHEMA, "scenario_sha256": digest(scenario),
            "model_id": MODEL_ID, "policy_id": policy_id, "intervals": intervals}


def generate_intervals(scenario: dict, policy_id: str) -> Iterator[dict]:
    """Yield actual raw intervals, with no clipping, search or feasibility flag."""
    s = validate_scenario(scenario)
    if policy_id not in ("baseline", "candidate"):
        raise ContractError("policy_id", "must be baseline or candidate")
    policy = next(p for p in s["policies"] if p["id"] == policy_id)
    network = s["network"]
    root = network["root"]
    order = network_order(network)
    profiles = {p["node_id"]: p for p in s["profiles"]}
    incoming = {branch["child"]: branch for branch in network["branches"]}
    storage = s["storage"]
    storage_node = storage["node_id"]
    eta_c = float(storage["charge_efficiency"]["value"])
    eta_d = float(storage["discharge_efficiency"]["value"])
    energy = float(storage["initial_energy"]["value"])
    s_base = float(s["base"]["apparent_power"]["value"])

    for index, interval in enumerate(s["intervals"]):
        duration = interval["end_s"] - interval["start_s"]
        dispatch = float(policy["schedule"]["values"][index])
        charge = max(dispatch, 0.0)
        discharge = max(-dispatch, 0.0)
        end_energy = energy + (eta_c * charge - discharge / eta_d) * duration
        conversion_loss = ((1 - eta_c) * charge + (1 / eta_d - 1) * discharge) * duration
        nodal = {}
        accumulated_p = {}
        accumulated_q = {}
        for node in network["nodes"]:
            profile = profiles.get(node)
            values = {field: float(profile[field]["values"][index]) if profile else 0.0
                      for field in ("load", "reactive_load", "generation_available", "curtailment")}
            values["served_load"] = values["load"]
            values["unserved_load"] = 0.0
            values["generation_injected"] = values["generation_available"] - values["curtailment"]
            nodal[node] = values
            accumulated_p[node] = values["served_load"] - values["generation_injected"]
            if node == storage_node:
                accumulated_p[node] += charge - discharge
            accumulated_q[node] = values["reactive_load"]

        flows = {}
        for child in reversed(order[1:]):
            branch = incoming[child]
            p, q = accumulated_p[child], accumulated_q[child]
            flows[branch["id"]] = {"real_power": p, "reactive_power": q,
                                    "loading": math.hypot(p, q) / branch["rating"]["value"]}
            accumulated_p[branch["parent"]] += p
            accumulated_q[branch["parent"]] += q

        voltages = {root: float(network["root_voltage"]["value"]) ** 2}
        for child in order[1:]:
            branch = incoming[child]
            flow = flows[branch["id"]]
            voltages[child] = voltages[branch["parent"]] - 2 * (
                branch["resistance"]["value"] * flow["real_power"] / s_base
                + branch["reactance"]["value"] * flow["reactive_power"] / s_base)
            if not math.isfinite(voltages[child]) or voltages[child] <= 0:
                raise SolverFailure(
                    f"{interval['id']} at {child}: no positive squared voltage in the declared approximation")
        for node in network["nodes"]:
            nodal[node]["voltage_squared"] = voltages[node]

        raw = dict(interval)
        raw["nodes"] = [{"node_id": node, **_quantities(nodal[node], NODE_FIELDS, node, interval)}
                        for node in network["nodes"]]
        raw["branches"] = [{"branch_id": branch["id"],
                            **_quantities(flows[branch["id"]], BRANCH_FIELDS, branch["id"], interval)}
                           for branch in network["branches"]]
        raw["storage"] = _quantities({"charge": charge, "discharge": discharge,
                                      "energy_start": energy, "energy_end": end_energy,
                                      "conversion_loss": conversion_loss},
                                     STORAGE_FIELDS, storage_node, interval)
        raw["grid"] = _quantities({"import_power": max(accumulated_p[root], 0.0),
                                   "export_power": max(-accumulated_p[root], 0.0),
                                   "reactive_power": accumulated_q[root]},
                                  GRID_FIELDS, root, interval)
        yield raw
        energy = end_energy


def generate(scenario: dict, policy_id: str) -> dict:
    return envelope(scenario, policy_id, list(generate_intervals(scenario, policy_id)))


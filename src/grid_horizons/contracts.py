"""Closed declarative contracts. No engine, plugin or implicit unit conversion.

Copyright (C) 2026 Lucas Santana. SPDX-License-Identifier: AGPL-3.0-only
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

from . import MODEL_ID, SCENARIO_SCHEMA

MAX_INPUT_BYTES = 1024 * 1024
MAX_RAW_BYTES = 16 * 1024 * 1024
MAX_NODES = 16
MAX_INTERVALS = 96
IDENTIFIER = re.compile(r"[a-z][a-z0-9-]{0,47}\Z")


class ContractError(ValueError):
    """An inspectable input/result error, without a developer traceback."""

    def __init__(self, path: str, message: str):
        self.path = path
        self.message = message
        super().__init__(f"{path}: {message}")

    def as_dict(self) -> dict:
        return {"path": self.path, "message": self.message}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False,
                      ensure_ascii=True).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError("$", f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ContractError("$", f"nonfinite JSON number {value} is not supported")


def decode_json(data: bytes, limit: int = MAX_INPUT_BYTES) -> Any:
    if len(data) > limit:
        raise ContractError("$", f"JSON exceeds the {limit}-byte limit")
    try:
        result = json.loads(data.decode("utf-8"), object_pairs_hook=_unique_pairs,
                            parse_constant=_reject_constant)
        pending = [(result, 0)]
        while pending:
            value, depth = pending.pop()
            if depth > 32:
                raise ContractError("$", "JSON nesting exceeds 32 levels")
            if isinstance(value, dict):
                pending.extend((item, depth + 1) for item in value.values())
            elif isinstance(value, list):
                pending.extend((item, depth + 1) for item in value)
        return result
    except ContractError:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        # JSONDecodeError contains source positions but not source file paths.
        detail = str(exc) if isinstance(exc, json.JSONDecodeError) else "invalid UTF-8, number or nesting"
        raise ContractError("$", f"cannot decode JSON: {detail}") from exc


def load_json(path: Path, limit: int = MAX_INPUT_BYTES) -> Any:
    try:
        with path.open("rb") as stream:
            return decode_json(stream.read(limit + 1), limit)
    except OSError as exc:
        raise ContractError("$", f"cannot read JSON: {exc.strerror}") from exc


def object_fields(value: Any, fields: set[str], path: str,
                  optional: set[str] | None = None) -> dict:
    if not isinstance(value, dict):
        raise ContractError(path, "must be an object")
    missing = fields - value.keys()
    unknown = value.keys() - fields - (optional or set())
    if missing:
        raise ContractError(path, "missing fields: " + ", ".join(sorted(missing)))
    if unknown:
        raise ContractError(path, "unknown fields: " + ", ".join(sorted(unknown)))
    return value


def exact(value: Any, expected: Any, path: str) -> None:
    if type(value) is not type(expected) or value != expected or canonical_bytes(value) != canonical_bytes(expected):
        raise ContractError(path, f"must equal {expected!r}")


def finite(value: Any, path: str, lower: float = -1e15,
           upper: float = 1e15) -> float:
    if type(value) not in (int, float):
        raise ContractError(path, "must be a finite number; booleans are not quantities")
    if not lower <= value <= upper or not math.isfinite(value):
        raise ContractError(path, f"must be finite and in [{lower:g}, {upper:g}]")
    return float(value)


def identifier(value: Any, path: str) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ContractError(path, "use 1–48 lowercase letters, digits or hyphens, beginning with a letter")
    return value


def sequence(value: Any, path: str, minimum: int, maximum: int) -> list:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise ContractError(path, f"must be an array with {minimum}–{maximum} entries")
    return value


def quantity(value: float | list[float], unit: str, location: str, basis: str,
             sign: str = "nonnegative", support: Any = "constant") -> dict:
    return {"values" if isinstance(value, list) else "value": value,
            "unit": unit, "basis": basis, "sign": sign,
            "location": location, "support": support}


def read_quantity(value: Any, *, unit: str, location: str, basis: str,
                  sign: str = "nonnegative", support: Any = "constant",
                  path: str, lower: float = -1e15, upper: float = 1e15,
                  count: int | None = None) -> float | list[float]:
    numeric_field = "value" if count is None else "values"
    object_fields(value, {numeric_field, "unit", "basis", "sign", "location", "support"}, path)
    for name, expected in (("unit", unit), ("location", location), ("basis", basis),
                           ("sign", sign), ("support", support)):
        exact(value[name], expected, f"{path}.{name}")
    if count is None:
        return finite(value["value"], f"{path}.value", lower, upper)
    values = sequence(value["values"], f"{path}.values", count, count)
    return [finite(number, f"{path}.values[{i}]", lower, upper)
            for i, number in enumerate(values)]


def interval_support(interval: dict, aggregation: str = "mean") -> dict:
    return {"interval_id": interval["id"], "start_s": interval["start_s"],
            "end_s": interval["end_s"], "aggregation": aggregation}


def network_order(network: dict) -> list[str]:
    """Return a rooted order after validating topology; no numerical equations."""
    order = [network["root"]]
    for node in order:
        order.extend(branch["child"] for branch in network["branches"]
                     if branch["parent"] == node)
    return order


def validate_scenario(scenario: Any) -> dict:
    """Validate identity, dimensions, topology and input domain, not feasibility.

    Dispatch/power/energy limit violations arising from a valid candidate are
    retained for evaluation. The scenario is not modified or repaired.
    """
    s = object_fields(scenario, {
        "schema_version", "scenario_id", "title", "provenance", "model_id", "timeline",
        "intervals", "base", "network", "profiles", "storage", "policies", "limits",
        "uncertainty"}, "$", {"annotations"})
    exact(s["schema_version"], SCENARIO_SCHEMA, "$.schema_version")
    exact(s["model_id"], MODEL_ID, "$.model_id")
    identifier(s["scenario_id"], "$.scenario_id")
    if not isinstance(s["title"], str) or not 1 <= len(s["title"]) <= 120 or any(
            ord(c) < 32 or ord(c) == 127 for c in s["title"]):
        raise ContractError("$.title", "must contain 1–120 printable characters")
    exact(s["provenance"], {"kind": "ORIGINAL_SYNTHETIC", "license": "AGPL-3.0-only",
                           "record_id": "GH-SYNTHETIC-001"}, "$.provenance")
    exact(s["timeline"], {"unit": "s", "origin": "fictional_study_start", "support": "half_open"},
          "$.timeline")
    exact(s["uncertainty"], {"inputs": "SYNTHETIC_FIXED", "model_error": "NOT_QUANTIFIED",
                            "preference": "NONE"}, "$.uncertainty")
    if "annotations" in s:
        annotations = s["annotations"]
        if not isinstance(annotations, dict) or len(annotations) > 16 or any(
                not isinstance(k, str) or not isinstance(v, str) or not 1 <= len(k) <= 64
                or len(v) > 500 for k, v in annotations.items()):
            raise ContractError("$.annotations", "must be at most 16 short text pairs")

    intervals = sequence(s["intervals"], "$.intervals", 1, MAX_INTERVALS)
    interval_ids: set[str] = set()
    previous_end = 0
    for i, interval in enumerate(intervals):
        path = f"$.intervals[{i}]"
        object_fields(interval, {"id", "start_s", "end_s"}, path)
        identity = identifier(interval["id"], f"{path}.id")
        if identity in interval_ids:
            raise ContractError(path, "duplicate interval ID")
        interval_ids.add(identity)
        if type(interval["start_s"]) is not int or type(interval["end_s"]) is not int:
            raise ContractError(path, "interval endpoints must be integer seconds")
        if interval["start_s"] != previous_end or not previous_end < interval["end_s"] <= 86400:
            raise ContractError(path, "intervals must be positive, contiguous, start at 0 and end by 86400 s")
        previous_end = interval["end_s"]
    count = len(intervals)

    base = object_fields(s["base"], {"apparent_power", "voltage_line_to_line"}, "$.base")
    read_quantity(base["apparent_power"], unit="VA", location="network", basis="three_phase_total",
                  sign="positive", path="$.base.apparent_power", lower=1000, upper=1e9)
    read_quantity(base["voltage_line_to_line"], unit="V", location="network", basis="line_to_line_rms",
                  sign="positive", path="$.base.voltage_line_to_line", lower=100, upper=1e5)
    network = object_fields(s["network"], {"nodes", "root", "root_voltage", "branches"}, "$.network")
    nodes = sequence(network["nodes"], "$.network.nodes", 2, MAX_NODES)
    for i, node in enumerate(nodes):
        identifier(node, f"$.network.nodes[{i}]")
    if len(nodes) != len(set(nodes)) or network["root"] not in nodes:
        raise ContractError("$.network", "node IDs must be unique and include the root")
    root = network["root"]
    read_quantity(network["root_voltage"], unit="pu", location=root, basis="voltage_base",
                  sign="positive", path="$.network.root_voltage", lower=.9, upper=1.1)
    branches = sequence(network["branches"], "$.network.branches", len(nodes) - 1, len(nodes) - 1)
    parent_of: dict[str, str] = {}
    branch_ids: set[str] = set()
    for i, branch in enumerate(branches):
        path = f"$.network.branches[{i}]"
        object_fields(branch, {"id", "parent", "child", "resistance", "reactance", "rating"}, path)
        branch_id = identifier(branch["id"], f"{path}.id")
        if branch_id in branch_ids:
            raise ContractError(path, "duplicate branch ID")
        branch_ids.add(branch_id)
        parent, child = branch["parent"], branch["child"]
        if parent not in nodes or child not in nodes:
            raise ContractError(path, "dangling branch endpoint")
        if child == root or child == parent or child in parent_of:
            raise ContractError(path, "root cannot have a parent; other nodes need exactly one distinct parent")
        parent_of[child] = parent
        for name in ("resistance", "reactance"):
            read_quantity(branch[name], unit="pu", location=branch_id, basis="impedance_base",
                          path=f"{path}.{name}", lower=0, upper=.2)
        read_quantity(branch["rating"], unit="VA", location=branch_id, basis="three_phase_total",
                      sign="positive", path=f"{path}.rating", lower=1, upper=1e9)
    for node in nodes:
        seen = set()
        current = node
        while current != root:
            if current in seen or current not in parent_of:
                raise ContractError("$.network", "topology must be a connected radial tree without cycles")
            seen.add(current)
            current = parent_of[current]

    profiles = sequence(s["profiles"], "$.profiles", len(nodes) - 1, len(nodes) - 1)
    profile_nodes: set[str] = set()
    for i, profile in enumerate(profiles):
        path = f"$.profiles[{i}]"
        object_fields(profile, {"node_id", "load", "reactive_load", "generation_available", "curtailment"}, path)
        node = profile["node_id"]
        if not isinstance(node, str) or node not in nodes or node == root or node in profile_nodes:
            raise ContractError(path, "one profile is required for each non-root node")
        profile_nodes.add(node)
        for field, unit, sign in (("load", "W", "consumption_positive"),
                                  ("reactive_load", "var", "consumption_positive"),
                                  ("generation_available", "W", "injection_positive"),
                                  ("curtailment", "W", "potential_not_injected")):
            read_quantity(profile[field], unit=unit, location=node, basis="three_phase_total",
                          sign=sign, support="scenario_intervals", path=f"{path}.{field}",
                          count=count, lower=0, upper=1e6)
        if any(c > g for c, g in zip(profile["curtailment"]["values"],
                                     profile["generation_available"]["values"])):
            raise ContractError(path, "curtailment cannot exceed available generation")

    storage = object_fields(s["storage"], {"node_id", "capacity", "initial_energy", "charge_limit",
                            "discharge_limit", "charge_efficiency", "discharge_efficiency",
                            "require_final_equal_initial"}, "$.storage")
    node = storage["node_id"]
    if not isinstance(node, str) or node not in nodes or node == root:
        raise ContractError("$.storage.node_id", "must name a non-root node")
    specs = {
        "capacity": ("J", "stored_energy", "positive", 1, 1e12),
        "initial_energy": ("J", "stored_energy", "nonnegative", 0, 1e12),
        "charge_limit": ("W", "three_phase_total", "nonnegative", 0, 1e6),
        "discharge_limit": ("W", "three_phase_total", "nonnegative", 0, 1e6),
        "charge_efficiency": ("1", "conversion_ratio", "positive", .01, 1),
        "discharge_efficiency": ("1", "conversion_ratio", "positive", .01, 1),
    }
    for field, (unit, basis, sign, lower, upper) in specs.items():
        read_quantity(storage[field], unit=unit, location=node, basis=basis, sign=sign,
                      path=f"$.storage.{field}", lower=lower, upper=upper)
    if storage["initial_energy"]["value"] > storage["capacity"]["value"]:
        raise ContractError("$.storage.initial_energy", "initial energy exceeds capacity")
    exact(storage["require_final_equal_initial"], True, "$.storage.require_final_equal_initial")

    policies = sequence(s["policies"], "$.policies", 2, 2)
    for i, (policy, policy_id, kind) in enumerate(zip(policies, ("baseline", "candidate"), ("idle", "fixed"))):
        path = f"$.policies[{i}]"
        object_fields(policy, {"id", "kind", "schedule"}, path)
        exact(policy["id"], policy_id, f"{path}.id")
        exact(policy["kind"], kind, f"{path}.kind")
        schedule = read_quantity(policy["schedule"], unit="W", location=node, basis="three_phase_total",
                                 sign="charging_positive", support="scenario_intervals",
                                 path=f"{path}.schedule", count=count, lower=-1e6, upper=1e6)
        if kind == "idle" and any(number != 0 for number in schedule):
            raise ContractError(path, "idle baseline must have exactly zero storage dispatch")

    limits = object_fields(s["limits"], {"voltage_min", "voltage_max"}, "$.limits")
    for field in limits:
        read_quantity(limits[field], unit="pu", location="all_nodes", basis="voltage_base", sign="positive",
                      path=f"$.limits.{field}", lower=.9, upper=1.1)
    if limits["voltage_min"]["value"] > limits["voltage_max"]["value"]:
        raise ContractError("$.limits", "voltage minimum exceeds maximum")
    # Bound size even when callers supply in-memory objects rather than JSON files.
    if len(canonical_bytes(s)) > MAX_INPUT_BYTES:
        raise ContractError("$", "scenario exceeds the input byte limit")
    return s

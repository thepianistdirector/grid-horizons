"""Read fixed original assets from the source tree or the built zip application.

Copyright (C) 2026 Lucas Santana. SPDX-License-Identifier: AGPL-3.0-only
"""

from __future__ import annotations

import hashlib
import pkgutil
from pathlib import Path

from . import __version__
from .contracts import decode_json

ASSETS = {
    "scenario.json": "scenarios/orchard-storage.json",
    "model.json": "docs/models/lossless-lindistflow-storage-v1.json",
}


def asset_bytes(name: str) -> bytes:
    relative = ASSETS[name]  # Only fixed built-in assets, never a user-supplied path.
    try:
        data = pkgutil.get_data("grid_horizons", "data/" + name)
        if data is not None:
            return data
    except OSError:
        pass
    return (Path(__file__).resolve().parents[2] / relative).read_bytes()


def example_scenario() -> dict:
    return decode_json(asset_bytes("scenario.json"))


def model_record() -> dict:
    return decode_json(asset_bytes("model.json"))


def build_identity() -> dict:
    try:
        data = pkgutil.get_data("grid_horizons", "data/build.json")
        if data is not None:
            return decode_json(data)
    except OSError:
        pass
    files = sorted(Path(__file__).parent.glob("*.py"))
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.name.encode("utf-8") + b"\0" + path.read_bytes())
    return {"version": __version__, "kind": "source-tree",
            "implementation_sha256": digest.hexdigest(), "source_revision": None}


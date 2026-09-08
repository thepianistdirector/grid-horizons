#!/usr/bin/env python3
"""Source-tree CLI entry point. SPDX-License-Identifier: AGPL-3.0-only."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from grid_horizons.cli import main

if __name__ == "__main__":
    raise SystemExit(main())

"""The raw adapter interface; this module contains no producer/evaluator math.

Copyright (C) 2026 Lucas Santana. SPDX-License-Identifier: AGPL-3.0-only
"""

# field -> (unit, basis, sign convention, interval aggregation)
NODE_FIELDS = {
    "voltage_squared": ("pu2", "voltage_base_squared", "nonnegative", "snapshot"),
    "load": ("W", "three_phase_total", "consumption_positive", "mean"),
    "served_load": ("W", "three_phase_total", "consumption_positive", "mean"),
    "unserved_load": ("W", "three_phase_total", "consumption_positive", "mean"),
    "reactive_load": ("var", "three_phase_total", "consumption_positive", "mean"),
    "generation_available": ("W", "three_phase_total", "injection_positive", "mean"),
    "curtailment": ("W", "three_phase_total", "potential_not_injected", "mean"),
    "generation_injected": ("W", "three_phase_total", "injection_positive", "mean"),
}
BRANCH_FIELDS = {
    "real_power": ("W", "three_phase_total", "parent_to_child_positive", "mean"),
    "reactive_power": ("var", "three_phase_total", "parent_to_child_positive", "mean"),
    "loading": ("1", "apparent_power_over_rating", "nonnegative", "snapshot"),
}
STORAGE_FIELDS = {
    "charge": ("W", "three_phase_total", "charging_positive", "mean"),
    "discharge": ("W", "three_phase_total", "discharging_positive", "mean"),
    "energy_start": ("J", "stored_energy", "stored_energy_positive", "state_start"),
    "energy_end": ("J", "stored_energy", "stored_energy_positive", "state_end"),
    "conversion_loss": ("J", "storage_conversion_loss", "nonnegative", "integral"),
}
GRID_FIELDS = {
    "import_power": ("W", "three_phase_total", "into_feeder_positive", "mean"),
    "export_power": ("W", "three_phase_total", "out_of_feeder_positive", "mean"),
    "reactive_power": ("var", "three_phase_total", "into_feeder_positive", "mean"),
}
NOT_EVALUATED = [
    "physical network losses (assumed zero only in the lossless model)",
    "full AC power flow and real-network applicability",
    "current/ampacity and transformer thermal state",
    "storage standing loss, degradation and electrochemical charge",
    "costs, emissions and lifecycle effects",
    "model-form uncertainty magnitude",
]


# Frozen confirmation preregistration

Written after the declared exploratory budget and before any confirmation run.

```json
{
  "question": "Do terminal-neutral storage schedules improve total energy losses or peak import versus idle storage, and how does ideal discrete tap control change the tradeoff?",
  "sources": [
    {
      "title": "MATPOWER manual \u00a74.3.2, Current Summation Method",
      "url": "https://matpower.app/manual/matpower/DistributionPowerFlow.html",
      "accessed": "2026-09-08",
      "context": "Radial backward/forward current summation; no MATPOWER execution or validation claimed."
    },
    {
      "title": "PyPSA documentation, Storage",
      "url": "https://docs.pypsa.org/latest/user-guide/optimization/storage/",
      "accessed": "2026-09-08",
      "context": "Charging/discharging efficiency directions and cyclic terminal state; no PyPSA execution claimed."
    }
  ],
  "exploratory_seeds": [
    11,
    13
  ],
  "confirmation_seeds": [
    41,
    43,
    47,
    53
  ],
  "load_scales": [
    0.7,
    0.85,
    1.0
  ],
  "solar_scale": 1,
  "steps": 96,
  "fixed_comparators": [
    "idle storage + tap 0 baseline",
    "idle storage + tap -2",
    "idle storage + tap 2",
    "idle storage + tap 4"
  ],
  "search": {
    "storage": [
      {
        "amplitude_kw": 2,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      },
      {
        "amplitude_kw": 2,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      },
      {
        "amplitude_kw": 4,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      },
      {
        "amplitude_kw": 4,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      },
      {
        "amplitude_kw": 8,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      },
      {
        "amplitude_kw": 8,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      },
      {
        "amplitude_kw": 12,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      },
      {
        "amplitude_kw": 12,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      }
    ],
    "combined": [
      {
        "amplitude_kw": 2,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      },
      {
        "amplitude_kw": 2,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      },
      {
        "amplitude_kw": 4,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      },
      {
        "amplitude_kw": 4,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      },
      {
        "amplitude_kw": 8,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      },
      {
        "amplitude_kw": 8,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      },
      {
        "amplitude_kw": 12,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      },
      {
        "amplitude_kw": 12,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      }
    ],
    "budget": "8 candidates each family, every seed \u00d7 load combination; 48 evaluations per family, no adaptive additions"
  },
  "selection": "Among candidates feasible on all four seed 11/13 \u00d7 load .7/.85 training cases whose baselines are feasible, choose lowest arithmetic mean total_loss_kwh separately from lowest mean peak_import_kw; tie break lexical policy id. Load 1 excluded before ranking; report all failure outcomes. Freeze both winners per family before confirmation.",
  "primary_objective": "total_loss_kwh = network_loss_kwh + storage_loss_kwh",
  "secondary_objective": "peak_import_kw; independently selected, no combined scalar score",
  "falsifiers": [
    "Selected storage total-loss benefit is falsified within this panel if any comparable confirmation case has total_loss >= baseline.",
    "Line-loss reduction does not establish total-loss reduction when conversion losses exceed line savings.",
    "Any infeasible baseline excludes its entire scenario from ranking, even if another policy becomes feasible.",
    "Any invalid energy or power residual, nonconvergence, terminal SOC error or limit violation invalidates a candidate benefit claim."
  ],
  "uncertainty": "Report min/max paired differences across four frozen seeds by load, no population inference or significance. Seeds alter hourly solar only; demand profile and feeder shared.",
  "stopping_rule": "Exactly one default demonstration +12 exploration +12 confirmation =25 scenarios, 96 intervals; verify each. No tuning after confirmation. Stop if 300 CPU seconds exceeded; preserve all attempts.",
  "scope": "Original synthetic balanced constant-PQ 13-bus feeder; no physical/public-feeder, lifecycle, universal optimum or field claims.",
  "frozen_selected": {
    "storage_loss": {
      "source_policy": "storage_1",
      "parameters": {
        "amplitude_kw": 2,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      },
      "selection_metric": "total_loss_kwh",
      "training_case_count": 4,
      "mean_training_objective": 6.3739270671143915
    },
    "storage_peak": {
      "source_policy": "storage_4",
      "parameters": {
        "amplitude_kw": 8,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 0
      },
      "selection_metric": "peak_import_kw",
      "training_case_count": 4,
      "mean_training_objective": 63.18090696787917
    },
    "combined_loss": {
      "source_policy": "combined_1",
      "parameters": {
        "amplitude_kw": 2,
        "charge_start": 10,
        "charge_end": 14,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      },
      "selection_metric": "total_loss_kwh",
      "training_case_count": 4,
      "mean_training_objective": 6.103779260677028
    },
    "combined_peak": {
      "source_policy": "combined_4",
      "parameters": {
        "amplitude_kw": 8,
        "charge_start": 9,
        "charge_end": 13,
        "discharge_start": 17,
        "discharge_end": 21,
        "tap": 4
      },
      "selection_metric": "peak_import_kw",
      "training_case_count": 4,
      "mean_training_objective": 63.15713932779005
    }
  },
  "frozen_at_utc": "2026-09-08T17:25:21Z",
  "selection_sha256": "5f23d0ad605f9d97f59d66491a50246299552f3c4bfa3a51bc212d5ede078cac",
  "protocol_sha256": "1d11f9b8b3bc864658f81e82475fe960a44a8407e1e33044916b72e2a39f0a4d"
}
```

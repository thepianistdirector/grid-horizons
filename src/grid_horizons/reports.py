"""Accessible offline views over evaluator-owned evidence, with no network code.

Copyright (C) 2026 Lucas Santana. SPDX-License-Identifier: AGPL-3.0-only
"""

from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import math
import os
import re
import uuid
from pathlib import Path

from .contracts import MAX_RAW_BYTES, canonical_bytes, digest, load_json
from .evaluator import compare
from .raw_contract import NODE_FIELDS, BRANCH_FIELDS, STORAGE_FIELDS, GRID_FIELDS, NOT_EVALUATED

REPORT_SCHEMA = "grid-horizons.report/v1"
LABELS = {
    "import_energy": "Imported energy", "export_energy": "Exported energy",
    "net_import_energy": "Net imported energy", "served_load_energy": "Served load",
    "unserved_load_energy": "Unserved load", "available_generation_energy": "Generation potential",
    "injected_generation_energy": "Actual generation injected", "curtailed_potential_energy": "Curtailed potential",
    "storage_charge_energy": "Storage charging energy", "storage_discharge_energy": "Storage discharged energy",
    "storage_conversion_loss": "Storage conversion loss", "initial_storage_energy": "Initial stored energy",
    "final_storage_energy": "Final stored energy", "peak_import_power": "Peak real import",
    "min_voltage": "Minimum modeled voltage", "max_voltage": "Maximum modeled voltage",
    "max_loading": "Maximum apparent-power loading",
}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def display(quantity: dict | None) -> str:
    if not quantity:
        return "Not available"
    value, unit = quantity["value"], quantity["unit"]
    if unit == "J": value, unit = value / 3600000, "kWh"
    if unit == "W": value, unit = value / 1000, "kW"
    if unit == "1": value, unit = value * 100, "% of rating"
    decimals = 5 if unit == "pu" else 3
    number = f"{value:,.{decimals}f}".rstrip("0").rstrip(".")
    if number == "-0": number = "0"
    return f"{number} {unit}"


def _status(state: str) -> str:
    names = {"COMPLETED_VALID": "Model-feasible", "COMPLETED_INFEASIBLE": "Model-infeasible",
             "INVALID_RESULT": "Invalid output", "RESOURCE_EXHAUSTED": "Resource budget exhausted",
             "FAILED_SOLVER": "Numerical run failed", "FAILED_EVALUATOR": "Evaluator failed",
             "CANCELLED": "Cancelled", "LOST": "Interrupted / lost", "NOT_RUN": "Not run"}
    return names.get(state, state)


CSS = """
:root { color-scheme: light; --ink:#172b3a; --muted:#526272; --blue:#244e77; --gold:#b77a28; --line:#d8e0e5; --paper:#fafbf9; }
* { box-sizing:border-box; } html { scroll-behavior:auto; }
body { margin:0; background:var(--paper); color:var(--ink); font:16px/1.6 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
a { color:var(--blue); text-underline-offset:3px; } a:hover { text-decoration-thickness:2px; }
:focus-visible { outline:3px solid #aa610c; outline-offset:4px; }
.skip { position:absolute; left:16px; top:-90px; background:white; padding:12px; z-index:2; }.skip:focus { top:12px; }
.wrap { width:min(1120px,calc(100% - 48px)); margin:auto; }
header { border-bottom:1px solid var(--line); background:#fff; }
.brand { display:flex; align-items:center; justify-content:space-between; gap:20px; padding:22px 0; }
.wordmark { font-size:17px; font-weight:750; letter-spacing:-.4px; }.wordmark span { display:inline-grid; place-items:center; background:var(--ink); color:white; width:32px; height:32px; margin-right:10px; font-size:12px; letter-spacing:1px; }
.version { font-size:13px; color:var(--muted); }
nav { display:flex; gap:24px; padding:0 0 17px; flex-wrap:wrap; font-size:14px; }
main { padding-bottom:60px; }.hero { display:grid; grid-template-columns:1.7fr 1fr; gap:54px; padding:50px 0 32px; }
.eyebrow { margin:0 0 12px; font-size:11px; font-weight:750; letter-spacing:1.8px; text-transform:uppercase; color:var(--blue); }
h1 { font-size:clamp(30px,4vw,46px); line-height:1.12; letter-spacing:-1.6px; margin:0 0 20px; font-weight:650; max-width:650px; }
h2 { font-size:24px; line-height:1.3; letter-spacing:-.6px; margin:0 0 12px; } h3 { font-size:17px; margin:0 0 12px; }
p { margin:0 0 14px; }.intro { color:var(--muted); max-width:610px; }.case { border-left:1px solid var(--line); padding-left:26px; }
.case dl { margin:0; }.case dt { font-size:12px; color:var(--muted); }.case dd { margin:0 0 12px; font-weight:600; }
.connections { padding:0; margin:0; list-style:none; font-size:13px; }.connections li { margin:5px 0; overflow-wrap:anywhere; }
.verdict { background:#edf2f6; border:1px solid #cbd9e4; padding:22px 26px; margin:0 0 30px; }
.verdict p:last-child { margin:0; }.verdict strong { display:block; font-size:18px; margin-bottom:6px; }
.caps { font-size:11px; letter-spacing:1.2px; font-weight:750; color:var(--blue); }
.arms { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
.arm { background:#fff; border:1px solid var(--line); padding:24px; border-top:4px solid var(--blue); min-width:0; }
.arm.candidate { border-top-color:var(--gold); }.arm-head { display:flex; gap:12px; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; margin-bottom:20px; }
.badge { display:inline-block; font-size:12px; font-weight:650; border:1px solid #bdcbd5; padding:3px 8px; border-radius:3px; }
.pair { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin:0; }.pair dt { font-size:13px; color:var(--muted); }.pair dd { margin:4px 0 0; font-size:27px; line-height:1.25; font-variant-numeric:tabular-nums; letter-spacing:-.6px; }
.arm small { display:block; margin-top:18px; color:var(--muted); font-size:12px; }.state { font-size:11px; font-family:ui-monospace,monospace; overflow-wrap:anywhere; }
section { scroll-margin-top:20px; }.section { margin-top:42px; }.section-head { display:flex; align-items:baseline; justify-content:space-between; gap:20px; }.note { color:var(--muted); font-size:14px; }
.table-wrap { overflow-x:auto; border:1px solid var(--line); background:white; margin:16px 0; }.table-wrap:focus { outline-offset:2px; }
table { border-collapse:collapse; width:100%; font-size:14px; } th,td { padding:12px 16px; border-bottom:1px solid #e4e9ec; text-align:left; vertical-align:top; } thead { background:#f2f5f6; } th { font-weight:600; } tbody tr:last-child td,tbody tr:last-child th { border-bottom:0; }
td.numeric,th.numeric { text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; } caption { text-align:left; font-size:13px; color:var(--muted); padding:12px 16px; border-bottom:1px solid var(--line); }
.quantity-table { min-width:540px; }.trajectory { min-width:790px; }.attempt-table { min-width:550px; }
.columns { display:grid; grid-template-columns:1fr 1fr; gap:32px; }.limits { padding:22px 24px; background:#f2f4ef; border:1px solid #d7ded1; }.limits ul { padding-left:20px; margin-bottom:0; }.limits li { margin:7px 0; }
details { border:1px solid var(--line); background:#fff; margin:12px 0; } summary { cursor:pointer; padding:15px 18px; font-weight:600; } details>div { padding:0 18px 18px; }
.downloads { display:flex; gap:10px 20px; flex-wrap:wrap; padding:0; list-style:none; font-size:14px; }.download { padding:8px 12px; display:inline-block; border:1px solid var(--line); background:#fff; }
code { font:12px/1.5 ui-monospace,SFMono-Regular,Consolas,monospace; overflow-wrap:anywhere; } pre { white-space:pre-wrap; padding:16px; background:#f0f3f5; overflow-wrap:anywhere; }
.finding { padding:12px 16px; border-left:3px solid #b77a28; background:#fff7e9; margin:10px 0; overflow-wrap:anywhere; }
footer { border-top:1px solid var(--line); padding:25px 0; color:var(--muted); font-size:12px; } footer .wrap { display:flex; gap:20px; justify-content:space-between; flex-wrap:wrap; }
@media(max-width:720px) { .wrap { width:calc(100% - 32px); }.hero { grid-template-columns:1fr; gap:22px; padding-top:32px; }.case { border-left:0; border-top:1px solid var(--line); padding:20px 0 0; }.case dl { display:grid; grid-template-columns:1fr 1fr; gap:12px; }.arms,.columns { grid-template-columns:1fr; }.section-head { display:block; }.verdict { padding:18px; }.arm { padding:20px; } nav { gap:12px 20px; }.brand { padding:16px 0; }.pair dd { font-size:25px; }.version { max-width:95px; text-align:right; }.section { margin-top:32px; } }
@media print { body { background:white; font-size:10pt; }.wrap { width:100%; }.hero { padding-top:16px; }.table-wrap { overflow:visible; }.trajectory,.quantity-table,.attempt-table { min-width:0; }th,td { padding:6px; } nav,.skip { display:none; } .arm,.verdict,section { break-inside:avoid; } details { display:block; } }
@media(prefers-reduced-motion:reduce) { * { scroll-behavior:auto !important; } }
"""


def _metric(result: dict | None, name: str) -> str:
    return display(result.get("metrics", {}).get(name)) if result else "Not available"


def _trajectory(raw: dict, label: str, state: str) -> str:
    rows = []
    for r in raw.get("intervals", []):
        try:
            st, grid = r["storage"], r["grid"]
            voltage = min(math.sqrt(n["voltage_squared"]["value"]) for n in r["nodes"])
            loading = max(b["loading"]["value"] for b in r["branches"]) * 100
            rows.append(f'<tr><th scope="row">{esc(r["id"])} · {r["start_s"]/3600:g}–{r["end_s"]/3600:g} h</th>'
                        f'<td class="numeric">{grid["import_power"]["value"]/1000:g}</td>'
                        f'<td class="numeric">{grid["export_power"]["value"]/1000:g}</td>'
                        f'<td class="numeric">{grid["reactive_power"]["value"]/1000:g}</td>'
                        f'<td class="numeric">{st["charge"]["value"]/1000:g} / {st["discharge"]["value"]/1000:g}</td>'
                        f'<td class="numeric">{st["energy_end"]["value"]/3600000:g}</td>'
                        f'<td class="numeric">{voltage:.5f}</td><td class="numeric">{loading:.2f}%</td></tr>')
        except (KeyError, TypeError, ValueError):
            rows.append('<tr><td colspan="8">Incomplete or malformed interval. Inspect raw JSON and evaluator findings.</td></tr>')
    if not rows:
        rows.append('<tr><td colspan="8">No complete intervals retained.</td></tr>')
    return f'''<div class="table-wrap" role="region" aria-label="{esc(label)} interval records" tabindex="0">
<table class="trajectory"><caption>{esc(label)} · {_status(state)}. Raw adapter trajectory; its evaluator state governs eligibility.</caption>
<thead><tr><th scope="col">Interval [start, end)</th><th scope="col" class="numeric">Import<br>kW</th><th scope="col" class="numeric">Export<br>kW</th><th scope="col" class="numeric">Reactive<br>kvar</th><th scope="col" class="numeric">Charge / discharge<br>kW</th><th scope="col" class="numeric">Stored at end<br>kWh</th><th scope="col" class="numeric">Min. voltage<br>pu</th><th scope="col" class="numeric">Max. loading<br>VA / rating</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>'''


def render_html(data: dict, raw_by_policy: dict) -> str:
    scenario, study = data["scenario"], data["study"]
    by_policy = {r["policy_id"]: r for r in data["results"]}
    comparison = data["comparison"]
    baseline, candidate = by_policy.get("baseline"), by_policy.get("candidate")
    eligible = comparison["state"] == "INDETERMINATE"
    narrative = (f'Peak real import: <b>{_metric(baseline,"peak_import_power")}</b> for idle storage and '
                 f'<b>{_metric(candidate,"peak_import_power")}</b> for the fixed schedule. '
                 f'Net imported energy: <b>{_metric(baseline,"net_import_energy")}</b> and '
                 f'<b>{_metric(candidate,"net_import_energy")}</b>, respectively.' if eligible else
                 'At least one policy lacks a valid, feasible completed result. Inspect the retained failure or limit findings before comparing quantities.')
    arms = []
    for policy_id, title in (("baseline", "Idle storage"), ("candidate", "Fixed storage schedule")):
        r = by_policy.get(policy_id)
        state = r["state"] if r else "NOT_RUN"
        arms.append(f'''<article class="arm {policy_id}"><div class="arm-head"><div><p class="eyebrow">{policy_id}</p><h3>{title}</h3></div><span class="badge">{_status(state)}</span></div><dl class="pair"><div><dt>Peak real import</dt><dd>{_metric(r,'peak_import_power')}</dd></div><div><dt>Net imported energy</dt><dd>{_metric(r,'net_import_energy')}</dd></div></dl><small>Served load {_metric(r,'served_load_energy')} · final storage {_metric(r,'final_storage_energy')}</small><span class="state">{esc(state)}</span></article>''')
    quantity_rows = ''.join(f'<tr><th scope="row">{label}</th><td class="numeric">{_metric(baseline,key)}</td><td class="numeric">{_metric(candidate,key)}</td></tr>' for key,label in LABELS.items())
    connections = ''.join(f'<li>{esc(b["parent"])} → {esc(b["child"])} · {b["rating"]["value"]/1000:g} kVA rating</li>' for b in scenario["network"]["branches"])
    trajectories = ''.join(_trajectory(raw_by_policy[p], "Idle storage" if p == "baseline" else "Fixed storage schedule", by_policy[p]["state"]) for p in ("baseline","candidate") if p in raw_by_policy)
    findings = []
    for r in data["results"]:
        for finding in r["findings"]:
            findings.append(f'<div class="finding"><b>{esc(r["policy_id"])} · {esc(finding["code"])}</b><br>{esc(finding["message"])}<br><code>{esc(finding.get("location",""))} {esc(finding.get("interval", ""))}</code></div>')
    if not findings:
        findings = ['<p class="note">No modeled constraint or consistency findings in the retained completed results. This is not AC or engineering validation.</p>']
    ledger_rows = []
    for r in data["results"]:
        for key, q in r.get("ledger", {}).items():
            ledger_rows.append(f'<tr><th scope="row">{esc(r["policy_id"])} · {esc(key.replace("_"," "))}</th><td class="numeric">{q["value"]:.12g} {esc(q["unit"])}</td></tr>')
    attempt_rows = ''.join(f'<tr><th scope="row"><code>{esc(r["attempt_id"])}</code></th><td>{esc(r["policy_id"])}</td><td>{esc(r["state"])}</td></tr>' for r in data["attempts"])
    downloads = [('scenario.json','Scenario JSON'),('report.json','Report JSON'),('intervals.csv','Raw quantities CSV'),('model.json','Model record'),('study.json','Study manifest'),('source.json','Source record')]
    for p in raw_by_policy:
        downloads.extend([(p+'-raw.json',p.capitalize()+' raw JSON'),(p+'-manifest.json',p.capitalize()+' run manifest')])
    links = ''.join(f'<li><a class="download" href="{url}" download>{label}</a></li>' for url,label in downloads)
    hours = scenario["intervals"][-1]["end_s"] / 3600
    content = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'"><meta name="color-scheme" content="light"><title>{esc(scenario['title'])} · Grid Horizons</title><style>{CSS}</style></head><body>
<a class="skip" href="#main">Skip to study</a><header><div class="wrap"><div class="brand"><div class="wordmark"><span aria-hidden="true">GH</span>Grid Horizons</div><div class="version">Offline laboratory<br>Version {esc(study['software']['version'])}</div></div><nav aria-label="Study sections"><a href="#overview">Overview</a><a href="#quantities">Quantities</a><a href="#trajectories">Trajectories</a><a href="#evidence">Evidence &amp; files</a></nav></div></header>
<main id="main" class="wrap"><section class="hero" id="overview"><div><p class="eyebrow">Fictional energy study · original synthetic inputs</p><h1>{esc(scenario['title'])}</h1><p class="intro">Two predeclared storage policies. The same demand and generation. Every interval retained, with independent checks before comparison.</p><p class="note">Lossless linearized radial model with storage conversion losses. No real-grid advice or improvement claim.</p></div><aside class="case" aria-label="Scenario at a glance"><dl><div><dt>Study size</dt><dd>{len(scenario['network']['nodes'])} nodes · {len(scenario['intervals'])} intervals · {hours:g} h</dd></div><div><dt>Fictional voltage limits</dt><dd>{scenario['limits']['voltage_min']['value']:g}–{scenario['limits']['voltage_max']['value']:g} pu</dd></div></dl><p class="caps">Simulated connections</p><ul class="connections">{connections}</ul></aside></section>
<div class="verdict"><p class="caps">{esc(comparison['state'])}</p><strong>{'A tradeoff to inspect. No overall winner.' if eligible else 'This comparison is not eligible.'}</strong><p>{narrative}</p><p class="note">{esc(comparison['reason'])}</p></div><div class="arms">{''.join(arms)}</div>
<section class="section" id="quantities"><div class="section-head"><h2>The full quantity vector</h2><p class="note">Same inputs · separate quantities · no composite score</p></div><p class="note">Energy is stored in joules and shown here in kWh (1 kWh = 3,600,000 J). Curtailment is unused potential, separate from actual injection. Infeasible quantities are diagnostic; failed or invalid attempts have no metrics.</p><div class="table-wrap" role="region" aria-label="Policy quantity comparison" tabindex="0"><table class="quantity-table"><caption>Whole-study evaluator totals and modeled extrema. Export is retained when interpreting net import.</caption><thead><tr><th scope="col">Quantity</th><th scope="col" class="numeric">Idle storage</th><th scope="col" class="numeric">Fixed schedule</th></tr></thead><tbody>{quantity_rows}</tbody></table></div></section>
<section class="section" id="trajectories"><h2>Follow the intervals</h2><p class="note">Half-open intervals start at a fictional time origin. Active and reactive power have separate units. Scroll tables horizontally on narrow screens; each table can receive keyboard focus.</p>{trajectories or '<p>No interval evidence yet. Resume the study to create a new attempt.</p>'}</section>
<section class="section columns"><div><h2>Independent checks</h2>{''.join(findings)}<details><summary>Balance residuals, in their original units</summary><div><p class="note">Floating-point consistency tolerances do not estimate physical model error.</p><div class="table-wrap" role="region" aria-label="Balance residuals" tabindex="0"><table><thead><tr><th scope="col">Ledger</th><th scope="col">Residual</th></tr></thead><tbody>{''.join(ledger_rows) or '<tr><td colspan="2">No valid residual ledger available.</td></tr>'}</tbody></table></div></div></details></div><aside class="limits"><h2>Model limits stay visible</h2><p>The network balance assumes zero line loss; physical network loss is not computed. Storage conversion losses are computed separately.</p><p class="caps">Not evaluated</p><ul>{''.join('<li>'+esc(x)+'</li>' for x in NOT_EVALUATED)}</ul><p class="note">No optimization, live controls, private utility data, operational advice or qualified engineering validation.</p></aside></section>
<section class="section" id="evidence"><h2>Reopen the evidence</h2><p class="note">These exports are views of immutable scenario and attempt records. The complete study directory retains unsuccessful attempts. A fresh run always uses a new directory.</p><ul class="downloads">{links}</ul><details><summary>Tool identity and reproduction</summary><div><p>Scenario SHA-256<br><code>{esc(study['scenario_sha256'])}</code></p><p>Implementation SHA-256<br><code>{esc(study['software']['implementation_sha256'])}</code></p><p>From the parent of the complete study directory, using its original tool build:</p><pre><code>python3 grid-horizons-{esc(study['software']['version'])}.pyz verify study
python3 grid-horizons-{esc(study['software']['version'])}.pyz rerun study --output study-rerun</code></pre><p class="note">Replace “study” with the actual directory name. Source-tree development uses “python3 grid-horizons.py”. The JSON report retains exact software identity; a static report alone is not a simulator.</p></div></details><details><summary>All {len(data['attempts'])} retained attempts</summary><div><div class="table-wrap" role="region" aria-label="Retained attempt history" tabindex="0"><table class="attempt-table"><thead><tr><th scope="col">Attempt</th><th scope="col">Policy</th><th scope="col">Terminal state</th></tr></thead><tbody>{attempt_rows or '<tr><td colspan="3">No admitted terminal attempts yet.</td></tr>'}</tbody></table></div><p class="note">Raw records and run manifests for every attempt remain in the study’s attempts directory. Retrying creates a new identity and preserves old failures.</p></div></details></section></main><footer><div class="wrap"><span>Grid Horizons · original content AGPL-3.0-only · Lucas Santana</span><span>Software checks and human/domain review are separate.</span></div></footer></body></html>'''
    return content


def _csv_text(value) -> str:
    text = str(value)
    return "'" + text if text.startswith(("=", "+", "-", "@", "\t", "\r")) else text


def csv_export(results: list[dict], raw_by_policy: dict, scenario: dict) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(["attempt_id", "policy_id", "terminal_state", "interval_id", "start_s", "end_s",
                     "location", "quantity", "value", "unit", "basis", "sign", "aggregation"])
    by_policy = {r["policy_id"]: r for r in results}
    for policy_id, raw in raw_by_policy.items():
        result = by_policy[policy_id]
        for row in raw.get("intervals", []):
            if not isinstance(row, dict):
                writer.writerow([result["attempt_id"], policy_id, result["state"], "MALFORMED_INTERVAL"])
                continue
            node_records = row.get("nodes", [])
            branch_records = row.get("branches", [])
            groups = [(n, NODE_FIELDS) for n in node_records if isinstance(n, dict)] if isinstance(node_records, list) else []
            groups += [(b, BRANCH_FIELDS) for b in branch_records if isinstance(b, dict)] if isinstance(branch_records, list) else []
            groups += [(row.get("storage", {}), STORAGE_FIELDS), (row.get("grid", {}), GRID_FIELDS)]
            for record, fields in groups:
                record = record if isinstance(record, dict) else {}
                for field in fields:
                    q = record.get(field, {})
                    q = q if isinstance(q, dict) else {}
                    support = q.get("support", {})
                    support = support if isinstance(support, dict) else {}
                    values = [result["attempt_id"], policy_id, result["state"], row.get("id", "MISSING"),
                              row.get("start_s", "MISSING"), row.get("end_s", "MISSING"), q.get("location", "MISSING"),
                              field, q.get("value", "MISSING"), q.get("unit", "MISSING"), q.get("basis", "MISSING"),
                              q.get("sign", "MISSING"), support.get("aggregation", "MISSING")]
                    writer.writerow([v if type(v) in (int, float) else _csv_text(v) for v in values])
    return stream.getvalue().encode("utf-8")


def _report_directory_check(directory: Path) -> dict:
    from .coordinator import StudyError, file_digest
    if directory.is_symlink() or not directory.is_dir():
        raise StudyError("Missing or linked report snapshot")
    for path in directory.iterdir():
        if path.is_symlink() or not path.is_file():
            raise StudyError("Report artifacts must be regular files")
    index = load_json(directory / "integrity.json")
    if not isinstance(index, dict) or set(index) != {"schema_version", "files"} or index["schema_version"] != 1 or not isinstance(index["files"], dict):
        raise StudyError("Malformed report integrity index")
    if set(index["files"]) != {p.name for p in directory.iterdir()} - {"integrity.json"}:
        raise StudyError("Report artifact coverage differs")
    for name, expected in index["files"].items():
        if file_digest(directory / name) != expected:
            raise StudyError(f"Report artifact digest differs: {name}")
    return index


def write_report(study: Path, study_manifest: dict, scenario: dict,
                 results: list[dict], attempts: list[dict]) -> None:
    from .coordinator import atomic_bytes, atomic_json, _sync_directory, StudyError
    raw_by_policy = {r["policy_id"]: load_json(study / "attempts" / r["attempt_id"] / "raw.json", MAX_RAW_BYTES) for r in results}
    comparison = compare(results) if len(results) == 2 else {
        "state": "INELIGIBLE", "reason": "Both policies do not yet have terminal evidence.", "differences": {}}
    data = {"schema_version": REPORT_SCHEMA, "study": study_manifest, "scenario": scenario,
            "results": results, "attempts": attempts, "comparison": comparison,
            "view_note": "Derived report; immutable scenario/run records remain the evidence authority."}
    report_id = digest(data)
    files = {"report.json": canonical_bytes(data) + b"\n", "report.html": render_html(data, raw_by_policy).encode("utf-8"),
             "intervals.csv": csv_export(results, raw_by_policy, scenario)}
    for name in ("scenario.json", "model.json", "source.json", "study.json"):
        files[name] = (study / name).read_bytes()
    for result in results:
        policy_id = result["policy_id"]
        files[policy_id + "-raw.json"] = canonical_bytes(raw_by_policy[policy_id]) + b"\n"
        files[policy_id + "-manifest.json"] = (study / "attempts" / result["attempt_id"] / "manifest.json").read_bytes()
    destination = study / "reports" / report_id
    if not destination.exists():
        staging = study / "reports" / (".preparing-" + uuid.uuid4().hex)
        staging.mkdir()
        for name, content in files.items():
            atomic_bytes(staging / name, content)
        atomic_json(staging / "integrity.json", {"schema_version": 1,
                    "files": {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}})
        os.rename(staging, destination)
        _sync_directory(study / "reports")
    index = _report_directory_check(destination)
    if index["files"] != {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}:
        raise StudyError("Existing report snapshot differs from deterministic rendering")
    for name, content in files.items():
        if name not in {"scenario.json", "model.json", "source.json", "study.json"}:
            atomic_bytes(study / name, content, replace=True)
    atomic_json(study / "latest-report.json", {"schema_version": 1, "report_id": report_id}, replace=True)


def verify_reports(study: Path, selected: list[dict] | None = None, attempts: list[dict] | None = None) -> None:
    from .coordinator import StudyError, file_digest, _inside
    pointer = load_json(_inside(study, "latest-report.json"))
    if not isinstance(pointer, dict) or set(pointer) != {"schema_version", "report_id"} or pointer["schema_version"] != 1:
        raise StudyError("Malformed latest report pointer; resume to regenerate derived views")
    report_id = pointer["report_id"]
    if not isinstance(report_id, str) or not re.fullmatch(r"[0-9a-f]{64}", report_id):
        raise StudyError("Malformed report identity")
    directory = _inside(study, "reports/" + report_id)
    index = _report_directory_check(directory)
    data = load_json(directory / "report.json", MAX_RAW_BYTES)
    if digest(data) != report_id:
        raise StudyError("Report identity differs from its payload")
    if selected is not None and (data.get("results") != selected or data.get("attempts") != attempts):
        raise StudyError("Derived report is stale; resume to regenerate it from immutable attempts")
    for name, expected in index["files"].items():
        if file_digest(_inside(study, name)) != expected:
            raise StudyError("Derived report view is incomplete or changed; resume to regenerate it from immutable evidence")

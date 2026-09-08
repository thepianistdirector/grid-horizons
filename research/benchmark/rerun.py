#!/usr/bin/env python3
"""Reproduce fixed benchmark using frozen CLI; independent reference only. AGPL-3.0-only."""
import argparse
import csv
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
PACKAGE = PROJECT / 'releases/1.0.0rc1/grid-horizons.pyz'

def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def cpu():
    a, b = resource.getrusage(resource.RUSAGE_SELF), resource.getrusage(resource.RUSAGE_CHILDREN)
    return a.ru_utime + a.ru_stime + b.ru_utime + b.ru_stime

def linear(matrix, rhs):
    """Original dense partial-pivot elimination, no numerical dependencies."""
    n = len(rhs)
    a = [list(row) + [r] for row, r in zip(matrix, rhs)]
    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(a[i][k]))
        a[k], a[pivot] = a[pivot], a[k]
        if abs(a[k][k]) < 1e-14:
            raise ArithmeticError('singular Newton Jacobian')
        for i in range(k + 1, n):
            ratio = a[i][k] / a[k][k]
            for j in range(k + 1, n + 1):
                a[i][j] -= ratio * a[k][j]
    x = [0.] * n
    for i in range(n - 1, -1, -1):
        x[i] = (a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x

def reference(s, p, t):
    """Nodal complex power equations and analytic rectangular Jacobian."""
    n = len(s['branches']) + 1
    y = [[0j] * n for _ in range(n)]
    for b in s['branches']:
        i, j = b['parent'], b['child']
        adm = 1 / complex(b['r_pu'], b['x_pu'])
        y[i][i] += adm; y[j][j] += adm
        y[i][j] -= adm; y[j][i] -= adm
    demand = [complex(s['load_kw'][t][i] - s['solar_kw'][t][i] +
                      (p['dispatch_kw'][t] if i == s['storage']['node'] else 0),
                      s['reactive_kvar'][t][i]) / s['base_kva'] for i in range(n)]
    v = [complex(1 + .00625 * p['tap'][t])] * n
    for iteration in range(31):
        current = [sum(y[i][j] * v[j] for j in range(n)) for i in range(n)]
        f = [v[i] * current[i].conjugate() + demand[i] for i in range(1, n)]
        residual = max(map(abs, f))
        if residual <= 1e-11:
            break
        if iteration == 30:
            raise ArithmeticError('independent Newton iteration budget exhausted')
        jac = []
        for i in range(1, n):
            real, imag = [], []
            for j in range(1, n):
                dx = (current[i].conjugate() if i == j else 0) + v[i] * y[i][j].conjugate()
                dy = (1j * current[i].conjugate() if i == j else 0) - 1j * v[i] * y[i][j].conjugate()
                real.extend((dx.real, dy.real)); imag.extend((dx.imag, dy.imag))
            jac.extend((real, imag))
        step = linear(jac, [-q for z in f for q in (z.real, z.imag)])
        for i in range(1, n):
            v[i] += complex(step[2 * (i - 1)], step[2 * (i - 1) + 1])
    source = v[0] * current[0].conjugate() * s['base_kva']
    losses = []
    for b in s['branches']:
        a, z = v[b['parent']], v[b['child']]
        flow = (a - z) / complex(b['r_pu'], b['x_pu'])
        losses.append(((a * flow.conjugate()) + (z * (-flow).conjugate())).real * s['base_kva'])
    return dict(interval=t, voltage=[[z.real, z.imag] for z in v],
                source_kva=[source.real, source.imag], branch_loss_kw=losses,
                network_loss_kw=sum(losses), residual_pu=residual, iterations=iteration)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, default=HERE / 'attempt-001')
    args = ap.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(HERE):
        raise SystemExit('Output must remain inside research/benchmark')
    plan = json.loads((HERE / 'preregistration.json').read_text())
    if digest(PACKAGE) != plan['package_sha256']:
        raise SystemExit('Frozen package hash mismatch')
    out.mkdir(exist_ok=False)
    for folder in ('logs', 'inputs', 'reference'):
        (out / folder).mkdir()
    started, started_cpu = time.perf_counter(), cpu()
    commands = []
    def cli(*args):
        if cpu() - started_cpu > 240:
            raise RuntimeError('Preregistered CPU stopping rule')
        index = len(commands)
        cmd = [sys.executable, str(PACKAGE), 'lab', *map(str, args)]
        t, c = time.perf_counter(), cpu()
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
        result = subprocess.run(cmd, capture_output=True, env=env, timeout=60)
        (out / 'logs' / f'{index:03d}.stdout').write_bytes(result.stdout)
        (out / 'logs' / f'{index:03d}.stderr').write_bytes(result.stderr)
        commands.append(dict(index=index, argv=cmd, exit_code=result.returncode,
                             wall_seconds=time.perf_counter() - t, cpu_seconds=cpu() - c,
                             stdout_bytes=len(result.stdout), stderr_bytes=len(result.stderr)))
        write(out / 'commands.json', commands)
        if result.returncode:
            raise RuntimeError(f'CLI failed; preserved logs {index}')
        return json.loads(result.stdout)
    identity = cli('identity')
    if identity['build']['implementation_sha256'] != plan['implementation_sha256']:
        raise RuntimeError('Implementation identity mismatch')
    cli('example', '--seed', 17, '--steps', 96, '--output', out / 'inputs' / 'original-example.json')
    # Input generation is the only import from the packaged implementation.
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(PACKAGE))
    from grid_horizons.ac import example
    cases = []
    for seed, steps, tolerance in itertools.product([17, 23, 31], [24, 48, 96, 288], [1e-6, 1e-8, 1e-10, 1e-12]):
        s = example(seed=seed, steps=steps)
        s['policies'] = s['policies'][:1]
        s['solver']['tolerance'] = tolerance
        name = f's{seed}-n{steps}-tol{tolerance:.0e}'
        cases.append((dict(id=name, group='core', seed=seed, steps=steps, tolerance=tolerance), s))
    s = json.loads((out / 'inputs' / 'original-example.json').read_text())
    cases.append((dict(id='original-four-policies', group='original', seed=17, steps=96, tolerance=1e-10), s))
    for control in ['no-load', 'analytic-two-bus', 'failed-solver']:
        s = example(seed=17, steps=24)
        s['policies'] = s['policies'][:1]
        s['solver']['tolerance'] = 1e-12
        if control == 'failed-solver':
            s['solver']['max_iterations'] = 1
        else:
            if control == 'analytic-two-bus':
                s['branches'] = [dict(parent=0, child=1, r_pu=.1, x_pu=0., current_limit_pu=.9)]
                s['storage']['node'] = 1
            n = len(s['branches']) + 1
            for key in ('load_kw', 'reactive_kvar', 'solar_kw'):
                s[key] = [[0.] * n for _ in range(24)]
            if control == 'analytic-two-bus':
                s['load_kw'] = [[0., 10.] for _ in range(24)]
        s['name'] = control
        cases.append((dict(id=control, group='control', seed=17, steps=24, tolerance=1e-12), s))
    for meta, s in cases:
        write(out / 'inputs' / (meta['id'] + '.json'), s)
    # A bounded two-case campaign replaces first two standalone runs.
    write(out / 'inputs' / 'campaign.json', dict(schema='grid-horizons.campaign/v1', scenarios=[s for _, s in cases[:2]]))
    cli('campaign', out / 'inputs' / 'campaign.json', '--output', out / 'campaign')
    data = []
    reference_cpu = 0.
    for index, (meta, s) in enumerate(cases):
        if cpu() - started_cpu > 240:
            raise RuntimeError('Preregistered CPU stopping rule')
        study = out / 'campaign' / f'case-{index:03d}' if index < 2 else out / meta['id']
        if index >= 2:
            cli('run', out / 'inputs' / (meta['id'] + '.json'), '--output', study)
        cli('verify', study)
        summary = json.loads((study / 'summary.json').read_text())
        for p in s['policies']:
            raw = json.loads((study / (p['id'] + '.json')).read_text())
            ev = raw['evaluation']
            item = dict(**meta, policy=p['id'], study=str(study.relative_to(out)), state=ev['state'],
                        violations=len(ev['violations']), invalid=len(ev['invalid']),
                        violation_reasons=sorted(set(x['reason'] for x in ev['violations'])),
                        invalid_reasons=sorted(set(x['reason'] for x in ev['invalid'])),
                        ranking=summary['ranking'], metrics=ev['metrics'])
            refs, discrepancies = [], []
            c = cpu()
            for t, row in enumerate(raw['raw']['rows']):
                r = reference(s, p, t)
                refs.append(r)
                voltage = max(abs(complex(*a) - complex(*b)) for a, b in zip(row['voltage'], r['voltage']))
                source = abs(complex(*row['source_kva']) - complex(*r['source_kva']))
                loss = abs(ev['intervals'][t]['network_loss_kw'] - r['network_loss_kw'])
                discrepancies.append(dict(interval=t, voltage_abs_pu=voltage, source_abs_kva=source, loss_abs_kw=loss))
            reference_cpu += cpu() - c
            write(out / 'reference' / (meta['id'] + '-' + p['id'] + '.json'), dict(reference=refs, discrepancies=discrepancies))
            if refs:
                item['reference'] = {k: max(x[k] for x in discrepancies) for k in ('voltage_abs_pu', 'source_abs_kva', 'loss_abs_kw')}
                item['reference'].update(max_residual_pu=max(x['residual_pu'] for x in refs),
                                         max_iterations=max(x['iterations'] for x in refs))
                item['solver_iterations'] = dict(min=min(x['iterations'] for x in raw['raw']['rows']), max=max(x['iterations'] for x in raw['raw']['rows']))
                if meta['id'] == 'analytic-two-bus':
                    v = (1 + math.sqrt(1 - 4 * .1 * .1)) / 2
                    loss = .1 * (.1 / v) ** 2 * s['base_kva']
                    item['analytic'] = dict(expected_voltage_pu=v, expected_loss_kw=loss,
                                            producer_voltage_error_pu=max(abs(complex(*r['voltage'][1]) - v) for r in raw['raw']['rows']),
                                            producer_loss_error_kw=max(abs(r['network_loss_kw'] - loss) for r in ev['intervals']),
                                            newton_voltage_error_pu=max(abs(complex(*r['voltage'][1]) - v) for r in refs))
            data.append(item)
        write(out / 'results.json', data)
        print(f'{index + 1}/{len(cases)} {meta["id"]}; cumulative CPU {cpu() - started_cpu:.2f}s', flush=True)
    fields = ['id', 'group', 'seed', 'steps', 'tolerance', 'policy', 'state', 'violations', 'invalid', 'violation_reasons', 'invalid_reasons']
    metric_names = list(next(x for x in data if x['metrics'])['metrics'])
    with (out / 'all-scenario-feasibility.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields + metric_names)
        w.writeheader()
        for row in data:
            w.writerow({**{k: row[k] for k in fields}, **row['metrics']})
    write(out / 'costs.json', dict(wall_seconds=time.perf_counter() - started,
                                  cpu_seconds=cpu() - started_cpu, reference_cpu_seconds=reference_cpu,
                                  cli_cpu_seconds=sum(x['cpu_seconds'] for x in commands),
                                  cli_commands=len(commands), scenarios=len(cases), policy_combinations=len(data),
                                  intervals=sum(x['steps'] for x in data),
                                  output_bytes_before_hash_manifest=sum(p.stat().st_size for p in out.rglob('*') if p.is_file()),
                                  paid_resources=False, runtime_identity=identity,
                                  package_sha256=digest(PACKAGE), preregistration_sha256=digest(HERE / 'preregistration.json'),
                                  rerun_script_sha256=digest(Path(__file__))))
    write(out / 'hashes.json', {str(p.relative_to(out)): digest(p) for p in sorted(out.rglob('*')) if p.is_file()})

if __name__ == '__main__':
    main()

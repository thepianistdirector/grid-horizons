#!/usr/bin/env python3
"""Additive release bridge; preserve original preregistration and evidence."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import time
import zipfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, default=HERE / 'bridge-rc2-001')
    args = ap.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(HERE):
        raise SystemExit('Output must remain within benchmark')
    out.mkdir(exist_ok=False)
    old = PROJECT / 'releases/1.0.0rc1/grid-horizons.pyz'
    new = PROJECT / 'releases/1.0.0rc2/grid-horizons.pyz'
    implementation = '3f46ec88b717c2811186fe2c4c7f2c926a37e110281c115798720bd87e143023'
    source = HERE / 'attempt-001/original-four-policies'
    prereg = dict(frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 reason='Root supplied rc2 fixing input size, help and graph scaling after rc1 confirmation. Additive bridge checks no numerical change.',
                 original_preregistration_sha256=sha(HERE / 'preregistration.json'),
                 old_package_sha256=sha(old), new_package_sha256=sha(new), new_implementation_sha256=implementation,
                 case='Original seed17 96-step four-policy scenario, exact saved rc1 scenario input',
                 acceptance='ac.py/ac_check.py byte-identical across packages; raw records and full evaluations identical for every policy; verify succeeds.',
                 budget='One additional scenario, four policy combinations, 96 intervals each; total 53 scenarios/59 combinations; one CPU child at a time.')
    write(out / 'preregistration.json', prereg)
    write(out / 'preregistration-hash.json', {'sha256':sha(out / 'preregistration.json')})
    module_hashes = {}
    with zipfile.ZipFile(old) as a, zipfile.ZipFile(new) as b:
        for module in ['grid_horizons/ac.py', 'grid_horizons/ac_check.py']:
            h1, h2 = hashlib.sha256(a.read(module)).hexdigest(), hashlib.sha256(b.read(module)).hexdigest()
            module_hashes[module] = dict(rc1=h1, rc2=h2, identical=h1 == h2)
    commands = []
    for command in [['identity'], ['run', str(source / 'scenario.json'), '--output', str(out / 'study')], ['verify', str(out / 'study')]]:
        argv = [sys.executable, str(new), 'lab'] + command
        t = time.perf_counter(); c = resource.getrusage(resource.RUSAGE_CHILDREN)
        r = subprocess.run(argv, capture_output=True, timeout=60)
        d = resource.getrusage(resource.RUSAGE_CHILDREN)
        idx = len(commands)
        (out / f'{idx}.stdout').write_bytes(r.stdout); (out / f'{idx}.stderr').write_bytes(r.stderr)
        commands.append(dict(argv=argv, exit_code=r.returncode, wall_seconds=time.perf_counter()-t,
                             cpu_seconds=d.ru_utime+d.ru_stime-c.ru_utime-c.ru_stime))
        write(out / 'commands.json', commands)
        if r.returncode:
            raise SystemExit('Bridge CLI failure retained')
        if command == ['identity']:
            assert json.loads(r.stdout)['build']['implementation_sha256'] == implementation
    records = {name: json.loads((source / (name+'.json')).read_text()) ==
               json.loads((out / 'study' / (name+'.json')).read_text())
               for name in ['baseline', 'storage', 'tap', 'combined']}
    result = dict(modules=module_hashes, full_policy_records_identical=records,
                  passed=all(records.values()) and all(x['identical'] for x in module_hashes.values()),
                  cpu_seconds=sum(x['cpu_seconds'] for x in commands),
                  wall_seconds=sum(x['wall_seconds'] for x in commands))
    write(out / 'result.json', result)
    write(out / 'hashes.json', {str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file()})
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()

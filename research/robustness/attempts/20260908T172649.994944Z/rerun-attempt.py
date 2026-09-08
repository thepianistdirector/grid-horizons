#!/usr/bin/env python3
"""Frozen robustness design. CLI is the only producer; new attempt per invocation."""
import argparse
import collections
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
EXPECTED = 'cdf8e0b82397cbad5e9f5979fd01d98fd931a7c772c5dcd1c8b42a35ac90a4a4'
SEEDS = [101, 103, 107, 109]
# name, load scale, solar scale, load delay h, solar delay h, R scale, I-limit scale
DESIGN = [('nominal',1,1,0,0,1,1), ('load_low',.8,1,0,0,1,1),
          ('load_high',1.2,1,0,0,1,1), ('solar_low',1,.7,0,0,1,1),
          ('solar_high',1,1.3,0,0,1,1), ('load_early',1,1,-3,0,1,1),
          ('load_late',1,1,3,0,1,1), ('solar_early',1,1,0,-2,1,1),
          ('solar_late',1,1,0,2,1,1), ('resistance_high',1,1,0,0,1.5,1),
          ('derated',1,1,0,0,1,.8), ('joint_adverse',1.2,.7,3,-2,1.5,.8)]

def dump(path, data):
    with path.open('x') as f:
        json.dump(data, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args=parser.parse_args()
    out=(args.output or HERE/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')).resolve()
    if not out.is_relative_to(HERE):
        raise SystemExit('Output must stay within robustness directory')
    out.mkdir(parents=True, exist_ok=False)
    package=PROJECT/'releases/1.0.0rc1/grid-horizons.pyz'
    start=time.perf_counter(); own_start=time.process_time()
    initial=resource.getrusage(resource.RUSAGE_CHILDREN)
    allowed=os.sched_getaffinity(0); os.sched_setaffinity(0,{min(allowed)})
    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    commands=[]
    def cpu():
        usage=resource.getrusage(resource.RUSAGE_CHILDREN)
        return time.process_time()-own_start+usage.ru_utime+usage.ru_stime-initial.ru_utime-initial.ru_stime
    def cli(label,*args,allow_failure=False):
        if cpu()>290: raise RuntimeError('CPU stopping rule')
        t=time.perf_counter(); before=cpu()
        cmd=[sys.executable,str(package),'lab',*map(str,args)]
        result=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=60)
        (out/(label+'.stdout.txt')).write_text(result.stdout)
        (out/(label+'.stderr.txt')).write_text(result.stderr)
        record=dict(label=label,command=cmd,returncode=result.returncode,wall_seconds=time.perf_counter()-t,cpu_seconds=cpu()-before)
        commands.append(record)
        with (out/'commands.jsonl').open('a') as f: f.write(json.dumps(record)+'\n')
        if result.returncode and not allow_failure: raise RuntimeError(record)
        return result
    identity=json.loads(cli('identity','identity').stdout)
    assert identity['build']['implementation_sha256']==EXPECTED, identity
    dump(out/'provenance.json',dict(identity=identity,package=str(package),package_sha256=sha(package),python=platform.python_version(),python_executable=str(Path(sys.executable).resolve()),python_executable_sha256=sha(Path(sys.executable).resolve()),preregistration_sha256=sha(HERE/'preregistration.md'),rerun_sha256=sha(Path(__file__)),affinity=sorted(os.sched_getaffinity(0)),source_hashes={str(p.relative_to(PROJECT)):sha(p) for p in [PROJECT/'docs/v1/CONTRACT.md',PROJECT/'docs/v1/MODEL.md',PROJECT/'src/grid_horizons/ac.py',PROJECT/'src/grid_horizons/ac_check.py',PROJECT/'src/grid_horizons/lab.py']}))
    scenarios=[]; design=[]
    for seed in SEEDS:
        basepath=out/f'example-{seed}.json'
        cli(f'example-{seed}','example','--seed',seed,'--steps',96,'--output',basepath)
        base=json.loads(basepath.read_text())
        for name,ls,ss,lh,sh,rs,il in DESIGN:
            s=copy.deepcopy(base); s['name']=f'robustness seed {seed} / {name}'
            for key,scale,shift in [('load_kw',ls,lh),('reactive_kvar',ls,lh),('solar_kw',ss,sh)]:
                s[key]=[[round(v*scale,9) for v in base[key][(i-int(shift*4))%96]] for i in range(96)]
            for branch in s['branches']:
                branch['r_pu']*=rs; branch['current_limit_pu']*=il
            scenarios.append(s); design.append(dict(seed=seed,treatment=name))
    outage=copy.deepcopy(scenarios[0]); outage['name']='unsupported source outage / disconnected parent -1'; outage['branches'][0]['parent']=-1
    all_scenarios=scenarios+[outage]
    spec=out/'campaign.json'; dump(spec,dict(schema='grid-horizons.campaign/v1',scenarios=all_scenarios))
    dump(out/'design.json',design)
    r=cli('campaign-all','campaign',spec,'--output',out/'campaign-all',allow_failure=True)
    studies=[]; inventories=[]
    if r.returncode==0:
        studies=[out/'campaign-all'/f'case-{i:03d}' for i in range(48)]
        inventories=json.loads((out/'campaign-all/inventory.json').read_text())
    else:
        if 'file exceeds' not in r.stdout and 'size' not in r.stdout and 'MiB' not in r.stdout:
            raise RuntimeError('Unexpected campaign failure: '+r.stdout)
        for j,seed in enumerate(SEEDS):
            items=scenarios[j*12:(j+1)*12]+([outage] if j==3 else [])
            shard=out/f'campaign-{seed}.json'; dump(shard,dict(schema='grid-horizons.campaign/v1',scenarios=items))
            result=cli(f'campaign-{seed}','campaign',shard,'--output',out/f'campaign-{seed}',allow_failure=True)
            if result.returncode==0:
                studies.extend(out/f'campaign-{seed}'/f'case-{i:03d}' for i in range(12))
                inventories.extend(dict(x,seed=seed) for x in json.loads((out/f'campaign-{seed}/inventory.json').read_text()))
            else:
                if 'file exceeds' not in result.stdout and 'size' not in result.stdout and 'MiB' not in result.stdout: raise RuntimeError(result.stdout)
                for i,s in enumerate(items):
                    path=out/f'input-{seed}-{i:02d}.json'; dump(path,s)
                    study=out/f'run-{seed}-{i:02d}'
                    run_result=cli(f'run-{seed}-{i:02d}','run',path,'--output',study,allow_failure=i==12)
                    inventories.append(dict(seed=seed,case=i,state='REJECTED_INPUT' if run_result.returncode else 'RECORDED',stdout=run_result.stdout))
                    if i<12: studies.append(study)
    dump(out/'all-attempt-inventory.json',dict(commands=commands,scenario_attempts=inventories,unique_modeled_scenarios=48,unsupported_outage_inputs=1))
    nominal=out/'nominal-standalone.json'; dump(nominal,scenarios[0])
    cli('run-nominal','run',nominal,'--output',out/'standalone')
    cli('verify-standalone','verify',out/'standalone')
    rows=[]
    for i,study in enumerate(studies):
        cli(f'verify-{i:03d}','verify',study)
        summary=json.loads((study/'summary.json').read_text())
        if i==0:
            repeated=json.loads((out/'standalone/summary.json').read_text())
            assert summary['policies']==repeated['policies']
        base=next(p for p in summary['policies'] if p['policy']=='baseline')
        for policy in summary['policies']:
            m=policy['metrics']; bm=base['metrics']
            row=dict(**design[i],study=str(study.relative_to(out)),policy=policy['policy'],state=policy['state'],baseline_state=base['state'],ranked=policy['policy'] in summary['ranking'],violations=policy['violations'],invalid=policy['invalid'],metrics=m)
            row.update(loss_saving_kwh=bm['total_loss_kwh']-m['total_loss_kwh'],peak_saving_kw=bm['peak_import_kw']-m['peak_import_kw'],network_saving_kwh=bm['network_loss_kwh']-m['network_loss_kwh'])
            row['loss_saving_percent']=100*row['loss_saving_kwh']/bm['total_loss_kwh']
            row['peak_saving_percent']=100*row['peak_saving_kw']/bm['peak_import_kw']
            rows.append(row)
    aggregate={}
    for policy in ['baseline','storage','tap','combined']:
        subset=[r for r in rows if r['policy']==policy]
        eligible=[r for r in subset if r['state']==r['baseline_state']=='COMPLETED_VALID']
        keys=['loss_saving_kwh','loss_saving_percent','peak_saving_kw','peak_saving_percent','network_saving_kwh']
        aggregate[policy]=dict(states=dict(collections.Counter(r['state'] for r in subset)),all_scenario_ranges={k:[min(r[k] for r in subset),max(r[k] for r in subset)] for k in keys},eligible_count=len(eligible),eligible_ranges={k:[min(r[k] for r in eligible),max(r[k] for r in eligible)] for k in keys} if eligible else {},loss_improves_eligible=sum(r['loss_saving_kwh']>0 for r in eligible),peak_improves_eligible=sum(r['peak_saving_kw']>0 for r in eligible),practical_loss_eligible=sum(r['loss_saving_kwh']>=.5 for r in eligible),practical_peak_eligible=sum(r['peak_saving_kw']>=1 for r in eligible))
    findings=dict(design=design,modeled_scenarios=48,trajectories=192,unique_seed_count=4,aggregate=aggregate,rows=rows,max_power_residual_pu=max(r['metrics']['max_power_residual_pu'] for r in rows),max_abs_energy_residual_kwh=max(abs(r['metrics']['energy_residual_kwh']) for r in rows),max_abs_terminal_storage_delta_kwh=max(abs(r['metrics']['storage_delta_kwh']) for r in rows),standalone_deterministic_repeat=True,verified_studies=49)
    dump(out/'findings.json',findings)
    usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    dump(out/'costs.json',dict(wall_seconds=time.perf_counter()-start,total_cpu_seconds=cpu(),child_peak_rss_kib=usage.ru_maxrss,command_count=len(commands),scenario_executions=50,modeled_policy_trajectories_including_repeat=196,solver_intervals_including_repeat=196*96,one_cpu_affinity=True,package_sha256_after=sha(package),budget_cpu_seconds=300))
    dump(out/'final-command-inventory.json',commands)
    dump(out/'checksums.json',{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file()})
    print(json.dumps(dict(output=str(out),aggregate=aggregate,costs=json.loads((out/'costs.json').read_text())),indent=2))

if __name__=='__main__': main()

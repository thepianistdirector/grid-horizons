#!/usr/bin/env python3
"""Execute the predeclared selected-policy transfer appendix and RC2 bridge."""
import collections
import copy
import datetime
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import zipfile
from rerun import HERE, PROJECT, dump, sha

def main():
    out=HERE/'appendix-attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out.mkdir(parents=True,exist_ok=False)
    main_attempt=sorted(p.parent for p in (HERE/'attempts').glob('*/findings.json'))[-1]
    package=PROJECT/'releases/1.0.0rc2/grid-horizons.pyz'
    prior=PROJECT/'releases/1.0.0rc1/grid-horizons.pyz'
    start=time.perf_counter(); cpu_start=time.process_time()
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1')
    commands=[]
    def cpu():
        r=resource.getrusage(resource.RUSAGE_CHILDREN)
        return time.process_time()-cpu_start+r.ru_utime+r.ru_stime
    def cli(label,*args):
        t=time.perf_counter(); c=cpu()
        cmd=[sys.executable,str(package),'lab',*map(str,args)]
        r=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=60)
        (out/(label+'.stdout.txt')).write_text(r.stdout)
        (out/(label+'.stderr.txt')).write_text(r.stderr)
        record=dict(label=label,command=cmd,returncode=r.returncode,wall_seconds=time.perf_counter()-t,cpu_seconds=cpu()-c)
        commands.append(record)
        with (out/'commands.jsonl').open('a') as f: f.write(json.dumps(record)+'\n')
        assert r.returncode==0, r.stdout
        assert cpu()<275
        return json.loads(r.stdout)
    identity=cli('identity','identity')
    assert identity['build']['implementation_sha256']=='3f46ec88b717c2811186fe2c4c7f2c926a37e110281c115798720bd87e143023'
    unchanged={}
    import hashlib
    with zipfile.ZipFile(package) as now, zipfile.ZipFile(prior) as old:
        for name in ('grid_horizons/ac.py','grid_horizons/ac_check.py'):
            assert now.read(name)==old.read(name)
            unchanged[name]=hashlib.sha256(now.read(name)).hexdigest()
    selection_path=PROJECT/'research/policies/selection.json'
    selection=json.loads(selection_path.read_text()); dump(out/'selection.json',selection)
    dump(out/'provenance.json',dict(identity=identity,package_sha256=sha(package),main_attempt=str(main_attempt),selection_source_sha256=sha(selection_path),unchanged_rc1_rc2_members=unchanged,appendix_preregistration_sha256=sha(HERE/'appendix-preregistration.md'),script_sha256=sha(Path(__file__))))
    originals=json.loads((main_attempt/'campaign.json').read_text())['scenarios'][:48]
    scenarios=[]; designs=[]
    for original in originals:
        treatment=original['name'].split(' / ')[1]
        if treatment not in ('nominal','load_late','joint_adverse'): continue
        s=copy.deepcopy(original); s['policies']=[s['policies'][0]]
        for name,selected in selection['selected'].items():
            pars=selected['parameters']; a=pars['amplitude_kw']
            dispatch=[a if pars['charge_start']<=(t+.5)/4<pars['charge_end'] else -a*.95*.95 if pars['discharge_start']<=(t+.5)/4<pars['discharge_end'] else 0. for t in range(96)]
            s['policies'].append(dict(id=name,dispatch_kw=dispatch,tap=[pars['tap']]*96))
        scenarios.append(s); designs.append(dict(seed=s['provenance']['seed'],treatment=treatment))
    dump(out/'campaign.json',dict(schema='grid-horizons.campaign/v1',scenarios=scenarios))
    cli('campaign','campaign',out/'campaign.json','--output',out/'campaign')
    rows=[]
    for i,design in enumerate(designs):
        study=out/'campaign'/f'case-{i:03d}'; cli(f'verify-{i:03d}','verify',study)
        summary=json.loads((study/'summary.json').read_text())
        baseline=next(p for p in summary['policies'] if p['policy']=='baseline')
        for p in summary['policies']:
            m=p['metrics']; b=baseline['metrics']
            rows.append(dict(**design,policy=p['policy'],state=p['state'],baseline_state=baseline['state'],metrics=m,violations=p['violations'],invalid=p['invalid'],loss_saving_kwh=b['total_loss_kwh']-m['total_loss_kwh'],peak_saving_kw=b['peak_import_kw']-m['peak_import_kw']))
    bridge_input=out/'bridge-input.json'; dump(bridge_input,originals[0])
    cli('run-bridge','run',bridge_input,'--output',out/'bridge')
    cli('verify-bridge','verify',out/'bridge')
    for name in ('baseline','storage','tap','combined'):
        assert json.loads((out/'bridge'/f'{name}.json').read_text())==json.loads((main_attempt/'standalone'/f'{name}.json').read_text())
    aggregate={}
    for name in ['baseline',*selection['selected']]:
        subset=[r for r in rows if r['policy']==name]
        aggregate[name]=dict(states=dict(collections.Counter(r['state'] for r in subset)),jointly_feasible=sum(r['state']==r['baseline_state']=='COMPLETED_VALID' for r in subset),all_scenario_loss_saving_kwh=[min(r['loss_saving_kwh'] for r in subset),max(r['loss_saving_kwh'] for r in subset)],all_scenario_peak_saving_kw=[min(r['peak_saving_kw'] for r in subset),max(r['peak_saving_kw'] for r in subset)])
    dump(out/'findings.json',dict(aggregate=aggregate,rows=rows,modeled_scenarios=12,trajectories=60,bridge_exact_raw_and_evaluation_equality=True,verified_studies=13,max_power_residual_pu=max(r['metrics']['max_power_residual_pu'] for r in rows),max_abs_energy_residual_kwh=max(abs(r['metrics']['energy_residual_kwh']) for r in rows)))
    dump(out/'costs.json',dict(wall_seconds=time.perf_counter()-start,total_cpu_seconds=cpu(),child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,scenario_executions=13,modeled_policy_trajectories_including_bridge=64,intervals=64*96,commands=len(commands)))
    dump(out/'checksums.json',{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file()})
    print(json.dumps(dict(output=str(out),aggregate=aggregate),indent=2))

if __name__=='__main__': main()

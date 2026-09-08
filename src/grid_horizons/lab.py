"""Versioned study persistence and CLI. AGPL-3.0-only."""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import os
import platform
import sys
import time
import zipfile
from pathlib import Path
from . import ac
from .ac_check import evaluate
from .assets import build_identity
from .contracts import decode_json


def data_bytes(x): return (json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p):
    if p.stat().st_size>64*1024*1024: raise ValueError('file exceeds 64 MiB')
    return decode_json(p.read_bytes(), 64*1024*1024)
def write(p,x):
    with p.open('xb') as f: f.write(data_bytes(x))
def identity(): return dict(build=build_identity(),python=platform.python_version(),system=platform.system(),machine=platform.machine(),model=ac.MODEL)


def run(s,out,stop_after=None):
    ac.validate(s);out.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter();write(out/'scenario.json',s)
    write(out/'manifest.json',dict(schema='grid-horizons.ac-study/v2',identity=identity(),scenario_sha256=sha(data_bytes(s))))
    policies=[]
    for p in s['policies']:
        raw=ac.produce(s,p,stop_after)
        ev=evaluate(s,p,raw) if raw['state']=='SOLVED' else dict(state=raw['state'],error=raw.get('error'),metrics={},violations=[],invalid=[],intervals=[])
        record=dict(policy=p['id'],raw=raw,evaluation=ev)
        write(out/(p['id']+'.json'),record);policies.append(dict(policy=p['id'],**ev))
    valid=[x for x in policies if x['state']=='COMPLETED_VALID']
    base=next(x for x in policies if x['policy']=='baseline')
    ranking=sorted(valid,key=lambda x:x['metrics']['total_loss_kwh']) if base['state']=='COMPLETED_VALID' else []
    summary=dict(schema='grid-horizons.ac-summary/v2',name=s['name'],policies=policies,ranking=[x['policy'] for x in ranking],ranking_objective='network plus storage conversion loss kWh; only feasible candidates and feasible baseline',seconds=time.perf_counter()-start)
    write(out/'summary.json',summary)
    from .lab_report import render
    (out/'report.html').write_text(render(s,summary),encoding='utf-8')
    with (out/'feasibility.csv').open('x',newline='') as f:
        writer=csv.writer(f);writer.writerow(['policy','state','violations','invalid','total_loss_kwh','peak_import_kw','min_voltage_pu','max_loading'])
        for x in policies: writer.writerow([x['policy'],x['state'],len(x['violations']),len(x['invalid'])]+[x['metrics'].get(k,'') for k in ('total_loss_kwh','peak_import_kw','min_voltage_pu','max_loading')])
    write(out/'checksums.json',{p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()})
    return summary


def verify(path):
    hashes=read(path/'checksums.json')
    if not isinstance(hashes,dict) or not hashes: raise ValueError('invalid checksums')
    actual={p.name for p in path.iterdir() if p.is_file()}-{'checksums.json'}
    if actual!=set(hashes): raise ValueError('missing or unexpected study files')
    for name,digest in hashes.items():
        if Path(name).name!=name or sha((path/name).read_bytes())!=digest: raise ValueError('study integrity mismatch: '+name)
    s=ac.validate(read(path/'scenario.json'));m=read(path/'manifest.json')
    if m['schema']!='grid-horizons.ac-study/v2' or m['scenario_sha256']!=sha(data_bytes(s)): raise ValueError('manifest mismatch')
    if m['identity']['build']['implementation_sha256']!=identity()['build']['implementation_sha256']: raise ValueError('different implementation; reopen with original packaged build')
    summary=read(path/'summary.json')
    evaluations=[]
    for p in s['policies']:
        record=read(path/(p['id']+'.json'))
        if record['policy']!=p['id']: raise ValueError('policy binding mismatch')
        if record['raw']['state']=='SOLVED':
            ev=evaluate(s,p,record['raw'])
            if ev!=record['evaluation']: raise ValueError('independent evaluation mismatch')
        else:
            if record['raw']['state'] not in ('CANCELLED','FAILED_SOLVER'): raise ValueError('unknown failure state')
            ev=dict(state=record['raw']['state'],error=record['raw'].get('error'),metrics={},violations=[],invalid=[],intervals=[])
            if ev!=record['evaluation']: raise ValueError('failure evaluation mismatch')
        evaluations.append(dict(policy=p['id'],**ev))
    if summary['policies']!=evaluations or summary['name']!=s['name']: raise ValueError('summary mismatch')
    base=next(x for x in evaluations if x['policy']=='baseline')
    ranking=[x['policy'] for x in sorted([x for x in evaluations if x['state']=='COMPLETED_VALID'],key=lambda x:x['metrics']['total_loss_kwh'])] if base['state']=='COMPLETED_VALID' else []
    if ranking!=summary['ranking']: raise ValueError('ranking mismatch')
    return summary


def export(path,output):
    verify(path)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(path.iterdir()):
            if p.is_file(): z.write(p,p.name)


def import_study(archive,output):
    with zipfile.ZipFile(archive) as z:
        entries=z.infolist()
        if len(entries)>40 or sum(x.file_size for x in entries)>128*1024*1024: raise ValueError('archive resource bound exceeded')
        names=[x.filename for x in entries]
        if len(names)!=len(set(names)) or any(Path(n).name!=n or '\\' in n or n in ('.','..') for n in names): raise ValueError('unsafe archive paths')
        output.mkdir(parents=True,exist_ok=False)
        for item in entries:
            with (output/item.filename).open('xb') as f: f.write(z.read(item))
    return verify(output)


def main(argv):
    p=argparse.ArgumentParser(prog='grid-horizons lab',description='Offline AC feeder laboratory; original synthetic data only')
    sub=p.add_subparsers(dest='command',required=True)
    e=sub.add_parser('example');e.add_argument('--output',type=Path,required=True);e.add_argument('--seed',type=int,default=17);e.add_argument('--steps',type=int,choices=(24,48,96,288,480),default=96)
    for name in ('validate','run'):
        c=sub.add_parser(name);c.add_argument('scenario',type=Path)
        if name=='run': c.add_argument('--output',type=Path,required=True);c.add_argument('--stop-after',type=int)
    for name in ('verify','rerun','resume','export'):
        c=sub.add_parser(name);c.add_argument('study',type=Path)
        if name!='verify': c.add_argument('--output',type=Path,required=True)
    c=sub.add_parser('import');c.add_argument('archive',type=Path);c.add_argument('--output',type=Path,required=True)
    c=sub.add_parser('campaign');c.add_argument('spec',type=Path);c.add_argument('--output',type=Path,required=True)
    sub.add_parser('identity')
    a=p.parse_args(argv)
    try:
        if sys.platform!='linux' or sys.implementation.name!='cpython' or sys.version_info[:2]!=(3,12): raise ValueError('supported environment: Linux CPython 3.12')
        if a.command=='identity': result=identity()
        elif a.command=='example':
            s=ac.validate(ac.example(seed=a.seed,steps=a.steps));write(a.output,s);result=dict(state='EXAMPLE_WRITTEN',path=str(a.output))
        elif a.command=='validate': ac.validate(read(a.scenario));result=dict(state='VALIDATED_INPUT')
        elif a.command=='run':
            if a.stop_after is not None and a.stop_after<0: raise ValueError('stop-after must be nonnegative')
            result=run(read(a.scenario),a.output,a.stop_after)
        elif a.command=='verify': result=verify(a.study)
        elif a.command in ('rerun','resume'):
            try: verify(a.study)
            except FileNotFoundError:
                if a.command!='resume' or (a.study/'checksums.json').exists(): raise
                m=read(a.study/'manifest.json');s=ac.validate(read(a.study/'scenario.json'))
                if m['identity']!=identity() or m['scenario_sha256']!=sha(data_bytes(s)): raise ValueError('interrupted manifest mismatch')
            result=run(read(a.study/'scenario.json'),a.output)
            # Explicit new directory is the new attempt. Original evidence is never changed.
        elif a.command=='export': export(a.study,a.output);result=dict(state='EXPORTED',path=str(a.output))
        elif a.command=='import': result=import_study(a.archive,a.output)
        else:
            spec=read(a.spec)
            if set(spec)!= {'schema','scenarios'} or spec['schema']!='grid-horizons.campaign/v1' or not isinstance(spec['scenarios'],list) or not 1<=len(spec['scenarios'])<=120: raise ValueError('campaign: schema and 1..120 inline scenarios required')
            a.output.mkdir(parents=True,exist_ok=False);write(a.output/'spec.json',spec);attempts=[]
            for i,s in enumerate(spec['scenarios']):
                try:
                    r=run(s,a.output/f'case-{i:03d}');attempts.append(dict(case=i,state='RECORDED',policies=[dict(policy=x['policy'],state=x['state'],metrics=x['metrics']) for x in r['policies']]))
                except (ValueError,TypeError,KeyError) as exc: attempts.append(dict(case=i,state='REJECTED_INPUT',error=str(exc)))
                temp=a.output/'inventory.next.json';temp.write_bytes(data_bytes(attempts));os.replace(temp,a.output/'inventory.json')
            result=dict(state='CAMPAIGN_RECORDED',attempts=len(attempts),inventory=str(a.output/'inventory.json'))
        if 'policies' in result: result=dict(states={x['policy']:x['state'] for x in result['policies']},ranking=result['ranking'],seconds=result['seconds'])
        print(json.dumps(result,indent=2,allow_nan=False));return 0
    except (ValueError,TypeError,KeyError,OSError,zipfile.BadZipFile) as exc:
        print(json.dumps(dict(state='REJECTED',error=str(exc),recovery='Preserve existing evidence. Correct the input or use its original build, then choose a new output path.')));return 2

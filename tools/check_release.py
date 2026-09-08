"""Exercise the packaged CLI in a clean project-local venv and directory."""
import argparse
import hashlib
import json
import os
import platform
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('package',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
a.package=a.package.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
shutil.copyfile(a.package,out/'grid-horizons.pyz')
subprocess.run([sys.executable,'-m','venv','--without-pip',str(out/'venv')],check=True)
python=out/'venv/bin/python';env={'PATH':str(python.parent)+':/usr/bin:/bin','LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1'}
records=[];start=time.perf_counter()
def command(args,expected=0):
 t=time.perf_counter();r=subprocess.run([str(python),'-I','grid-horizons.pyz',*args],cwd=out,env=env,capture_output=True,text=True,timeout=60)
 records.append(dict(args=args,code=r.returncode,seconds=time.perf_counter()-t,stdout=r.stdout,stderr=r.stderr))
 (out/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
 if r.returncode!=expected:raise AssertionError((args,r.returncode,r.stdout,r.stderr))
 return json.loads(r.stdout) if r.stdout.startswith('{') else r.stdout
id=command(['lab','identity']);command(['lab','example','--output','scenario.json']);command(['lab','validate','scenario.json'])
command(['lab','run','scenario.json','--output','study']);command(['lab','verify','study'])
command(['lab','export','study','--output','study.zip']);command(['lab','import','study.zip','--output','reopened']);command(['lab','rerun','reopened','--output','rerun'])
for name in ['baseline.json','storage.json','tap.json','combined.json']:
 assert (out/'study'/name).read_bytes()==(out/'rerun'/name).read_bytes()
command(['lab','run','scenario.json','--output','study'],2)
command(['lab','run','scenario.json','--output','cancelled','--stop-after','5']);command(['lab','resume','cancelled','--output','resumed']);command(['lab','verify','cancelled'])
# Model a process killed after manifest/scenario persistence: retain unfinished original.
(out/'interrupted').mkdir()
for name in ('scenario.json','manifest.json'):shutil.copyfile(out/'study'/name,out/'interrupted'/name)
command(['lab','resume','interrupted','--output','recovered'])
s=json.loads((out/'scenario.json').read_text());s['outage']=True;(out/'invalid.json').write_text(json.dumps(s));command(['lab','run','invalid.json','--output','invalid-study'],2)
s.pop('outage');huge=dict(s,base_kva=10**400);(out/'huge.json').write_text(json.dumps(huge));command(['lab','validate','huge.json'],2);command(['lab','run','huge.json','--output','huge-study'],2);assert not (out/'huge-study').exists()
s['solver']['max_iterations']=1;(out/'nonconverge.json').write_text(json.dumps(s));failed=command(['lab','run','nonconverge.json','--output','failed']);assert set(failed['states'].values())=={'FAILED_SOLVER'}
(out/'reopened'/'baseline.json').write_text('{}');command(['lab','verify','reopened'],2)
s=json.loads((out/'scenario.json').read_text());s['policies']=[s['policies'][0]]
# Exercise >1 MiB campaign reading and invalid-case inventory while staying under 120 cases.
campaign={'schema':'grid-horizons.campaign/v1','scenarios':[s]*36+[{'outage':True},huge]}
(out/'campaign.json').write_text(json.dumps(campaign,indent=2));assert (out/'campaign.json').stat().st_size>1024*1024
command(['lab','campaign','campaign.json','--output','campaign'])
inv=json.loads((out/'campaign/inventory.json').read_text());assert len(inv)==38 and all(x['state']=='REJECTED_INPUT' for x in inv[-2:])
# Legacy v1 remains available in the very same packaged app.
command(['example','--output','legacy.json']);command(['run','legacy.json','--output','legacy']);command(['verify','legacy'])
result=dict(state='PASS',identity=id,checks=len(records),wall_seconds=time.perf_counter()-start,max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,package_sha256=hashlib.sha256(a.package.read_bytes()).hexdigest(),artifact_bytes=sum(p.stat().st_size for p in out.rglob('*') if p.is_file()),environment=dict(kind='fresh venv and directory, subprocesses on same Linux host; no container, separate machine, or external person',python=platform.python_version(),machine=platform.machine(),isolated_python=True,private_credentials=False))
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

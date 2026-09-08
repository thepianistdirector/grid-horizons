#!/usr/bin/env python3
"""Reproduce frozen policy experiment using packaged CLI only; no producer imports."""
import argparse, copy, csv, hashlib, json, platform, resource, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PACKAGE=ROOT/'releases/1.0.0rc1/grid-horizons.pyz'
EXPECTED='cdf8e0b82397cbad5e9f5979fd01d98fd931a7c772c5dcd1c8b42a35ac90a4a4'
PARAMS=[{'amplitude_kw':a,'charge_start':h,'charge_end':h+4,'discharge_start':17,'discharge_end':21,'tap':0} for a in [2,4,8,12] for h in [9,10]]
SOURCES=[{'title':'MATPOWER manual §4.3.2, Current Summation Method','url':'https://matpower.app/manual/matpower/DistributionPowerFlow.html','accessed':'2026-09-08','context':'Radial backward/forward current summation; no MATPOWER execution or validation claimed.'},{'title':'PyPSA documentation, Storage','url':'https://docs.pypsa.org/latest/user-guide/optimization/storage/','accessed':'2026-09-08','context':'Charging/discharging efficiency directions and cyclic terminal state; no PyPSA execution claimed.'}]
def write(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def command(out,label,*args):
 used=sum(json.loads(p.read_text())['cpu_seconds'] for p in (out/'commands').glob('*.json'))
 if used>=300:raise RuntimeError('Fixed 300-second CPU budget exhausted; preserve attempts')
 before=resource.getrusage(resource.RUSAGE_CHILDREN); t=time.perf_counter()
 p=subprocess.run([sys.executable,str(PACKAGE),'lab',*map(str,args)],capture_output=True,text=True,timeout=max(1,300-used))
 after=resource.getrusage(resource.RUSAGE_CHILDREN)
 record={'label':label,'argv':[sys.executable,str(PACKAGE),'lab',*map(str,args)],'returncode':p.returncode,'wall_seconds':time.perf_counter()-t,'cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'stdout':p.stdout,'stderr':p.stderr}
 write(out/'commands'/f'{label}.json',record)
 return p

def policy(pid,param):
 d=[param['amplitude_kw'] if param['charge_start']<=(i+.5)/4<param['charge_end'] else -param['amplitude_kw']*.95*.95 if 17<=(i+.5)/4<21 else 0. for i in range(96)]
 return {'id':pid,'dispatch_kw':d,'tap':[param['tap']]*96}
def scenario(base,scale,policies,name):
 s=copy.deepcopy(base);s['name']=name
 for key in ['load_kw','reactive_kvar']:
  s[key]=[[round(v*scale,7) for v in row] for row in s[key]]
 s['policies']=[{'id':'baseline','dispatch_kw':[0.]*96,'tap':[0]*96}]+[{'id':f'tap_{tap:+d}'.replace('+','p').replace('-','m'),'dispatch_kw':[0.]*96,'tap':[tap]*96} for tap in [-2,2,4]]+policies
 return s

def campaign(out,phase,scenarios):
 # Batches of two stay below the rc1 legacy 1 MiB JSON decoding cap.
 for batch in range(0,len(scenarios),2):
  spec=out/'inputs'/f'{phase}-{batch//2:02d}.json';write(spec,{'schema':'grid-horizons.campaign/v1','scenarios':scenarios[batch:batch+2]})
  assert spec.stat().st_size<1024*1024
  result=command(out,f'{phase}-campaign-{batch//2:02d}','campaign',spec,'--output',out/phase/f'batch-{batch//2:02d}')
  if result.returncode:raise RuntimeError(result.stdout)

def collect(out,phase):
 return [(p.parent,json.loads(p.read_text())) for p in sorted((out/phase).glob('batch-*/case-*/summary.json'))]
def select(out):
 groups={}
 for directory,summary in collect(out,'exploration'):
  name=summary['name'];scale=float(name.split('scale=')[1]);family=name.split('family=')[1].split()[0]
  if scale==1:continue
  baseline=next(x for x in summary['policies'] if x['policy']=='baseline')
  if baseline['state']!='COMPLETED_VALID':continue
  for p in summary['policies']:
   if p['policy'].startswith(family+'_'):groups.setdefault((family,p['policy']),[]).append(p)
 selected={};scores=[]
 for family in ['storage','combined']:
  eligible={pid:rows for (fam,pid),rows in groups.items() if fam==family and len(rows)==4 and all(x['state']=='COMPLETED_VALID' for x in rows)}
  if not eligible:raise RuntimeError('No eligible candidates')
  for metric,kind in [('total_loss_kwh','loss'),('peak_import_kw','peak')]:
   best=min(eligible,key=lambda pid:(sum(x['metrics'][metric] for x in eligible[pid])/4,pid))
   param=copy.deepcopy(PARAMS[int(best.rsplit('_',1)[1])]);param['tap']=4 if family=='combined' else 0
   selected[f'{family}_{kind}']={'source_policy':best,'parameters':param,'selection_metric':metric,'training_case_count':4,'mean_training_objective':sum(x['metrics'][metric] for x in eligible[best])/4}
  for (fam,pid),rows in groups.items():
   if fam==family:scores.append({'family':family,'policy':pid,'eligible':pid in eligible,'states':[x['state'] for x in rows],'mean_total_loss_kwh':sum(x['metrics']['total_loss_kwh'] for x in rows)/len(rows),'mean_peak_import_kw':sum(x['metrics']['peak_import_kw'] for x in rows)/len(rows)})
 write(out/'selection.json',{'selected':selected,'all_training_scores':scores});return selected

def inventory(out):
 attempts=[];rows=[]
 directories=[(out/'default',json.loads((out/'default/summary.json').read_text()))]+collect(out,'exploration')+collect(out,'confirmation')+[(p.parent,json.loads(p.read_text())) for p in sorted((out/'bridge').glob('*/summary.json'))]
 for d,s in directories:
  scenario_data=json.loads((d/'scenario.json').read_text()); base=next(p for p in s['policies'] if p['policy']=='baseline');eligible=base['state']=='COMPLETED_VALID'
  attempts.append({'directory':str(d.relative_to(out)),'name':s['name'],'baseline_state':base['state'],'ranking':s['ranking'],'policy_count':len(s['policies'])})
  for p in s['policies']:
   raw=json.loads((d/(p['policy']+'.json')).read_text())['raw']; energies=[scenario_data['storage']['initial_kwh']]+[x['energy_end_kwh'] for x in raw.get('rows',[])]
   pol=next(x for x in scenario_data['policies'] if x['id']==p['policy'])
   rows.append({'directory':str(d.relative_to(out)),'scenario':s['name'],'policy':p['policy'],'state':p['state'],'ranking_eligible':eligible and p['state']=='COMPLETED_VALID','violations':len(p['violations']),'invalid':len(p['invalid']),'violation_reasons':';'.join(sorted(set(x['reason'] for x in p['violations']))),'min_soc_kwh':min(energies),'max_soc_kwh':max(energies),'max_abs_dispatch_kw':max(map(abs,pol['dispatch_kw'])),**p['metrics']})
  label='verify-'+str(d.relative_to(out)).replace('/','-')
  if not (out/'commands'/(label+'.json')).exists(): command(out,label,'verify',d)
 write(out/'all-attempts.json',attempts)
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (out/'all-scenario-feasibility.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
 write(out/'all-results.json',rows)
 commands=[json.loads(p.read_text()) for p in (out/'commands').glob('*.json')]
 write(out/'resources.json',{'cli_cpu_seconds':sum(c['cpu_seconds'] for c in commands),'cli_wall_seconds':sum(c['wall_seconds'] for c in commands),'scenario_count':len(attempts),'policy_trajectories':len(rows),'intervals_per_scenario':96,'process_policy':'Sequential subprocess.run; one active solver process','disk_bytes_at_measurement':sum(p.stat().st_size for p in out.rglob('*') if p.is_file()),'command_count':len(commands),'failed_commands':[c['label'] for c in commands if c['returncode']]})

def main():
 global PACKAGE
 ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['explore','confirm','bridge','inventory']);ap.add_argument('--output',type=Path,default=Path(__file__).parent);a=ap.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'inputs').mkdir(exist_ok=True)
 if a.phase=='explore':
  if (out/'protocol.json').exists():raise RuntimeError('Choose a fresh output directory; existing evidence preserved')
  identity=json.loads(command(out,'identity','identity').stdout);assert identity['build']['implementation_sha256']==EXPECTED
  write(out/'identity.json',{'packaged_cli':identity,'package_sha256':sha(PACKAGE),'investigator_model':'gpt-6-astra','investigator_effort':'high','model_verification':'Actual session turn_context inspected before experiments; matches requested model.','runtime_executable':sys.executable,'platform':platform.platform(),'source_isolation':'Read-only workflow and package hashes; not OS-enforced isolation.'})
  protocol={'question':'Do terminal-neutral storage schedules improve total energy losses or peak import versus idle storage, and how does ideal discrete tap control change the tradeoff?','sources':SOURCES,'exploratory_seeds':[11,13],'confirmation_seeds':[41,43,47,53],'load_scales':[.7,.85,1.0],'solar_scale':1,'steps':96,'fixed_comparators':['idle storage + tap 0 baseline','idle storage + tap -2','idle storage + tap 2','idle storage + tap 4'],'search':{'storage':PARAMS,'combined':[{**p,'tap':4} for p in PARAMS],'budget':'8 candidates each family, every seed × load combination; 48 evaluations per family, no adaptive additions'},'selection':'Among candidates feasible on all four seed 11/13 × load .7/.85 training cases whose baselines are feasible, choose lowest arithmetic mean total_loss_kwh separately from lowest mean peak_import_kw; tie break lexical policy id. Load 1 excluded before ranking; report all failure outcomes. Freeze both winners per family before confirmation.','primary_objective':'total_loss_kwh = network_loss_kwh + storage_loss_kwh','secondary_objective':'peak_import_kw; independently selected, no combined scalar score','falsifiers':['Selected storage total-loss benefit is falsified within this panel if any comparable confirmation case has total_loss >= baseline.','Line-loss reduction does not establish total-loss reduction when conversion losses exceed line savings.','Any infeasible baseline excludes its entire scenario from ranking, even if another policy becomes feasible.','Any invalid energy or power residual, nonconvergence, terminal SOC error or limit violation invalidates a candidate benefit claim.'],'uncertainty':'Report min/max paired differences across four frozen seeds by load, no population inference or significance. Seeds alter hourly solar only; demand profile and feeder shared.','stopping_rule':'Exactly one default demonstration +12 exploration +12 confirmation =25 scenarios, 96 intervals; verify each. No tuning after confirmation. Stop if 300 CPU seconds exceeded; preserve all attempts.','scope':'Original synthetic balanced constant-PQ 13-bus feeder; no physical/public-feeder, lifecycle, universal optimum or field claims.'}
  write(out/'protocol.json',protocol)
  command(out,'example-default','example','--seed',17,'--steps',96,'--output',out/'inputs/default.json')
  command(out,'run-default','run',out/'inputs/default.json','--output',out/'default')
  scenarios=[]
  for seed in [11,13]:
   path=out/'inputs'/f'example-{seed}.json';command(out,f'example-{seed}','example','--seed',seed,'--steps',96,'--output',path);base=json.loads(path.read_text())
   for scale in [.7,.85,1.]:
    for family in ['storage','combined']:
     policies=[policy(f'{family}_{i}',{**param,'tap':4 if family=='combined' else 0}) for i,param in enumerate(PARAMS)]
     scenarios.append(scenario(base,scale,policies,f'exploration family={family} seed={seed} scale={scale}'))
  campaign(out,'exploration',scenarios);selected=select(out)
  prereg={**protocol,'frozen_selected':selected,'frozen_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'selection_sha256':sha(out/'selection.json'),'protocol_sha256':sha(out/'protocol.json')};write(out/'preregistration.json',prereg)
  (out/'preregistration.md').write_text('# Frozen confirmation preregistration\n\nWritten after the declared exploratory budget and before any confirmation run.\n\n```json\n'+json.dumps(prereg,indent=2)+'\n```\n')
 elif a.phase=='confirm':
  if (out/'confirmation-start.json').exists():raise RuntimeError('Confirmation already attempted; preserve evidence')
  prereg=json.loads((out/'preregistration.json').read_text());selected=prereg['frozen_selected'];scenarios=[]
  for seed in prereg['confirmation_seeds']:
   path=out/'inputs'/f'example-{seed}.json';command(out,f'example-{seed}','example','--seed',seed,'--steps',96,'--output',path);base=json.loads(path.read_text())
   for scale in prereg['load_scales']:
    scenarios.append(scenario(base,scale,[policy(name,v['parameters']) for name,v in selected.items()],f'confirmation seed={seed} scale={scale}'))
  write(out/'confirmation-start.json',{'preregistration_sha256':sha(out/'preregistration.json'),'started_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
  campaign(out,'confirmation',scenarios);inventory(out)
 elif a.phase=='bridge':
  if (out/'bridge-identity.json').exists():raise RuntimeError('Bridge already attempted; preserve evidence')
  original=PACKAGE;PACKAGE=ROOT/'releases/1.0.0rc2/grid-horizons.pyz'
  identity=json.loads(command(out,'bridge-identity','identity').stdout)
  assert identity['build']['implementation_sha256']=='3f46ec88b717c2811186fe2c4c7f2c926a37e110281c115798720bd87e143023'
  write(out/'bridge-identity.json',{'identity':identity,'package_sha256':sha(PACKAGE),'purpose':'Additional compatibility reproductions; excluded from policy selection and confirmation inference.'})
  results=[]
  for i,(d,_) in enumerate(collect(out,'exploration')+collect(out,'confirmation')[:1]):
   dest=out/'bridge'/f'case-{i:02d}'
   result=command(out,f'bridge-run-{i:02d}','run',d/'scenario.json','--output',dest)
   assert result.returncode==0,result.stdout
   result=command(out,'verify-'+str(dest.relative_to(out)).replace('/','-'),'verify',dest)
   assert result.returncode==0,result.stdout
   comparisons=[]
   for policy_row in json.loads((d/'scenario.json').read_text())['policies']:
    name=policy_row['id']+'.json';comparisons.append({'file':name,'raw_and_evaluation_byte_equal':(d/name).read_bytes()==(dest/name).read_bytes(),'sha256':sha(dest/name)})
   assert all(x['raw_and_evaluation_byte_equal'] for x in comparisons)
   results.append({'original':str(d.relative_to(out)),'bridge':str(dest.relative_to(out)),'verified':True,'comparisons':comparisons})
  write(out/'bridge-comparison.json',results);PACKAGE=original;inventory(out)
 else:inventory(out)
if __name__=='__main__':main()

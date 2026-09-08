#!/usr/bin/env python3
"""Bounded process-separated reproduction; actual package produces every trajectory."""
import argparse,collections,copy,csv,hashlib,json,math,os,pathlib,resource,runpy,subprocess,sys,time,zipfile
sys.dont_write_bytecode=True
HERE=pathlib.Path(__file__).resolve().parent
PROJECT=HERE.parent.parent
RESEARCH=HERE.parent

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True,allow_nan=False)+'\n')
def cpu():
 a,b=resource.getrusage(resource.RUSAGE_SELF),resource.getrusage(resource.RUSAGE_CHILDREN)
 return a.ru_utime+a.ru_stime+b.ru_utime+b.ru_stime

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path,default=HERE/('attempt-'+time.strftime('%Y%m%dT%H%M%S')));ap.add_argument('--candidate',default='1.0.0rc2');args=ap.parse_args()
 out=args.output.resolve();assert out.is_relative_to(HERE);out.mkdir(exist_ok=False);(out/'logs').mkdir()
 start=time.perf_counter();c0=cpu();cmds=[];checks=[];records=[];states={};packages={}
 for version in ('1.0.0rc1','1.0.0rc2',args.candidate):
  p=PROJECT/'releases'/version/'grid-horizons.pyz'
  with zipfile.ZipFile(p) as z:
   packages[version]={'path':str(p),'sha256':sha(p),'modules':{n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.endswith('.py')}}
 def check(name,passed,**data): checks.append(dict(name=name,passed=bool(passed),**data))
 def cli(version,*argv):
  assert cpu()-c0<290
  cmd=[sys.executable,'-I',packages[version]['path'],'lab',*map(str,argv)];t=time.perf_counter();c=cpu()
  q=subprocess.run(cmd,capture_output=True,timeout=50,env={'PATH':os.environ.get('PATH',''),'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
  i=len(cmds);(out/'logs'/f'{i:03d}.stdout').write_bytes(q.stdout);(out/'logs'/f'{i:03d}.stderr').write_bytes(q.stderr)
  cmds.append(dict(index=i,argv=cmd,returncode=q.returncode,cpu_seconds=cpu()-c,wall_seconds=time.perf_counter()-t));write(out/'commands.json',cmds)
  return q
 for n in ('grid_horizons/ac.py','grid_horizons/ac_check.py'):
  check('rc1_rc2_module_unchanged',packages['1.0.0rc1']['modules'][n]==packages['1.0.0rc2']['modules'][n],module=n)
 for study in ('benchmark','policies','robustness'):
  counts=collections.Counter();intervals=0;casecount=0
  for file in sorted((RESEARCH/study).rglob('summary.json')):
   directory=file.parent;s=read(directory/'scenario.json');summary=read(file);m=read(directory/'manifest.json');version=m['identity']['build']['version'];casecount+=1
   # Whole retained corpus: package reevaluation of raw evidence, no new producer run.
   q=cli(version,'verify',directory)
   legacy_size=(study=='policies' and 'exploration' in directory.parts and file.stat().st_size>1048576)
   check('retained_bundle_verify',q.returncode==(2 if legacy_size else 0),study=study,path=str(directory.relative_to(RESEARCH)),expected_rc1_size_defect=legacy_size,returncode=q.returncode)
   hashes=read(directory/'checksums.json');check('retained_hashes',all(sha(directory/k)==v for k,v in hashes.items()),path=str(directory.relative_to(RESEARCH)))
   base=next(x for x in summary['policies'] if x['policy']=='baseline')
   expected=sorted([x for x in summary['policies'] if x['state']=='COMPLETED_VALID'],key=lambda x:x['metrics']['total_loss_kwh']) if base['state']=='COMPLETED_VALID' else []
   check('feasibility_before_ranking',summary['ranking']==[x['policy'] for x in expected],path=str(directory.relative_to(RESEARCH)))
   for p in s['policies']:
    r=read(directory/(p['id']+'.json'));ev=r['evaluation'];counts[ev['state']]+=1;intervals+=len(r['raw']['rows'])
    item=dict(study=study,directory=str(directory.relative_to(RESEARCH)),policy=p['id'],state=ev['state'],metrics=ev['metrics'],ranking=summary['ranking']);records.append(item)
    if r['raw']['state']=='SOLVED':
     energy=s['storage']['initial_kwh'];st=s['storage'];maxerr=0.;conversion=0.
     for t,row in enumerate(r['raw']['rows']):
      d=p['dispatch_kw'][t];dt=s['dt_hours'][t];end=energy+dt*(max(d,0)*st['eta_charge']-max(-d,0)/st['eta_discharge'])
      maxerr=max(maxerr,abs(row['energy_start_kwh']-energy),abs(row['energy_end_kwh']-end));energy=end
      conversion+=dt*(max(d,0)*(1-st['eta_charge'])+max(-d,0)*(1/st['eta_discharge']-1))
     check('independent_storage_ledger',maxerr<=1e-6 and abs(conversion-ev['metrics']['storage_loss_kwh'])<=1e-6,path=str(directory.relative_to(RESEARCH)),policy=p['id'])
  states[study]=dict(bundles=casecount,states=dict(counts),solved_intervals=intervals)
 # Finite sample predetermined from original states/treatments; all inputs unchanged.
 b=RESEARCH/'benchmark/attempt-001';p=RESEARCH/'policies'
 robust=next(x.parent for x in (RESEARCH/'robustness/attempts').glob('*/run-101-00/summary.json')).parent
 appendix=next(x.parent for x in (RESEARCH/'robustness/appendix-attempts').glob('*/campaign/case-000/summary.json')).parent
 samples=[b/'campaign/case-000',b/'s17-n24-tol1e-12',b/'analytic-two-bus',b/'no-load',b/'failed-solver',p/'exploration/batch-00/case-000',p/'confirmation/batch-00/case-000',robust/'run-101-00',robust/'run-101-11',appendix/'case-001']
 refs=runpy.run_path(str(RESEARCH/'benchmark/rerun.py'));reference=refs['reference'];reference_checks=[]
 for i,original in enumerate(samples):
  s=read(original/'scenario.json');assert len(s['dt_hours'])<=480
  dest=out/f'rerun-{i:02d}';q=cli(args.candidate,'run',original/'scenario.json','--output',dest);check('sample_run',q.returncode==0,original=str(original))
  q=cli(args.candidate,'verify',dest);check('sample_verify',q.returncode==0,original=str(original))
  for policy in s['policies']:
   fn=policy['id']+'.json';check('exact_raw_and_evaluation',sha(original/fn)==sha(dest/fn),original=str(original.relative_to(RESEARCH)),policy=policy['id'])
   r=read(dest/fn)
   if i in (1,2,3,6,8) and r['raw']['state']=='SOLVED':
    # Reuses the reviewed independently authored Newton method; does not claim third-solver authorship.
    errors=[]
    for t,row in enumerate(r['raw']['rows']):
     ref=reference(s,policy,t);errors.append(dict(interval=t,voltage=max(abs(complex(*a)-complex(*b)) for a,b in zip(row['voltage'],ref['voltage'])),source=abs(complex(*row['source_kva'])-complex(*ref['source_kva'])),loss=abs(r['evaluation']['intervals'][t]['network_loss_kw']-ref['network_loss_kw'])))
    maxima={k:max(x[k] for x in errors) for k in ('voltage','source','loss')};reference_checks.append(dict(original=str(original.relative_to(RESEARCH)),policy=policy['id'],intervals=len(errors),maxima=maxima));check('newton_comparison',maxima['voltage']<1e-8 and maxima['source']<1e-6 and maxima['loss']<1e-6,**reference_checks[-1])
 # Invalid topology: no output directory should be created.
 s=read(samples[1]/'scenario.json');s['branches'][0]['parent']=-1;write(out/'invalid-outage.json',s)
 q=cli(args.candidate,'run',out/'invalid-outage.json','--output',out/'invalid-outage');check('unsupported_outage_rejected',q.returncode==2 and not (out/'invalid-outage').exists())
 # Validator/persistence namespace edge. RC2 expected known defect; fixed candidate must reject all.
 for reserved in ('summary','scenario','manifest','checksums'):
  s=read(samples[1]/'scenario.json');policy=copy.deepcopy(s['policies'][0]);policy['id']=reserved;s['policies'].append(policy);write(out/f'reserved-{reserved}.json',s)
  q=cli(args.candidate,'validate',out/f'reserved-{reserved}.json');check('reserved_policy_rejected',q.returncode==2,policy=reserved,candidate=args.candidate)
 # Snapshot study findings and compare aggregate counts, including bridge/repeat evidence.
 for study in ('benchmark','policies'):
  rows=list(csv.DictReader((RESEARCH/study/'all-scenario-feasibility.csv').open()));got=collections.Counter(x['state'] for x in rows)
  check('complete_csv_counts',dict(got)==states[study]['states'],study=study,csv_rows=len(rows),raw_states=states[study]['states'])
 inventory={str(f.relative_to(PROJECT)):dict(sha256=sha(f),bytes=f.stat().st_size) for folder in ('benchmark','policies','robustness') for f in (RESEARCH/folder).rglob('*') if f.is_file()}
 write(out/'source-evidence-inventory.json',inventory);write(out/'package-hashes.json',packages);write(out/'all-records.json',records);write(out/'newton-checks.json',reference_checks);write(out/'checks.json',checks)
 result=dict(candidate=args.candidate,scenario_runs=len(samples)+1,scenario_interval_limit=480,solver_processes_parallel=1,cpu_seconds=cpu()-c0,wall_seconds=time.perf_counter()-start,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,states=states,checks=len(checks),failed_checks=[x for x in checks if not x['passed']],cost_scope='Self and sequential child CPU for review script; excludes authoring/model inference and earlier manual namespace repro.',inventory_file_bytes=sum(v['bytes'] for v in inventory.values()))
 write(out/'result.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()

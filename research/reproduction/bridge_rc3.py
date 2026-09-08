#!/usr/bin/env python3
"""Additive three-study RC3 verification, no changes to existing evidence."""
import ast,collections,copy,hashlib,json,os,pathlib,resource,subprocess,sys,time,zipfile
H=pathlib.Path(__file__).resolve().parent;P=H.parent.parent;R=H.parent
out=H/('bridge-rc3-'+time.strftime('%Y%m%dT%H%M%S'));out.mkdir();(out/'logs').mkdir();checks=[];commands=[];start=time.perf_counter()
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cpu():
 a,b=resource.getrusage(resource.RUSAGE_SELF),resource.getrusage(resource.RUSAGE_CHILDREN);return a.ru_utime+a.ru_stime+b.ru_utime+b.ru_stime
c0=cpu()
def ck(name,ok,**kw):checks.append(dict(name=name,passed=bool(ok),**kw))
def cli(*args):
 cmd=[sys.executable,'-I',str(P/'releases/1.0.0rc3/grid-horizons.pyz'),'lab',*map(str,args)];c=cpu();t=time.perf_counter();q=subprocess.run(cmd,capture_output=True,timeout=45,env={'PATH':os.environ.get('PATH',''),'PYTHONDONTWRITEBYTECODE':'1'});i=len(commands);(out/'logs'/f'{i:02d}.stdout').write_bytes(q.stdout);(out/'logs'/f'{i:02d}.stderr').write_bytes(q.stderr);commands.append(dict(argv=cmd,returncode=q.returncode,cpu_seconds=cpu()-c,wall_seconds=time.perf_counter()-t));return q
packages={}
for version in ('1.0.0rc2','1.0.0rc3'):
 p=P/'releases'/version/'grid-horizons.pyz'
 with zipfile.ZipFile(p) as z:packages[version]=dict(sha256=sha(p),ac=z.read('grid_horizons/ac.py').decode(),ac_check_sha256=hashlib.sha256(z.read('grid_horizons/ac_check.py')).hexdigest())
ck('evaluator_unchanged',packages['1.0.0rc2']['ac_check_sha256']==packages['1.0.0rc3']['ac_check_sha256'])
for function in ('example','solve','produce'):
 trees=[ast.parse(packages[v]['ac']) for v in packages];nodes=[next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name==function) for t in trees];ck('producer_function_unchanged',ast.dump(nodes[0])==ast.dump(nodes[1]),function=function)
for v in packages:packages[v]['ac_sha256']=hashlib.sha256(packages[v].pop('ac').encode()).hexdigest()
base=R/'benchmark/attempt-001/s17-n24-tol1e-12'
for name in ('scenario','manifest','summary','checksums'):
 s=read(base/'scenario.json');p=copy.deepcopy(s['policies'][0]);p['id']=name;s['policies'].append(p);input=out/(name+'.json');input.write_text(json.dumps(s));q=cli('validate',input);ck('reserved_name_rejected',q.returncode==2,policy=name)
 # run invalid input also must reject without directory creation.
 dest=out/('invalid-'+name);q=cli('run',input,'--output',dest);ck('reject_before_output_creation',q.returncode==2 and not dest.exists(),policy=name)
robust=next(x.parent for x in (R/'robustness/attempts').glob('*/run-101-11/summary.json'))
originals=[base,R/'policies/exploration/batch-00/case-000',robust]
for i,source in enumerate(originals):
 dest=out/f'study-{i}';q=cli('run',source/'scenario.json','--output',dest);ck('bridge_run',q.returncode==0,source=str(source.relative_to(R)));q=cli('verify',dest);ck('bridge_verify',q.returncode==0)
 for p in read(source/'scenario.json')['policies']:ck('exact_policy_file',sha(source/(p['id']+'.json'))==sha(dest/(p['id']+'.json')),policy=p['id'],source=str(source.relative_to(R)))
 if i==1:ck('large_generated_summary_verifies',(dest/'summary.json').stat().st_size>1048576 and q.returncode==0,bytes=(dest/'summary.json').stat().st_size)
result=dict(checks=checks,failed=[x for x in checks if not x['passed']],packages=packages,commands=commands,producer_scenarios=3,rejected_runs=4,cpu_seconds=cpu()-c0,wall_seconds=time.perf_counter()-start,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('commands','checks','packages')},indent=2))

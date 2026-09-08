#!/usr/bin/env python3
"""RC4 validate-only correction check; zero producer scenarios."""
import ast,hashlib,json,os,pathlib,resource,subprocess,sys,time,zipfile
H=pathlib.Path(__file__).resolve().parent;P=H.parent.parent
out=H/('check-rc4-'+time.strftime('%Y%m%dT%H%M%S'));out.mkdir();checks=[];commands=[];start=time.perf_counter()
def cpu():
 a,b=resource.getrusage(resource.RUSAGE_SELF),resource.getrusage(resource.RUSAGE_CHILDREN);return a.ru_utime+a.ru_stime+b.ru_utime+b.ru_stime
c0=cpu()
def ck(n,ok,**kw):checks.append(dict(name=n,passed=bool(ok),**kw))
def cli(*args):
 cmd=[sys.executable,'-I',str(P/'releases/1.0.0rc4/grid-horizons.pyz'),'lab',*map(str,args)];q=subprocess.run(cmd,capture_output=True,timeout=20,env={'PATH':os.environ.get('PATH','')});i=len(commands);(out/f'{i:02d}.stdout').write_bytes(q.stdout);(out/f'{i:02d}.stderr').write_bytes(q.stderr);commands.append(dict(argv=cmd,returncode=q.returncode));return q
identity=cli('identity');identity=json.loads(identity.stdout);ck('expected_implementation',identity['build']['implementation_sha256']=='b2eeb117a34ea3423136a0082442d1b93f01b0c6e13dab429772a0d2c3a8f8e3')
packages={};sources={}
for version in ('1.0.0rc3','1.0.0rc4'):
 path=P/'releases'/version/'grid-horizons.pyz'
 with zipfile.ZipFile(path) as z:
  sources[version]=z.read('grid_horizons/ac.py').decode();packages[version]=dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),ac_sha256=hashlib.sha256(sources[version].encode()).hexdigest(),ac_check_sha256=hashlib.sha256(z.read('grid_horizons/ac_check.py')).hexdigest())
ck('evaluator_bytes_unchanged',packages['1.0.0rc3']['ac_check_sha256']==packages['1.0.0rc4']['ac_check_sha256'])
for fn in ('example','solve','produce'):
 nodes=[next(x for x in ast.parse(s).body if isinstance(x,ast.FunctionDef) and x.name==fn) for s in sources.values()];ck('producer_function_unchanged',ast.dump(nodes[0])==ast.dump(nodes[1]),function=fn)
# Inspect validation diff independently as well as exercising the malformed input.
import difflib
(out/'ac-validation.diff').write_text(''.join(difflib.unified_diff(sources['1.0.0rc3'].splitlines(True),sources['1.0.0rc4'].splitlines(True))))
q=cli('validate',H/'invalid-huge-integer.json');result=json.loads(q.stdout);ck('huge_integer_structured_rejection',q.returncode==2 and result['state']=='REJECTED' and not q.stderr,actual=result)
for reserved in ('scenario','manifest','summary','checksums'):
 input=next(H.glob('bridge-rc3-*'))/(reserved+'.json');q=cli('validate',input);ck('reserved_name_still_rejected',q.returncode==2 and json.loads(q.stdout)['state']=='REJECTED',policy=reserved)
for source in (P/'research/benchmark/attempt-001/s17-n24-tol1e-12/scenario.json',P/'research/policies/exploration/batch-00/case-000/scenario.json',next(H.glob('bridge-rc3-*'))/'custom-control.json'):
 q=cli('validate',source);ck('ordinary_input_still_validates',q.returncode==0 and json.loads(q.stdout)['state']=='VALIDATED_INPUT',source=str(source))
result=dict(checks=checks,failed=[x for x in checks if not x['passed']],commands=commands,packages=packages,identity=identity,producer_scenarios=0,cpu_seconds=cpu()-c0,wall_seconds=time.perf_counter()-start,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('checks','commands','packages','identity')},indent=2))

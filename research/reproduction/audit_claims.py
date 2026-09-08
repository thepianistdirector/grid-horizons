#!/usr/bin/env python3
"""Independent retained-table/selection audit; no simulations."""
import collections,hashlib,json,pathlib,resource,time
R=pathlib.Path(__file__).resolve().parent.parent;O=R/'reproduction';checks=[];start=time.perf_counter();c0=time.process_time()
def read(p):return json.loads(p.read_text())
def ck(name,ok,**data):checks.append(dict(name=name,passed=bool(ok),**data))
def equal(a,b):return abs(a-b)<1e-12
# Benchmark every recorded table row and reference discrepancy versus raw data.
b=R/'benchmark';results=read(b/'attempt-001/results.json');tight={k:0. for k in ('voltage_abs_pu','source_abs_kva','loss_abs_kw')}
for row in results:
 path=b/'attempt-001'/row['study'];raw=read(path/(row['policy']+'.json'));ev=raw['evaluation'];ck('benchmark_row',ev['metrics']==row['metrics'] and ev['state']==row['state'],case=row['id'],policy=row['policy'])
 ref=b/'attempt-001/reference'/(row['id']+'-'+row['policy']+'.json')
 if ref.exists():
  d=read(ref);errors=[]
  for t,(actual,reference) in enumerate(zip(raw['raw']['rows'],d['reference'])):
   errors.append(dict(interval=t,voltage_abs_pu=max(abs(complex(*a)-complex(*z)) for a,z in zip(actual['voltage'],reference['voltage'])),source_abs_kva=abs(complex(*actual['source_kva'])-complex(*reference['source_kva'])),loss_abs_kw=abs(ev['intervals'][t]['network_loss_kw']-reference['network_loss_kw'])))
  ck('benchmark_retained_newton_comparison',errors==d['discrepancies'] and len(errors)==len(raw['raw']['rows']),case=row['id'],policy=row['policy'])
  if row['group']=='core' and row['tolerance']<=1e-10:
   for k in tight:tight[k]=max(tight[k],max(x[k] for x in errors))
f=read(b/'findings.json');ck('benchmark_claim_maxima',tight==f['tight_tolerance_comparison_maxima']);ck('benchmark_primary_states',dict(collections.Counter(x['state'] for x in results))==f['original_states'])
ck('benchmark_preregistration_hash',hashlib.sha256((b/'preregistration.json').read_bytes()).hexdigest()==f['preregistration_sha256'])
# Policy all rows including bridges, confirm paired ranges, equal-budget training winners.
p=R/'policies';rows=read(p/'all-results.json');summaries={}
for row in rows:
 path=p/row['directory'];r=read(path/(row['policy']+'.json'));ev=r['evaluation'];ck('policy_all_rows',row['state']==ev['state'] and all(row[k]==v for k,v in ev['metrics'].items()),directory=row['directory'],policy=row['policy'])
 summaries[row['directory']]=read(path/'summary.json')
selection=read(p/'selection.json');protocol=read(p/'protocol.json');pre=read(p/'preregistration.json');freeze=read(p/'confirmation-start.json')
ck('policy_preregistration_hash',hashlib.sha256((p/'preregistration.json').read_bytes()).hexdigest()==freeze['preregistration_sha256'])
ck('policy_selection_hash',hashlib.sha256((p/'selection.json').read_bytes()).hexdigest()==pre['selection_sha256'])
ck('protocol_frozen_hash',hashlib.sha256((p/'protocol.json').read_bytes()).hexdigest()==pre['protocol_sha256'])
ck('frozen_before_confirmation',pre['frozen_at_utc']<freeze['started_at_utc'])
training=[(d,s) for d,s in summaries.items() if d.startswith('exploration/')];counts=collections.Counter();scores={}
for d,s in training:
 case=read(p/d/'scenario.json');baseline=next(x for x in s['policies'] if x['policy']=='baseline')
 ck('training_seed_disjoint',case['provenance']['seed'] in protocol['exploratory_seeds'] and case['provenance']['seed'] not in protocol['confirmation_seeds'])
 for x in s['policies']:
  if x['policy'].startswith(('storage_','combined_')):
   counts[x['policy'].split('_')[0]]+=1
   if baseline['state']=='COMPLETED_VALID':scores.setdefault(x['policy'],[]).append(x)
ck('equal_exploration_budget',dict(counts)=={'storage':48,'combined':48},counts=dict(counts))
for alias,selection_row in selection['selected'].items():
 family=alias.split('_')[0];metric=selection_row['selection_metric'];valid={k:v for k,v in scores.items() if k.startswith(family+'_') and len(v)==4 and all(x['state']=='COMPLETED_VALID' for x in v)}
 scored={k:sum(x['metrics'][metric] for x in v)/len(v) for k,v in valid.items()};winner=min(scored,key=lambda k:(scored[k],k));ck('independent_selection',winner==selection_row['source_policy'] and equal(scored[winner],selection_row['mean_training_objective']),alias=alias,winner=winner)
confirm={d:s for d,s in summaries.items() if d.startswith('confirmation/')};f=read(p/'findings.json');pairwise=[]
for claim in f['paired_confirmation']:
 deltas={k:[] for k in ('network_loss_kwh','total_loss_kwh','peak_import_kw')}
 for d,s in confirm.items():
  scenario=read(p/d/'scenario.json');base=next(x for x in s['policies'] if x['policy']=='baseline');policy=next(x for x in s['policies'] if x['policy']==claim['policy'])
  # Infer declared scale from preserved input name.
  name=scenario['name']
  if str(claim['load_scale']) not in name:continue
  for k in deltas:deltas[k].append(policy['metrics'][k]-base['metrics'][k])
 ck('confirmation_paired_range',all(len(v)==4 and [min(v),max(v)]==claim[k+'_delta_range'] for k,v in deltas.items()),policy=claim['policy'],load=claim['load_scale'])
# Robustness: original and appendix row-to-raw and all aggregate reported ranges.
r=R/'robustness';f=read(r/'findings.json')
for group,pathkey in [('main','main_path'),('appendix','appendix_path')]:
 data=f[group];base=r/f[pathkey]
 if base.is_file():base=base.parent
 for row in data['rows']:
  case_name=row['study'] if group=='main' else 'campaign/case-%03d'%([101,103,107,109].index(row['seed'])*3+['nominal','load_late','joint_adverse'].index(row['treatment']));path=base/case_name;raw=read(path/(row['policy']+'.json'));ck('robustness_row',row['metrics']==raw['evaluation']['metrics'] and row['state']==raw['evaluation']['state'],group=group,study=case_name,policy=row['policy'])
 for policy,a in data['aggregate'].items():
  rr=[x for x in data['rows'] if x['policy']==policy];ck('robustness_states',dict(collections.Counter(x['state'] for x in rr))==a['states'],group=group,policy=policy)
  if group=='main':
   eligible=[x for x in rr if x['state']==x['baseline_state']=='COMPLETED_VALID'];ck('robustness_eligible',len(eligible)==a['eligible_count'],policy=policy)
   for key,subset in [('all_scenario_ranges',rr),('eligible_ranges',eligible)]:
    ck('robustness_all_ranges',all([min(x[k] for x in subset),max(x[k] for x in subset)]==v for k,v in a[key].items()),policy=policy,group=key)
  else:
   ck('appendix_loss_range',[min(x['loss_saving_kwh'] for x in rr),max(x['loss_saving_kwh'] for x in rr)]==a['all_scenario_loss_saving_kwh'],policy=policy)
   ck('appendix_peak_range',[min(x['peak_saving_kw'] for x in rr),max(x['peak_saving_kw'] for x in rr)]==a['all_scenario_peak_saving_kw'],policy=policy)
result=dict(checks=checks,failed=[x for x in checks if not x['passed']],cpu_seconds=time.process_time()-c0,wall_seconds=time.perf_counter()-start)
(O/'claim-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))

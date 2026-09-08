import copy
import json
import math
import tempfile
import unittest
from pathlib import Path
from grid_horizons import ac
from grid_horizons.ac_check import evaluate
from grid_horizons.lab import run, verify, export, import_study

class ACLabTests(unittest.TestCase):
 def test_analytic_resistive(self):
  s=ac.example(steps=24);s['branches']=[dict(parent=0,child=1,r_pu=.1,x_pu=0,current_limit_pu=1)]
  v=(1+math.sqrt(.96))/2
  r=ac.solve(s,[0,10],[0,0],1)
  self.assertAlmostEqual(r['voltage'][1][0],v,places=10)
  self.assertAlmostEqual(r['source_kva'][0]-10,.1*(.1/v)**2*100,places=8)
 def test_zero(self):
  s=ac.example(steps=24);r=ac.solve(s,[0]*13,[0]*13,1.0125)
  self.assertEqual(r['voltage'],[[1.0125,0]]*13)
 def test_mutations(self):
  s=ac.example(steps=24,load_scale=.8);p=s['policies'][0];raw=ac.produce(s,p)
  self.assertEqual(evaluate(s,p,raw)['state'],'COMPLETED_VALID')
  for field,value in [('source_kva',[900,0]),('energy_end_kwh',41),('dispatch_kw',1),('voltage',[[1,0]]*13)]:
   r=copy.deepcopy(raw);r['rows'][0][field]=value
   self.assertEqual(evaluate(s,p,r)['state'],'INVALID_RESULT',field)
  r=copy.deepcopy(raw);r['rows'].pop();self.assertEqual(evaluate(s,p,r)['state'],'INVALID_RESULT')
 def test_infeasible_no_clipping(self):
  s=ac.example(steps=24);s['storage']['capacity_kwh']=41
  r=ac.produce(s,s['policies'][1]);ev=evaluate(s,s['policies'][1],r)
  self.assertEqual(ev['state'],'COMPLETED_INFEASIBLE')
  self.assertGreater(max(x['energy_end_kwh'] for x in r['rows']),41)
 def test_nonconvergence_and_cancel(self):
  s=ac.example(steps=24);s['solver']['max_iterations']=1
  self.assertEqual(ac.produce(s,s['policies'][0])['state'],'FAILED_SOLVER')
  self.assertEqual(ac.produce(ac.example(steps=24),s['policies'][0],0)['state'],'CANCELLED')
 def test_input_rejections(self):
  for mutate in [lambda s:s.update(outage=True),lambda s:s['branches'][0].update(parent=2),lambda s:s['storage'].update(eta_charge=True),lambda s:s['dt_hours'].pop(),lambda s:s['load_kw'][0].__setitem__(1,float('nan')),lambda s:s.update(base_kva=10**400)]:
   s=ac.example(steps=24);mutate(s)
   with self.assertRaises(ValueError):ac.validate(s)
 def test_reserved_policy_names_rejected_before_writing(self):
  for name in ('scenario','manifest','summary','checksums'):
   s=ac.example(steps=24);s['policies'][1]['id']=name
   with tempfile.TemporaryDirectory() as d:
    out=Path(d)/'study'
    with self.assertRaisesRegex(ValueError,'reserved'):run(s,out)
    self.assertFalse(out.exists())
  s=ac.example(steps=24);s['policies'][1]['id']='custom_schedule'
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'study';run(s,out);verify(out)
 def test_round_trip_and_integrity(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);s=ac.example(steps=24);run(s,d/'a');verify(d/'a');export(d/'a',d/'a.zip');import_study(d/'a.zip',d/'b')
   self.assertEqual((d/'a'/'baseline.json').read_bytes(),(d/'b'/'baseline.json').read_bytes())
   (d/'b'/'baseline.json').write_text('{}')
   with self.assertRaises(ValueError):verify(d/'b')

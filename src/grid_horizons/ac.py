"""Original bounded balanced AC laboratory. SPDX-License-Identifier: AGPL-3.0-only."""
from __future__ import annotations
import copy
import math
import random

SCHEMA = 'grid-horizons.ac-scenario/v2'
MODEL = 'balanced-radial-pq/v2'


def example(seed=17, steps=96, load_scale=1., solar_scale=1.):
    rng = random.Random(seed)
    parents = [0, 1, 2, 3, 2, 5, 6, 1, 8, 9, 8, 11]
    branches = [dict(parent=p, child=i+1, r_pu=round(.006+.0015*(i%4),6),
                     x_pu=.004, current_limit_pu=.9 if i==0 else .55)
                for i,p in enumerate(parents)]
    load=[]; solar=[]; q=[]
    weights=[0]+[.65+.07*(i%5) for i in range(1,13)]
    cloud=[.8+.2*rng.random() for _ in range(24)]
    for t in range(steps):
        h=(t+.5)*24/steps
        shape=.55+.25*math.exp(-((h-8)/2)**2)+.65*math.exp(-((h-19)/2.5)**2)
        sun=max(0.,math.sin(math.pi*(h-6)/12)) if 6<h<18 else 0.
        load.append([round(load_scale*8*w*shape,7) for w in weights])
        q.append([round(.25*x,7) for x in load[-1]])
        solar.append([round(solar_scale*24*sun*cloud[int(h)],7) if n in (4,7,10,12) else 0. for n in range(13)])
    dt=24/steps
    schedule=[8. if 10<=((t+.5)*dt)<14 else -8*.95*.95 if 17<=((t+.5)*dt)<21 else 0. for t in range(steps)]
    return dict(schema=SCHEMA, model=MODEL, name=f'Synthetic Canopy 13 / seed {seed}',
                provenance=dict(kind='ORIGINAL_SYNTHETIC',license='AGPL-3.0-only',generator='canopy13/v1',seed=seed),
                base_kva=100.,base_kv=12.47,dt_hours=[dt]*steps,branches=branches,
                load_kw=load,reactive_kvar=q,solar_kw=solar,
                voltage_limits_pu=[.95,1.05],solver=dict(tolerance=1e-10,max_iterations=100),
                storage=dict(node=7,capacity_kwh=80.,initial_kwh=40.,power_kw=20.,eta_charge=.95,eta_discharge=.95),
                policies=[dict(id='baseline',dispatch_kw=[0.]*steps,tap=[0]*steps),
                          dict(id='storage',dispatch_kw=schedule,tap=[0]*steps),
                          dict(id='tap',dispatch_kw=[0.]*steps,tap=[2]*steps),
                          dict(id='combined',dispatch_kw=schedule,tap=[2]*steps)])


def validate(s):
    def require(ok,message):
        if not ok: raise ValueError(message)
    def fields(obj, expected,where):
        require(isinstance(obj,dict) and set(obj)==set(expected.split()),f'{where}: unsupported or missing fields')
    def number(x,lo,hi): return type(x) in (int,float) and lo<=x<=hi and math.isfinite(x)
    fields(s,'schema model name provenance base_kva base_kv dt_hours branches load_kw reactive_kvar solar_kw voltage_limits_pu solver storage policies','scenario')
    require(s['schema']==SCHEMA and s['model']==MODEL,'unsupported schema/model; use original build for older studies')
    require(isinstance(s['name'],str) and 0<len(s['name'])<=160,'name: 1..160 characters')
    fields(s['provenance'],'kind license generator seed','provenance')
    require(s['provenance']['kind']=='ORIGINAL_SYNTHETIC' and s['provenance']['license']=='AGPL-3.0-only','only original synthetic AGPL data admitted')
    require(isinstance(s['provenance']['generator'],str) and len(s['provenance']['generator'])<=100,'generator string')
    require(type(s['provenance']['seed']) is int,'seed must be integer')
    require(number(s['base_kva'],1,100000) and number(s['base_kv'],.1,100),'base out of domain')
    dt=s['dt_hours']; require(isinstance(dt,list) and 1<=len(dt)<=480,'1..480 intervals')
    require(all(number(x,1/3600,24) for x in dt) and abs(sum(dt)-24)<1e-8,'positive intervals must sum to 24 hours')
    b=s['branches'];require(isinstance(b,list) and 1<=len(b)<=32,'2..33 buses')
    for i,x in enumerate(b):
        fields(x,'parent child r_pu x_pu current_limit_pu','branch')
        require(type(x['child']) is int and x['child']==i+1 and type(x['parent']) is int and 0<=x['parent']<i+1,'ordered connected radial topology required; outages unsupported')
        require(number(x['r_pu'],1e-6,.2) and number(x['x_pu'],0,.2) and number(x['current_limit_pu'],.001,100),'branch outside domain')
    n=len(b)+1
    for k in ('load_kw','reactive_kvar','solar_kw'):
        require(isinstance(s[k],list) and len(s[k])==len(dt),'profile length mismatch')
        require(all(isinstance(row,list) and len(row)==n and row[0]==0 and all(number(x,0,10000) for x in row) for row in s[k]),'profile dimensions, signs or units invalid; root must be zero')
    v=s['voltage_limits_pu'];require(isinstance(v,list) and len(v)==2 and all(number(x,.8,1.2) for x in v) and v[0]<v[1],'voltage limits invalid')
    fields(s['solver'],'tolerance max_iterations','solver')
    require(number(s['solver']['tolerance'],1e-13,1e-3) and type(s['solver']['max_iterations']) is int and 1<=s['solver']['max_iterations']<=100,'solver budget invalid')
    st=s['storage'];fields(st,'node capacity_kwh initial_kwh power_kw eta_charge eta_discharge','storage')
    require(type(st['node']) is int and 1<=st['node']<n,'storage node invalid')
    require(number(st['capacity_kwh'],.001,10000) and number(st['initial_kwh'],0,st['capacity_kwh']) and number(st['power_kw'],0,10000),'storage bounds invalid')
    require(number(st['eta_charge'],.5,1) and number(st['eta_discharge'],.5,1),'efficiency out of domain')
    policies=s['policies'];require(isinstance(policies,list) and 1<=len(policies)<=16,'1..16 policies')
    ids=[]
    for p in policies:
        fields(p,'id dispatch_kw tap','policy')
        require(isinstance(p['id'],str) and 0<len(p['id'])<=40 and all(c.isalnum() or c in '-_' for c in p['id']),'policy id invalid')
        require(p['id'] not in {'scenario','manifest','summary','checksums'},'policy id is reserved for study metadata')
        ids.append(p['id'])
        require(isinstance(p['dispatch_kw'],list) and len(p['dispatch_kw'])==len(dt) and all(number(x,-10000,10000) for x in p['dispatch_kw']),'dispatch invalid')
        require(isinstance(p['tap'],list) and len(p['tap'])==len(dt) and all(type(x) is int and -4<=x<=4 for x in p['tap']),'tap must be discrete -4..4')
    require(len(ids)==len(set(ids)) and 'baseline' in ids,'unique policies including baseline required')
    p=policies[ids.index('baseline')];require(all(x==0 for x in p['dispatch_kw']) and all(x==0 for x in p['tap']),'baseline is fixed idle, zero tap')
    return s


def solve(s, net, reactive, slack):
    """Complex-current backward/forward sweep; no evaluator call or feasibility repair."""
    n=len(net);v=[complex(slack)]*n
    def currents(volts):
        a=[complex(net[i],reactive[i]).conjugate()/volts[i].conjugate()/s['base_kva'] for i in range(n)]
        for b in reversed(s['branches']): a[b['parent']]+=a[b['child']]
        return a
    for iteration in range(1,s['solver']['max_iterations']+1):
        if any(abs(x)<.2 or not math.isfinite(abs(x)) for x in v): raise ArithmeticError('voltage iteration left numerical domain')
        a=currents(v);new=[complex(slack)]*n
        for b in s['branches']: new[b['child']]=new[b['parent']]-complex(b['r_pu'],b['x_pu'])*a[b['child']]
        delta=max(abs(x-y) for x,y in zip(v,new));v=new
        if delta<=s['solver']['tolerance']:
            a=currents(v)
            return dict(voltage=[[x.real,x.imag] for x in v],source_kva=[(v[0]*a[0].conjugate()*s['base_kva']).real,(v[0]*a[0].conjugate()*s['base_kva']).imag],iterations=iteration,update_pu=delta)
    raise ArithmeticError('iteration budget exhausted')


def produce(s,p,stop_after=None):
    energy=s['storage']['initial_kwh'];rows=[]
    for t,dt in enumerate(s['dt_hours']):
        if stop_after is not None and t>=stop_after: return dict(state='CANCELLED',rows=rows,error='requested interval-boundary cancellation')
        dispatch=p['dispatch_kw'][t];st=s['storage']
        end=energy+(max(dispatch,0)*st['eta_charge']+min(dispatch,0)/st['eta_discharge'])*dt
        net=[x-y for x,y in zip(s['load_kw'][t],s['solar_kw'][t])];net[st['node']]+=dispatch
        try: row=solve(s,net,s['reactive_kvar'][t],1+.00625*p['tap'][t])
        except ArithmeticError as exc: return dict(state='FAILED_SOLVER',rows=rows,error=str(exc),failed_interval=t)
        row.update(interval=t,energy_start_kwh=energy,energy_end_kwh=end,dispatch_kw=dispatch,tap=p['tap'][t])
        rows.append(row);energy=end
    return dict(state='SOLVED',rows=rows)

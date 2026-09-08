"""Independent Ohm/incidence evaluator. No producer imports. AGPL-3.0-only."""
import math


def evaluate(s,p,raw):
    invalid=[];violations=[];details=[]
    totals=dict(import_kwh=0.,export_kwh=0.,load_kwh=0.,solar_kwh=0.,network_loss_kwh=0.,storage_loss_kwh=0.)
    max_residual=0.;peak=0.;min_v=2.;max_v=0.;max_loading=0.;energy=s['storage']['initial_kwh']
    try:
        if raw['state']!='SOLVED' or len(raw['rows'])!=len(s['dt_hours']): raise ValueError('incomplete solved trajectory')
        for t,(row,dt) in enumerate(zip(raw['rows'],s['dt_hours'])):
            def fail(reason): invalid.append(dict(interval=t,reason=reason))
            def limit(reason,value): violations.append(dict(interval=t,reason=reason,value=value))
            st=s['storage'];d=p['dispatch_kw'][t];charge=max(d,0);discharge=max(-d,0)
            if set(row)!=set('voltage source_kva iterations update_pu interval energy_start_kwh energy_end_kwh dispatch_kw tap'.split()): raise ValueError('raw fields mismatch')
            if row['interval']!=t or row['dispatch_kw']!=d or row['tap']!=p['tap'][t]: fail('declared policy/interval mismatch')
            if type(row['iterations']) is not int or not 1<=row['iterations']<=s['solver']['max_iterations']: fail('iteration count')
            if not 0<=row['update_pu']<=s['solver']['tolerance']: fail('reported convergence tolerance')
            def finite(x):
                if type(x) not in (int,float) or not math.isfinite(x): raise ValueError('nonfinite or nonnumeric raw value')
                return x
            for key in ('energy_start_kwh','energy_end_kwh','dispatch_kw','update_pu'): finite(row[key])
            if len(row['voltage'])!=len(s['branches'])+1 or any(len(x)!=2 for x in row['voltage']) or len(row['source_kva'])!=2: raise ValueError('voltage/source dimensions')
            v=[complex(finite(x[0]),finite(x[1])) for x in row['voltage']]
            source=complex(*[finite(x) for x in row['source_kva']])
            if abs(v[0]-complex(1+.00625*p['tap'][t]))>1e-10: fail('slack voltage')
            currents=[0j]*len(v);loss=0.;loading=[]
            for b in s['branches']:
                i,j=b['parent'],b['child'];current=(v[i]-v[j])/complex(b['r_pu'],b['x_pu'])
                currents[i]+=current;currents[j]-=current
                loss+=b['r_pu']*abs(current)**2*s['base_kva']
                ratio=abs(current)/b['current_limit_pu'];loading.append(ratio)
                if ratio>1+1e-9: limit(f'branch {i}-{j} current loading',ratio)
            residual=0.
            for i in range(len(v)):
                expected=complex(s['load_kw'][t][i]-s['solar_kw'][t][i]+(d if i==st['node'] else 0),s['reactive_kvar'][t][i])
                balance=v[i]*currents[i].conjugate()*s['base_kva']+expected-(source if i==0 else 0)
                residual=max(residual,abs(balance)/s['base_kva'])
                if not .8-1e-9<=abs(v[i])<=1.2+1e-9: limit(f'bus {i} model domain',abs(v[i]))
                if not s['voltage_limits_pu'][0]-1e-9<=abs(v[i])<=s['voltage_limits_pu'][1]+1e-9: limit(f'bus {i} voltage',abs(v[i]))
            if residual>1e-7: fail('complex nodal power residual exceeds 1e-7 pu')
            max_residual=max(max_residual,residual)
            expected_end=energy+dt*(charge*st['eta_charge']-discharge/st['eta_discharge'])
            if abs(row['energy_start_kwh']-energy)>1e-6 or abs(row['energy_end_kwh']-expected_end)>1e-6: fail('storage transition/continuity')
            energy=row['energy_end_kwh'];storage_loss=dt*(charge*(1-st['eta_charge'])+discharge*(1/st['eta_discharge']-1))
            if not -1e-6<=energy<=st['capacity_kwh']+1e-6: limit('storage capacity',energy)
            if abs(d)>st['power_kw']+1e-9: limit('storage power',d)
            values=dict(import_kwh=max(0,source.real)*dt,export_kwh=max(0,-source.real)*dt,load_kwh=sum(s['load_kw'][t])*dt,solar_kwh=sum(s['solar_kw'][t])*dt,network_loss_kwh=loss*dt,storage_loss_kwh=storage_loss)
            for k,x in values.items(): totals[k]+=x
            peak=max(peak,source.real);min_v=min(min_v,min(map(abs,v)));max_v=max(max_v,max(map(abs,v)));max_loading=max(max_loading,max(loading))
            details.append(dict(interval=t,dt_hours=dt,min_voltage_pu=min(map(abs,v)),max_voltage_pu=max(map(abs,v)),max_loading=max(loading),source_kw=source.real,network_loss_kw=loss,energy_kwh=energy,residual_pu=residual,voltage_pu=list(map(abs,v)),branch_loading=loading))
        delta=energy-s['storage']['initial_kwh']
        if abs(delta)>1e-6: violations.append(dict(interval='terminal',reason='terminal storage neutrality',value=delta))
        balance=totals['import_kwh']-totals['export_kwh']+totals['solar_kwh']-totals['load_kwh']-totals['network_loss_kwh']-totals['storage_loss_kwh']-delta
        if abs(balance)>1e-6: invalid.append(dict(interval='total',reason='full energy balance exceeds 1e-6 kWh'))
        totals.update(storage_delta_kwh=delta,energy_residual_kwh=balance,peak_import_kw=peak,min_voltage_pu=min_v,max_voltage_pu=max_v,max_loading=max_loading,max_power_residual_pu=max_residual,total_loss_kwh=totals['network_loss_kwh']+totals['storage_loss_kwh'])
    except (KeyError,TypeError,ValueError,IndexError,OverflowError,ZeroDivisionError) as exc:
        invalid.append(dict(interval='structure',reason=str(exc)))
    return dict(state='INVALID_RESULT' if invalid else 'COMPLETED_INFEASIBLE' if violations else 'COMPLETED_VALID',invalid=invalid,violations=violations,metrics=totals,intervals=details)

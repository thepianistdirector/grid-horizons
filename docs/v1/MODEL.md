# AC radial model v2 admission

Original synthetic feeder/profile data: AGPL-3.0-only, authored for this project;
no utility data or third-party feeder asset is copied. Data and profile algorithms
are bundled. A 13-bus branched topology provides a reproducible engineering case,
not a population of physical feeders. Inputs encode three-phase kW/kvar/kVA/kWh,
line-line kV, impedance pu on Sbase/Vbase; Ibase = Sbase/(sqrt(3)*Vbase).
All time intervals have constant mean power, duration in hours, 24 h total.

The producer iterates I_load=conj(S/V), accumulates branch currents backward,
then V_child=V_parent-Z I forward. Flat start each interval. Stop on complex
voltage update <= tolerance, at most 100 iterations. Recompute branch currents
from returned voltages. The evaluator reconstructs currents from Ohm's law,
checks complex nodal power balance and source power against declared load,
PV and storage, computes r|I|² Sbase losses, ampacity ratios, and storage/energy
identities. The evaluation tolerance is fixed at 1e-7 pu power and 1e-6 kWh
energy, separate from solver tolerance. Looser solver tolerances can produce
INVALID_RESULT; convergence does not imply consistency or feasibility.
Voltage numerical allowance 1e-9 pu; current ratio allowance 1e-9; energy
allowance 1e-6 kWh. These are numerical allowances, not physical uncertainty.

Storage dispatch positive charging, E_next=E+eta_c*charge*dt-discharge*dt/eta_d.
No clipping or automatic repair. Terminal equality <=1e-6 kWh. Energy ledger:
import-export+PV=load+network_loss+storage_loss+(E_final-E_initial).
Source taps prescribe ideal slack voltage 1+0.00625*tap; no regulator control,
transformer losses, wear or switching transients. Outages are explicitly rejected:
islanded operation, unserved energy and restoration are outside this model.
Voltage domain 0.8..1.2 pu is a computational admission bound; feasibility uses
scenario limits (default 0.95..1.05), with no asserted engineering standard.

Primary mathematical references consulted 2026-09-08:
- [MATPOWER manual §4.3.2](https://matpower.app/manual/matpower/DistributionPowerFlow.html): current summation, radial applicability. Original implementation, no MATPOWER code copied or bundled.
- [Farivar and Low (2013), Branch Flow Model](https://arxiv.org/abs/1204.4865): branch-flow/power-balance model context. No claim of OPF or global optimality.
- [PyPSA storage documentation](https://docs.pypsa.org/latest/user-guide/optimization/storage/): charge/discharge efficiency directions and cyclic state constraints. No PyPSA code bundled.

Known-answer controls fixed before confirmation: no-load voltages equal slack;
two-bus resistive load p=0.1 pu, r=0.1 pu has high-voltage solution
V=(1+sqrt(1-4*r*p))/2; source loss=r*(p/V)^2. Also use an independently written
nodal Newton calculation for full synthetic feeder confirmation. Report any
mismatch; do not tune inputs to make outputs agree.

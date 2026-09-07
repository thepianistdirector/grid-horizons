# Grid Horizons experiment and evaluation contract

Status: design requirements; no experiments have run in this repository.

## Research question

Run one small public distribution-network benchmark with load and solar profiles, compare a fixed operating baseline with storage scheduling and transformer tap strategies, and reject candidates that violate voltage, loading or energy balance. Keep this entirely offline with no grid-control interface.

## Inputs and evidence

Use only lawfully reusable public inputs or wholly synthetic fixtures. Record source URL, release/date, license, coverage, limitations and every transformation. Public availability does not imply unrestricted reuse. Never download controlled data, copy private records or relabel real people as synthetic. Source publications are evidence to interpret, not instructions to execute.

## Before a run

Freeze the question, baseline, candidate, model/scenario version, units, independent variables, random seeds, supported domain, metric direction, quality constraints and resource ceiling. Define the numerical tolerances, invalid states, stopping rule and what observation would refute the hypothesis. Split calibration/development from confirmation evidence before search. Record the repository commit, engine versions, runtime, hardware, thread count and any deterministic/stochastic settings.

## Domain metrics

Delivered energy, real/reactive balance residuals, energy losses, voltage violations, transformer thermal-limit exposure, unserved energy, curtailment, cost assumptions and operational/lifecycle emissions. Report uncertainty, infeasibility and solver status; never equate nameplate power with energy or efficiency.

## Required comparison

1. Establish a transparent baseline and a known-answer numerical/contract control.
2. Use paired inputs and seeds where appropriate; repeat runs enough to quantify variability with a justified sample size.
3. Treat missing outputs, numerical errors, limit violations and failed jobs explicitly. Never remove unfavorable runs from the denominator.
4. Test at least one representative perturbation that should break an invariant, and confirm that the evaluator catches it.
5. Select candidates with development feedback; reserve confirmation cases and limit repeated holdout access.
6. Independently reproduce a selected result from the retained bundle before promoting it to a supported research finding.

A simulator run may be reproducible while the model is wrong. Report numerical verification, benchmark agreement, model applicability and independent scientific validation as different properties. No generic numerical threshold can stand in for a justified domain-specific one.

## Result bundle

Include the accepted experiment specification; source/model records; baseline and candidate inputs; raw outputs; diagnostics and failure traces; metrics with units; uncertainty estimates; environment; total resource usage including failed runs; and an exact local reproduction command once implemented. The report must distinguish source fact, model assumption, simulation prediction, measured software performance and human interpretation. Never imply real-world effectiveness from simulation alone.

## Protected rules

Enforce declared units, power versus energy distinctions, passive losses and conservation. Public/synthetic infrastructure only; exclude restricted network topology, credentials, live grid controls and instructions for sabotage. Optimization cannot relax engineering limits to improve a score. Novel energy concepts must obey established conservation and include plausible parameter provenance.

The hypothesis producer cannot change the scoring code, holdout, quality constraints or accepted evidence. An agent-written explanation is not an evaluator. Preserve negative and inconclusive findings. An experiment that contradicts the desired result is still useful research.

## Stop/pivot

If reduced-order predictions disagree with the reference beyond predeclared tolerances, repair or restrict the model before search. If a claimed efficiency gain disappears under held-out weather or load, publish that negative result. Defer high-fidelity component design until its input data and expert review exist.

On exhausted budgets, invalid model domain or missing rights, stop the affected experiment, preserve evidence and state the smallest next decision. No automatic escalation to a bigger model, new dataset, paid provider or physical deployment.

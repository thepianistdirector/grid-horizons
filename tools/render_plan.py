#!/usr/bin/env python3
"""Render deterministic human views and publication material from plan/tasks.json."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def dumps(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'

def render_tasks(plan):
    lines=['# Grid Horizons contributor tasks','',
           'Generated from `plan/tasks.json` by `python3 tools/render_plan.py`; edit the canonical ledger and regenerate. [STATUS.md](STATUS.md) records the owner handoff and evidence narrative. These contracts do not establish completed implementation.', '',
           f"{len(plan['tasks'])} tasks across {len(plan['waves'])} outcome waves. Original IDs, full acceptance and 71 original dependency edges remain preserved in [immutable lineage](docs/lineage/foundation-2026-09-07/plan/tasks.json). New synthetic work never completes the broader public-feeder, transformer or tap contracts.",'',
           'A status change requires actual evidence, not the existence of a row. Exact paths for later work are proposed ownership seams; bind a bounded packet before implementation. Native platform IDs remain null until actual supported publication/read-back.','']
    for t in plan['tasks']:
        lines += [f"## {t['id']} — {t['title']}",'',f"- Wave: {t['wave']}; status: **{t['status']}**; release: {t['targetRelease']}; origin: {t['origin']}.",
                  '- Dependencies: '+(', '.join(t['dependsOn']) or 'none')+'.',
                  '- Owned scope: '+', '.join('`'+p+'`' for p in t['ownedPaths'])+'.',
                  '- Acceptance: '+t['acceptance'], '- Outcome: '+t['outcome'], '- Feature area: '+t['featureArea'],
                  '- Source/decision references: '+', '.join(t['sourceRefs']),
                  '- Risk/evidence needs: '+' '.join(t['riskEvidence']),
                  '- Textual-only prerequisites: '+('; '.join(t['textualPrerequisites']) or 'none recorded')+'.',
                  '- Evidence: '+('; '.join(t['evidence']) or 'not yet recorded')+'.','']
    return '\n'.join(lines)

def render_roadmap(plan):
    lines=['# Grid Horizons outcome roadmap','',
           'Generated from `plan/tasks.json`; regenerate with `python3 tools/render_plan.py`. Current delivery is the bounded v1.0 contract in docs/v1/CONTRACT.md; historical 0.1 and long-term contracts remain preserved.', '',
           plan['scope']['objective'], '',plan['scope'].get('release10',plan['scope']['release01']), '', plan['scope']['evidenceBoundary'], '',
           'Original foundation contracts remain DONE for documentation/tooling only. Every new proposal starts PLANNED and later transitions require recorded evidence. The original public feeder, reference solver, transformer and full tap/storage programme remains separate later work.', '',
           'The source nine-wave programme and all original contracts are preserved byte-for-byte in [lineage](docs/lineage/foundation-2026-09-07/ROADMAP.md). Current outcome waves remap its work without relaxing acceptance. [Reconciliation](docs/lineage/owner-launch-reconciliation.md) records the launch decision and source treatments.', '',
           'Current v1.0 critical path: nonlinear synthetic laboratory → three frozen computational studies → skeptical reproduction → exact release package → external/qualified review and owner approval → public access and Tanduna readback. Waves 28–30 are the bounded cut; prior aspirational waves retain their own future contracts.', '',
           'Later domains require their own source, rights, model applicability, reference and qualified-review gates. Exploratory concepts are hypotheses, not promised delivery. Exact dates, paid resources, domain reviewers and external dependency adoption remain unallocated. Cut richer visuals, scale, search and additional domains before quantity integrity, conservation, feasibility and reproducibility.', '',
           '| Wave | Outcome | Horizon | Tasks |', '| --- | --- | --- | ---: |']
    for w in plan['waves']:
        lines.append(f"| {w['order']} | {w['title']} | {w['targetRelease']} | {len(w['taskIds'])} |")
    for w in plan['waves']:
        lines += ['',f"## Wave {w['order']}: {w['title']}",'',f"Outcome: {w['outcome']}",'',f"Release horizon: **{w['targetRelease']}**. Gate: **{w['gateDecision']}**.",'',
                  'Entry dependencies: '+(', '.join(w['entryDependencies']) or 'accepted original foundation source')+'.','',
                  'Assigned tasks: '+', '.join(w['taskIds'])+'.','', 'Exit evidence:']
        lines += ['- '+e for e in w['exitEvidence']]
        lines += ['', 'Gate decisions: CONTINUE, REDIRECT, DESCOPE, HOLD or TERMINATE. An unresolved prerequisite or missing required human/qualified evidence keeps the affected gate open.']
    lines += ['', '## Publication and release state','',
              'Native publication state: '+plan['publication']['state']+'. '+plan['publication']['publicObservation'], '',
              'The discussion proposal is not accepted delivery authority. Private drafts may exist; compare authenticated state before any write. Exact native IDs are acquired from supported publication and read-back; a local export is not publication.', '',
              'Current access instructions: '+plan['publication']['accessInstructionsState']+'. '+(' '.join(plan['publication']['accessInstructions']) or 'No public package or verified access command is claimed by the planning preparation.'), '',
              'Replan when rights fail, references disagree, coupling breaks conservation, confirmation becomes tuning data, uncertainty reverses conclusions, reviewer availability changes or measured workload invalidates architecture assumptions. Preserve negative evidence and reopen only affected downstream claims.', '']
    return '\n'.join(lines)

def publication(plan):
    return {'exportSchemaVersion':1,'kind':'NATIVE_PLAN_IMPORT_PREPARATION_NOT_PUBLICATION',
            'canonicalSource':'plan/tasks.json','project':plan['project'],'contractVersion':plan['contractVersion'],
            'scope':plan['scope'],'publication':plan['publication'],
            'counts':{'tasks':len(plan['tasks']),'waves':len(plan['waves']),'dependencies':sum(len(t['dependsOn']) for t in plan['tasks']),
                      'sourceTasks':len(plan['sourceMappings']),'sourceDependencies':sum(len(m['structuredPrerequisites']) for m in plan['sourceMappings']),
                      'release01Tasks':sum(t['targetRelease']=='0.1' for t in plan['tasks'])},
            'waves':plan['waves'],'tasks':plan['tasks'],'sourceMappings':plan['sourceMappings']}

def rendered_files(plan):
    return {'TASKS.md':render_tasks(plan),'ROADMAP.md':render_roadmap(plan),'plan/publication.json':dumps(publication(plan))}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    plan=json.loads((ROOT/'plan/tasks.json').read_text()); drift=[]
    for name,content in rendered_files(plan).items():
        p=ROOT/name
        if args.check:
            if not p.is_file() or p.read_text()!=content:drift.append(name)
        else:p.write_text(content)
    if drift:
        print('FAIL: generated view drift: '+', '.join(drift));return 1
    print('PASS: generated views '+('match' if args.check else 'written')+' canonical plan');return 0
if __name__=='__main__':raise SystemExit(main())

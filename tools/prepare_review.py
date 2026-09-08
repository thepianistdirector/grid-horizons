"""Seal local review assets, never publish. SPDX-License-Identifier: AGPL-3.0-only."""
import hashlib
import json
import shutil
import time
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='1.0.0rc4'
PACKAGING_REVISION=2
out=ROOT/'releases'/f'v{VERSION}-review-r{PACKAGING_REVISION}'
out.mkdir(parents=True,exist_ok=False)
start=time.perf_counter()

def collect(base):
    return {str(p.relative_to(ROOT)):p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}

def bundle(name,files,extra=None):
    with zipfile.ZipFile(out/name,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,9,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,p.read_bytes())
        for name,content in sorted((extra or {}).items()): z.writestr(name,content)

# Whitelist source and retained evidence; exclude caches, environments and Git internals.
files={p.name:p for p in ROOT.glob('*.md')}
for name in ['LICENSE','.gitignore','grid-horizons.py']:files[name]=ROOT/name
for name in ['src','tests','tools','scenarios','docs','plan','research']:files.update(collect(ROOT/name))
archives={f'releases/{v}/grid-horizons.pyz':ROOT/'releases'/v/'grid-horizons.pyz' for v in ['1.0.0rc1','1.0.0rc2','1.0.0rc3',VERSION]}
files.update(archives);files['grid-horizons.pyz']=ROOT/'releases'/VERSION/'grid-horizons.pyz'
qa={}
for name in ['study','cancelled','failed','interrupted','recovered','resumed']:
    qa.update(collect(ROOT/'runs/clean-rc4'/name))
for name in ['commands.json','result.json','invalid.json','huge.json','nonconverge.json','campaign/inventory.json','campaign/spec.json']:
    p=ROOT/'runs/clean-rc4'/name
    if p.exists():qa[str(p.relative_to(ROOT))]=p
for p in (ROOT/'runs/browser-ac-rc4').glob('*'):
    if p.is_file():qa[str(p.relative_to(ROOT))]=p
files.update(qa)
shutil.copyfile(ROOT/'releases'/VERSION/'grid-horizons.pyz',out/f'grid-horizons-{VERSION}.pyz')
bundle(f'grid-horizons-{VERSION}-complete.zip',files)
for study in ['benchmark','policies','robustness']:
    selected=collect(ROOT/'research'/study);selected.update(archives)
    selected.update(collect(ROOT/'src'))
    if study=='robustness':
        for dependency in ('selection.json','preregistration.json'):
            selected['research/policies/'+dependency]=ROOT/'research/policies'/dependency
    selected['LICENSE']=ROOT/'LICENSE'
    for name in ['MODEL.md','CONTRACT.md','REVIEW-INSTRUCTIONS.md']:selected['docs/v1/'+name]=ROOT/'docs/v1'/name
    intro=f'# Grid Horizons {study} study\n\nOpen research/{study}/report.md for the manuscript and exact rerun instructions.\nRun the Python scripts from this extracted root. Historical zipapps and complete\nraw results are included. Linux x86_64 CPython 3.12 is the supported runtime;\n3.12.14 was tested. This is locally prepared synthetic computational evidence,\nnot a public release, peer-reviewed paper, human study or physical validation.\nOriginal code/data: AGPL-3.0-only.\n\nThis archive includes the source/provenance files needed for replay. Robustness\nincludes its frozen cross-study policy selection. Investigator/model labels in\nhistorical scripts identify the original investigation; they do not attest to\nthe person or model executing a later reproduction. Actual Python/platform\nidentity is recorded on each run. Preserve the original output directories and\nchoose the fresh destinations documented in the study report.\n'
    bundle(f'grid-horizons-study-{study}.zip',selected,{'README.md':intro})
evidence=collect(ROOT/'research/reproduction');evidence.update(qa);evidence.update(collect(ROOT/'docs/v1'));evidence.update(archives);evidence['LICENSE']=ROOT/'LICENSE'
bundle('grid-horizons-reproduction-validation.zip',evidence)
for name in ['LAUNCH-COPY.md','REVIEW-INSTRUCTIONS.md']:shutil.copyfile(ROOT/'docs/v1'/name,out/name)
shutil.copyfile(ROOT/'plan/publication.json',out/'tanduna-plan.json')
assets=[]
for p in sorted(out.iterdir()):
    if p.suffix=='.zip':
        with zipfile.ZipFile(p) as z:
            bad=z.testzip()
            if bad:raise ValueError(f'archive CRC failure: {p} {bad}')
    assets.append(dict(name=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
record=dict(version=VERSION,packaging_revision=PACKAGING_REVISION,state='LOCAL_PREPARATION_NOT_PUBLICATION',assets=assets,assembly_wall_seconds=time.perf_counter()-start,source_file_count=len(files),source_bytes=sum(p.stat().st_size for p in files.values()),destinations=dict(github=f'https://github.com/thepianistdirector/grid-horizons/releases/tag/v{VERSION}',tanduna='https://tanduna.com/projects/grid-horizons',native_plan='255 tasks / 31 waves; local export only'),open_gates=['Actual external first-use observation','Qualified model-interpretation review','Owner approval for exact public artifacts/version and Tanduna update','Authorized publication, fresh public downloads and native readback'])
(out/'ASSETS.json').write_text(json.dumps(record,indent=2)+'\n')
(out/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['name']+'\n' for x in assets))
rows='\n'.join(f"| [{a['name']}]({a['name']}) | {a['bytes']:,} | `{a['sha256']}` |" for a in assets)
(out/'REVIEW.md').write_text(f'''# Grid Horizons v1.0 release review

**Exact prepared candidate: {VERSION}, packaging revision {PACKAGING_REVISION}.** Local software and computational acceptance
passes. No public release, public commit, Tanduna write, paper submission, participant
contact or new paid resource has occurred. The native goal remains active.

## Ready artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
{rows}

The complete archive extracts into an install-free project root, with current and
historical zipapps, source, all three research packages, skeptical reproduction,
raw outputs, failure inventories, screenshots, validation logs, docs and canonical
plan. Use `python3 grid-horizons.pyz lab example --output my-input.json`, then follow
README.md. No private credentials or runtime pip packages are needed.

Application SHA-256: `15aaa7913e4069b9483fcb721032c812a8babc865968d652bb681f031abc7c6e`.
Implementation: `b2eeb117a34ea3423136a0082442d1b93f01b0c6e13dab429772a0d2c3a8f8e3`.
Supported/tested: Linux x86_64, CPython 3.12 (3.12.14 observed), offline Chromium
report. 75 runtime tests, 34 plan tests, 22 clean-package commands, 22 browser checks.
Clean test used a new venv/process/directory on the same host, not a container,
second physical machine or external person. Independent agent review supports all
three bounded studies after auditing 153 study bundles and 1,224 Newton intervals.

## Proposed destinations and remaining gates

GitHub: [the project release page](https://github.com/thepianistdirector/grid-horizons/releases),
proposed prerelease tag `v{VERSION}` with the exact listed assets and approved source.
Tanduna: [Grid Horizons](https://tanduna.com/projects/grid-horizons), using the prepared
255-task/31-wave native plan export and English launch copy. A local export does
not establish submission, acceptance, adoption or native publication. No paper
submission or social post is included in this request.

The owner must identify/authorize an actual external first-use participant and a
qualified distribution-model reviewer, using REVIEW-INSTRUCTIONS.md. Their evidence
remains absent and cannot be supplied by agents. Any required correction produces
a new checked candidate and reviewable hashes. After these gates, explicit approval
is required for this exact public version, assets and Tanduna update; previous
release approvals do not carry over. This requirement comes from Lucas's September
8 owner mandate, not an inferred tool restriction.

Three findings are computationally supported: convergence can fail independent
residual validation; storage peak/line-loss benefits can increase total energy loss;
and nominal schedule feasibility fails under predeclared timing/current stresses.
All claims are confined to the declared synthetic model. No field deployment,
certification, peer review, human study or broad physical validation is claimed.
''')
print(json.dumps(record,indent=2))

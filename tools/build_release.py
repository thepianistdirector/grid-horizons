"""Build a deterministic dependency-free zipapp and corresponding source. AGPL-3.0-only."""
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from grid_horizons.assets import build_identity, ASSETS
from grid_horizons import __version__
out=ROOT/'releases'/__version__
out.mkdir(parents=True,exist_ok=False)
identity=build_identity();identity['kind']='zipapp'
revision=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True)
identity['source_revision']=revision.stdout.strip() if revision.returncode==0 else None
identity['source_state']='implementation hash and bundled source identify the build; Git base alone does not identify uncommitted work'
def bundle(path,files):
 with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in sorted(files.items()):
   info=zipfile.ZipInfo(name,date_time=(2026,9,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
files={'__main__.py':b'from grid_horizons.cli import main\nraise SystemExit(main())\n','LICENSE':(ROOT/'LICENSE').read_bytes()}
for p in (ROOT/'src/grid_horizons').glob('*.py'): files['grid_horizons/'+p.name]=p.read_bytes()
for name,relative in ASSETS.items():files['grid_horizons/data/'+name]=(ROOT/relative).read_bytes()
files['grid_horizons/data/build.json']=json.dumps(identity,sort_keys=True).encode()
bundle(out/'grid-horizons.pyz',files)
source={}
for base in ['src','tests','tools','scenarios','docs','plan']:
 for p in (ROOT/base).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.png','.pdf'): source[str(p.relative_to(ROOT))]=p.read_bytes()
for p in ROOT.glob('*.md'):source[p.name]=p.read_bytes()
for name in ['LICENSE','grid-horizons.py','.gitignore']:source[name]=(ROOT/name).read_bytes()
bundle(out/'grid-horizons-source.zip',source)
(out/'build.json').write_text(json.dumps(identity,indent=2)+'\n')
(out/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(out.iterdir()) if p.name!='SHA256SUMS'))
print(json.dumps(dict(directory=str(out),identity=identity),indent=2))

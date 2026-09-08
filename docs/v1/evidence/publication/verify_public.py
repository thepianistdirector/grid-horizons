import hashlib,json,subprocess,urllib.request,time
from pathlib import Path
root=Path(__file__).resolve().parent
expected=json.loads((root/'upload-manifest.json').read_text())
api='https://api.github.com/repos/thepianistdirector/grid-horizons/releases/tags/v1.0.0rc4'
def get(url):
 return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Grid-Horizons-public-verification','Accept':'application/vnd.github+json' if 'api.github.com' in url else '*/*'}),timeout=120)
with get(api) as r: release=json.load(r)
assert not release['draft'] and release['prerelease'] and release['tag_name']=='v1.0.0rc4'
(root/'public-release-api.json').write_text(json.dumps(release,indent=2)+'\n')
assets={x['name']:x for x in release['assets']}
assert set(assets)=={x['name'] for x in expected}
(root/'public-downloads').mkdir(exist_ok=False)
records=[]
for row in expected:
 a=assets[row['name']]; assert a['size']==row['bytes']
 assert a.get('digest')=='sha256:'+row['sha256'],a
 p=root/'public-downloads'/row['name'];h=hashlib.sha256();n=0;t=time.time()
 with get(a['browser_download_url']) as r,p.open('wb') as out:
  while True:
   b=r.read(1024*1024)
   if not b:break
   out.write(b);h.update(b);n+=len(b)
 assert n==row['bytes'] and h.hexdigest()==row['sha256']
 records.append(dict(name=row['name'],url=a['browser_download_url'],bytes=n,sha256=h.hexdigest(),seconds=time.time()-t,anonymous=True,state='PASS'))
 (root/'public-download-verification.json').write_text(json.dumps(dict(state='PASS_SO_FAR',assets=records),indent=2)+'\n')
 print('Verified anonymous download: '+row['name'],flush=True)
(root/'public-download-verification.json').write_text(json.dumps(dict(state='PASS',assets=records,release_url=release['html_url'],source_commit='ab9d4c8b4f753abc0ea21456e4186dcc54901d9d',environment='same Linux host; unauthenticated HTTPS; no separate machine or human test'),indent=2)+'\n')

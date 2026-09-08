/** Development-only Chromium CDP verification; no package dependencies. */
import { spawn } from 'node:child_process';
import { readFile, writeFile, mkdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.resolve(root, process.argv[2] || 'runs/first-study/report.html');
const output = path.resolve(root, process.argv[3] || 'runs/browser');
if (!source.startsWith(root + '/') || !output.startsWith(root + '/runs/browser')) throw Error('QA paths must stay in this project and runs/browser');
await mkdir(output, { recursive: true });
await mkdir(path.join(root, '.cache/browser/profile'), { recursive: true });
const binary = process.env.GRID_BROWSER || '/home/codex/.cache/ms-playwright/chromium_headless_shell-1193/chrome-linux/headless_shell';
let browser, ws, seq = 0;
const pending = new Map(), events = [], checks = [];
const check = (name, pass, evidence) => { checks.push({ name, pass: Boolean(pass), evidence }); };
const pause = ms => new Promise(r => setTimeout(r, ms));
try {
 let endpoint = process.env.GRID_CDP_ENDPOINT;
 if (!endpoint) {
  browser = spawn(binary, ['--headless', '--disable-gpu', '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=0', `--user-data-dir=${root}/.cache/browser/profile`, 'about:blank'], { env: { ...process.env, LD_LIBRARY_PATH: `${root}/.cache/browser/root/usr/lib64${process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : ''}` }, stdio: ['ignore', 'ignore', 'pipe'] });
  let log = '';
  endpoint = await new Promise((resolve, reject) => { const timer = setTimeout(() => reject(Error('Chromium launch timeout')), 15000); browser.stderr.on('data', d => { log += d; const m = log.match(/DevTools listening on (ws:\/\/[^\s]+)/); if (m) { clearTimeout(timer); resolve(m[1]); } }); browser.once('exit', code => { clearTimeout(timer); reject(Error(`Chromium exited ${code}: ${log}`)); }); });
  await writeFile(path.join(output, 'browser-launch.log'), log);
 }
 ws = new WebSocket(endpoint);
 await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
 ws.onmessage = ({ data }) => { const msg = JSON.parse(data); if (msg.id) { const p = pending.get(msg.id); if (p) { pending.delete(msg.id); msg.error ? p.reject(Error(JSON.stringify(msg.error))) : p.resolve(msg.result); } } else events.push(msg); };
 const call = (method, params = {}, sessionId) => new Promise((resolve, reject) => { const id = ++seq; pending.set(id, { resolve, reject }); ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) })); });
 const { targetId } = await call('Target.createTarget', { url: 'about:blank' });
 const { sessionId } = await call('Target.attachToTarget', { targetId, flatten: true });
 const c = (method, params = {}) => call(method, params, sessionId);
 const evaluate = async expression => { const r = await c('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true }); if (r.exceptionDetails) throw Error(JSON.stringify(r.exceptionDetails)); return r.result.value; };
 const key = async (key, code = key, extra = {}) => { await c('Input.dispatchKeyEvent', { type: 'keyDown', key, code, ...(key === 'Enter' ? {text:'\r'} : key === ' ' ? {text:' '} : {}), ...extra }); await c('Input.dispatchKeyEvent', { type: 'keyUp', key, code, ...extra }); };
 const viewport = async (width, height, mobile = false, deviceScaleFactor = 1) => { await c('Emulation.setDeviceMetricsOverride', { width, height, mobile, deviceScaleFactor }); await evaluate('scrollTo(0,0)'); await pause(120); };
 const shot = async (name, full = false) => { const metrics = await c('Page.getLayoutMetrics'); const r = await c('Page.captureScreenshot', { format: 'png', captureBeyondViewport: full, ...(full ? { clip: { x: 0, y: 0, width: metrics.cssContentSize.width, height: metrics.cssContentSize.height, scale: 1 } } : {}) }); await writeFile(path.join(output, name + '.png'), Buffer.from(r.data, 'base64')); };
 await c('Page.enable'); await c('Runtime.enable'); await c('Log.enable');
 await c('Page.navigate', { url: pathToFileURL(source).href }); await pause(300);
 const version = await call('Browser.getVersion');
 check('Meaningful rendered study', await evaluate('document.body.innerText.includes("Grid Horizons") && document.querySelectorAll("table").length >= 3'), await evaluate('({title: document.title, textCharacters:document.body.innerText.length})'));
 await viewport(1440, 1000); await shot('desktop'); await shot('desktop-full', true);
 const widths = [];
 for (const [w,h,name] of [[390,844,'phone'],[320,844,'narrow320'],[720,500,'zoom200-reflow']]) {
  await viewport(w,h,false, name==='zoom200-reflow'?2:1);
  const measurements = await evaluate('({innerWidth, documentWidth:document.documentElement.scrollWidth, bodyWidth:document.body.scrollWidth, scrollRegions:[...document.querySelectorAll(".table-wrap")].filter(x=>x.getClientRects().length).map(x=>({label:x.getAttribute("aria-label"),width:x.clientWidth,scrollWidth:x.scrollWidth}))})');
  widths.push({ name, ...measurements }); check(`${name}: no page horizontal overflow`, measurements.documentWidth <= w && measurements.bodyWidth <= w, measurements);
  await shot(name); if (w===390) { await shot('phone-full', true); await evaluate('scrollTo(0,document.querySelector(".arms").getBoundingClientRect().top+scrollY-35)'); await shot('phone-comparison'); }
 }
 // Browser keyboard input (not synthetic DOM events).
 await viewport(390,844); await c('Page.navigate', { url: pathToFileURL(source).href }); await pause(200);
 await key('Tab','Tab',{windowsVirtualKeyCode:9});
 const skip = await evaluate('({text:document.activeElement.textContent,outline:getComputedStyle(document.activeElement).outlineStyle,top:document.activeElement.getBoundingClientRect().top})');
 check('First Tab exposes visible skip link', skip.text==='Skip to study' && skip.top>=0 && skip.outline==='solid', skip); await shot('keyboard-skip');
 await key('Enter','Enter',{windowsVirtualKeyCode:13}); check('Skip link reaches main', await evaluate('location.hash==="#main"'), await evaluate('({hash:location.hash,active:document.activeElement.id})'));
 await evaluate('document.querySelectorAll("nav a")[1].focus()'); await key('Enter','Enter',{windowsVirtualKeyCode:13}); check('Section link works with Enter',await evaluate('location.hash==="#quantities"'),await evaluate('location.hash'));
 await evaluate('document.querySelector("details summary").focus()'); await key('Enter','Enter',{windowsVirtualKeyCode:13}); check('Details opens with Enter',await evaluate('document.querySelector("details").open'),await evaluate('document.activeElement.textContent')); await shot('keyboard-details');
 await key(' ','Space',{windowsVirtualKeyCode:32}); check('Details closes with Space',await evaluate('!document.querySelector("details").open'));
 await evaluate('document.querySelector(".table-wrap").focus(); document.querySelector(".table-wrap").scrollLeft=0');
 for(let n=0;n<5;n++) await key('ArrowRight','ArrowRight',{windowsVirtualKeyCode:39}); await pause(250);
 const scroll = await evaluate('({scrollLeft:document.activeElement.scrollLeft,outline:getComputedStyle(document.activeElement).outlineStyle,label:document.activeElement.getAttribute("aria-label")})');
 check('Focused table scrolls with Right Arrow',scroll.scrollLeft>0 && scroll.outline==='solid',scroll); await shot('keyboard-table-scroll');
 const downloads = await evaluate('[...document.querySelectorAll("a[download]")].map(a=>({label:a.textContent,href:a.href}))');
 for(const link of downloads) { let valid=false, bytes=0; try { const p=fileURLToPath(link.href); if(path.dirname(p)===path.dirname(source)) { const s=await stat(p); valid=s.isFile() && s.size>0; bytes=s.size; } }catch{} check(`Local export: ${link.label}`,valid,{href:link.href,bytes}); }
 check('At least six evidence downloads',downloads.length>=6,downloads.length);
 const downloadPath=path.join(output,'downloads'); await mkdir(downloadPath,{recursive:true});
 await call('Browser.setDownloadBehavior',{behavior:'allow',downloadPath,eventsEnabled:true});
 await evaluate('document.querySelector("a[download]").focus()'); await key('Enter','Enter',{windowsVirtualKeyCode:13}); await pause(300);
 const downloadEvents=events.filter(x=>x.method==='Browser.downloadProgress');
 let sameDownload=false; try { sameDownload=(await readFile(path.join(downloadPath,'scenario.json'))).equals(await readFile(path.join(path.dirname(source),'scenario.json'))); } catch{}
 const openedExport=await evaluate('({url:location.href,text:document.body.innerText})');
 let opensExact=false; try { opensExact=JSON.stringify(JSON.parse(openedExport.text))===JSON.stringify(JSON.parse(await readFile(path.join(path.dirname(source),'scenario.json'),'utf8'))); } catch {}
 check('Keyboard export opens or downloads exact scenario JSON',sameDownload || opensExact,{downloadCompleted:downloadEvents.some(x=>x.params.state==='completed'),openedExactJSON:opensExact,url:openedExport.url});
 await c('Page.navigate',{url:pathToFileURL(source).href}); await pause(150);

 const cues = await evaluate('({badges:[...document.querySelectorAll(".badge")].map(x=>x.textContent),roles:[...document.querySelectorAll(".arm .eyebrow")].map(x=>x.textContent),states:[...document.querySelectorAll(".state")].map(x=>x.textContent),verdict:document.querySelector(".verdict").innerText})');
 check('Status and policy identity use explicit text',cues.badges.length===2 && cues.roles.includes('baseline') && cues.roles.includes('candidate') && cues.states.every(Boolean),cues);
 if(process.argv[4]) {
  const errorPath=path.resolve(root,process.argv[4]); if(!errorPath.startsWith(root+'/runs/')) throw Error('Error fixture must be project-local');
  await c('Page.navigate',{url:pathToFileURL(errorPath).href}); await pause(150); await viewport(390,844);
  const errorState=await evaluate('({states:[...document.querySelectorAll(".state")].map(x=>x.textContent),verdict:document.querySelector(".verdict").innerText,body:document.body.innerText})');
  check('Unsuccessful-attempt view labels unavailable comparison',errorState.body.includes('CANCELLED') && errorState.verdict.includes('not eligible'),{source:path.relative(root,errorPath),...errorState});
  await evaluate('scrollTo(0,document.querySelector(".verdict").getBoundingClientRect().top+scrollY-20)'); await shot('phone-unsuccessful'); await shot('phone-unsuccessful-full',true);
 }
 const errors=events.filter(x=>x.method==='Runtime.exceptionThrown'||x.method==='Log.entryAdded'&&x.params.entry.level==='error'); check('No browser runtime/console errors',errors.length===0,errors);
 const result={date:new Date().toISOString(),source:path.relative(root,source),sourceSha256:createHash('sha256').update(await readFile(source)).digest('hex'),browser:version,viewportNotes:'Desktop 1440x1000; phone 390x844; narrow 320x844. 200% reflow proxy: 720x500 CSS px at DPR 2 (equivalent layout to 1440x1000 at 200%); not browser UI zoom.',checks,widths};
 await writeFile(path.join(output,'results.json'),JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({output,passed:checks.filter(x=>x.pass).length,failed:checks.filter(x=>!x.pass)},null,2));
 await call('Browser.close'); ws.close();
 if(checks.some(x=>!x.pass)) process.exitCode=1;
} finally { ws?.close(); if(browser && browser.exitCode===null) browser.kill('SIGTERM'); }

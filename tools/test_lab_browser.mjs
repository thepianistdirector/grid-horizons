/** Product report CDP QA using existing Chromium; no third-party JS. */
import {spawn} from 'node:child_process';
import {readFile,writeFile,mkdir,stat} from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=path.resolve(root,process.argv[2]||'runs/rc1-study/report.html');
const output=path.resolve(root,process.argv[3]||'runs/browser-ac-rc1');
if(!source.startsWith(root+'/')||!output.startsWith(root+'/runs/browser'))throw Error('project-local QA paths required');
await mkdir(output,{recursive:true});
const binary=process.env.GRID_BROWSER||'/home/codex/.cache/ms-playwright/chromium_headless_shell-1193/chrome-linux/headless_shell';
let browser,ws,seq=0;const pending=new Map(),events=[],checks=[];
const check=(name,pass,evidence)=>checks.push({name,pass:Boolean(pass),evidence});
const pause=ms=>new Promise(r=>setTimeout(r,ms));
try{
 browser=spawn(binary,['--headless','--disable-gpu','--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',`--user-data-dir=${output}/profile`,'about:blank'],{env:{...process.env,LD_LIBRARY_PATH:`${root}/.cache/browser/root/usr/lib64${process.env.LD_LIBRARY_PATH?':'+process.env.LD_LIBRARY_PATH:''}`},stdio:['ignore','ignore','pipe']});
 let log='';const endpoint=await new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('launch timeout')),15000);browser.stderr.on('data',d=>{log+=d;const m=log.match(/DevTools listening on (ws:\/\/[^\s]+)/);if(m){clearTimeout(timer);resolve(m[1]);}});browser.once('exit',code=>{clearTimeout(timer);reject(Error(`exit ${code}: ${log}`));});});
 ws=new WebSocket(endpoint);await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
 ws.onmessage=({data})=>{const m=JSON.parse(data);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}}else events.push(m);};
 const call=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params,...(sessionId?{sessionId}:{})}));});
 const {targetId}=await call('Target.createTarget',{url:'about:blank'});const {sessionId}=await call('Target.attachToTarget',{targetId,flatten:true});
 const c=(method,params={})=>call(method,params,sessionId);
 const evaluate=async expression=>{const r=await c('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 const key=async(key,code=key,extra={})=>{await c('Input.dispatchKeyEvent',{type:'keyDown',key,code,...(key==='Enter'?{text:'\r'}:{}),...extra});await c('Input.dispatchKeyEvent',{type:'keyUp',key,code,...extra});};
 const shot=async name=>{const r=await c('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await writeFile(path.join(output,name+'.png'),Buffer.from(r.data,'base64'));};
 await c('Page.enable');await c('Runtime.enable');await c('Log.enable');await c('Page.navigate',{url:pathToFileURL(source).href});await pause(250);
 const version=await call('Browser.getVersion');
 check('Report renders actual four-policy table',await evaluate('document.querySelectorAll(".table-wrap tbody")[0].rows.length===4 && document.querySelectorAll("#buses tr").length===13'));
 for(const [w,h,name] of [[1440,1000,'desktop'],[390,844,'phone'],[320,844,'narrow'],[720,500,'reflow200-proxy']]){
  await c('Emulation.setDeviceMetricsOverride',{width:w,height:h,mobile:false,deviceScaleFactor:name==='reflow200-proxy'?2:1});await evaluate('scrollTo(0,0)');await pause(100);
  const size=await evaluate('({width:innerWidth,document:document.documentElement.scrollWidth})');check(name+' no horizontal page overflow',size.document<=w,size);await shot(name);
 }
 await c('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,mobile:false,deviceScaleFactor:1});
 await c('Page.navigate',{url:pathToFileURL(source).href});await pause(100);await key('Tab','Tab',{windowsVirtualKeyCode:9});
 check('Visible keyboard skip link',await evaluate('document.activeElement.textContent==="Skip to study" && document.activeElement.getBoundingClientRect().top>=0'));await key('Enter','Enter',{windowsVirtualKeyCode:13});check('Skip reaches main',await evaluate('location.hash==="#main"'));
 await evaluate('document.querySelector("#policy").focus()');await key('ArrowDown','ArrowDown',{windowsVirtualKeyCode:40});await key('Enter','Enter',{windowsVirtualKeyCode:13});await pause(100);
 check('Policy changes using real keyboard',await evaluate('document.querySelector("#policy").value==="1"'));
 const before=await evaluate('document.querySelector("#detail").innerText');await evaluate('document.querySelector("#interval").focus()');
 for(let i=0;i<45;i++)await key('ArrowRight','ArrowRight',{windowsVirtualKeyCode:39});
 const after=await evaluate('({interval:document.querySelector("#interval").value,detail:document.querySelector("#detail").innerText})');check('Interval changes evaluated metrics',after.interval==='45' && after.detail!==before,after);await shot('trajectory');
 await evaluate('document.querySelector("details summary").focus()');await key('Enter','Enter',{windowsVirtualKeyCode:13});check('Failure details keyboard disclosure',await evaluate('document.querySelector("details").open'));
 const downloads=await evaluate('[...document.querySelectorAll("a[download]")].map(x=>({href:x.href,label:x.textContent}))');
 for(const link of downloads){let ok=false;try{const p=fileURLToPath(link.href);ok=path.dirname(p)===path.dirname(source)&&(await stat(p)).size>0;}catch{}check('Evidence export '+link.label,ok);}
 await evaluate('document.querySelector("a[download]").focus()');await key('Enter','Enter',{windowsVirtualKeyCode:13});await pause(150);
 const exported=await evaluate('document.body.innerText');let exact=false;try{exact=JSON.stringify(JSON.parse(exported))===JSON.stringify(JSON.parse(await readFile(path.join(path.dirname(source),'scenario.json'),'utf8')));}catch{}
 check('Keyboard export opens exact scenario JSON',exact);
 if(process.argv[4]){const error=path.resolve(root,process.argv[4]);await c('Page.navigate',{url:pathToFileURL(error).href});await pause(150);check('Cancellation shows unavailable interval, no invented metrics',await evaluate('document.querySelector("#detail").innerText.includes("CANCELLED") && document.querySelectorAll("#buses tr").length===0'));await shot('cancelled');}
 check('No runtime or console errors',!events.some(x=>x.method==='Runtime.exceptionThrown'||x.method==='Log.entryAdded'&&x.params.entry.level==='error'));
 await writeFile(path.join(output,'results.json'),JSON.stringify({source,sourceSha256:createHash('sha256').update(await readFile(source)).digest('hex'),browser:version,date:new Date().toISOString(),checks},null,2)+'\n');
 console.log(JSON.stringify({output,passed:checks.filter(x=>x.pass).length,failed:checks.filter(x=>!x.pass)},null,2));await call('Browser.close');ws.close();if(checks.some(x=>!x.pass))process.exitCode=1;
}finally{ws?.close();if(browser&&browser.exitCode===null)browser.kill('SIGTERM');}

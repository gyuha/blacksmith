import { chromium } from 'playwright-core';
const b = await chromium.launch({ executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true,
  args:['--enable-gpu','--ignore-gpu-blocklist','--use-angle=metal','--autoplay-policy=no-user-gesture-required','--mute-audio'] });
const p = await b.newPage({ viewport:{width:1280,height:720} });
const errs=[]; p.on('pageerror',e=>errs.push(String(e))); p.on('console',m=>{if(m.type()==='error')errs.push(m.text());});
await p.goto(process.argv[2], { waitUntil:'load' });
await p.waitForTimeout(+(process.argv[4]||4500));
await p.screenshot({ path: process.argv[3] });
const s = await p.evaluate(()=>window.__game.state);
console.log(JSON.stringify({fps:s.fps, phase:s.phase, gold:s.gold}), 'errors', errs.length);
await b.close();

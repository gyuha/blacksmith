// Keyboard-only playtest for THE TEMPER.
// Reads window.__game.state to time the hammer; never writes into the game.
export async function play(page, { seconds, t0 }) {
  const st = () => page.evaluate(() => window.__game.state);
  const wait = ms => page.waitForTimeout(ms);

  const until = async (fn, timeout = 8000, step = 12) => {
    const t = Date.now();
    while (Date.now() - t < timeout) {
      const s = await st();
      if (fn(s)) return s;
      await wait(step);
    }
    return await st();
  };

  const goTo = async (station) => {
    let s = await st();
    const order = ['hearth', 'bench', 'shop'];
    let guard = 0;
    while (s.station !== station && guard++ < 5) {
      const i = order.indexOf(s.station), j = order.indexOf(station);
      const key = (j - i + 3) % 3 === 1 ? 'KeyD' : 'KeyA';
      await page.keyboard.press(key);
      await wait(240);
      s = await until(x => x.station === station, 1000);
    }
    return s;
  };

  // release a little before the middle of the zone: the keyup lands inside it
  const strike = async () => {
    await until(s => s.outcome === null && s.mode === 'bench', 6000);
    await page.keyboard.down('Space');
    const target = s => s.charging && s.cursor >= s.zoneLo + 0.05 * (s.zoneHi - s.zoneLo);
    await until(target, 3000, 8);
    await page.keyboard.up('Space');
    await until(s => s.outcome !== null, 1200, 8);
    const mid = await st();
    await until(s => s.outcome === null || s.phase === 'end', 3500, 25);
    return mid.outcome;
  };

  let s = await st();
  if (s.phase === 'title') { await page.keyboard.press('Space'); await wait(600); }

  const log = [];
  let guard = 0;
  const t_start = Date.now();
  const elapsed = () => (Date.now() - t_start) / 1000;
  while (guard++ < 30) {
    s = await st();
    if (s.phase === 'end') break;

    if (!s.held) {
      await goTo('shop');
      const shops = await st();
      if (shops.phase === 'end') break;
      await page.keyboard.press('Space');
      await wait(450);
      if (!(await st()).held) break;
      continue;
    }

    if (s.tier >= 10) {
      for (let k = 0; k < 3; k++) {
        const g = await goTo('shop');
        if (g.station !== 'shop') continue;
        await page.keyboard.press('Space');
        await wait(500);
        const ss = await st();
        if (ss.phase === 'end' || !ss.held) break;
      }
      s = await st();
      if (s.phase === 'end') break;
      continue;
    }

    if (s.strikes <= 1 && s.tier >= 4) {
      await goTo('hearth');
      const qs = await st();
      if (qs.held && qs.strikes <= 1) { await page.keyboard.press('Space'); await wait(450); }
      if ((await st()).phase === 'end') break;
    }

    if (s.gold < s.tax) {                       // cannot pay the forge fee: sell first
      await goTo('shop');
      const ss = await st();
      if (ss.held) { await page.keyboard.press('Space'); await wait(500); }
      continue;
    }
    await goTo('bench');
    const b = await st();
    if (b.mode !== 'bench' || !b.held) continue;
    const out = await strike();
    const after = await st();
    log.push({ t: +elapsed().toFixed(1), out, tier: after.tier, strikes: after.strikes });
  }

  console.log('run log:', JSON.stringify(log));
  const end = await st();
  console.log('end:', JSON.stringify({ phase: end.phase, ended: end.ended, gold: end.gold, tier: end.tier }));
  await wait(1500);
}

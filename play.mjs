// Keyboard-only playtest for THE TEMPER (open room).
// Steers with WASD from the player position published in window.__game.state; never writes into the game.
// Route: order window -> (round the crate's south side) -> anvil/furnace -> back to the order window.
export async function play(page, { seconds, t0 }) {
  const st = () => page.evaluate(() => window.__game.state);
  const wait = ms => page.waitForTimeout(ms);

  const down = new Set();
  const setKeys = async want => {
    for (const k of [...down]) if (!want.has(k)) { await page.keyboard.up(k); down.delete(k); }
    for (const k of want) if (!down.has(k)) { await page.keyboard.down(k); down.add(k); }
  };

  // walk to (x, z) holding WASD (yaw stays 0: W = north/-z, D = east/+x)
  const steerTo = async (x, z, tol = 0.15, timeout = 14000) => {
    const t = Date.now();
    let last = await st(), lastT = Date.now(), lastD = Infinity;
    while (Date.now() - t < timeout) {
      const s = await st();
      const dx = x - s.player.x, dz = z - s.player.z, d = Math.hypot(dx, dz);
      if (d <= tol) { await setKeys(new Set()); return s; }
      const want = new Set();
      if (dx > 0.06) want.add('KeyD'); else if (dx < -0.06) want.add('KeyA');
      if (dz > 0.03) want.add('KeyS'); else if (dz < -0.03) want.add('KeyW');
      await setKeys(want);
      if (d < lastD - 0.05) { lastD = d; lastT = Date.now(); }
      else if (Date.now() - lastT > 2500) { await setKeys(new Set()); throw new Error(`stuck at (${s.player.x},${s.player.z}) heading to (${x},${z})`); }
      await wait(25);
    }
    await setKeys(new Set());
    throw new Error(`timeout steering to (${x},${z})`);
  };
  const route = async pts => { for (const [x, z] of pts) await steerTo(x, z, 0.18); };
  const press = async code => { await page.keyboard.press(code); await wait(180); };

  // hold SPACE, release a little inside the band
  const strike = async () => {
    await page.keyboard.down('Space');
    const t = Date.now();
    for (;;) {
      const s = await st();
      if (s.charging && s.cursor >= s.zoneLo + 0.05 * (s.zoneHi - s.zoneLo)) break;
      if (!s.charging && Date.now() - t > 600) break;
      if (Date.now() - t > 3000) break;
      await wait(8);
    }
    await page.keyboard.up('Space');
    const u = Date.now();
    for (;;) {                                   // outcome plays out (~1.6 s)
      const s = await st();
      if (s.outcome === null && Date.now() - u > 150) break;
      if (Date.now() - u > 4000) break;
      await wait(30);
    }
  };

  let s = await st();
  if (s.phase === 'title') { await page.keyboard.press('Space'); await wait(600); }
  const z = s.zones;
  const ORDER = [z.order.x, z.order.z + 0.9];          // in front of the order window
  const ANVIL = [3.0, 1.65];                           // beside the anvil, inside craft + forge radii
  const OUT = [[-1.0, 0.2], [0.6, 0.8], [1.6, 1.65], ANVIL];   // south of the crate: (1.6,1.65) -> (3.0,1.65)
  const BACK = [[1.6, 1.65], [0.6, 0.8], [-1.0, 0.2], ORDER];

  const tEnd = Date.now() + (seconds ?? 90) * 1000;
  let guard = 0;
  while (guard++ < 40 && Date.now() < tEnd) {
    s = await st();
    if (s.ordersCompleted >= 1) break;
    const h = s.held;
    if (!s.order && !h) {                               // 1. take the order
      if (s.player.traveled < 3) await route([[-2.6, 1.2], [-2.6, -1.2]]);   // look round the west side first
      await route([ORDER]);
      await press('KeyE');
    } else if (s.order && !h) {                         // 2. pick up a bar at the craft zone
      await route(OUT);
      await press('KeyE');
    } else if (h && h.struck && h.tier >= s.order.req) { // 5. deliver
      await route(BACK);
      await press('KeyE');
    } else {                                            // 3-4. heat, then strike
      await route([ANVIL]);
      if (h.heat < 0.5) await press('KeyE');
      await strike();
    }
  }
  await setKeys(new Set());
  const end = await st();
  console.log('end:', JSON.stringify({ orders: end.ordersCompleted, gold: end.gold, traveled: end.player.traveled, log: end.interactLog.map(e => `${e.action}@${e.zone}`) }));
  await wait(500);
}

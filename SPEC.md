# SPEC — forge bench game, from forgetax.mp4

Source: `forgetax.mp4` (91.8 min, 1280x720, 30 fps) — a capture of the released game *FORGE TAX*.
Studied: `study/` (frames t=1730..1860 of the source, `clip_forge.mp4`) and stills `refs/ref_1734..1800.jpg`.
Deliverable is an **original homage**: same bench framing, palette and gamble, own world, names and UI.

## The source's shape (what I measured, not remembered)

- 80% of the clip is a **locked-off first-person bench view**. No avatar on screen, no orbit.
- Composition: weapon lies diagonally in the lower third, tip to the right; hammer head enters from the
  right edge; behind it a dark olive-grey brick wall with pinned paper notices (calendars, tally sheets);
  a hanging tool rack at the right; a wide translucent plaque floats above the bench.
- The strike: hammer falls, **sparks** spray off the blade, a **die tumbles** across the bench, the blade
  flares white (success) or prismatic (best outcome) or cracks (failure).
- Between strikes: a workbench close-up, then a wide hearth shot (arched stone furnace, orange fire
  spilling onto the floor), then a shop wall of lit display cabinets.
- Palette (study.json, 14 colours): `#0e0e0d #161713 #12110d #24241a #262923 #1d211a #353728 #464837
  #2b3327 #3b4435 #555946 #373c32` — olive graphite, near-black, no blue. Warm amber key light, crimson
  only on destruction, prismatic only on the best proc.

## Camera

First person, eye 1.62 m, 60° vertical FOV, no avatar. WASD walks (2.6 m/s, circle collider r=0.22 against
walls and furniture), mouse (pointer lock after a click) **and** the arrow keys look: `←→` turn, `↑↓` pitch.
A held blade sits low-left, the hammer low-right (only near the anvil). Small shake on impact, slight head-bob.

## Hero

Not a character — the **blade**. Readable at 100 px: a long pale steel blade with a single dark fuller,
brass guard, wrapped grip, lying at 18° on the bench. Its state is the whole readability problem: tier
is told by **glow** (none → thin white edge → warm gold → white-hot → prismatic), never by text.

## The one mechanic

**Strike and wager** (kept from the first build). Near the anvil, hold `Space` to wind up; a heat band on a
small HUD gauge sweeps while you hold. Release inside the band and the roll is nudged toward success
(*focused strike*); late means a weaker roll. A hotter bar gives a wider band. Outcomes: **shatter** (bar
lost, take another), **damage** (tier −1), **hold**, **rise** (+1), **surge** (+2..+3, prismatic flare).
Each strike costs 12 g. The band can be widened ×1.9 once by the exchange's tonic.

## World (the rebuilt room, art3d GLBs)

One 10 × 8 m room, centre = origin, `+x` east, `+z` south. Models: `room_shell`, `room_order_window`,
`room_exchange`, `room_anvil_bench`, `room_furnace`, `room_display`, `room_gate`, `room_weapon_rack`,
`room_material_crate`, plus `fire.glb` in the firebox; `blade.glb` and `hammer.glb` are recycled.
Colliders are the loaded models' footprints (shrunk 6 cm) plus any interior brick boxes read from the shell (none now: one open room).

| zone | where | model | role |
|---|---|---|---|
| `order` | north wall, west bay (x≈-1.6, 2.05 m deep, stand at z≈-1.9) | order window | take the order, deliver the blade; a dark silhouette waits at the window while an order is open |
| `exchange` | north wall, east bay (x≈+1.6) | exchange panel | spend 100 g on a steadying tonic (wider band, next strike) |
| `craft` | east, anvil bench + material crate | anvil bench, crate | take an iron bar (40 g), strike (`Space`) |
| `forge` | east, furnace front | furnace + fire | heat the bar to 100 % (cools over ~45 s; a strike needs ≥ 20 %) |
| `display` | south wall | lit cabinet | put a finished blade on show and sell it (80 % of its value) |
| `gate` | west, opening | iron gate | decoration (chained shut) |
| `rack` | west wall beside the gate | weapon rack | hang a finished blade (decoration, no gold) |

Each zone is `{x, z, radius, model}` — `x,z` is a standing spot in front of the prop, `radius` the reach.
The engine, not the caller, checks `dist(player, zone) ≤ radius` before any interaction.

## Loop

`order`: `E` hear an order (a blade of tier ≥ N) → `craft`: `E` take a bar → `forge`: `E` heat →
`craft`: hold `Space`, release in the band (repeat until the blade reaches the order's tier) → `order`: `E`
deliver, paid `pay + 90 × (tier − wanted)`. Side paths: `exchange` (tonic), `display` (sell), `rack` (hang).
Start gold 500; `R` restarts the run (same seed ⇒ same orders and rolls).

```
order(E accept) → craft(E pickup) → forge(E heat) → craft(Space strike, tier up?) → order(E deliver) → gold
                                            ↑ no, strike again / reheat ┘
```

Keys: `WASD` move · mouse / `←→↑↓` look · `E` use · `Space` strike · `R` restart.
URL: `?autostart` skips the title, `?seed=N` fixes orders and rolls, `?cam=x,y,z,yaw,pitch` is a debug camera.

## State contract (`window.__game.state`)

`fps, phase ('title'|'play'), gold, goldStart, ordersCompleted, player:{x,z,yaw,pitch,traveled},
held (null | {name,tier,struck,heat}), order, zones:{order,exchange,craft,forge,display,gate,rack},
interactLog:[{action,zone,dist,t}]` where `action ∈ accept(order) pickup(craft) heat(forge) strike(craft)
deliver(order) exchange display hang`. Also `charging, cursor, zoneLo, zoneHi, outcome, calib, displayed, hung, near, prompt`.

## Look

- ACES Filmic, exposure ~1.0, **one grade**: warm lift in shadows (+amber), slight desaturation of the
  greens, crushed blacks.
- Fog: exponential, near-black olive, so the room's far wall melts.
- Bloom: threshold high; only the blade glow, the fire and the lamp bloom.
- Vignette ~0.30, grain ~0.012, faint chromatic aberration on the glow.
- Materials: rough brick with mortar shadow, oily dark plank floor, worn bench top with burn marks,
  pitted iron for anvil/hammer. Metal is the only shiny thing.
- Text: title, one controls line, and small corner readouts (gold, tier pips). No plaque of stat rows.

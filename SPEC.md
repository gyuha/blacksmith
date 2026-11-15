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

Bench mode: fixed, ~0.55 m above the bench, 22° down-pitch, **50 mm-equiv, flat** (little distortion),
weapon bottom-left-to-centre, wall filling the top 2/3. Small camera kick (2-4 px) on impact, a slow
2-3 cm breathing drift so it is alive. Hub mode: same eye height, first person, 55 mm, gentle 40 ms
damped follow, no roll.

## Hero

Not a character — the **blade**. Readable at 100 px: a long pale steel blade with a single dark fuller,
brass guard, wrapped grip, lying at 18° on the bench. Its state is the whole readability problem: tier
is told by **glow** (none → thin white edge → warm gold → white-hot → prismatic), never by text.

## The one mechanic

**Strike and wager.** The bench is the slot: pay the forge tax, then swing.
- Hold `Space` to wind up; the hammer's arc is a metre. A **heat band** on the blade sweeps while you hold
  (the only gauge). Release inside the band and the roll is nudged toward success (*focused strike*);
  release late and you swing wide for a weaker roll.
- The die tumbles on the bench after each strike. Outcomes: **shatter** (blade lost), **damage** (tier −1),
  **hold** (no change, tax paid), **rise** (+1), **surge** (+2..+4, prismatic flare, the video's 대성공).
- Each blade has a limited number of strikes (pips on its plaque); when they run out it is spent and can
  only be sold.

## Key moment (must be in the take)

A **surge** on a high-tier blade: white-hot flare, prismatic spill across the bench, sparks, camera kick,
hammer held raised. The take must reach it.

## World

One room, three places:
- **Bench** (the still frame of the video) — the interaction.
- **Hearth** — arched stone furnace, fire in it; stand close to **re-heat** a damaged blade (restores 1 tier,
  costs gold).
- **Shelf** — lit cabinet with three blades of rising quality; walk up and `Space` to buy; the bought blade
  is carried to the bench.
Loop: buy → bench → strike → sell or re-heat → bigger blade. Goal: sell a blade at **+10 or better** (a
"masterwork"); that ends the run on a calm hearth shot. `R` restarts.

## Look

- ACES Filmic, exposure ~1.0, **one grade**: warm lift in shadows (+amber), slight desaturation of the
  greens, crushed blacks.
- Fog: exponential, near-black olive, so the room's far wall melts.
- Bloom: threshold high; only the blade glow, the fire and the lamp bloom.
- Vignette ~0.5, grain ~0.035, slight chromatic aberration on the glow.
- Materials: rough brick with mortar shadow, oily dark plank floor, worn bench top with burn marks,
  pitted iron for anvil/hammer. Metal is the only shiny thing.
- Text: title, one controls line, and small corner readouts (gold, tier pips). No plaque of stat rows.

## Players

One.

# THE TEMPER

A browser game rebuilt from `forgetax.mp4`, played with a keyboard, made with Three.js.
You stand at a forge bench. You lay a blade on the anvil, pay the forge's fee, and swing.
The number on the blade goes up — until it doesn't.

## What it was rebuilt from

`forgetax.mp4` is 91.8 minutes (5,509 s, 1280×720, 30 fps) of a released game, **FORGE TAX**.
`gameplay.txt` was not in the repo, so the design came from the video itself:

- `study/` — frames every second of the forge segment (source t=1730–1860), contact sheet, palette, cut report
  (`study_video.py` on a 130 s cut of the source).
- `refs/` — six full-res stills used as the style references for every generated image.
- `SPEC.md` — the written spec: camera, hero, mechanic, key moment, world, look.

The measured shape of the source: 80 % of the clip is a locked-off first-person bench view — blade diagonally in
the lower third, iron hammer entering from the right, dark olive brick wall with pinned calendars behind, a
translucent plaque floating over the bench. Palette: `#0e0e0d #161713 #24241a #353728 #464837 #555946` — olive
graphite and near-black, warm amber key light, crimson only on destruction, prismatic only on the best proc.

This game is an **original homage**, as agreed: same framing, palette, materials and gamble; its own world, item
names, gauge, room and no FORGE TAX branding or copied UI strings.

## Controls

| Key | Does |
|---|---|
| `Space` | start · buy / sell at the case · quench at the hearth |
| hold `Space` at the bench | wind the hammer up; a cursor sweeps the brass rule |
| release `Space` | strike. Release while the cursor is in the **green** and the roll is biased your way |
| `A` `D` / `←` `→` | step between hearth → bench → case |
| `R` | restart |
| gamepad | left stick steps, A acts |

**The loop.** Buy or take a blade → bench: each strike costs a small forge fee and rolls
shatter / damage / hold / rise / surge. A **surge** (the source's 대성공) jumps 2–3 tiers with a prismatic flare.
Only *failures* spend the blade's durability; the hearth can quench it for two more attempts.
Sell at the case. Sell a blade at **+10** and the run ends a masterwork.

**URL parameters:** `?autostart` skips the title, `?seed=N` fixes every roll, `?tier=N` (debug) starts holding a
blade at that tier, `?station=hearth|bench|shop`, `?top=1` (debug) overhead view.

**State contract** for the playtest: `window.__game.state` → phase, station, gold, held, tier, strikes, value,
tax, charging, cursor, zoneLo, zoneHi, focus, outcome, ended, fps.

## The look

ACES Filmic, one grade (lift + warm gain + 20 % harmonise toward luminance), bloom with a high threshold,
exponential fog, vignette, grain, and a slight chromatic fringe on the glow. The blade's glow is the readability
system: dull steel → warm edge → white-hot → prismatic. Only the blade, the fire and the lamp bloom.

## Assets — every one generated on fal

**Images were made with `openai/gpt-image-2.5/flare/edit`**, the model requested for this project (7 calls),
each one fed a frame of the video as a reference. Textures: brick, bench top, floor planks, pinned calendar.
Concepts: the blade, the hammer.

| Asset | Endpoint | Notes |
|---|---|---|
| `textures/brick.png` | `openai/gpt-image-2.5/flare/edit` | seamless, 3×3 tiling checked |
| `textures/benchwood.png` | `openai/gpt-image-2.5/flare/edit` | seamless |
| `textures/floorplank.png` | `openai/gpt-image-2.5/flare/edit` | seamless |
| `textures/paper_cal.png` | `openai/gpt-image-2.5/flare/edit` | transparent background, calendar with X-marks |
| `models/sword_concept.png` | `openai/gpt-image-2.5/flare/edit` | reference sheet for the blade |
| `models/hammer_concept.png` | `openai/gpt-image-2.5/flare/edit` | reference sheet for the hammer |
| `models/blade.glb` | `meshy/v7.1/image-to-3d` | 11.3k tris → decimated + JPEG-packed to 632 KB |
| `models/hammer.glb` | `meshy/v7.1/image-to-3d` | decimated to 586 KB |
| 12 sound effects | `fal-ai/elevenlabs/sound-effects/v2` | strike, whoosh, success, surge, shatter, damage, fire loop, coins, dice, select, purchase, room tone |
| `music/forge_theme.mp3` | `elevenlabs/music/v2.5` | instrumental, 90 s, low cello + zither |

Everything else is **built in Blender** (`build_props.py`) instead of bought: bench, anvil, arched hearth, ember
bed, shop cabinet, stool, oil lamp, coal bucket, tool rack — then exported to GLB. Earlier exploratory
`fal-ai/nano-banana-pro/edit` and `fal-ai/birefnet/v2` calls are still in `assets/*/fal_log.json`.

**Calls:** 30 logged fal jobs (+1 meshy job whose log line was lost when the tool timed out) — 12 SFX,
7 image edits, 5 early image calls, 3 cutouts, 2 image-to-3D, 1 music. Estimated cost ≈ **$4**, not metered.
One generated spark sprite and the vignette/grain are shader work, not assets.

## Proof it plays

- `takes/take_final.mp4` — **30.8 s, 1848 frames, 60.0 fps, 0 console errors**, recorded with
  `record_play.mjs` from `?autostart&seed=3` while `play.mjs` played it with the keyboard only.
- `takes/take_best10.mp4` — the liveliest 10 s window (`best_window.py`: 5.75 s → 15.75 s).
- The run, from the scenario's own log: surge on the first strike (+0 → +3), a **shatter** at 7.6 s, a fresh
  blade climbing 0 → 6, prismatic surges at 25.8 s (+6 → +9) and 28.5 s (+9 → +12), sold at ~31 s for
  **38,787 gold — a masterwork**.
- `pairs/` — three side-by-side pairs against the source, at the same spots each time:
  `pair_1757` (bench, blade resting vs. mid-strike), `pair_1800` (the blazing high-tier blade), `pair_1762`
  (the hearth). Left is always the video, right is the game.

## What still differs from the video

- **The blade model** is slimmer and paler than the source's broad steel blade with its dark fuller and
  red-brown grip; the fuller reads weakly.
- **The panel.** The source floats a big translucent plaque of stats and percentages. Deliberately not copied —
  the game shows one small brass gauge and two corner counters instead (gold, tier, strikes).
- **The hearth** is brick with a stylised arch and cone-shaped flames; the source's is cut grey stone with a
  heavy mantel, a bentwood chair and tools leaning beside it.
- **The shop** is one cabinet — two blades on its shelves, one on the counter; the source has a whole wall of
  lit display cases and a shopkeeper.
- **The room** is much smaller and emptier than the source's forge, which is dense with props.
- **Scale of the gamble**: one blade, three station cameras, ~30 s to a masterwork. The source is a
  92-minute economy with dice, boosters and repair items; those systems are not here.
- The grade is a little warmer and more saturated in the mid-tones than the source's olive graphite.

## Running it

```bash
cd /Users/gyuha/workspace/blacksmith
python3 -m http.server 8123          # any static server; 8000 was taken on this machine
open http://127.0.0.1:8123/index.html
```

Replay the take:

```bash
node .agents/skills/video-to-game/scripts/record_play.mjs \
  "http://127.0.0.1:8123/index.html?autostart&seed=3" play.mjs \
  -o takes/take.mp4 --seconds 40 --size 1280x720
```

Rebuild the Blender props: `blender --background --python build_props.py`
Shrink a generated mesh: `blender --background --python shrink.py -- in.glb out.glb`

## Tasks

`Taskfile.yml` (go-task) wraps everything above. `task` lists them, `task doctor` checks the toolchain.

```bash
task serve        # :8123
task verify       # headless load, fails on any console error
task shot QUERY='station=shop' OUT=probe/shop.png
task record       # re-film the take with seed 3 (SEED=, REC_SECONDS=, OUT= to override)
task best         # rank windows, cut takes/take_best10.mp4
task pairs        # rebuild the three side-by-side pairs
task props        # rebuild the Blender GLBs (skipped when up to date)
task shrink -- assets/models/in.glb assets/models/out.glb
task cost         # per-endpoint count of the logged fal calls
task study        # clip the forge segment, then frames + sheet + palette
```

`fal:image`, `fal:sfx` and `fal:mesh` are thin wrappers over `fal_asset.py` — they spend money, so they are not
wired into anything automatic.

## Files

```
index.html          the whole game (Three.js 0.160 from a pinned import map, no build step)
assets/textures/    fal images: brick, bench, floor, calendar
assets/models/      blade + hammer (fal image-to-3D) and 8 Blender props (GLB)
assets/sfx/         12 fal sound effects      assets/music/  1 fal track
play.mjs            the keyboard scenario       takes/        recordings
pairs/              side-by-side against the video
SPEC.md             the spec written before the code
build_props.py      procedural props       shrink.py   mesh decimation
shot.mjs            one-shot screenshot helper (dev)
Taskfile.yml        task runner: serve, verify, record, pairs, props, cost
study/ refs/        frames and stills taken from the video
```

`forgetax.mp4` stays as the source reference; `.gitignore` excludes `*.mp4`, so the takes are not tracked.

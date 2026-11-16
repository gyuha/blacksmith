# Room rebuild handoff

## Coordinate convention

The gameplay floor plan is centered at `(0, 0)` with `+x = east` and `+z = south`.
`y` is vertical. The exported GLBs are standard Blender Z-up meshes; the gameplay
coordinates below are placement coordinates, not a request to rotate the assets.
The room shell floor is `y = 0` and its footprint is approximately `10.0 x 8.0 m`.

| GLB | Local origin / dimensions (m) | Recommended placement | Interaction anchor(s) |
|---|---|---|---|
| `room_shell.glb` | origin at floor center `(0,0,0)`; `10.0 x 8.0 x 3.28` | `(0,0,0)` | room center `(0,0,0)`; gate opening centered on west edge |
| `room_order_window.glb` | base-centered; `2.82 x 2.05 x 2.35` | north wall, west bay `(-1.6,-3.45,0)` | order point `(-1.6,-3.05,1.0)` |
| `room_exchange.glb` | base-centered; `2.90 x 0.655 x 2.35` | north wall, east bay `(+1.6,-3.45,0)` | dial `(1.0,-3.05,0.4)`; slots `(1.6,-3.05,1.5)` |
| `room_anvil_bench.glb` | base-centered; `2.25 x 0.95 x 1.19` | east work zone `(3.15,0.3,0)` | strike point `(3.05,0.05,1.2)` |
| `room_furnace.glb` | base-centered; `1.95 x 0.84 x 2.36` | east wall, `(4.0,2.1,0)` | firebox `(4.0,1.65,0.4)`; re-heat point `(3.45,1.65,1.0)` |
| `room_display.glb` | base-centered; `2.95 x 0.62 x 2.28` | south wall `(0,3.35,0)` | purchase center `(0,3.0,1.1)` |
| `room_gate.glb` | base-centered; `2.42 x 0.30 x 2.43` | west opening `(-4.85,0,0)` | doorway `(-4.55,0,1.1)` |
| `room_weapon_rack.glb` | base-centered; `2.30 x 0.24 x 0.74` | west wall beside gate `(-4.65,-2.0,1.5)` | rack face `(-4.45,-2.0,1.8)` |
| `room_material_crate.glb` | base-centered; `1.02 x 0.80 x 0.88` | beside bench `(2.8,0.9,0)` | pickup center `(2.8,0.9,0.9)` |

`fire.glb` is an optional companion export for `room_furnace.glb`; its root mesh
is named `fire` and uses the emissive flame material. If the runtime wants one
draw call, place it at the furnace firebox anchor and merge it at import time.

## Layout intent

- North: order window and the three-slot exchange panel.
- East: anvil/workbench and arched brick furnace.
- South: three-column lit display cabinet.
- West: iron gate opening and wall weapon rack.
- The crate is deliberately a generic material container, not a branded prop.

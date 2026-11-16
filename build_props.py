import bpy, bmesh, math, os
from mathutils import Vector

OUT = "/Users/gyuha/workspace/blacksmith/assets/models"
TEX = "/Users/gyuha/workspace/blacksmith/assets/textures"

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(name, color, rough=0.8, metal=0.0, tex=None, emit=None, emit_strength=0.0, uv_scale=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1) if tex else (*color, 1)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metal
    if tex:
        img = bpy.data.images.load(os.path.join(TEX, tex))
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = img
        n.location = (-500, 0)
        mapn = nt.nodes.new('ShaderNodeMapping'); mapn.location = (-700, 0)
        if isinstance(uv_scale, (tuple, list)):
            map_scale = (*uv_scale, 1) if len(uv_scale) == 2 else tuple(uv_scale)
        else:
            map_scale = (uv_scale, uv_scale, 1)
        mapn.inputs['Scale'].default_value = map_scale
        tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-900, 0)
        nt.links.new(tc.outputs['UV'], mapn.inputs['Vector'])
        nt.links.new(mapn.outputs['Vector'], n.inputs['Vector'])
        nt.links.new(n.outputs['Color'], bsdf.inputs['Base Color'])
    if emit:
        bsdf.inputs['Emission Color'].default_value = (*emit, 1)
        bsdf.inputs['Emission Strength'].default_value = emit_strength
    return m

def box(name, size, loc, mat=None, bevel=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0], size[1], size[2])  # cube size=1 spans 1 unit each way
    bpy.ops.object.transform_apply(scale=True)
    if bevel > 0:
        b = o.modifiers.new('bev', 'BEVEL'); b.width = bevel; b.segments = 2
        bpy.ops.object.modifier_apply(modifier=b.name)
    if mat: o.data.materials.append(mat)
    return o

def cyl(name, r, depth, loc, mat=None, verts=24, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    if mat: o.data.materials.append(mat)
    return o

def join(objs, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    o = bpy.context.object; o.name = name
    return o

def drop_to_floor(o):
    """origin at base centre, base on y=0 (world z=0)"""
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.location.z -= o.dimensions.z / 2

def export(o, name):
    out_path = os.path.join(OUT, name + '.glb')
    if os.path.exists(out_path):
        print('skip existing', name)
        return
    drop_to_floor(o)
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, name + '.glb'),
                              export_format='GLB', use_selection=True,
                              export_apply=True, export_yup=True)
    print('wrote', name, tuple(round(d, 2) for d in o.dimensions))

reset()

WOOD   = mat('wood',   (0.055, 0.042, 0.032), 0.72, 0.0, tex='benchwood.png', uv_scale=2.0)
ROUGHW = mat('roughwood', (0.032, 0.026, 0.020), 0.88)
# The source tile contains roughly 4 bricks across by 10 courses.  Repeating
# it 10x8 over the wall keeps a brick close to 0.25 x 0.065 m at room scale.
BRICK  = mat('brick',  (0.09, 0.075, 0.06), 0.9, 0.0, tex='brick.png', uv_scale=(10.0, 8.0))
IRON   = mat('iron',   (0.055, 0.05, 0.048), 0.42, 0.85)
DARKIRON = mat('darkiron', (0.028, 0.026, 0.025), 0.55, 0.8)
BRASS  = mat('brass',  (0.32, 0.21, 0.07), 0.35, 0.9)
LEATHER= mat('leather',(0.030, 0.019, 0.013), 0.72)
EMBER  = mat('ember',  (1.0, 0.35, 0.06), 0.6, 0.0, emit=(1.0, 0.36, 0.08), emit_strength=3.2)
FLAME  = mat('flame',  (1.0, 0.55, 0.15), 0.5, 0.0, emit=(1.0, 0.46, 0.10), emit_strength=4.0)
GLASS  = mat('glass',  (1.0, 0.82, 0.45), 0.3, 0.0, emit=(1.0, 0.78, 0.4), emit_strength=7.0)
COAL   = mat('coal',   (0.02, 0.02, 0.021), 0.75)

# ---------------- workbench ----------------
parts = []
parts.append(box('top', (1.9, 0.95, 0.09), (0, 0, 0.83), WOOD, bevel=0.012))
parts.append(box('rail', (1.9, 0.10, 0.05), (0, -0.44, 0.90), LEATHER, bevel=0.02))
for sx in (-1, 1):
    for sy in (-1, 1):
        parts.append(box('leg', (0.10, 0.10, 0.78), (sx * 0.82, sy * 0.36, 0.39), ROUGHW))
parts.append(box('apron', (1.72, 0.06, 0.12), (0, 0.36, 0.70), ROUGHW))
parts.append(box('shelf', (1.6, 0.72, 0.05), (0, 0.02, 0.22), ROUGHW))
parts.append(box('vise', (0.22, 0.16, 0.13), (-0.72, -0.30, 0.94), DARKIRON, bevel=0.01))
export(join(parts, 'bench'), 'bench')

# ---------------- anvil ----------------
a = []
a.append(box('abase', (0.46, 0.30, 0.06), (0, 0, 0.03), DARKIRON, bevel=0.008))
a.append(box('awaist', (0.24, 0.20, 0.16), (0, 0, 0.14), DARKIRON, bevel=0.01))
a.append(box('abody', (0.46, 0.24, 0.10), (0, 0, 0.27), IRON, bevel=0.02))
a.append(box('aface', (0.52, 0.26, 0.035), (0, 0, 0.335), IRON, bevel=0.008))
a.append(box('ahorn', (0.20, 0.10, 0.06), (0.33, 0, 0.32), IRON, bevel=0.015, rot=(0, 0, 0)))
for k in (-1, 1):
    a.append(box('aheel', (0.10, 0.14, 0.07), (-0.27, 0, 0.315), IRON, bevel=0.012))
export(join(a, 'anvil'), 'anvil')

# ---------------- hearth (arched stone furnace) ----------------
W, H, D = 1.7, 1.95, 0.58
walls = []
walls.append(box('back', (W, 0.12, H), (0, D / 2 - 0.06, H / 2)))
for sx in (-1, 1):
    walls.append(box('side', (0.34, D, H), (sx * (W / 2 - 0.17), 0, H / 2)))
walls.append(box('lintel', (W, D, 0.62), (0, 0, H - 0.31)))
walls.append(box('sill', (W, D, 0.14), (0, 0, 0.07)))
# arch voussoirs
for i in range(11):
    ang = math.pi * (i + 0.5) / 11.0
    r = 0.50
    x = math.cos(ang) * r
    z = 1.24 + math.sin(ang) * r
    walls.append(box('arch%d' % i, (0.19, 0.13, 0.20), (x, -D / 2 + 0.065, z),
                     rot=(0, -ang - math.pi / 2, 0)))
h = join(walls, 'hearth')
h.data.materials.clear()
h.data.materials.append(BRICK)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')
export(h, 'hearth')

fire = []
# ember bed across the firebox floor
import random as _r
_r.seed(7)
for i in range(9):
    x = -0.40 + i * 0.10 + (_r.random() - 0.5) * 0.03
    y = -0.16 + _r.random() * 0.30
    s = 0.11 + _r.random() * 0.05
    fire.append(box('em%d' % i, (s, s, 0.055 + _r.random() * 0.03), (x, y, 0.06), EMBER, bevel=0.012))
# charred logs
for i in range(3):
    fire.append(box('log%d' % i, (0.62, 0.09, 0.09), (0.0, -0.10 + i * 0.11, 0.13 + i * 0.035),
                    COAL, bevel=0.02, rot=(0, 0, (i - 1) * 0.18)))
# flames rising behind the logs
for i in range(13):
    x = -0.38 + i * 0.060 + (_r.random() - 0.5) * 0.03
    y = -0.08 + _r.random() * 0.20
    h = 0.22 + _r.random() * 0.40
    w = 0.035 + _r.random() * 0.030
    bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=w, radius2=0.0, depth=h,
                                    location=(x, y, 0.14 + h / 2),
                                    rotation=(0, 0, _r.random() * 1.5))
    fl = bpy.context.object; fl.name = 'fl%d' % i
    fl.data.materials.append(FLAME)
    fire.append(fl)
export(join(fire, 'hearth_fire'), 'hearth_fire')

# ---------------- shop cabinet ----------------
c = []
cw, ch, cd = 1.8, 1.95, 0.48
c.append(box('cback', (cw, 0.08, ch), (0, cd / 2, ch / 2), ROUGHW))
for sx in (-1, 1):
    c.append(box('cside', (0.09, cd, ch), (sx * (cw / 2 - 0.045), 0, ch / 2), ROUGHW))
c.append(box('ctop', (cw, cd + 0.06, 0.10), (0, 0, ch - 0.05), ROUGHW, bevel=0.008))
c.append(box('cbase', (cw, cd + 0.06, 0.14), (0, 0, 0.07), ROUGHW, bevel=0.008))
shelf_z = [0.62, 1.10, 1.58]
for z in shelf_z:
    c.append(box('cshelf', (cw - 0.16, cd - 0.05, 0.04), (0, 0, z), ROUGHW))
for sx in (-0.60, 0.0, 0.60):
    c.append(box('cdiv', (0.04, cd - 0.06, ch - 0.30), (sx, 0, ch / 2), ROUGHW))
c.append(box('ccounter', (cw + 0.10, cd + 0.30, 0.12), (0, -cd / 2 - 0.10, 0.86), ROUGHW, bevel=0.01))
export(join(c, 'cabinet'), 'cabinet')

# ---------------- stool ----------------
s = [box('seat', (0.42, 0.34, 0.06), (0, 0, 0.44), WOOD, bevel=0.012)]
for sx in (-1, 1):
    for sy in (-1, 1):
        s.append(box('sleg', (0.055, 0.055, 0.42), (sx * 0.15, sy * 0.12, 0.21), ROUGHW))
s.append(box('sbrace', (0.34, 0.045, 0.045), (0, 0, 0.14), ROUGHW))
export(join(s, 'stool'), 'stool')

# ---------------- oil lamp ----------------
l = []
l.append(cyl('lbase', 0.10, 0.03, (0, 0, 0.015), BRASS))
l.append(cyl('lbody', 0.075, 0.11, (0, 0, 0.09), BRASS))
l.append(cyl('lneck', 0.03, 0.05, (0, 0, 0.17), BRASS))
l.append(box('lglobe', (0.15, 0.15, 0.20), (0, 0, 0.28), GLASS, bevel=0.05))
l.append(cyl('lcap', 0.055, 0.03, (0, 0, 0.395), BRASS))
l.append(cyl('lhandle', 0.055, 0.012, (0.11, 0, 0.26), BRASS, rot=(0, math.pi / 2, 0)))
export(join(l, 'lamp'), 'lamp')

# ---------------- coal bucket ----------------
b = []
b.append(cyl('bbody', 0.17, 0.30, (0, 0, 0.15), DARKIRON, verts=28))
b.append(cyl('brim', 0.185, 0.03, (0, 0, 0.30), IRON, verts=28))
for i in range(6):
    ang = i * 1.05
    b.append(box('cl%d' % i, (0.09, 0.09, 0.07), (0.07 * math.cos(ang), 0.07 * math.sin(ang), 0.335), COAL, bevel=0.015))
export(join(b, 'bucket'), 'bucket')

# ---------------- wall tool rack ----------------
t = []
t.append(box('board', (1.25, 0.05, 0.62), (0, 0, 0.31), ROUGHW, bevel=0.006))
for x in (-0.45, -0.15, 0.15, 0.45):
    t.append(cyl('peg%d' % int(x * 10), 0.014, 0.10, (x, -0.06, 0.44), DARKIRON, rot=(math.pi / 2, 0, 0)))
# hanging tongs silhouette
t.append(box('tong_a', (0.03, 0.02, 0.42), (-0.15, -0.07, 0.22), DARKIRON))
t.append(box('tong_b', (0.03, 0.02, 0.42), (-0.11, -0.07, 0.22), DARKIRON))
t.append(box('tong_j', (0.06, 0.02, 0.03), (-0.13, -0.07, 0.42), DARKIRON))
export(join(t, 'toolrack'), 'toolrack')

print('ALL DONE')

# ---------------------------------------------------------------------------
# Room rebuild set.  These are intentionally separate, game-facing assets;
# the older study props above remain untouched and are never overwritten.
# Blender space is Z-up.  The handoff note uses gameplay X/Z for the floor
# plan (+X east, +Z south) and calls out the conversion explicitly.
# Export manifest (kept explicit for asset handoff checks):
# room_shell.glb room_order_window.glb room_exchange.glb room_anvil_bench.glb
# room_furnace.glb room_display.glb room_gate.glb room_weapon_rack.glb
# room_material_crate.glb

def room_join(parts, name, material=None):
    o = join(parts, name)
    if material:
        o.data.materials.clear(); o.data.materials.append(material)
    return o

def room_shell():
    p = []
    p.append(box('floor', (10.0, 8.0, 0.16), (0, 0, 0.08), mat('floor_olive', (0.075, 0.072, 0.055), 0.82, tex='floorplank.png', uv_scale=1.2), bevel=0.01))
    # North, east and south walls; west wall is split around the gate opening.
    p += [box('north_wall', (10.0, 0.24, 3.2), (0, -3.88, 1.68), BRICK),
          box('east_wall', (0.24, 7.76, 3.2), (4.88, 0, 1.68), BRICK),
          box('south_wall', (10.0, 0.24, 3.2), (0, 3.88, 1.68), BRICK),
          box('west_left', (0.24, 3.55, 3.2), (-4.88, -2.22, 1.68), BRICK),
          box('west_right', (0.24, 3.55, 3.2), (-4.88, 2.22, 1.68), BRICK),
          box('west_header', (0.24, 2.45, 0.82), (-4.88, 0, 2.87), BRICK)]
    for x in (-3.4, 0, 3.4):
        p.append(box('beam', (0.18, 7.7, 0.16), (x, 0, 3.16), DARKIRON, bevel=0.02))
    return room_join(p, 'room_shell')

def room_order_window():
    p = [box('counter', (2.82, 0.82, 0.18), (0, 0, 0.92), WOOD, bevel=0.03),
         box('sill', (2.82, 0.16, 1.95), (0, 0.32, 1.60), BRICK),
         box('leftpost', (0.20, 0.20, 2.35), (-1.31, 0.29, 1.65), IRON),
         box('rightpost', (0.20, 0.20, 2.35), (1.31, 0.29, 1.65), IRON)]
    for x in (-1.00, -0.67, -0.33, 0, 0.33, 0.67, 1.00):
        p.append(cyl('bar', 0.038, 2.05, (x, 0.16, 1.62), IRON, verts=12, rot=(math.pi/2, 0, 0)))
    p.append(box('lintel', (2.82, 0.20, 0.18), (0, 0.29, 2.72), BRASS, bevel=0.02))
    return room_join(p, 'room_order_window')

def room_exchange():
    p = [box('backplate', (2.82, 0.12, 2.28), (0, 0, 1.15), DARKIRON, bevel=0.03),
         box('toprail', (2.90, 0.18, 0.12), (0, -0.01, 2.30), BRASS),
         box('counter', (2.90, 0.45, 0.16), (0, -0.20, 0.20), WOOD, bevel=0.025)]
    for x in (-0.92, 0, 0.92):
        p += [box('slot', (0.74, 0.20, 1.10), (x, -0.12, 1.46), GLASS, bevel=0.05),
              box('slotframe', (0.84, 0.08, 1.20), (x, -0.22, 1.46), BRASS, bevel=0.025)]
    p.append(box('counterbox', (0.70, 0.24, 0.28), (0.84, -0.42, 0.42), DARKIRON, bevel=0.03))
    for x in (0.70, 0.84, 0.98):
        p.append(box('digit', (0.06, 0.03, 0.12), (x, -0.56, 0.44), EMBER, bevel=0.01))
    p.append(cyl('dial', 0.18, 0.08, (-0.90, -0.42, 0.42), BRASS, verts=24, rot=(math.pi/2, 0, 0)))
    p.append(box('dialmark', (0.03, 0.02, 0.15), (-0.90, -0.49, 0.53), EMBER, bevel=0.005))
    return room_join(p, 'room_exchange')

def room_anvil_bench():
    b = []
    b.append(box('bench_top', (2.25, 0.95, 0.12), (0, 0, 0.88), WOOD, bevel=0.025))
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.append(box('leg', (0.12, 0.12, 0.82), (sx*0.95, sy*0.34, 0.43), ROUGHW))
    b.append(box('lower_shelf', (1.85, 0.70, 0.06), (0, 0.03, 0.25), ROUGHW))
    b.append(box('anvil_base', (0.50, 0.34, 0.07), (0.52, -0.08, 0.96), DARKIRON, bevel=0.01))
    b.append(box('anvil_body', (0.30, 0.24, 0.16), (0.52, -0.08, 1.06), DARKIRON, bevel=0.018))
    b.append(box('anvil_face', (0.58, 0.28, 0.08), (0.52, -0.08, 1.17), IRON, bevel=0.02))
    b.append(box('horn', (0.22, 0.15, 0.07), (0.86, -0.08, 1.16), IRON, bevel=0.03))
    return room_join(b, 'room_anvil_bench')

def room_furnace():
    p = [box('back', (1.95, 0.18, 2.35), (0, 0.28, 1.18), BRICK),
         box('left', (0.38, 0.75, 2.35), (-0.78, 0, 1.18), BRICK),
         box('right', (0.38, 0.75, 2.35), (0.78, 0, 1.18), BRICK),
         box('lintel', (1.95, 0.75, 0.52), (0, 0, 2.10), BRICK),
         box('sill', (1.95, 0.75, 0.15), (0, 0, 0.075), BRICK)]
    for i in range( nine := 9):
        ang = math.pi * (i + 0.5) / nine
        p.append(box('voussoir', (0.22, 0.16, 0.24), (math.cos(ang)*0.55, -0.39, 1.48 + math.sin(ang)*0.55), BRICK, bevel=0.01, rot=(0, -ang-math.pi/2, 0)))
    f = [box('coalbed', (1.10, 0.42, 0.08), (0, -0.25, 0.18), COAL, bevel=0.03)]
    for i, x in enumerate((-0.42, -0.21, 0, 0.21, 0.42)):
        f.append(box('ember', (0.16, 0.16, 0.07), (x, -0.25, 0.27 + (i%2)*0.03), EMBER, bevel=0.02))
    for i, x in enumerate((-0.40, -0.20, 0, 0.20, 0.40)):
        bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.09, radius2=0.0, depth=0.42 + (i%3)*0.09, location=(x, -0.28, 0.50 + (i%3)*0.03))
        fl = bpy.context.object; fl.name = 'flame'; fl.data.materials.append(FLAME); f.append(fl)
    return room_join(p, 'room_furnace'), room_join(f, 'fire')

def room_display():
    p = [box('back', (2.80, 0.12, 2.25), (0, 0.22, 1.13), ROUGHW),
         box('top', (2.95, 0.60, 0.12), (0, 0, 2.22), WOOD, bevel=0.02),
         box('base', (2.95, 0.60, 0.16), (0, 0, 0.08), WOOD, bevel=0.02)]
    for x in (-1.36, 1.36): p.append(box('side', (0.12, 0.60, 2.18), (x, 0, 1.15), WOOD))
    for x in (-0.46, 0.46): p.append(box('divider', (0.08, 0.50, 2.12), (x, 0, 1.14), WOOD))
    for z in (0.72, 1.40): p.append(box('shelf', (2.65, 0.48, 0.06), (0, -0.02, z), WOOD))
    for x in (-0.92, 0, 0.92): p.append(box('blade_glow', (0.10, 0.05, 0.42), (x, -0.30, 0.40), GLASS, bevel=0.02))
    return room_join(p, 'room_display')

def room_gate():
    p = [box('leftpost', (0.16, 0.30, 2.35), (-1.13, 0, 1.18), IRON),
         box('rightpost', (0.16, 0.30, 2.35), (1.13, 0, 1.18), IRON),
         box('top', (2.42, 0.30, 0.16), (0, 0, 2.36), IRON)]
    for x in (-0.85, -0.42, 0, 0.42, 0.85): p.append(cyl('bar', 0.045, 2.15, (x, 0, 1.22), IRON, verts=12))
    return room_join(p, 'room_gate')

def room_weapon_rack():
    p = [box('board', (2.30, 0.10, 0.72), (0, 0, 0.40), ROUGHW, bevel=0.02)]
    for x in (-0.85, -0.28, 0.28, 0.85):
        p.append(cyl('peg', 0.035, 0.18, (x, -0.10, 0.58), IRON, verts=12, rot=(math.pi/2, 0, 0)))
        p.append(box('hanging_tool', (0.07, 0.04, 0.52), (x, -0.15, 0.28), DARKIRON, bevel=0.02, rot=(0, 0, (x*0.15))))
    return room_join(p, 'room_weapon_rack')

def room_material_crate():
    p = [box('crate', (0.95, 0.75, 0.62), (0, 0, 0.31), WOOD, bevel=0.035)]
    for x in (-0.36, 0.36): p.append(box('band', (0.07, 0.80, 0.68), (x, 0, 0.34), IRON, bevel=0.01))
    for y in (-0.27, 0.27): p.append(box('band', (1.02, 0.07, 0.68), (0, y, 0.34), IRON, bevel=0.01))
    p += [cyl('ingot', 0.11, 0.30, (-0.20, -0.08, 0.71), BRASS, verts=6, rot=(0.18, 0.1, 0.25)),
          cyl('ore', 0.13, 0.22, (0.18, 0.10, 0.68), IRON, verts=7, rot=(0.2, 0.1, -0.3))]
    return room_join(p, 'room_material_crate')

def render_north_preview():
    # Arrange the two north-wall assets for a quick handoff render without
    # changing their exported local origins.
    keep = {'room_shell', 'room_order_window', 'room_exchange'}
    for o in bpy.context.scene.objects:
        o.hide_render = o.name not in keep
    bpy.data.objects['room_order_window'].location = (-1.55, -3.42, 0)
    bpy.data.objects['room_exchange'].location = (1.55, -3.42, 0)
    bpy.ops.object.camera_add(location=(0, 2.7, 1.65))
    cam = bpy.context.object
    cam.name = 'north_preview_camera'
    target = Vector((0, -3.45, 1.35))
    cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = 46
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type='AREA', location=(0, -1.1, 3.0))
    key = bpy.context.object; key.name = 'north_preview_key'; key.data.energy = 950; key.data.shape = 'RECTANGLE'; key.data.size = 5.5
    key.rotation_euler = (Vector((0, -3.5, 1.0)) - key.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.ops.object.light_add(type='AREA', location=(0, -3.0, 1.3))
    fill = bpy.context.object; fill.name = 'north_preview_fill'; fill.data.energy = 300; fill.data.size = 3.0
    fill.rotation_euler = (Vector((0, -3.8, 1.3)) - fill.location).to_track_quat('-Z', 'Y').to_euler()
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 900; scene.render.resolution_y = 600; scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = '/Users/gyuha/workspace/blacksmith/refs/room_preview_north.png'
    if scene.world is None:
        scene.world = bpy.data.worlds.new('north_preview_world')
    scene.world.color = (0.008, 0.009, 0.007)
    bpy.ops.render.render(write_still=True)
    print('wrote refs/room_preview_north.png')

def report_room_contracts():
    shell = bpy.data.objects['room_shell']
    inner = []
    for v in shell.data.vertices:
        p = shell.matrix_world @ v.co
        if -4.4 < p.x < 4.4 and -3.4 < p.y < 3.4 and 0.2 <= p.z <= 2.0:
            inner.append(p)
    print('MEASURE shell_inner_vertices_0.6m z0.2-2.0 =', len(inner))
    for name in ('room_order_window', 'room_exchange'):
        o = bpy.data.objects[name]
        print('MEASURE', name, 'bbox_wdh=', tuple(round(v, 3) for v in (o.dimensions.x, o.dimensions.y, o.dimensions.z)))

export(room_shell(), 'room_shell')
export(room_order_window(), 'room_order_window')
export(room_exchange(), 'room_exchange')
export(room_anvil_bench(), 'room_anvil_bench')
furnace, fire = room_furnace()
export(furnace, 'room_furnace')
export(fire, 'fire')
export(room_display(), 'room_display')
export(room_gate(), 'room_gate')
export(room_weapon_rack(), 'room_weapon_rack')
export(room_material_crate(), 'room_material_crate')
render_north_preview()
report_room_contracts()
print('ROOM SET DONE')

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
        mapn.inputs['Scale'].default_value = (uv_scale, uv_scale, 1)
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
BRICK  = mat('brick',  (0.09, 0.075, 0.06), 0.9, 0.0, tex='brick.png', uv_scale=1.6)
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

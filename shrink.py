import bpy, sys, os
src, dst = sys.argv[-2], sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
for img in list(bpy.data.images):
    if img.size[0] > 1024:
        img.scale(1024, 1024)
for o in list(bpy.data.objects):
    if o.type == 'MESH':
        bpy.context.view_layer.objects.active = o
        m = o.modifiers.new('dec', 'DECIMATE')
        m.ratio = 0.45
        bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.export_scene.gltf(filepath=dst, export_format='GLB', export_image_format='JPEG',
                          export_jpeg_quality=88, export_apply=True)
print('shrank', src, '->', dst, os.path.getsize(dst)//1024, 'KB')

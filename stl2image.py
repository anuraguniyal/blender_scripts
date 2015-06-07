"""
stl2image script takes a stl file and renders it into a image file e.g.
/Applications/Blender/blender.app/Contents/MacOS/blender --python stl2image.py -- ~/Downloads/bearing.stl /tmp/b8.png
"""

import sys
import math

import bpy
import mathutils

def set_camera_lights(target):
    # set the origin to bounding box center
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    # move camera away from target we want to shoot buggest side so we should move away in direction of shortest side
    min_d = min(target.dimensions)
    # move camera by double of max dimension
    cam_move = max(target.dimensions)*1.5
    obj_rot = math.radians(20) # how much to rotate object
    if target.dimensions.x == min_d:
        cam_location = (cam_move, 0, 0)
        lamp_location = (cam_move*1.5, 0, 0)
        cam_rotation = (0.0, math.radians(90), 0.0)
        target_rotation = (0.0, obj_rot, obj_rot)
    elif target.dimensions.y == min_d:
        cam_location = (0, cam_move, 0)
        lamp_location = (0, cam_move*1.5, 0)
        cam_rotation = (-math.radians(90), 0.0, 0.0)
        target_rotation = (obj_rot, 0.0, obj_rot)
    else:
        cam_location = (0, 0, cam_move)
        lamp_location = (0, 0, cam_move*1.5)
        cam_rotation = (0.0, 0.0, 0.0)
        target_rotation = (obj_rot, obj_rot, 0.0)

    # rotate object a bit
    target.rotation_euler = target_rotation

    camera = bpy.data.objects['Camera']
    # set camera far away from the biggest face of bounding box
    camera.location = target.location + mathutils.Vector(cam_location)
    camera.rotation_euler = cam_rotation
    # set light behind camera
    bpy.data.objects['Lamp'].location = target.location + mathutils.Vector(lamp_location)
    # incease dra size for debugging and viewing in gui mode
    bpy.data.cameras['Camera'].draw_size = target.dimensions.length/2
    # set big enough clip
    bpy.data.cameras['Camera'].clip_end = cam_move+target.dimensions.length+100
    bpy.data.lamps['Lamp'].type = 'HEMI' #SUN is also good
    # set background color to white
    bpy.data.worlds['World'].horizon_color = (1, 1, 1)

def import_stl(stlfile):
    """
    import stl file and return the object
    """
    bpy.ops.import_mesh.stl(filepath=stlfile)
    # blender will import object with name=filename but capitalized
    # we can rely on that or for now imported object should be active
    target = bpy.context.selected_objects[0]
    return target

def save_image(imagefile):
    # set resolution and make x=y to have square view
    scene = bpy.data.scenes['Scene']
    scene.render.resolution_x = scene.render.resolution_y = 1080

    bpy.data.scenes['Scene'].render.filepath = imagefile
    bpy.ops.render.render( write_still=True )

stlfile = sys.argv[-2]
imagefile = sys.argv[-1]

target = import_stl(stlfile)
set_camera_lights(target)
save_image(imagefile)

#bpy.ops.wm.quit_blender()

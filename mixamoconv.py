# -*- coding: utf-8 -*-

'''
    Copyright (C) 2017  Enzio Probst
  
    Created by Enzio Probst

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import bpy
from bpy_types import Object
import os
import re
import logging

log = logging.getLogger(__name__)

def remove_namespace(s=''):
    """function for removing all namespaces from strings, objects or even armatrure bones"""

    if type(s) == str:
        i = re.search(r"[:_]", s[::-1])
        if i:
            return s[-(i.start())::]
        else:
            return s

    elif type(s) == Object:
        if s.type == 'ARMATURE':
            for bone in s.data.bones:
                bone.name = remove_namespace(bone.name)
        s.name = remove_namespace(s.name)
        return 1
    return -1


def rename_bones(s='', t='unreal'):
    """function for renaming the armature bones to a target skeleton"""
    unreal = {
        'root': 'Root',
        'Hips': 'Pelvis',
        'Spine': 'spine_01',
        'Spine1': 'spine_02',
        'Spine2': 'spine_03',
        'LeftShoulder': 'clavicle_l',
        'LeftArm': 'upperarm_l',
        'LeftForeArm': 'lowerarm_l',
        'LeftHand': 'hand_l',
        'RightShoulder': 'clavicle_r',
        'RightArm': 'upperarm_r',
        'RightForeArm': 'lowerarm_r',
        'RightHand': 'hand_r',
        'Neck1': 'neck_01',
        'Neck': 'neck_01',
        'Head': 'head',
        'LeftUpLeg': 'thigh_l',
        'LeftLeg': 'calf_l',
        'LeftFoot': 'foot_l',
        'RightUpLeg': 'thigh_r',
        'RightLeg': 'calf_r',
        'RightFoot': 'foot_r',
        'LeftHandIndex1': 'index_01_l',
        'LeftHandIndex2': 'index_02_l',
        'LeftHandIndex3': 'index_03_l',
        'LeftHandMiddle1': 'middle_01_l',
        'LeftHandMiddle2': 'middle_02_l',
        'LeftHandMiddle3': 'middle_03_l',
        'LeftHandPinky1': 'pinky_01_l',
        'LeftHandPinky2': 'pinky_02_l',
        'LeftHandPinky3': 'pinky_03_l',
        'LeftHandRing1': 'ring_01_l',
        'LeftHandRing2': 'ring_02_l',
        'LeftHandRing3': 'ring_03_l',
        'LeftHandThumb1': 'thumb_01_l',
        'LeftHandThumb2': 'thumb_02_l',
        'LeftHandThumb3': 'thumb_03_l',
        'LeftHand': 'lowerarm_twist_01_l',
        'LeftArm': 'upperarm_twist_01_l',
        'RightHandIndex1': 'index_01_r',
        'RightHandIndex2': 'index_02_r',
        'RightHandIndex3': 'index_03_r',
        'RightHandMiddle1': 'middle_01_r',
        'RightHandMiddle2': 'middle_02_r',
        'RightHandMiddle3': 'middle_03_r',
        'RightHandPinky1': 'pinky_01_r',
        'RightHandPinky2': 'pinky_02_r',
        'RightHandPinky3': 'pinky_03_r',
        'RightHandRing1': 'ring_01_r',
        'RightHandRing2': 'ring_02_r',
        'RightHandRing3': 'ring_03_r',
        'RightHandThumb1': 'thumb_01_r',
        'RightHandThumb2': 'thumb_02_r',
        'RightHandThumb3': 'thumb_03_r',
        'RightHand': 'lowerarm_twist_01_r',
        'RightArm': 'upperarm_twist_01_r',
        'LeftToeBase': 'ball_l',
        'LeftUpLeg': 'thigh_twist_01_l',
        'RightToeBase': 'ball_r',
        'RightUpLeg': 'thigh_twist_01_r'
    }
    schema = {'unreal': unreal }
    if type(s) == str:
        i = schema[t].get(s)
        if i:
            return i
        else:
            log.warning('WARNING %s bone is missing', s)
            return s
    elif type(s) == Object:
        if s.type == 'ARMATURE':
            for bone in s.data.bones:
                bone.name = rename_bones(remove_namespace(bone.name))
        s.name = rename_bones(s.name)
        return 1
    return -1

def apply_restoffset(armature, hipbone, restoffset):
    """function to apply restoffset to rig, should be used if rest-/bindpose does not stand on ground with feet"""
    # apply rest offset to restpose
    bpy.context.scene.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.transform.translate(value=restoffset, constraint_axis=(False, False, False),
                                constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED',
                                proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.object.mode_set(mode='OBJECT')

    # apply restoffset to animation of hip
    restoffset_local = (restoffset[0], restoffset[2], -restoffset[1])
    for axis in range(3):
        fcurve = armature.animation_data.action.fcurves.find("pose.bones[\"" + hipbone.name + "\"].location", axis)
        for pi in range(len(fcurve.keyframe_points)):
            fcurve.keyframe_points[pi].co.y -= restoffset_local[axis] / armature.scale.x
    return 1


def apply_kneefix(armature, offset, bonenames=['RightUpLeg', 'LeftUpLeg']):
    """workaround for flickering knees after export (moves joints in restpose by offset, can break animation)"""
    bpy.context.scene.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    for name in bonenames:
        armature.data.edit_bones[name].select_tail = True
    bpy.ops.transform.translate(value=offset, proportional='DISABLED', release_confirm=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    return 1


def hip_to_root(armature, use_x=True, use_y=True, use_z=True, on_ground=True, scale=1.0, restoffset=(0, 0, 0),
                hipname='', fixbind=True, apply_rotation=True, apply_scale=False):
    """function to bake hipmotion to RootMotion in MixamoRigs"""

    root = armature
    root.name = "root"
    framerange = root.animation_data.action.frame_range

    for hipname in ('Hips', 'mixamorig:Hips', 'mixamorig_Hips', hipname):
        hips = root.pose.bones.get(hipname)
        if hips != None:
            break
    if hips == None:
        return -1

    # Scale by ScaleFactor
    if scale != 1.0:
        for i in range(3):
            fcurve = root.animation_data.action.fcurves.find('scale', i)
            if fcurve != None:
                root.animation_data.action.fcurves.remove(fcurve)
        root.scale *= scale

    # apply restoffset to restpose and correct animation
    apply_restoffset(root, hips, restoffset)

    hiplocation_world = root.matrix_local * hips.bone.head
    z_offset = hiplocation_world[2]

    # Create helper to bake the root motion
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0), layers=(
    True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
    False, False, False, False))
    rootBaker = bpy.context.object
    rootBaker.name = "rootBaker"

    if use_z:
        print("using z")
        bpy.ops.object.constraint_add(type='COPY_LOCATION')
        bpy.context.object.constraints["Copy Location"].name = "Copy Z_Loc"
        bpy.context.object.constraints["Copy Z_Loc"].target = root
        bpy.context.object.constraints["Copy Z_Loc"].subtarget = hips.name
        bpy.context.object.constraints["Copy Z_Loc"].use_x = False
        bpy.context.object.constraints["Copy Z_Loc"].use_y = False
        bpy.context.object.constraints["Copy Z_Loc"].use_z = True
        bpy.context.object.constraints["Copy Z_Loc"].use_offset = True
        if on_ground:
            print("using on ground")
            rootBaker.location[2] = -z_offset
            bpy.ops.object.constraint_add(type='LIMIT_LOCATION')
            bpy.context.object.constraints["Limit Location"].use_min_z = True

    bpy.ops.object.constraint_add(type='COPY_LOCATION')
    bpy.context.object.constraints["Copy Location"].use_x = use_x
    bpy.context.object.constraints["Copy Location"].use_y = use_y
    bpy.context.object.constraints["Copy Location"].use_z = False
    bpy.context.object.constraints["Copy Location"].target = root
    bpy.context.object.constraints["Copy Location"].subtarget = hips.name

    bpy.ops.object.constraint_add(type='COPY_ROTATION')
    bpy.context.object.constraints["Copy Rotation"].target = root
    bpy.context.object.constraints["Copy Rotation"].subtarget = hips.name
    bpy.context.object.constraints["Copy Rotation"].use_y = False
    bpy.context.object.constraints["Copy Rotation"].use_x = False

    bpy.ops.nla.bake(frame_start=framerange[0], frame_end=framerange[1], step=1, only_selected=True, visual_keying=True,
                     clear_constraints=True, clear_parents=False, use_current_action=False, bake_types={'OBJECT'})

    # Create helper to bake hipmotion in Worldspace
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0), layers=(
    True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
    False, False, False, False))
    hipsBaker = bpy.context.object
    hipsBaker.name = "hipsBaker"

    bpy.ops.object.constraint_add(type='COPY_LOCATION')
    bpy.context.object.constraints["Copy Location"].target = root
    bpy.context.object.constraints["Copy Location"].subtarget = hips.name

    bpy.ops.object.constraint_add(type='COPY_ROTATION')
    bpy.context.object.constraints["Copy Rotation"].target = root
    bpy.context.object.constraints["Copy Rotation"].subtarget = hips.name

    bpy.ops.nla.bake(frame_start=framerange[0], frame_end=framerange[1], step=1, only_selected=True, visual_keying=True,
                     clear_constraints=True, clear_parents=False, use_current_action=False, bake_types={'OBJECT'})

    # select armature
    root.select = True
    bpy.context.scene.objects.active = root

    if apply_rotation or apply_scale:
        bpy.ops.object.transform_apply(location=False, rotation=apply_rotation, scale=apply_scale)

    # Bake Root motion to Armature (root)
    bpy.ops.object.constraint_add(type='COPY_LOCATION')
    bpy.context.object.constraints["Copy Location"].target = rootBaker

    bpy.ops.object.constraint_add(type='COPY_ROTATION')
    bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["rootBaker"]
    bpy.context.object.constraints["Copy Rotation"].use_offset = True

    bpy.ops.nla.bake(frame_start=framerange[0], frame_end=framerange[1], step=1, only_selected=True, visual_keying=True,
                     clear_constraints=True, clear_parents=False, use_current_action=True, bake_types={'OBJECT'})

    bpy.ops.object.mode_set(mode='POSE')
    hips.bone.select = True
    root.data.bones.active = hips.bone

    bpy.ops.pose.constraint_add(type='COPY_LOCATION')
    hips.constraints["Copy Location"].target = hipsBaker
    bpy.ops.pose.constraint_add(type='COPY_ROTATION')
    hips.constraints["Copy Rotation"].target = hipsBaker

    bpy.ops.nla.bake(frame_start=framerange[0], frame_end=framerange[1], step=1, only_selected=True, visual_keying=True,
                     clear_constraints=True, clear_parents=False, use_current_action=True, bake_types={'POSE'})

    # Delete helpers
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    hipsBaker.select = True
    rootBaker.select = True

    bpy.ops.object.delete(use_global=False)

    # bind armature to dummy mesh if it doesn't have any
    if fixbind:
        bindmesh = None
        for child in root.children:
            for mod in child.modifiers:
                if mod.type == 'ARMATURE':
                    if mod.object == root:
                        bindmesh = child
                        break
        if bindmesh == None:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0),
                                             layers=(
                                             True, False, False, False, False, False, False, False, False, False, False,
                                             False, False, False, False, False, False, False, False, False))
            binddummy = bpy.context.object
            binddummy.name = 'binddummy'
            root.select = True
            bpy.context.scene.objects.active = root
            bpy.ops.object.parent_set(type='ARMATURE')
        elif apply_rotation or apply_scale:
            bindmesh.select = True
            bpy.context.scene.objects.active = bindmesh
            bpy.ops.object.transform_apply(location=False, rotation=apply_rotation, scale=apply_scale)

    return 1


def batch_hip_to_root(source_dir, dest_dir, use_x=True, use_y=True, use_z=True, on_ground=True, scale=1.0,
                      restoffset=(0, 0, 0), hipname='', fixbind=True, apply_rotation=True, apply_scale=False,
                      b_remove_namespace=True, add_leaf_bones=False, knee_offset=(0, 0, 0), ignore_leaf_bones=True):
    """Batch Convert MixamoRigs"""

    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1

    numfiles = 0
    for file in os.scandir(source_dir):
        file_ext = file.name[-4::]
        file_loader = {
            ".fbx": lambda filename: bpy.ops.import_scene.fbx(filepath=filename, axis_forward='-Z',
                                                              axis_up='Y', directory="",
                                                              filter_glob="*.fbx", ui_tab='MAIN',
                                                              use_manual_orientation=False, global_scale=1.0,
                                                              bake_space_transform=False,
                                                              use_custom_normals=True,
                                                              use_image_search=True,
                                                              use_alpha_decals=False, decal_offset=0.0,
                                                              use_anim=True, anim_offset=1.0,
                                                              use_custom_props=True,
                                                              use_custom_props_enum_as_string=True,
                                                              ignore_leaf_bones=False,
                                                              force_connect_children=False,
                                                              automatic_bone_orientation=True,
                                                              primary_bone_axis='Y',
                                                              secondary_bone_axis='X',
                                                              use_prepost_rot=True),
            ".dae": lambda filename: bpy.ops.wm.collada_import(filepath=filename, filter_blender=False,
                                                               filter_backup=False, filter_image=False,
                                                               filter_movie=False, filter_python=False,
                                                               filter_font=False, filter_sound=False,
                                                               filter_text=False, filter_btx=False,
                                                               filter_collada=True, filter_alembic=False,
                                                               filter_folder=True, filter_blenlib=False,
                                                               filemode=8, display_type='DEFAULT',
                                                               sort_method='FILE_SORT_ALPHA',
                                                               import_units=False, fix_orientation=True,
                                                               find_chains=True, auto_connect=True,
                                                               min_chain_length=0)
        }
        if file_ext in file_loader:
            numfiles += 1
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=True)

            # remove all datablocks
            for mesh in bpy.data.meshes:
                bpy.data.meshes.remove(mesh, do_unlink=True)
            for material in bpy.data.materials:
                bpy.data.materials.remove(material, do_unlink=True)
            for action in bpy.data.actions:
                bpy.data.actions.remove(action, do_unlink=True)

            # import FBX
            file_loader[file_ext](file.path)

            # namespace removal
            if b_remove_namespace:
                for obj in bpy.context.selected_objects:
                    remove_namespace(obj)

            def getArmature(objects):
                for a in objects:
                    if a.type == 'ARMATURE':
                        return a

            armature = getArmature(bpy.context.selected_objects)
            # do hip to Root conversion
            if hip_to_root(armature, use_x=use_x, use_y=use_y, use_z=use_z, on_ground=on_ground, scale=scale,
                           restoffset=restoffset, hipname=hipname, fixbind=fixbind, apply_rotation=apply_rotation,
                           apply_scale=apply_scale) == -1:
                return -1
            apply_kneefix(armature, knee_offset,
                          bonenames=bpy.context.scene.mixamo.knee_bones.decode('utf-8').split(','))
            # remove newly created orphan actions
            for action in bpy.data.actions:
                if action != armature.animation_data.action:
                    bpy.data.actions.remove(action, do_unlink=True)

            # store file to disk
            output_file = dest_dir + file.name[:-3] + ".fbx"
            bpy.ops.export_scene.fbx(filepath=output_file,
                                     version='BIN7400',
                                     use_selection=False,
                                     apply_unit_scale=False,
                                     add_leaf_bones=add_leaf_bones)
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=False)
    return numfiles


if __name__ == "__main__":
    print("mixamoconv Hello.")

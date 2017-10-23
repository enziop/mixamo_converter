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

bl_info = {
    "name": "Mixamo Converter",
    "author": "Enzio Probst",
    "version": (1, 0, 6),
    "blender": (2, 7, 8),
    "location": "3D View > Tool Shelve > Mixamo Tab",
    "description": ("Script to bake Root motion for Mixamo Animations"),
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/enziop/mixamo_converter/wiki",
    "tracker_url": "https://github.com/enziop/mixamo_converter/issues" ,
    "category": "Animation"
}

import bpy
from . import mixamoconv

class MixamoPropertyGroup(bpy.types.PropertyGroup):
    '''Property container for options and paths of mixamo Converter'''
    advanced = bpy.props.BoolProperty(
        name="Advanced Options",
        description="Display advanced options",
        default=False)
    experimental = bpy.props.BoolProperty(
        name="Experimental Options",
        description="Experimental Options (use with caution, dirty workarounds)",
        default=False)

    use_x = bpy.props.BoolProperty(
        name="Use X",
        description="If enabled, Horizontal motion is transfered to RootBone",
        default=True)
    use_y = bpy.props.BoolProperty(
        name="Use Y",
        description="If enabled, Horizontal motion is transfered to RootBone",
        default=True)
    use_z = bpy.props.BoolProperty(
        name="Use Z",
        description="If enabled, vertical motion is transfered to RootBone",
        default=True)
    on_ground = bpy.props.BoolProperty(
        name="On Ground",
        description="If enabled, root bone is on ground and only moves up at jumps",
        default=True)

    scale = bpy.props.FloatProperty(
        name="Scale",
        description="Scale down the Rig by this factor",
        default=1.0)
    restoffset = bpy.props.FloatVectorProperty(
        name="Restpose Offset",
        description="Offset restpose by this. Use to correct if origin is not on ground",
        default=(0.0, 0.0, 0.0))
    knee_offset = bpy.props.FloatVectorProperty(
        name="Knee Offset",
        description="Offset knee joints by this. Use to fix flipping legs.",
        default=(0.0, 0.0, 0.0))
    knee_bones = bpy.props.StringProperty(
        name="Knee Bones",
        description="Names of knee bones to offset. Seperate names with commas.",
        maxlen = 256,
        default = "RightUpLeg,LeftUpLeg",
        subtype='BYTE_STRING')
    force_overwrite = bpy.props.BoolProperty(
        name="Force Overwrite",
        description="If enabled, overwrites files if output path is the same as input",
        default=False)

    inpath = bpy.props.StringProperty(
        name="Input Path",
        description="Path to mixamorigs",
        maxlen = 256,
        default = "",
        subtype='FILE_PATH')
    add_leaf_bones = bpy.props.BoolProperty(
        name="Add Leaf Bones",
        description="If enabled, adds leaf bones on export when batchconverting",
        default=False)
    outpath = bpy.props.StringProperty(
        name="Output Path",
        description="Where Processed rigs should be saved to",
        maxlen = 256,
        default = "",
        subtype='FILE_PATH')
    ignore_leaf_bones = bpy.props.BoolProperty(
        name="Ignore Leaf Bones",
        description="Ignore leaf bones on import",
        default=True)

    hipname = bpy.props.StringProperty(
        name="Hip Name",
        description="Additional Hipname to search for if not MixamoRig",
        maxlen = 256,
        default = "",
        subtype='BYTE_STRING')
    b_remove_namespace = bpy.props.BoolProperty(
        name="Remove Namespace",
        description="Removes Naespaces from objects and bones",
        default=True)
    b_unreal_bones = bpy.props.BoolProperty(
        name="Use Unreal Engine bone schema",
        description="Renames bones to match unreal engine schema",
        default=False)
    fixbind = bpy.props.BoolProperty(
        name="Fix Bind",
        description="If enabled, adds a dummy mesh and binds it, to prevent loss of bindpose when exporting fbx",
        default=True)
    apply_rotation = bpy.props.BoolProperty(
        name="Apply Rotation",
        description="Applies rotation during conversion to prevent rotation and scaling issues",
        default=True)
    apply_scale = bpy.props.BoolProperty(
        name="Apply Scale",
        description="Applies scale during conversion to prevent rotation and scaling issues",
        default=False)


class OBJECT_OT_RemoveNamespace(bpy.types.Operator):
    '''Button/Operator for removing namespaces from selection'''
    bl_idname = "mixamo.remove_namespace"
    bl_label = ""
    description = "Removes all namespaces of selection (for single Convert)"

    def execute(self, context):
        mixamo = context.scene.mixamo
        if not bpy.context.object:
            self.report({'ERROR_INVALID_INPUT'}, "Error: no object selected.")
            return{'CANCELLED'}
        for obj in bpy.context.selected_objects:
            status = mixamoconv.remove_namespace(obj)
            if status == -1:
                self.report({'ERROR_INVALID_INPUT'}, 'Invalid Object in selection')
                return{'CANCELLED' }
        return{'FINISHED'}

class OBJECT_OT_UseBlenderBoneNames(bpy.types.Operator):
    '''Button/Operator for renaming bones to match unreal skeleton'''
    bl_idname = "mixamo.unreal_bones"
    bl_label = ""
    description = "Renames bones to match the unreal skeleton (for single Convert)"

    def execute(self, context):
        mixamo = context.scene.mixamo
        if not bpy.context.object:
            self.report({'ERROR_INVALID_INPUT'}, "Error: no object selected.")
            return{ 'CANCELLED'}
        for obj in bpy.context.selected_objects:
            status = mixamoconv.rename_bones(obj)
            if status == -1:
                self.report({'ERROR_INVALID_INPUT'}, 'Invalid Object in selection')
                return{ 'CANCELLED'}
        return{'FINISHED' }

class OBJECT_OT_ConvertSingle(bpy.types.Operator):
    '''Button/Operator for converting single Rig'''
    bl_idname = "mixamo.convertsingle"
    bl_label = "Convert Single"
    description = "Bakes rootmotion for a single, already imported rig."

    def execute(self, context):
        mixamo = context.scene.mixamo
        if bpy.context.object == None:
            self.report({'ERROR_INVALID_INPUT'}, "Error: no object selected.")
            return{ 'CANCELLED'}
        if bpy.context.object.type != 'ARMATURE':
            self.report({'ERROR_INVALID_INPUT'}, "Error: %s is not an Armature." % bpy.context.object.name)
            return{ 'CANCELLED'}
        if bpy.context.object.data.bones[0].name not in ('mixamorig:Hips', 'mixamorig_Hips', 'Hips', mixamo.hipname):
            self.report({'ERROR_INVALID_INPUT'},
                        "Selected object %s is not a Mixamo rig, or at least naming does not match!" % bpy.context.object.name)
            return{ 'CANCELLED'}
        status = mixamoconv.hip_to_root(
            armature = bpy.context.object,
            use_x = mixamo.use_x,
            use_y =mixamo.use_y,
            use_z =mixamo.use_z,
            on_ground =mixamo.on_ground,
            scale =mixamo.scale,
            restoffset =mixamo.restoffset,
            hipname =mixamo.hipname,
            fixbind =mixamo.fixbind,
            apply_rotation =mixamo.apply_rotation,
            apply_scale =mixamo.apply_scale)
        if status == -1:
            self.report({'ERROR_INVALID_INPUT'}, 'Error: Hips not found')
            return{ 'CANCELLED'}
        self.report({'INFO'}, "Rig Converted")
        return{ 'FINISHED'}


class OBJECT_OT_ApplyRestoffset(bpy.types.Operator):
    '''Button/Operator for converting single Rig'''
    bl_idname = "mixamo.apply_restoffset"
    bl_label = "Apply Restoffset"
    description = "Applies Restoffset to restpose and corrects animation"

    def execute(self, context):
        mixamo = context.scene.mixamo
        if bpy.context.object == None:
            self.report({'ERROR_INVALID_INPUT'}, "Error: no object selected.")
            return{ 'CANCELLED'}
        if bpy.context.object.type != 'ARMATURE':
            self.report({'ERROR_INVALID_INPUT'}, "Error: %s is not an Armature." % bpy.context.object.name)
            return{ 'CANCELLED'}
        if bpy.context.object.data.bones[0].name not in ('mixamorig:Hips', 'mixamorig_Hips', 'Hips', mixamo.hipname):
            self.report({'ERROR_INVALID_INPUT'},
                        "Selected object %s is not a Mixamo rig, or at least naming does not match!" % bpy.context.object.name)
            return{ 'CANCELLED'}
        status = mixamoconv.apply_restoffset(bpy.context.object, bpy.context.object.data.bones[0], mixamo.restoffset)
        if status == -1:
            self.report({'ERROR_INVALID_INPUT'}, 'apply_restoffset Failed')
            return{ 'CANCELLED'}
        return{ 'FINISHED'}


class OBJECT_OT_ConvertBatch(bpy.types.Operator):
    '''Button/Operator for starting batch conversion'''
    bl_idname = "mixamo.convertbatch"
    bl_label = "Batch Convert"
    description = "Converts all mixamorigs from the [Input Path] and exports them to the [Ouput Path]"

    def execute(self, context):
        mixamo = context.scene.mixamo
        inpath = mixamo.inpath
        outpath = mixamo.outpath
        if inpath == '':
            self.report({'ERROR_INVALID_INPUT'}, "Error: no Input Path set.")
            return{ 'CANCELLED'}
        if outpath == '':
            self.report({'ERROR_INVALID_INPUT'}, "Error: no Output Path set.")
            return{ 'CANCELLED'}
        if (inpath == outpath) and not mixamo.force_overwrite:
            self.report({'ERROR_INVALID_INPUT'},
                        "Input and Output path are the same, source files would be overwritten.")
            return{ 'CANCELLED'}
        if (inpath == outpath) & mixamo.force_overwrite:
            self.report({'WARNING'}, "Input and Output path are the same, source files will be overwritten.")
        numfiles = mixamoconv.batch_hip_to_root(
            bpy.path.abspath(inpath),
            bpy.path.abspath(outpath),
            use_x =mixamo.use_x,
            use_y =mixamo.use_y,
            use_z =mixamo.use_z,
            on_ground =mixamo.on_ground,
            scale =mixamo.scale,
            restoffset =mixamo.restoffset,
            hipname =mixamo.hipname,
            fixbind =mixamo.fixbind,
            apply_rotation =mixamo.apply_rotation,
            apply_scale =mixamo.apply_scale,
            b_remove_namespace =mixamo.b_remove_namespace,
            add_leaf_bones =mixamo.add_leaf_bones,
            knee_offset =mixamo.knee_offset,
            ignore_leaf_bones =mixamo.ignore_leaf_bones)
        if numfiles == -1:
            self.report({'ERROR_INVALID_INPUT'}, 'Error: Hips not found')
            return{ 'CANCELLED'}
        self.report({'INFO'}, "%d files converted" % numfiles)
        return{ 'FINISHED'}


class MixamoconvPanel(bpy.types.Panel):
    """Creates a Tab in the Toolshelve in 3D_View"""
    bl_label = "Mixamo Rootbaker"
    bl_idname = "ANIMATION_PT_mixamo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Mixamo"

    def draw(self, context):
        layout = self.layout

        scene = bpy.context.scene

        ''' Annoying warning Box
        #box with general info
        infobox = layout.box()
        infobox.label(icon = 'ERROR', text = "Attention:")
        row = infobox.row()
        row.label("Batch Convert will delete everything from your current scene")
        row = infobox.row()
        row.label("Only use in empty or startup scene")
        '''

        box = layout.box()
        # Options for how to do the conversion
        row = box.row()
        row.prop(scene.mixamo, "use_z", toggle =True)
        if scene.mixamo.use_z:
            row.prop(scene.mixamo, "on_ground", toggle =True)

        # Button for conversion of single Selected rig
        row = box.row()
        row.scale_y = 2.0
        row.operator("mixamo.convertsingle")

        box = layout.box()
        row = box.row()
        row.prop(scene.mixamo, "advanced", toggle=True)

        # row.prop(scene.mixamo, "mode")
        if scene.mixamo.advanced:
            split = box.split()
            col = split.column(align =True)
            col.prop(scene.mixamo, "use_x", toggle =True)
            col.prop(scene.mixamo, "use_y", toggle =True)
            col.prop(scene.mixamo, "use_z", toggle =True)

            box.label(text="Bone names:")
            box.prop(scene.mixamo, "hipname")

            row = box.row()
            row.prop(scene.mixamo, 'b_remove_namespace', text="Remove Namespaces")
            row.operator("mixamo.remove_namespace", icon='PLAY')
            row.enabled = not scene.mixamo.b_unreal_bones

            row = box.row()
            row.prop(scene.mixamo, 'b_unreal_bones', text="Use Unreal Engine bone names")
            row.operator("mixamo.unreal_bones", icon='PLAY')
            row.enabled = not scene.mixamo.b_remove_namespace

            box.label(text="Fixes:")
            row = box.row()
            row.prop(scene.mixamo, "fixbind")
            row.prop(scene.mixamo, "apply_rotation")

            row = box.row()
            row.prop(scene.mixamo, "apply_scale")
            if scene.mixamo.apply_scale:
                row.prop(scene.mixamo, "scale")

            # box = box.box()
            row = box.row()
            row.prop(scene.mixamo, "experimental", toggle=True, icon='ERROR')
            if scene.mixamo.experimental:
                row = box.row()
                split = box.split()
                col = split.column()
                col.prop(scene.mixamo, "restoffset")
                # row = box.row()
                col.operator("mixamo.apply_restoffset")
                col = split.column()
                col.prop(scene.mixamo, "knee_offset")
                col.prop(scene.mixamo, "knee_bones")

        box = layout.box()
        # input and output paths for batch conversion
        box.label(text="Batch")
        split = box.split()
        col = split.column()
        col.prop(scene.mixamo, "inpath")

        # row = box.row()
        col.prop(scene.mixamo, "outpath")
        if scene.mixamo.advanced:
            col = split.column()
            col.prop(scene.mixamo, "ignore_leaf_bones")
            col.prop(scene.mixamo, "add_leaf_bones")

        box.prop(scene.mixamo, "force_overwrite")

        # button to start batch conversion
        row = box.row()
        row.scale_y = 2.0
        row.operator("mixamo.convertbatch")
        status_row = box.row()


def register():
    bpy.utils.register_class(MixamoPropertyGroup)
    bpy.types.Scene.mixamo = bpy.props.PointerProperty(type=MixamoPropertyGroup)
    bpy.utils.register_module(__name__)
    '''
    bpy.utils.register_class(OBJECT_OT_ConvertSingle)
    bpy.utils.register_class(OBJECT_OT_ConvertBatch)
    bpy.utils.register_class(MixamoconvPanel)
    '''


def unregister():
    bpy.utils.unregister_module(__name__)
    '''
    bpy.utils.unregister_class(MixamoPropertyGroup)
    bpy.utils.unregister_class(OBJECT_OT_ConvertSingle)
    bpy.utils.register_class(OBJECT_OT_ConvertBatch)
    bpy.utils.unregister_class(MixamoconvPanel)
    '''


if __name__ == "__main__":
    register()



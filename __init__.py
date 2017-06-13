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
    "version": (1, 0, 1),
    "blender": (2, 7, 8),
    "location": "3D View > Tool Shelve > Mixamo Tab",
    "description": ("Script to bake Root motion for Mixamo Animations"),
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "" ,
    "category": "Animation"
}

import bpy
from . import mixamoconv

class MixamoPropertyGroup(bpy.types.PropertyGroup):
    '''Property container for options and paths of mixamo Converter'''
    use_x = bpy.props.BoolProperty(
                    name="Use X",
                    description="If enabled, Horizontal motion is transfered to RootBone",
                    default=True)
    use_y = bpy.props.BoolProperty(
                    name="Use Y",
                    description="If enabled, Horizontal motion is transfered to RootBone",
                    default=True)
    use_vertical = bpy.props.BoolProperty(
                    name="Use Vertical",
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
    outpath = bpy.props.StringProperty(
                    name="Output Path",
                    description="Where Processed rigs should be saved to",
                    maxlen = 256,
                    default = "",
                    subtype='FILE_PATH')
    hipname = bpy.props.StringProperty(
                    name="Hip Name",
                    description="Additional Hipname to search for if not MixamoRig",
                    maxlen = 256,
                    default = "",
                    subtype='BYTE_STRING')

class OBJECT_OT_ConvertSingle(bpy.types.Operator):
    '''Button/Operator for converting single Rig'''
    bl_idname = "mixamo.convertsingle"
    bl_label = "Convert Single"
    description = "Bakes rootmotion for a single, already imported rig."
    
    def execute(self, context):
        if bpy.context.object == None:
            self.report({'ERROR_INVALID_INPUT'}, "Error: no object selected.")
            return{'CANCELLED'}
        if bpy.context.object.type != 'ARMATURE':
            self.report({'ERROR_INVALID_INPUT'}, "Error: %s is not an Armature." % bpy.context.object.name)
            return{'CANCELLED'}
        if bpy.context.object.data.bones[0].name not in ('mixamorig:Hips', 'Hips', bpy.context.scene.mixamo.hipname):
            self.report({'ERROR_INVALID_INPUT'}, "Selected object %s is not a Mixamo rig, or at least naming does not match!" % bpy.context.object.name)
            return{'CANCELLED'}
        self.report({'INFO'}, "Rig Converted")
        status = mixamoconv.HipToRoot(armature = bpy.context.object, use_x = context.scene.mixamo.use_x, use_y = context.scene.mixamo.use_y, use_z = context.scene.mixamo.use_vertical, on_ground = context.scene.mixamo.on_ground, scale = context.scene.mixamo.scale, hipname = bpy.context.scene.mixamo.hipname)
        if status == -1:
            self.report({'ERROR_INVALID_INPUT'}, 'Error: Hips not found')
            return{'CANCELLED'}
        return{'FINISHED'}

class OBJECT_OT_ConvertBatch(bpy.types.Operator):
    '''Button/Operator for starting batch conversion'''
    bl_idname = "mixamo.convertbatch"
    bl_label = "Batch Convert"
    description = "Converts all mixamorigs from the [Input Path] and exports them to the [Ouput Path]"
    
    def execute(self, context):
        inpath = bpy.context.scene.mixamo.inpath
        outpath = bpy.context.scene.mixamo.outpath
        if inpath == '':
            self.report({'ERROR_INVALID_INPUT'}, "Error: no Input Path set.")
            return{'CANCELLED'}
        if outpath == '':
            self.report({'ERROR_INVALID_INPUT'}, "Error: no Output Path set.")
            return{'CANCELLED'}
        if (inpath == outpath) and not bpy.context.scene.mixamo.force_overwrite:
            self.report({'ERROR_INVALID_INPUT'}, "Input and Output path are the same, source files would be overwritten.")
            return{'CANCELLED'}
        if (inpath == outpath) & bpy.context.scene.mixamo.force_overwrite:
            self.report({'WARNING'}, "Input and Output path are the same, source files will be overwritten.")
        numfiles = mixamoconv.BatchHipToRoot(bpy.path.abspath(inpath), bpy.path.abspath(outpath), use_x = context.scene.mixamo.use_x, use_y = context.scene.mixamo.use_y, use_z = context.scene.mixamo.use_vertical, on_ground = context.scene.mixamo.on_ground, scale = context.scene.mixamo.scale, hipname = bpy.context.scene.mixamo.hipname)
        if numfiles == -1:
            self.report({'ERROR_INVALID_INPUT'}, 'Error: Hips not found')
            return{'CANCELLED'}
        self.report({'INFO'}, "%d files converted" % numfiles)
        return{'FINISHED'}

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
        row.prop(scene.mixamo, "use_x")
        row.prop(scene.mixamo, "use_y")
        row = box.row()
        row.prop(scene.mixamo, "use_vertical")
        row.prop(scene.mixamo, "on_ground")
        row = box.row()
        row.prop(scene.mixamo, "hipname")
        row = box.row()
        row.prop(scene.mixamo, "scale")
        # Button for conversion of single Selected rig
        row = box.row()
        row.scale_y = 2.0
        row.operator("mixamo.convertsingle")
        
        
        box = layout.box()
        # input and output paths for batch conversion
        box.label(text="Batch")
        row = box.row()
        row.prop(scene.mixamo, "inpath")
        row = box.row()
        row.prop(scene.mixamo, "outpath")
        row = box.row()
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
    
    

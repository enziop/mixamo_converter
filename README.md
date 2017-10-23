# Mixamo Converter
is a Blender Plugin that Converts Mixamo animations to work in Unreal Engine 4 with root motion
Blender 2.78 or newer needed to work

### It can
* convert single animations (FBX or Collada) if they are previously imported by the user
* Batch convert all input FBX and Collada files from a folder to a new location
* Renames the bones in the skeleton to match the maniquine unreal skeleton

## Installation
* first you have to get blender from https://www.blender.org/download/
* Download Mixamo Converter repository as ZIP (no need to unpack it)
* Open up Blender
* go to: File -> User Preferences -> Addons -> Install from File...
* select the ZIP you downloaded and click install from file
* now it should be the only addon visibly and you can enable it
* if you want to keep it enabled over multiple blender sessions you can click "save user preferences" on the bottom of the window

## Usage
The Addon UI is located in the Toolshelve of the 3D view.
You can open it by pressing T with the mouse in the 3D View
or with the little plus sign on the left side of the 3D View
In the Toolshelve there are several tabs on the left side,
one of them should be named Mixamo

### Options: [Use Z] [On Ground]
it will behave as follows in Unreal Engine 4
Only rotation along the Up Axis is transfered to the root
##### Both Enabled (recommended):
A Root bone which stays on ground except for cases when the Hip moves higher than its restpose location
##### Only [Use Z] Enabled:
the root bone can go below the Ground
this will result in wierd behaviour if one Big Collider is used for the Character in Unreal
##### [Use Z] is Disabled
no Vertical motion at all is transfered to the Root and [On Ground] becomes obsolete

#### Options: [Use X] [Use Y]
Those can be disabled to prevent movement of root on groundplane.
Useful if one doesn't want to use root motion for some Animations but still needs to have the same converted rig. If so just disable Use Vertical, Use X and Use Y.

#### Option [Hip Name]
Here you can specify a custom HipName if your Rig doesn't come from Mixamo. It will then also search for a bone with this name and consider it as Hip to bake From if found.

#### Option [Remove Namespace]
If enabled, removes all namespaces, leaving you with only the object/bone bare names.
This option is not compatible with "Use Unreal Engine bone names" option.
To convert the bones of the armature in the scene select the armature and press the play button.
Check this option to enable it for batch conversions.

#### Option [Use Unreal Engine bone names]
If enabled, renames all bones in the armature to match the unreal engine maniquine skeleton. If a bone doesn't match a warning is printed and the name becomes the original one but without the 'mixamo' namespace (as Remove Namespace does).
This option is not compatible with "Remove Namespace" option.
To convert the bones of the armature in the scene select the armature and press the play button.
Check this option to enable it for batch conversions.

#### Option [Fix Bind]
If your source files only contain a rig without a mesh, adds a dummy mesh and binds it to the armature. Otherwise the bindpose will not be saved properly.
Useful if you download packs from mixamo, where all the animations don't have meshes, but only the rigs.

#### Option [Apply Rotation]
Makes sure, that there are no unneeded rotations on the character or its root bone, which would often cause unexpected rotation behaviour in unreal.

#### Option [Apply Scale]
Applies the scale of the character and its rig, so they have scale 1, but doesn't change the actual size of the character.

#### Option [Scale]
Scaling factor for actually resizing your character.

### Experimental Options

#### Option [Restpose Offset]
Offsets the restpose of your rig without offsetting the animation. Can be used to correct for an offset of the restpose that one might have accidentally added during animation editing or retargeting.

#### Option [Knee Offset]
Very kludgy workaround which can result in bones being out of place in animation.
Can be used to fix rotational flickering occuring in some animations after export (seems to be an exporter bug). (mostly observed on legs but can be used on any bones)
It moves the tip joint of given bones by the given vector in the restpose.

### Batch Conversion:
* Here you can specify an Input- and Outputpath for Batchconversion
* the output files will have the same names as the input files, existing files will be overwritten
* The [force overwrite] option is only for the case where Input- and Outputlocation are the same
* If input and output path are set you can press [Batch Convert] to convert all FBX files from source location and save it to target location
* this takes around 10 seconds per file, there is no progress bar yet so be patient
* The source location should only contain FBX files containing original mixamo rigs otherwise the script will not work
* files not ending with .fbx are ignored and can stay in source directory

### ATTENTION!
Batch Convert will delete everything from your currently open blenderscene
so only use it in a newly startet instance of blender or an empty scene
    
Happy Converting

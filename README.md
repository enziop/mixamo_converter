# Mixamo Converter
is a Blender Plugin that Converts Mixamo animations to work in Unreal Engine 4 with root motion
Blender 2.78 or newer needed to work

### It can
* convert single animations if they are previously imported by the user
* Batch convert all FBX files from a folder to a new location

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

### Options: [Use Vertical] [On Ground]
it will behave as follows in Unreal Engine 4
Only rotation along the Up Axis is transfered to the root
##### Both Enabled (recommended):
A Root bone which stays on ground except for cases when the Hip moves higher than its restpose location
##### Only [Use Vertical] Enabled:
the root bone can go below the Ground
this will result in wierd behaviour if one Big Collider is used for the Character in Unreal
##### [Use Vertical] is Disabled
no Vertical motion at all is transfered to the Root and [On Ground] becomes obsolete

#### Options: [Use X] [Use Y]
Those can be disabled to prevent movement of root on groundplane.
Useful if one doesn't want to use root motion for some Animations but still needs to have the same converted rig. If so just disable Use Vertical, Use X and Use Y.

#### Option [Hip Name]
Here you can specify a custom HipName if your Rig doesn't come from Mixamo. It will then also search for a bone with this name and consider it as Hip to bake From if found.

#### Option [Scale]
Scaling factor for unit conversion problems. Sometimes the scale of the root is keyed resulting in Scaling of Character if you apply the animation to your skeleton in Unreal.
If set to something else than 1.0 it will remove existing scaling keys and scale the skeleton by this factor.

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

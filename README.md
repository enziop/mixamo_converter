# Mixamo Converter
is a Blender Plugin that Converts Mixamo animations to work in Unreal Engine 4 with root motion
Blender 2.80 or newer needed to work. For blender 2.78+ use blender27 branch of the converter.

### It can
* convert single animations (FBX or Collada) if they are previously imported by the user
* Batch convert all input FBX and Collada files from a folder to a new location
* Renames the bones in the skeleton to match the maniquine unreal skeleton

## Installation
* first you have to get blender from https://www.blender.org/download/
* Download Mixamo Converter repository as ZIP (no need to unpack it)
* Open up Blender
* go to: Edit -> Preferences -> Addons -> Install from File...
* select the ZIP you downloaded and click install from file
* now it should be in the list (search for mixamo) and you can enable it

## Usage
The Addon UI is located in the UI Region of the 3D view.
You can open it by pressing N with the mouse in the 3D View
or with the little arrow on the right side of the 3D View
In the UI Area there are several tabs on the right side,
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

Note: When importing the mixamo skeleton to unreal, you still need to perform a retarget.
For a fast retargeting, after importing the converted FBX of your mixamo character in T pose, open its skeleton and retarget it to the humanoid rig but
DO NOT PRESS the 'automapping' button for mixamo skeletons. If it's pressed, the automapping will match the mixamo bones to wrong rig nodes.

Please note that, most of the bones in the mixamo skeleton have a 1:1 mapping to Humanoid rig nodes, but for the following ones:

* lowerarm_twist_01_l -> hand_l
* upperarm_twist_01_l -> upperarm_l
* lowerarm_twist_01_r -> hand_r
* upperarm_twist_01_r -> upperarm_r
* thigh_twist_01_l -> thigh_l
* calf_twist01_l ->  None
* thigh_twist_01_r -> thigh_r
* calf_twist01_r -> None

For more info please check the [unreal documentation](https://docs.unrealengine.com/latest/INT/Engine/Animation/RetargetingDifferentSkeletons/)

Moreover to retarget your mixamo skeleton (in T pose) to the unreal one (A pose), both have to share the same retarget pose.'
You can easily set T pose to the unreal skeleton following the instructions in this [video](https://www.youtube.com/watch?v=D8nH2Yo9PT8)

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

#### Option [Foot Bone Workaround]
Workaround which attempts to fix the twisting of the foot bones (specifically, LeftToeBase/ball_l and RightToeBase/ball_r) of certain meshes,
which may appear rotated by 180 degrees after conversion.

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

### Video Tutorials

#### Importing a mixamo character into unreal with and retarget animations
The video starts showing how to install the mixamoconv plugin into blender.
Then it describe how to quickly batch convert a mixamo character (same procedure for anims), import it to unreal, reterget the mixamo skeleton and retarget some maniquine anims to the mixamo skeleton.
Remember the converter is now located in the Right Panel (UI) which can be opened by pressing N.


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/z97w4vrm8Eo/0.jpg)](https://www.youtube.com/watch?v=z97w4vrm8Eo)    


#### Development
If you wanna contribute to this project you can edit the project with PyCharm and run the changes straightway in Blender.
To achieve this you have to:
+  Download Pycharm community edition from [jetbrains.com](https://www.jetbrains.com/pycharm/download)
+  Open blender
+  open a text view, click + and paste there the code below 
+  Replace /the/path/to/the/git/project with the path to github project in the below code
+  Edit the changes in Pycharm
+  Click "Run Script" in blender to reload the project with the new changes

```python
import bpy
import os
import sys

git_path=r'/the/path/to/the/git/project'
sys.path.insert(0, git_path)
filename = os.path.join(git_path, '__init__.py')

exec(compile(open(filename).read(), filename, 'exec'))
```

Happy Converting

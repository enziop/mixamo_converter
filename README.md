# Mixamo Converter
is a Blender Plugin that Converts Mixamo animations to work in Unreal Engine 4 with root motion

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
#### Both Enabled (recommended):
    A Root bone which stays on ground except for cases when the Hip moves higher than its restpose location
#### Only [Use Vertical] Enabled:
    the root bone can go below the Ground
    this will result in wierd behaviour if one Big Collider is used for the Character in Unreal
#### [Use Vertical] is Disabled
    no Vertical motion at all is transfered to the Root and [On Ground] becomes obsolete
Only rotation along the Up Axis is transfered to the root

### Batch Conversion:
* Here you can specify an Input- and Outpupath for Batchconversion
* the output files will have the same names as the input files, existing files will be overwritten
* The [force overwrite] option is only for the case where Input- and Outputlocation are the same
* If input and output path are set you can press [Batch Convert] to convert all FBX files from source location and save it to target location
* this takes around 10 seconds per file, there is no progress bar yet so be patient
* The source location should only contain FBX files containing original mixamo rigs otherwise the script will not work
* files not ending with .fbx are ignored and can stay in source directory

### !!!ATTETION!!!
Batch Convert will delete everything from your currently open blenderscene
so only use it in a newly startet instance of blender or an empty scene
    
Happy Converting

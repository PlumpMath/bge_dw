## Dark War

Dark War is a survival horror / shooter game. It's being developed in Blender Game Engine, specifically UPBGE. Using regular Blender or older UPBGE versions may break the blend files.

Engine: UPBGE 0.1.3 - [Download](https://drive.google.com/file/d/0B3GouQIyoCmrdHJJbVMxazdBenc/view?usp=sharing)

The repository is well organized. There's not too many abbreviations in file names, each file type has its own case pattern in names.

#### Directories description
ROOT - Contains blend libraries, main game files and docs.

config - INI files that loads global saved data to bge.logic.globalDict at game start.

save - Contains player's savegame files. For now the files are INI for debugging, but this will be changed in the future.

scripts - Contains all Python scripts used around the game. The packages are divided in different contexts.

sounds - Self explanatory. Contains music and sound effects, separated by context.

source - Contains media source files like reference images, image and audio editing project files, etc.

textures - Self explanatory. Contains textures of models, GUI and misc elements of the game.

#### More help can be found at Dark_War_Docs.py

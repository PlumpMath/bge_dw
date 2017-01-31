import bge
import aud
from bge.logic import expandPath

"""  This module contais all sound processing of the levels, like music, ambience, events, etc. """

def level_sound(cont):
	""" Plays the level sounds, music, ambience, etc. It reads properties of level_sounds group object and sets the music and ambience based on it. The properties are "ambience" and "music".
	
	SCENE: current level
	OBJECT: 'level_sounds'
	FREQUENCY: property change dependent """

	# Basic
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	S_always = cont.sensors[0].positive
	
	# Objects
	O_group = own.groupObject
	
	# Actuators
	A_music = cont.actuators["music"]
	A_ambience = cont.actuators["ambience"]
	
	# Properties
	sfx_volume = float(globalDict["options"]["sound"]["sfx_volume"])
	music_volume = float(globalDict["options"]["sound"]["music_volume"])
	ambience_volume = float(globalDict["options"]["sound"]["ambience_volume"])
	path_music = expandPath("//sounds/")
	path_ambience = expandPath("//sounds/ambience/")
	ext = ".ogg"
	
	### Sounds ###
	# Ambience
	disturbing_01 = aud.Factory(path_ambience + "ambience_disturbing_01" + ext)
	disturbing_02 = aud.Factory(path_ambience + "ambience_disturbing_02" + ext)
	inside_01 = aud.Factory(path_ambience + "ambience_inside_01" + ext)
	inside_02 = aud.Factory(path_ambience + "ambience_inside_02" + ext)
	wind_01 = aud.Factory(path_ambience + "ambience_wind" + ext)
	wind_02 = aud.Factory(path_ambience + "ambience_wind_trees" + ext)
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		current_ambience = None
		current_music = None
		
		### Set the current sound
		if "ambience" in O_group:
			
			if O_group["ambience"] == "wind_01":
				A_ambience.sound = wind_01
				
			if O_group["ambience"] == "wind_02":
				A_ambience.sound = wind_02
				
			if O_group["ambience"] == "inside_01":
				A_ambience.sound = inside_01
				
			if O_group["ambience"] == "inside_02":
				A_ambience.sound = inside_02
				
			if O_group["ambience"] == "disturbing_01":
				A_ambience.sound = disturbing_01
				
			if O_group["ambience"] == "disturbing_02":
				A_ambience.sound = disturbing_02
		
		A_music.volume = music_volume
		A_ambience.volume = ambience_volume
		
		cont.activate(A_ambience)

import bge
from bge.logic import expandPath
import aud

""" This module contains all sound processing of the player, like weapons, environment interaction, speech and other. """

################################ SOUND ################################

def init_sounds(cont):
	""" Initializes the sounds, loading them and setting them to a property in sounds object.
	
	SCENE: current level
	OBJECT: 'sounds'
	FREQUENCY: once """

	# Basic
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	S_always = cont.sensors[0].positive
	
	# Objects
	O_sounds = own
	
	# Properties
	path_sfx = expandPath("//sounds/sfx/weapons/")
	ext = ".wav"
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		### Factories ###
		# Weapons
		shotgun = aud.Factory(path_sfx + "shot_shotgun" + ext).buffer()
		submachinegun = aud.Factory(path_sfx + "shot_submachinegun" + ext).buffer()
		assault_rifle = aud.Factory(path_sfx + "shot_assault_rifle" + ext).buffer()
		flamer = aud.Factory(path_sfx + "shot_flamer" + ext).buffer()
		grenade_rifle = aud.Factory(path_sfx + "shot_grenade_rifle" + ext).buffer()
		railgun = aud.Factory(path_sfx + "shot_railgun" + ext).buffer()
		
		clipin = aud.Factory(path_sfx + "sfx_clipin" + ext).buffer()
		clipout = aud.Factory(path_sfx + "sfx_clipout" + ext).buffer()
		cocking_01 = aud.Factory(path_sfx + "sfx_cocking_01" + ext).buffer()
		cocking_02 = aud.Factory(path_sfx + "sfx_cocking_02" + ext).buffer()
		
		weapons = {"shotgun" : shotgun,
		"submachinegun" : submachinegun,
		"assault_rifle" : assault_rifle,
		"flamer" : flamer,
		"grenade_rifle" : grenade_rifle,
		"railgun" : railgun,
		"clipin" : clipin,
		"clipout" : clipout,
		"cocking_01" : cocking_01,
		"cocking_02" : cocking_02}
		
		### Sounds library ###
		O_sounds["sfx"] = {}
		
		### Set the library to a game object property
		O_sounds["sfx"]["weapons"] = weapons
		
	pass

def play_weapon(cont):
	""" Plays the weapon sounds, like shooting, cocking, etc.
	
	SCENE: current level
	OBJECT: 'sounds'
	FREQUENCY: property change dependent """

	# Basic
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	S_clip_changed = cont.sensors["clip_changed"].positive
	S_item_changed = cont.sensors["item_changed"].positive
	S_action_changed = cont.sensors["action_changed"].positive
	S_always = cont.sensors["always_play_weapon"]
	S_shooting_changed = cont.sensors["shooting_changed"].positive
	
	# Objects
	O_sounds = own
	O_collision = O_sounds.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_input = O_collision.childrenRecursive.get("input")
	O_combat = O_collision.childrenRecursive.get("combat")
	
	# Actuators
	A_shot = cont.actuators["shot"]
	A_cocking = cont.actuators["cocking"]
	A_clipout = cont.actuators["clipout"]
	A_clipin = cont.actuators["clipin"]
	A_empty_clip = cont.actuators["empty_clip"]
	
	# Properties
	sfx_volume = float(globalDict["options"]["sound"]["sfx_volume"])
	
	### Sounds ###
	# Weapons
	weapons = O_sounds["sfx"]["weapons"]
	
	############################
	######## INITIALIZE ########
	############################
	
	if not O_data["is_busy"] and sfx_volume > 0.0:
		
		### If aiming ###
		if O_data["current_action"] == "aiming":
			
			# Active process
			S_always.usePosPulseMode = False
			
			### Set the weapon sounds ###
			# Shotguns
			if O_combat["name"] == "shotgun" or O_combat["name"] == "shotgun_2_barrel" or O_combat["name"] == "shotgun_auto":
				A_shot.sound = weapons["shotgun"]
				A_cocking.sound = weapons["cocking_02"]
				
			# Submachinegun
			if O_combat["name"] == "submachinegun":
				A_shot.sound = weapons["submachinegun"]
				A_cocking.sound = weapons["cocking_01"]
				
			# Assault rifle
			if O_combat["name"] == "assault_rifle":
				A_shot.sound = weapons["assault_rifle"]
				A_cocking.sound = weapons["cocking_01"]
				
			# Flamer
			if O_combat["name"] == "flamer":
				A_shot.sound = weapons["flamer"]
				A_cocking.sound = weapons["cocking_01"]
				
			# Grenade rifle
			if O_combat["name"] == "grenade_rifle":
				A_shot.sound = weapons["grenade_rifle"]
				A_cocking.sound = weapons["cocking_01"]
				
			# Railgun
			if O_combat["name"] == "railgun":
				A_shot.sound = weapons["railgun"]
				A_cocking.sound = weapons["cocking_01"]
			
			### Play sound ###
			if O_input["is_shooting"]:
				
				# Shoot
				if S_clip_changed and O_combat["current_clip"] > -1 and O_combat["current_clip"] < O_combat["max_clip"]: 
				
					# Set sfx_volume
					A_shot.volume = sfx_volume
					
					# Stop current sounds and play new
					A_shot.stopSound()
					cont.activate(A_shot)
					A_shot.startSound()
					
				# Empty
				if O_combat["current_clip"] == 0 and S_shooting_changed:
					
					A_empty_clip.stopSound()
					cont.activate(A_empty_clip)
					A_empty_clip.startSound()
				
				
		### If not aiming ###
		if O_data["current_action"] != "aiming":
			
			# Passive process
			S_always.usePosPulseMode = True
			
			### If reloading or cocking
			if S_action_changed:
				
				# Clipout
				if O_data["current_action"] == "reloading":
					A_clipout.volume = sfx_volume
					
					A_clipout.startSound()
					cont.activate(A_clipout)
					
				# Cocking
				if O_data["current_action"] == "cocking":
					A_cocking.volume = sfx_volume
					
					A_cocking.startSound()
					cont.activate(A_cocking)
				
			# Clipin
			if S_clip_changed:
				A_clipin.volume = sfx_volume
				
				A_clipin.startSound()
				cont.activate(A_clipin)
				
	pass




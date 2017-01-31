import bge
from bge.logic import expandPath
from mathutils import Vector
from scripts.utils import *

""" This module contains the combat behavior of the player, like changing the combat props and acting over the environment when combat related (attacking enemies, damaging environment, etc). """
	
################################ COMBAT ################################

def item_change(cont):
	
	""" Sets the combat properties based on item change.
	
	SCENE: current level
	OBJECT: 'combat'
	FREQUENCY: input and property change dependent """
	
	# Basic
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	S_always = cont.sensors["always_item_change"]
	S_item_changed = cont.sensors["item_changed"].positive
	S_timer_positive = cont.sensors["timer_positive"].positive
	
	# Objects
	O_combat = own
	O_collision = O_combat.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_input = O_collision.childrenRecursive.get("input")
	
	# Properties
	current_player = globalDict["state"]["current_player"]
	weapons = globalDict["database"]["weapons"]
	
	
	############################
	######## INITIALIZE ########
	############################
	
	if not O_data["is_busy"]:
		
		# Fix null item at start
		if O_data["current_item"] == 0:
			O_data["current_item"] = int(current_player["status"]["current_item"])
		
		### Change props from current item to O_combat props ###
		if S_item_changed:
			
			# Current item in dict format
			current_item = current_player["item_" + str(O_data["current_item"])]
			
			item_name = current_item["name"]
			
			### Set props from globalDict to current item ###
			if True:
				O_combat["name"] = current_item["name"]
				O_combat["type"] = weapons[item_name]["type"]
				O_combat["shot_time"] = float(weapons[item_name]["shot_time"])
				O_combat["cocking_type"] = int(weapons[item_name]["cocking_type"])
				O_combat["cocking_time"] = float(weapons[item_name]["cocking_time"])
				O_combat["current_clip"] = int(current_item["current_clip"])
				O_combat["max_clip"] = int(weapons[item_name]["max_clip"])
				O_combat["ammo_stock"] = int(current_item["ammo_stock"])
				O_combat["damage"] = int(weapons[item_name]["damage"])
				
			O_combat["timer_cock"] = -O_combat["cocking_time"]
			
	pass

def set_attack_props(cont):
	
	""" Sets the attack properties based on main properties change.
	
	SCENE: current level
	OBJECT: 'combat'
	FREQUENCY: input and property change dependent """
	
	# Basic
	own = cont.owner
	globalDict = bge.logic.globalDict
	current_player = globalDict["state"]["current_player"]
	
	# Sensors
	S_timer_positive = cont.sensors["timer_positive"].positive
	S_shooting_changed = cont.sensors["shooting_changed"].positive
	
	# Objects
	O_combat = own
	O_collision = O_combat.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_armature = O_collision.childrenRecursive.get("player_armature")
	O_input = O_collision.childrenRecursive.get("input")
	
	# Properties
	current_item = "item_" + str(O_data["current_item"])
	
	############################
	######## INITIALIZE ########
	############################
	
	# Not busy
	if not O_data["is_busy"]:
		
		# Not cooldown, cocking or reloading and is shooting
		if S_timer_positive and O_input["is_shooting"] == True and O_data["current_action"] == "aiming":
				
				### Decrease current_clip ammo and set shoot cooldown ###
				if O_combat["current_clip"] > 0:
					O_combat["current_clip"] -= 1
					current_player[current_item]["current_clip"] = int(current_player[current_item]["current_clip"]) - 1
					
					# Set to cocking time if shotgun
					if O_combat["name"] == "shotgun" or O_combat["name"] == "shotgun_2_barrel":
						O_combat["timer_cock"] = -O_combat["cocking_time"]
					
					# Set to normal cooldown if another weapon
					else:
						O_combat["timer_cock"] = -O_combat["shot_time"]
				
	pass

def set_reload_props(cont):
	
	""" Sets the reloading and cocking properties based on main properties change.
	
	SCENE: current level
	OBJECT: 'combat'
	FREQUENCY: input and property change dependent """
	
	# Basic
	own = cont.owner
	globalDict = bge.logic.globalDict
	current_player = globalDict["state"]["current_player"]
	
	# Sensors
	S_always = cont.sensors["always_set_reload_props"]
	S_reloading_changed = cont.sensors["reloading_changed"].positive
	S_action_changed = cont.sensors["action_changed"].positive
	S_item_changed = cont.sensors["item_changed"].positive
	
	# Objects
	O_combat = own
	O_collision = O_combat.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_armature = O_collision.childrenRecursive.get("player_armature")
	O_input = O_collision.childrenRecursive.get("input")
	
	# Properties
	reloading_time = 2.0
	current_item = current_player["item_" + str(O_data["current_item"])]
	
	############################
	######## INITIALIZE ########
	############################
	
	if not O_data["is_busy"]:
		
		# Activate passive processing #
		if S_action_changed and O_data["current_action"] != "aiming" and O_combat["timer_cock"] < 0.0:
			S_always.usePosPulseMode = True
			
		# Deactivate passive processing #
		if S_action_changed and O_data["current_action"] == "aiming" and O_combat["timer_cock"] > 0.0:
			S_always.usePosPulseMode = False
		
		# When action is available
		if O_data["current_action"] == "aiming":
		
			### Reload ###
			if S_reloading_changed and O_combat["current_clip"] < O_combat["max_clip"] and O_combat["ammo_stock"] > 0:
				
				O_data["current_action"] = "reloading"
				O_combat["timer_reload"] = -reloading_time
				O_combat["timer_cock"] = -reloading_time - O_combat["cocking_time"]
				
		### Refill current_clip ###
		if O_armature.getActionName(2) == "player_body_reload" and O_armature.getActionFrame(2) > 40.0:
			
			# Decrease from ammo_stock to fill current _clip
			if O_combat["ammo_stock"] - (O_combat["max_clip"] - O_combat["current_clip"]) >= 0:
				
				O_combat["ammo_stock"] -= O_combat["max_clip"] - O_combat["current_clip"]
				O_combat["current_clip"] += O_combat["max_clip"] - O_combat["current_clip"]
				
				current_item["ammo_stock"] = O_combat["ammo_stock"]
				current_item["current_clip"] = O_combat["current_clip"]
				
			# Set remaining ammo_stock to current_clip
			if O_combat["ammo_stock"] - (O_combat["max_clip"] - O_combat["current_clip"]) < 0:
				
				O_combat["current_clip"] += O_combat["ammo_stock"]
				O_combat["ammo_stock"] = 0
				
				current_item["ammo_stock"] = O_combat["ammo_stock"]
				current_item["current_clip"] = O_combat["current_clip"]
	
		### Cocking ###
		if O_combat["timer_cock"] > -O_combat["cocking_time"] and O_combat["timer_cock"] < 0.0 and O_combat["timer_reload"] > 0.0:
			if O_data["current_action"] == "reloading" or O_data["current_action"] == "aiming":
				O_combat["timer_cock"] = -O_combat["cocking_time"]
				O_data["current_action"] = "cocking"
		
		### Aiming ###
		if O_data["current_action"] == "cocking" and O_combat["timer_cock"] > 0.0 and O_combat["timer_reload"] > 0.0:
			O_data["current_action"] = "aiming"
			
		
		
	pass


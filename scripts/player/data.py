import bge
from bge.logic import expandPath
from mathutils import Vector
from scripts.utils import *

""" This module contains all main data processing of the player, like changing properties used all around the game, initializing values, etc. """

################################ DATA ################################

def init_libs(cont):
	""" Initializes player libraries. Only called by init_all.
	
	SCENE: current level
	OBJECT: 'data'
	FREQUENCY: once """
	
	# Basic
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors[0].positive
	
	# Properties
	path = bge.logic.expandPath("//libs/")
	weapons = "resources/weapons.blend"
	actions = "actors/player.blend"
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		### Load libs ###
		if True:
			
			# Load weapon meshes
			bge.logic.LibLoad(path + weapons, "Mesh")
			print("weapons.blend meshes was successfully loaded")
			
			# Load player actions
			bge.logic.LibLoad(path + actions, "Action", load_actions=True)
			print("player.blend actions was successfully loaded")
			
	pass

def init_keys(cont):
	""" Initializes the game keys based on values of globalDict. Only called by init_all.
	
	SCENE: current level
	OBJECT: 'data'
	FREQUENCY: once """
	
	# Basic
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	S_always = cont.sensors[0].positive
	
	# Objects
	O_data = own
	O_collision = O_data.parent
	O_input = O_collision.childrenRecursive.get("input")
	
	# Properties
	player_status = globalDict["state"]["current_player"]["status"]
	sensors = O_input.sensors
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		### Set the game keys ###
		for key_sen in sensors:
			# For each keyboard sensor, change the key
			if type(key_sen) == bge.types.SCA_KeyboardSensor:
				key_sen.key = int(globalDict["options"]["keys"][key_sen.name])
					
		# Warning message
		print("Player key config applied to", player_status["name"])
		
	pass

def init_all(cont):
	""" Initializes player properties based on the current game state and stored settings, including game keys.
	
	SCENE: current level
	OBJECT: 'data'
	FREQUENCY: once """
	
	# Basic
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	S_always = cont.sensors[0].positive
	
	# Objects
	O_data = own
	O_collision = O_data.parent
	O_player_head = O_collision.childrenRecursive.get("player_head")
	O_player_body = O_collision.childrenRecursive.get("player_body")
	O_combat = O_collision.childrenRecursive.get("combat")
	O_input = O_collision.childrenRecursive.get("input")
	O_items = O_collision.childrenRecursive.get("items")
	
	# Properties
	current_player = globalDict["state"]["current_player"]
	player_status = globalDict["state"]["current_player"]["status"]
	sensors = O_input.sensors
	current_item = current_player["item_" + str(player_status["current_item"])]
	weapons = globalDict["database"]["weapons"]
	path = bge.logic.expandPath("//../libs/")
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		### Load libs ###
		init_libs(cont)
		
		### Set the game keys ###
		init_keys(cont)
		
		### Set the globalDict props to GameObject props ###
		if True:
			
			# Stats
			O_data["name"] = player_status["name"]
			O_data["color"] = player_status["color"]
			O_data["health"] = int(player_status["health"])
			O_data["current_item"] = int(player_status["current_item"])
			
			# Combat
			O_combat["name"] = current_item["name"]
			O_combat["type"] = weapons[current_item["name"]]["type"]
			O_combat["shot_time"] = float(weapons[current_item["name"]]["shot_time"])
			O_combat["cocking_type"] = int(weapons[current_item["name"]]["cocking_type"])
			O_combat["cocking_time"] = float(weapons[current_item["name"]]["cocking_time"])
			O_combat["current_clip"] = int(current_item["current_clip"])
			O_combat["max_clip"] = int(weapons[current_item["name"]]["max_clip"])
			O_combat["ammo_stock"] = int(current_item["ammo_stock"])
			O_combat["damage"] = int(weapons[current_item["name"]]["damage"])
		
		### Change player helmet's visor color ###
		if True:
			
			# Green
			if O_data["color"] == "Green":
				O_player_head.color = [0.0, 1.0, 0.0, 1.0]
				O_player_body.color = [0.0, 1.0, 0.0, 1.0]
				
			# Red
			if O_data["color"] == "Red":
				O_player_head.color = [1.0, 0.0, 0.0, 1.0]
				O_player_body.color = [1.0, 0.0, 0.0, 1.0]
				
			# Blue
			if O_data["color"] == "Blue":
				O_player_head.color = [0.0, 0.5, 1.0, 1.0]
				O_player_body.color = [0.0, 0.5, 1.0, 1.0]
				
			# Yellow
			if O_data["color"] == "Yellow":
				O_player_head.color = [1.0, 1.0, 0.0, 1.0]
				O_player_body.color = [1.0, 1.0, 0.0, 1.0]
				
			# Purple
			if O_data["color"] == "Purple":
				O_player_head.color = [1.0, 0.0, 1.0, 1.0]
				O_player_body.color = [1.0, 0.0, 1.0, 1.0]
				
			# Orange
			if O_data["color"] == "Orange":
				O_player_head.color = [1.0, 0.5, 0.0, 1.0]
				O_player_body.color = [1.0, 0.5, 0.0, 1.0]
				
			# Other
			if O_data["color"] == "None":
				O_player_head.color = [1.0, 1.0, 1.0, 1.0]
				O_player_body.color = [1.0, 1.0, 1.0, 1.0]
		
		### Warning message ###
		print("Config applied to player", player_status["name"])
	
	pass

def set_move_speed(cont):
	""" Speed transition of the move speed, smoothing the movement.
	
	SCENE: current level
	OBJECT: 'data'
	FREQUENCY: continuous """
	
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors["always_set_move_speed"]
	S_move_v_changed = cont.sensors["move_v_changed"].positive
	S_move_h_changed = cont.sensors["move_h_changed"].positive
	
	# Objects
	O_data = own
	O_collision = own.parent
	O_input = O_collision.childrenRecursive.get("input")
	
	# Properties
	move_speed_max = 0.1
	smooth_factor = 0.01
	
	############################
	######## INITIALIZE ########
	############################
	
	### Activate constant processing when pressing move buttons
	if S_move_v_changed or S_move_h_changed:
		if O_input["move_vertical"] != "none" or O_input["move_horizontal"] != "none":
			S_always.usePosPulseMode = True
	
	### Constant processing of move speed ###
	if S_always.positive and not O_data["is_busy"]:

		### Speed vertical ###
		if True:
			
			# Up
			if O_input["move_vertical"] == "up":
				
				# Walk
				if not O_input["is_running"]:
					
					# Raise if not at max speed
					if O_data["move_speed_v"] < move_speed_max - 0.0001:
						O_data["move_speed_v"] += smooth_factor
						
					# Lower if was running
					if O_data["move_speed_v"] > move_speed_max - 0.0001:
						O_data["move_speed_v"] -= smooth_factor
						
				# Run
				if O_input["is_running"]:
					if O_data["move_speed_v"] < move_speed_max * 2 - 0.0001:
						O_data["move_speed_v"] += smooth_factor
			
			# Down
			if O_input["move_vertical"] == "down":
				
				# Walk
				if not O_input["is_running"]:
					
					# Raise if not at max speed
					if O_data["move_speed_v"] > -move_speed_max + 0.0001:
						O_data["move_speed_v"] -= smooth_factor
						
					# Lower if was running
					if O_data["move_speed_v"] < -move_speed_max + 0.0001:
						O_data["move_speed_v"] += smooth_factor
					
				# Run
				if O_input["is_running"]:
					if O_data["move_speed_v"] > -move_speed_max * 2 + 0.0001:
						O_data["move_speed_v"] -= smooth_factor
			
			# Stop
			if O_input["move_vertical"] == "none":
				
				# Raise
				if O_data["move_speed_v"] < 0.0:
						O_data["move_speed_v"] += smooth_factor
						
				# Lower
				if O_data["move_speed_v"] > 0.0:
						O_data["move_speed_v"] -= smooth_factor
				
				# Fix when not 0
				if O_data["move_speed_v"] >= -smooth_factor and O_data["move_speed_v"] <= smooth_factor:
					O_data["move_speed_v"] = 0.0
		
		### Speed horizontal ###
		if True:
			# Right
			if O_input["move_horizontal"] == "right":
				
				# Walk
				if not O_input["is_running"]:
					
					# Raise if not at max speed
					if O_data["move_speed_h"] < move_speed_max - 0.0001:
						O_data["move_speed_h"] += smooth_factor
						
					# Lower if was running
					if O_data["move_speed_h"] > move_speed_max - 0.0001:
						O_data["move_speed_h"] -= smooth_factor
						
				# Run
				if O_input["is_running"]:
					if O_data["move_speed_h"] < move_speed_max * 2 - 0.0001:
						O_data["move_speed_h"] += smooth_factor
			
			# Left
			if O_input["move_horizontal"] == "left":
				
				# Walk
				if not O_input["is_running"]:
					
					# Raise if not at max speed
					if O_data["move_speed_h"] > -move_speed_max + 0.0001:
						O_data["move_speed_h"] -= smooth_factor
						
					# Lower if was running
					if O_data["move_speed_h"] < -move_speed_max + 0.0001:
						O_data["move_speed_h"] += smooth_factor
					
				# Run
				if O_input["is_running"]:
					if O_data["move_speed_h"] > -move_speed_max * 2 + 0.0001:
						O_data["move_speed_h"] -= smooth_factor
			
			# Stop
			if O_input["move_horizontal"] == "none":
				
				# Raise
				if O_data["move_speed_h"] < 0.0:
						O_data["move_speed_h"] += smooth_factor
						
				# Lower
				if O_data["move_speed_h"] > 0.0:
						O_data["move_speed_h"] -= smooth_factor
				
				# Fix when not 0
				if O_data["move_speed_h"] >= -smooth_factor and O_data["move_speed_h"] <= smooth_factor:
					O_data["move_speed_h"] = 0.0
					
		### Disable processing if not pressing move buttons ###
		if O_data["move_speed_h"] == 0.0 and O_data["move_speed_v"] == 0.0:
			
			if O_input["move_horizontal"] == "none" and O_input["move_vertical"] == "none":
				S_always.usePosPulseMode = False
		
	pass

################################ INPUT ################################

def input_to_props(cont):
	
	""" Sets the player properties based on input or interaction with other actors and elements.
	
	SCENE: current level
	OBJECT: 'input'
	FREQUENCY: input and interaction dependent """
	
	# Basic
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	S_up = cont.sensors["up"].positive
	S_down = cont.sensors["down"].positive
	S_left = cont.sensors["left"].positive
	S_right = cont.sensors["right"].positive
	S_run = cont.sensors["run"].positive
	S_use = cont.sensors["use"].positive
	S_reload = cont.sensors["reload"].positive
	S_item_1 = cont.sensors["item_1"].positive
	S_item_2 = cont.sensors["item_2"].positive
	S_item_3 = cont.sensors["item_3"].positive
	S_item_4 = cont.sensors["item_4"].positive
	S_shoot = cont.sensors["shoot"].positive
	
	# Objects
	O_input = own
	O_collision = own.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_combat = O_collision.childrenRecursive.get("combat")
	
	# Properties
	reload_time = 1.9
	is_local_player = O_data["name"] == globalDict["state"]["current_player"]["status"]["name"]
	
	############################
	######## INITIALIZE ########
	############################
	
	# Active events
	if not O_data["is_busy"] and is_local_player:
		
		### Item ###
		if O_data["current_action"] == "aiming" and O_combat["timer_cock"] > 0.0:
			
			# Item 1
			if S_item_1:
				O_data["current_item"] = 1
				globalDict["state"]["current_player"]["status"]["current_item"] = "1"
				
			# Item 2
			if S_item_2:
				O_data["current_item"] = 2
				globalDict["state"]["current_player"]["status"]["current_item"] = "2"
				
			# Item 3
			if S_item_3:
				O_data["current_item"] = 3
				globalDict["state"]["current_player"]["status"]["current_item"] = "3"
				
			# Item 4
			if S_item_4:
				O_data["current_item"] = 4
				globalDict["state"]["current_player"]["status"]["current_item"] = "4"
		
		### Move ###
		if True:
			
		### Vertical move ###
			# None
			if not S_up and not S_down or S_up and S_down:
				O_input["move_vertical"] = "none"
			# Up
			if S_up and not S_down:
				O_input["move_vertical"] = "up"
			# Down
			if not S_up and S_down:
				O_input["move_vertical"] = "down"
				
			### Horizontal move ###
			# None
			if not S_left and not S_right or S_left and S_right:
				O_input["move_horizontal"] = "none"
			# Left
			if S_left and not S_right:
				O_input["move_horizontal"] = "left"
			# Right
			if not S_left and S_right:
				O_input["move_horizontal"] = "right"
		
		### Run ###
		if True:
			# On
			if S_run:
				O_input["is_running"] = True
			# Off
			if not S_run:
				O_input["is_running"] = False
		
		### Use ###
		if True:
			# On
			if S_use:
				O_input["is_using"] = True
			# Off
			if not S_use:
				O_input["is_using"] = False
			
		### Shoot ###
		if True:
			
			# On
			if S_shoot:
				O_input["is_shooting"] = True
				
			# Off
			if not S_shoot:
				O_input["is_shooting"] = False
				
		### Reload ###
		if True:
			
			# On
			if S_reload:
				O_input["is_reloading"] = True
				
			# Off
			if not S_reload:
				O_input["is_reloading"] = False
				
	pass


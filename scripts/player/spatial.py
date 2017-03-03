import bge
from bge.logic import expandPath, LibList, LibLoad, LibFree
from mathutils import Vector
import sys

""" This module contains player behavior based on environment interaction and other things related to direct gameplay, like moving, camera behavior, etc. """

################################ PASSIVE ################################

def camera_collision(cont):
	""" Makes the player's camera avoid to pass through solid objects.
	
	SCENE: current level
	OBJECT: 'spatial'
	FREQUENCY: continuous """
	
	scene = bge.logic.getCurrentScene()
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	S_always = cont.sensors["always_camera_collision"]
	
	# Objects
	O_spatial = own
	O_collision = O_spatial.parent
	O_axis = O_collision.childrenRecursive.get("camera_axis")
	O_camera = O_collision.childrenRecursive.get("player_camera")
	O_focus = O_collision.childrenRecursive.get("camera_col_focus")
	O_root = O_collision.childrenRecursive.get("camera_root")
	O_data = O_collision.childrenRecursive.get("data")
	
	# Variables
	distance = O_focus.getDistanceTo(O_root) # Distance between cam_col_focus and cam_root
	ray = O_focus.rayCast(O_root, O_focus, distance + 0.05, "obstacle", 0, 1) # Returns tuple (hit object, collision hitpoint, etc)
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always.positive:
		
		# Set camera to ray hit position if obstacle detected
		if ray[0] != None:
			O_camera.worldPosition = ray[1]
			O_camera.localPosition = O_camera.localPosition - Vector((0.01, 0.05, 0.0))
			
		# Set camera to root position if obstacle is not detected
		elif ray[0] == None:
			O_camera.worldPosition = O_root.worldPosition
		
	pass

################################ ACTIVE ################################

def move(cont):
	""" Moves the player through the environment.
	
	SCENE: current level
	OBJECT: 'spatial'
	FREQUENCY: continuous """
	
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors["always_move"]
	S_move_v_changed = cont.sensors["move_v_changed"].positive
	S_move_h_changed = cont.sensors["move_h_changed"].positive
	S_running_changed = cont.sensors["running_changed"].positive
	
	# Objects
	O_spatial = own
	O_collision = O_spatial.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_input = O_collision.childrenRecursive.get("input")
	
	# Properties
	speed_factor = 0.32
	diagonal_factor = 0.75
	
	############################
	######## INITIALIZE ########
	############################
	
	### Activate constant processing when pressing move buttons
	if S_move_v_changed or S_move_h_changed:
		
		if O_input["move_vertical"] != "none" or O_input["move_horizontal"] != "none":
			S_always.usePosPulseMode = True
	
	if S_always.positive:
		
		### Linear move ###
		if O_input["move_horizontal"] == "none" and O_input["move_vertical"] != "none" or O_input["move_horizontal"] != "none" and O_input["move_vertical"] == "none" or O_input["move_horizontal"] == "none" and O_input["move_vertical"] == "none":
			
			# Move player_collision with smooth provided by move_speed properties
			O_collision.applyMovement([-O_data["move_speed_h"] * speed_factor, -O_data["move_speed_v"] * speed_factor, 0.0], True)
			
		### Diagonal move ###
		if O_input["move_horizontal"] != "none" and O_input["move_vertical"] != "none":
			
			# Move player_collision with smooth provided by move_speed properties
			O_collision.applyMovement([-O_data["move_speed_h"] * (speed_factor * diagonal_factor), -O_data["move_speed_v"] * (speed_factor * diagonal_factor), 0.0], True)
			
		### Disable processing if not pressing move buttons ###
		if O_data["move_speed_h"] == 0.0 and O_data["move_speed_v"] == 0.0:
			
			if O_input["move_horizontal"] == "none" and O_input["move_vertical"] == "none":
				S_always.usePosPulseMode = False
		
	pass
	
def mouse_look(cont):
	""" Processes the mouse look of the player and updates.
	
	SCENE: current level
	OBJECT: 'spatial'
	FREQUENCY: mouse input dependent """
	
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	S_mouse = cont.sensors["mouse"].positive
	S_always = cont.sensors["always_mouse_look"]
	
	# Actuators
	A_mouse_x = cont.actuators["mouse_x"]
	A_mouse_y = cont.actuators["mouse_y"]
	A_look_vertical = cont.actuators["look_vertical"]
	
	# Objects
	O_spatial = own
	O_collision = own.parent
	O_armature = O_collision.childrenRecursive.get("player_armature")
	O_combat = O_collision.childrenRecursive.get("combat")
	O_data = O_collision.childrenRecursive.get("data")
	
	# Properties
	mouse_sensitivity = float(globalDict["options"]["controls"]["mouse_sensitivity"])
	is_local_player = O_data["name"] == globalDict["state"]["current_player"]["status"]["name"]
	
	############################
	######## INITIALIZE ########
	############################
	
	if is_local_player:
	
		### Activate passive processing when not moving mouse ###
		if not S_mouse and not S_always.usePosPulseMode:
			S_always.usePosPulseMode = True
		
		### Deactivate passive processing when moving mouse ###
		if S_mouse and S_always.usePosPulseMode:
			S_always.usePosPulseMode = False
		
		### If not busy ###
		if not O_data["is_busy"]:
		
			### If in passive processing or mouse moving ###
			if S_always.positive or S_mouse:
				
				### Set mouse sensitivity from options ###
				if True:
					
					# mouse_x
					if A_mouse_x.sensitivity != [mouse_sensitivity, mouse_sensitivity]:
						A_mouse_x.sensitivity = [mouse_sensitivity, mouse_sensitivity]
						
					# mouse_y
					if A_mouse_y.sensitivity != [-mouse_sensitivity, -mouse_sensitivity]:
						A_mouse_y.sensitivity = [-mouse_sensitivity, -mouse_sensitivity]
				
				### Activate the mouse_x ###
				if True:
					cont.activate(A_mouse_x)
					cont.activate(A_mouse_y)
					
				### Set mouse_y property value
				if True:
					O_armature["mouse_y"] = -A_mouse_y.angle[1] + A_mouse_y.limit_y[1] + 1.0
			
			### Process armature look
			if O_data["current_action"] == "aiming":
				
				### Fireweapon ###
				if O_combat["type"] == "fireweapon":
					A_look_vertical.action = "player_body_aim_fireweapon"
					
				### Grenade ###
				if O_combat["type"] == "grenade":
					A_look_vertical.action = "player_body_aim_grenade"
					
				cont.activate(A_look_vertical)
		
	pass

def load_chunks(cont):
	""" This function is intended to load parts of the scenery (named chunks) dynamically based on player position in the world, and this way, being possible to make open world games easily.
	Each part of the scenery is a blend file, named according to its coordinate (in a scale of 50 X 50 meters).
	
	SCENE: current level
	OBJECT: 'spatial'
	FREQUENCY: collision with chunk area dependent """
	
	own = cont.owner
	maps = expandPath("//map/")
	ext = ".blend"
	
	# Sensors
	S_always = cont.sensors["always_load_chunks"]
	S_in_chunk = cont.sensors["in_chunk"]
	
	# Objects
	O_collision = own.parent
	
	# Properties
	P_async = True
	
	def gen_chunk_name(coords_list):
		"""  Generates a string name of the map chunk, in the format "001_002". """
		
		return str("chunk_" + str(coords_list[0]).zfill(3) + "_" + str(coords_list[1]).zfill(3))
		
	############################
	######## INITIALIZE ########
	############################
	
	### Load the adjacent chunks when inside a chunk ###
	if S_in_chunk.positive:
		
		# Chunks
		chunk_current = [S_in_chunk.hitObject["coord_x"], S_in_chunk.hitObject["coord_y"]]
		chunk_nw = [chunk_current[0] - 1, chunk_current[1] + 1] # Northwest
		chunk_n = [chunk_current[0], chunk_current[1] + 1] # North
		chunk_ne = [chunk_current[0] + 1, chunk_current[1] + 1] # Northeast
		chunk_w	= [chunk_current[0] - 1, chunk_current[1]] # West
		chunk_e = [chunk_current[0] + 1, chunk_current[1]] # East
		chunk_sw = [chunk_current[0] - 1, chunk_current[1] - 1] # Southwest
		chunk_s = [chunk_current[0], chunk_current[1] - 1] # South
		chunk_se = [chunk_current[0] + 1, chunk_current[1] - 1] # Southeast
		
		# Set current chunk properties in player
		O_collision["current_chunk_x"] = chunk_current[0]
		O_collision["current_chunk_y"] = chunk_current[1]
		
		### Load chunks ###
		if True:
			
			# Current
			if not (maps + gen_chunk_name(chunk_current) + ext) in LibList():
				LibLoad(maps + gen_chunk_name(chunk_current) + ext, "Scene", async = True, load_actions = True)
			
			# Northwest
			if S_in_chunk.hitObject["northwest"] and not (maps + gen_chunk_name(chunk_nw) + ext) in LibList():
				LibLoad(maps + gen_chunk_name(chunk_nw) + ext, "Scene", async = P_async, load_actions = True)
				
			# North
			if S_in_chunk.hitObject["north"] and not (maps + gen_chunk_name(chunk_n) + ext) in LibList():
				LibLoad(maps + gen_chunk_name(chunk_n) + ext, "Scene", async = P_async, load_actions = True)
				
			# Northeast
			if S_in_chunk.hitObject["northeast"] and not (maps + gen_chunk_name(chunk_ne) + ext) in LibList():
				LibLoad(maps + gen_chunk_name(chunk_ne) + ext, "Scene", async = P_async, load_actions = True)
				
			# West
			if S_in_chunk.hitObject["west"] and not (maps + gen_chunk_name(chunk_w) + ext) in LibList():
				LibLoad(maps + gen_chunk_name(chunk_w) + ext, "Scene", async = P_async, load_actions = True)
				
			# East
			if S_in_chunk.hitObject["east"] and not (maps + gen_chunk_name(chunk_e) + ext) in LibList():
				LibLoad(maps + gen_chunk_name(chunk_e) + ext, "Scene", async = P_async, load_actions = True)
				
			# Southwest
			if S_in_chunk.hitObject["southwest"] and not (maps + gen_chunk_name(chunk_sw) + ext) in LibList():
				LibLoad(maps + gen_chunk_name(chunk_sw) + ext, "Scene", async = P_async, load_actions = True)
				
			# South
			if S_in_chunk.hitObject["south"] and not (maps + gen_chunk_name(chunk_s) + ext) in LibList():
				LibLoad(maps + gen_chunk_name(chunk_s) + ext, "Scene", async = P_async, load_actions = True)
				
			# Southeast
			if S_in_chunk.hitObject["southeast"] and not (maps + gen_chunk_name(chunk_se) + ext) in LibList():
				LibLoad(maps + gen_chunk_name(chunk_se) + ext, "Scene", async = P_async, load_actions = True)
				
			# Warning message
			print("Loaded adjacents of " + str(O_collision["current_chunk_x"]) + "_" + str(O_collision["current_chunk_y"]) + ext)
		
		### Free unused chunks ###
		# Iterate over loaded libs
		
		for lib in LibList():
			
			# Check if libs have coordinates in its names
			if "\map\chunk_" in lib:
					
				lib_coords = [int(lib[-13:-10]), int(lib[-9:-6])]
				
				# Check if lib is 2 chunks away from current coordinates
				if O_collision["current_chunk_x"] > lib_coords[0] + 1 or O_collision["current_chunk_x"] < lib_coords[0] - 1 or O_collision["current_chunk_y"] > lib_coords[1] + 1 or O_collision["current_chunk_y"] < lib_coords[1] - 1:
					
					# Free chunk and warn through message
					LibFree(lib)
					print("Freed", lib[-13:])
					
	### If not in a chunk area ###
	if not S_in_chunk.positive:
		print("Not in chunk area")

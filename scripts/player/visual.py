import bge
from bge.logic import expandPath
from mathutils import Vector
from scripts.utils import *

""" This module contains visual events of the player, like animations, mesh replacing, etc. """

################################ ANIMATION ################################

def anim_legs(cont):
	""" Animates the player legs based on the current properties.
	
	SCENE: current level
	OBJECT: 'visual'
	FREQUENCY: property change dependent """
	
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors["always_anim_legs"]
	S_move_v_changed = cont.sensors["move_v_changed"].positive
	S_move_h_changed = cont.sensors["move_h_changed"].positive
	S_running_changed = cont.sensors["running_changed"].positive
	
	# Actuators
	A_legs = cont.actuators["legs"]
	
	# Objects
	O_visual = own
	O_collision = O_visual.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_input = O_collision.childrenRecursive.get("input")
	
	# Properties
	move_vertical = O_input["move_vertical"]
	move_horizontal = O_input["move_horizontal"]
	is_running = O_input["is_running"]
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always.positive and not O_data["is_busy"]:
		
		### Idle ###
		if move_vertical == "none" and move_horizontal == "none":
			A_legs.action = "player_legs_idle"
			A_legs.frameStart, A_legs.frameEnd = 1.0, 39.0
			cont.activate(A_legs)
		
		### Walk ###
		if not is_running:
			
			### Linear ###
			# Forward
			if move_vertical == "up" and move_horizontal == "none":
				A_legs.action = "player_legs_walk_fw"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Backward
			if move_vertical == "down" and move_horizontal == "none":
				A_legs.action = "player_legs_walk_bw"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Left
			if move_vertical == "none" and move_horizontal == "left":
				A_legs.action = "player_legs_walk_L"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Right
			if move_vertical == "none" and move_horizontal == "right":
				A_legs.action = "player_legs_walk_R"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			### Diagonal ###
			# Forward left
			if move_vertical == "up" and move_horizontal == "left":
				A_legs.action = "player_legs_walk_fwL"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Forward right
			if move_vertical == "up" and move_horizontal == "right":
				A_legs.action = "player_legs_walk_fwR"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Backward left
			if move_vertical == "down" and move_horizontal == "left":
				A_legs.action = "player_legs_walk_bwL"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Backward right
			if move_vertical == "down" and move_horizontal == "right":
				A_legs.action = "player_legs_walk_bwR"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
		
		### Run ###
		if is_running:
			
			### Linear ###
			# Forward
			if move_vertical == "up" and move_horizontal == "none":
				A_legs.action = "player_legs_run_fw"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Backward
			if move_vertical == "down" and move_horizontal == "none":
				A_legs.action = "player_legs_run_bw"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Left
			if move_vertical == "none" and move_horizontal == "left":
				A_legs.action = "player_legs_run_L"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 17.0
				cont.activate(A_legs)
				
			# Right
			if move_vertical == "none" and move_horizontal == "right":
				A_legs.action = "player_legs_run_R"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 17.0
				cont.activate(A_legs)
				
			### Diagonal ###
			# Forward left
			if move_vertical == "up" and move_horizontal == "left":
				A_legs.action = "player_legs_run_fwL"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Forward right
			if move_vertical == "up" and move_horizontal == "right":
				A_legs.action = "player_legs_run_fwR"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Backward left
			if move_vertical == "down" and move_horizontal == "left":
				A_legs.action = "player_legs_run_bwL"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
			# Backward right
			if move_vertical == "down" and move_horizontal == "right":
				A_legs.action = "player_legs_run_bwR"
				A_legs.frameStart, A_legs.frameEnd = 1.0, 16.0
				cont.activate(A_legs)
				
	pass

def anim_body(cont):
	""" Animates the player body based on the current properties.
	
	SCENE: current level
	OBJECT: 'visual'
	FREQUENCY: property change dependent """
	
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors["always_anim_body"]
	S_using_changed = cont.sensors["using_changed"].positive
	S_shooting_changed = cont.sensors["shooting_changed"].positive
	S_reloading_changed = cont.sensors["reloading_changed"].positive
	S_action_changed = cont.sensors["action_changed"].positive
	
	# Actuators
	A_body = cont.actuators["body"]
	
	# Objects
	O_visual = own
	O_collision = own.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_combat = O_collision.childrenRecursive.get("combat")
	O_armature = O_collision.childrenRecursive.get("player_armature")
	O_input = O_collision.childrenRecursive.get("input")
	
	# Properties
	shooting = O_input["is_shooting"] == True
	aiming = O_data["current_action"] == "aiming"
	reloading = O_data["current_action"] == "reloading"
	cocking = O_data["current_action"] == "cocking"
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always.positive:
		
		### Weapon animations ###
		if S_action_changed:
			
			# Aiming
			if aiming and not O_armature.isPlayingAction(2):
				cont.deactivate(A_body)
			
			# Reloading
			if reloading:
				A_body.action = "player_body_reload"
				A_body.frameStart = 1.0
				A_body.frameEnd = 55.0
				cont.activate(A_body)
				
			# Cocking
			if cocking:
				
				# Type 1
				if O_combat["cocking_type"] == 1:
					A_body.action = "player_body_cocking_1"
					A_body.frameStart = 1.0
					A_body.frameEnd = 20.0
					cont.activate(A_body)
					
				# Type 2
				if O_combat["cocking_type"] == 2:
					A_body.action = "player_body_cocking_2"
					A_body.frameStart = 1.0
					A_body.frameEnd = 15.0
					cont.activate(A_body)
	
	pass

################################ SKIN ################################

def set_color(cont):
	""" Sets the color of the object. Usually, the object has the option "Object color" checked in materials tab.
	
	SCENE: current level
	OBJECT: any with custom color
	FREQUENCY: once """
	
	# Basic
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors[0]
	
	# Colors
	red = [1.0, 0.0, 0.0, 1.0]
	green = [0.0, 1.0, 0.0, 1.0]
	blue = [0.0, 0.0, 1.0, 1.0]
	gold = [1.0, 0.5, 0.0, 1.0]
	black = [0.0, 0.0, 0.0, 1.0]
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always.positive and "color" in own:
		
		# Red
		if own["color"] == "red":
			own.color = red
			
		# Green
		if own["color"] == "green":
			own.color = green
		
		# Blue
		if own["color"] == "blue":
			own.color = blue
			
		# Gold
		if own["color"] == "gold":
			own.color = gold
		
		# Black
		if own["color"] == "black":
			own.color = black
		
	pass

def set_item_gfx(cont):
	""" Changes the item_slot mesh based on current_item property.
	
	SCENE: current level
	OBJECT: 'visual'
	FREQUENCY: property change dependent """
	
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors["always_set_item_gfx"]
	S_item_changed = cont.sensors["item_changed"].positive
	
	# Objects
	O_visual = own
	O_collision = own.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_combat = O_collision.childrenRecursive.get("combat")
	O_item_slot = O_collision.childrenRecursive.get("item_slot")
	
	# Properties
	globalDict = bge.logic.globalDict
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always.positive or S_item_changed:
		
		equip_item = O_combat["name"]
		
		### Get currently equiped item ###
		if S_item_changed:
			
			# Item slot
			if O_data["current_item"] != 0:
				equip_item = O_combat["name"]
				
		### Replace mesh ###
		# None
		if equip_item == "none":
			O_item_slot.replaceMesh("item_slot")
		
		# Weapon mesh
		if equip_item != "none":
			O_item_slot.replaceMesh("msh_" + equip_item)
		
	pass

################################ EFFECTS ################################
	
def shot_flash(cont):
	""" Shows the visual representation of shot flash and shells.
	
	SCENE: current level
	OBJECT: 'visual'
	FREQUENCY: continuous """
	
	# Basic
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors["always_shot_flash"]
	S_clip_changed = cont.sensors["clip_changed"].positive
	
	# Objects
	O_visual = own
	O_collision = O_visual.parent
	O_data = O_collision.childrenRecursive.get("data")
	O_input = O_collision.childrenRecursive.get("input")
	O_shot_light = O_collision.childrenRecursive.get("shot_light")
	O_shot_flash_01 = O_collision.childrenRecursive.get("shot_flash_01")
	O_combat = O_collision.childrenRecursive.get("combat")
	
	# Actuators
	A_bullet_shell = cont.actuators["bullet_shell"]
	
	# Properties
	has_ammo = between(O_combat["current_clip"], -1, O_combat["max_clip"])
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always.positive:
		
		# Enable flash time and pulse processing
		if S_clip_changed and O_data["current_action"] == "aiming" and O_input["is_shooting"] and has_ammo:
			cont.activate(A_bullet_shell)
			O_visual["flash_time"] = -0.12
			S_always.usePosPulseMode = True
			
		# Turn on light / flash mesh and gradually fade out
		if O_visual["flash_time"] < 0.0:
			O_shot_light.energy = -O_visual["flash_time"] * 20
			O_shot_flash_01.color = [1.0, 1.0 ,1.0, -O_visual["flash_time"] * 10]
			
		# Turn off light / flash mesh and disable processing
		if O_visual["flash_time"] > 0.0:
			O_shot_light.energy = 0.0
			O_shot_flash_01.color = [1.0, 1.0 ,1.0, 0.0]
			S_always.usePosPulseMode = False
		
	pass

def laser_sight(cont):
	""" Makes the player's laser_sight follow the current hit point in scene.
	
	SCENE: current level
	OBJECT: 'visual'
	FREQUENCY: continuous """
	
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors["always_laser_sight"]
	S_mouse = cont.sensors["mouse"].positive
	S_action_changed = cont.sensors["action_changed"].positive
	S_ray = cont.sensors["ray"]
	S_timer_positive = cont.sensors["timer_positive"].positive
	
	# Objects
	O_visual = own
	O_collision = O_visual.parent
	O_combat = O_collision.childrenRecursive.get("combat")
	O_data = O_collision.childrenRecursive.get("data")
	O_laser_sight = O_collision.childrenRecursive.get("laser_sight")
	O_shot_origin = O_collision.childrenRecursive.get("shot_origin")
	O_laser_sight_point = O_collision.childrenRecursive.get("laser_sight_point")
	
	ray_range = 20.0
	
	############################
	######## INITIALIZE ########
	############################
	
	### Process ###
	if S_mouse or S_always.positive:
		
		### Disable passive processing ###
		if S_mouse:
			S_always.usePosPulseMode = False
			
		### Enable passive processing ###
		if not S_mouse:
			S_always.usePosPulseMode = True
		
		# Set the ray range
		if S_ray.range != ray_range:
			S_ray.range = ray_range
		
		### Only process if aiming ###
		if O_data["current_action"] == "aiming" and S_timer_positive:
			
			# Set laser visible, if not already
			if not O_laser_sight.visible: 
				O_laser_sight.visible = True
			
			### If not objects colliding ###
			if S_ray.hitObject == None:
				O_laser_sight.localScale[1] = ray_range
				O_laser_sight_point.visible = False
			
			### If object detected ###
			if S_ray.hitObject != None:
				
				# Set point visible
				if not O_laser_sight_point.visible:
					O_laser_sight_point.visible = True
				
				# Scale laser_sight to distance to hitpoint
				O_laser_sight.localScale[1] = O_shot_origin.getDistanceTo(S_ray.hitPosition)
				
				# Set laser_sight_point to position of hitpoint
				O_laser_sight_point.worldPosition = S_ray.hitPosition
				O_laser_sight_point.localPosition[1] += 0.025
				
	### Dont process if not aiming ###
	if S_action_changed and O_data["current_action"] != "aiming" and not S_timer_positive:
		
		# Disable visual of laser
		O_laser_sight.visible = False
		O_laser_sight_point.visible = False
			
	pass
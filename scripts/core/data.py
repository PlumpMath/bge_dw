import bge
import aud
import configparser
import os

""" This module stores and processes global game data. It manages global variables, game options, save games, loads sound data to memory, etc. """

def init_config(cont):
	
	"""	Initializes the basic template for load the rest of game config. It simply organizes the globalDict into several dictionaries to access specific data.
	
	SCENE: 'global_data'
	OBJECT: 'config_loader'
	FREQUENCY: once """
	
	own = cont.owner
	globalDict = bge.logic.globalDict
	path = bge.logic.expandPath("//")
	parser = configparser.ConfigParser()
	
	# Sensors
	S_always = cont.sensors[0].positive
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
	
		# Game options (default)
		options_game = {"crosshair_color" : "White",
		"language" : "en"}
		
		options_graphics = {"resolution_w" : 1366,
		"resolution_h" : 768,
		"fullscreen" : 0}
		
		options_controls = {"mouse_sensitivity" : 1.0}
		
		options_keys = {"up" : 45, "down" : 41, "left" : 23, "right" : 26, "run" : 55, "use" : 27, "reload" : 40, "shoot" : 116,"item_1" : 14, "item_2" : 15, "item_3" : 16, "item_4" : 17}
		
		options_sound = {"sfx_volume" : 1.0,
		"ambience_volume" : 0.3,
		"music_volume" : 0.8}
	
		### Load and set options ###
		if not "options" in globalDict:
			
			try:
				# Open ini file to retrieve options
				with open(path + "options.ini", "r") as cfg:
					
					# Read options
					parser.read_file(cfg)
					
					# Set each option to its variable
					options_game = dict(parser.items("game"))
					options_graphics = dict(parser.items("graphics"))
					options_sound = dict(parser.items("sound"))
					options_controls = dict(parser.items("controls"))
					options_keys = dict(parser.items("keys"))
					
					print("Options loaded from options.ini")
					
			# If can't retrieve options
			except:
				
				# Warning message
				print("Failed to load options.ini, write and use default")
				
				# Try to create default file
				with open(path + "options.ini", 'w') as cfg:
					
					# Add default values to parser
					parser["game"] = options_game
					parser["graphics"] = options_graphics
					parser["sound"] = options_sound
					parser["controls"] = options_controls
					parser["keys"] = options_keys
					
					# Write game_options.ini to default
					parser.write(cfg)
		
		### Init globalDict ###
		if not "options" in globalDict:
			
			globalDict["options"] = {"game" : options_game,
			"graphics" : options_graphics, "controls" : options_controls, "sound" : options_sound, "keys" : options_keys}
			
	pass

def init_strings(cont):
	
	"""	Initializes the game strings. The strings are used on text around the game, like menus, subtitles, etc, and are loaded according to its respective language.
	
	SCENE: 'global_data'
	OBJECT: 'config_loader'
	FREQUENCY: once """
	
	own = cont.owner
	globalDict = bge.logic.globalDict
	path = bge.logic.expandPath("//lang/")
	parser = configparser.ConfigParser()
	lang = globalDict["options"]["game"]["language"]
	
	# Sensors
	S_always = cont.sensors[0].positive
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		### Game Strings default (English) ###
		
		# Common strings
		menu_common = {"ok" : "Ok",
		"cancel" : "Cancel",
		"next" : "Next",
		"previous" : "Previous",
		"continue" : "Continue",
		"player_name" : "Soldier Name",
		"ammo" : "Ammo"}
		
		# Main menu strings
		menu_main = {"campaign" : "Campaign",
		"desc_campaign" : "Play a campaign in story mode.",
		"multiplayer" : "Multiplayer",
		"desc_multiplayer" : "Play with other players on LAN or around the world.",
		"options" : "Options",
		"desc_options" : "Change the general game options.",
		"quit" : "Quit",
		"desc_quit" : "Quit Dark War... No one will miss you."}
		
		# Options menu strings
		menu_options = {"game" : "Game",
		"desc_game" : "General game options, like language and gameplay.",
		"graphics" : "Graphics",
		"desc_graphics" : "Graphic options, like resolution and other.",
		"sound" : "Sound",
		"desc_sound" : "Sound options, like volumes, disable / enable SFX and music.",
		"controls" : "Controls",
		"desc_controls" : "General controls options, like mouse and keys assignments."}
		
		# Game options menu strings
		menu_game = {"crosshair_color" : "Crosshair Color",
		"desc_crosshair_color" : "Choose the in-game crosshair color.",
		"language" : "Language",
		"desc_language" : "Choose the game language, from menus to subtitles."}
		
		# Graphic options menu strings
		menu_graphics = {"resolution" : "Resolution",
		"desc_resolution" : "Select the desired game screen resolution.",
		"fullscreen" : "Fullscreen",
		"desc_fullscreen" : "Choose if run game in fullscreen or windowed mode."}
		
		# Control options menu strings
		menu_controls = {"mouse_sensitivity" : "Mouse Sensitivity",
		"desc_mouse_sensitivity" : "Change the sensitivity of the mouse aim.",
		"up" : "Up Button",
		"down" : "Down Button",
		"left" : "Left Button",
		"right" : "Right Button",
		"use" : "Use Button",
		"run" : "Run Button",
		"reload" : "Reload Button",
		"item_1" : "Item 1 Button",
		"item_2" : "Item 2 Button",
		"item_3" : "Item 3 Button",
		"item_4" : "Item 4 Button",
		"desc_advice_key" : "Click on the key to change its assignment.",
		"desc_press_key" : "Press the desired key..."}
		
		# Campaign menu strings
		menu_campaign = {"player_create" : "Create Soldier",
		"desc_player_create" : "Create a new soldier to start the campaign.",
		"player_change" : "Change Soldier",
		"desc_player_change" : "Load an previously created soldier."}
		
		# Player menu strings
		menu_player = {"zone_current" : "Current Zone",
		"desc_zone_play" : "Go into the current zone.",
		"equip_current" : "Your current equipment includes this."}
		
		### Load or write strings ###
		if not "strings" in globalDict:
			
			try:
				# Open ini file to retrieve strings
				with open(path + lang + ".ini", "r") as ini:
					
					# Read strings
					parser.read_file(ini)
					
					# Set each string section to its variable
					menu_common = dict(parser.items("menu_common"))
					menu_main = dict(parser.items("menu_main"))
					menu_options = dict(parser.items("menu_options"))
					menu_game = dict(parser.items("menu_game"))
					menu_graphics = dict(parser.items("menu_graphics"))
					menu_controls = dict(parser.items("menu_controls"))
					menu_campaign = dict(parser.items("menu_campaign"))
					menu_player = dict(parser.items("menu_player"))
					
					print("Strings loaded from", lang + ".ini")
					
			# If can't retrieve strings
			except:
				
				# Warning message
				print("Failed to load " + lang + ".ini, write and use default strings")
				
				# Try to create default file
				with open(path + lang + ".ini", 'w') as ini:
					
					# Add default values to parser
					parser["menu_common"] = menu_common
					parser["menu_main"] = menu_main
					parser["menu_options"] = menu_options
					parser["menu_game"] = menu_game
					parser["menu_graphics"] = menu_graphics
					parser["menu_controls"] = menu_controls
					parser["menu_campaign"] = menu_campaign
					parser["menu_player"] = menu_player
					
					# Write game_options.ini to default
					parser.write(ini)
		
			### Initialize globalDict ###
			globalDict["strings"] = {}
			globalDict["strings"]["menu_main"] = menu_main
			
	pass

def init_player(cont):
	
	"""	Loads the player saved data
	
	SCENE: 'global_data'
	OBJECT: 'config_loader'
	FREQUENCY: once """
	
	own = cont.owner
	globalDict = bge.logic.globalDict
	path = bge.logic.expandPath("//save/")
	parser = configparser.ConfigParser()
	
	# Sensors
	S_always = cont.sensors[0].positive
	
	# Properties
	saved_games = []
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		# Game state (default)
		player_status = {"name" : "No Name",
		"color" : "None",
		"health" : "100",
		"current_item" : "1",
		"current_level" : "1"}
		
		player_item_1 = {"name" : "none",
		"current_clip" : "0",
		"ammo_stock" : "0"}
		
		player_item_2 = {"name" : "none",
		"current_clip" : "0",
		"ammo_stock" : "0"}
		
		player_item_3 = {"name" : "none",
		"current_clip" : "0",
		"ammo_stock" : "0"}
		
		player_item_4 = {"name" : "none",
		"current_clip" : "0",
		"ammo_stock" : "0"}
		
		### Adds all savegames to list of saved games
		for file in os.listdir(path):
			if file.endswith(".ini"):
				saved_games.append(file)
				
		### Open first saved game ###
		with open(path + saved_games[0], "r") as save_file:
			
			# Read savegame file
			parser.read_file(save_file)
			
			# Set properties from savegame file
			player_status = dict(parser.items("status"))
			player_item_1 = dict(parser.items("item_1"))
			player_item_2 = dict(parser.items("item_2"))
			player_item_3 = dict(parser.items("item_3"))
			player_item_4 = dict(parser.items("item_4"))
			
		player = {"status" : player_status,
		"item_1" : player_item_1,
		"item_2" : player_item_2,
		"item_3" : player_item_3,
		"item_4" : player_item_4}
		
		### Load and set options ###
		if not "state" in globalDict:
			globalDict["state"] = {"loaded_player" : player,
			"current_player" : player}
			
		# Warning message
		print("Player", globalDict["state"]["loaded_player"]["status"]["name"] ,"loaded from", saved_games[0])
		
	pass

def init_resources(cont):
	""" Loads reusable game resources, like meshes, sounds, etc.
	
	SCENE: global_data
	OBJECT: 'data_storage'
	FREQUENCY: once """
	
	own = cont.owner
	path = bge.logic.expandPath("//libs/resources/")
	
	# Sensors
	S_always = cont.sensors[0]
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		### Load weapons mesh libraries
		if True:
			weapons = bge.logic.LibLoad(path + "weapons.blend", "Mesh")
			print("weapons.blend was successfully loaded")
			
	pass
	
def init_database(cont):
	
	"""	Initializes the game database, like weapons, enemies and environment infos. All data is read from .ini files in config/database.
	
	SCENE: 'global_data'
	OBJECT: 'config_loader'
	FREQUENCY: once """
	
	own = cont.owner
	globalDict = bge.logic.globalDict
	path = bge.logic.expandPath("//database/")
	database_parser = configparser.ConfigParser()
	
	# Sensors
	S_always = cont.sensors[0].positive
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		### Init globalDict database keys ###
		if not "database" in globalDict:
			globalDict["database"] = {}
		
		### Load weapons ###
		with open( path + "weapons.ini", "r" ) as file:
			
			# Read file
			database_parser.read_file(file)
			
			# Add values to variables
			shotgun = dict(database_parser.items("shotgun"))
			shotgun_2_barrel = dict(database_parser.items("shotgun_2_barrel"))
			shotgun_auto = dict(database_parser.items("shotgun_auto"))
			submachinegun = dict(database_parser.items("submachinegun"))
			assault_rifle = dict(database_parser.items("assault_rifle"))
			laser_rifle = dict(database_parser.items("laser_rifle"))
			grenade_rifle = dict(database_parser.items("grenade_rifle"))
			flamer = dict(database_parser.items("flamer"))
			railgun = dict(database_parser.items("railgun"))
			grenade = dict(database_parser.items("grenade"))
			grenade_cluster = dict(database_parser.items("grenade_cluster"))
			grenade_napalm = dict(database_parser.items("grenade_napalm"))
			grenade_eraser = dict(database_parser.items("grenade_eraser"))
			
			# Add data to corresponding section in globalDict
			globalDict["database"]["weapons"] = {"shotgun" : shotgun,
			"shotgun_2_barrel" : shotgun_2_barrel,
			"shotgun_auto" : shotgun_auto,
			"submachinegun" : submachinegun,
			"assault_rifle" : assault_rifle,
			"laser_rifle" : laser_rifle,
			"grenade_rifle" : grenade_rifle,
			"flamer" : flamer,
			"railgun" : railgun,
			"grenade" : grenade,
			"grenade_cluster" : grenade_cluster,
			"grenade_napalm" : grenade_napalm,
			"grenade_eraser" : grenade_eraser}
			
			print("Weapons database loaded from weapons.ini")
			
	pass
	
def init_globalDict(cont):
	
	"""	Executes all the previous loader functions.
	
	SCENE: 'global_data'
	OBJECT: 'config_loader'
	FREQUENCY: once """
	
	own = cont.owner
	
	# Sensors
	S_always = cont.sensors[0].positive
	path = bge.logic.expandPath("//map/")
	
	############################
	######## INITIALIZE ########
	############################
	
	if S_always:
		
		init_config(cont)
		init_strings(cont)
		init_player(cont)
		init_database(cont)
		
		bge.logic.addScene("game_map", True)












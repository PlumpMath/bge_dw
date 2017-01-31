""" This file contains reference help for the inner game content. Using a text editor with code folding you can navigate this file easily. Classes are topics, variable identifiers are subjects and variable values are its descriptions. """

class globalDict:
	""" At game start, global data are loaded to globalDict using different loaders. This data can be accessed at any time, and is a complex dictionary organized in different levels. The globalDict keys are the following. """
	
	class state:
		""" The current game state, defining the data to be constantly updated when the game is running. """
		
		class current_player:
			""" The current_player data is updated according to the gameplay and player actions. If player dies or exits the level, current_player is overwritten by loaded_player. """
			
			class status:
				""" General player status, like player name, health, skin color, current level in campaign, current item held, etc. """
				
				name = "Player name - str"
				color = "Player skin color - str"
				health = "Player health - int"
				current_level = "Current level in campaign mode - int"
				current_item = "Current item held by player - int"
				
			class item_1:
				""" Item accessed through the corresponding hotkey, containing the corresponding attributes. """
				
				ammo_stock = "Current weapon ammo stock - int"
				cocking_time = "Time of the cocking weapon animation - float"
				cocking_type = "Cocking animation type - int"
				current_clip = "Current weapon clip - int"
				damage = "Damage the weapon can do - int"
				max_clip = "Current weapon max clip - int"
				name = "Current weapon name - str"
				shot_time = "Time between each shot - float"
				type = "Weapon type, like fireweapon, grenade, etc - str"
				
			class item_2:
				""" Item accessed through the corresponding hotkey, containing the corresponding attributes. """
				
				ammo_stock = "Current weapon ammo stock - int"
				cocking_time = "Time of the cocking weapon animation - float"
				cocking_type = "Cocking animation type - int"
				current_clip = "Current weapon clip - int"
				damage = "Damage the weapon can do - int"
				max_clip = "Current weapon max clip - int"
				name = "Current weapon name - str"
				shot_time = "Time between each shot - float"
				type = "Weapon type, like fireweapon, grenade, etc - str"
				
			class item_3:
				""" Item accessed through the corresponding hotkey, containing the corresponding attributes. """
				
				ammo_stock = "Current weapon ammo stock - int"
				cocking_time = "Time of the cocking weapon animation - float"
				cocking_type = "Cocking animation type - int"
				current_clip = "Current weapon clip - int"
				damage = "Damage the weapon can do - int"
				max_clip = "Current weapon max clip - int"
				name = "Current weapon name - str"
				shot_time = "Time between each shot - float"
				type = "Weapon type, like fireweapon, grenade, etc - str"
				
			class item_4:
				""" Item accessed through the corresponding hotkey, containing the corresponding attributes. """
				
				ammo_stock = "Current weapon ammo stock - int"
				cocking_time = "Time of the cocking weapon animation - float"
				cocking_type = "Cocking animation type - int"
				current_clip = "Current weapon clip - int"
				damage = "Damage the weapon can do - int"
				max_clip = "Current weapon max clip - int"
				name = "Current weapon name - str"
				shot_time = "Time between each shot - float"
				type = "Weapon type, like fireweapon, grenade, etc - str"
				
		class loaded_player:
			""" The loaded_player data is loaded from the selected savegame. If the player win a level, the loaded_player is overwritten by current_player. """
			
			class status:
				""" General player status, like player name, health, skin color, current level in campaign, current item held, etc. """
				
				name = "Player name - str"
				color = "Player skin color - str"
				health = "Player health - int"
				current_level = "Current level in campaign mode - int"
				current_item = "Current item held by player - int"
				
			class item_1:
				""" Item accessed through the corresponding hotkey, containing the corresponding attributes. """
				
				ammo_stock = "Current weapon ammo stock - int"
				cocking_time = "Time of the cocking weapon animation - float"
				cocking_type = "Cocking animation type - int"
				current_clip = "Current weapon clip - int"
				damage = "Damage the weapon can do - int"
				max_clip = "Current weapon max clip - int"
				name = "Current weapon name - str"
				shot_time = "Time between each shot - float"
				type = "Weapon type, like fireweapon, grenade, etc - str"
				
			class item_2:
				""" Item accessed through the corresponding hotkey, containing the corresponding attributes. """
				
				ammo_stock = "Current weapon ammo stock - int"
				cocking_time = "Time of the cocking weapon animation - float"
				cocking_type = "Cocking animation type - int"
				current_clip = "Current weapon clip - int"
				damage = "Damage the weapon can do - int"
				max_clip = "Current weapon max clip - int"
				name = "Current weapon name - str"
				shot_time = "Time between each shot - float"
				type = "Weapon type, like fireweapon, grenade, etc - str"
				
			class item_3:
				""" Item accessed through the corresponding hotkey, containing the corresponding attributes. """
				
				ammo_stock = "Current weapon ammo stock - int"
				cocking_time = "Time of the cocking weapon animation - float"
				cocking_type = "Cocking animation type - int"
				current_clip = "Current weapon clip - int"
				damage = "Damage the weapon can do - int"
				max_clip = "Current weapon max clip - int"
				name = "Current weapon name - str"
				shot_time = "Time between each shot - float"
				type = "Weapon type, like fireweapon, grenade, etc - str"
				
			class item_4:
				""" Item accessed through the corresponding hotkey, containing the corresponding attributes. """
				
				ammo_stock = "Current weapon ammo stock - int"
				cocking_time = "Time of the cocking weapon animation - float"
				cocking_type = "Cocking animation type - int"
				current_clip = "Current weapon clip - int"
				damage = "Damage the weapon can do - int"
				max_clip = "Current weapon max clip - int"
				name = "Current weapon name - str"
				shot_time = "Time between each shot - float"
				type = "Weapon type, like fireweapon, grenade, etc - str"
				
			
				
		class loaded_player:
			pass
		
	class strings:
		""" Strings are loaded based in the current language settings. Used mostly in GUI text, they are divided in several keys for better context organization. Since there's too much strings, they will not be covered in this help at start, but its context and key names are self explanatory. """
		
		menu_common = "Commonly used words in menus - dict"
		menu_main = "Strings in main menu - dict"
		menu_options = "Strings in options menu - dict"
		menu_game = "Strings in game options menu - dict"
		menu_graphics = "Strings in graphic options menu - dict"
		menu_controls = "Strings in control options menu - dict"
		menu_campaing = "Strings in campaign menu - dict"
		menu_player = "Strings in player creation menu - dict"
		
	class options:
		pass
		
	class database:
		pass
		
class Groups:
	""" Descriptions of game objects groups. It may contain hierarchy order, description of object functions and properties used. """
	
	class player:
		pass
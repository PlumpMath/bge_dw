import bge

def set_text(cont):
	
	""" Sets text of current UI label based on strings stored at globalDict. The use is for different languages.
	
	SCENE: current GUI
	OBJECT: current text label
	FREQUENCY: once """
	
	own = cont.owner
	globalDict = bge.logic.globalDict
	game_strings = globalDict["strings"]
	
	# Objects
	button = own.parent
	
	# Sensors
	always = cont.sensors[0].positive
	
	############################
	######## INITIALIZE ########
	############################
	
	if always and "button" in button:
			
			if button["button"] != "":
			
				# Sets the label's text to its corresponding reference in strings library
				own["Text"] = game_strings[button["string_section"]][button["string_key"]]
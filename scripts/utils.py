import bge

""" This module contains useful functions """

def str2bool(string):
	""" Converts string values to boolean values based on common contents of strings that represents booleans. """
	
	# Check if value is string
	if type(string) == str:
	
		# Return True
		if string == "True" or string == "true" or string == "Yes" or string == "yes" or string == "On" or string == "on" or string == "Positive" or string == "positive":
			return True
			
		# Return False
		elif string == "False" or string == "false" or string == "No" or string == "no" or string == "Off" or string == "off" or string == "Negative" or string == "negative":
			return False
		
		# Return None
		else:
			return None
			
	# Warning message if unsuccessful
	else:
		print("Value", string, "is not a valid string")

def between(value, min, max):
	""" Returns if value is between two other values. Useful because floats can't use range(min, max). """
	
	# Check if value is numeric
	if type(value) == float or type(value) == int or str(value).isnumeric:
		
		# Return True if value is between min and max values
		if float(value) > float(min) and float(value) < float(max):
			return True
		
		# Return False if value 
		else:
			return False
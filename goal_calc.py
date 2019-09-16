import numpy as np


def user_input():

	print "Starting user_input"

	global angle
	global distance

	angle = float(raw_input("Input Goal position angle:") or "80") 
	distance = float(raw_input("Input Goal Position distance from orifice:") or "1.414") 
	
	print angle
	print distance
	print "End of user_input"
	return angle, distance

def goal_pos_calc(angle = 0, distance = 0):

	print "Starting goal_pos-calc with angle",angle, "and distance", distance

	if angle == 0:
		angle, distance = user_input()
	
	if __name__ == '__main__':

		print "Angle = ", angle, "Deg"
		print "Distance = ", distance,"Metres"

	print "Angle = ", angle, "Deg"
	print "Distance = ", distance,"Metres"	
	'''angle 45deg and distance 1.414m should return x and y values of 1m. 
	'''
	# create a dictionary called goal.
	goal = {}

	#initiate dict keys, "angle" and "distance",
	goal["angle "]= angle 
	goal["distance"] = distance

	#find the x and y coordinates of the goal position using trig.
	angle = angle * np.pi/180
	x = distance*np.sin(angle) # opposite side x.
	y = distance*np.cos(angle) # adjasent side y. 6/arcsin = x
	print "x", x
	print "y", y 

	if __name__ == '__main__':
		print "x =", x, "y =", y
	
	'''x,y are calculated relative to the orifice. The x,y at the 
	orifice needs adding to goal x,y so goal is in the same frame.
	'''
	orifice = {"x": 0.31329, "y": (-0.65148)} #robot home position is 100mm forward of orifice i.e -0.75148.
	x =  orifice["x"] + x
	y = -y # invert y so it points in the correct direction.
	y =  orifice["y"] + y

	print "x homed", x
	print "y homed", y
	print "End of goal_pos_calc"
	#return angle, distance #used for force calculation in force_calculator.py
	return x,y # used along with ur_data by next_state to calculate a trajectory.

	'''
	the first iteration returns the goal position x,y in the robot's frame.
	the second iteration returns the x,y of the next step in the robot's frame.
	'''
	

if __name__ == '__main__':
    x,y = goal_pos_calc()
    print "x =", x, "y =", y

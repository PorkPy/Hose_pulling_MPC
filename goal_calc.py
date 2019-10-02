import numpy as np


def user_input():
	print ""
	print "Starting user_input"

	global angle
	global distance

	angle = float(raw_input("Input Goal position angle:") or "45") 
	distance = float(raw_input("Input Goal Position distance from orifice:") or "1.415") 
	
	print "Return User Input Angle, Distance", angle, distance
	return angle, distance

def goal_pos_calc(angle = 0, distance = 0):

	print ""
	# If called with values, those values for angle and distance will be from the force.beam_adjust calc.
	print "Starting goal_pos-calc with angle",angle, "and distance", distance

	if angle == 0:
		angle, distance = user_input()

	
		'''angle 45deg and distance 1.414m should return x and y values of 1m'''
	# create a dictionary called goal.
	goal = {}

	#initiate dict keys, "angle" and "distance",
	goal["angle "]= angle 
	goal["distance"] = distance

	# If called empty: find the x and y coordinates of the goal position using trig.
	# If called full: find x,y of new iterative step.
	angle = angle * np.pi/180
	x = distance*np.sin(angle) # opposite side x.
	y = distance*np.cos(angle) # adjasent side y. 6/arcsin = x
	#y = y*(-1)
	



	if __name__ == '__main__':
		print "x =", x, "y =", y
	
	print "Return Goal Position x ,y ", x,y
	
	#return angle, distance #used for force calculation in force_calculator.py
	return x,y # used along with ur_data by next_state to calculate a trajectory.

	'''
	the first iteration returns the goal position x,y in the robot's frame.
	the second iteration returns the x,y of the next step in the robot's frame.
	'''
	

# if __name__ == '__main__':
#     x,y = goal_pos_calc()
#     print "x =", x, "y =", y

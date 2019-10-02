

import numpy as np
import ur_data as ur
import goal_calc as goal
import cPickle as pickle
import force_calculator as f

'''
	NOTES... Do i need all the offsetting calculations if 
	im only using relative move commands? I think 
	i could just add the offset just before the robot command 
	is sent.

	Need to include some iterative function to get the next 
	iterative position. 
	'''

def state_calc(e = 0, x_current = 0, y_current = 0, x_goal = 0, y_goal = 0):
	print ""
	print "Starting state_calc"

	''' this code takes in the robot's current position and user defined goal position, and 
	calculates the distance between them.
	it then breaks down that distance into intervals and returns the next intervale as an angle
	and distance which then gets imported into force_calculator.
	'''


	if e == 0:
		#import current robot position and add to dictionary current_pos.
		pose = {}
		pose["x"],pose["y"],pose["z"],pose["Rx"],pose["Ry"],pose["Rz"] = ur.where_now()
		
		#create a dictionary of the current x,y position.
		current_pos_x = pose["x"]
		current_pos_y = pose["y"]

	else:
		current_pos_x = x_current
		current_pos_y = y_current

	
	
	'''This block gets the goal position in x,y and uses it to work out the angle and distance between 
	the current position and the goal.
	'''
	

	if e == 0:
		# import user defined goal position.
		x_goal,y_goal = goal.goal_pos_calc()

		
	if e == 0:
		'''Translate the robot into the task space by offsetting the current robot position. 
		'''
		current_pos_x, current_pos_y = ur.base_to_task(current_pos_x, current_pos_y)

	#current_pos_y = current_pos_y *(-1)

	print "current_pos_x", current_pos_x
	print "current_pos_y", current_pos_y

	'''build new dict to find lengths of opposite and adjacent sides of triangle
	formed between current position and goal position. These are then used to 
	find the hypotenuse which is the trajectory between the current and goal positions.
	'''
	
	opposite = x_goal - current_pos_x # opposite
	adjacent = y_goal - current_pos_y # adjacent

	print "x_goal", x_goal, "y_goal", y_goal

	print "opposite", opposite
	print "adjacent", adjacent

	#take absolute values for opp and adj to avoid queer math anomalies.
	opposite = np.abs(opposite)
	adjacent = np.abs(adjacent)
	
	
	# square the opposite and adjacent sides.
	x_sq = (opposite)**2 #adj^2
	y_sq = (adjacent)**2 #oppo^2

	# calculate hypotenuse between current and goal pos.
	#this is needed in order to build a new triangle to feed back into the goal calc.
	polar_rad = np.sqrt(x_sq + y_sq) 

	print "polar rad xxx", polar_rad
	x = opposite
	y = adjacent

	'''find the new angle in degrees to feed back into goal calc.
	'''
	polar_angle = np.arctan(x/y) # in radians.
	polar_angle = polar_angle *(180/np.pi) # convert rad to deg.
	print "polar anglexxx", polar_angle

	# segment the hypotenuse into 10mm intervals.
	interval =  0.1 #10mm interval  #polar_rad
	
		

	'''This block uses the angle between the current position and the goal to find the 
	x,y of a new interation or step towards the goal. It then determins the angle and 
	distance between the next step and the orifice in order to work out the force
	applided to a hose when pulled at those values.
	'''
	
	x,y = goal.goal_pos_calc(polar_angle, interval)

	x = x
	y = y#*(-1) #sign needs inverting to make it relative to robot space. but srews up trig functions.
	#better to leave sign untill value gets posed to robot.
	

	'''what is the force at this new x,y iteration?
	'''

	'''ultimately, this scrip returns the angle and distance of the next iterative move
	which is then fed back to the force_calculator for evaluation.

	Need to return the polar_rad for force-calc because force 
	calcs should be relative to the orifice position.
	But the angle needs to be between the next iterative position and the orifice, 
	now the next position and the current position. Even though the robot is moving from
	its current position, the hose is always being pulled from the orifice.

	Home position is 0,0 in the task space.
	what is the iterative position relative to task space?
	current position is an absolute relative to the orifice
	whereas, x,y are only relative to the current pos.
	By adding these values we get x,y relative to the orifice. 
	now one can calculate the angle and distance between the orifice 
	and the new iterative move.
	'''
	# x_rel = next_x_relative_to_orifice
	print "current_pos_x", current_pos_x
	print "current_pos_y", current_pos_y
	next_x_rel = current_pos_x + x
	next_y_rel = current_pos_y + y
	next_y_rel = np.abs(next_y_rel)
	print "next_x_reletive to orifice", next_x_rel
	print "next_y_reletive to orifice", next_y_rel
	'''find the angle and distance between iterative step and the orifice by 
	squaring the opposite and adjacent sides.
	no need for subtracting orifice from next position as 
	orifice is 0,0.
	'''
	next_x_sq = next_x_rel**2 #adj^2
	next_y_sq = next_y_rel**2 #oppo^2

	# calculate hypotenuse between iterative step and orifice.
	#this is needed in order to build a new triangle to feed 
	#length back into the goal calc.
	polar_rad = np.sqrt(next_x_sq + next_y_sq) #distance from orifice to iterative step.


	polar_angle = np.arctan(next_x_rel/next_y_rel) # in radians.between orifice and iterative step.
	polar_angle = polar_angle *(180/np.pi) # convert rad to deg.

		
	# Pickle everything to avoid circular feferences.
	pickel_goal = x_goal, y_goal #persistant goal values
	with open('pickle_goal.pickle', "wb") as file5:
		pickle.dump(pickel_goal, file5, -1)


	pickel_file = x,y #of iterative step.
	with open('pickle_file.pickle', "wb") as file1: 
		pickle.dump(pickel_file, file1, -1)

	pickel_send = polar_rad, polar_angle # remember, this is between step and orifice!
	with open('pickle_send.pickle', "wb") as file2:
		pickle.dump(pickel_send, file2, -1)


	pickel_next_move = next_x_rel, next_y_rel # remember, this is between step and orifice!
	with open('pickel_next_move.pickle', "wb") as file6:
		pickle.dump(pickel_next_move, file6, -1)

	print "Return: polar_rad", polar_rad # between next step and orifice
	print "Return polar_angle", polar_angle # between next step and orifice.
	print "Return x, y", x,y 
	print "Return next steps relative to orifice", next_x_rel, next_y_rel
	return polar_rad, polar_angle, x, y, next_x_rel, next_y_rel


if __name__ == '__main__':
	state_calc()

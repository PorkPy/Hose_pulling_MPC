

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

def state_calc():

	print "Starting state_calc"

	''' this code takes in the robot's current position and user defined goal position, and 
	calculates the distance between them.
	it then breaks down that distance into intervals and returns the next intervale as an angle
	and distance which then gets imported into force_calculator.
	'''

	#origin, orifice position in space.
	home_pos = {"x": 0.31329, "y": (-0.65148)} # y changed from -0.75148 which is robot home_pos.

	#import current robot position and add to dictionary current_pos.
	pose = {}
	pose["x"],pose["y"],pose["z"],pose["Rx"],pose["Ry"],pose["Rz"] = ur.where_now()
	
	# user defined current robot position.
	#x_1 = float(raw_input("x_1 :"))
	#y_1 = float(raw_input("y_1 :"))

	#create a dictionary of the current x,y position.
	current_pos = {"x_1": pose["x"], "y_1": pose["y"]}
	

	# import user defined goal position.
	x,y = goal.goal_pos_calc()

	x_2 = x # goal x position in in robot's frame.
	y_2 = y
	print "x_2", x_2
	print "y_2", y_2

	#create a dictionary of the goal x,y pos
	goal_pos = {"x_2": x_2, "y_2": y_2}


	'''offset current robot pos x,y coordinates relative to orifice which is the home_pos -100mm in y.
	 	For ease of implimentation, the home position has been updated to include the -100mm offset in y, 
		meaning the home_pos is in fact the orifice pos.
	'''
	current_pos["x_1"] = current_pos["x_1"] - home_pos["x"]
	current_pos["y_1"] = (current_pos["y_1"] - home_pos["y"])
	

	#un-offset goal pos x,y coordinates relative to home_pos which is the origin.
	'''This is necessary because even though goal_calc already applide an offset
	to the goal_pos, the raw goal_pos is needed to do trajectory calculations.
	However, the robot controller will need the offsetted values to move.
	'''
	goal_pos["x_2"] = (goal_pos["x_2"] - home_pos["x"])
	goal_pos["y_2"] = (goal_pos["y_2"] - home_pos["y"])

	print "goal_pos:", goal_pos 

	'''build new dict to find lengths of opposite and adjacent sides of triangle
	formed between current position and goal position. These are then used to 
	find the hypotenuse which is the trajectory between the current and goal positions.
	'''
	dict_3 = {}
	dict_3["x_3"] = goal_pos["x_2"] - current_pos["x_1"] # opposite
	dict_3["y_3"] = goal_pos["y_2"] - current_pos["y_1"] # adjcent

	#take absolute values for opp and adj to avoid quire math enomolies
	dict_3["x_3"] = np.abs(dict_3["x_3"])
	dict_3["y_3"] = np.abs(dict_3["y_3"])
	
	print "dict_3", dict_3

	# square the opposite and adjacent sides.
	x_3_sq = (dict_3["x_3"])**2 #adj^2
	y_3_sq = (dict_3["y_3"])**2 #oppo^2

	# calculate hypotenuse between current and goal pos.
	#this is needed in order to build a new triangle to feed back into the goal calc.
	polar_rad = np.sqrt(x_3_sq + y_3_sq) 

	'''set dict items to variable because combining dicts 
	and trig functions seemed to be causing a problem
	'''
	x = dict_3["x_3"] # distance in x from current to goal pos.
	y = dict_3["y_3"] # distance in y from current to goal pos.

	'''find the new angle in degrees to feed back into goal calc.

	'''
	polar_angle = np.arctan(x/y) # in radians.
	polar_angle = polar_angle *(180/np.pi) # convert rad to deg.
	print "polar_rad =", polar_rad
	print "polar_angle", polar_angle
	

	# segment the hypotenuse into 10mm intervals.
	interval =  0.01 #10mm interval  #polar_rad

	#there is no point working out the x,y if the force is too high!
	#input x,y into force calc.
	force = f.force_calc(polar_angle, interval)

	print "force =", force

	#print "interval", interval
	#send new angle and distance to goal_pos_cal to find new x,y interval.
	x,y = goal.goal_pos_calc(polar_angle, interval)

	x = x
	y = y
	print "x", x
	print "y", y

	'''what is the force at this new x,y iteration?
	'''

	# build new dict containing the next move increment. 
	delta_x = pose["x"] + interval
	delta_y = pose["y"] + interval

	dict_delta = {"x": delta_x, "y": delta_y}

	#print "delta_x" , delta_x
	#print "delta_y" , delta_y


	#subtract the delta poss' from origin??
	# Not needed as we calibrated our positions relative to the origin to begin with.

	#square the deltas to find length of hyp(beam bend equ)
	delta_x_sq = delta_x**2
	delta_y_sq = delta_y**2
	print delta_x
	print delta_y

	#find the polar_rad coordinates for the next interitive position reletive to origin
	length = np.sqrt(delta_x_sq + delta_y_sq)

	print "length" , length

	# determin the cossin of the angle of the next move.
	cosin_angle = np.sqrt(delta_y_sq)/length

	#determin the angle of the next move.
	angle = np.arccos(cosin_angle)

	print "angle" , angle

	# change angle from rad to deg.
	angle_deg = angle *(180/3.142)

	print "angle_deg", angle_deg


	#dict_delta = state_calc()
	print_out1 = dict_delta["x"]
	print_out_2 = dict_delta["y"]
	print "x iteration = ", print_out1
	print "y iteration = ", print_out_2
	print "Angle =", angle_deg
	print "Move distance", interval

	with open('pickle_file.pickle', "wb") as file:
		pickle.dump(dict_delta, file, -1)

	print "End of state_calc"
	return  length, angle_deg


if __name__ == '__main__':
	state_calc()

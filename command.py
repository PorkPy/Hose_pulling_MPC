#this can be expanded to include robot pose.

import os
import ur_data as ur
import next_state 
import goal_calc as goal
import force_calculator 
import glob
import cPickle as pickle
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import time



	
def robot_command(x_current, y_current):

	print ""
	print "Starting robot_command"
	print "next_x_rel", x_current
	'''
	As state_calc function has already been invoked, we can get picked values.
	We need x and y values for the next state in order to build a robot move 
	command. These next_state x,y values are concatinated with the remaining
	robot state vaules by unpickling where_now from ur_data as ur_dat has 
	already been invoked by state_calc.

	The below unpickling function may be simplifide if it's found that
	some of the picked objects are not needed.

	need to move the user input to work at beginning of force calculator.
	may need to change the order of some opps.
	#'''


	'''open pickled angle and distance from force_calc and convert 
	to x,y using goal_pos_calc.
	'''
	
	# # Get x,y of goal_pos.
	# with open('pickle_goal.pickle', "rb") as file5:
	# 	x_goal,y_goal = pickle.load(file5) 

	#open pickle append to get list of intervals so far.
	with open('pickle_append.pickle', "rb") as file4:
		intervals = pickle.load(file4)

	# # get x,y of the current iteration and add to pickle_append.
	# with open('pickle_file.pickle', "rb") as file1:
	# 	x_current,y_current = pickle.load(file1)

	# assign the current iteration tuple x,y to the variable "this_interval".
	this_interval = (x_current ,y_current) 

	
	# Append "this_interval" to the list of intervals.
	intervals.append(this_interval)
	print "intervals"

	# we now have a primed pickle file for later use in each iteration.
	with open("pickle_append.pickle", "wb") as file4:
		pickle.dump(intervals, file4, -1)


	
	return
	

	

def get_values():


	# file handling. this section removes previous pickle files.
	directory = os.getcwd()
	print os.getcwd()
	mpc = "/home/ur10pc/Desktop/mpc"
	if directory == mpc:
		for file in glob.glob("*.pickle"):
			os.remove(file)
	elif os.path.exists("/home/ur10pc/Desktop/mpc"):
		os.chdir("/home/ur10pc/Desktop/mpc")
	else:
		f = open("/home/ur10pc/Desktop/mpc")
	os.chdir("/home/ur10pc/Desktop/mpc")


	'''This function gathers all the information necessary to invoke
	the robot_command function above which uses said info to 
	build a robot command which iteratively progresses the robot 
	closer to the goal position.
	TODO: Once the robot can move one step close when the force is
	sufficiently low, the next stage when the force is high is to have the force calculator
	adjust the length of the beam bending equation to find a 
	suitable distance from the orifice where the force is low
	enough to move the robot to that location. 
	'''
	print ""
	print "Starting get_values"

	# find force by invoking force_cal
	force_prediction = force_calculator.force_calc()
	print "Force prediction =", force_prediction, "N"
	max_force = float(raw_input("Enter Max Force (Default = 20N) : ") or "20")

	with open('pickel_next_move.pickle', "rb") as file6:
		next_x_rel, next_y_rel = pickle.load(file6)


	nextmove = None
	
	# Get x,y of goal_pos.
	with open('pickle_goal.pickle', "rb") as file5:
		x_goal,y_goal = pickle.load(file5) 
	 
	print "x_goal", x_goal 
	print "y_goal", y_goal

	# on first iteration, pickle file won't yet exist.
	if not os.path.isfile("pickle_append.pickle"):
		intervals = []	
		with open("pickle_append.pickle", "wb") as file4:
			pickle.dump(intervals, file4, -1)

	

	next_y_rel = np.abs(next_y_rel)
	y_goal = np.abs(y_goal)
	x_error = x_goal - next_x_rel
	y_error = y_goal - next_y_rel

	x_error = x_error
	y_error = y_error
	print "x_error", x_error

	with open('pickle_send.pickle', "rb") as file1:
		polar_rad, polar_angle = pickle.load(file1)
	
	i = 1
	
	# while the robot is not at the goal, loop throght finding the next iterative step.
	while (  y_error >0.1 or x_error>0.1): #or y_error not in range(0, 10)): #or (y_error not in range(-0.5,0.5)):

		#while i < 5:
		print "restart while loop"
		print " polar_angle", polar_angle, "polar_rad", polar_rad

		force_prediction = force_calculator.force_calc(polar_rad, polar_angle)



		# if force is low enough, send invoke robot_command to save current (x,y). 
		if force_prediction < max_force:
			robot_command(next_x_rel, next_y_rel)
		else:
			# if force is too large invoke beam_adjust to find new beam length and lower force.
			while force_prediction > max_force:

				force = force_calculator.beam_adjust()
				print "force step = ", force
				force_prediction = force

			print "final force = ", force
			# again, is force is ok, invoke robot_command to save new (x,y)
		

		# Open pickle where new angle and distance are saved by beam_adjust.
		with open('pickle_send.pickle', "rb") as file2:  
			pickle_out = pickle.load(file2)

		# Assign variables to pickled objects.
		L_1, pull_angle = pickle_out

		# Using new angle and distance; get new x,y for next iterative move.
		x_current, y_current = goal.goal_pos_calc(pull_angle, L_1)
		
		# invoke robot_command to save append latest x,y step.
		
		robot_command(x_current, y_current)

		# Now with the current low force x,y saved, start over to find the next xy.
		e = 1 # Used to swith offset function on/off in next_state
		# We input the current x,y into state_calc and get a new iterative step x,y out.
		polar_rad, polar_angle, x_current,y_current, next_x_rel, next_y_rel= next_state.state_calc(e, next_x_rel, next_y_rel, x_goal, y_goal)

		
		#i = i +1
		#print "i =", i
		x_error = x_goal - next_x_rel
		next_y_rel = np.abs(next_y_rel)
		y_goal = np.abs(y_goal)
		y_error = y_goal - next_y_rel
		x_error = x_error
		y_error = y_error

		print "x_error", x_error
		print "y_error", y_error

		i += 1
		print "i =", i
		print ""
		print ""

	with open("pickle_append.pickle",  "rb") as file4:
			intervals = pickle.load(file4)

	#print "intervals", intervals

	
	# need to indent this block depending on wheather the robot is 
	#moving at each step or not. Otherwise ur_control wont get any data until get_values returns.
	# if nextmove is not None:

	# 	print "Return Next Move", nextmove
	# 	# return nexmove list to ur_control to move robot.
	# 	return nextmove 
	# else:
		
	# 	print "Force is too high"


	# robot_moves = []
	# #robot_moves = [i[0] for i in intervals]
	# for i in intervals:
	# 	(x,y)  = ur.task_to_base(i)
	# 	robot_moves.append((x,y))

	return intervals


if __name__ == '__main__':
	intervals = get_values()

	print "intervals ="
	pprint(intervals) 


	robot_moves = [list(i) for i in intervals]

	print ""
	print "robot_moves_list ="
	pprint(robot_moves)

	for i in range(len(robot_moves)):
		robot_moves[i][1] = - robot_moves[i][1]

	print ""
	print "robot_moves_inverted_Y"
	pprint(robot_moves)


	robot_moves = [tuple(i) for i in robot_moves]

	print ""
	print "robot_moves_tuple"
	pprint(robot_moves)

	robot_moves_offset =[]
	for i in robot_moves:
		(x,y)  = ur.task_to_base(i)
		robot_moves_offset.append((x,y))
	
	


	robot_moves_offset = [list(i) for i in robot_moves_offset]

	zeros = [0,0,0,0]

	for i in robot_moves_offset:
		robot_moves_offset.extend(zeros)

	print ""
	print "robot_moves_offset"
	pprint(robot_moves_offset)


	fig = plt.figure()
	data = np.array(intervals)
	
	axes = plt.gca()
	axes.set_xlim([0,1.5])
	axes.set_ylim([1.5,0])
	x, y = data.T
	plt.scatter(x,y)
	plt.show()
	plt.close(fig)



		
	fig = plt.figure()
	data = np.array(robot_moves)
	
	axes = plt.gca()
	axes.set_xlim([0,1.5])
	axes.set_ylim([-1.5,0])
	x, y = data.T
	plt.scatter(x,y)
	plt.show()
	plt.close(fig)


	fig = plt.figure()
	data = np.array(robot_moves_offset)
	
	axes = plt.gca()
	axes.set_xlim([0,1.5])
	axes.set_ylim([-1.5,0])
	x, y = data.T
	plt.scatter(x,y)
	plt.show()
	plt.close(fig)
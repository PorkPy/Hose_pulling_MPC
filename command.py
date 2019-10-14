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
	print "next_y_rel", y_current
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

	

	# assign the current iteration tuple x,y to the variable "this_interval".
	this_interval = (x_current ,y_current) 

	
	# Append "this_interval" to the list of intervals.
	intervals.append(this_interval)
	print ""
	#print "intervals"
	#pprint(intervals)
	print ""

	# we now have a primed pickle file for later use in each iteration.
	with open("pickle_append.pickle", "wb") as file4:
		pickle.dump(intervals, file4, -1)



	with open('pickle_xy.pickle', "rb") as file8: 
		xy_intervals = pickle.load(file8)

	# get x,y of the current iteration and add to pickle_append.
	with open('pickle_file.pickle', "rb") as file1:
		x,y = pickle.load(file1)

	this_xy_interval = x,y
	xy_intervals.append(this_xy_interval)

	pickel_file = xy_intervals #of iterative steps.
	with open('pickle_xy.pickle', "wb") as file8: 
		pickle.dump(pickel_file, file8, -1)
	
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
	max_force = float(raw_input("Enter Max Force (Default = 2N) : ") or "2")

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

	# on first iteration, pickle file won't yet exist.
	if not os.path.isfile("pickle_xy.pickle"):
		xy_intervals = []	
		with open("pickle_xy.pickle", "wb") as file8:
			pickle.dump(xy_intervals, file8, -1)

	
	x_error = x_goal - next_x_rel
	y_error = y_goal - next_y_rel

	x_error = x_error
	y_error = y_error
	print "x_error", x_error

	with open('pickle_send.pickle', "rb") as file1:
		polar_rad, polar_angle = pickle.load(file1)
	
	

	x_error = np.abs(x_error)
	y_error = np.abs(y_error)

	print "x_error", x_error
	print "y_error", y_error
	print "before loop next x rel", next_x_rel, next_y_rel
	i = 1
	
	# while the robot is not at the goal, loop throght finding the next iterative step.
	while x_error > 0.05 or y_error > 0.05: 

		print "error", x_error, y_error

		if x_error <= 0:
			break

		if i ==100:
			break

		

		#while i < 5:
		print "restart while loop"
		print " polar_angle", polar_angle, "polar_rad", polar_rad


		force_prediction = force_calculator.force_calc(polar_rad, polar_angle)



		# if force is low enough, send invoke robot_command to save current (x,y). 
		if force_prediction < max_force:
			robot_command(next_x_rel, next_y_rel)
		else:
			# if force is too large invoke beam_adjust to find new beam length and lower force.
			
			if np.abs(next_x_rel) < np.abs(x_goal): 

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
			next_x_rel, next_y_rel = goal.goal_pos_calc(pull_angle, L_1)
			
			# invoke robot_command to save append latest x,y step.
			
			robot_command(next_x_rel, next_y_rel)

		# Now with the current low force x,y saved, start over to find the next xy.
		e = 1 # Used to swith offset function on/off in next_state
		# We input the current x,y into state_calc and get a new iterative step x,y out.

		print " next_x_rel", next_x_rel
		print "next_y_rel", next_y_rel
		polar_rad, polar_angle, x_current,y_current, next_x_rel, next_y_rel= next_state.state_calc(e, \
			next_x_rel, \
			next_y_rel, \
			x_goal, \
			y_goal\
			)

		
	
		x_error = x_goal - next_x_rel		
		y_error = y_goal - next_y_rel
		

		

		

		i += 1
		print "i =", i
		print ""
		print ""

		x_error = np.abs(x_error)
		y_error = np.abs(y_error)
		print "x_error", x_error
		print "y_error", y_error

	print "goal_x", x_goal
	print "goal_y", y_goal

	robot_command(next_x_rel, next_y_rel)
	robot_command(x_goal, y_goal)

	with open("pickle_append.pickle",  "rb") as file4:
			intervals = pickle.load(file4)

	

	return intervals

def robotmove_intervals():
	intervals = get_values()

	


	#pprint(intervals) 


	robot_moves = [list(i) for i in intervals]

	
	#pprint(robot_moves)

	# for i in range(len(robot_moves)):
	# 	robot_moves[i][1] = - robot_moves[i][1]

	
		
	#pprint(robot_moves)
	del robot_moves[0]


	robot_moves = [tuple(i) for i in robot_moves]

	print "robot_moves"
	pprint(robot_moves)

	robot_moves_offset =[]
	for i in robot_moves:
		(x,y)  = ur.task_to_base(i)
		robot_moves_offset.append((x,y))


	robot_movesx = [list(i) for i in robot_moves_offset]

	del robot_movesx[0]

	print "offset moves"
	pprint(robot_movesx)


	plt.ion()	
	fig = plt.figure()
	data = np.array(robot_moves)
	#plt.figure(num='Task Frame Moves')
	plt.title('Task Frame Moves')
	plt.xlabel('x')
	plt.ylabel('y')
	axes = plt.gca()
	axes.set_xlim([-1.5,1.5])
	axes.set_ylim([-1.5,0])
	x, y = data.T
	plt.scatter(x,y,)
	plt.show()
	plt.waitforbuttonpress(0)
	

	plt.ion()
	fig = plt.figure()
	data = np.array(robot_movesx)
	plt.title('Base Frame Moves')
	plt.xlabel('x')
	plt.ylabel('y')	
	axes = plt.gca()
	axes.set_xlim([-1.5,1.5])
	axes.set_ylim([-1.5,0])
	x, y = data.T
	plt.scatter(x,y)
	plt.show()
	plt.waitforbuttonpress(0)

	#plt.close("all")
	

	zeros = [0.05, 3.142, 0, 0]

	for i in range(len(robot_movesx)):
		robot_movesx[i].extend(zeros)

	
	# fig = plt.figure()
	# ax = fig.add_subplot(111, polar=True)
	# plt.scatter(x,y)
	# ax.set_thetamin(-90)
	# ax.set_thetamax(90)
	# plt.show()
	# plt.waitforbuttonpress(0)
	# plt.close("all")




	robot_moves_offset = [list(i) for i in robot_moves_offset]

	zeros = [0,0,0,0]


	for i in range(len(robot_moves_offset)):
		robot_moves_offset[i].extend(zeros)

		


	


	with open('pickle_xy.pickle', "rb") as file8:
		xy_intervals = pickle.load(file8)



	

	robot_moves_intervals = [list(i) for i in xy_intervals]


	for i in range(len(robot_moves_intervals)):
		robot_moves_intervals[i][1] = - robot_moves_intervals[i][1]

	for i in range(len(robot_moves_intervals)):
		robot_moves_intervals[i].extend(zeros)

	



	return robot_movesx

if __name__ == "__main__":
	robotmove_intervals()

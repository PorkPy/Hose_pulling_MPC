#this can be expanded to include robot pose.

import ur_data as ur
import next_state 
import goal_calc as goal
import force_calculator as force
import cPickle as pickle

	
def robot_command():

	"Starting robot_command"
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
	with open('pickle_file.pickle', "rb") as file:  # x and y values only, need to propend to full robot state.
		pickle_out = pickle.load(file)

	dict_delta = pickle_out
	print "dict_delta", dict_delta


	# keys = ["x","y","z","Rx","Ry","Rz"]
	# sorted(keys)
	# where = ur.where_now()
	# values = list(where)
	# now = dict(zip(keys, values))

	with open('ur_data.pickle', "rb") as ur_file:  
		pickle_data = pickle.load(ur_file)

	now = pickle_data

	dict_delta["x"] = dict_delta["x"]/1000
	dict_delta["y"] = dict_delta["y"]/1000

	# create a short variable to input into robot command-(move)
	nextmove = {"x" : dict_delta['x'],
				"y" : dict_delta["y"], 
				"z" : now["z" ], 
				"Rx": now["Rx"], 
				"Ry": now["Ry"], 
				"Rz": now["Rz"]} 

	#print "next_move = ", nextmove


	move = ("movel(pose_trans(get_actual_tcp_pose(),p %s),a=0.2,v=0.25) " % nextmove + "\n")

	print "End of robot_command"

def get_values():

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

	print "Starting get_values"


	force_prediction = force.force_calc()
	print "Force prediction =", force_prediction, "N"
	max_force = float(raw_input("Enter Max Force (Default = 20N) : ") or "20")

	if force_prediction < max_force:
		robot_command()
	print "End of get_values"

if __name__ == '__main__':
    get_values()
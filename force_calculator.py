

#hose pulling force calc

import numpy as np
import next_state 
import cPickle as pickle
import goal_calc as goal


def beam_adjust():

	print ""
	print "Starting Beam Adjust"
	with open('pickle_send.pickle', "rb") as file2:  
		pickle_out = pickle.load(file2)

	L_1, pull_angle = pickle_out
	print "pull_angle", pull_angle
	print "L_1", L_1
	L_1 = L_1 + 0.01

	pickel_send = L_1, pull_angle 
	with open('pickle_send.pickle', "wb") as file2:
		pickle.dump(pickel_send, file2, -1)

	force = force_calc(L_1, pull_angle)
	print ""
	print ""
	return force



def force_calc(L_1 = 0.0, pull_angle = 0.0):
	print ""
	print "Starting force_calc with L_1", L_1, " pull_angle", pull_angle
	#with open('pickle_file.pickle', "rb") as file:  # x and y values only, need to propend to full robot state.
		#pickle_out = pickle.load(file)

	'''get length and angle values for next state, not current or 
	goal state. We dont need the force prediction for the state we are in
	because we are in it and it can be measured by the force sensor.
	we don't yet need the force of the goal position.... or do we????

	but what is the goal force means it is unachievable?
	the tajectory needs to take into account the predicted force at the goal
	in order to suggest better trajectory steps that will ensure 
	a low force goal state once the robot gets there.

	does making each iterative move low-force automatically mean 
	that the goal will also be low force??

	if we do need the goal force at the beginning, it means we need to
	calculate the enire trajectory before we take any physical moves.
	after the first physical move, we can update the force value in 
	that state. The difference between the predicted force and the accual force 
	can be used to add a bias term to the substquant tajectory calculations.

	this then looks a lot more like MPC, where we anticipate some future event 
	(the high force area), which is similar to observing an approching curener 
	for an autonomous car, and adjusting our trajectory to change that 
	future prediction. 

	example; I acan djust the beam length so i can move to a reasonabley low force
	area on the next move but that doesn't mean the goal force will also be low.

	I need to plan every step of the trajectory to find the resultant goal force.
	if the goal (or any other state) force is still too high, the bean length needs to 
	be increased further in step one, and the whole trajectory ran again.
	'''
	if L_1 == 0.0:
		L_1, pull_angle, x ,y, next_x_rel, next_y_rel= next_state.state_calc()

 

	# elif length == 1.0:
	# 	with open('pickle_send.pickle', "rb") as file2:  
	# 		pickle = pickle.load(file2)

	# 	L_1, pull_angle = pickle
	# 	print "pull_anglexx", pull_angle
	# 	print "L_1xx", L_1
	# else:
	# 	print "From beam adjust"

	 # x_goal and y_goal are to back propergate the oeriginal goal x,y to get_values
	print "pull_anglezzz", pull_angle
	print "L_1zzz", L_1






	#pull_angle = angle_deg
	#L_1 = length # distance from applied load to hole.
	#pull_angle = 60 #angle of pull in degrees
	Y = 35e6 #Young's modulus of elasticity for soft pvc
	I =  2.2e-9 #m^4  #6.55e-10???? #11.5mm hose, 7e-10 #16mm hose 2.2e-9    # #2nd moment of area m^4   5.105e-11 #6mm hose
	#L_1 = 0.1 #distance between fulcrum and effort
	L_2 = 0.01 #distance detween fulcrum and load
	mu = 1 #coefficient of friction, normally 0.2 for polymers on steel
	hose_dia = 0.16 #hose diameter in mm 11.5 or 16
	hole_dia = 0.2#hole diameter in mm, 17, 18, 19, 20
	hole_thk = 0.10 #hole thickness in mm, always 10mm
	acceleration = 0.100 #acceleration m/s^2


	#calculate angle of interference 
	int_angle = (np.arccos(hose_dia/(np.sqrt(hole_dia**2.0+hole_thk**2.0))))-(np.arctan(hole_thk/hole_dia)) 
	int_angle_deg = int_angle *180/np.pi #convert int_angle into degrees because pull_angle is inputted by user as degrees

	'''equation for subtracting redundant bend angle before force is observed'''
	if pull_angle >= int_angle_deg:
		rec_pull_angle =(pull_angle - int_angle_deg)
	else:
		rec_pull_angle = 0

	if pull_angle > int_angle_deg: # this is to take away the friction when the hole is not cutting into the hose
		mu=1
	else:
		mu= 0.2  # mu = 0.2 for normal friction & 0.7 with ploughing friction, derivedn erec_pull_angleperimentally
				#ploughing friction has now been adjusted to account for contact area between circles.
				#mu = 0.7 for 4 and 3mm clearance, 1.5 for 2mm clearance and 2 for 1mm clearance

	rec_pull_angle = rec_pull_angle*(np.pi/180) #convert back to radians


	A = (rec_pull_angle*2*Y*I)/L_1**2 #bending equ
	B = A*(L_1/hole_thk) #lever equ
	C = A+B #load on fulcrum
	sum_f = B+C #sum of forces acting on the hole

	stat_tension = (sum_f*mu)/np.cos(rec_pull_angle) #Max tension at static equilibrium #needs to be in radians !!!!
	round_tension = round(stat_tension,2) #round static tention to 2dp


	'''Dynamic Force'''

	mass = sum_f/9.81 #convert normal force to mass for F=ma


	if round_tension <=2:
		round_tension = 2 	# experimental results show that there is usually a force due 
							#to friction of 2N when there is no bending of the hose.

	force = (mass*acceleration + sum_f*mu)/np.cos(rec_pull_angle) #Dynamic force

	print "Return Force = ", force, "N"

	pickel_file = L_1,pull_angle
	with open('pickle_L_1_pull_angle.pickle', "wb") as file3:
		pickle.dump(pickel_file, file3, -1)

	

	return force

if __name__ == '__main__':
	force = force_calc()
	print "Dynamic Force = ", force, " Newtons"
# Echo client program
import socket
import time
import struct
import cPickle as pickle
import numpy as np
from pprint import pprint
import math

HOST = "123.124.125.11" # The remote host
PORT_30003 = 30003

def where_now():
	print ""
	print "Starting where_now"

	count = 0
	home_status = 0
	program_run = 0





	# while (True):
	# 	if program_run == 0:
	# 		try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(10)
	s.connect((HOST, PORT_30003))
	time.sleep(1.00)
	print ""
	packet_1 = s.recv(4)
	packet_2 = s.recv(8)
	packet_3 = s.recv(48)
	packet_4 = s.recv(48)
	packet_5 = s.recv(48)
	packet_6 = s.recv(48)
	packet_7 = s.recv(48) 
	packet_8 = s.recv(48)
	packet_9 = s.recv(48)
	packet_10 = s.recv(48)
	packet_11 = s.recv(48)

	packet_12 = s.recv(8)
	packet_12 = packet_12.encode("hex") #convert the data from \x hex notation to plain hex
	x = str(packet_12)
	x = struct.unpack('!d', packet_12.decode('hex'))[0]
	#print "X = ", x * 1000

	packet_13 = s.recv(8)
	packet_13 = packet_13.encode("hex") #convert the data from \x hex notation to plain hex
	y = str(packet_13)
	y = struct.unpack('!d', packet_13.decode('hex'))[0]
	#print "Y = ", y * 1000

	packet_14 = s.recv(8)
	packet_14 = packet_14.encode("hex") #convert the data from \x hex notation to plain hex
	z = str(packet_14)
	z = struct.unpack('!d', packet_14.decode('hex'))[0]
	#print "Z = ", z * 1000

	packet_15 = s.recv(8)
	packet_15 = packet_15.encode("hex") #convert the data from \x hex notation to plain hex
	Rx = str(packet_15)
	Rx = struct.unpack('!d', packet_15.decode('hex'))[0]
	#print "Rx = ", Rx

	packet_16 = s.recv(8)
	packet_16 = packet_16.encode("hex") #convert the data from \x hex notation to plain hex
	Ry = str(packet_16)
	Ry = struct.unpack('!d', packet_16.decode('hex'))[0]
	#print "Ry = ", Ry

	packet_17 = s.recv(8)
	packet_17 = packet_17.encode("hex") #convert the data from \x hex notation to plain hex
	Rz = str(packet_17)
	Rz = struct.unpack('!d', packet_17.decode('hex'))[0]
	#print "Rz = ", Rz

	global pose 
	pose = {"x": x, "y": y, "z": z, "Rx": Rx, "Ry": Ry, "Rz": Rz} 
	
	#print pose["x"]

	# create a short variable to input into robot command-(move)
	#nextmove =  [goal['x'], goal['y'], goal['z'], goal['Rx'], goal['Ry'], goal['Rz']]

	#return pose

	home_status = 1
	program_run = 0
	s.close()
			# except socket.error as socketerror:
			# 	print("Error: ", socketerror)

	with open('ur_data.pickle', "wb") as ur_file:
		pickle.dump(pose, ur_file, -1)


	print "Return Robot Pose", pose
	return pose["x"],pose["y"],pose["z"],pose["Rx"],pose["Ry"],pose["Rz"]





if __name__ == '__main__':


	print ""

	pose["x"],pose["y"],pose["z"],pose["Rx"],pose["Ry"],pose["Rz"] = where_now()
	print pose["x"],pose["y"],pose["z"],pose["Rx"],pose["Ry"],pose["Rz"]
	print ""


	home_pos_x = 0.3
	home_pos_y = -0.65

	x = pose["x"]
	y = pose["y"]

	offset_pose_x = x - home_pos_x
	offset_pose_y = y - home_pos_y
	

	x_interval = 0.25
	y_interval = -0.25
	
	''' As the robot base frame is not lined up square with the task frame, 
	there needs to be some maths magic to get the task coordinates 
	back into the robot frame.
	if the robot moves 1000mm in x in the task frame, the position
	of x will be out by 2.626% of the overall move distance, but also moving 
	in x only will also push y off course by 22.8%, hense the code below
	which add a correction factor to each term. 
	'''
	
	# Here, I'm trying to get back the move command issued to the robot from the baseframe.
	# I think it would be useful to easily get the robot position in task space. 
	
	
	'''This snippit takes the home position in the robot's 
	frame, adds the move performed, subtracts the correction 
	factor for its own dirtection, then subtracts the
	corrction factor for the orthogonal direction. (6.5deg)
	'''
	baseframe_x = (((home_pos_x + x_interval)*1000 - (26.28*x_interval))) - (228*y_interval)
	baseframe_y = (((home_pos_y + y_interval)*1000 - (26.28*y_interval))) + (228*x_interval)

	print "pose_x = ", x
	print "pose_y = ", y
	print ""

	print "offset_pose_x =", offset_pose_x
	print "offset_pose_y", offset_pose_y
	print ""


	print "baseframe_x", baseframe_x
	print "baseframe_y", baseframe_y
	print""

	theta = np.radians(13)
	c, s = np.cos(theta), np.sin(theta)
	j = np.array(((c,s), (s, -c)))
	pprint(j)
	print""

	
	m = np.dot(j, [0.25,-0.25])

	pprint(m)
	print""

	

def task_to_base((x,y)= (0,0)):

	points = (x,y)
	x = points[0]
	y = points[1]

	home_pos_x = 0.3
	home_pos_y = -0.65


	theta = np.radians(13.2)
	origin = 0, 0
	#x = 0
	if x == 0:
		point = 0.25, -0.25
	else:
		
		point = x, y

	ox, oy = origin
	px, py = point

	qx = ox + math.cos(theta) * (px - ox) - math.sin(theta) * (py - oy)
	qy = oy + math.sin(theta) * (px - ox) + math.cos(theta) * (py - oy)

	qx = qx + home_pos_x
	qy = qy + home_pos_y
	return qx, qy

    
    #Rotate a point counterclockwise by a given theta around a given origin.

    #The theta should be given in radians.
   
	




def base_to_task(x=0, y=0):
    """
    Rotate a point counterclockwise by a given theta around a given origin.

    The theta should be given in radians.
    """
    theta = np.radians(13.2)
    origin = 0.3, -0.65
    point = x, y

    ox, oy = origin
    px, py = point

    qx = ox + math.cos(theta) * (px - ox) + math.sin(theta) * (py - oy)
    qy = oy + math.sin(theta) * (px - ox) - math.cos(theta) * (py - oy)
    
    qx = qx - 0.3
    qy = qy + 0.65
    return qx, qy


if __name__ == "__main__":

	qx, qy = base_to_task(x,y)
	print "x, y =", x ,y 
	print ""
	print "base to task = qx,qy = ", qx, qy
	print ""


	qx, qy = task_to_base((qx, qy))
	print "task to base = qx,qy = ", qx, qy
	print ""
	
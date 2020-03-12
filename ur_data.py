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
	print( "")
	print("Starting where_now")

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
	print ("")
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



	#print pose["x"]

	# create a short variable to input into robot command-(move)
	#nextmove =  [goal['x'], goal['y'], goal['z'], goal['Rx'], goal['Ry'], goal['Rz']]

	#return pose

	home_status = 1
	program_run = 0
	s.close()
			# except socket.error as socketerror:
			# 	print("Error: ", socketerror)
	pose = x,y
	with open('ur_data.pickle', "wb") as ur_file:
		pickle.dump(pose, ur_file, -1)

	#y = np.abs(y)
	return x,y





# if __name__ == '__main__':


# 	print ("")

# 	x, y = where_now()



# 	home_pos_x = 0.3
# 	home_pos_y = 0.65





def task_to_base((x,y)= (0,0)):

	# points = (x,y)
	# x = points[0]
	# y = points[1]
	# home_pos_x = 0.3
	# home_pos_y = 0.65
	theta = 0.215
	origin = 0, 0
	point = x, y
	ox, oy = origin
	px, py = point
	qx = ox + math.cos(theta) * (px - ox) - math.sin(theta) * (py - oy)
	qy = oy + math.sin(theta) * (px - ox) + math.cos(theta) * (py - oy)
	qx += 0.05
	qy -= 0.463
	return qx, qy

    #Rotate a point counterclockwise by a given theta around a given origin.

    #The theta should be given in radians.

def base_to_task(x=0, y=0):
	"""
	Rotate a point counterclockwise by a given theta around a given origin.
	The theta should be given in radians.
	"""
	x-=	0.05	#0.05  #  make the offset first then rotate.
	y+=	0.463	#0.463
	theta = -0.215 # rotating clockwise from task to base frame.
	origin = 0,0
	point = x, y
	ox, oy = origin
	px, py = point
	qx = ox + math.cos(theta) * (px - ox) - math.sin(theta) * (py - oy)
	qy = oy + math.sin(theta) * (px - ox) + math.cos(theta) * (py - oy)

	# qx -=  1  #0.05
	# qy +=   1  #0.463

	return qx, qy




if __name__ == "__main__":

	qx, qy = base_to_task(0.1,0.1)       #(0.1679,0.539)
	# print "x, y =", x ,y
	# print ""
	# print "base to task = qx,qy = ", qx, qy
	# print ""
	print(qx, qy)


	qx, qy = task_to_base((qx, qy))
	# print "task to base = qx,qy = ", qx, qy
	# print ""
	print(qx, qy)

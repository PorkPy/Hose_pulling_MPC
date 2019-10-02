#http://www.zacobria.com/universal-robots-zacobria-forum-hints-tips-how-to/x-y-and-z-position/
#Echo client program
import socket
import command

import time
HOST = "123.124.125.11"   # The remote host
PORT = 30002              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send ("set_analog_inputrange(0, 0)" + "\n")
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send ("set_analog_inputrange(1, 0)" + "\n")
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send ("set_analog_outputdomain(0, 0)" + "\n")
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send ("set_analog_outputdomain(1, 0)" + "\n")
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send ("set_tool_voltage(24)" + "\n")
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send ("set_runstate_outputs([])" + "\n")
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send ("set_payload(0.0)" + "\n")
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send ("set_gravity([0.0, 0.0, 9.82])" + "\n")
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send ("get_actual_tcp_pose" + "\n")
bob = s.recv(1024)
s.close()

print "hello"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


nextmove = command.get_values()
#move = ("movel(pose_trans(get_actual_tcp_pose(),p %s),a=0.2,v=0.25) " % nextmove + "\n")

print "goodbye"
#print move
#s.send(move)
x = nextmove["x"]
y = nextmove["y"]


move = ("speedl([%s,%s,0,0,0,0], 0.2, 2, 2)" % (x,y) + "\n")
print move
s.send (move)
time.sleep(1)
move = ("speedl([0,0,0,0,0,0], 0.2, 2, 2)" + "\n")
s.send(move)
#s.send ("stopj(20)" + "\n")
#data = s.recv(1024)
s.close()

#s.send ("speedj([0.2,0.3,0.1,0.05,0,0], 0.5, 0.5)" + "\n")

#s.send ("speedl([-0.1,-0.1,0,0,0,0], 0.2, 2)" + "\n")
#time.sleep(3)
#s.send ("Stopj(0.02)" + "\n")


#import time
#this can be expanded to include robot pose.
#goal = {"x": 0, "y": 0, "z": 0} 

# user inputs x,y goal coordinates for end-effector.
#x = input("Input Goal Position x Coordinate:") 
#y = input("Input Goal Position y Coordinate:")

#find robot pose values and input here for Rx,Ry and Rz to keep pose fixed.
#goal = {"x": x, "y": y, "z": 0, "Rx": 0, "Ry": 0, "Rz": 0} 

# create a short variable to input into robot command-(move)
#nextmove =  [goal['x'], goal['y'], goal['z'], goal['Rx'], goal['Ry'], goal['Rz']] #[0,-0.03,0,0,0,3.14]  # =[x, y, z, Rx, Ry, Rz]. 

#nextmove = Output from nn. e.g gives a move of 30mm in y direction and a rotation of the EE about z 180 degrees."""

#get current tcp pose and add nextmove.
#move = ("movel(pose_trans(get_actual_tcp_pose(),p %s),a=0.2,v=0.25) " % nextmove + "\n") 

# send command to robot. uncomment s.send to send command to robot.
#s.send(move) 

#test move output
#print(move)










#s.send ("movej(p[0.0000000000000000, 0.4300000000000000, 0.4000000000000000, 0.0000000000000000, 2.0000000000000000, 0.0000000000000000], a=0.3962634015954636, v=0.0471975511965976)" + "\n")
#s.send ("movel (p[0.2,0.3,0.5,0,0,3.14], a=1.2, v=0.25)" + "\n")
#time.sleep(3)
#move = ("movel(pose_trans(get_actual_tcp_pose(),p[0,0.01,0,0,0,0]),a=0.2,v=0.25)" + "\n") #this works!

#time.sleep(2)


#s.send ("movej([-1.8263219632699421, -1.7319098497843228, 1.7991931614989278, -1.6389153321983159, -1.5723347175650684, 2.8868157860256334], a=0.3962634015954636, v=0.0471975511965976)" + "\n")
 
#time.sleep(10)
#s.send ("movej(p[0.0000000000000000, 0.4300000000000000, 0.4000000000000000, 0.0000000000000000, 2.0000000000000000, 0.0000000000000000], a=0.3962634015954636, v=0.0471975511965976)" + "\n")
 
#time.sleep(10)
#s.send ("movej(p[0.0000000000000000, 0.6300000000000000, 0.4000000000000000, 0.0000000000000000, 2.0000000000000000, 0.0000000000000000], a=0.3962634015954636, v=0.0471975511965976)" + "\n")
#print("Start time is:",time.time())

#i = 1000 
#while i>0:
	
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# s.connect((HOST, PORT))

	# # data = s.recv(1024)
	# # s.close()
	# # print ("Received", repr(bob))

	# #Echo client program
	# s.send("set_digital_out(2,True)"+"\n")
	# data = s.recv(1024)
	# s.close
	# #print("Received", repr(data))

	# time.sleep(0.25)

	# #s.connect((HOST,PORT))
	# s.send("set_digital_out(2,False)"+"\n")
	# data = s.recv(1024)
	# s.close
	# #print("Received", repr(data))

	# time.sleep(0.25)

	# i +-1


#print(time.time())
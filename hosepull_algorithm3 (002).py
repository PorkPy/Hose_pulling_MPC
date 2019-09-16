#A mistake was found in the force acting on a block equation. There was no need to include the sin(x)*mu
# as this is part of the friction force which is already taken care of in the bending and lever equations. 
import os
import time
import numpy as np
import sys
#import pygame
from art import *
pygame.init()

duration = 0.05  # seconds
freq = 659.2551  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

time.sleep(0.05)

duration = 0.05  # seconds
freq = 698.4565  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

time.sleep(0.05)



duration = 0.05  # seconds
freq = 783.9909  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

time.sleep(0.05)

duration = 1  # seconds
freq = 880.0000  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

time.sleep(1)



'''
import figlet

f = Figlet(font='slant')
word = 'HELLO'
curr_word = ''
for char in word:
    os.system('reset') #assuming the platform is linux, clears the screen
    curr_word += char;
    print f.renderText(curr_word)
    time.sleep(1)
'''
'''
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False

font = pygame.font.SysFont("comicsansms", 72)

text = font.render("Hello, World", True, (0, 128, 0))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
    
    screen.fill((255, 255, 255))
    screen.blit(text,
        (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    
    pygame.display.flip()
    clock.tick(60)

###################################################
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
screen = pygame.font.SysFont('Comic Sans MS', 30)

textsurface = screen.render('Some Text', False, (0, 0, 0))

screen.blit(textsurface,(0,0))
'''
###########################################################


#os.system('spd-say "your program has finished"')

print('\007')

unichr(9608)
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = u'\u2588' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 


print("\033[1;36;40m \n")
#font_40 = pygame.font.Font(None, 40) 
#text2 = font_40.render("Welcome to the hose pulling force calculator")
tprint("Welcome "" to")
tprint("The "" Hose "" Pulling")
tprint("Force "" Calculator")  # correct --> tprint("test",font="cybermedium")


os.system('spd-say "Welcome to the hose pulling force calculator"')
time.sleep(3)
os.system('spd-say "Please enter the hose external diameter"')


print("\033[1;37;40m \n")
D1 = input("What is the hose external diameter in mm? ")
print""

print("\033[1;31;40m  \n")
print "Hose external diameter set to:  %.1fmm" % (D1)
type(D1)
d=D1/1000.0
#os.system('spd-say "External diameter set to %s milimetres"' % (D1))
print""
time.sleep(1)

print("\033[1;37;40m \n")

#os.system('spd-say "Press enter to contiue"')
#raw_input("Press Enter to continue...")
print""



os.system('spd-say "Please enter the hose internal diameter"')
D2 = input("What is the hose internal diameter in mm ")
print""
print("\033[1;31;40m  \n")
print "Hose internal diameter set to: %.1fmm" % (D2)
type(D2)
d2=D2/1000.0
#os.system('spd-say "Internal diameter set to %s milimetres"' % (D2))
print""
time.sleep(1)

print("\033[1;37;40m \n")
os.system('spd-say "Press Enter to calculate 2nd moment of area"')
raw_input("Press Enter to calculate 2nd moment of area")
os.system('spd-say "Calculating second moment of area"')

total = 300
i = 0
while i <= total:
    progress(i, total, status='Calculating 2nd moment of area')
    time.sleep(0.01)  # emulating long-playing job
    i += 1

os.system('spd-say "Calculation Completed"')
print""
print""


I = (np.pi*(d**4.0-d2**4.0)/64)
time.sleep(2)
os.system('spd-say "second moment of area is %.1e metres to the forth power"' % (I))
print"2nd moment of area = %.1em^4" % (I)
time.sleep(5)


print""
#print(I)
#print(d)
#print(d2)
#print(d-d2)

print("\033[1;37;40m \n")

os.system('spd-say "Please enter the Youngs modulus"')
Y = input("What is the Young's modulus in scientific 'e' format? ")
print""
print("\033[1;31;40m  \n")
print "Young's modulus set to: %.1e" % (Y)
type(Y)
#os.system('spd-say "youngs modulus set to %.1e"' % (Y))
print""

time.sleep(2)

print("\033[1;37;40m \n")
os.system('spd-say "Please enter the orifice diameter"')
z = input("What is the orifice diameter in mm ")
print""
print("\033[1;31;40m  \n")
print "orifice internal diameter set to: %.1fmm" % (z)
type(z)
#os.system('spd-say "hole diameter set to %d milimetres"' % (z))
z=float(z)
Z=z/1000
print""

time.sleep(2)

print("\033[1;37;40m \n")
os.system('spd-say "Please enter the orifice depth"')
t = input("What is the orifice depth in mm ")
print""
print("\033[1;31;40m  \n")
print "Orifice depth set to: %.1fmm" % (t)
type(t)
#os.system('spd-say "Orifice depth set to %d milimetres"' % (t))
t=float(t)
T=t/1000
print""

time.sleep(3)

print("\033[1;37;40m \n")
print"calculating interference angle, please wait"
time.sleep(1)
os.system('spd-say "Calculating interference angle"')
print""




total = 300
i = 0
while i <= total:
    progress(i, total, status='Calculating interference angle')
    time.sleep(0.01)  # emulating long-playing job
    i += 1

os.system('spd-say "Calculation Completed"')
time.sleep(2)

#import sys
#sys.stdout.write('\a')
#sys.stdout.flush()

print""
print""

x2 = (np.arccos(D1/(np.sqrt(z**2.0+t**2.0))))-(np.arctan(t/z)) #angle of interfiance formula
x3 = x2 *180/np.pi #convert x2 into degrees




print("\033[1;31;40m \n")
print"The interference angle for a %dmm hose pulled through a %dmm hole is %.1f degrees" % (D1, z, x3)
ia=round(x3, 1)
os.system('spd-say "Interference angle is %s degrees"' % (ia))
print""
#print(ia)
time.sleep(5)

print("\033[1;37;40m \n")
os.system('spd-say "Please enter the pull angle in degrees"')
x1 = input("What is the pull angle in degrees? ")
print""
print("\033[1;31;40m  \n")
type(x1)
os.system('spd-say "Pull angle set to %s degrees"' % (x1))
print "Pull angle is set to: ", x1, "degrees"



print("\033[1;37;40m \n")
os.system('spd-say "Please enter the distance from the bending force to the orifice"')
L_1 = input("What is the distance from bending force to orifice in metres? ")
print""
print("\033[1;31;40m  \n")
type(L_1)
#os.system('spd-say "Pull angle set to %s degrees"' % (L_1))
print "Distance set to: ", L_1, "metres"



x4 = x1 - x3 #subtract angle of interference from angle of pull

print("\033[1;37;40m  \n")
#x1 = 10 #angle of pull in degrees
#Y = 35e6 #Young's modulus of elasticity for soft pvc
#I =  2.2e-9 #m^4  #6.55e-10???? #11.5mm hose, 7e-10 #16mm hose 2.2e-9    # #2nd moment of area m^4   5.105e-11 #6mm hose
#L_1 = 0.1 #distance between fulcrum and effort
#L_2 = 0.01 #distance detween fulcrum and load
#mu = 0.2 #coefficient of friction, normally 0.2 for polymers on steel
#d = 16 #hose diameter in mm 11.5 or 16
#Z = 17#hole diameter in mm, 17, 18, 19, 20
#T = 10.0 #hole thickness in mm, always 10mm




print("\033[1;37;40m \n")
os.system('spd-say "Please enter the end effectors acceleration"')
a = input("What is the end-effector acceleration? ")
print""
print("\033[1;31;40m  \n")
type(a)
#os.system('spd-say "Acceleration set to %s metres per second squared"' % (a))
print "Acceleration set to: ", a, "m/s^2"

print""
print""
time.sleep(2)
print("\033[1;37;40m \n")
print"Calculating normal force"



'''when the pulling angle (x1) is greater than the interference angle (x3) extra friction known as ploughing
is observed'''
if x1 >= x3:
	x =(x1 - x3)
else:
	x = 0

if x1 > x3: # this is to take away the ploughing friction when the hole is not cutting into the hose
	mu=1
else:
	mu= 1  # mu = 0.2 for normal friction & 0.7 with ploughing friction, derivedn experimentally
			#ploughing friction has now been adjusted to account for contact area beyween circles.
			#mu = 0.7 for 4 and 3mm clearance, 1.5 for 2mm clearance and 2 for 1mm clearance

x = x*(np.pi/180) #convert back to radians


print("\033[1;37;40m \n")

os.system('spd-say "Calculating normal force"')
print""
time.sleep(1)

total = 100
i = 0
while i <= total:
    progress(i, total, status='Calculating bending force on hose')
    time.sleep(0.01)  # emulating long-playing job
    i += 1

#os.system('spd-say "Calculation Completed"')
time.sleep(0.5)


#os.system('spd-say "Calculating leverage"')
print""
time.sleep(0.5)

total = 50
i = 0
while i <= total:
    progress(i, total, status='Calculating leverage')
    time.sleep(0.01)  # emulating long-playing job
    i += 1

#os.system('spd-say "Calculation Completed"')
time.sleep(0.5)


#os.system('spd-say "Calculating load on fulcrume"')
print""


total = 50
i = 0
while i <= total:
    progress(i, total, status='Calculating load on fulcrum')
    time.sleep(0.01)  # emulating long-playing job
    i += 1

#os.system('spd-say "Calculation Completed"')


#os.system('spd-say "Calculating sum of forces"')
print""
time.sleep(0.5)

total = 100
i = 0
while i <= total:
    progress(i, total, status='Calculating sum of forces')
    time.sleep(0.01)  # emulating long-playing job
    i += 1

os.system('spd-say "Calculation Completed"')
time.sleep(2)

print""
print""


A = (x*2*Y*I)/L_1**2 #bending equ
B = A*(L_1/t) #lever equ
C = A+B #load on fulcrum
D = B+C #sum of forces acting on the hole


print("\033[1;31;40m \n")
os.system('spd-say "Normal force between hose and orifice is %.1f newtons"' % (D))
print"Normal force between hose and orifice is %.1f newtons" % (D)
time.sleep(6)


print("\033[1;37;40m \n")
os.system('spd-say "Please enter the coefficient of friction"')
mu = input("What is the coefficient of friction? ")
print""
print("\033[1;31;40m  \n")
type(mu)
#os.system('spd-say "Pull angle set to %s degrees"' % (L_1))
print "friction coefficient se to: ", mu, 


f = (D*mu)/np.cos(x) #Max tension at static equilibrium #needs to be in radians !!!!
F = round(f,2) #round static tention to 2dp

'''Dynamic Force'''
mass = D/9.81 #convert normal force to mass for F=ma
acceleration = a  #acceleration m/s^2


if F <=2:
	F = 2 	# experimental results show that there is usually a force due 
			#to friction of 2N when there is no bending of the hose.

force = (mass*acceleration + D*mu)/np.cos(x) #Dynamic force

force = round(force,2)

mass =round(mass,2)



print("\033[1;31;40m \n")
print("Maximum force at static equilibrium when pulling on a %.1f mm hose through a %.1f mm hole" % (D1, z)),
print("at %sdeg = %sN " % (x1, F)),

print""

os.system('spd-say "Maximum force at static equilibrium when pulling on a %.1f milimetre hose through a %.1f milimetre hole at %.1f degrees is %.1f newtons "' % (D1, z, x1, F)),
time.sleep(2)
print""
print("\033[1;37;40m \n")
raw_input("Press Enter to continue")

print("\033[1;36;40m \n")

print("")
print("")
time.sleep(2)
os.system('spd-say "Dynamic force with mass %s kilograms at %s metres per second squared is %s newtons"' % (mass, acceleration, force)),
print("Dynamic Force with mass: %skg at %sm/s^2 = %sN" % (mass, acceleration, force))
print("")

time.sleep(8)
print("\033[1;33;40m \n")
print("")
print("")

print "Thank you for using the hose pulling force calculator!"
print""
print"Please share this calculator with your friends!"
os.system('spd-say "Thank you for using the hose pulling force calculator"')
time.sleep(3)
os.system('spd-say "Please share this calculator with your friends"')
print""
print""
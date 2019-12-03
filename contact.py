

'''
This calculator works out the Hertzian contact area for a cylinder inside a larger cylinder.
'''

import numpy as np

I = 2.7e-9

theta = 20

l_1 = 0.01	#	length of orifice

l_2 = 0.1   #   length of beam

f = 7.258	#	force

v_1 = 0.32**2	#	Poisson's Ratio for object 1

v_2 = 0.29**2	#	Poisson's Ratio for object 2

E_1 = 35e6	#	Young's Modulus for object 1

E_2 = 200e9		#	Young's Modulus for object 2

d_1 = 0.016		#	Diameter of hose

d_2 = 0.020		#	Diameter of orifice

#   These two variables select which orifice size we are dealing with.
#   Current orifice diameter. [0,1,2,3] = [17,18,19,20]mm
#   This is easier that changing all the references to the generated
#   list of lists individually.

A = 0 # A = rad_chunks list

B = A  #   B = area_chunks list



mylist = [0.017, 0.018, 0.019, 0.020] # This is a list of orifice sizes in meters

angles = [0,10,20,30,40,50,60,70,80,90]

# Find the clearance angle between the 16mm hose and each orifice size [17, 18, 19, 20]mm, and put the results into a list called clearance list.

clearance_list = []
for i in mylist:
    clearance =  (np.arccos(d_1/(np.sqrt((i**2.0)+(l_1**2.0)))))-(np.arctan(l_1/i))
    clearance_list.append(clearance)

# Convert clearance angles to degrees so we can subtract from pull angles.

deg_clearance_list = []
for i in clearance_list:
    deg_clearance = i*(180/np.pi)
    deg_clearance_list.append(deg_clearance)

# Subtract clearance angle from desired bending angle, but only if bend angle is greater than the clearance.

adjusted_angle_list = []
for i in deg_clearance_list:
    for angle in angles:
        if angle >= i:
            angle = angle - i
        else:
            angle = 0
        adjusted_angle_list.append(angle)

# Change angles back into rads for bending formula

rad_angle_list = []
for i in adjusted_angle_list:
    rad_angle = i*(np.pi/180)
    rad_angle_list.append(rad_angle)



from pprint import pprint

#pprint(adjusted_angle_list)

# Split the list of bending angles in to 4 smaller lists, one for each orifice size.

deg_chunks = [adjusted_angle_list[x:x+10] for x in xrange(0, len(adjusted_angle_list), 10)]
rad_chunks = [rad_angle_list[x:x+10] for x in xrange(0, len(rad_angle_list), 10)]
# print
# pprint(deg_chunks[3])
# print
# pprint(rad_chunks[3])


# Determine the bending force for a specific orifice diameter for pull angles 0-90 degrees

bend_force_list_20mm = []
for i in rad_chunks[A]:     # rad_chunks[3] specifies the 20mm orifice chunk
    bend_force = (2 * i * E_1 * 2.7e-9) / (0.1**2)
    bend_force_list_20mm.append(bend_force)

print
pprint(bend_force_list_20mm)

# Find F_y, the Y component of the pulling force vector in the robot's base frame.


pull_force_list_20mm = [] # A list of pulling force for the 20mm orifice.
for i, j in zip(bend_force_list_20mm, rad_chunks[A]):
    pull_force = (i*(2*0.1+0.01)*0.1)/(0.01*np.cos(j))
    pull_force_list_20mm.append(pull_force)

print
print "pull_force_list_20mm = "
pprint(pull_force_list_20mm)


# Find the vector sum of the pulling forces in the base frame.
# This is equal to the Y component in the robot's tool frame.

base_force_vector_list = []
for i, j in zip(pull_force_list_20mm, bend_force_list_20mm):
    base_force_vector = np.sqrt((i**2)+(j**2))
    base_force_vector_list.append(base_force_vector)

# print
# print "base_force_vector_list = "
# pprint(base_force_vector_list)

# Format values in vector list

base_force_vector_list2 = []
for i in base_force_vector_list:
    base_force_vector = "{:7.3f}".format(i)
    base_force_vector_list2.append(base_force_vector)

print
print "base_force_vector_list2"
pprint(base_force_vector_list2)




contact_area_list = []
for i in mylist:
    for j in bend_force_list_20mm:

        Er = ((1.0/d_1) + (1.0/(-i)))   #   Equivalent Radius

        Rem = ((1.0-v_1)/E_1) + ((1.0-v_2)/E_2)  #   Reduced Elastic Modulus

        c = Rem/Er    #   Ratio of REM/Er. Basically the mechanical properties

        a = (2.0*j)/(np.pi*0.001)  #   This looks like a pressure calculation

        b = np.sqrt(c*a)    #   The main equation is thus; the sqrt of the product of pressure and mechanical properties. b is the symbol used for the contact half-width

        b2 =b*2000.0   #   To get the full contact with b2 = b * 2
        contact_area_list.append(b2)

# print
# print "contact_area_list = "
# pprint(contact_area_list)




    #b2 = "{:.3e}".format(b2) #    Some pretty formatting

#print
#print"Contact Area = %s" % b2


area_chunks = [contact_area_list[x:x+10] for x in xrange(0, len(contact_area_list), 10)]


# print
# pprint(area_chunks[3])

# contact_area_20mm = []
# for i in area_chunks[B]:
#     i = "{:7.3f}".format(i)
#     contact_area_20mm.append(i)

print
print "Contact area for pull angle over a 20mm orifice"
pprint(area_chunks[B])

normalise_contact_area_20mm_list = []
for i in area_chunks[B]:
    normalise_contact_area_20mm = 1+(i/(max(area_chunks[B]))) #8.534 is the largest value in the list
    normalise_contact_area_20mm_list.append(normalise_contact_area_20mm)

print
print "normalise_contact_area_20mm_list = "
pprint(normalise_contact_area_20mm_list)



# Find the product of base pulling force vector and the normalized contact area.

pulling_force_with_contact_area_adjustment_list = []
bob = list([i*j for i, j in zip(base_force_vector_list, normalise_contact_area_20mm_list)])
    # pulling_force_with_contact_area_adjustment = i * j
    # pulling_force_with_contact_area_adjustment_list.append(pulling_force_with_contact_area_adjustment)

print
print "bob ="
pprint(bob)





# print "pulling_force_with_contact_area_adjustment_list = "
# pprint(pulling_force_with_contact_area_adjustment_list)


# dave = (list(map(lambda x,y:x*y,base_force_vector_list, area_chunks[B])))
# print
# print "dave = "
# pprint(dave)




# [a*b for a,b in zip(lista,listb)] # list comprehension
# map(lambda x,y:x*y,lista,listb) # map and lambda function


# Learned model using pulling angle data
MPC style controller for pulling hoses using a UR10 robot


This branch swops the hand derived physics model for the first learned model of the system dynamics.
The inputs to the pickled model in this controller are the length and pull angle, same as the derived model. 
This is to keep the models as similar as possible for comparison. 

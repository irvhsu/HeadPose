import numpy as numpy

##############################################################
# Class: Vote
# 
# Encapsulates a vote, which contains a predicted location for
# the center of the head, as well as the head's 3D orientation.
##############################################################

class Vote:
  def __init__(self, theta_center, theta_angles):
  	self.theta_center = theta_center
  	self.theta_angles = theta_angles

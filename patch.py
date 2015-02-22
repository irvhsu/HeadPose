import numpy as np

##############################################################
# Class: Patch
##############################################################

class Patch:
  def __init__(self, data, width=20, height=20, theta_offsets=None, theta_angles=None, isFromHead=False):
    # The offset x, y, and z to the center of the head
    self.theta_offsets = theta_offsets
        
    # The angles of the corresponding head
    self.theta_angles = theta_angles

    # Whether or not the patch is from the head
    self.isFromHead = isFromHead

    # Patch data, represented as a matrix
    self.data = np.array(data)
               
    # Stores the width of the patch
    self.width = width
        
    # Stores the height of the patch
    self.height = height


  def getSubPatchMeanDiff(self, matrix1, matrix2):
    return np.mean(matrix1) - np.mean(matrix2)

  # f1_corners and f2_corners: each an np matrix where the first row
  # is the (x,y) of the top left corner, and the second row is the (x,y)
  # of the bottom right corner
  def getSubPatches(self, f1_corners, f2_corners):
    f1_width, f1_height = f1_corners[1] - f1_corners[0]
    f2_width, f2_height = f2_corners[1] - f2_corners[0]
    
    f1_data = np.zeros([f1_height, f1_width])
    f2_data = np.zeros([f2_height, f2_width])

    f1_data = self.data[f1_corners[0][1]:f1_corners[0][1] + \
              f1_height, f1_corners[0][0]:f1_corners[0][0] + f1_width]

    f2_data = self.data[f2_corners[0][1]:f2_corners[0][1] + \
              f2_height, f2_corners[0][0]:f2_corners[0][0] + f2_width]

    return f1_data, f2_data


  


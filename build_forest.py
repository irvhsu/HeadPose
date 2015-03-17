from forest import Forest
import numpy as np

patches1 = np.load('patches_1.npy')
for patch in patches1:
  offsets = patch.theta_offsets
  patch.theta_offsets = np.reshape(offsets, [3, 1])

real_random_forest = Forest(patches=patches1)

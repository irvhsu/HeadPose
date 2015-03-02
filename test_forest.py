import numpy as np
from patch import Patch
from tree import Tree
from forest import Forest


num_patches = 5000

all_patches = []
for i in range(num_patches):
    # Creates a matrix of random data used to initialize a patch
    data = np.random.rand(24, 32)

    # Offset between center of patch and center of head, given as a random theta
    # value in the range [-0.5, 0.5] * 50
    theta_offsets = (np.random.rand(3, 1) - 0.5) * 50

    # Random theta angles, in degrees
    theta_angles = np.random.rand(3, 1) * 90

    is_from_head = True if np.random.uniform() < 0.33 else False

    patch = Patch(data=data, theta_offsets=theta_offsets, theta_angles=theta_angles, is_from_head=is_from_head)

    all_patches.append(patch)

my_forest = Forest(patches=np.array(all_patches), num_trees=10)
    



import numpy as np
from patch import Patch
from tree import Tree

test_data1 = np.random.rand(24, 32)
test_data2 = np.random.rand(24, 32)

patch1 = Patch(data=test_data1, theta_offsets=np.array([[1], [2], [3]]), theta_angles=np.array([[30], [60], [90]]))
patch2 = Patch(data=test_data2, theta_offsets=np.array([[12.5], [2.1], [-3]]), theta_angles=np.array([[45], [20], [10]]))

myTree = Tree(np.array([patch1, patch2]))

import numpy as np
from patch import Patch

test_data = np.random.rand(480, 640)

patch = Patch(test_data)

# Random corners 1: (3, 20) and (10, 40)
# Random corners 2: (300, 320) and (400, 440)

f1_corners = np.array([[3, 20], [10, 40]])
f2_corners = np.array([[300, 320], [400, 440]])

f1, f2 = patch.getSubPatches(f1_corners, f2_corners)

print "F1: ", f1.shape
print "F2: ", f2.shape

mean = patch.getSubPatchMeanDiff(f1, f2)

print "Mean: ", mean



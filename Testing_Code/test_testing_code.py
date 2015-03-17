import numpy as np
import sys
sys.path.append('../')
from read_files import *
from forest import Forest

from testing_code import *
from vote import Vote


# np.load returns an array (in this case of size 1), so get the first element
random_forest = np.load('../small_forest.npy')[0]

# get depth image of 100th frame, second folder
depth_pathname = getPathname(2, 100, "_depth.bin")
depth_pathname = '../' + depth_pathname
depth_image = readDepthImage(depth_pathname)

# If successful
if depth_image is not None:

	# Get ground truth center and angles
	gt_pathname = getPathname(2, 100, "_pose.txt")
	gt_pathname = '../' + gt_pathname
	gt_center, gt_angles = readGroundTruth(gt_pathname)

	# Read camera matrix
	K = readCameraMatrix2(2)

	# Obtain vote(s) from the forest (multiple if more than one head is present)
	final_votes = getForestEstimate(random_forest, depth_image, K)
	if len(final_votes) == 0:
		print "No head detected."
	else:
		# Get predicted center/orientation
		estimated_center = final_votes[0].theta_center
		estimated_angles = final_votes[0].theta_angles

		# Print results
		print "Ground Truth Center: ", gt_center
		print "Ground Truth Angles: ", gt_angles
		print "Estimated Center: ", estimated_center
		print "Estimated Angles: ", estimated_angles
else:
	print "NONE"



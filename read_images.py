import numpy as np
import scipy.io

# Read in a depth image
def readDepthImage(filename):
	f = open(filename, "rb")
	width =	np.fromfile(f, dtype=np.int32, count=1)
	height = np.fromfile(f, dtype=np.int32, count=1)

	depth_img = np.zeros([height * width])
	
	num_empty = 0
	num_full = 0
	p = 0

	while (p < width * height):
		num_empty = np.fromfile(f, dtype=np.int32, count=1)
		for i in range(num_empty):
			depth_img[p + i] = 0

		num_full = np.fromfile(f, dtype=np.int32, count=1)
		depth_img[p + num_empty] = np.fromfile(f, dtype=np.int16, count=num_full)
		p += num_empty + num_full

	f.close()

	return depth_img


# Test readDepthImage functionality
def testReadDepthImage(folder, frame):
	path = '../kinect_head_pose_db/' + folder + '/' + frame
	img = readDepthImage(path)
	print len(img[img > 0])


# Read ground truth file and return both theta_center and theta_angles
def readGroundTruth(filename):
	theta_center = np.array([])       # Center of the head: x, y, z
	theta_angles = np.zeros([3, 1])   # Orientation: pitch, roll, yaw
	r_mat = np.zeros([3, 3])          # Rotation matrix
	counter = 0
	f = open(filename, "r")
	for line in f:
		if (counter < 3):
			r_mat[counter, :] =  np.array([float(x) for x in line.rsplit()])

		if (counter == 4):
			theta_center = np.array([float(x) for x in line.rsplit()])

	# Convert rotation matrix into angles
	theta_angles[0] = np.arctan(r_mat[2, 1]/r_mat[2, 2])
	theta_angles[1] = -np.arcsin(r_mat[2, 0])
	theta_angles[2] = np.arctan(r_mat[1, 0]/r_mat[0,0])

	return theta_center, theta_angles


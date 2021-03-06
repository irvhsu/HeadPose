import numpy as np
import scipy.io
import os.path

# Read in a depth image, return as an array of values
# The file format is as follows: The first two lines
# are the width and height of the depth image, respectively.
# The rest of the file consists of a "num_empty" counter
# that represents how many 0's representing the segmented out
# background should be inserted, followed by a "num_full" counter
# that represents how many foreground values are to follow. The file
# is thus simply a repeat of num_empty, followed by num_full and the
# foreground values.
def readDepthImage(pathname):
	if not os.path.isfile(pathname):
		return None
	f = open(pathname, "rb")
	width =	np.fromfile(f, dtype=np.int32, count=1)
	height = np.fromfile(f, dtype=np.int32, count=1)

	# Init empty depth image
	depth_img = np.zeros([height * width])

	num_empty = 0
	num_full = 0
	p = 0

	num_empty_sum = 0
	num_full_sum = 0
	# For every pixel in the image
	while (p < width * height):

		num_empty = np.fromfile(f, dtype=np.int32, count=1)
		for i in range(num_empty):
			depth_img[p + i] = np.int16(0)
		p += num_empty

		num_full = np.fromfile(f, dtype=np.int32, count=1)
		for i in range(num_full):
			depth_img[p + i] = np.fromfile(f, dtype=np.int16, count=1)
		p += num_full

	f.close()

	# Reshape into a matrix
	depth_img = np.reshape(depth_img, [height, width])

	# Return the resulting depth image
	return depth_img


# Given a folder, frame number, and extension, returns the complete pathname
def getPathname(folder, frame, extension):
	num_zeros = 3 - len(str(frame))
	zeros = num_zeros*'0'
	path = '../kinect_head_pose_db/' + str(folder) + '/frame_00' + zeros + str(frame) + extension
	return path


# Test readDepthImage functionality
def testReadDepthImage(folder, frame):
	path = getPathname(folder, frame, "_depth.bin")
	img = readDepthImage(path)
	print len(img[img > 0])
	print len(img[img < 0])


# Read ground truth file and return both theta_center and theta_angles
def readGroundTruth(pathname):
	theta_center = np.array([])       # Center of the head: x, y, z
	theta_angles = np.zeros([3, 1])   # Orientation: pitch, roll, yaw
	r_mat = np.zeros([3, 3])          # Rotation matrix
	line_number = 0
	f = open(pathname, "r")
	for line in f:

		# Store the first three lines into the rotation matrix
		if (line_number < 3):
			r_mat[line_number, :] =  np.array([float(x) for x in line.rsplit()])

		# Store the elements of the fifth line as the center of the head (x, y, z)
		if (line_number == 4):
			theta_center = np.array([float(x) for x in line.rsplit()])
		line_number += 1

	# Convert rotation matrix into angles
	theta_angles[0] = np.arctan(float(r_mat[2, 1])/float(r_mat[2, 2])) # Pitch
	theta_angles[1] = -np.arcsin(float(r_mat[2, 0])) # Yaw
	theta_angles[2] = np.arctan(float(r_mat[1, 0])/float(r_mat[0,0])) # Roll

	return theta_center, theta_angles * 180./np.pi


# Tests the functionality of readGroundTruth, and prints results
def testReadGroundTruth(folder, frame):
	path = getPathname(folder, frame, "_pose.txt")
	theta_center, theta_angles = readGroundTruth(path)
	print "Head Center: ", theta_center
	print "Head Orientation: ", theta_angles


# Reads in the camera matrix K from a depth.cal file (first 3 lines)
def readCameraMatrix(folder):
	pathname = '../kinect_head_pose_db/' + str(folder) + '/depth.cal'
	# Initialize camera matrix
	K = np.zeros([3, 3])
	f = open(pathname, "r")
	for i in range(3):
		line = f.readline().rsplit()
		K[i, :] = np.array([float(x) for x in line])
	return K

# Reads in the camera matrix K from a depth.cal file (first 3 lines)
# Different path name for testing code within the Testing Code folder
def readCameraMatrix2(folder):
	pathname = '../../kinect_head_pose_db/' + str(folder) + '/depth.cal'
	# Initialize camera matrix
	K = np.zeros([3, 3])
	f = open(pathname, "r")
	for i in range(3):
		line = f.readline().rsplit()
		K[i, :] = np.array([float(x) for x in line])
	return K



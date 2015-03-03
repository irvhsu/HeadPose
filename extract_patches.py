import numpy as np
import scipy.io
from patch import Patch
from read_images import *

def getAllPatches():
	num_folders = 22
	all_patches = []
	for folder_num in range(num_folders):
		f = open('../' + str(folder_num) + '/size.txt')
		begin_frame = int(f.readline().rsplit())
		end_frame = int(f.readline().rsplit())
		f.close()
		for frame_num in range(begin_frame, end_frame + 1):
			pathname = getPathname(folder_num, frame_num, "_depth.bin")
			depth_image = readDepthImage(pathname)
			curr_image_patches = getPatchesFromImage(depth_image)
			all_patches.append(curr_image_patches)
	return all_patches


def getPatchesFromImage(depth_image):
	depth_image = np.reshape(depth_image, [480, 640])


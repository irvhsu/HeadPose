import numpy as np
import random
from patch import Patch
from read_files import *

# Gets all of the patches from all of the images within the given folders
def getAllPatches(folder_list):
    all_patches = []
    for folder_num in folder_list:
        f = open('../kinect_head_pose_db/' + str(folder_num) + '/size.txt')
        begin_frame = int(f.readline().rsplit()[0])
        end_frame = int(f.readline().rsplit()[0])
        f.close()
        K = readCameraMatrix(folder_num)
        print "K: ", K
        for frame_num in range(begin_frame, end_frame + 1):
            print "Image: ", frame_num

            # Pathname for depth image
            depth_pathname = getPathname(folder_num, frame_num, "_depth.bin")
            depth_image = readDepthImage(depth_pathname)
            if depth_image is None:
                continue
            # Pathname for ground truth
            gt_pathname = getPathname(folder_num, frame_num, "_pose.txt")
            theta_center, theta_angles = readGroundTruth(gt_pathname)

            # Get all patches from the current image
            curr_image_patches = getPatchesFromImage(depth_image, theta_center, theta_angles, K)
            all_patches.append(curr_image_patches)

    return np.concatenate(all_patches)


# Samples 20 patches from an image in a folder: 10 positive, 10 negative
# All patches must contain at least one non-zero pixel. Positive patches
# satisfy the heuristic: distance from center of patch to center of head
# is within 10 mm
def getPatchesFromImage(depth_image, theta_center, theta_angles, K):
    # Negative and positive patches
    negative_patches = []
    positive_patches = []
    # Height and width of image
    height = 480
    width = 640

    # Height and width of patch
    patch_height = 100
    patch_width = 100
    
    # Stride of patch sampling window
    stride = 1

    # Threshold used for heuristic (mm)
    threshold = 50

    # Number of samples (same for both positive and negative patches)
    num_samples = 10

    # Image data
    depth_image = np.reshape(depth_image, [height, width])
    
    # Number of patches sampled from a row
    num_patches_in_row = (width - patch_width) / stride + 1

    # Number of patches sampled from a column
    num_patches_in_column = (height - patch_height) / stride + 1

    for i in range(num_patches_in_column):
        for j in range(num_patches_in_row):
            # Extract patch from depth image based on position of window
            current_patch = depth_image[i*stride : (i*stride + patch_height), j*stride : (j*stride + patch_width)]
            if not isValidPatch(current_patch):
                continue

            # Get location of center pixel of patch
            u = i*stride + np.floor(patch_height/2)
            v = j*stride + np.floor(patch_width/2)

            # Get x, y, z coordinates of center pixel from its depth
            center_pixel_z = depth_image[u, v] # Depth
            if center_pixel_z <= 0:
                continue
            center_pixel_x = center_pixel_z * (v - K[0, 2])/K[0, 0]
            center_pixel_y = center_pixel_z * (u - K[1, 2])/K[1, 1]

            # Get vector pointing from center of patch to center of head
            theta_patch_center = np.array([center_pixel_x, center_pixel_y, center_pixel_z])
            theta_offsets = theta_center - theta_patch_center
            theta_offsets = np.reshape(theta_offsets, [3, 1])
            
            # Get distance by taking norm of theta_offsets
            distance = np.linalg.norm(theta_offsets)

            # print distance
            is_from_head = (distance <= threshold)
            new_patch = Patch(data=current_patch, theta_offsets=theta_offsets,
                                theta_angles=theta_angles, is_from_head=is_from_head)

            if is_from_head:
                positive_patches.append(new_patch)
            else:
                negative_patches.append(new_patch)

    num_positive_patches = min(num_samples, len(positive_patches))
    num_negative_patches = min(num_samples, len(negative_patches))
    print "Pos: ", num_positive_patches
    print "Neg: ", num_negative_patches

    # Randomly sample positive and negative patches from respective lists
    # rand_positive_patches = random.sample(positive_patches, num_positive_patches)
    # rand_negative_patches = random.sample(negative_patches, num_negative_patches)

    rand_positive_patches = np.random.choice(positive_patches, replace=False, size=num_positive_patches)
    rand_negative_patches = np.random.choice(negative_patches, replace=False, size=num_negative_patches)

    return np.concatenate((rand_positive_patches, rand_negative_patches))
    # return np.array(rand_positive_patches + rand_negative_patches)

# Determines if the given patch is a valid patch (i.e., at least one pixel > 0)
def isValidPatch(patch):
    return np.sum(patch) > 0




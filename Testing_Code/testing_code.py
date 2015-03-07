import numpy as np
import pickle
from forest import Forest
from vote import Vote

# Get output parameters from the forest
def getForestEstimate(forest, depth_image, K):

    # Extract an array of patches from the depth image
    image_patches = getPatches(depth_image, K)

    # The max level of trace of the variance a leaf can have 
    max_trace_variance = 800

    # The list that will hold all of the votes based on these patches
    all_votes = []

    # We pass every patch through every tree in the forest
    for patch in image_patches:
        for tree in forest.trees:

            # Obtain a vote for a single patch passed to a single tree
            new_vote = tree.testPatch(patch, max_trace_variance)

            # If the vote is not valid, continue
            if new_vote is None:
                continue
            all_votes.append(new_vote)

    # Use the collected votes to predict the overall estimate; return this value
    final_vote = getFinalVote(all_votes)
    return final_vote

# Extract patches from image
def getPatches(depth_image, K):

    all_patches = []

    # Height and width of image
    image_height = depth_image.shape[0]
    image_width = depth_image.shape[1]

    # Height and width of patch
    patch_height = 100
    patch_width = 100

    # Number of patches to sample
    num_samples = 500
    
    # Stride of patch sampling window
    stride = 1
    
    # Number of patches sampled from a row
    num_patches_in_row = (width - patch_width) / stride + 1

    # Number of patches sampled from a column
    num_patches_in_column = (height - patch_height) / stride + 1

    for i in range(num_patches_in_column):
        for j in range(num_patches_in_row):

            # Get next patch
            current_patch = depth_image[i*stride : (i*stride + patch_height), j*stride : (j*stride + patch_width)]

            # Get (u, v) coordinates of the center of the patch
            u = i*stride + np.floor(patch_height/2)
            v = j*stride + np.floor(patch_width/2)

            # Calculate the xyz-location of the center pixel of the patch
            center_pixel_z = depth_image[u, v] # Depth
            if center_pixel_z <= 0:
                continue
            center_pixel_x = center_pixel_z * (v - K[0, 2])/K[0, 0]
            center_pixel_y = center_pixel_z * (u - K[1, 2])/K[1, 1]

            # Ignore patches consisting of less than 10% data (i.e. 90% or more is zero)
            num_nonzero = len(current_patch[current_patch > 0])
            if num_nonzero/(patch_width*patch_height) <= .10:
                continue

            # Construct new patch from the data
            new_patch = Patch(data=current_patch, center_coords=np.array([[center_pixel_x], [center_pixel_y], [center_pixel_z]]))

            # Append to what we've collected so far
            all_patches.append(new_patch)

    # Randomly choose num_patches from all_patches, return this array
    num_patches = min(num_samples, len(all_patches))
    rand_patches = np.random.choice(all_patches, replace=False, size=num_patches)
    return rand_patches

def getFinalVote(all_votes):
    pass




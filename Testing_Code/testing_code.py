import numpy as np
import pickle
from forest import Forest

# Get output parameters from the forest
def getForestEstimate(forest, depth_image):
	pass


# Extract patches from image
def getPatches(depth_image):

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

            center_depth = depth_image[u, v] # Depth
            if center_depth <= 0:
                continue

            # Construct new patch from the data
            new_patch = Patch(data=current_patch)

            # Append to what we've collected so far
            all_patches.append(new_patch)

    # Randomly choose num_patches from all_patches
    num_patches = min(num_samples, len(all_patches))
    rand_patches = np.random.choice(all_patches, replace=False, size=num_patches)
    return rand_patches




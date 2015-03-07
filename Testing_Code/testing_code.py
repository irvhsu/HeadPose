import numpy as np
import pickle
from forest import Forest

# Get output parameters from the forest
def getForestEstimate(forest, depth_image):
	pass


# Extract patches from image
def getPatches(depth_image):
    # Height and width of image
    height = 480
    width = 640

    # Height and width of patch
    patch_height = 100
    patch_width = 100
    
    # Stride of patch sampling window
    stride = 1

    depth_image = np.reshape(depth_image, [height, width])
    
    # Number of patches sampled from a row
    num_patches_in_row = (width - patch_width) / stride + 1

    # Number of patches sampled from a column
    num_patches_in_column = (height - patch_height) / stride + 1


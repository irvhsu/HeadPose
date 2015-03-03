import numpy as np
from extract_patches import *

folders = [1, 2, 3]

all_patches = getAllPatches(folders)

print len(all_patches)

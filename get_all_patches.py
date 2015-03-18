import numpy as np
from extract_patches import *

def getPatchesFromFolder(folder_number):
  folders = [folder_number]
  all_patches = getAllPatches(folders)
  filename = 'new_patches_' + str(folder_number) + '.npy'
  np.save(filename, all_patches)

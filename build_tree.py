import numpy as np
from tree import Tree

def buildTree(folderNumber, treeID, numTrees=10):

	# Filename to read patches from
	filename = "patches_" + str(folderNumber) + ".npy"

	# Get the actual patches
	all_patches = np.load(filename)

	# Determine the number of patches to train the tree on
	num_patches = len(all_patches)
	num_train_patches = np.ceil(num_patches/numTrees)

	# Get random subset of all patches
	random_indices = np.random.choice(range(num_patches), replace=False, size=num_train_patches)
	train_patches = all_patches[random_indices]

	# Train tree on this random subset
	curr_tree = Tree(patches=train_patches)

	# Write tree to a file
	outFile = "tree" + str(treeID) + ".npy"
	np.save(outFile, curr_tree)

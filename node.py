import numpy as np
from patch import Patch

##############################################################
# Class: Node
##############################################################

class Node:
	def __init__(self, patches=None, isLeaf=False):
		self.isLeaf = isLeaf
		self.children = None
		self.binary_test = None

		if patches:
			self.patches = patches

	def setBinaryTest(self, binary_test):
		self.binary_test = binary_test

	# Computes the entropy for the node
	def computeEntropy(self):
		pass

	# Returns a list (size = 2) of candidate children based on the
	# results of running the binary test
	def getCandidateChildren(self, binary_test):
		f1_corners, f2_corners, tau = binary_test['f1'], binary_test['f2'], binary_test['tau']
		left_patches = np.array([])    # Patches assigned to the left child node
		right_patches = np.array([])   # Patches assigned to the right child node
		for patch in self.patches:
			f1_data, f2_data = patch.getSubPatches(f1_corners, f2_corners)
			meanDiff = patch.getSubPatchMeanDiff(f1_data, f2_data)
			if meanDiff > tau:
				right_patches = np.append(right_patches, patch)
			else
				left_patches = np.append(left_patches, patch)

		left_node = Node(patches=left_patches)
		right_node = Node(patches=right_patches)
		candidates = np.array([left_node, right_node])

		return candidates


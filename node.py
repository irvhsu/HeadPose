import numpy as np
import math
from patch import Patch

##############################################################
# Class: Node
##############################################################

class Node:
    def __init__(self, patches=None, isLeaf=False, children=None, binary_test=None):
        self.patches = patches
        self.isLeaf = isLeaf
        self.children = children
        self.binary_test = binary_test
        self.getParams()

    # Sets the children nodes of the node
    def setChildren(self, children):
        self.children = children
        
    # Sets the binary test associated with the node
    def setBinaryTest(self, binary_test):
        self.binary_test = binary_test

    # Computes the entropy for the node
    def computeEntropy(self):
        offset_cov, angle_cov = self.getCovariances()
        entropy = np.log(np.linalg.det(offset_cov) + np.linalg.det(angle_cov))
        return entropy

    # Get covariance for theta offsets and theta angles
    def getCovariances(self):
        offset_cov = np.cov(self.theta_offsets)    # Covariance for theta offsets
        angle_cov = np.cov(self.theta_angles)      # Covariance for theta angles
        return offset_cov, angle_cov

    # Get mean for theta offsets and theta angles
    def getMeans(self):
        return np.reshape(np.mean(self.theta_offsets, axis=1), [3, 1]), np.reshape(np.mean(self.theta_angles, axis=1), [3, 1])

    # Get theta offsets and theta angles
    def getParams(self):
        theta_offsets = []
        theta_angles = []
        for patch in self.patches:
            theta_offsets.append(patch.theta_offsets)
            theta_angles.append(patch.theta_angles)
        theta_offsets = np.concatenate(tuple(theta_offsets), axis=1)
        theta_angles = np.concatenate(tuple(theta_angles), axis=1)
        self.theta_offsets = theta_offsets
        self.theta_angles = theta_angles
        
    # Returns the fraction of patches within the node that were taken from the head
    def getPercentFromHead(self):
        patchClasses = np.array([1 if patch.is_from_head else 0 for patch in self.patches])
        return np.mean(patchClasses)       


    # Returns a list (size = 2) of candidate children based on the
    # results of running the binary test
    def getCandidateChildren(self, binary_test):
        candidates = np.array([])
        f1_corners, f2_corners, tau = binary_test['f1'], binary_test['f2'], binary_test['tau']
        left_patches = np.array([])    # Patches assigned to the left child node
        right_patches = np.array([])   # Patches assigned to the right child node
        for patch in self.patches:
            f1_data, f2_data = patch.getSubPatches(f1_corners, f2_corners)
            meanDiff = patch.getSubPatchMeanDiff(f1_data, f2_data)
            if meanDiff > tau:
                right_patches = np.append(right_patches, patch)
            else:
                left_patches = np.append(left_patches, patch)
        if len(left_patches) > 5 and len(right_patches) > 5:
            left_node = Node(patches=left_patches)
            right_node = Node(patches=right_patches)
            candidates = np.array([left_node, right_node])

        return candidates

    # Given a binary test, determine which child the patch goes to
    def testPatch(self, patch):
        f1_corners, f2_corners, tau = self.binary_test['f1'], self.binary_test['f2'], self.binary_test['tau']
        f1_data, f2_data = patch.getSubPatches(f1_corners, f2_corners)
        meanDiff = patch.getSubPatchMeanDiff(f1_data, f2_data)
        # 0: left child; 1: right child
        result = 1 if meanDiff > tau else 0
        return result



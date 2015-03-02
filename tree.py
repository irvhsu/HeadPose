import numpy as np
import random
from patch import Patch
from node import Node

##############################################################
# Class: Tree
##############################################################

class Tree:
  def __init__(self, patches, max_depth=10, min_patches=5, tau_range=[-10, 10], rate_change=10, root_node=None):
    
    # Stores all of the patches
    self.patches = patches

    # Stores the maximum allowed depth in the tree
    self.max_depth = max_depth
    
    # Stores the minimum required patches per node   
    self.min_patches = min_patches

    # Stores the min and max allowed values of the threshold tau
    self.tau_range = tau_range

    # Lambda value for weighing information gain
    self.rate_change = rate_change
    
    # Number of randomly generated binary tests per node
    self.num_tests = 1000

    # Create a new tree if no tree is passed in
    self.root_node = root_node
    if root_node is None:
      self.root_node = self.constructTree()

  # Wrapper function for constructTreeHelper
  def constructTree(self):
    current_depth = 0
    root_node = Node(patches=self.patches, isLeaf=False)
    root_node = self.constructTreeHelper(root_node, current_depth)
    return root_node
  

  # Given a node, constructs the subtree starting at that node
  def constructTreeHelper(self, current_node, current_depth):
    # Stop if current depth is equal to the maximum depth or if too few patches in the current node
    print "Current Depth: ", current_depth
    if current_depth == self.max_depth or len(current_node.patches) <= self.min_patches:
      current_node.isLeaf = True
      return current_node

    # Find optimal binary test
    best_binary_test = self.getBestBinaryTest(current_node, current_depth)
    current_node.setBinaryTest(best_binary_test)

    # If there is no best binary test
    if not best_binary_test:
      current_node.isLeaf = True
      return current_node

    # Returns a list (size = 2) of candidate children based on the
    # results of running the binary test
    candidate_children = current_node.getCandidateChildren(best_binary_test)
    
    # If no children found, return
    if len(candidate_children) == 0:
      current_node.isLeaf = True
      return current_node
    left_child, right_child = candidate_children

    # Recurse on left and right child nodes
    left_child = self.constructTreeHelper(left_child, current_depth + 1)
    right_child = self.constructTreeHelper(right_child, current_depth + 1)    
    
    current_node.setChildren(np.array([left_child, right_child]))
    
    return current_node
  
  # Gets the best binary test from a randomly generated pool of tests. The best test
  # is defined as the one that yields the highest information gain.
  def getBestBinaryTest(self, current_node, current_depth):
    best_binary_test = None
    best_info_gain = float('-inf')
    for test in range(self.num_tests):
      current_test = self.generateBinaryTest()
      candidate_children = current_node.getCandidateChildren(current_test)
      # If no candidate children, continue
      if len(candidate_children) == 0:
        continue
      # Compute information gain for current test
      current_info_gain = self.computeInfoGain(current_node, candidate_children[0], candidate_children[1], current_depth)
      if current_info_gain >= best_info_gain:
        best_info_gain = current_info_gain
        best_binary_test = current_test
    return best_binary_test


  # Generates a binary test based on randomly chosen F1 and F2 patches, and tau
  def generateBinaryTest(self):
    f1_corners = self.computeRandomF()
    f2_corners = self.computeRandomF()
    tau = random.uniform(self.tau_range[0], self.tau_range[1])
    binary_test = {'f1': f1_corners, 'f2': f2_corners, 'tau': tau}
    return binary_test

  # Generates a random subrectangular region F of a patch, by defining the upper left and bottom right corners.
  # The location of the upper left corner is used as the lower bound for the location of the bottom right corner.
  def computeRandomF(self):
    max_x_value = self.patches[0].width
    max_y_value = self.patches[0].height
    upper_corner = [np.random.randint(0, max_x_value), np.random.randint(0, max_y_value)]
    bottom_corner = [np.random.randint(upper_corner[0], max_x_value), \
                     np.random.randint(upper_corner[1], max_y_value)]
    return np.array([upper_corner, bottom_corner])
      
  
  # Computes the information gain given a pair of candidate children
  def computeInfoGain(self, current_node, left_child, right_child, depth):
    UC = self.computeUC(left_child, right_child)
    UR = self.computeUR(current_node, left_child, right_child)
    return (UC + (1 - np.exp(-depth/self.rate_change)*UR))


  # Computes the classification measure U_C to evaluate the goodness of a split
  def computeUC(self, left_child, right_child):
    PL_size = len(left_child.patches)
    PR_size = len(right_child.patches)
    left_percent_from_head = left_child.getPercentFromHead()
    right_percent_from_head = right_child.getPercentFromHead()

    numer = PL_size*(left_percent_from_head*np.log(left_percent_from_head) + (1 - left_percent_from_head)*np.log(1 - left_percent_from_head))+ \
            PR_size*(right_percent_from_head*np.log(right_percent_from_head) + (1 - right_percent_from_head)*np.log(1 - right_percent_from_head))
    denom = PL_size + PR_size

    return (numer/denom)

  # Computes the regression measure U_R to evaluate the goodness of a split
  def computeUR(self, current_node, left_child, right_child):
    self_entropy = current_node.computeEntropy()
    left_entropy = left_child.computeEntropy()
    right_entropy = right_child.computeEntropy()

    w_l = len(left_child.patches)/len(current_node.patches)
    w_r = len(right_child.patches)/len(current_node.patches)

    info_gain = self_entropy - (w_l*left_entropy + w_r*right_entropy)
    return info_gain
     

import numpy as np
import random
from patch import Patch
from node import Node
from Testing_Code.vote import Vote

##############################################################
# Class: Tree
##############################################################

class Tree:
  def __init__(self, patches, max_depth=15, min_patches=20, tau_range=[-100, 100], rate_change=10, root_node=None):
    
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
    print "Number of patches in curr_node: ", len(current_node.patches)
    print "Current Depth: ", current_depth
    print "Percent From Head: ", current_node.getPercentFromHead()
    if current_depth == self.max_depth or len(current_node.patches) <= self.min_patches:
      current_node.isLeaf = True
      return current_node

    # Find optimal binary test
    best_binary_test = self.getBestBinaryTest(current_node, current_depth)
    current_node.setBinaryTest(best_binary_test)

    # If there is no best binary test
    if best_binary_test is None:
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
        if best_binary_test is not None:

          print "Optimal Tau: ", best_binary_test['tau']
          print "Best Info Gain: ", best_info_gain
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

    # Width and height of all patches are the same, so look at the first one (WLOG)
    max_x_value = self.patches[0].width
    max_y_value = self.patches[0].height
    upper_corner = [np.random.randint(0, max_x_value), np.random.randint(0, max_y_value)]

    max_x_value_capped = min(upper_corner[0] + 40, max_x_value)
    max_y_value_capped = min(upper_corner[1] + 40, max_y_value)

    bottom_corner = [np.random.randint(upper_corner[0], max_x_value_capped), \
                     np.random.randint(upper_corner[1], max_y_value_capped)]
    return np.array([upper_corner, bottom_corner])
      
  
  # Computes the information gain given a pair of candidate children
  def computeInfoGain(self, current_node, left_child, right_child, depth):
    UC = self.computeUC(left_child, right_child)
    UR = self.computeUR(current_node, left_child, right_child)
    return (UC + (1 - np.exp(-float(depth)/float(self.rate_change)))*UR)


  # Computes the classification measure U_C to evaluate the goodness of a split
  def computeUC(self, left_child, right_child):
    PL_size = float(len(left_child.patches))
    PR_size = float(len(right_child.patches))
    left_percent_from_head = left_child.getPercentFromHead()
    right_percent_from_head = right_child.getPercentFromHead()
    # print "Left Percent From Head: ", left_percent_from_head
    # print "right_percent_from_Head: ", right_percent_from_head

    numer_left = PL_size*(left_percent_from_head*np.log(left_percent_from_head) + (1 - left_percent_from_head)*np.log(1 - left_percent_from_head))
    numer_right = PR_size*(right_percent_from_head*np.log(right_percent_from_head) + (1 - right_percent_from_head)*np.log(1 - right_percent_from_head))
    if np.isnan(numer_left):
      numer_left = 0
    if np.isnan(numer_right):
      numer_right = 0
    numer = numer_left + numer_right
    denom = PL_size + PR_size
    # print "UC: ", (float(numer)/float(denom))
    return (float(numer)/float(denom))

  # Computes the regression measure U_R to evaluate the goodness of a split
  def computeUR(self, current_node, left_child, right_child):
    self_entropy = current_node.computeEntropy()
    # print "Self entropy: ", self_entropy
    left_entropy = left_child.computeEntropy()
    right_entropy = right_child.computeEntropy()
    # print "Left Entropy: ", left_entropy
    # print "Right Entropy: ", right_entropy

    w_l = float(len(left_child.patches))/float(len(current_node.patches))
    w_r = float(len(right_child.patches))/float(len(current_node.patches))
    # print "Ratio Patches in Left: ", w_l
    # print "Ratio Patches in Right: ", w_r
    # print "Number of patches in Left: ", len(left_child.patches)
    # print "Number of patches in Right: ", len(right_child.patches)

    info_gain = self_entropy - (w_l*left_entropy + w_r*right_entropy)
    # print "UR: ", info_gain
    return info_gain
  

  # Given a patch, propogate it down the tree to a leaf
  # Output the mean of the leaf's distribution of parameters only if certain conditions are met
  def testPatch(self, patch, threshold):

    # Start from root node
    current_node = self.root_node

    # Iteratively proceed down the tree until reaching a leaf
    while not current_node.isLeaf:

      # Figure out which child to go to (0 is left, 1 is right)
      next_node_index = current_node.testPatch(patch)

      # Move to this node
      current_node = current_node.children[next_node_index]

    # Return the current node's parameters if and only if all the patches in the leaf
    # are from the head and if trace(cov) < threshold

    offset_cov, angle_cov = current_node.getCovariances()

    cov_trace_sum = np.trace(offset_cov) + np.trace(angle_cov)
    # print cov_trace_sum

    if current_node.getPercentFromHead() >= .98 and cov_trace_sum < threshold:
      # Get mean for theta offsets and theta angles
      mean_offset, mean_angles = current_node.getMeans()
      mean_offset = np.reshape(mean_offset, [3, 1])
      mean_angles = np.reshape(mean_angles, [3, 1])
      predicted_center = mean_offset + patch.center_coords


      vote = Vote(theta_center=predicted_center, theta_angles=mean_angles)
      return vote
    return None


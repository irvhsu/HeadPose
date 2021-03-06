import numpy as np
import random
from patch import Patch
from node import Node
from tree import Tree

##############################################################
# Class: Forest
##############################################################

class Forest:
  def __init__(self, patches=None, num_trees=10, trees=None):
    
    # The number of trees in the forest
    self.num_trees = num_trees

    # The input patches that we will use to construct the forest
    self.patches = patches

    # A list of the individual trees in the forest
    self.trees = []

    if trees is not None:
      self.trees = trees

    if patches is not None:
      # Constructs the trees in the forest
      self.buildForest()


  # Populates the trees in the forest
  def buildForest(self):

    # Total number of patches
    num_patches = len(self.patches)

    # For every tree
    for i in range(self.num_trees):
      print "Tree: ", i
      # Divide data evenly between trees
      num_train_patches = np.ceil(float(num_patches)/float(self.num_trees))

      # Get random subset of data of appropriate size
      random_indices = np.random.choice(range(num_patches), replace=False, size=num_train_patches)
      train_patches = self.patches[random_indices]

      # Create and append new tree
      curr_tree = Tree(patches=train_patches)
      self.trees.append(curr_tree)





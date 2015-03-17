import numpy as np
from tree import Tree
from forest import Forest

def convertTreesToForest(folderName)
  all_trees = []
  num_trees = 10
  for tree_num in range(1, num_trees + 1):
    tree_name = folderName + '/tree_' + str(tree_num) + '.npy'
    tree = np.load(tree_name)
    tree = np.reshape(tree, [1, ])[0]
    all_trees.append(tree)

  for tree in all_trees:
    print tree

  random_forest = Forest(patches=None, num_trees=10, trees=all_trees)

  print random_forest

  return random_forest



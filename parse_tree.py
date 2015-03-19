import sys
import numpy as np
from tree import Tree
from node import Node

# Gets the tree from the corresponding .npy file,
# and returns a .sif file of all nodes and edges
def parseTree(filename):
	tree = np.load(filename)
	tree = np.reshape(tree, [1, ])[0]

	writeToFile(tree.root_node, depth=0, node_id=0)


# Writes the subtree starting at the node to a .sif file
def writeToFile(node, depth, node_id):
	if node is None: return
	
	if node.children is not None:
		print str(node_id) + " edge " + str(depth) # str(node_id + 1)
		print str(node_id) + " edge " + str(depth) # str(node_id + 2)

		writeToFile(node.children[0], depth + 1, node_id + 1)
		writeToFile(node.children[1], depth + 1, node_id + 2)

def main(args):
	filename = args[1]
	parseTree(filename)

if __name__ == '__main__':
	main(sys.argv)
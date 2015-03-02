import numpy as np
from patch import Patch
from tree import Tree


def printOutTree(node, depth=0):
    ret = ""

    # Print right branch
    if node.children != None:
        ret += printOutTree(node.children[1], depth + 1)

    # Print own value
    ret += "\n" + ("    "*depth) + "NODE"

    # Print left branch
    if node.children != None:
        ret += printOutTree(node.children[0], depth + 1)

    return ret


def printSidewaysHelper(node, indent):
    if node is not None:
        if node.children is not None:
            printSidewaysHelper(node.children[0], indent + "     ")
        print indent + "NODE" + "\n"
        if node.children is not None:
            printSidewaysHelper(node.children[1], indent + "     ")


def printSideways(root_node):
    printSidewaysHelper(root_node, "")


num_patches = 500
all_patches = []
for i in range(num_patches):
    # Creates a matrix of random data used to initialize a patch
    data = np.random.rand(24, 32)

    # Offset between center of patch and center of head, given as a random theta
    # value in the range [-0.5, 0.5] * 50
    theta_offsets = (np.random.rand(3, 1) - 0.5) * 50

    # Random theta angles, in degrees
    theta_angles = np.random.rand(3, 1) * 90

    is_from_head = True if np.random.uniform() < 0.33 else False

    patch = Patch(data=data, theta_offsets=theta_offsets, theta_angles=theta_angles, is_from_head=is_from_head)

    all_patches.append(patch)

myTree = Tree(np.array(all_patches))

printedTree = printOutTree(myTree.root_node)
print printedTree




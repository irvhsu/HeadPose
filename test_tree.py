import numpy as np
from patch import Patch
from tree import Tree


def main():
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

    printSideways(myTree.root_node)


def printSideways(root_node):
    printSidewaysHelper(root_node, "")


def printSidewaysHelper(node, indent):
    if node is not None:
        if node.children is not None:
            printSidewaysHelper(node.children[0], indent + "     ")
        print indent + "NODE" + "\n"
        if node.children is not None:
            printSidewaysHelper(node.children[1], indent + "     ")

# Own implementation (does not print out branches)
def printOutTree(root_node):
    if root_node is None:
        print ""

    current_level = [root_node]
    while len(current_level) > 0:
        next_level = []
        for n in current_level:
            print "NODE"
            if n.children is not None:
                next_level.append(n.children[0])
                next_level.append(n.children[1])
        print "\n"
        current_level = next_level


if __name__ == '__main__':
    main()
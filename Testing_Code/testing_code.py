import numpy as np
import pickle
from patch import Patch
from forest import Forest
from vote import Vote

# Get output parameters from the forest
def getForestEstimate(forest, depth_image, K):

    # Extract an array of patches from the depth image
    image_patches = getPatches(depth_image, K)

    print "Num Patches Extracted: ", len(image_patches)

    # The max level of trace of the variance a leaf can have 
    max_trace_variance = 500

    # The list that will hold all of the votes based on these patches
    all_votes = []

    # We pass every patch through every tree in the forest
    for patch in image_patches:
        for tree in forest.trees:

            # Obtain a vote for a single patch passed to a single tree
            new_vote = tree.testPatch(patch, max_trace_variance)

            # If the vote is not valid, continue
            if new_vote is None:
                continue

            all_votes.append(new_vote)
    print "Num Votes: ", len(all_votes)
    # Use the collected votes to predict the overall estimate; return this value
    # final_votes: final centroids
    final_votes = getFinalVote(np.array(all_votes), forest.num_trees)
    return final_votes

# Extract patches from image
def getPatches(depth_image, K):

    print "Getting Patches"

    all_patches = []

    # Height and width of image
    image_height = depth_image.shape[0]
    image_width = depth_image.shape[1]

    # Height and width of patch
    patch_height = 100
    patch_width = 100

    # Number of patches to sample
    num_samples = 1000
    
    # Stride of patch sampling window
    stride = 1
    
    # Number of patches sampled from a row
    num_patches_in_row = (image_width - patch_width) / stride + 1

    # Number of patches sampled from a column
    num_patches_in_column = (image_height - patch_height) / stride + 1

    for i in range(num_patches_in_column):
        for j in range(num_patches_in_row):

            # Get next patch
            current_patch = depth_image[i*stride : (i*stride + patch_height), j*stride : (j*stride + patch_width)]

            # Get (u, v) coordinates of the center of the patch
            u = i*stride + np.floor(float(patch_height)/2.)
            v = j*stride + np.floor(float(patch_width)/2.)

            # Calculate the xyz-location of the center pixel of the patch
            center_pixel_z = depth_image[u, v] # Depth
            if center_pixel_z <= 0:
                continue
            center_pixel_x = center_pixel_z * float((v - K[0, 2]))/float(K[0, 0])
            center_pixel_y = center_pixel_z * float((u - K[1, 2]))/float(K[1, 1])
    
            # Ignore patches consisting of less than 10% data (i.e. 90% or more is zero)
            num_nonzero = float(len(current_patch[current_patch > 0]))
            if num_nonzero/(float(patch_width*patch_height)) <= .10:
                continue

            # Construct new patch from the data

            new_patch = Patch(data=current_patch, center_coords=np.array([[center_pixel_x], [center_pixel_y], [center_pixel_z]]))

            # Append to what we've collected so far
            all_patches.append(new_patch)

    # Randomly choose num_patches from all_patches, return this array

    num_patches = min(num_samples, len(all_patches))
    rand_patches = np.random.choice(all_patches, replace=False, size=num_patches)
    return rand_patches
    # return all_patches


def getFinalVote(all_votes, num_trees):
    # Head threshold: used to determine minimum number of votes in each cluster
    # (to classify cluster of votes as a head)
    current_clusters, current_centroids = getClusters(all_votes)
    
    stride = 1.0
    beta = 400.
    # Threshold denoting number of votes a cluster should have to be considered
    threshold = beta * float(num_trees)/float((stride ** 2))

    mean_shift_clusters, mean_shift_centroids = performMeanShift(current_clusters, current_centroids, threshold)
    final_clusters, final_centroids = computeFinalParams(mean_shift_clusters, mean_shift_centroids, threshold)
    return final_centroids


def getClusters(all_votes):

    print "Getting Clusters"
    # Number of parameters for theta: center coordinates, and orientation
    # theta_size = 6
    
    # Initialize current centroids to be empty; append to later using vstack
    # current_centroids = np.zeros([0, theta_size])
    current_centroids = np.array([])

    # List of clusters, where each cluster consists of an np.array of votes
    # current_clusters is the same size as current_centroids
    current_clusters = []

    # Max clusters
    max_clusters = 20

    # Average face diameter
    average_face_diameter = 236.4

    # Radius for clustering votes
    max_distance_to_centroid = (average_face_diameter ** 2)

    print len(all_votes)

    counter = 0
    # For every vote
    for vote in all_votes:
        if (counter % 1000) == 0:
            print counter
        counter = counter + 1
        cluster_found = False
        best_distance = float('Inf')
        # Index of best cluster
        best_cluster = 0

        # For every cluster
        for centroid_index in range(len(current_centroids)):
            if cluster_found: break
            centroid = current_centroids[centroid_index]
            difference = centroid.theta_center - vote.theta_center
            distance = np.sum(difference ** 2)

            # if distance >= max_distance_to_centroid: 
            #     continue

            # Found a best cluster
            best_cluster = centroid_index
            cluster_found = True
 
            current_clusters[best_cluster] = np.append(current_clusters[best_cluster], vote)

            # Compute centroid parameters
            average_center = np.reshape(np.mean(np.hstack(tuple([my_vote.theta_center for my_vote in current_clusters[best_cluster]])), axis=1), [3, 1])
            average_angles = np.reshape(np.mean(np.hstack(tuple([my_vote.theta_angles for my_vote in current_clusters[best_cluster]])), axis=1), [3, 1])

            current_centroids[best_cluster] = Vote(theta_center=average_center, theta_angles=average_angles)

        if not cluster_found and len(current_clusters) < max_clusters:
            new_cluster = np.array([])
            new_cluster = np.append(new_cluster, vote)

            current_clusters.append(new_cluster)
            current_centroids = np.append(current_centroids, vote)

    return current_clusters, current_centroids


def performMeanShift(current_clusters, current_centroids, threshold):
    print "Current Cluster length: ", len(current_clusters)
    print "Performing Mean Shift"
    max_mean_shift_iters = 10

    # List of clusters, each of which is an np.array of votes
    mean_shift_clusters = []

    # np.array of votes
    mean_shift_centroids = np.array([])
    
    # Average face diameter
    average_face_diameter = 236.4

    # Radius of sphere for mean shift: must be equal to 1/6 of the
    # average face diameter
    fraction_of_face = 1./6.
    mean_shift_radius2 = (fraction_of_face * average_face_diameter)**2
    

    # Perform mean shift for every cluster
    for centroid_index in range(len(current_centroids)):
            centroid = current_centroids[centroid_index]
            new_cluster = np.array([])

            for i in range(max_mean_shift_iters):
                new_cluster = np.array([])

                # For every vote in this cluster
                for vote in current_clusters[centroid_index]:
                    difference = centroid.theta_center - vote.theta_center
                    distance = np.sum(difference ** 2)                    
                    # if distance >= mean_shift_radius2: continue
                    new_cluster = np.append(new_cluster, vote)

                # Compute means of theta centers for each vote in the new cluster
                
                average_center = np.reshape(np.mean(np.hstack(tuple([my_vote.theta_center for my_vote in new_cluster])), axis = 1), [3, 1])
                average_angles = np.reshape(np.mean(np.hstack(tuple([my_vote.theta_angles for my_vote in new_cluster])), axis = 1), [3, 1])

                new_mean = Vote(theta_center=average_center, theta_angles=average_angles)
                old_mean = current_centroids[centroid_index]
                
                difference_center = new_mean.theta_center - old_mean.theta_center

                difference_mean = np.sum((difference_center ** 2))

                current_centroids[centroid_index] = new_mean

                if difference_mean < 1: break

            mean_shift_clusters.append(new_cluster)
            mean_shift_centroids = np.append(mean_shift_centroids, current_centroids[centroid_index])

    return mean_shift_clusters, mean_shift_centroids


# Computes the final parameters
def computeFinalParams(mean_shift_clusters, mean_shift_centroids, threshold):

    print "Computing final parameters"
    print "Mean Shift Cluster length: ", len(mean_shift_clusters)

    final_clusters = []
    final_centroids = np.array([])

    for cluster_index in range(len(mean_shift_clusters)):
        cluster = mean_shift_clusters[cluster_index]
        # if len(cluster) < threshold: continue
        centroid = mean_shift_centroids[cluster_index]
        final_clusters.append(cluster)
        final_centroids = np.append(final_centroids, centroid)

    return final_clusters, final_centroids


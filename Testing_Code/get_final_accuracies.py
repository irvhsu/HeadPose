import numpy as np
import sys
sys.path.append('../')
from read_files import *
from forest import Forest

from testing_code import *
from vote import Vote

# For use within Testing_Code directory
# Takes in the path to the random forest
def getFinalAccuracies(forest_path, folder_num):
    random_forest = np.load(forest_path)[0]
    # Train on folders 1-3, test on folder 4
    f = open('../../kinect_head_pose_db/' + str(folder_num) + '/size.txt')
    begin_frame = int(f.readline().rsplit()[0])
    end_frame = int(f.readline().rsplit()[0])
    f.close()    

    all_center_errors = []
    all_angle_errors = []

    for frame_num in range(begin_frame, end_frame + 1):

        # get depth image of frame_num-th frame, fourth folder
        depth_pathname = getPathname(folder_num, frame_num, "_depth.bin")
        depth_pathname = '../' + depth_pathname
        depth_image = readDepthImage(depth_pathname)

        if depth_image is None: continue

        # Get ground truth center and angles
        gt_pathname = getPathname(folder_num, frame_num, "_pose.txt")
        gt_pathname = '../' + gt_pathname
        gt_center, gt_angles = readGroundTruth(gt_pathname)
        gt_center = np.reshape(gt_center, [3, 1])

        # Read camera matrix
        K = readCameraMatrix2(folder_num)

        # Obtain vote(s) from the forest (multiple if more than one head is present)
        final_votes = getForestEstimate(random_forest, depth_image, K)
        if len(final_votes) == 0:
            print "No head detected."
        else:
            # Get predicted center/orientation
            estimated_center = final_votes[0].theta_center
            estimated_angles = final_votes[0].theta_angles
        
            # Print results
            print "Ground Truth Center: ", gt_center
            print "Ground Truth Angles: ", gt_angles
            print "Estimated Center: ", estimated_center
            print "Estimated Angles: ", estimated_angles

            center_error = np.linalg.norm(estimated_center - gt_center)
            angle_error = np.linalg.norm(estimated_angles - gt_angles)

            all_center_errors.append(center_error)
            all_angle_errors.append(angle_error)

            print "Error for Estimated Center: ", center_error
            print "Error for Estimated Angles: ", angle_error

    print "Average Center Error: ", np.mean(all_center_errors)
    print "Average Angle Error: ", np.mean(all_angle_errors)


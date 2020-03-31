# Pose Graph Reconstruction Steps

## Generating Partial Reconstructions:
### Given
1. images
1. 2D features
1. world pose priors (gps/gcs data/3rd party data)
1. camera priors

### Steps
1. Compute pairs of images that see the same features
1. For each unexplored pair:
    1. try to bootstrap a reconstruction
    1. try to grow the reconstruction
    1. remove all images used in the reconstruction from the list of unexplored pairs
    1. save the result as a partial reconstruction

## Bootstrapping a reconstruction:
### Goal
To estimate camera2 pose and the feature 3D locations in camera1's coordinate system

### Given
1. Image1, Image2
1. 2D features in Image1, 2D features in Image2
1. Camera priors
1. Pose priors
1. All 2D features

### Steps
1. Estimate the pose between camera1 and camera2 using image features
1. Estimate features' 3D locations in camera1 coordinates
1. Re-estimate camera2's pose in camera1's coordinate system using 3d feature and any world pose priors+
1. Update the 3D coordinates of the features now that we have adjusted camera2's position
1. Re-estimate camera2's pose in camera1's coordinate system using 3d feature and any world pose priors+ now that 3D features have been updated

\+ note that they are not in the same coordinate system because step 1 estimates poses in camera1s coordinate system

## Growing a reconstruction:
### Goal
Incrementally add as many cameras to an initial reconstruction as possible.

### Given
1. All 2D features
1. Set of 2D features that are currently in our reconstruction
1. current reconstruction (3d features and camera poses that have been estimated so far)
1. All unexplored images
1. camera priors
1. world pose priors

### Steps
1. Align the reconstruction to the world if world pose priors are provided
1. Do a bundle adjustment on the feature and camera locations using all cameras in the reconstruction, all features, and world pose priors+ 
1. remove bad feature-camera pairs from consideration in pose estimation
1. For all possible images that see the same features that are currently in our reconstruction pose graph
   1. Estimate the pose of this camera and add to the reconstruction
   1. Reoptimize the single camera location with respect to the feature locations in the image
   1. Triangulate 3d features not already in the reconstruction for newly added image
   1. Recalculate alignment to world, bundle, retriangulate and rebundle
      - we recalculate alignment to the world because we added a new camera to the reconstruction
      - rebundle because we added a new camera to our reconstruction and that changed the alignment to the world
      - retriangled because we rebundled
      - we rebundle because our point locations have been updated
1. Final alignment, bundle, remove outliers and addition of color

\+ expects reconstruction and world pose priors to be in the same coordinate system
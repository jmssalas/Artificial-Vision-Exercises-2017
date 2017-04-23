#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# This program assumes that the first image (for name) is the center of the panoramic and
# the next images will go to sides.
# Create a panoramic of 2000x600 pixels

# Execute: ./exercise12.py [-h] folder
# where:
#   - folder is folder which contains the images for the panoramic
# Use -h option for help

# Press 'Esc' key for exit

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Crea automáticamente un mosaico panorámico ajustando varias imágenes (>2).
## Recuerda que debe tratarse de una escena plana o de una escena cualquiera vista desde el mismo centro de proyección.
##################################

import numpy            as np
import cv2              as cv
import argparse

from    os              import listdir
from    os.path         import isdir, join, isfile


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('folder', help='Folder of images')
args = parser.parse_args()

# Check if 'source' param is not a file. If it's not file, then exit
if not isdir(args.folder):
    print('Error: {} is not a dir'.format(args.folder))
    exit(-2)

programName = 'exercise12'          # Program name

escKey = 27                         # Escape key code
enterKey = 10                       # Enter key code


method  = cv.xfeatures2d.SIFT_create()  # Keypoints method
bf      = cv.BFMatcher()                # Matcher

dx = 50        # displacement in X
dy = 50        # displacement in Y
sizeX = 2000    # size of plane in X
sizeY = 600     # size of plane in Y


# Read image in BGR
def readbgr(file):
    return cv.imread(file)

# Function which return the files into 'folder' param
def getImagesOfFolder(folder):
    return [ readbgr(join(folder,f)) for f in listdir(folder) if isfile(join(folder, f)) ]

# Get input key
def getInputKey():
    return cv.waitKey(1) & 0xFF

# Function which returns descriptor vector of 'img'
def getKeyPointsAndDescriptorVector(img):
    return method.detectAndCompute(img, mask=None)

# Function which calculates better coincidences between descriptor vectors
def getBetterMatches(desc1, desc2):
    distance = 0.75

    # Calculates the k=2 better coincidences between descriptor vectors
    matches = bf.knnMatch(desc1, desc2, k=2)

    # Filter the coincidences
    good = []
    for m, n in matches:
        if m.distance < distance * n.distance:
            good.append(m)

    return good

# Function which calculate the homography matrix between 'keypoints1' and 'keypoints2' with
# the better matches in 'good' param
def calculateHomographyWithRANSAC(keypoints1, keypoints2, good):
    # Create arrays needed for 'findHomography'
    src_pts = np.array([keypoints1[m.queryIdx].pt for m in good]).astype(np.float32).reshape(-1, 2)
    dst_pts = np.array([keypoints2[m.trainIdx].pt for m in good]).astype(np.float32).reshape(-1, 2)

    # 'cv.RANSAC' is the robust estimation method RANSAC y '3' is the degree of tolerance for declare a point like outlier
    H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 3)

    return H

# Make H of displacement
def desp(d):
    dx,dy = d
    return np.array([
            [1,0,dx],
            [0,1,dy],
            [0,0,1]])

# Apply the 'h' transformation into the plane of 'sizeX x sizeY' with a displacement of 'dx x dy'
def applyTransformation(h,x):
    return cv.warpPerspective(x, desp((dx,dy)) @ h,(sizeX,sizeY))

# Join 'img1' and 'img2' like maximum between them
def joinImages(img1, img2):
    return np.maximum(img1, img2)

# Function which make panoramic with 'images'
def makePanoramic(images):
    # Get the center of image (last image)
    image = images[len(images) - 1]
    for i in reversed(range(0, len(images))):
        img2 = images[i]

        # Calculate keypoints and descriptors vectors
        kps1, desc1 = getKeyPointsAndDescriptorVector(img=img2)
        kps2, desc2 = getKeyPointsAndDescriptorVector(img=image)

        # Calculate better matches between vectors
        good = getBetterMatches(desc1=desc1, desc2=desc2)

        # Calculate homography
        H = calculateHomographyWithRANSAC(keypoints1=kps1, keypoints2=kps2, good=good)

        # Join images
        image = joinImages(applyTransformation(H, img2), applyTransformation(np.eye(3), image))

    return image

# Main function.
def play():

    # Get images of folder params
    images = getImagesOfFolder(folder=args.folder)

    # Make panoramic
    image = makePanoramic(images=images)

    while (True):

        # Get input key
        key = getInputKey()

        if key == escKey: break

        # Show image
        cv.imshow(programName, image)

if __name__ == "__main__":
    play()
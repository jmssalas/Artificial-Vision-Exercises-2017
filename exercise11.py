#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit
# Press 'Enter' key for make transformation
# Press 'd' key for calculate distance between points
# Press 'c' key for clear all points
# Use mouse for select points

# Execute: ./exercise11.py [-h] source reference
# where:
#   - source is the source image
#   - reference is the reference image
# Use -h option for help

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Rectifica la imagen de un plano para medir distancias (tomando referencias manualmente)
##################################

import numpy            as np
import cv2              as cv
import argparse

from    os.path         import isfile


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('source', help='Source image')
parser.add_argument('reference', help='Reference image')
args = parser.parse_args()

# Check if 'source' param is not a file. If it's not file, then exit
if not isfile(args.source):
    print('Error: {} is not a file'.format(args.source))
    exit(-2)

# Check if 'reference' param is not a file. If it's not file, then exit
if not isfile(args.reference):
    print('Error: {} is not a file'.format(args.reference))
    exit(-2)



programName = 'exercise11'          # Program name

srcWindow = programName + ' - source'           # Original image's window
refWindow = programName + ' - reference'        # Reference image's window
dstWindow = programName + ' - transformed'      # Transformed image's window

escKey = 27                         # Escape key code
enterKey = 10                       # Enter key code
distanceKey = ord('d')              # distance key code
clearKey = ord('c')                 # clear key code

srcPoints = list()                  # List of points selected in srcWindow
refPoints = list()                  # List of points selected in refWindow
dstPoints = list()                  # List of points selected in dstWindow

# Dictionary of lists of points
points = {srcWindow: srcPoints, refWindow: refPoints, dstWindow: dstPoints}

# P1-P2 points on reference Image
p1, p2 = None, None
# Real distance between P1-P2 on reference image
measurement = 0

# This variables are for modify the references points before make transformation
dx = 100    # displacement in X
dy = 500    # displacement in Y
sx = 0.5    # scale factor in X
sy = 0.5    # scale factor in Y


# Mouse event handler
def srcMouseEventHandler(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        srcPoints.append((x,y))
        putPoint(image=srcImage, point=(x,y), text='p'+str(len(srcPoints)))

# Mouse event handler
def dstMouseEventHandler(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        dstPoints.append((x, y))
        putPoint(image=dstImage, point=(x,y), text='p'+str(len(dstPoints)))

# Mouse event handler
def refMouseEventHandler(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        refPoints.append((x, y))
        putPoint(image=refImage, point=(x,y), text='p'+str(len(refPoints)))


# Set window's name
cv.namedWindow(srcWindow)
# Set mouseCallback to srcMouseEventHandler
cv.setMouseCallback(srcWindow, srcMouseEventHandler)

# Set window's name
cv.namedWindow(refWindow)
# Set mouseCallback to refMouseEventHandler
cv.setMouseCallback(refWindow, refMouseEventHandler)


# Read image in BGR
def readbgr(file):
    return cv.imread(file)

# Get input key
def getInputKey():
    return cv.waitKey(1) & 0xFF

# Put 'text' param above 'image' param in the 'origin' position
def putText(image, text, origin):
    cv.putText(img=image, text=text, org=origin, fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,255,0))  # Draw the text

# Draw circle above 'image' with center in 'point' point
def drawCircle(image, point):
    cv.circle(img=image, center=point, radius=1, color=(0, 255, 0))

# Put 'point' point above 'image' image with 'text' text
def putPoint(image, point, text):
    drawCircle(image=image, point=point)
    x,y = point
    putText(image=image, text=text, origin=(x+1,y+1))

# Draw line above 'image' with origin 'origin' and destination 'destination'
def drawLine(image, origin, destination) :
    cv.line(img=image, pt1=origin, pt2=destination, color=(0, 255, 0))


# Make a vector (array 1D)
def vec(*argn):
    return np.array(argn)

# Make H of displacement
def desp(d):
    dx,dy = d
    return np.array([
            [1,0,dx],
            [0,1,dy],
            [0,0,1]])

# Make H of scale
def scale(s):
    sx,sy = s
    return np.array([
            [sx,0,0],
            [0,sy,0],
            [0,0,1]])

# Convert a normal points to homogeneous points
def homog(x):
    ax = np.array(x)
    uc = np.ones(ax.shape[:-1]+(1,))
    return np.append(ax,uc,axis=-1)

# Convert a homogeneous points to normal points
def inhomog(x):
    ax = np.array(x)
    return ax[..., :-1] / ax[...,[-1]]

# Apply a homogeneous transformation 'h' to 'x' normal points
def htrans(h,x):
    return inhomog(homog(x) @ h.T)



# Convert list to array
def convertListToArray(list):
    return np.array(list).reshape(-1, 2)

# Function which make transformation of source image above reference image
def makeTransformation():
    global dstImage, dstOriginal

    # I do it here because if I do it when set the others windows
    # a black window will be showed and this does not have much sense
    # Set window's name
    cv.namedWindow(dstWindow)
    # Set mouseCallback to dstMouseEventHandler
    cv.setMouseCallback(dstWindow, dstMouseEventHandler)


    # Convert points lists to arrays
    view = convertListToArray(srcPoints)
    dst = convertListToArray(refPoints)

    # Modify a little the reference image
    dst = htrans(desp(vec(dx,dy)) @ scale(vec(sx, sy)), dst)

    # Find homography
    H, _ = cv.findHomography(view, dst)

    # Undo transformation
    dstOriginal = cv.warpPerspective(srcOriginal, H, (800,800))
    dstImage = np.copy(dstOriginal)

# Function which convert 'distance' in pixel to 'measurement' measurement
def convertDistance(distance, measurement):
    # Calculate distance between p1 and p2
    distP1P2 = np.sqrt(np.sum((vec(p2) - vec(p1)) ** 2))

    return distance*measurement/distP1P2

# Function which calculate distance between points of transformed image
def calculateDistances():
    print('The distance is:')

    distance = 0.0
    # For each couple of points
    for p1, p2 in [ (vec(x), vec(y)) for (x,y) in zip(dstPoints, dstPoints[1:]) ]:
        # Calculate distance
        dis = np.sqrt(np.sum((p2 - p1) ** 2))
        distance += dis

    realDistance = convertDistance(distance, measurement)

    # Put real distance above 'dstImage'
    putText(image=dstImage, text='The real distance is '+str(realDistance), origin=(20,20))
    # Print real distance for console
    print('The real distance is', realDistance)


# Clear points lists
def clearPointsLists():
    for list in points.values():
        list.clear()

# Restart images
def restartImages():
    global srcImage, refImage, dstOriginal, dstImage
    srcImage = np.copy(srcOriginal)
    refImage = np.copy(refOriginal)

    if dstOriginal is not None:
        dstImage = np.copy(dstOriginal)

# Check if reference points above 'transformed' image have been selected.
# It is for getting a reference distance for calculating real distance between two points.
def checkIfReferencePointsHaveBeenSelected() :
    global measurement, p1, p2

    if p1 is not None or p2 is not None:
        return True

    if len(dstPoints) != 2:
        print('ERROR: You must select only two points')
        exit(-3)

    # Ask the real distance between P1-P2 on reference image
    measurement = float(input('Introduce the real distance between P1-P2:'))
    # Get P1-P2 points of refPoints before clear point list
    p1 = dstPoints[0]; p2 = dstPoints[1]

    clearPointsLists(); restartImages()

    return False


srcOriginal = readbgr(args.source)
refOriginal = readbgr(args.reference)
dstOriginal = None

srcImage = None
refImage = None
dstImage = None

# Main function.
def play():
    restartImages()

    while (True):

        # Get input key
        key = getInputKey()

        if key == escKey: break

        if key == enterKey:
            srcLen = len(srcPoints)
            refLen = len(refPoints)

            # Only make transformation if the points have been selected
            if srcLen != 0 and refLen != 0:
                # Check if there are same points in source and reference images
                if srcLen != refLen :
                    print('ERROR: The points on source and reference windows must be equals')
                    exit(-1)

                # Make transformation
                makeTransformation()

                # Clear points and restart images for can select others points
                clearPointsLists()
                restartImages()

                print('First, select only two reference point above transformed window. After, press "d".')

        if key == distanceKey:
            # Check if the transformation has been make before calculatedistances
            if dstImage is None:
                print('ERROR: First, you must make transformation')
                exit(-3)

            if not checkIfReferencePointsHaveBeenSelected() :
                print('Now, select points for calculate distance and press "d" again.')

            # Only calculate distances when at least two points have been selected
            if len(dstPoints) > 1:
                calculateDistances()

        if key == clearKey:
            clearPointsLists()
            restartImages()

        # Show frames
        cv.imshow(srcWindow, srcImage)
        cv.imshow(refWindow, refImage)
        if dstImage is not None:
            cv.imshow(dstWindow, dstImage)


if __name__ == "__main__":
    play()
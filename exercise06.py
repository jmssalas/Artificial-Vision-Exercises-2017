#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit
# Press 'Enter' key for select background

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Implementar el efecto chroma con imágenes en vivo de la webcam.
## Pulsando una tecla se captura el fondo y los objetos que aparezcan
## se superponen en otra imagen o secuencia de video. Comparar con backsub.py.
##################################

import numpy            as np
import cv2              as cv


programName = 'exercise06'          # Program name

escKey = 27                         # Escape key code
enterKey = 10                       # Enter key code

file = 'cube3.png'                  # Image when put objects of chroma

threshold = 25                      # Initial threshold

# Function which update threshold from trackbar
def update(v):
 global threshold
 threshold = v

# Set window's name
cv.namedWindow(programName)
# Create Trackbar on main window
cv.createTrackbar('Threshold', programName, threshold, 255, update)
# Change window's dimensions
cv.resizeWindow(programName, 550, 100)



# Function which get current frame
def getFrame(cap):
    # Read frame
    ret, fr = cap.read()
    return fr


# Convert BGR to YUV
def bgr2yuv(image):
    return cv.cvtColor(image, cv.COLOR_BGR2YUV)


# Get difference between 'frame1' and 'frame2' frames above axis=2
def compareFrames(frame1, frame2):
    return np.sum(abs(frame1.astype(float) - frame2.astype(float)), axis=2)


# Read image with 'file' name
def readImage(file):
    return cv.imread("images/" + file)


# Function which make chroma and get difference between 'background' and 'frame'
# for get mask and cut new object above other image
def makeChroma(background, frame):
    # Convert to YUV
    backyuv = bgr2yuv(background)
    frameyuv = bgr2yuv(frame)

    # Select U and V channels
    backuv = backyuv[:,:,[1,2]]
    frameuv = frameyuv[:,:,[1,2]]

    # Compare frames
    diff = compareFrames(frame1=frameuv, frame2=backuv)

    # Get mask
    mask = diff > threshold
    r, c = mask.shape

    # Convert mask to (0,255) range
    mask = np.clip(mask * 255, 0, 255).astype(np.uint8)
    # Convert mask to 3D and boolean
    mask3 = mask.reshape(r, c, 1).astype(bool)

    # Read image
    img = readImage(file)
    # Resize image
    image = cv.resize(img, (c,r))

    # Get objects of mask and put it above image
    np.copyto(image, frame, where=mask3)

    # Show mask
    cv.imshow('mask', mask)

    # Show objects
    cv.imshow('objects', image)

# Main function.
# Default -> dev = 0
def play(dev=0):
    background = None  # Background

    cap = cv.VideoCapture(dev)

    while (True):

        # Process Key
        key = cv.waitKey(1) & 0xFF

        if key == escKey: break

        # Get frame
        frame = getFrame(cap=cap)

        # Press enter key to select the background
        if key == enterKey:
            background = frame

        # Show frame
        cv.imshow(programName, frame)

        # If background has been selected, make chroma
        if background is not None:
            makeChroma(background=background, frame=frame)


if __name__ == "__main__":
    play()
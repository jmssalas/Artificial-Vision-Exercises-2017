#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit
# Press 'f' key for entry in oneFaceMode
# Use mouse for select face in oneFaceMode

# Execute: ./blurring-faces.py [-h] [-path PATH]
# options:
#   - [-h] for help
#   - [-path PATH] for indicate the path of library: default it uses: $HOME/miniconda3/share/OpenCV/haarcascades/' (adaboost)

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Detección de caras con la webcam en vivo, con emborronamiento de las mismas.
##################################

import numpy            as np
import cv2              as cv
import argparse

from   os               import environ


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-path', help='Path of library. Default: $HOME/miniconda3/share/OpenCV/haarcascades/')
args = parser.parse_args()
parser.print_help()

cpath = environ['HOME']+'/miniconda3/share/OpenCV/haarcascades/'

# Check if 'source' param is not a file. If it's not file, then exit
if args.path:
    cpath = args.path


face_cascade = cv.CascadeClassifier(cpath+'/haarcascade_frontalface_default.xml')

if face_cascade.empty():
    print('ERROR: The library has not can be loaded. Check the path.')
    exit(-1)



programName = 'exercise11'          # Program name

escKey = 27                         # Escape key code
enterKey = 10                       # Enter key code
oneFaceKey = ord('f')               # One face mode key code


drawing, lButtonUp = False, False   # - 'drawing' indicates that ROI rectangle is drawing
                                    # - 'lButtonUp' indicates that when left button up event happens,
                                    #    if mouse move event happens, then ROI rectangle doesn't change.

initialPosition = -1                        # Initial position

x0, y0 = initialPosition, initialPosition   # ROI's Initial position
xf, yf = initialPosition, initialPosition   # ROI's Final position

method  = cv.xfeatures2d.SIFT_create()  # Keypoints method
bf      = cv.BFMatcher()                # Matcher

minMatches = 5							# Minimum matches between getters faces and selected face
selectedFace = None                     # Selected faces to oneFacesMode
sigma = 15                              # Blurring factor


# Function which update minMatches from trackbar
def update(v):
 global minMatches
 minMatches = v

# Mouse event handler
def mouseEventHandler(event, x, y, flags, param):
    global x0, y0, xf, yf, drawing, lButtonUp

    if event == cv.EVENT_LBUTTONDOWN:  # Indicate init ROI rectangle
        drawing = True
        lButtonUp = False
        x0, y0 = x, y
        xf, yf = x0, y0

    elif event == cv.EVENT_MOUSEMOVE:  # Indicate changes of ROI rectangles
        if drawing and not lButtonUp:
            xf, yf = x, y

    elif event == cv.EVENT_LBUTTONUP:  # Indicate final ROI rectangle
        if drawing:
            xf, yf = x, y
            # Check ROI's points sign
            if yf < y0:
                aux = y0; y0 = yf; yf = aux

            if xf < x0:
                aux = x0; x0 = xf; xf = aux

            lButtonUp = True

# Set window's name
cv.namedWindow(programName)
# Set mouseCallback to mouseEventHandler
cv.setMouseCallback(programName, mouseEventHandler)

# Function which get current frame
def getFrame(cap):
    # Read frame
    ret, fr = cap.read()
    return fr

# Get input key
def getInputKey():
    return cv.waitKey(1) & 0xFF

# Function which returns descriptor vector of 'img'
def getDescriptorVector(img):
    return method.detectAndCompute(img, mask=None)[1]

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

# Function which draws ROI selected above 'frame' param with
# first vertex 'p0' and second vertex 'p1' and color 'color' param
def drawROI(frame, p0, pf, color):
    cv.rectangle(frame, p0, pf, color)



# Function which detects faces in 'img' image with 'face_cascade'
def detectFaces(img):
    return face_cascade.detectMultiScale(img)

# Do blurring above rectangle (x,y,w,h), image 'img' and 'sigma' blurring factor
def doBlurring(x,y,w,h,img,sigma):
    # Get face of image
    face = img[y:y + h, x:x + w]
    # Blurring face
    blur = cv.GaussianBlur(face, (0, 0), sigma)
    # Set face
    img[y:y + h, x:x + w] = blur

# Fuction which blurring 'faces' in 'img'
def blurringFaces(faces, img):
    for (x, y, w, h) in faces:
        #cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        doBlurring(x,y,w,h,img,sigma)


# Function which searches the face which has got like descriptor 'descriptor'
# in all image 'img' and if finds it, then blurring it.
def blurringFace(descriptor, img):

    # Detect all faces in 'img'
    faces = detectFaces(img=img)

    # For each face
    for (x, y, w, h) in faces:
        faceImg = img[y:y + h, x:x + w]

        # Get descriptor vector of 'faceImg'
        descFace = getDescriptorVector(img=faceImg)

        # Get better matches between 'descriptor' and 'descFace'
        matches = getBetterMatches(descriptor, descFace)

        # Check number of matches. If it is bigger than 'minMatches', then blurring face
        if len(matches) >= minMatches :
            doBlurring(x,y,w,h,img,sigma)


# One Face Mode -> Face selected with ROI
def oneFaceMode(cap):
    global lButtonUp, drawing, x0, xf, y0, yf

    # Create Trackbar on main window
    cv.createTrackbar('minMatches', programName, minMatches, 255, update)

    # Descriptor of selected face
    faceDesc = None

    while True:
        # Get input key
        key = getInputKey()

        if key == escKey: break

        # Get frame
        frame = getFrame(cap=cap)

        # Press enter key to select the ROI
        if key == enterKey:
            # Restart values of mouse's events
            lButtonUp = False
            drawing = False

            # Get descriptor vector of selected face
            faceDesc = getDescriptorVector(img=frame[y0:yf + 1, x0:xf + 1])

            # Delete ROI selection
            x0, y0, xf, yf = initialPosition, initialPosition, initialPosition, initialPosition

        if faceDesc is not None:
            blurringFace(descriptor=faceDesc, img=frame)

        # Draw ROI
        drawROI(frame=frame, p0=(x0, y0), pf=(xf, yf), color=(0, 255, 0))

        # Show frame
        cv.imshow(programName, frame)

    # Delete window for delete trackbar
    cv.destroyWindow(programName)

# Main function.
# Default -> dev = 0
def play(dev=0):

    cap = cv.VideoCapture(dev)

    while (True):

        # Get input key
        key = getInputKey()

        if key == escKey: break

        if key == oneFaceKey:
            # Activate one face mode
            oneFaceMode(cap=cap)

        # Get frame
        frame = getFrame(cap=cap)

        # Detect all faces
        faces = detectFaces(img=frame)
        # Blurring them
        blurringFaces(faces=faces, img=frame)

        # Show frame
        cv.imshow(programName, frame)

if __name__ == "__main__":
    play()
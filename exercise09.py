#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit
# Press 'Enter' key for process frame
# Use mouse for select ROI

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Reconocimiento de objetos con la webcam basado en el número de coincidencias de keypoints.
## Pulsando una tecla se pueden ir guardando modelos (p. ej. carátulas de CD). Cuando detectamos
## que la imagen está bastante quieta, o cuando se pulse otra tecla, calculamos los puntos de
## interés de la imagen actual y sus descriptores y vemos si hay suficientes coincidencias con los de algún modelo.
##################################

import numpy             as np
import cv2               as cv

programName = 'exercise09'

drawing, lButtonUp = False, False   # - 'drawing' indicates that ROI rectangle is drawing
                                    # - 'lButtonUp' indicates that when left button up event happens,
                                    #    if mouse move event happens, then ROI rectangle doesn't change.

initialPosition = -1                        # Initial position

x0, y0 = initialPosition, initialPosition   # ROI's Initial position
xf, yf = initialPosition, initialPosition   # ROI's Final position

# Key's code
escKey      = 27        # Escape key code
enterKey    = 10        # Enter key code
saveKey     = ord('s')	# Save key code


method  = cv.xfeatures2d.SIFT_create()  # Keypoints method
bf      = cv.BFMatcher()                # Matcher

models = list()							# List of models
minMatches = 5							# Minimum matches between frame and model

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
# Create Trackbar on main window
cv.createTrackbar('minMatches', programName, minMatches, 255, update)
# Change window's dimensions
cv.resizeWindow(programName, 550, 100)


# Function which draw ROI selected above 'frame' param with
# first vertex 'p0' and second vertex 'p1' and color 'color' param
def drawROI(frame, p0, pf, color):
    cv.rectangle(frame, p0, pf, color)

# Get input key
def getInputKey():
    return cv.waitKey(1) & 0xFF

# Get current frame
def getFrame(cap):
    ret, frame = cap.read()
    return frame #cv.cvtColor(frame, cv.COLOR_BGR2RGB)

# Function which returns descriptor vector of 'img'
def getDescriptorVector(img):
    return method.detectAndCompute(img, mask=None)[1]

# Function which calculates better coindicences between descriptor vectors
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

# Function which processes current 'frame' searching matches with models
def processFrame(frame):
    numModel = 1    # Number of closer model for show it

    # Get descriptor vector of 'frame'
    descFrame = getDescriptorVector(img=frame)

    # Foreach models
    for (desc, model) in models :
        # Get better matches between 'desc' and 'descFrame'
        matches = getBetterMatches(desc, descFrame)

        # Check number of matches. If it is bigger than 'minMatches', then show model in other window
        if len(matches) >= minMatches :
            cv.imshow('model '+str(numModel), model)
            numModel += 1

# Main function.
# Default -> dev = 0
def play(dev=0):
    global drawing, lButtonUp, x0, y0, xf, yf

    cap = cv.VideoCapture(dev)

    while True :
        # Get input key
        key = getInputKey()

        # Process input key
        if key == escKey: break

        frame = getFrame(cap=cap)

        # Press enter key to select the ROI
        if key == saveKey :
            # Restart values of mouse's events
            lButtonUp = False
            drawing = False

            # Select ROI
            roi = np.copy(frame[y0:yf + 1, x0:xf + 1])
            # Get descriptor vector of ROI
            desc = getDescriptorVector(img=roi)
            # Append desc and roi to models
            models.append((desc,roi))
            # Show selected ROI
            cv.imshow('roi', roi)

        # Press 'Enter' key for process current frame
        if key == enterKey:
            # Process frame
            processFrame(frame=frame)
            # Delete ROI selection
            x0, y0, xf, yf = initialPosition, initialPosition, initialPosition, initialPosition

        # Draw ROI
        drawROI(frame=frame, p0=(x0, y0), pf=(xf, yf), color=(0, 255, 0))

        # Show frame
        cv.imshow(programName, frame)


if __name__ == "__main__":
    play()
#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit
# Press 'Enter' key for capture ROI

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Construye un clasificador de objetos en base a la similitud de
## los histogramas de color del ROI (de los 3 canales por separado). Apóyate en exercise02.
##################################

import numpy             as np
import cv2               as cv

programName = 'exercise03'          # Program's name

roi = None                          # ROI selected
roiHistogram = None                 # ROI's histogram
maxDiff = 0.2                       # Max difference between ROI selected and current frame

drawing, lButtonUp = False, False   # - 'drawing' indicates that ROI rectangle is drawing
                                    # - 'lButtonUp' indicates that when left button up event happens,
                                    #    if mouse move event happens, then ROI rectangle doesn't change.

x0, y0 = -1, -1                     # ROI's Initial position
xf, yf = -1, -1                     # ROI's Final position

escKey = 27                         # Escape key code
enterKey = 10                       # Enter key code


# Function which get histogram of 'frame' param
def getHistogram(frame):
    v = cv.calcHist(images=[frame], channels=[0, 1, 2], mask=None, histSize=[8, 8, 8], ranges=[0, 256, 0, 256, 0, 256])
    v = v.flatten()
    hist = v / sum(v)
    return hist

# Function which get current frame
def getFrame(cap):
    # Read frame
    ret, fr = cap.read()
    return fr


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
            lButtonUp = True


# Set window's name
cv.namedWindow(programName)
# Set mouseCallback to mouseEventHandler
cv.setMouseCallback(programName, mouseEventHandler)


# Function which draw ROI selected above 'frame' param with
# first vertex 'p0' and second vertex 'p1' and color 'color' param
def drawROI(frame, p0, pf, color):
    cv.rectangle(frame, p0, pf, color)


# Function which process 'frameToProcess' param to search similar object on ROI
# and draws above 'frameToDraw' if it has found similar object on ROI
def processFrame(frameToProcess, frameToDraw):
    if roi is None: return  # If ROI hasn't been selected, return

    # Else, get RGB histogram of 'frame':
    frameroi = frameToProcess[y0:yf + 1, x0:xf + 1]

    frameHistogram = getHistogram(frameroi)

    # Get difference between current frame and ROI histograms
    diff = cv.compareHist(roiHistogram, frameHistogram, method=cv.HISTCMP_CHISQR)

    # If diff is smaller than or equals maxDiff, change ROI's color
    if diff <= maxDiff:
        drawROI(frame=frameToDraw, p0=(x0, y0), pf=(xf, yf), color=(255, 0, 0))


# Main function.
# Default -> dev = 0
def play(dev=0):
    global roi, roiHistogram, x0, y0, xf, yf

    cap = cv.VideoCapture(dev)

    pausa = False
    while (True):

        # Process Key
        key = cv.waitKey(1) & 0xFF

        if key == escKey: break
        if key == ord(' '): pausa = not pausa
        if pausa: continue

        # Get frame
        frame = getFrame(cap=cap)

        # Press enter key to select the ROI
        if key == enterKey:
            # Check ROI's points sign
            if yf < y0:
                aux = y0; y0 = yf; yf = aux

            if xf < x0:
                aux = x0; x0 = xf; xf = aux

            roi = np.copy(frame[y0:yf + 1, x0:xf + 1])
            roiHistogram = getHistogram(roi)
            cv.imshow('roi', roi)

        # Draw ROI rectangle above copy frame readed because if draw above origin frame,
        # when capture the same region of frame to calculate difference between ROI, the rectangle
        # is shown on the frame.
        framecpy = np.copy(frame)
        drawROI(frame=framecpy, p0=(x0, y0), pf=(xf, yf), color=(0, 255, 0))
        # Process current frame to search similar objects on ROI
        processFrame(frameToProcess=frame, frameToDraw=framecpy)

        # Show frame
        cv.imshow(programName, framecpy)


if __name__ == "__main__":
    play()
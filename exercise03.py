#!/usr/bin/env python

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Construye un clasificador de objetos en base a la similitud de
## los histogramas de color del ROI (de los 3 canales por separado). Apóyate en exercise02.
##################################

import numpy             as np
import cv2               as cv

frame           = None              # Current Frame
roi             = None              # ROI selected
roiHistogram    = None				# ROI's histogram
maxDiff         = 25000               # Max difference between ROI selected and current frame 


drawing, lButtonUp = False, False   # - 'drawing' indicates that ROI rectangle is drawing
									# - 'lButtonUp' indicates that when left button up event happens, 
                                	#    if mouse move event happens, then ROI rectangle doesn't change. 

x0, y0 = -1, -1                 	# ROI's Initial position
xf, yf = -1, -1                 	# ROI's Final position

escKey      = 27                    # Escape key code
enterKey    = 10                   	# Enter key code

R = 0                               # R channel                               
G = 1                               # G channel
B = 2                               # B channel

# Function which get RGB histogram of 'frame' param
def getRGBHistogram(frame):
	rgbHistogram = list()
	h,b = np.histogram(frame[:,:,R], bins=256)
	rgbHistogram.append(h)

	h,b = np.histogram(frame[:,:,G], bins=256)
	rgbHistogram.append(h)

	h,b = np.histogram(frame[:,:,B], bins=256)
	rgbHistogram.append(h)

	return rgbHistogram

# Mouse event handler
def mouseEventHandler(event, x, y, flags, param):
    global x0,y0,xf,yf,drawing,lButtonUp

    if event == cv.EVENT_LBUTTONDOWN: # Indicate init ROI rectangle
        drawing = True
        lButtonUp = False
        x0, y0 = x, y
        xf, yf = x0, y0

    elif event == cv.EVENT_MOUSEMOVE: # Indicate changes of ROI rectangles
        if drawing and not lButtonUp:
            xf, yf = x, y
        
    elif event == cv.EVENT_LBUTTONUP: # Indicate final ROI rectangle
        if drawing:
            xf, yf = x, y
            lButtonUp = True

# Set window's name
cv.namedWindow("webcam")
# Set mouseCallback to mouseEventHandler
cv.setMouseCallback("webcam", mouseEventHandler)

# Function which draw ROI selected above 'frame' param with
# first vertex 'p0' and second vertex 'p1' and color 'color' param
def drawROI(frame, p0, pf, color):
    cv.rectangle(frame, p0, pf, color)

# Function which process 'frame' param to search similar object to ROI
def processFrame(frame):
    if (roi is None) : return # If ROI hasn't been selected, return

    # Else, get RGB histogram of 'frame':
    frameHistogram = getRGBHistogram(frame[x0:xf+1, y0:yf+1])

    # Get difference between current frame and ROI histograms
    diff = np.sum(abs(frameHistogram[R] - roiHistogram[R]))
    diff = diff + np.sum(abs(frameHistogram[G] - roiHistogram[G]))
    diff = diff + np.sum(abs(frameHistogram[B] - roiHistogram[B]))

    # If diff is smaller than or equals maxDiff, change ROI's color
    if diff <= maxDiff :
        drawROI(frame = frame, p0 = (x0, y0), pf = (xf, yf), color = (255,0,0))


# Main function. 
# Default -> dev = 0
def play(dev=0):
    global frame,roi,roiHistogram

    cap = cv.VideoCapture(dev)

    pausa = False
    while(True):

        # Process Key
        key = cv.waitKey(1) & 0xFF
        
        # Press enter key to select the ROI
        if key == enterKey :
            roi = np.copy(frame[y0:yf+1, x0:xf+1])
            roiHistogram = getRGBHistogram(roi)
            
        if key == escKey : break
        if key == ord(' ') : pausa = not pausa
        if pausa: continue

        # Read frame
        ret, frame = cap.read()

        # Draw ROI rectangle
        drawROI(frame = frame, p0 = (x0, y0), pf = (xf, yf), color = (0,255,0))
        # Process current frame to search similar objects to ROI
        processFrame(frame)


        # Show frame
        cv.imshow('webcam',frame)

if __name__ == "__main__":
    play()
#!/usr/bin/env python

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Construye un clasificador de objetos en base a la similitud de
## los histogramas de color del ROI (de los 3 canales por separado). Apóyate en exercise02.
##################################

#%matplotlib inline

import numpy             as np
import cv2               as cv
import matplotlib.pyplot as plt
from matplotlib.pylab  import rcParams

def figsize(h=1,v=None):
    if (v==None): v = h
    rcParams['figure.figsize'] = h*6,v*4


frame = None                    	# Current Frame
roi = None                			# ROI selected
roiHistogram = None					# ROI's histogram

drawing, lButtonUp = False, False   # - 'drawing' indicates that ROI rectangle is drawing
									# - 'lButtonUp' indicates that when left button up event happens, 
                                	#    if mouse move event happens, then ROI rectangle doesn't change. 

x0, y0 = -1, -1                 	# ROI's Initial position
xf, yf = -1, -1                 	# ROI's Final position

escKey = 27                     	# Escape key code
enterKey = 10                   	# Enter key code


# Function which get RGB histogram of 'frame' param
def getRGBHistogram(frame):
	rgbHistogram = list()
	h,b = np.histogram(frame[:,:,0], bins=256)
	rgbHistogram.append(h)

	h,b = np.histogram(frame[:,:,1], bins=256)
	rgbHistogram.append(h)

	h,b = np.histogram(frame[:,:,2], bins=256)
	rgbHistogram.append(h)

	return rgbHistogram

# Mouse event handler
def mouseEventHandler(event, x, y, flags, param):
    global x0,y0,xf,yf,drawing,frame,lButtonUp,roi,roiHistogram

    if event == cv.EVENT_LBUTTONDOWN: # Indicate init ROI rectangle
        drawing = True
        x0, y0 = x, y
        xf, yf = x0, y0

    elif event == cv.EVENT_MOUSEMOVE: # Indicate changes of ROI rectangles
        if drawing and not lButtonUp:
            xf, yf = x, y
        
    elif event == cv.EVENT_LBUTTONUP: # Indicate final ROI rectangle
        if drawing:
            xf, yf = x, y
            lButtonUp = True
            roi = np.copy(frame[y0:yf+1, x0:xf+1])
            roiHistogram = getRGBHistogram(roi)


# Set window's name
cv.namedWindow("webcam")
# Set mouseCallback to mouseEventHandler
cv.setMouseCallback("webcam", mouseEventHandler)


def show(roi, frame):
	figsize(3,1)
	plt.subplot(1,3,1)
	plt.bar(range(256), roi[0])
	plt.bar(range(256), roi[1])
	plt.bar(range(256), roi[2])
	plt.title('roi')


	plt.subplot(1,3,2)
	plt.bar(range(256), frame[0])
	plt.bar(range(256), frame[1])
	plt.bar(range(256), frame[2]) 
	plt.title('frame')

	plt.subplot(1,3,3)
	plt.bar(range(256), roi[0] - frame[0])
	plt.bar(range(256), roi[1] - frame[1])
	plt.bar(range(256), roi[2] - frame[2]) 
	plt.title('roi - frame')
	figsize()


# Function which process 'frame' param to search similar object to ROI
def processFrame(frame):
	global roi,roiHistogram

	if (roi is None) : return # If ROI hasn't been selected, return

	# Else, get RGB histogram of 'frame':
	frameHistogram = getRGBHistogram(frame)

	print(np.sum(abs(frameHistogram[0] - roiHistogram[0])))

# Main function. 
# Default -> dev = 0
def play(dev=0):
    global frame,x0,y0,xf,yf,lButtonUp,drawing

    cap = cv.VideoCapture(dev)

    pausa = False
    while(True):

        # Process Key
        key = cv.waitKey(1) & 0xFF
        
        # Press enter key to select the ROI
        if key == enterKey:
            lButtonUp = False
            drawing = False

        if key == escKey: break
        if key == ord(' '): pausa = not pausa
        if pausa: continue

        # Read frame
        ret, frame = cap.read()
        

        if drawing : # Draw ROI rectangle
            cv.rectangle(frame, (x0,y0), (xf, yf), color = (0,255,0))
        else : # Process current frame to search similar objects to ROI
        	processFrame(frame)


        # Show frame
        cv.imshow('webcam',frame)

if __name__ == "__main__":
    play()
#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit
# Press 'Enter' key for clean ROI
# Press 's' key for store selected ROIs
# Use mouse for select ROI

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Amplía 'player.py' para seleccionar con el ratón una región de interés (ROI) y almacenar en una lista imágenes, 
## que pueden opcionalmente guardarse en disco. Este programa nos servirá como base para futuros ejercicios.
##################################


import cv2 as cv
import datetime

programName = 'exercise02'      # Program's name

frame = None                    # Current Frame
drawing, roi = False, False     # - 'drawing' indicates that ROI rectangle is drawing
                                # - 'roi' indicates that when left button up event happens, 
                                #    if mouse move event happens, then ROI rectangle doesn't change. 
x0, y0 = -1, -1                 # Initial position
xf, yf = -1, -1                 # Final position

roiList = list()                # List that contains ROI rectangles selected

escKey = 27                     # Escape key code
enterKey = 10                   # Enter key code


# Mouse event handler
def mouseEventHandler(event, x, y, flags, param):
    global x0,y0,xf,yf,drawing,frame,roi

    if event == cv.EVENT_LBUTTONDOWN: # Indicate init ROI rectangle
        drawing = True
        x0, y0 = x, y
        xf, yf = x0, y0

    elif event == cv.EVENT_MOUSEMOVE: # Indicate changes of ROI rectangles
        if drawing and not roi:
            xf, yf = x, y
        
    elif event == cv.EVENT_LBUTTONUP: # Indicate final ROI rectangle
        if drawing:
            xf, yf = x, y
            # Check ROI's points sign
            if yf < y0:
                aux = y0; y0 = yf; yf = aux

            if xf < x0:
                aux = x0; x0 = xf; xf = aux

            roi = True
            roiList.append(frame[y0:yf+1, x0:xf+1])

# Set window's name
cv.namedWindow(programName)
# Set mouseCallback to mouseEventHandler
cv.setMouseCallback(programName, mouseEventHandler)

# Main function. 
# Default -> dev = 0
def play(dev=0):
    global frame,x0,y0,xf,yf,roi,drawing

    cap = cv.VideoCapture(dev)

    pausa = False
    while(True):

        # Process Key
        key = cv.waitKey(1) & 0xFF
        
        if key == enterKey:
            roi = False
            drawing = False

        if key == escKey: break
        if key == ord(' '): pausa = not pausa
        if pausa: continue

        # Read frame
        ret, frame = cap.read()
        
        # Draw ROI rectangle
        if drawing :
            cv.rectangle(frame, (x0,y0), (xf, yf), color = (0,255,0))

        # Show frame
        cv.imshow(programName,frame)

        # Save ROI
        if key == ord('s'):
            numRoi = 1
            for roi in roiList:
                fname = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                cv.imwrite(fname+'-'+ str(numRoi) + '.png',roi)
                numRoi += 1


if __name__ == "__main__":
    play()
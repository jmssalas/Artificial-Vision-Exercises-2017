#!/usr/bin/env python

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Amplía 'player.py' para seleccionar con el ratón una región de interés (ROI) y almacenar en una lista imágenes, 
## que pueden opcionalmente guardarse en disco. Este programa nos servirá como base para futuros ejercicios.
##################################


import cv2 as cv
import datetime

frame = None
drawing, roi = False, False
x0, y0 = -1, -1
xf, yf = -1, -1

roiList = list()

escKey = 27
enterKey = 10


def mouseEventHandler(event, x, y, flags, param):
    global x0,y0,xf,yf,drawing,frame,roi

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        x0, y0 = x, y
        xf, yf = x0, y0

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing and not roi:
            xf, yf = x, y
        
    elif event == cv.EVENT_LBUTTONUP:
        if drawing:
            xf, yf = x, y
            roi = True
            roiList.append(frame[y0:yf+1, x0:xf+1])


cv.namedWindow("webcam")
cv.setMouseCallback("webcam", mouseEventHandler)


def play(f,dev=0):
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
        cv.imshow('webcam',frame)

        # Save ROI
        if key == ord('s'):
            numRoi = 1
            for roi in roiList:
                fname = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                cv.imwrite(fname+'-'+ str(numRoi) + '.png',roi)
                numRoi += 1


if __name__ == "__main__":
    play(lambda x: 255 - cv.cvtColor(x, cv.COLOR_RGB2GRAY))
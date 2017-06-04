#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Estima "a ojo" el campo de visión y parámetro f de tu cámara
## y comprueba que es consistente con el resultado de la calibración precisa mediante 'chessboard'.
##################################

import numpy            as np
import cv2              as cv

programName = 'exercise14'          # Program name

escKey = 27                         # Escape key code
enterKey = 10                       # Enter key code
distanceKey = ord('d')              # Distance key code
saveKey = ord('s')                  # Save key code
p1, p2 = None, None

# Mouse event handler
def mouseEventHandler(event, x, y, flags, param):
    global p1,p2
    if event == cv.EVENT_LBUTTONDOWN:
        if p1 is None:
            p1 = (x,y)
        else:
            p2 = (x,y)

# Set window's name
cv.namedWindow(programName)
# Set mouseCallback to srcMouseEventHandler
cv.setMouseCallback(programName, mouseEventHandler)


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

# Function which get current frame
def getFrame(cap):
    # Read frame
    ret, fr = cap.read()
    return fr

# Get input key
def getInputKey():
    return cv.waitKey(1) & 0xFF

# Main function.
# Default -> dev = 0
def play(dev=0):
    global p1, p2

    cap = cv.VideoCapture(dev)

    count = 1
    while (True):

        # Get input key
        key = getInputKey()

        if key == escKey: break

        # Get frame
        frame = getFrame(cap=cap)

        if p1 is not None:
            putPoint(frame, p1, 'p1')
        if p2 is not None:
            putPoint(frame, p2, 'p2')

        if p1 is not None and p2 is not None:
            if key == distanceKey:
                # Calculate distance
                distance = np.sqrt(np.sum((np.array(p2) - np.array(p1)) ** 2))
                # Show distance
                print(distance)

        if key == saveKey:
            print(frame.shape)
            cv.imwrite('image'+str(count)+'.png', frame)
            count += 1

        # Show frame
        cv.imshow(programName, frame)

if __name__ == "__main__":
    play()
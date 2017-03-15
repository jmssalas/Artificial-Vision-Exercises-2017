#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Programa de reconocimiento de formas con la webcam basado
## en descriptores frecuenciales. Posibles aplicaciones: reconocimiento de matrículas.
##################################

import numpy             as np
import cv2               as cv

programName = 'exercise10'

# Key's code
escKey          = 27    # Escape key code
enterKey        = 10    # Enter key code


# Get input key
def getInputKey():
    return cv.waitKey(1) & 0xFF

# Get current frame
def getFrame(cap):
    ret, frame = cap.read()
    return frame #cv.cvtColor(frame, cv.COLOR_BGR2RGB)


# Main function.
# Default -> dev = 0
def play(dev=0):

    cap = cv.VideoCapture(dev)

    while True :
        # Get input key
        key = getInputKey()

        # Process input key
        if key == escKey: break

        frame = getFrame(cap=cap)

        cv.imshow(programName, frame)


if __name__ == "__main__":
    play()
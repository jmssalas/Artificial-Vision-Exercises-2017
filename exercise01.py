#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Modificación de los canales de color (brillo, saturación, etc.) sobre la secuencia de imágenes tomada con la webcam.
##################################

import cv2 as cv

programName = 'exercise01'          # Program's name

cap = cv.VideoCapture(0)

while(cv.waitKey(1) != 27):
    ret, frame = cap.read()

    # Do copy for avoid aliasing
    copy = frame.copy()

    # Convert RGB to HLS
    hls = cv.cvtColor(copy,cv.COLOR_BGR2HLS)
    
    # Modify L and S channels
    hls[:,:,2] = 255
    hls[:,:,1] = 128

    # Convert HLS to RGB
    copy = cv.cvtColor(hls, cv.COLOR_HLS2BGR)
    
    # Show image
    cv.imshow(programName,copy)

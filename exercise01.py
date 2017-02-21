#!/usr/bin/env python

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Modificación de los canales de color (brillo, saturación, etc.) sobre la secuencia de imágenes tomada con la webcam.
##################################

import cv2 as cv

cap = cv.VideoCapture(0)

while(cv.waitKey(1) != 27):
    ret, frame = cap.read()

    # Do copy for avoid aliasing
    copy = frame.copy()

    # Convert RGB to HLS
    hls = cv.cvtColor(copy,cv.COLOR_RGB2HLS)
    
    # Modify L and S channels
    hls[:,:,2] = 255
    hls[:,:,1] = 128

    # Convert HLS to RGB
    copy = cv.cvtColor(hls, cv.COLOR_HLS2RGB)
    
    # Show image
    cv.imshow('webcam',copy)

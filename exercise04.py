#!/usr/bin/env python

# Code on Github repository: git@github.com:jmssalas/Artificial-Vision-Exercises-2017.git

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Construye un generador que detecte frames estáticos,
## o frames en movimiento, a partir de una secuencia de imágenes. Apóyate en 'deque.py'.
##################################

import numpy        as          np
import cv2          as          cv
from collections    import      deque
from umucv.stream   import      mkStream

from exercise03 import getHistogram

programName = 'exercise04'          # Program name
escKey = 27                         # Escape key code
maxDiff = 250000                   # Max difference between folowed frame

# Function which makes a history of 'n' frames of 'stream' stream
def history(stream, n):
    d = deque(maxlen=n)
    for k in range(n-1):
        d.append(next(stream))
    while True:
        d.append(next(stream))
        yield np.array(d)


# Get difference between 'frame1' and 'frame2' frames.
def compareFrames(frame1, frame2):
    return np.sum(abs(frame1.astype(float) - frame2.astype(float)))


# Get current frame of 'list'
def currentFrame(list):
    return list[nframes-1]


# Get previous frame of 'list'
def previousFrame(list):
    return list[nframes-2]


stream = mkStream(sz=(200,200), dev='0')    # Make a stream with size = (200,200) and dev = 0
nframes = 9                                # Num of frames
for h in history(stream, nframes):

    # Show history's frames
    row1 = np.hstack([h[8],h[7],h[6]])
    row2 = np.hstack([h[5],h[4],h[3]])
    row3 = np.hstack([h[2],h[1],h[0]])
    image = np.vstack([row1,row2,row3])
    cv.imshow(programName, image)

    # Calculate differences between current frame and previous frame
    diff = compareFrames(currentFrame(h),previousFrame(h))

    # If difference is bigger than 'maxDiff' -> A movement has been detected
    if diff >= maxDiff:
        print('I caught you!')

    if cv.waitKey(1) == escKey: break;
#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Needed library:  pip install --upgrade https://robot.inf.um.es/material/umucv.tar.gz

# Press 'Esc' key for exit
# Use mouse for select point where move image

# Execute: ./exercise13.py [-h] [--dev DEV] [--size SIZE]
# options:
#   - [-h] for help
#   - [--dev DEV] for indicate device of program: video file or webcam device (default=0)
#   - [--size SIZE] for indicate size of image with format: wxh (default=640x480)

# A example with video file:
# ./exercise13.py --dev=file:images/rot4.mjpg

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Crea un efecto de realidad aumentada dinámico.
## (Nota del autor: En esta versión, puedes clickar en la pantalla para que la
##   imagen virtual se mueva a ese punto).
##################################

import cv2          as cv
import numpy        as np
import numpy.linalg as la

from umucv.stream   import mkStream, withKey
from umucv.htrans   import htrans, pose, kgen
from umucv.util     import lineType, cube, showCalib
from umucv.contours import extractContours, redu

programName = 'exercise13'          # Program name

escKey = 27                         # Escape key code

import argparse

def readsize(s):
    try:
        return map(int, s.split('x'))
    except:
        raise argparse.ArgumentTypeError("size must be wxh")

parser = argparse.ArgumentParser()
parser.add_argument('--dev', type=str, default='0', help='image source ')
parser.add_argument('--size', help='image size', type=readsize, default=(640,480))
args = parser.parse_args()

# Virtual image
imvirt = cv.resize(cv.imread('images/thing.png'),(200,200))

# Stream of images
stream = mkStream(args.size, args.dev)

# Size of images
HEIGHT, WIDTH = next(stream).shape[:2]
size = WIDTH,HEIGHT
print(size)

# Calibration matrix
K = kgen(size,1.7) # fov aprox 60 degree

print(K)

# Marker
marker = np.array(
       [[0,   0,   0],
        [0,   1,   0],
        [0.5, 1,   0],
        [0.5, 0.5, 0],
        [1,   0.5, 0],
        [1,   0,   0]])

poses = None                    # Matrix of cameras
worldX, worldY = None, None     # World coordinates

# Mouse event handler
def mouseEventHandler(event, x, y, flags, param):
    global poses, worldX, worldY

    if event == cv.EVENT_LBUTTONDOWN:
        # If there is not camera, return
        if poses is [] or poses is None: return;

        p = poses[0]                                # Get first camera
        H = getHOfCameraMatrix(camera=p)            # Get H homography of 'p'
        invH = la.inv(H)                            # Get inverse of H
        worldPoint = htrans(invH, (x, y))           # Get worldPoint of image point (x,y)
        worldX = round(worldPoint[0], ndigits=2)    # Get coordinate X (round with 2 digits)
        worldY = round(worldPoint[1], ndigits=2)    # Get coordinate Y (round with 2 digits)
        print('x =',worldX,', y =',worldY)          # Print worldPoint (X,Y)

# Set window's name
cv.namedWindow(programName)
# Set mouseCallback to srcMouseEventHandler
cv.setMouseCallback(programName, mouseEventHandler)

# Get H homography of camera matrix 'camera' 3x4 with contains
# the dimensions 0,1, and 3 of 'camera'.
def getHOfCameraMatrix(camera):
    H = np.zeros(shape=(3,3))
    H[:,0] = camera[:,0]; H[:,1] = camera[:,1]; H[:,2] = camera[:,3]
    return H

# Draw circle above 'image' with center in 'point' point
def drawCircle(image, point):
    cv.circle(img=image, center=point, radius=5, color=(0, 255, 0))

# Put 'point' point above 'image' image
def putPoint(image, point):
    x,y = point
    drawCircle(image=image, point=(int(x), int(y)))

# Utils functions given by teacher
def polygons(cs,n,prec=2):
    rs = [ redu(c,prec) for c in cs ]
    return [ r for r in rs if len(r) == n ]

def rots(c):
    return [np.roll(c,k,0) for k in range(len(c))]

def bestPose(K,view,model):
    poses = [ pose(K, v.astype(float), model) for v in rots(view) ]
    return sorted(poses,key=lambda p: p[0])[0]


# Variables of shift
dx = 0.0
dxReturn = False
dy = 0.0
dyReturn = False

# Function which move points of virtual image
def moveImage() :
    global dx,dy,dxReturn,dyReturn

    # Round dx, dy, because the 'getPerspectiveTransform()' function modify them
    dx = round(dx, ndigits=2); dy = round(dy, ndigits=2)

    # If worldX and worldY have not been selected, return
    if worldX is None or worldY is None : return;

    if dx != worldX :
        # Move coordinate X
        if dx > worldX :
            dxReturn = True

        if dx < worldX :
            dxReturn = False

        if dxReturn :
            dx -= 0.01
        else :
            dx += 0.01

    if dy != worldY :
        # Move coordinate Y
        if dy > worldY :
            dyReturn = True

        if dy < worldY :
            dyReturn = False

        if dyReturn :
            dy -= 0.01
        else :
            dy += 0.01


# Main function
def play() :
    global poses

    for key,frame in withKey(stream):
        # Extract contours
        g = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        cs = extractContours(g, minarea=5, reduprec=2)

        # Get polygons of 6 sides
        good = polygons(cs,6,3)

        # Get best cameras
        poses = []
        for g in good:
            err,Me = bestPose(K,g,marker)
            if err < 2:
                poses += [Me]

        # Undo comment for draw contours
        #cv.drawContours(frame,[c.astype(int) for c in cs], -1, (255,255,0), 1, lineType)
        #cv.drawContours(frame,[c.astype(int) for c in good], -1, (0,0,255), 3, lineType)
        #cv.drawContours(frame,[htrans(M,marker).astype(int) for M in poses], -1, (0,255,255), 1, lineType)
        #cv.drawContours(frame,[htrans(M,cube).astype(int) for M in poses], -1, (0,255,0), 1, lineType)

        # for each camera:
        for p in poses:
            # Get src points of virtual image
            src = np.array([[0.,0],[0,400],[400,400],[400,0]]).astype(np.float32)
            # Get dst points of real image
            dst = htrans(p, np.array([[dx, dy, 0], [dx+1, dy, 0], [dx+1, dy, 1], [dx, dy, 1]])).astype(np.float32)
            # Get homography
            H = cv.getPerspectiveTransform(src,dst)
            # Apply homography
            cv.warpPerspective(imvirt,H,size,frame,0,cv.BORDER_TRANSPARENT)

            # Move points of image
            moveImage()

            # If worldX and worldY have been selected, draw them
            if worldX is not None and worldY is not None:
                img = htrans(p,(worldX, worldY,0))
                putPoint(image=frame, point=img)

        showCalib(K,frame)
        cv.imshow(programName,frame)


if __name__ == "__main__":
    play()
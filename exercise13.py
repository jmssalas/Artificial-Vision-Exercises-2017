#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# pip install --upgrade https://robot.inf.um.es/material/umucv.tar.gz
# python exercise13.py --dev=file:images/rot4.mjpg

# Press 'Esc' key for exit

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Crea un efecto de realidad aumentada dinámico.
##################################

import cv2          as cv
import numpy        as np

from umucv.stream   import mkStream, withKey
from umucv.htrans   import htrans, pose, kgen
from umucv.util     import lineType, cube, showCalib
from umucv.contours import extractContours, redu

programName = 'exercise13'          # Program name

escKey = 27                         # Escape key code
enterKey = 10                       # Enter key code

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

imvirt = cv.resize(cv.imread('images/thing.png'),(200,200))

stream = mkStream(args.size, args.dev)

HEIGHT, WIDTH = next(stream).shape[:2]
size = WIDTH,HEIGHT
print(size)

K = kgen(size,1.7) # fov aprox 60 degree

print(K)

marker = np.array(
       [[0,   0,   0],
        [0,   1,   0],
        [0.5, 1,   0],
        [0.5, 0.5, 0],
        [1,   0.5, 0],
        [1,   0,   0]])


def polygons(cs,n,prec=2):
    rs = [ redu(c,prec) for c in cs ]
    return [ r for r in rs if len(r) == n ]

def rots(c):
    return [np.roll(c,k,0) for k in range(len(c))]

def bestPose(K,view,model):
    poses = [ pose(K, v.astype(float), model) for v in rots(view) ]
    return sorted(poses,key=lambda p: p[0])[0]


dy = 0.0
dyReturn = False
dz = 0.0
dzReturn = False

def moveImage() :
    global dy,dz,dyReturn,dzReturn

    if dy > 1 :
        dyReturn = True

    if dy < 0 :
        dyReturn = False

    if dyReturn :
        dy -= 0.01
    else :
        dy += 0.01

    if dz > 1 :
        dzReturn = True

    if dz < 0 :
        dzReturn = False

    if dzReturn :
        dz -= 0.01
    else :
        dz += 0.01


for key,frame in withKey(stream):
    g = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    cs = extractContours(g, minarea=5, reduprec=2)

    good = polygons(cs,6,3)

    poses = []
    for g in good:
        err,Me = bestPose(K,g,marker)
        if err < 2:
            poses += [Me]

    #cv.drawContours(frame,[c.astype(int) for c in cs], -1, (255,255,0), 1, lineType)

    #cv.drawContours(frame,[c.astype(int) for c in good], -1, (0,0,255), 3, lineType)

    #cv.drawContours(frame,[htrans(M,marker).astype(int) for M in poses], -1, (0,255,255), 1, lineType)

    #cv.drawContours(frame,[htrans(M,cube).astype(int) for M in poses], -1, (0,255,0), 1, lineType)

    for p in poses:
        src = np.array([[0.,0],[0,200],[200,200],[200,0]]).astype(np.float32)

        dst = htrans(p, np.array([[0, dy, 0], [1, dy, 0], [1, dy, dz], [0, dy, dz]])).astype(np.float32)
        H = cv.getPerspectiveTransform(src,dst) #(es la homografía plana)
        cv.warpPerspective(imvirt,H,size,frame,0,cv.BORDER_TRANSPARENT)

    showCalib(K,frame)
    cv.imshow('source',frame)

    moveImage()
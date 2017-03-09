#!/usr/bin/env python

# Code on Github repository: git@github.com:jmssalas/Artificial-Vision-Exercises-2017.git

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Construye un servidor web sencillo usando flask que muestre
## una cierta transformación de las imágenes tomadas con la cámara. Apóyate en server.py.
##################################

#  $ ./server.py
#  On browser:  http://localhost:5000/

import numpy            as np
import cv2              as cv
from flask              import Flask, abort, send_file
from PIL                import Image, ImageDraw
from io                 import BytesIO

programName = 'exercise05'

cap = cv.VideoCapture(0)
assert cap.isOpened()

def getframe():
    ret, frame = cap.read()
    return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

# Sobel Mask
def grad(x):
    gx =  cv.Sobel(x,-1,1,0)
    gy = -cv.Sobel(x,-1,0,1)
    return gx,gy


app = Flask(__name__)

@app.route('/')
def transformImage():
    g = getframe()

    gaussianBlur = cv.GaussianBlur(g, (0,0), 3)
    medianBlur = cv.medianBlur(g, 17)
    sobelx,sobely = grad(gaussianBlur)


    row1 = np.hstack([gaussianBlur, medianBlur])
    row2 = np.hstack([sobelx, sobely])

    allImages = np.vstack([row1, row2])

    image = Image.fromarray(allImages, mode='RGB')

    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=False)  # debug=True parece incompatible con V4L2 !?
#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Construye un servidor web sencillo usando flask que muestre
## una cierta transformación de las imágenes tomadas con la cámara.
##################################

# $ ./exercise05.py
# On browser:
# For gaussian blurring -> http://localhost:5000/transforms/gaussianBlur/<blurringFactor>
# For convert to black&white -> http://localhost:5000/transforms/convertToBW
# For threshold -> http://localhost:5000/transforms/threshold/<threshold>
# For edges -> http://localhost:5000/transforms/edges/<thresholds> when thresholds='thresh1xthresh2' and thresh1 < thresh2

import re
import numpy            as np
import cv2              as cv
from flask              import Flask, abort, send_file
from PIL                import Image
from io                 import BytesIO

programName = 'exercise05'

cap = cv.VideoCapture(0)
assert cap.isOpened()


# Get current frame converted to RGB
def getframe():
    ret, frame = cap.read()
    return cv.cvtColor(frame, cv.COLOR_BGR2RGB)


# Send 'image' param to browser
def sendImage(image, mode='RGB'):
    img = Image.fromarray(image, mode=mode)

    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')


app = Flask(__name__)

@app.route('/transforms/gaussianBlur/<blurringFactor>')
def gaussianBlur(blurringFactor):
    try:
        sigma = int(blurringFactor)
    except:
        abort(400)

    g = getframe()

    return sendImage(cv.GaussianBlur(g, (0, 0), sigma))


@app.route('/transforms/convertToBW')
def convertToBW():
    g = getframe()

    return sendImage(cv.cvtColor(g, cv.COLOR_RGB2GRAY), mode='L')


@app.route('/transforms/threshold/<threshold>')
def threshold(threshold):
    try:
        thresh = int(threshold)
    except:
        abort(400)

    g = getframe()

    return sendImage(cv.threshold(g, thresh, maxval=255, type=cv.THRESH_BINARY))


@app.route('/transforms/edges/<thresholds>')
def edges(thresholds):
    # Extract digits from request variable, when 'thresh1xthresh2' and thresh1 < thresh2
    try:
        [threshMin, threshMax] = [int(s) for s in re.findall(r'\d+', thresholds)]
        # Check if range of thresholds is correct
        if threshMin >= threshMax :
            abort(400)
    except:
        abort(400)

    g = getframe()

    return sendImage(cv.Canny(g.astype(np.uint8), threshold1=threshMin, threshold2=threshMax), mode='L')


if __name__ == '__main__':
    app.run(debug=False)  # debug=True parece incompatible con V4L2 !?
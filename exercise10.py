#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit
# Press 'Enter' key for process ROI
# For folder with images mode: press 'n' key for next image
#
# Execute: ./exercise10.py [-h] [-d DEV] templates labels
# where:
#   - templates is an image which contains the template models
#   - labels is a string with labels of template models
# options:
#   - [-h] for help
#   - [-d DEV] for indicate device of program: folder with images or webcam device (default: webcam 0)

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Reconocimiento de formas con la webcam (o sobre un conjunto de imágenes)
## basado en descriptores frecuenciales.
##################################

import numpy             as np
import numpy.fft         as fft
import cv2               as cv
import argparse

from    os.path          import isfile, isdir
from    umucv.stream     import mkStream

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('templates', help='Image which contains the template models')
parser.add_argument('labels', help='Labels of template models')
parser.add_argument('-d', '--dev', type=str, help='Device of program: folder with images or webcam device')
parser.print_help()
args = parser.parse_args()

# Check if 'templates' param is not a file. If it's not file, then exit
if not isfile(args.templates) :
    print('Error: {} is not a file'.format(args.templates))
    exit(-1)


stream = None       # Stream of images
isWebCam = True     # Indicate if stream is a webcam or images collection

# Check if -d option has been put and is not numeric -> Folder with images selected
if args.dev and not args.dev.isnumeric():
    # Check if it is a folder
    if not isdir(args.dev):
        print('Error: {} is not a dir'.format(args.dev))
        exit(-1)

    # Create stream
    stream = mkStream(dev='glob:'+args.dev+'*')
    # Set isWebCan to False
    isWebCam = False
elif args.dev: # If it is numeric -> device selected

    stream = mkStream(dev=args.dev)
else: # If it has not been put, default : device 0
    stream = mkStream(dev='0')

programName = 'exercise10'   # Program name

# Key's code
escKey          = 27        # Escape key code
enterKey        = 10        # Enter key code
nextFrame       = ord('n')  # Next frame code

drawing, lButtonUp = False, False   # - 'drawing' indicates that ROI rectangle is drawing
                                    # - 'lButtonUp' indicates that when left button up event happens,
                                    #    if mouse move event happens, then ROI rectangle doesn't change.

initialPosition = -1                        # Initial position

x0, y0 = initialPosition, initialPosition   # ROI's Initial position
xf, yf = initialPosition, initialPosition   # ROI's Final position

# Mouse event handler
def mouseEventHandler(event, x, y, flags, param):
    global x0, y0, xf, yf, drawing, lButtonUp

    if event == cv.EVENT_LBUTTONDOWN:  # Indicate init ROI rectangle
        drawing = True
        lButtonUp = False
        x0, y0 = x, y
        xf, yf = x0, y0

    elif event == cv.EVENT_MOUSEMOVE:  # Indicate changes of ROI rectangles
        if drawing and not lButtonUp:
            xf, yf = x, y

    elif event == cv.EVENT_LBUTTONUP:  # Indicate final ROI rectangle
        if drawing:
            xf, yf = x, y
            # Check ROI's points sign
            if yf < y0:
                aux = y0; y0 = yf; yf = aux

            if xf < x0:
                aux = x0; x0 = xf; xf = aux

            lButtonUp = True

# Set window's name
cv.namedWindow(programName)
# Set mouseCallback to mouseEventHandler
cv.setMouseCallback(programName, mouseEventHandler)

# Function which draw ROI selected above 'frame' param with
# first vertex 'p0' and second vertex 'p1' and color 'color' param
def drawROI(frame, p0, pf, color):
    cv.rectangle(frame, p0, pf, color)



# Utils functions
def orientation(x):
    return cv.contourArea(x.astype(np.float32),oriented=True) >= 0

def fixOrientation(x):
    if orientation(x):
        return x
    else:
        return np.flipud(x)

# Extract contours of 'g' image
def extractContours(g, minlen=50, holes=False):
    if holes:
        mode = cv.RETR_CCOMP
    else:
        mode = cv.RETR_EXTERNAL
    gt = cv.adaptiveThreshold(g,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,101,-10)
    a,contours,b = cv.findContours(gt.copy(), mode ,cv.CHAIN_APPROX_NONE)
    ok = [fixOrientation(c.reshape(len(c),2)) for c in contours if cv.arcLength(c,closed=True) >= minlen]
    return ok


def readbgr(file):
    return cv.imread(file)

def bgr2gray(x):
    return cv.cvtColor(x,cv.COLOR_BGR2GRAY)

# Frequency invariant
def invar(c, wmax=10):
    z = c[:, 0] + c[:, 1] * 1j  # Convert 'c' to complex
    f = fft.fft(z)              # Calculate FFT

    fa = abs(f)                 # Get absolute value for get rotation and initial point invariant

    s = fa[1] + fa[-1]
    fp = fa[2:wmax + 2]
    fn = np.flipud(fa)[1:wmax + 1]
    return np.hstack([fp, fn]) / s

# Function which compares a vector 'c' with models 'mods' and returns sorted distances
# and corresponded label
def mindist(c,mods,labs):
    import numpy.linalg as la
    ds = [(la.norm(c-mods[m]),labs[m]) for m in range(len(mods)) ]
    return sorted(ds, key=lambda x: x[0])

# Get input key
def getInputKey():
    return cv.waitKey(1) & 0xFF


# Load models and calculate invariant features of models
# Return (models, feats)
def loadModels(image):
    # Convert to gray and invert image
    g = 255-bgr2gray(readbgr(image))

    # Models -> Sort the letters for X coordinate
    models = sorted(extractContours(g), key=lambda x: x[0,0])

    # Invariant features of all models
    feats = [invar(m) for m in models]

    return models, feats


# Function which processes current 'frame' searching matches with 'models' and show the licence plat number with 'labels'
def processFrame(frame, models, labels, feats):
    # Convert to gray and invert image
    g = 255 - bgr2gray(x=frame)

    cv.imshow('roi', g)

    # Extract contours sorted by X coordinate
    things = sorted(extractContours(g, holes=True), key=lambda x: x[0,0])

    print('The result is: ')
    for x in things:
        d, l = mindist(invar(x), feats, labels)[0]
        if d < 0.10:
            print(l, end='')

    print('\n')


# Function which execute webCamMode
def webCamMode(models, labels, feats):
    global lButtonUp, drawing, x0, xf, y0, yf

    for frame in stream:
        # Get input key
        key = getInputKey()

        # Process input key
        if key == escKey: break

        # Press 'Enter' key for process current frame
        if key == enterKey:
            if x0 != initialPosition and xf != initialPosition and y0 != initialPosition and yf != initialPosition:
                # Restart values of mouse's events
                lButtonUp = False
                drawing = False

                # Select ROI
                roi = np.copy(frame[y0:yf + 1, x0:xf + 1])
                # Process frame
                processFrame(frame=roi, models=models, labels=labels, feats=feats)

                # Delete ROI selection
                x0, y0, xf, yf = initialPosition, initialPosition, initialPosition, initialPosition

        # Draw ROI
        drawROI(frame=frame, p0=(x0, y0), pf=(xf, yf), color=(0, 255, 0))

        # Show frame
        cv.imshow(programName, frame)


# Function which execute imageMode
def imageMode(models, labels, feats):

    for frame in stream:
        # Process frame
        processFrame(frame=frame, models=models, labels=labels, feats=feats)

        while True:
            key = getInputKey()

            if key == nextFrame or key == escKey: break;

            # Show frame
            cv.imshow(programName, frame)

        if key == escKey: break;

def play():

    # Labels and templates
    labels = args.labels
    templates = args.templates

    # Load models and its invariant features
    models, feats = loadModels(image=templates)

    if isWebCam :
        webCamMode(models, labels, feats)
    else:
        imageMode(models, labels, feats)


if __name__ == "__main__":
    play()
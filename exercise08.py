#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit
# Press 'a' key for add and subtract filter
# Press 'b' key for multiplication and division filter
# Press 'c' key for shift filter
# Press 'd' key for horizontal edges filter
# Press 'e' key for vertical edges filter
# Press 'f' key for mean blurring filter
# Press 'g' key for gaussian blurring filter

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Mostrar el efecto de diferentes filtros de imagen sobre la imagen en vivo
## de la webcam, seleccionando con el teclado el filtro deseado y permitiendo
## modificar sus posibles parámetros (p.ej. el nivel de suavizado) con
## las teclas de flecha.
##################################

import numpy             as np
import cv2               as cv
import scipy.signal      as signal

programName = 'exercise08'

# Key's code
escKey          = 27    # Escape key code
enterKey        = 10    # Enter key code
upKey           = 82    # Up arrow key code
downKey         = 84    # Down arroy key code

# Filters
Add_Sub         = 0     # Add and Subtract filter
Mul_Div         = 1     # Multiplication and division filter
Shift           = 2     # Shift filter
HorizontalEdges = 3     # Horizontal edges filter
VerticalEdges   = 4     # Vertical edges filter
MeanBlurring    = 5     # Mean blurring filter
GaussianBlur    = 6     # Gaussian blurring filter

# Filters which uses convolution matrix
convolutionFilters = [Add_Sub, Mul_Div, Shift, HorizontalEdges, VerticalEdges, MeanBlurring]

# Filters codes
filtersCodes = {Add_Sub: ord('a'), Mul_Div: ord('b'), Shift: ord('c'), HorizontalEdges: ord('d'),
                VerticalEdges: ord('e'), MeanBlurring: ord('f'), GaussianBlur: ord('g')}

# Initial values of filters
initialValues = {Add_Sub: 1, Mul_Div: 2, Shift: 11, HorizontalEdges: 1, VerticalEdges: 1, MeanBlurring: 11,
                 GaussianBlur: 1}

# Current values of filters
currentValues = initialValues.copy()

# It indicates if filter has been used for first time
firstTime = {Add_Sub: True, Mul_Div: True, Shift: True, HorizontalEdges: True, VerticalEdges: True,
             MeanBlurring: True, GaussianBlur: True}

# Filters steps
filtersSteps = {Add_Sub: 0.2, Mul_Div: 0.2, Shift: 1, HorizontalEdges: 1, VerticalEdges: 1, MeanBlurring: 1,
                GaussianBlur: 1}

roi = None                          # ROI selected
roiHistogram = None                 # ROI's histogram
maxDiff = 0.2                       # Max difference between ROI selected and current frame

drawing, lButtonUp = False, False   # - 'drawing' indicates that ROI rectangle is drawing
                                    # - 'lButtonUp' indicates that when left button up event happens,
                                    #    if mouse move event happens, then ROI rectangle doesn't change.

x0, y0 = -1, -1                     # ROI's Initial position
xf, yf = -1, -1                     # ROI's Final position


# Get current frame converted to RGB
def getFrame(cap):
    ret, frame = cap.read()
    return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

# Convert RGB to BGR
def rgb2bgr(x):
    return cv.cvtColor(x, cv.COLOR_RGB2BGR)

# Convert RGB to GRAY
def rgb2gray(x):
    return cv.cvtColor(x,cv.COLOR_RGB2GRAY)

# Convert int GRAY to float GRAY
def gray2float(x):
    return x.astype(float) / 255

# Put 'text' param above 'image' param in the (x,y) position
def putText(image, text, x, y):
    cv.putText(img=image, text=text, org=(x, y), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=1, color=255)  # Draw the text

# Function which apply 'k' convolution matrix to 'x' params
def applyConvolutionMatrix(k, x):
    return signal.convolve2d(x[:,:], k, boundary='symm', mode='same')

# Get input key
def getInputKey():
    return cv.waitKey(1) & 0xFF

# Check if it is first time for set value
def checkFirstTime(filter):
    if firstTime[filter]: return initialValues[filter]
    return currentValues[filter]

# Get current framen converted to gray
def getFrameConvertedToGray(cap):
    # Get frame
    frame = getFrame(cap=cap)
    # Convert to float GRAY
    return gray2float(rgb2gray(frame))


# Modify 'value' param depending on 'key' param:
#  - if it is 'upKey', will add 'step' to 'value'.
#  - if it is 'downKey', will subtract 'step' to 'value'.
#  - else will do nothing.
def processUpDownKeys(key, value, step=1.0):
    if key == upKey : return value + step
    if key == downKey: return value - step
    return value


# Apply 'ker' convolution matrix to 'img' and show result
def applyConvMatrixAndShowResult(ker, img, value):
    # Apply convolution matrix
    filteredFrame = applyConvolutionMatrix(ker, img)
    # Put text
    putText(image=filteredFrame, text='value = ' + str(value), x=2, y=15)
    # Show filtered frame
    cv.imshow(programName, filteredFrame)


# Get convolution matrix of 'filter' filter with 'ancle' ancle
def getConvolutionMatrix(filter, ancle):
    anc = ancle
    if filter == Add_Sub :
        ker = np.array([[0, 0, 0]
                           , [0, 1 + anc, 0]
                           , [0, 0, 0]])

    elif filter == Mul_Div :
        ker = np.array([[0, 0, 0]
                           , [0, anc, 0]
                           , [0, 0, 0]])

    elif filter == Shift :
        if anc < 3: anc = 3
        ker = np.zeros([anc, anc])
        ker[0, 0] = 1
        ker[anc - 1, anc - 1] = 1
        ker = ker / np.sum(ker)

    elif filter == HorizontalEdges :
        ker = np.array([[0, 0, 0]
                          , [-anc, 0, anc]
                          , [0, 0, 0]])

    elif filter == VerticalEdges :
        ker = np.array([[0, -anc, 0]
                          , [0, 0, 0]
                          , [0, anc, 0]])

    elif filter == MeanBlurring :
        if anc < 3: anc = 3
        ker = np.ones([anc, anc])
        ker = ker / np.sum(ker)

    else: # Default, do nothing
        anc = 1
        ker = np.array([[0, 0, 0]
                           , [0, anc, 0]
                           , [0, 0, 0]])

    return ker, anc


# Apply 'filter' filter to 'img' image with 'value' value
def applyFilterAndShowResult(filter, img, value):
    if filter == GaussianBlur :
        if value < 1 : val = 1
        else : val = value
        filteredFrame = cv.GaussianBlur(img, (0,0), val)
        text = 'sigma = ' + str(val)

    else :
        filteredFrame = img
        text = 'value = ' + str(value)

    # Put text
    putText(image=filteredFrame, text=text, x=2, y=15)
    # Show filtered frame
    cv.imshow(programName, filteredFrame)


# Apply 'filter' filter to captured frames of 'cap'
def applyFilter(cap, filter):
    global currentValues

    # Check if it is first time for set value
    value = checkFirstTime(filter=filter)

    # Set first time to false
    firstTime[filter] = False

    # Get input key
    key = getInputKey()
    while key != escKey :

        # Convert frame to float gray
        fframe = getFrameConvertedToGray(cap=cap)

        # Process input key
        ancle = processUpDownKeys(key, value, step=filtersSteps[filter])

        # Check if 'filter' is a filter which uses convolution matrix
        if filter in convolutionFilters :
            # Convolution matrix
            ker, ancle = getConvolutionMatrix(filter=filter, ancle=ancle)

            # Apply convolution matrix and show result
            applyConvMatrixAndShowResult(ker=ker, img=fframe, value=ancle)

        else :
            applyFilterAndShowResult(filter=filter, img=fframe, value=ancle)


        # Update values
        currentValues[filter], value = ancle, ancle

        # Get input key
        key = getInputKey()

    # Set first time to true
    firstTime[filter] = True


# Main function.
# Default -> dev = 0
def play(dev=0):
    global firstTime

    cap = cv.VideoCapture(dev)

    while True:

        # Get input key
        key = getInputKey()

        # Process input key
        if key == escKey: break

        if key == filtersCodes[Add_Sub] :
            applyFilter(cap=cap, filter=Add_Sub)

        if key == filtersCodes[Mul_Div] :
            applyFilter(cap=cap, filter=Mul_Div)

        if key == filtersCodes[Shift] :
            applyFilter(cap=cap, filter=Shift)

        if key == filtersCodes[HorizontalEdges] :
            applyFilter(cap=cap, filter=HorizontalEdges)

        if key == filtersCodes[VerticalEdges] :
            applyFilter(cap=cap, filter=VerticalEdges)

        if key == filtersCodes[MeanBlurring] :
            applyFilter(cap=cap, filter=MeanBlurring)

        if key == filtersCodes[GaussianBlur] :
            applyFilter(cap=cap, filter=GaussianBlur)

        # Get frame
        frame = getFrame(cap=cap)
        cv.imshow(programName, rgb2bgr(frame))


if __name__ == "__main__":
    play()
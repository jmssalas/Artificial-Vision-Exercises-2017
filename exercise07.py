#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Implementa la segmentación por color usando modelos de histograma
## en un programa que admite como argumento:
##   a) una carpeta con trozos de imagen que sirven como muestras de color y
##   b) otra imagen que deseamos clasificar.
## El resultado puede ser un conjunto de máscaras para cada clase,
## o una "imagen de etiquetas", donde diferentes colores indican cada una de las regiones.
##################################

import numpy             as np
import cv2               as cv
import argparse
from    os               import listdir
from    os.path          import isfile, join, isdir


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('models', help='Folder which contains the color models')
parser.add_argument('image', help="Image's file")
args = parser.parse_args()

# Check if 'models' param is not a folder. If it's not folder, then exit
if not isdir(args.models) :
    print('Error: {} is not a folder'.format(args.models))
    exit(-1)

# Check if 'file' param is not a file. If it's not file, then exit
if not isfile(join(args.image)):
    print('Error: {} is not a file'.format(args.image))
    exit(-2)


programName = 'exercise07'  # Program name

minimumDistance = 200       # Minimum distance that a pixel should have to be show with its color model

# Key's code
escKey          = 27        # Escape key code
enterKey        = 10        # Enter key code


# Get input key
def getInputKey():
    return cv.waitKey(1) & 0xFF

# Read file in RGB color
def readrgb(file):
    return cv.cvtColor( cv.imread(file), cv.COLOR_BGR2RGB)

# Show 'img' image with window's name 'name' in RGB
def imshowRGB(name, img):
    cv.imshow(name, cv.cvtColor(img, cv.COLOR_RGB2BGR))

# Function which return the files into 'folder' param
def getFilesOfFolder(folder):
    return [f for f in listdir(folder) if isfile(join(folder, f))]

# Function which return the models of 'files' files. This models are chosen like mean of its color.
def getModelsOfFiles(folder, files):
    return [ np.mean(f,(0,1)) for f in [ readrgb(join(folder,img)) for img in files ] ]

# Get absolute differences between image 'img' and models 'models'
def getAbsoluteDifferences(img, models):
    return [ np.sum(abs(img - m), axis=2) for m in models ]

# Get closer model of the distances 'distances' param
def getCloserModel(distances):
    return np.argmin(distances, axis=0)

# Filter pixels which don't belong to any models
def filterPixels(img, distances):
    minDistance = np.min(distances, axis=0)
    img[minDistance > minimumDistance] = 0, 0, 0
    return img

# Convert 'img' image's pixels with the closer model into 'models' models
def convertImage(img, models):
    # Get absolute differences between 'img' image and 'models' models
    distances = getAbsoluteDifferences(img=img, models=models)
    # Get closer model with 'distances' distances
    model = getCloserModel(distances=distances)

    # Prepare result image
    res = np.zeros(img.shape, dtype=np.uint8)

    # Fill result
    for k in range(len(models)):
        res[model==k] = models[k]

    # Return result filtered
    return filterPixels(img=res, distances=distances)

# Main function.
# Default -> dev = 0
def play():

    print('-> Load models into {} folder...'.format(args.models))
    files = getFilesOfFolder(folder=args.models)
    models = getModelsOfFiles(folder=args.models, files=files)
    print('-> Models loaded')

    print('-> Convert {} image'.format(args.image))
    image = readrgb(args.image)
    convertedImage = convertImage(img=image, models=models)
    print('-> Image {} converted'.format(args.image))

    while True :
        # Get input key
        key = getInputKey()

        # Process input key
        if key == escKey: break

        imshowRGB('original', image)
        cv.imshow('converted', convertedImage)



if __name__ == "__main__":
    play()
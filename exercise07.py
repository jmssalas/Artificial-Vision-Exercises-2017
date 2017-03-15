#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

# Press 'Esc' key for exit

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Implementar la segmentación por color en un programa que
## admite como argumento a) una carpeta con trozos de imagen
## que sirven como muestras de color y b) otra imagen o
## secuencia de video que deseamos clasificar.
##################################

import numpy             as np
import cv2               as cv

programName = 'exercise07'

escKey = 27                         # Escape key code

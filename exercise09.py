#!/usr/bin/env python

# Code on Github repository: https://github.com/jmssalas/Artificial-Vision-Exercises-2017

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Reconocimiento de objetos con la webcam basado en el número de
## coincidencias de keypoints. Pulsando una tecla se pueden ir
## guardando modelos (p. ej. carátulas de CD). Cuando detectamos
## que la imagen está bastante quieta, o cuando se pulse otra tecla,
## calculamos los puntos de interés de la imagen actual y sus
## descriptores y vemos si hay suficientes coincidencias con los de algún modelo.
##################################

import numpy             as np
import cv2               as cv

programName = 'exercise09'
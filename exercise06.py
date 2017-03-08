#!/usr/bin/env python

# Code on Github repository: git@github.com:jmssalas/Artificial-Vision-Exercises-2017.git

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Implementar el efecto chroma con imágenes en vivo de la webcam.
## Pulsando una tecla se captura el fondo y los objetos que aparezcan
## se superponen en otra imagen o secuencia de video. Comparar con backsub.py.
##################################

import numpy             as np
import cv2               as cv

programName = 'exercise06'
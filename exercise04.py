#!/usr/bin/env python

# Code on Github repository: git@github.com:jmssalas/Artificial-Vision-Exercises-2017.git

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Construye un generador que detecte frames estáticos,
## o frames en movimiento, a partir de una secuencia de imágenes. Apóyate en deque.py.
##################################

import numpy             as np
import cv2               as cv

programName = 'exercise04'
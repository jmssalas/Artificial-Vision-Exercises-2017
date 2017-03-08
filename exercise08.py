#!/usr/bin/env python

# Code on Github repository: git@github.com:jmssalas/Artificial-Vision-Exercises-2017.git

##################################
## PROBLEM STATEMENT (IN SPANISH)
## -------------------------------
##
## Mostrar el efecto de diferentes filtros de imagen sobre
## la imagen en vivo de la webcam, seleccionando con el
## teclado el filtro deseado y permitiendo modificar sus
## posibles parámetros (p.ej. el nivel de suavizado) con
## las teclas de flecha. Puede ser interesante permitir
## la selección de un ROI dentro de la imagen y mostrar
## el efecto del filtro en ese mismo ROI para comparar el
## resultado con el resto de la imagen.
##################################

import numpy             as np
import cv2               as cv

programName = 'exercise08'
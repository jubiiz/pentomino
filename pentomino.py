import os
import cv2
import numpy as np
from processor import *
from sides import *
from numext import *

class Cell():
    def __init__(self, value, coordinates, sides):
        self.value = value
        self.coordinates = coordinates
        self.sides = sides

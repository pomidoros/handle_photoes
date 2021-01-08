import numpy as np
from skimage.io import imread, imshow, imsave
from skimage import img_as_float, img_as_ubyte
from matplotlib import pyplot as plt
import os


PROSKURIN_DIRECTORY = "proskurin_photo"
ORIGINAL_PATH = "original"
FINITE_PATH = "finite"
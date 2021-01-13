from settings import *


def make_channels(ph):
    r = img_as_float(ph[:, :, 0])
    g = img_as_float(ph[:, :, 1])
    b = img_as_float(ph[:, :, 2])
    return [r, g, b]
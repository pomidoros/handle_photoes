from settings import *
from random import choice
from test_paths import find_color_photo
from common_functions.general_useful_funcs import make_channels


def lite_handle(chnls):
    return img_as_ubyte((chnls[0] + chnls[1] + chnls[2]) / 3)


def advanced_handle(chnls):
    return img_as_ubyte(0.2126 * chnls[0] + 0.7152 * chnls[1] + 0.0722 * chnls[2])


def from_color_to_grey(img, ver="adv"):
    list_of_channels = make_channels(img)
    if ver == "lite":
        handled_image = lite_handle(list_of_channels)
    elif ver == "adv":
        handled_image = advanced_handle(list_of_channels)

    return handled_image


def convert(path=None, version="lite"):
    if path is None:
        paths = find_color_photo()
        chosen_path = choice(paths)
    else:
        chosen_path = path

    image = imread(chosen_path)
    result_image = from_color_to_grey(image, version)

    return result_image


if __name__ == "__main__":
    img = convert(version="adv")
    imshow(img)
    plt.show()

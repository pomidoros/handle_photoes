from settings import *
from random import choice
import re

orig_dir = ORIGINAL_PATH


def find_color_photo():
    list_of_photos = os.listdir(orig_dir)
    handled_list = []
    for cur in list_of_photos:
        new_add = re.findall('\w+_color.png', cur)
        if new_add is not None:
            handled_list.extend(new_add)
    return handled_list


def lite_handle(chnls):
    return img_as_ubyte((chnls[0] + chnls[1] + chnls[2]) / 3)


def advanced_handle(chnls):
    return img_as_ubyte(0.21 * chnls[0] + 0.71 * chnls[1] + 0.08 * chnls[2])


def make_channels(ph):
    r = img_as_float(ph[:, :, 0])
    g = img_as_float(ph[:, :, 1])
    b = img_as_float(ph[:, :, 2])
    return [r, g, b]


def convert(com="test", ver="lite"):
    if com == "test":
        paths = find_color_photo()
        chosen_path = choice(paths)
    else:
        chosen_path = com
    chosen_path = orig_dir + "/" + chosen_path
    img = imread(chosen_path)
    list_of_channels = make_channels(img)
    if ver == "lite":
        result_image = lite_handle(list_of_channels)
    elif ver == "adv":
        result_image = advanced_handle(list_of_channels)

    return result_image


if __name__ == "__main__":
    img = convert(ver="adv")
    imshow(img)
    plt.show()

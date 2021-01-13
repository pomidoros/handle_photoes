from settings import *
from test_paths import COLOR_LOW_CONTRAST_PATH, COLOR_LOW_CONTRAST_PATH_SAVE
import color_to_grey as ctg


# минимальное и максимальное значения для повышения контраста
def find_min_max(im):
    pixels_list = sorted(im.ravel())
    pix_len = len(pixels_list)
    percent = 0.05
    shorten_len = int(percent * pix_len)
    minim = pixels_list[shorten_len]
    maxim = pixels_list[pix_len - shorten_len - 1]
    return minim, maxim


# преобразование контраста для черно-белых фото
def stable_auto_contrast_grey(im):
    im = im.astype("float")
    key_params = find_min_max(im)
    diff = key_params[1] - key_params[0]
    result_image = np.clip((im - key_params[0]) * 255 / diff, 0, 255)
    result_image = result_image.astype("uint8")
    return result_image


def from_yuv_to_rgb(comps):
    r = img_as_ubyte(np.clip(comps[0] + 1.2803 * comps[2], 0, 1.0))
    g = img_as_ubyte(np.clip(comps[0] - 0.2148 * comps[1] - 0.3805 * comps[2], 0, 1.0))
    b = img_as_ubyte(np.clip(comps[0] + 2.1279 * comps[1], 0, 1.0))
    return np.dstack((r, g, b))


# преобразование контраста для цветных фотографий
def stable_auto_contrast_color(path):
    img = imread(path)
    yuv = from_rgb_to_yuv(img)
    result_img = from_yuv_to_rgb(yuv)
    return result_img


def find_y_component(img):
    # получаем компоненту яркости
    y = ctg.from_color_to_grey(img)
    # увеличиваем её контраст
    y = stable_auto_contrast_grey(y)
    # преобразуем её в вещественную
    y = img_as_float(y)
    return y


def find_u_component(chnls):
    comp = -0.0999 * chnls[0] - 0.3360 * chnls[1] + 0.4360 * chnls[2]
    return comp


def find_v_component(chnls):
    comp = 0.6150 * chnls[0] - 0.5586 * chnls[1] - 0.0563 * chnls[2]
    return comp


def from_rgb_to_yuv(img):
    img = img_as_float(img)
    y_comp = find_y_component(img)
    channels = ctg.make_channels(img)
    u_comp = find_u_component(channels)
    v_comp = find_v_component(channels)
    return [y_comp, u_comp, v_comp]



if __name__ == "__main__":
    path = COLOR_LOW_CONTRAST_PATH
    result = stable_auto_contrast_color(path)
    imsave(COLOR_LOW_CONTRAST_PATH_SAVE, result)
    imshow(result)
    plt.show()


# handled_image = stable_auto_contrast_grey(img)
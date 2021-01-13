from settings import *
from test_paths import COLOR_LOW_CONTRAST_PATH, COLOR_LOW_CONTRAST_PATH_SAVE
from images_handle import color_to_grey as ctg
from common_functions.general_useful_funcs import make_channels


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
    # eсли в функцию поступает не массив, а путь к файлу
    if issubclass(im, str):
        im = imread(im)
    im = im.astype("float")
    # получаем минимальное и максимальное значения для стабильного автоконтраста
    key_params = find_min_max(im)
    # разница межд максимальным и минимальным
    diff = key_params[1] - key_params[0]

    result_image = np.clip((im - key_params[0]) * 255 / diff, 0, 255).astype("uint8")
    return result_image


# переводим по формулам YUV в RGB
def from_yuv_to_rgb(comps):
    r = img_as_ubyte(np.clip(comps[0] + 1.2803 * comps[2], 0, 1.0))
    g = img_as_ubyte(np.clip(comps[0] - 0.2148 * comps[1] - 0.3805 * comps[2], 0, 1.0))
    b = img_as_ubyte(np.clip(comps[0] + 2.1279 * comps[1], 0, 1.0))
    return np.dstack((r, g, b))


# преобразование контраста для цветных фотографий
def stable_auto_contrast_color(path):
    img = imread(path)
    yuv_format = from_rgb_to_yuv(img)
    result_img = from_yuv_to_rgb(yuv_format)
    return result_img


def y_component(img):
    # получаем компоненту яркости
    y = ctg.from_color_to_grey(img)
    # увеличиваем её контраст
    y = stable_auto_contrast_grey(y)
    # преобразуем её в вещественную
    y = img_as_float(y)
    return y


def u_component(chnls):
    comp = -0.0999 * chnls[0] - 0.3360 * chnls[1] + 0.4360 * chnls[2]
    return comp


def v_component(chnls):
    comp = 0.6150 * chnls[0] - 0.5586 * chnls[1] - 0.0563 * chnls[2]
    return comp


# переводим изображение в формат YUV для корректировки яркости
def from_rgb_to_yuv(img):
    img = img_as_float(img)
    # получаем каналы
    channels = make_channels(img)

    # получаем каналы Y, U и V
    y_comp = y_component(img)
    u_comp = u_component(channels)
    v_comp = v_component(channels)
    return [y_comp, u_comp, v_comp]


if __name__ == "__main__":
    path = COLOR_LOW_CONTRAST_PATH
    result = stable_auto_contrast_color(path)
    imsave(COLOR_LOW_CONTRAST_PATH_SAVE, result)
    imshow(result)
    plt.show()


# handled_image = stable_auto_contrast_grey(img)
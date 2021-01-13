from settings import *
from test_paths import proskurin_files
from random import choice
import math
import warnings

# игнорирование предупреждений
warnings.simplefilter("ignore")


# обрезание фотографии
def cut_photo_frame(fr):
    percent = 0.1
    w_clipped = math.floor(fr.shape[1] * percent)
    h_clipped = math.floor(fr.shape[0] * percent)
    return fr[h_clipped:fr.shape[0] - h_clipped, w_clipped:fr.shape[1] - w_clipped]


# обрезание массива
def cut_frames(frs):
    for i in range(len(frs)):
        frs[i] = cut_photo_frame(frs[i])
    return frs


# смещение слоя fr1 относительно слоя fr2
def imposition_coord(fr1, fr2):
    x = 0
    y = 0
    list_of_coords = []
    corr = -1
    for j in range(-15, 16):
        bias_y = np.roll(fr1, j, axis=0)
        for i in range(-15, 16):
            bias_x = np.roll(bias_y, i, axis=1)
            cur_corr = (bias_x * fr2).sum()
            if corr < cur_corr:
                corr = cur_corr
                x = i
                y = j
    return (x, y)


# нахождение всех смещений
def imposition_coords(frs):
    # список смещений (в наборах точек)
    list_of_biases = []
    # смещение канала B относительно G
    b_rel_g = imposition_coord(frs[0], frs[1])
    list_of_biases.append(b_rel_g)
    # смещение канала R относительно G
    r_rel_g = imposition_coord(frs[2], frs[1])
    list_of_biases.append(r_rel_g)

    return list_of_biases


# конструируем смещённые фреймы
def imposition(frs, coords):
    b = np.roll(frs[0], coords[0][1], axis=0)
    b = np.roll(b, coords[0][0], axis=1)
    r = np.roll(frs[2], coords[1][1], axis=0)
    r = np.roll(r, coords[1][0], axis=1)
    return [b, frs[1], r]


# вывод фреймов
def print_frames(frs):
    for fr in frs:
        fr = img_as_ubyte(fr)
        imshow(fr)
        plt.show()


# обработка фотографии
def proskurin_photo_handle(path):
    # чтение изображения
    image_arr = imread(path)

    # находим высоту каждого блока
    h = image_arr.shape[0] // 3

    # получаем каналы (которые явяются кадрами)
    b = image_arr[0:h-1, :]
    g = image_arr[h:2*h-1, :]
    r = image_arr[2*h: 3*h-1, :]

    # обрезаем каналы (кадры)
    frames = cut_frames([b, g, r])
    frames = [img_as_float(fr) for fr in frames]

    # находим смещения кадров (в виде наборов точек)
    biases = imposition_coords(frames)

    # получаем смещённые кадры
    handled_frames = imposition(frames, biases)

    # получаем готовое изображение
    result_image = img_as_ubyte(np.dstack((handled_frames[2], handled_frames[1], handled_frames[0])))

    return biases, result_image


# функция находит координаты во всех каналах, соответствующие координате из g-канала
def correspond_coords_in_proskurin_photo(img, g_coord):
    img = imread(img)
    h = img.shape[0] // 3
    # обработка фотографии
    biases = proskurin_photo_handle(img)
    g_row, g_col = g_coord
    b = (g_row - h - biases[0][1], g_col - biases[0][0])
    r = (g_row + h - biases[1][1] + (img.shape[0] % 3), g_col - biases[1][0])
    return b, r


# основная функция (является оболочкой)
def proskurin_shell(path=None):
    # если не передано изображение
    if path is None:
        # берём рандомный файл для обработки
        path = choice(proskurin_files())
    # нужные смещения
    result_photo, result_coords = proskurin_photo_handle(path)
    return result_coords, result_photo


# тестирующая функция
if __name__ == "__main__":
    image, coords = proskurin_shell()
    imshow(image)
    plt.show()

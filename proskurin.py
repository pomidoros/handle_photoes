from settings import *
from test_paths import PROSKURIN_DIRECTORY
from random import choice
import math

main_directory_path = PROSKURIN_DIRECTORY


def rand_proskurin_image():
    all_paths = create_paths()
    random_path = choose_random_image(all_paths)
    return imread(random_path)


# выбор рандомного изображения для теста
def choose_random_image(paths):
    return choice(paths)


# вспомогательная функция для корректного получения путей
def create_paths():
    paths = []
    for name in sorted(os.listdir(main_directory_path)):
        paths.append(main_directory_path + "/" + name)
    return paths


# перезапись корявых названий изображений на структурированные
def rewrite_files_names():
    i = 1
    for name in os.listdir(main_directory_path):
        os.rename(main_directory_path + "/" + name, main_directory_path + "/" + str(i) + ".png")
        i += 1


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


# наложение слоёв
# исправить говно-код
def imposition_coord(frs):
    g = frs[1]
    x = 0
    y = 0
    list_of_coords = []
    corr = -1
    for j in range(-15, 16):
        b = np.roll(frs[0], j, axis=0)
        for i in range(-15, 16):
            b1 = np.roll(b, i, axis=1)
            cur_corr = (b1*g).sum()
            if corr < cur_corr:
                corr = cur_corr
                x = i
                y = j

    list_of_coords.append((x, y))

    x = 0
    y = 0
    corr = -1
    for j in range(-15, 16):
        r = np.roll(frs[2], j, axis=0)
        for i in range(-15, 16):
            r1 = np.roll(r, i, axis=1)
            cur_corr = (r1*g).sum()
            if corr < cur_corr:
                corr = cur_corr
                x = i
                y = j

    list_of_coords.append((x, y))
    return list_of_coords


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
def current_photo_handle(ph):
    frames = []
    h = ph.shape[0] // 3
    b = ph[0:h-1, :]
    g = ph[h:2*h-1, :]
    r = ph[2*h: 3*h-1, :]
    frames.extend([b, g, r])
    frames = cut_frames(frames)
    frames = [img_as_float(fr) for fr in frames]
    # находим смещения кадров
    coords = imposition_coord(frames)
    # получаем смещённые кадры
    handled_frames = imposition(frames, coords)

    return coords, img_as_ubyte(np.dstack((handled_frames[2], handled_frames[1], handled_frames[0])))


# функция находит координаты во всех каналах, соответствующие координате из g-канала
def align(img, g_coord):
    img = imread(img)
    h = img.shape[0] // 3
    print(h)
    # обработка фотографии
    biases = current_photo_handle(img)
    print(biases)
    g_row, g_col = g_coord
    b = (g_row - h - biases[0][1], g_col - biases[0][0])
    r = (g_row + h - biases[1][1] + (img.shape[0] % 3), g_col - biases[1][0])
    return b, r


# основная функция
def main_handle_of_photos(path=None):
    # если не передано изображение
    if path is None:
        # берём рандомное
        cur_photo = rand_proskurin_image()
    else:
        cur_photo = imread(path)
    # нужные смещения
    result_photo, result_coords = current_photo_handle(cur_photo)
    return result_coords, result_photo


# тестирующая функция
if __name__ == "__main__":
    image, coords = main_handle_of_photos()
    imshow(image)
    plt.show()
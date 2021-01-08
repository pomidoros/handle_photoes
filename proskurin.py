from settings import *
from random import choice
import math

main_directory_path = PROSKURIN_DIRECTORY


# чтение изображений из дирректории
def read_images(paths):
    imgs = []
    for path in paths:
        imgs.append(imread(path))
    return imgs


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


# выбор рандомного изображения для теста
def choose_random_image(paths):
    random_image = choice(paths)
    return paths.index(random_image)


# массив пикселей нужной фотографии
def test_photo(imgs, paths):
    ind = choose_random_image(paths)
    return imgs[ind]


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


# вывод изображения из наложения полученных кадров
def print_imposition(frs):
    result_image = img_as_ubyte(np.dstack((frs[2], frs[1], frs[0])))
    imshow(result_image)
    plt.show()


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
    # тестовый вывод готового кадра
    print_imposition(handled_frames)

    return coords


# основная функция
def main_handle_of_photos():
    # пути к фото
    paths_of_photos = create_paths()
    # массив изображений
    images = read_images(paths_of_photos)
    # получаем рандомное изображение
    cur_photo = test_photo(images, paths_of_photos)
    # нужные смещения
    result_coords = current_photo_handle(cur_photo)
    return result_coords


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


# print(align("proskurin_photo/5.png", (508, 237)))

# тестирующая функция
main_handle_of_photos()

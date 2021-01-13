from settings import *
from test_paths import *
from common_functions.general_useful_funcs import make_channels


def to_grey_world(path):
    # преобразуем изображение во float
    img = imread(path).astype("float")
    # получаем каналы
    channels = make_channels(img)

    # считаем средние для каналов
    mean_r = np.mean(channels[0])
    mean_g = np.mean(channels[1])
    mean_b = np.mean(channels[2])

    # считаем среднее средних
    total_mean = (mean_r + mean_g + mean_b) / 3

    # считаем коэффициенты каналов
    coeff_r = mean_r / total_mean
    coeff_g = mean_g / total_mean
    coeff_b = mean_b / total_mean

    # получаем новые каналы
    result_r = channels[0] / coeff_r
    result_g = channels[1] / coeff_g
    result_b = channels[2] / coeff_b

    # соединяем каналы
    result_img = np.dstack((result_r, result_g, result_b))

    # преобразуем в формат RGB
    result_img = np.clip(np.round(result_img), 0, 255).astype("uint8")

    return result_img


if __name__ == "__main__":
    # получаем путь к фотке
    original_path = COLOR_GREY_WORLD_PATH
    # получаем готовое изображение
    image = to_grey_world(original_path)
    # путь сохранения фотки
    save_path = COLOR_GREY_WORLD_PATH_SAVE
    # сохраняем
    imsave(save_path, image)

    # выводим изображение
    imshow(img_as_ubyte(image))
    plt.show()

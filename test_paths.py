import os
import re


# директория фотографий Проскурина
PROSKURIN_DIRECTORY = "proskurin_photo"
# директория изображений для обработки
ORIGINAL_PATH = "original"
# директория изображений для сохранения
SAVE_PATH = "finite"

COLOR_LOW_CONTRAST_PATH = ORIGINAL_PATH + "/tiger_low_contrast_color.png"
GREY_LOW_CONTRAST_PATH = ORIGINAL_PATH + "/tiger_low_contrast_grey.png"


COLOR_LOW_CONTRAST_PATH_SAVE = SAVE_PATH + "/tiger_high_contrast_color.png"
GREY_LOW_CONTRAST_PATH_SAVE = SAVE_PATH + "/tiger_high_contrast_grey.png"


COLOR_GREY_WORLD_PATH = ORIGINAL_PATH + "/not_grey_world_color.png"
COLOR_GREY_WORLD_PATH_SAVE = SAVE_PATH + "/grey_world_color.png"


# находим цветные фото
def find_color_photo():
    list_of_photos = os.listdir(ORIGINAL_PATH)
    handled_list = []
    for file in list_of_photos:
        add_file = re.findall('\w+_color.png', file)
        if add_file != []:
            handled_list.extend(add_file)
    result_list = []
    for new_add in handled_list:
        result_list.append(ORIGINAL_PATH + "/" + new_add)
    return result_list


# находим черно-белые фото
def find_grey_photo():
    list_of_photos = os.listdir(ORIGINAL_PATH)
    handled_list = []
    for cur in list_of_photos:
        new_add = re.findall('\w+_grey.png', cur)
        if new_add is not None:
            handled_list.extend(ORIGINAL_PATH + "/" + new_add)
    return handled_list


# все пути к фотография Проскурина
def proskurin_files(dir=PROSKURIN_DIRECTORY):
    paths = []
    for name in sorted(os.listdir(dir)):
        paths.append(dir + "/" + name)
    return paths

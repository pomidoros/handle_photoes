from settings import *
from test_paths import *
from colorama import Fore, Back, Style
from images_handle.color_to_grey import from_color_to_grey
from images_handle.make_contrast import stable_auto_contrast_grey, stable_auto_contrast_color
from images_handle.proskurin import proskurin_photo_handle
from images_handle.grey_world import to_grey_world


# цвет для ошибок
def handle_error(text):
    return "\n" + Fore.WHITE + Back.BLACK + text + "\n" + Style.RESET_ALL


# типы операций
types_of_operations = [
    "1.\tHandle of Proskurin's photos",
    "2.\tMake 'Grey world' handle of photo",
    "3.\tMake contrast photo",
    "4.\tConvert color photo to grey photo",
    "0.\tExit"
]


while True:
    print("Choice the type of handle:\n")
    for operation in types_of_operations:
        print(operation)

    try:
        user_input = int(input())
        if user_input not in range(len(types_of_operations)):
            raise Exception(handle_error(f"You should input integer value between 0 and {len(types_of_operations) - 1}"))

    except ValueError:
        print(handle_error("You should input integer value"))
        continue

    except Exception as err:
        print(err)
        continue

    else:
        photo_path = input("Input path to file: ")
        image = None

        if user_input == 1:
            image, coord = proskurin_photo_handle(photo_path)

        elif user_input == 2:
            image = to_grey_world(photo_path)

        elif user_input == 3:
            print("\t\t(1) Color photo")
            print("\t\t(2) Black-white photo")

            user_choice = int(input())

            if user_choice == 1:
                image = stable_auto_contrast_color(photo_path)

            elif user_choice == 2:
                image = stable_auto_contrast_grey(photo_path)

        elif user_input == 4:
            image = from_color_to_grey(photo_path)

        elif user_input == 0:
            print("Bye")
            break

        imshow(image)
        plt.show()

        continue_answer = input("Continue? y/n ")

        if continue_answer == "y" or continue_answer == "yes":
            continue

        elif continue_answer == "n" or continue_answer == "no":
            print("Bye")
            break

        else:
            print("What?")

# HANDLE PHOTOS # 
#
#


#### INSTALL
#
##### I. For pushing this project you should enter:
`git clone git@github.com:slovenberg/handle_photoes.git . `
##### II. For installing packages you should enter next command in the root of project:
`pip install -r requirements.txt`
#
#### ARCHITECTURE
Directory consist from:
* settings.py - import all required packages
* test_path.py - import all necessary variables and functions
* user.py - test all functions in single program
* original/ - directory with original photos for tests
* finite/ - directory with finite photos after handle
* common_functions/ - directory for correct working some functions
* proskurin_photo/
* image_handle/ - files with general functions
    * color_to_grey.py
    * grey_world.py
    * make_contrast.py
    * proskurin.py
* requirements.py - install packages
#
#### USING
For using you should write next commands at the start of file:
```shell script
from settings import *
from test_paths import *
```
#
#### On this moment you can use several types of changing photos:
| Package | Function | 
| ------- | -------- |
| images_handle.color_to_grey | from_color_to_grey() |
| images_handle.make_contrast | stable_auto_contrast_grey() |
| images_handle.make_contrast | stable_auto_contrast_color() |
| images_handle.proskurin | proskurin_photo_handle() |
| images_handle | proskurin_photo_handle() |


[original_grey_world]: pictures_for_readme/not_grey_world_color.png
[original_color]: pictures_for_readme/tiger_color.png
[original_color]: pictures_for_readme/not_grey_world_color.png
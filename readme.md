To start app, just run main.py file

Instruction:
Use button "загрузить изображение", to select the folder with images (you can use mine that names img). 
Than select one of images in the left sidebar. You can first add this picture of person to database (button "добавить личность в базу") or immediately check if person is already exist in database (button "совершить поиск по базе"). You can check both by name and photo.



if there is an error with installing module dlib, you can try this command: conda install -c conda-forge dlib. Or if you don`t have conda, than:
Download the dlib binary suitable for your version of Python and Windows from the official website (https://pypi.org/project/dlib/#files) or from an external source, such as Christoph Gohlke's repository.
Install it using pip, specifying the path to the downloaded file:
pip install <path_to_downloaded_wheel_file>

**Note: in this app, for training purposes, when you add photo to database you add exactly photo but in binary form. In correct way, application should add only path to picture because this way is more faster. 

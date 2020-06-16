import os


if os.name == 'posix':
	DIR_SEP = '/'
	SRC_DIR = '/storage/emulated/0/Download'
	PYTHON_FILE_DST = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/Pygame/cartesian_axes'
	TEST_FILE_DST = PYTHON_FILE_DST + '/test'
	IMG_FILE_DST = PYTHON_FILE_DST + '/image'
	DOC_FILE_DST = PYTHON_FILE_DST + '/doc'	
else:
	# Windows
	DIR_SEP = '\\'
	SRC_DIR = 'D:\\Users\\Jean-Pierre\\Downloads'
	PYTHON_FILE_DST = 'D:\\Development\\Python\\Pygame_2d_Cartesian_coordinates_system'
	TEST_FILE_DST = PYTHON_FILE_DST + '\\test'
	IMG_FILE_DST = PYTHON_FILE_DST + '\\image'
	DOC_FILE_DST = PYTHON_FILE_DST + '\\doc'

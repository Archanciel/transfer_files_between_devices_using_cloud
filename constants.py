import os


if os.name == 'posix':
	DIR_SEP = '/'
	BASE_DST_FILE_DIR = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/'
	TEST_SUB_DIR = '/test'
	IMG_SUB_DIR = '/images'
	DOC_SUB_DIR = '/doc'	
else:
	# Windows
	DIR_SEP = '\\'
	BASE_DST_FILE_DIR = 'D:\\Development\\Python'
	TEST_SUB_DIR = '\\test'
	IMG_SUB_DIR = '\\images'
	DOC_SUB_DIR = '\\doc'

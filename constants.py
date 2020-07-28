import os

VERSION_NUMBER = 1.1
DATE_TIME_FORMAT_CONFIG_FILE = '%Y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT_USER_INPUT = '%y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT_USER_INPUT_SHORT = '%y-%m-%d'

if os.name == 'posix':
	DIR_SEP = '/'
	CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
else:
	# Windows
	DIR_SEP = '\\'
	CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'

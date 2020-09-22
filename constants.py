import os

VERSION_NUMBER = 1.3
DATE_TIME_FORMAT_CONFIG_FILE = '%d/%m/%Y %H:%M:%S'
DATE_TIME_FORMAT_USER_INPUT = '%d/%m/%y %H:%M:%S'
DATE_TIME_FORMAT_USER_INPUT_SHORT = '%d/%m/%y'

if os.name == 'posix':
	DIR_SEP = '/'
	CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
else:
	# Windows
	DIR_SEP = '\\'
	CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'

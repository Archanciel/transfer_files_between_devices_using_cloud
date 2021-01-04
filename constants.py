import os

VERSION_NUMBER = 2.2
DATE_TIME_FORMAT_CONFIG_FILE = '%d/%m/%Y %H:%M:%S'
DATE_TIME_FORMAT_USER_INPUT = '%d/%m/%y %H:%M:%S'
DATE_TIME_FORMAT_USER_INPUT_SHORT = '%d/%m/%y'

if os.name == 'posix':
	CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
else:
	# Windows
	CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'

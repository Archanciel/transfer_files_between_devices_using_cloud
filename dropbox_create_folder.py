import os, io, dropbox

from configmanager import ConfigManager

if os.name == 'posix':
	CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
else:
	CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'
	
def createEmptyFolder(dropboxBaseFolder, newFolder):
	# creating a temp dummy destination file path
	dummyFileTo = dropboxBaseFolder + newFolder + '/' + 'temp.bin'

	# creating a virtual in-memory binary file
	f = io.BytesIO(b"\x00")

	# uploading the dummy file in order to create the containing folder		
	dbx.files_upload(f.read(), dummyFileTo)
	
	# now that the folder is created, delete the dummy file	
	dbx.files_delete_v2(dummyFileTo)

cm = ConfigManager(CONFIG_FILE_PATH_NAME)
access_token = cm.dropboxApiKey
dbx = dropbox.Dropbox(access_token)

dropboxBaseDir = '/test_dropbox'
dropboxNewSubDir = '/new_empty_sub_dir'

createEmptyFolder(dropboxBaseDir, dropboxNewSubDir)
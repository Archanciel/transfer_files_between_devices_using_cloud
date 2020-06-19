import os
import dropbox
from configmanager import ConfigManager

if os.name == 'posix':
	CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
else:
	CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'
	
cm = ConfigManager(CONFIG_FILE_PATH_NAME)
access_token = cm.dropboxApiKey
dbx = dropbox.Dropbox(access_token)

local_directory = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/tempdir'
dropboxDestDir = '/test_dropbox'

upload_entry_list = []

for root, dirs, files in os.walk(local_directory):
	for fileName in files:
		# construct the full local path
		local_file_path = os.path.join(root, fileName)
		f = open(local_file_path, 'rb')
		upload_session_start_result = dbx.files_upload_session_start(f.read(), close=True) # assuming small files
		cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                               offset=f.tell())
		commit = dropbox.files.CommitInfo(path=dropboxDestDir + "/{}".format(fileName))
		upload_entry_list.append(dropbox.files.UploadSessionFinishArg(cursor=cursor, commit=commit))

print('Uploaded files\n')

for uploadSessionFinishArg in upload_entry_list:
	print(uploadSessionFinishArg.commit.path)

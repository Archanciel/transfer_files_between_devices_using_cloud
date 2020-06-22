import os, io, dropbox

from constants import DIR_SEP
from configmanager import ConfigManager

class TransferData:
	def __init__(self, access_token):
		self.dbx = dropbox.Dropbox(access_token)

	def upload_file(self, file_from, file_to):
		"""
		Uploads a file to Dropbox using API v2. Warning: if the uploaded
		file already exists in the Dropbox destination dir, the upload
		will fail if the file is different from the initially uploaded
		file !
		"""

		with open(file_from, 'rb') as f:
			self.dbx.files_upload(f.read(), file_to)

	def download_file(self, file_from, file_to):
		with open(file_to, "wb") as f:
			metadata, res = self.dbx.files_download(path=file_from)
			f.write(res.content)
			print(metadata.name + ' downloaded')

	def delete_file(self, file):
		self.dbx.files_delete_v2(file)

	def create_folder(self, dropboxBaseFolder, newFolder):
		# creating a temp dummy destination file path
		dummyFileTo = dropboxBaseFolder + newFolder + '/' + 'temp.bin'

		# creating a virtual in-memory binary file
		f = io.BytesIO(b"\x00")

		# uploading the dummy file in order to create the containing folder
		self.dbx.files_upload(f.read(), dummyFileTo)

		# now that the folder is created, delete the dummy file
		self.dbx.files_delete(dummyFileTo)

	def list_files(self, dropboxDir):
		fileListMetaData = self.dbx.files_list_folder(path=dropboxDir)
		for fileMetaData in fileListMetaData.entries:
			print(fileMetaData.name)

def main():
	if os.name == 'posix':
		CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
	else:
		CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'

	cm = ConfigManager(CONFIG_FILE_PATH_NAME)
	access_token = cm.dropboxApiKey
	transferData = TransferData(access_token)
	dropboxDir = '/test_dropbox'
	#dropboxDir = '/test_dropbox/batch_explore'
	file_from = 'configmanager.py'
	file_to = dropboxDir +'/configmanager.py'  # The full path to upload the file to, including the file name

	# API v2
	transferData.upload_file(file_from, file_to)
	
	print('\nList files after upload\n')
	transferData.list_files(dropboxDir)
	#input('Downloading ')
	file_from = dropboxDir + '/configmanager.py' # The full path of the file to download, including the file name
	file_to = cm.downloadPath + DIR_SEP + 'configmanager_downloaded.py'
	transferData.download_file(file_from, file_to)

	# deleting file so a new version can be upladed without error
	transferData.delete_file(file_from)
	print('\nList files after delete\n')
	transferData.list_files(dropboxDir)
	print('\nList files in dropbox dir /not exist. Raises exception\n')
	
	try:
		transferData.list_files(dropboxDir + '/not_exist')
	except Exception as e:
		print(str(e))
	
	transferData.create_folder(dropboxDir, '/not_exist')
	
	print('\nnow list files after /not_exist was created. Will not raise exception.')
	transferData.list_files(dropboxDir + '/not_exist')
	
	print('\nnow deleting the newly created folder.')
	
	# now, deleting the created folder
	transferData.delete_file(dropboxDir + '/not_exist')
	
	print('\nList files in dropbox dir /not exist which was deleted. Raises exception\n')
	
	try:
		transferData.list_files(dropboxDir + '/not_exist')
	except Exception as e:
		print(str(e))
	

if __name__ == '__main__':
	main()

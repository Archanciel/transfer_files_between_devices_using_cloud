import os, dropbox

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
		self.dbx.files_delete(file)
		
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
	file_from = 'configmanager.py'
	file_to = dropboxDir +'/configmanager.py'  # The full path to upload the file to, including the file name

	# API v2
	transferData.upload_file(file_from, file_to)
	
	print('\nList files after upload\n')
	transferData.list_files(dropboxDir)

	file_from = dropboxDir + '/configmanager.py' # The full path of the file to download, including the file name
	file_to = 'configmanager_downloaded.py'
	transferData.download_file(file_from, file_to)

	# deleting file so a new version can be upladed without error
	transferData.delete_file(file_from)
	print('\nList files after delete\n')
	transferData.list_files(dropboxDir)

if __name__ == '__main__':
	main()

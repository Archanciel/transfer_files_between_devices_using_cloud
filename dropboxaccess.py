import dropbox

from cloudaccess import CloudAccess
from configmanager import ConfigManager

class DropboxAccess(CloudAccess):
	def __init__(self, configManager):
		super().__init__()
		accessToken = configManager.dropboxApiKey
		self.dbx = dropbox.Dropbox(accessToken)

	def uploadFiles(self, file_from, file_to):
		"""
		Uploads a file to Dropbox using API v2. Warning: if the uploaded
		file already exists in the Dropbox destination dir, the upload
		will fail if the file is different from the initially uploaded
		file !
		"""

		with open(file_from, 'rb') as f:
			self.dbx.files_upload(f.read(), file_to)

	def downloadFiles(self, file_from, file_to):
		with open(file_to, "wb") as f:
			metadata, res = self.dbx.files_download(path=file_from)
			f.write(res.content)
			print(metadata)

	def deleteFiles(self, file):
		self.dbx.files_delete(file)

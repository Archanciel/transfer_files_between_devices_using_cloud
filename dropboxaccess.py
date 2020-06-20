import dropbox

from cloudaccess import CloudAccess
from configmanager import ConfigManager

class DropboxAccess(CloudAccess):
	def __init__(self, configManager, projectName):
		super().__init__(configManager.dropboxBaseDir, projectName)
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
		
	def getCloudFileList(self):
		fileNameLst = []
		fileListMetaData = None
		
		try:			
			fileListMetaData = self.dbx.files_list_folder(path=self.cloudTransferDir)
		except dropbox.exceptions.ApiError as e:
			if isinstance(e.error, dropbox.files.ListFolderError):
				raise NotADirectoryError("Dropbox directory {} does not exist".format(self.cloudTransferDir))
			
		for fileMetaData in fileListMetaData.entries:
			fileNameLst.append(fileMetaData.name)
			
		return fileNameLst
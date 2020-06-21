import io, dropbox

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

	def deleteFile(self, file):
		self.dbx.files_delete_v2(file)

	def deleteFolder(self, folder):
		self.dbx.files_delete_v2(self.cloudTransferDir + '/' + folder)

	def deleteProjectFolder(self):
		self.dbx.files_delete_v2(self.cloudTransferDir)

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

	def createEmptyFolder(self, folderName):
		# ensuring folderName does not contain / 		
		folderName = folderName.replace('/', '')
		
		# creating a temp dummy destination file path
		dummyFileTo = self.cloudTransferDir + '/' + folderName + '/' + 'temp.bin'

		# creating a virtual in-memory binary file
		f = io.BytesIO(b"\x00")

		# uploading the dummy file in order to create the containing folder		
		self.dbx.files_upload(f.read(), dummyFileTo)
	
		# now that the folder is created, delete the dummy file	
		self.dbx.files_delete_v2(dummyFileTo)

	def createProjectFolder(self):
		# creating a temp dummy destination file path
		dummyFileTo = self.cloudTransferDir + '/temp.bin'

		# creating a virtual in-memory binary file
		f = io.BytesIO(b"\x00")

		# uploading the dummy file in order to create the containing folder
		self.dbx.files_upload(f.read(), dummyFileTo)

		# now that the folder is created, delete the dummy file
		self.dbx.files_delete_v2(dummyFileTo)

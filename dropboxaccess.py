import io, dropbox

from constants import DIR_SEP
from cloudaccess import CloudAccess
from configmanager import ConfigManager

class DropboxAccess(CloudAccess):
	def __init__(self, configManager, projectName):
		super().__init__(configManager.dropboxBaseDir, projectName)
		accessToken = configManager.dropboxApiKey
		self.dbx = dropbox.Dropbox(accessToken)

	def uploadFile(self, localFilePathName):
		"""
		Uploads a file to Dropbox using API v2. to avoid a conflict error if
		the file already exists on the cloud, the mode is set to 
		dropbox.files.WriteMode.overwrite.

		@param localFilePathName:
		"""
		cloudFilePathName = self.cloudTransferDir + '/' + localFilePathName.split(DIR_SEP)[-1]

		with open(localFilePathName, 'rb') as f:
			self.dbx.files_upload(f.read(), cloudFilePathName, mode=dropbox.files.WriteMode.overwrite)

	def downloadFile(self, cloudFileName, destFilePathName):
		"""

		@param cloudFileName:
		@param destFilePathName:
		"""
		cloudFilePathName = self.cloudTransferDir + '/' + cloudFileName

		with open(destFilePathName, "wb") as f:
			metadata, res = self.dbx.files_download(path=cloudFilePathName)
			f.write(res.content)

	def deleteFile(self, fileName):
		"""

		@param fileName:
		"""
		cloudFilePathName = self.cloudTransferDir + '/' + fileName
		self.dbx.files_delete_v2(cloudFilePathName)

	def deleteFolder(self, folder):
		"""

		@param folder:
		"""
		self.dbx.files_delete_v2(self.cloudTransferDir + '/' + folder)

	def deleteProjectFolder(self):
		"""

		"""
		self.dbx.files_delete_v2(self.cloudTransferDir)

	def getCloudFileList(self):
		"""

		@return:
		"""
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
		"""

		@param folderName:
		"""
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
		"""

		"""
		# creating a temp dummy destination file path
		dummyFileTo = self.cloudTransferDir + '/temp.bin'

		# creating a virtual in-memory binary file
		f = io.BytesIO(b"\x00")

		# uploading the dummy file in order to create the containing folder
		self.dbx.files_upload(f.read(), dummyFileTo)

		# now that the folder is created, delete the dummy file
		self.dbx.files_delete_v2(dummyFileTo)

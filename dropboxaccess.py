import io, dropbox

from constants import DIR_SEP
from cloudaccess import CloudAccess
from configmanager import ConfigManager

class DropboxAccess(CloudAccess):
	def __init__(self, configManager, projectName):
		super().__init__(configManager.dropboxBaseDir, projectName)
		accessToken = configManager.dropboxApiKey
		self.dbx = dropbox.Dropbox(accessToken)

	def uploadFileName(self, localFilePathName):
		"""
		Uploads a file ignoring its path component to the project folder on Dropbox
		using API v2.

		To avoid a conflict error if the file already exists on the cloud, the 
		mode is set to dropbox.files.WriteMode.overwrite.

		@param localFilePathName: file path name of file to upload
		"""
		cloudFilePathName = self.cloudProjectDir + '/' + localFilePathName.split(DIR_SEP)[-1]

		with open(localFilePathName, 'rb') as f:
			self.dbx.files_upload(f.read(), cloudFilePathName, mode=dropbox.files.WriteMode.overwrite)

	def uploadFilePathName(self, localFilePathName, localProjectDir):
		"""
		Uploads a file keeping its path component to the project folder on Dropbox
		using API v2.

		To avoid a conflict error if the file already exists on the cloud, the
		mode is set to dropbox.files.WriteMode.overwrite.

		@param localFilePathName: file path name of file to upload
		"""
		localProjectDir = localProjectDir + DIR_SEP
		filePathName = localFilePathName.replace(localProjectDir, '')
		filePathName = filePathName.replace('\\', '/')
		cloudFilePathName = self.cloudProjectDir + '/' + filePathName

		with open(localFilePathName, 'rb') as f:
			self.dbx.files_upload(f.read(), cloudFilePathName, mode=dropbox.files.WriteMode.overwrite)

	def downloadFile(self, cloudFileName, destFilePathName):
		"""
		Downloads the file whose name is cloudFileName to the passed destination 
		path name.
		
		@param cloudFileName: name of file to download
		@param destFilePathName: local directory in which the file will be
								 downloaded
		"""
		cloudFilePathName = self.cloudProjectDir + '/' + cloudFileName

		with open(destFilePathName, "wb") as f:
			metadata, res = self.dbx.files_download(path=cloudFilePathName)
			f.write(res.content)

	def deleteFile(self, fileName):
		"""
		Deletes the file whose name is fileName from the cloud project dir.
		
		@param fileName: name of file to remove from the cloud project dir
		"""
		cloudFilePathName = self.cloudProjectDir + '/' + fileName
		self.dbx.files_delete_v2(cloudFilePathName)

	def deleteProjectSubFolder(self, subFolderName):
		"""
		Deletes a sub directory of the project cloud directory. This method 
		is currently only used in unit tests.

		@param subFolder: name of the sub directory to remove from project 
						  cloud directory
		"""
		self.dbx.files_delete_v2(self.cloudProjectDir + '/' + subFolderName)

	def deleteProjectFolder(self):
		"""
		Deletes the cloud project directory. This method is currently only used
		in unit tests.
		"""
		self.dbx.files_delete_v2(self.cloudProjectDir)

	def getCloudFileNameList(self):
		"""
		Returns the list of file names of files contained in the cloud project 
		directory.
		
		@return: list of string file names
		"""
		fileNameLst = []
		fileListMetaData = None
		
		try:			
			fileListMetaData = self.dbx.files_list_folder(path=self.cloudProjectDir)
		except dropbox.exceptions.ApiError as e:
			if isinstance(e.error, dropbox.files.ListFolderError):
				raise NotADirectoryError("Dropbox directory {} does not exist".format(self.cloudProjectDir))
			
		for fileMetaData in fileListMetaData.entries:
			fileNameLst.append(fileMetaData.name)
			
		return fileNameLst

	def getCloudFilePathNameList(self):
		"""
		Returns the list of file path names of files contained in the cloud project
		directory.

		@return: list of string file names
		"""
		fileNameLst = []
		fileListMetaData = None

		try:
			fileListMetaData = self.dbx.files_list_folder(path=self.cloudProjectDir)
		except dropbox.exceptions.ApiError as e:
			if isinstance(e.error, dropbox.files.ListFolderError):
				raise NotADirectoryError("Dropbox directory {} does not exist".format(self.cloudProjectDir))

		for fileMetaData in fileListMetaData.entries:
			fileNameLst.append(fileMetaData.name)

		return fileNameLst

	def getCloudFilePathNameList(self):
		"""
		Returns the list of file names of files contained in the cloud project
		directory.

		@return: list of string file names
		"""
		fileNameLst = []
		fileListMetaData = None

		try:
			fileListMetaData = self.dbx.files_list_folder(path=self.cloudProjectDir, recursive=True)
		except dropbox.exceptions.ApiError as e:
			if isinstance(e.error, dropbox.files.ListFolderError):
				raise NotADirectoryError("Dropbox directory {} does not exist".format(self.cloudProjectDir))

		for fileMetaData in fileListMetaData.entries:
			fileNameLst.append(fileMetaData.name)

		return fileNameLst

	def createProjectSubFolder(self, subFolderName):
		"""
		Uses a multi step procedure to create an empty sub directory of
		the cloud project dir. This method is currently only used in unit 
		tests.

		@param subFolderName
		"""
		# ensuring subFolderName does not contain /
		subFolderName = subFolderName.replace('/', '')
		
		# creating a temp dummy destination file path
		dummyFileTo = self.cloudProjectDir + '/' + subFolderName + '/' + 'temp.bin'

		# creating a virtual in-memory binary file
		f = io.BytesIO(b"\x00")

		# uploading the dummy file in order to create the containing folder		
		self.dbx.files_upload(f.read(), dummyFileTo)
	
		# now that the folder is created, delete the dummy file	
		self.dbx.files_delete_v2(dummyFileTo)

	def createProjectFolder(self):
		"""
		Uses a multi step procedure to create an empty cloud project dir. This
		method is used when handling a new project added in the local configuration 
		file when this project does not yet have an existing cloud project dir.
		"""
		# creating a temp dummy destination file path
		dummyFileTo = self.cloudProjectDir + '/temp.bin'

		# creating a virtual in-memory binary file
		f = io.BytesIO(b"\x00")

		# uploading the dummy file in order to create the containing folder
		self.dbx.files_upload(f.read(), dummyFileTo)

		# now that the folder is created, delete the dummy file
		self.dbx.files_delete_v2(dummyFileTo)

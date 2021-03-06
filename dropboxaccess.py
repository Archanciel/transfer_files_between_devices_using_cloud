import os, io, dropbox
from os.path import sep

from cloudaccess import CloudAccess

class DropboxAccess(CloudAccess):
	def __init__(self, configManager, projectName):
		super().__init__(configManager.dropboxBaseDir, projectName, configManager.getProjectLocalDir(projectName) + sep)
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
		cloudFilePathName = self.cloudProjectDir + '/' + localFilePathName.split(sep)[-1]

		try:
			with open(localFilePathName, 'rb') as f:
				self.dbx.files_upload(f.read(), cloudFilePathName, mode=dropbox.files.WriteMode.overwrite)
		except dropbox.exceptions.ApiError as e:
			if isinstance(e.error, dropbox.files.UploadError):
				raise NameError()

	def uploadFilePathName(self, localFilePathName):
		"""
		Uploads a file keeping its path component to the project folder on Dropbox
		using API v2. Since the path of the file is kept, the structure of the
		cloud project sub directories will reproduce the structure of the local
		project sub directories.

		To avoid a conflict error if the file already exists on the cloud, the
		mode is set to dropbox.files.WriteMode.overwrite.

		@param localFilePathName: file path name of file to upload
		"""
		# keeping only the local project sub dir component
		filePathName = localFilePathName.replace(self.localProjectDir, '')
		
		if sep == '\\':
			# if run on Windows, replaces the Windows dir separator by the 
			# dropbox> dir separator
			filePathName = filePathName.replace('\\', '/')
			
		cloudFilePathName = self.cloudProjectDir + '/' + filePathName

		try:
			with open(localFilePathName, 'rb') as f:
				self.dbx.files_upload(f.read(), cloudFilePathName, mode=dropbox.files.WriteMode.overwrite)
		except dropbox.exceptions.ApiError as e:
			if isinstance(e.error, dropbox.files.UploadError):
				raise NameError()

	def downloadFile(self, cloudFileName, destFilePathName):
		"""
		Downloads the file whose name is cloudFileName to the passed destination 
		path name.
		
		@param cloudFileName: name of file to download
		@param destFilePathName: local directory in which the file will be
								 downloaded
		"""
		cloudFilePathName = self.cloudProjectDir + '/' + cloudFileName
		os.makedirs(os.path.dirname(destFilePathName), exist_ok=True)

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
			if hasattr(fileMetaData, 'is_downloadable'):
				# means the fileMetaData is for a file, not a directory
				fileNameLst.append(fileMetaData.name)
			
		return fileNameLst

	def getCloudFilePathNameList(self):
		"""
		Returns the list of file path names of files contained in the cloud project
		directory and sub-directories.

		@return: list of string file path names
		"""
		filePathNameLst = []
		fileListMetaData = None

		try:
			fileListMetaData = self.dbx.files_list_folder(path=self.cloudProjectDir, recursive=True)
		except dropbox.exceptions.ApiError as e:
			if isinstance(e.error, dropbox.files.ListFolderError):
				raise NotADirectoryError("Dropbox directory {} does not exist".format(self.cloudProjectDir))

		cloudProjectDir = self.cloudProjectDir + '/'

		for fileMetaData in fileListMetaData.entries:
			if hasattr(fileMetaData, 'is_downloadable'):
				# means the fileMetaData is for a file, not a directory
				filePathNameLst.append(fileMetaData.path_display.replace(cloudProjectDir, ''))

		return filePathNameLst

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

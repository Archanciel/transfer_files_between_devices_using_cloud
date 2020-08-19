from datetime import datetime
import requests

from constants import *
from requester import Requester
from configmanager import * 
from filelister import FileLister
from filemover import FileMover
from dropboxaccess import DropboxAccess

class TransferFiles:
	"""
	This is the main class of the TransferFiles utility.
	
	The TransferFiles utility is used to transfer files from one device to 
	another device using the cloud as intermediary location. What makes 
	TransferFiles unique is that the directory structures on both source and
	target devices can be different. A local configuration file (transfiles.ini)
	stores the information required for the transfer to be done correctly.
	"""
	def __init__(self, configFilePath=None, projectName=None):
		"""
			TransferFiles constructor.

		    @param configFilePath: used for unit testing only
		    @param projectName used for unit testing only
		"""
		if configFilePath == None:
			# we are not unit testing ...
			configFilePath = CONFIG_FILE_PATH_NAME
			
		self.configManager = ConfigManager(configFilePath)
		self.requester = Requester(self.configManager)
			
		if projectName == None:
			# we are not unit testing ...
			projectName = self.requester.getProjectName()
		
			if projectName == None:
				# user did choose Quit
				self.projectName = None
				return
			
		self.projectName = projectName
		self.localProjectDir = None

		try:
			self.localProjectDir = self.configManager.getProjectLocalDir(self.projectName)
		except KeyError as e:
			# this happens only when TransferFiles is launched from the command line
			# with an invalid project name passed as -p command line parm
			print('\nProject {} not defined in configuration file {}. Program closed.\n'.format(str(e), configFilePath))
			self.projectName = None
			return

		# currently, only Dropbox as cloud space is implemented
		self.cloudAccess = DropboxAccess(self.configManager, self.projectName)
		self.fileLister = FileLister(self.configManager)

	def transferFiles(self):
		"""
		This is the main TransferFiles method. Depending on the content of the
		cloud space for the current project, the user is prompted for uploading
		files modified locally or for downloading and transferring to the right
		local dirs of the files contained on the cloud.
		"""
		if self.projectName == None:
			# user did choose Quit
			return
			
		cloudFileLst = []

		try:
			if self.configManager.isProjectSubDirSynchronized(self.projectName):
				cloudFileLst = self.cloudAccess.getCloudFilePathNameList()
			else:
				cloudFileLst = self.cloudAccess.getCloudFileNameList()
		except NotADirectoryError as e:
			# means that the cloud project directory does not yet exist
			if self.requester.getCreateCloudFolderConfirmation(self.projectName):
				self.cloudAccess.createProjectFolder()
			else:
				return 

		if cloudFileLst == []:
			# if the cloud directory is empty, this means that we are in the state of uploading
			# to the cloud the files modified on the current device so that they will be available
			# to be transferred from the cloud to the local directories on the other device.
			self.uploadModifiedFilesToCloud()
		else:
			# if the cloud directory contains files, this means that we are in the state of transferring
			# those files to the current device. The transferred files will be downloaded to the
			# local download dir and deleted from the cloud. They will then be moved from the download
			# dir to the correct project dir and sub dirs.
			self.transferFilesFromCloudToLocalDirs(cloudFileLst)

	def transferFilesFromCloudToLocalDirs(self, cloudFileLst):
		"""
		This method first ask the user to confirm the download and transfer of
		the files available on the cloud. If the user refuses the download, he
		will be asked if he wants instead to upload files modified locally
		provided that local files exist whose modification date is after
		the last update date stored in the local configuration file.
		
		If the user confirms the download, the cloud files are downloaded to
		the local download dir and then deleted from the cloud. Then, the
		files are moved from the download dir to the correct project dir and
		sub-dirs, using the information specified in the download section of
		the project in the local configuration file.
		
		Finally, the last synch date is updated to now in the local configuration
		file.
		
		But the user may be nn the situation where he uploaded some modified files
		and then modified some uploaded files again or changed new files. In this
		case, he does not accept the download and will then be prompted for
		uploading the new modified files.
		
		@param cloudFileLst: contains the list of file names for the files
							 available on the cloud
		"""
		localProjectDirShort = DIR_SEP.join(self.localProjectDir.split(DIR_SEP)[-3:])

		questionStr = 'vvv {} files will be transferred from the cloud and then moved to the correct dir and sub-dir of {}.\nIf you want to upload new modified files instead, type N'.format(
			len(cloudFileLst), localProjectDirShort)
		doDownload, _ = self.requester.getUserConfirmation(questionStr, cloudFileLst)

		if doDownload:
			if self.configManager.isProjectSubDirSynchronized(self.projectName):
				# downloading the files from the cloud keeping their path component
				# directly to their final destination dir, the local project dir

				print('')  # empty line
				self.downloadAndDeleteFilesFromCloud(downloadPath=self.localProjectDir, cloudFileLst=cloudFileLst, targetName='directly to project')
				print('')  # empty line
			else:
				# downloading the files which have no path component from the cloud
				# to the download path and then moving them from the download path
 				# according to the sub dir parameters defined in the configuration
				# file for the project

				print('')  # empty line
				self.downloadAndDeleteFilesFromCloud(downloadPath=self.configManager.downloadPath, cloudFileLst=cloudFileLst, targetName='to download')
				print('')  # empty line

				# moving file from download dir to project dest dir and sub-dirs
				# according to the sub dir parameters defined in the configuration
				# file for the project

				fileMover = FileMover(self.configManager, self.projectName)
				fileMover.moveFilesToLocalDirs(cloudFileLst)

			# updating last synch time for the project in the local config file
			self.updateLastSynchTime()
		else:
			# lists modified local files and asks if they should be uploaded. Handles
			# the case where you did an upload and then modified files again on the
			# same device and want to add those files to the cloud
			self.uploadModifiedFilesToCloud()

	def uploadModifiedFilesToCloud(self):
		"""
		This method first obtain the list of local files whose modification date
		is after the last update date stored in the local configuration file.
		
		If this list is not empty, an upload confirmation is asked to the user.
		
		At this stage, the user has several choices: he can confirm the upload,
		he can ask to display a more detailed list showing the path of the
		modified files or he can decide to update the the last update date stored
		in the local configuration file so that the next time the program is
		executed, the list of modified files will be different.
		
		If the user confirms the upload, the modified files are uploaded to the
		cloud in the cloud dir specific to the project (having the same name
		than the project name) and the last update date stored in the local
		configuration file is set to now.
		
		In case no files were modified locally, we give the user the possibility
		to modify the last synch time. This can be useful if the user wants to
		move backward the last synch time in order to upload local files he
		modified during the last hours ...
		"""
		updatedFileNameLst, updatedFilePathNameLst, lastSyncTimeStr = self.fileLister.getModifiedFileLst(self.projectName)
		
		if updatedFileNameLst != []:
			if self.configManager.isProjectSubDirSynchronized(self.projectName):
				questionStr = '^^^ {} files were modified locally after {}\nand will be uploaded to the cloud, keeping the file path information.\nChoose P to display the path or U to update the last sync time'.format(
					len(updatedFileNameLst), lastSyncTimeStr)
			else:
				questionStr = '^^^ {} files were modified locally after {}\nand will be uploaded to the cloud.\nChoose P to display the path or U to update the last sync time'.format(
					len(updatedFileNameLst), lastSyncTimeStr)

			doUpload, lastSynchTimeChoice = self.requester.getUserConfirmation(questionStr, updatedFileNameLst, updatedFilePathNameLst)

			if doUpload: 
				print('')  # empty line
				if self.configManager.isProjectSubDirSynchronized(self.projectName):
					self.pathUploadToCloud(updatedFilePathNameLst)
				else:
					self.uploadToCloud(updatedFilePathNameLst)
			else:
				self.handleLastSynchTimeChoice(lastSynchTimeChoice)
		else:
			# here, neither modified files upload nor cloud files download is adequate. Instead
			# of simply closing the utility, we give the user the possibility to update the last 
			# synch time
			questionStr = 'No files modified locally since last sync time {}.\nChoose U to update the last sync time, Q or Enter to quit.'.format(lastSyncTimeStr)
			_, lastSynchTimeChoice = self.requester.getUserConfirmation(questionStr, updatedFileNameLst, updatedFilePathNameLst)
			self.handleLastSynchTimeChoice(lastSynchTimeChoice)

	def handleLastSynchTimeChoice(self, lastSynchTimeChoice):
		if lastSynchTimeChoice == '':
			# the user did choose not to upload anything and to leave the last sync
			# time unchanged
			return
		elif lastSynchTimeChoice == 'N':
			# the user did choose to update the last sync time to current time (now)
			self.updateLastSynchTime()
		else:
			# the user did enter a last sync time manually
			self.updateLastSynchTime(lastSynchTimeChoice)

	def uploadToCloud(self, updatedFilePathNameLst):
		"""
		Physically uploads the files contained in updatedFilePathNameLst to
		the cloud and sets the last update date stored in the configuration file
		to now. All the files are uploaded in the project cloud root dir.
		
		@param updatedFilePathNameLst: list of file path names to upload
		"""
		for localFilePathName in updatedFilePathNameLst:
			printFileName = localFilePathName.split(DIR_SEP)[-1]
			print('Uploading {} to the cloud ...'.format(printFileName))

			try:
				self.cloudAccess.uploadFileName(localFilePathName)
			except NameError as e:
				print('\tUploading {} failed. Possible cause: invalid file name ...'.format(printFileName))

		# updating last synch time for the project in config file
		self.updateLastSynchTime()

	def pathUploadToCloud(self, updatedFilePathNameLst):
		"""
		Physically uploads the files contained in updatedFilePathNameLst, creating
		project sub dirs on the cloud project dir and uploading the files in their
		correct sub dir. Then, the method sets the last update date stored in the
		configuration file to now.
		
		@param updatedFilePathNameLst: list of file path names to upload
		"""
		for localFilePathName in updatedFilePathNameLst:
			filePathNameElementLst = localFilePathName.split(DIR_SEP)[-4:]
			printFilePathName = DIR_SEP.join(filePathNameElementLst)
			print('Uploading {} to the cloud ...'.format(printFilePathName))

			try:
				self.cloudAccess.uploadFilePathName(localFilePathName)
			except NameError as e:
				print('\tUploading {} failed. Possible cause: invalid file name ...'.format(printFilePathName))

		# updating last synch time for the project in config file
		self.updateLastSynchTime()

	def updateLastSynchTime(self, userInpuLlastSynchTimeStr=''):
		"""
		If the passed lastSynchTimeStr is empty, sets the last update date
		stored in the configuration file to now. Else, if the user specified
		a synch date, validates it before setting it in the config file.
		
		@param userInpuLlastSynchTimeStr last synch time string as defined
										 manually by the user
		"""
		if userInpuLlastSynchTimeStr == '':
			validSynchTimeStr = datetime.now().strftime(DATE_TIME_FORMAT_CONFIG_FILE)
		else:
			isValid, validSynchTimeStr = self.validateLastSynchTimeStr(userInpuLlastSynchTimeStr)

			if not isValid:
				print('\nSynch time format invalid {}. Nothing changed.'.format(userInpuLlastSynchTimeStr))

				return

		self.configManager.updateLastSynchTime(self.projectName, validSynchTimeStr)
		print('\nUpdated last synch time to ' + validSynchTimeStr)

	def validateLastSynchTimeStr(self, userInputLastSynchTimeStr):
		try:
			dateTimeMod = datetime.strptime(userInputLastSynchTimeStr, DATE_TIME_FORMAT_USER_INPUT)
			return True, dateTimeMod.strftime(DATE_TIME_FORMAT_CONFIG_FILE)
		except ValueError:
			try:
				dateTimeMod = datetime.strptime(userInputLastSynchTimeStr, DATE_TIME_FORMAT_USER_INPUT_SHORT)
				return True, dateTimeMod.strftime(DATE_TIME_FORMAT_CONFIG_FILE)
			except ValueError:
				return False, ''
		
	def downloadAndDeleteFilesFromCloud(self, downloadPath, cloudFileLst, targetName):
		"""
		Physically downloads the files from the cloud and deletes them from
		the cloud.

		@param downloadPath: path to which the cloud files will be downloaded,
							 either the local download dir or directly to the
							 project dir and sub dirs
		@param cloudFileLst: list of files to transfer from the cloud. The list
							 contains either file names or file path names,
							 according to the value of the project
							 synchProjectSubDirStructure parm value as defined
							 in the configuration file
		@param targetName: 	 either 'download' or 'project', according to the value
							 of the project synchProjectSubDirStructure parm
							 value as defined
		"""
		for cloudFilePathName in cloudFileLst:
			destFilePathName = downloadPath + DIR_SEP + cloudFilePathName
			print('Transferring {} from the cloud {} dir ...'.format(cloudFilePathName, targetName))
			self.cloudAccess.downloadFile(cloudFilePathName, destFilePathName)
			self.cloudAccess.deleteFile(cloudFilePathName)

if __name__ == "__main__":
	tf = TransferFiles()

	try:
		tf.transferFiles()
	except requests.exceptions.ConnectionError:
		print("No internet access. Fix the problem and retry !")

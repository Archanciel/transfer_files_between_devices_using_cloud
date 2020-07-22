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
		self.downloadDir = self.configManager.downloadPath
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
		self.fileLister = FileLister(configManager=self.configManager)

	def transferFiles(self):
		"""
		This is the main TransferFiles method. Depending on the content of the
		cloud space for the current project, the user is prompted for uploading
		files modified locally or for downloading and transfering to the right
		local dirs of the files contained on the cloud.
		"""
		if self.projectName == None:
			# user did choose Quit
			return
			
		cloudFileLst = []

		try:
			cloudFileLst = self.cloudAccess.getCloudFileList()
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
		
		If the user confirms the download, the cloud files are dowloaded to
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
			print('')  # empty line
			self.downloadAndDeleteFilesFromCloud()
			print('')  # empty line

			# moving file from dowload dir to project dest dir and sub-dirs
			fileMover = FileMover(self.configManager, self.projectName)
			fileMover.moveFilesToLocalDirs()

			# updating last synch time for the project in the local config file
			self.updateLastSynchTime()
		else:
			# lists modified local files and asks if they should be uploaded. Handles
			# the case where you did an upload and then modified files again on the
			# same device and want to add those files to the cloud
			self.uploadModifiedFilesToCloud()

	def uploadModifiedFilesToCloud(self):
		"""
		This method first obtain the list of localfiles whose modification date
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
			questionStr = '^^^ {} files were modified locally after {}\nand will be uploaded to the cloud.\nChoose P to display the path or U to update the last sync time'.format(
				len(updatedFileNameLst), lastSyncTimeStr)
			doUpload, lastSynchTimeChoice = self.requester.getUserConfirmation(questionStr, updatedFileNameLst, updatedFilePathNameLst)

			if doUpload: 
				print('')  # empty line
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
		the cloud and sets the last update date stored in the 
		configuration file to now.
		
		@param updatedFilePathNameLst: list of file path names to upload
		"""
		for localFilePathName in updatedFilePathNameLst:
			print('Uploading {} to the cloud ...'.format(localFilePathName.split(DIR_SEP)[-1]))
			self.cloudAccess.uploadFile(localFilePathName)

		# updating last synch time for the project in config file
		self.updateLastSynchTime()

	def updateLastSynchTime(self, lastSynchTimeStr=''):
		"""
		If the passed lastSynchTimeStr is empty, sets the last update date
		stored in the configuration file to now. Else, if the user specifiej
		a synch date, validates it before settnng it in the config file.
		
		@param lastSynchTimeStr
		"""
		if lastSynchTimeStr == '':
			lastSynchTimeStr = datetime.now().strftime(DATE_TIME_FORMAT)
		elif not self.validateLastSynchTimeStr(lastSynchTimeStr):
			print('\nSynch time format invalid {}. Nothing changed.'.format(lastSynchTimeStr))

			return
		
		self.configManager.updateLastSynchTime(self.projectName, lastSynchTimeStr)
		print('\nUpdated last synch time to ' + lastSynchTimeStr)

	def validateLastSynchTimeStr(self, lastSynchTimeStr):
		try:
			datetime.strptime(lastSynchTimeStr, DATE_TIME_FORMAT)
			return True
		except ValueError:
			return False
		
	def downloadAndDeleteFilesFromCloud(self):
		"""
		Physically downloads the files from the cloud and deletes them from
		the cloud.
		"""
		cloudFileNameLst = self.cloudAccess.getCloudFileList()

		for fileName in cloudFileNameLst:
			destFileName = self.configManager.downloadPath + DIR_SEP + fileName
			print('Transferring {} from the cloud ...'.format(fileName))
			self.cloudAccess.downloadFile(fileName, destFileName)
			self.cloudAccess.deleteFile(fileName)

if __name__ == "__main__":
	tf = TransferFiles()

	try:
		tf.transferFiles()
	except requests.exceptions.ConnectionError:
		print("No internet access. Fix the problem and retry !")

import sys, argparse

from constants import *
from configmanager import ConfigManager

class Requester:
	def __init__(self, configManager):
		self.configManager = configManager
		
	def getProjectName(self, commandLineArgs=None):
		"""

		@param commandLineArgs: used for unit testing
		@return:
		"""
		if commandLineArgs == None:
			# we are not unit testing ...
			commandLineArgs = sys.argv[1:]

		if commandLineArgs != []:
			projectName = self.decodeCommandLineArgs(commandLineArgs)
		else:
			projectNameList = [x for x in self.configManager.projects]
			userPrompt = "Select project (Q to quit):\n\n"
			
			for (i, projectName) in enumerate(projectNameList): 
				userPrompt += str(i + 1) + ' ' + projectName + '\n'
				
			userPrompt += '\n'

			selection = '-1'
			projectName = ''

			while int(selection) <= 0:
				selection = input(userPrompt).upper()
				
				if selection == 'Q':
					return None
					
				try:
					if int(selection) <= 0:
						userPrompt = self.addErrorToUserPrompt(userPrompt)
					else:
						try:
							projectName = projectNameList[int(selection) - 1]
						except:
							userPrompt = self.addErrorToUserPrompt(userPrompt)
							selection = -1
				except ValueError as e:
					userPrompt = self.addErrorToUserPrompt(userPrompt)
					selection = -1
								
		return projectName

	def getCreateCloudFolderConfirmation(self, folderName):
		questionStr = 'Cloud project directory {} does not exist and will be created'.format(folderName)
		userPrompt = '\n' + questionStr + '.\n\nContinue (Y/N) '
		userChoice = input(userPrompt).upper()
		
		if userChoice == 'Y':
			return True
		else:
			return False
										
	def getUserConfirmation(self, questionStr, fileNameLst=[], filePathNameLst=[]):
		"""

		@param questionStr:
		@param fileNameLst:
		@param filePathNameLst:
		@return: True if user confims files upload and '' for new synch time
				 False if user cancels files upload and '' for new synch time
				 False and new synch time answer if user wants to update the
				 project synch time without uploading any file.
		"""
		if filePathNameLst != []:
			# this means that the method is called in order to upload files to
			# the cloud and not when asking to confirm downloading files from
			# the cloud. In this situation, it may be useful for the user to
			# see the path of the files which are candidates for upload, not
			# only their names.
			#
			# Additionally, the user has the possibility to update the last
			# synch time of the project.
			userPrompt = self.addFilesToUserPrompt(questionStr, fileNameLst, path='/P', upload='/U')
			userChoice = input(userPrompt).upper()
			
			if 'P' in userChoice:
				questionStr = questionStr.replace('P to display the path and ', '')	
				userPrompt = self.addFilesToUserPrompt(questionStr, filePathNameLst,path='', upload='/U')
			else:
				return self.handleUserChoice(userChoice)
		else:
			# here, we are prompting for downloading files from the cloud
			userPrompt = self.addFilesToUserPrompt(questionStr, fileNameLst)
		
		userChoice = input(userPrompt).upper()
					
		return self.handleUserChoice(userChoice)

	def handleUserChoice(self, userChoice):
		if 'U' in userChoice:
			return self.askUserNewSyncTime()
		elif userChoice == 'Y':
			return True, ''
		else:
			return False, ''
		
	def addFilesToUserPrompt(self, questionStr, fileNameLst, path='', upload=''):
		"""

		@param questionStr:
		@param fileNameLst:
		@param detail:
		@return:
		"""
		userPrompt = '\n'
				
		for fileName in fileNameLst:
			if DIR_SEP in fileName:
				# here, the file name is in fact a fuLl file path name. In order
				# to display a more readable file list, only the last 4 file
				# pathename element are kept
				filePathNameElementLst = fileName.split(DIR_SEP)[-4:]
				fileName = DIR_SEP.join(filePathNameElementLst)
 
			userPrompt += fileName + '\n'
						
		userPrompt += '\n' + questionStr + '.\n\nContinue (Y/N{}{}) '.format(path, upload)
					
		return userPrompt
	
	def addErrorToUserPrompt(self, userPrompt):
		"""

		@param userPrompt:
		@return:
		"""
		userPrompt = userPrompt.replace('Invalid selection. ', '')
		userPrompt = 'Invalid selection. ' + userPrompt
		
		return userPrompt
		
	def askUserNewSyncTime(self):
		userPrompt = '\nUpdating the project last synch time.\nType Enter to leave it unchanged, N to update it to Now and\nyyyy-mm-dd hh:mm:ss to fully specify the date '

		return False, input(userPrompt).upper()
				
	def decodeCommandLineArgs(self, argList):
		"""
		Uses argparse to acquire the user optional command line arguments.

		:param argList: were acquired from sys.argv or set by test code
		:return: document name (may be None), insertion point and image numbers list to add/insert
		"""
		parser = argparse.ArgumentParser(
			description="Version {}. The TransferFiles utility is used to transfer files from " \
						"one device to another device using the cloud as intermediary location. " \
						"What makes TransferFiles unique is that the directory structures on both " \
						"source target devices can be different. A local configuration file " \
						"(transfiles.ini) stores the information required for the transfer to " \
						"be done correctly. " \
						"TransferFiles can be used with or without command line parameters. " \
						"Without using the -p parameter to specify the project name (which " \
						"corresponds to the project section in " \
						"the configuration file), a menu listing the projects defined in the config " \
						"file is displayed in order for the user to select the project to which the " \
						"transfer is applied. ".format(VERSION_NUMBER)
		)

		parser.add_argument("-p", nargs="?", help="project name as defined in the configuration file.")

		args = parser.parse_args(argList)

		return args.p
		
if __name__ == "__main__":
	configManager = ConfigManager(CONFIG_FILE_PATH_NAME)
	rq = Requester(configManager)
	projectName = rq.getProjectName(None)
	print('\n' + projectName)

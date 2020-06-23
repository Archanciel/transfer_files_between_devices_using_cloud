import sys, argparse

from constants import *
from configmanager import ConfigManager

class Requester:
	def __init__(self, configManager):
		self.configManager = configManager
		
	def getProjectName(self, commandLineArgs):
		"""

		@param commandLineArgs:
		@return:
		"""
		if commandLineArgs == None:
			# we are not unit testing ...
			commandLineArgs = sys.argv[1:]

		project = self.decodeCommandLineArgs(commandLineArgs)
				
		if project == None:
			projectNameList = [x for x in self.configManager.projects]
			userPrompt = "Select project:\n\n"		
			
			for (i, projectName) in enumerate(projectNameList): 
				userPrompt += str(i + 1) + ' ' + projectName + '\n'
				
			userPrompt += '\n'

			selection = '-1'
			projectName = ''

			while int(selection) <= 0:
				selection = input(userPrompt)
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
				
	def getUserConfirmation(self, questionStr, fileNameLst=[], filePathNameLst=[]):
		"""

		@param questionStr:
		@param fileNameLst:
		@param filePathNameLst:
		@return:
		"""
		if filePathNameLst != []:
			# this means that the method is called in order to upload files to
			# the cloud an not when asking to confirm downloading files from
			# the cloud. In this situation, it may be useful for the user to
			# see the path of the files which are candidates for upload, not
			# only their names
			userPrompt = self.addFilesToUserPrompt(questionStr, fileNameLst, '/Detail')
			userChoice = input(userPrompt).upper()
			
			if 'D' in userChoice:	
				userPrompt = self.addFilesToUserPrompt(questionStr, filePathNameLst)
			elif userChoice == 'Y':
				return True
			else:
				return False
		else:
			userPrompt = self.addFilesToUserPrompt(questionStr, fileNameLst)
					
		if input(userPrompt).upper() == 'Y':	
			return  True
		else:
			return False

	def addFilesToUserPrompt(self, questionStr, fileNameLst, detail=''):
		"""

		@param questionStr:
		@param fileNameLst:
		@param detail:
		@return:
		"""
		userPrompt = '\n'
				
		for fileName in fileNameLst:
			if DIR_SEP in fileName:
				# here, the file name is in fact a fuL file path name. In order
				# to display a more readable file list, only the last 3 file
				# pathename element are kept
				filePathNameElementLst = fileName.split(DIR_SEP)[-3:]
				fileName = DIR_SEP.join(filePathNameElementLst)
 
			userPrompt += fileName + '\n'
						
		userPrompt += '\n' + questionStr + '. Continue (Y/N{}) '.format(detail)
					
		return userPrompt
	
	def addErrorToUserPrompt(self, userPrompt):
		"""

		@param userPrompt:
		@return:
		"""
		userPrompt = userPrompt.replace('Invalid selection. ', '')
		userPrompt = 'Invalid selection. ' + userPrompt
		return userPrompt

	def decodeCommandLineArgs(self, argList):
		"""
		Uses argparse to acquire the user optional command line arguments.

		:param argList: were acquired from sys.argv or set by test code
		:return: document name (may be None), insertion point and image numbers list to add/insert
		"""
		parser = argparse.ArgumentParser(
			description="Version {}. Adds or inserts all or part of the images contained in the current dir to a Word document. Each image " \
						"is added in a new paragraph. To facilitate further edition, the image " \
						"is preceded by a header line and followed by a bullet point section. " \
						"The images are added according to the ascending order of the number contained in their " \
						"file name. An error will occur if one of the image file name does not "
						"contain a number (valid image file names are: 1.jpg, image2.jpg, 3.png, ...). " \
						"If no document name is specified, the created document has " \
						"the same name as the containing dir. An existing document with " \
						"same name is never overwritten. Instead, a new document with a " \
						"name incremented by 1 (i.e. myDoc1.docx, myDoc2.docx, ...) " \
						"is created. " \
						"Using the utility in add mode, i.e. without specifying an insertion " \
						"point, creates a new document in which the specified images will be added. " \
						"If the current dir already contains a document with images and comments you " \
						"want to keep, use the insertion parameter which will insert the new images at " \
						"the specified position and preserve the initial content. " \
						"Without using the -p parameter, all the images of the current dir are collected " \
						"for the addition/insertion. -p enables to specify precisely the images to " \
						"add/insert using only the numbers contained in the image file names. ".format(VERSION_NUMBER)
		)
		parser.add_argument("-d", "--document", nargs="?", help="existing document to which the images are " \
																"to be added. For your convenience, the initial document is " \
																"not modified. Instead, the original document is copied with a " \
																"name incremented by one and the images are added/inserted to the copy.")
		parser.add_argument("-i", "--insertionPos", type=int, nargs="?",
							help="paragraph number BEFORE which to insert the " \
								 "images. 1 --> start of document (before paragraph 1). " \
								 "0 --> end of document. ")
		parser.add_argument("-p", "--pictures", nargs="*", help="numbers contained in the image file names which are selected " \
																"to be inserted in the existing document. Exemple: -p 1 8 4-6 9-10 or " \
																"-p 1,8, 4-6, 9-10 means the images whose name contain the specified numbers will be added or " \
																"or inserted in ascending number order, in this case 1, 4, 5, 6, 8, 9, 10. " \
																"If this parm is omitted, all the pictures in the curreent " \
																"dir are added or inserted. ")
		args = parser.parse_args(argList)

		return args.document
		
if __name__ == "__main__":
	configManager = ConfigManager(CONFIG_FILE_PATH_NAME)
	rq = Requester(configManager)
	projectName = rq.getProjectName(None)
	print('\n' + projectName)
		
import os, sys, argparse

from configmanager import ConfigManager 
from filelister import FileLister
from filemover import FileMover
from dropboxaccess import DropboxAccess

if os.name == 'posix':
	CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
else:
	CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'

VERSION_NUMBER = 0.1

class TransferFiles:
	def __init__(self, commandLineArgs):
		"""
		    :param commandLineArgs: used only for unit testing only
		"""
		if commandLineArgs == None:
			commandLineArgs = sys.argv[1:]

		userDocumentName, userInsertionPos, imageNumbersToAdd = self.getCommandLineArgs(commandLineArgs)

		configManager = ConfigManager(CONFIG_FILE_PATH_NAME)
		downLoadDir = configManager.downloadPath
		self.fileLister = FileLister(configManager=configManager, fromDir=downLoadDir)
		projectDir = configManager.projects['transFileCloudTestProject']['projectPath']
		self.fileMover = FileMover(configManager, downLoadDir, projectDir)
		self.cloudAccess = DropboxAccess(configManager)

	def getCommandLineArgs(self, argList):
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

		return args.document, args.insertionPos, args.pictures
		
if __name__ == "__main__":
	tf = TransferFiles(None)
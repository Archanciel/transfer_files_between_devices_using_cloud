import re

def convertWildcardExpToRegexpStr(wildcardExp):
	patternStr = wildcardExp.replace("\\", "\\\\")
	patternStr = patternStr.replace(".", "\.")
	patternStr = patternStr.replace("*", ".*")
	patternStr += "\Z"
	
	# no effect !
	# patternStr = "\A" + patternStr
	
	return patternStr

def tryWCExp(wildcardExp):
	patternStr = convertWildcardExpToRegexpStr(wildcardExp)
	print('wildcardExp ', wildcardExp)
	print('patternStr ', patternStr)
	pattern = re.compile(patternStr)
	l = ['testclass.py', 'testobj.pyc', '/excldir/subdir/*.*', '/excldir/subdir/testConvert.py', '/excldir/subdir/testConvert.pyc', 'd:\\excldir\\subdir\\test_Co21.py', 'd:\\excldir\\subdir\\test_Co21.pyc', 'd:\excldir\subdir\Test_Co22.py', 'd:\excldir\subdir\Test_Co22.pyc', 'd:\excldir\test_ALWAYS_USE_DOUBLE_BACKSLASH.py']

	print('\ntest strings:\n')
	
	for x in l:
		print(x)

	print('\nmatched string list:')
	print([x for x in l if pattern.match(x)])  
	print('\n')
	
wildcardExp = "test*.py"
tryWCExp(wildcardExp)

wildcardExp = "/excldir/subdir/*.py"
tryWCExp(wildcardExp)

wildcardExp = "/excldir/subdir/*.*"
tryWCExp(wildcardExp)

wildcardExp = "d:\\excldir\\subdir\\*.py"
tryWCExp(wildcardExp)

wildcardExp = "d:\\excldir\\subdir\\*.*"
tryWCExp(wildcardExp)

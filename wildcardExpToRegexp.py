import re

def convertWildcardExpToRegexpStr(wildcardExp):
	patternStr = wildcardExp.replace(".", "\.")
	patternStr = patternStr.replace("*", ".*")
	patternStr += "\Z"
	
	return patternStr

wildcardExp = "test*.py"
patternStr = convertWildcardExpToRegexpStr(wildcardExp)
print(patternStr)
#pattern = re.compile("test.*\.py\Z")
pattern = re.compile(patternStr)
l = ["testConvert.py", "test_Co21.py", "test_Co21.pyc"]
print([x for x in l if pattern.match(x)])  
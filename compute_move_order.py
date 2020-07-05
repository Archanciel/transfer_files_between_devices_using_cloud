import re

def convertWildcardExpToRegexpStr(wildcardExp):
	patternStr = wildcardExp.replace("\\", "\\\\")
	patternStr = patternStr.replace(".", "\.")
	patternStr = patternStr.replace("*", ".*")
	patternStr += "\Z"
	
	# no effect !
	# patternStr = "\A" + patternStr
	
	return patternStr

'''
wildchard1 = dir1
wildchard2 = dir2

if dir1 in dir2 and
pattern1 match wildchard2
	handle 2 before 1
'''
def computeMoveOrder(typeTupleOne, typeTupleTwo):
	wildchardOne, dirOne = typeTupleOne
	wildchardTwo, dirTwo = typeTupleTwo
	
	regexpOne = convertWildcardExpToRegexpStr(wildchardOne)
	patternOne = re.compile(regexpOne)
	
	if dirOne in dirTwo and \
		patternOne.match(wildchardTwo.replace("*", "a")):
		return typeTupleTwo, typeTupleOne
	else:
		return typeTupleOne, typeTupleTwo

print("\nOrder is important")
		
testTypeTuple = ("Test*.py", "/python/project/test")
pyTypeTuple = ("*.py", "/python/project")

print(computeMoveOrder(pyTypeTuple, testTypeTuple))
print(computeMoveOrder(testTypeTuple, pyTypeTuple))

print("\nOrder not important")
imgTypeTuple = ("*.jpg", "/python/project/images")
pyTypeTuple = ("*.py", "/python/project")

print(computeMoveOrder(pyTypeTuple, imgTypeTuple))
print(computeMoveOrder(imgTypeTuple, pyTypeTuple))

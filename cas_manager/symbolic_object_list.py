import symbolic_object

class symbolic_object_list:
	@classmethod
	def initialize(cls):
	    cls.symObjects = {}
	    #used to assign keys to new objects. It is only incremented, never decremented
	    cls.objKeyCounter = 1 

	@classmethod
	def addObject(cls, symObject):
		#NOTE: Shoule probably have code to detect duplicates here. But that could be too time consumning. Please decide.
	    cls.symObjects[cls.objKeyCounter] = symObject
	    print symObject
	    symObject.setKeyID(cls.objKeyCounter)
	    cls.objKeyCounter+=1

	@classmethod
	def addObjectWithLinks(cls, symObj, keyStr, srcObjs):
		cls.addObject(symObj)
		symObj.addInRelation(keyStr, srcObjs)
		for x in srcObjs:
			cls.symObjects[x].addOutRelation(keyStr, cls.objKeyCounter-1)

	@classmethod
	def getObj(cls, objKey):
	    return cls.symObjects[objKey]
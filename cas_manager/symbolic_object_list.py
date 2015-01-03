import pickle

import symbolic_object
from egebraServer import models

class symbolic_object_list:
	"""Static-like class that interfaces"""

	@classmethod
	def initialize(cls):
		"""Deprecated: Not required anymore, as a database is now used. Included to avoid some errors with previous code."""
		pass

	@classmethod
	def addObject(cls, symObject, notebookId):
	    """Add an object to the given notebook"""
	    #NOTE: Shoule probably have code to detect duplicates here. But that could be too time consumning. Please decide.
	    newObj = models.SymbolicObjects()
	    newObj.pklObj = ""
	    newObj.notebook = models.Notebooks.objects.filter(id=notebookId)[0]
	    newObj.save()
	    symObject.setKeyID(newObj.id)
	    models.SymbolicObjects.objects.filter(id=newObj.id).update(pklObj = pickle.dumps(symObject))


	@classmethod
	def addObjectWithLinks(cls, symObj, keyStr, srcObjs):
		"""Add an object with the specified links. All objects are reffered to with their keys which in Models is implemented as 'id'"""
		symObj.addInRelation(keyStr, srcObjs)
		cls.addObject(symObj)
		for x in srcObjs:
			y = cls.getObj(x)
			y.addOutRelation(keyStr, cls.objKeyCounter-1)
			models.SymbolicObjects.objects.filter(id = x).update(pklObj = pickle.dumps(y))

	@classmethod
	def getObj(cls, objKey):
		"""Get the object given the key."""
		return models.objects.filter(id=objKey)[0]
import cas_manager.symbolic_object
from cas_manager.symbolic_object_list import symbolic_object_list
import cas_manager.compute
import cas_manager.scheduler
import cas_manager.generic_cas_computations

computationScheduler = None
def initialize(compScheduler):
	global computationScheduler
	computationScheduler = compScheduler

def createSymbolicObject(symString, strType, dstNotebookId):
	assert(type(symString) is str)
	assert(type(strType) is str)
	symObj = cas_manager.symbolic_object.symbolicObject(symString, strType)
	symbolic_object_list.addObject(symObj, dstNotebookId)
	return symObj

def pushComputation(keyStr, symObjKeys, priority=0):
	assert(type(keyStr) is str)
	#assert(type(symObjKeys) is List)
	computationScheduler.scheduleComputation(keyStr, symObjKeys, priority)

def popResult():
	'''Returns any computed result if available. Returns None if no result is available'''
	if computationScheduler.pendingResults.empty():
		return None
	return computationScheduler.pendingResults.get()

def getPossibleComputations():
	return cas_manager.generic_cas_computations.getPossibleComputations()